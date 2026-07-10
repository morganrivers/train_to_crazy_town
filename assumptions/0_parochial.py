"""Assumption 0 — the parochial root worldview.

This is the BASE of every chain: the least-crazy assumptions (only my family and
local community count, in the present generation) plus the machinery every later
assumption modifies. At this stop there are no real reusable moral functions yet
— `moral_weight` says "people near me", `welfare_range` says "everyone I count
counts fully", and that is the whole theory. Later assumption files ADD new
functions (a discount rate, a suffering multiplier, a simulation probability),
REDEFINE these ones (wider circles, welfare-range tables), or CHANGE their
parameters — each producing a new worldview from the same slate.

Assumption files are never imported as modules; assumptions/worldviews.py
`exec`s them IN ORDER into one shared namespace, so a later file sees (and may
capture, wrap, or replace) everything the chain has defined so far.
"""

NAME = "parochial"
LABEL = "Parochial\ncommunity + nation"
EDGE_LABEL = None
FIGURES = ["common-sense default"]
REQUIRES = []
EXCLUDES = []
TERMINAL = False
DESC = (
    "Least-crazy end of the line. What matters is humans in my family and local "
    "community, in the present generation. Distant strangers, animals and the "
    "future are outside the circle (weight 0), so the local option wins. The "
    "soup kitchen's value is a worked BOTEC — people made happier per dollar "
    "times their wellbeing gain, netted against the counterfactual of the money "
    "sitting in a bank — and every worldview downstream imports that agreed "
    "number unchanged. The pre-EA commonsense baseline; no single EA figure "
    "defends it."
)

import math    # noqa: E402  (assumption files run via exec, in chain order)
import random  # noqa: E402

import botecs  # noqa: E402  (the empirical axis — one worked derivation per org)
from botecs import (  # noqa: E402,F401  (re-exported into the chain namespace)
    lognormal_mean, uniform_mean, standard_normal, _sq_num, _sym_lognormal,
)

HUMAN_NEURONS = 8.6e10

# ---- the donation slate (fixed across EVERY worldview) -----------------------
# Each entry is org IDENTITY plus a `botec_id` naming its direct-effect
# derivation in the botecs/ package (the EMPIRICAL axis: one true value per
# quantity, improved in one place, read by every worldview — NOT forked). The
# botec computes E[direct effect] on the org's PRIMARY beneficiary in that
# beneficiary's OWN welfare units, BEFORE any moral weighting; the chain's
# `coefficient` supplies the moral circle, the species welfare range and any
# discount. The CIs are calibrated (see botecs/near_term.py) so the
# "animals matter a lot" worldview reproduces Vasco Grilo's published multiples
# and the GiveWell baseline reproduces his ~0.00994 DALY/$.
#
#   domain                    — which moral circle the beneficiary is in
#   animal / averts_intense_suffering / neurons — read by later assumptions
#   botec_id                  — the derivation in botecs/ (its provenance and
#                               sources live there, tagged per factor)
SLATE = [
    {"id": "soup_kitchen", "name": "Local soup kitchen", "domain": "local_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "botec_id": "soup_kitchen"},
    {"id": "gd", "name": "GiveDirectly", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "botec_id": "gd"},
    {"id": "amf", "name": "GiveWell top charity (AMF)", "domain": "global_human",
     "animal": False, "averts_intense_suffering": True, "neurons": 8.6e10,
     "botec_id": "amf"},
    {"id": "aim", "name": "AIM / Charity Entrepreneurship", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "botec_id": "aim"},
    {"id": "thl", "name": "The Humane League", "domain": "farmed_animal",
     "animal": True, "averts_intense_suffering": True, "neurons": 2.2e8,
     "botec_id": "thl"},
    {"id": "swp", "name": "Shrimp Welfare Project", "domain": "invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "botec_id": "swp"},
    {"id": "wildbugs", "name": "Wild insects (humane pesticides)", "domain": "wild_invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "botec_id": "wildbugs"},
    # ALLFED and AI safety are WORKED BOTECs sharing the SAME astronomical
    # `futureDalysAtStake` (botecs/future.py), so which one a longtermist funds
    # is arithmetic on their x-risk-reduced-per-dollar, not a chosen result.
    {"id": "allfed", "name": "ALLFED", "domain": "future_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "botec_id": "allfed"},
    {"id": "redwood", "name": "AI safety (Redwood Research)", "domain": "xrisk_future",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "botec_id": "redwood"},
]

Z90 = botecs.Z90


def org_botec(org):
    """The botec (empirical derivation) backing an org."""
    return botecs.get(org["botec_id"])


def direct_daly_per_usd(org):
    """Exact E[direct effect] of the org, before moral weighting — the mean of
    its botec. Factors are independent and each term is multilinear, so the
    expectation is the term-wise product of factor means summed over terms."""
    return org_botec(org).mean()


# ---- the parochial moral theory ---------------------------------------------
def moral_weight(domain):
    """Who counts. At the root: only people near me."""
    return 1.0 if domain == "local_human" else 0.0


def welfare_range(org):
    """How much one counted individual counts. At the root: whoever is inside
    the circle counts fully (and only humans are inside it anyway)."""
    return 1.0


def uncertain_factors(org):
    """The multiplicative UNCERTAIN moral parameters this worldview applies to
    an org, beyond the structural circle (moral_weight × welfare_range). Each
    factor is a dict:
      name    — Squiggle variable name (defined once in the model's prelude)
      mean    — exact E[factor], used by the Python-side ranking
      dist    — Squiggle source for the factor's distribution
      point   — True when the assumption PINS the value (no uncertainty left)
      comment — one-line justification and source, rendered into the model
    Assumptions that introduce an uncertain magnitude (a discount, a
    probability, a multiplier) WRAP this instead of baking a point estimate
    into `coefficient`: the generated model then carries the full distribution,
    while the ranking uses the exact expectation. Factors are independent by
    construction, so E[product] = product of E[each] — the Python point math
    and the Squiggle model agree exactly. None at the root."""
    return []


def lognormal_factor(name, lo, hi, comment):
    """An uncertain factor whose two-sided 90% CI is [lo, hi] (rendered
    symbolically so its mean stays analytic), or a pinned point when lo == hi.
    `sampler` carries the raw spec so the confidence Monte-Carlo can draw from
    the same distribution the mean summarises."""
    return {"name": name, "mean": lognormal_mean(lo, hi), "point": lo == hi,
            "dist": _sq_num(lo) if lo == hi else _sym_lognormal(lo, hi),
            "sampler": ("point", lo) if lo == hi else ("lognormal", lo, hi),
            "comment": comment}


def beta_factor(name, a, b, comment):
    """An uncertain PROBABILITY factor, beta(a, b) — properly bounded to [0, 1]
    where a lognormal would leak past 1. Mean is exactly a/(a+b)."""
    return {"name": name, "mean": a / (a + b), "point": False,
            "dist": f"Sym.beta({_sq_num(a)}, {_sq_num(b)})",
            "sampler": ("beta", a, b), "comment": comment}


def coefficient(org):
    """The whole moral coefficient this worldview puts on an org: the
    structural circle (who counts, and how much one counted individual counts)
    times the expectation of every registered uncertain factor. Later
    assumptions change the answer by redefining or wrapping the functions this
    multiplies together (or `coefficient` itself)."""
    c = moral_weight(org["domain"]) * welfare_range(org)
    for f in uncertain_factors(org):
        c *= f["mean"]
    return c


def externality_coefficient(org):
    """Additive term alongside `coefficient`, PER UNIT of the org's direct
    effect — a downstream SIDE EFFECT of funding it that scales with how much
    the org actually achieves (more DALYs bought means more beneficiaries,
    means more side effect), so the org's value is
    direct × (coefficient + externality_coefficient) and the generated model
    keeps the side effect correlated with the same uncertain direct-effect
    distribution. Zero at the root; the meat-eater problem redefines this to
    charge human-welfare orgs for the factory farming their beneficiaries'
    diets cause (negative = harm)."""
    return 0.0


def expected_values():
    """{org name: E[wDALY averted per $]} under this worldview — the Python-side
    twin of the generated Squiggle model's `scored` list."""
    return {org["name"]: direct_daly_per_usd(org)
            * (coefficient(org) + externality_coefficient(org))
            for org in SLATE}


# ---- confidence: which org is ACTUALLY the best buy, not just in expectation --
# The models carry full distributions, so "GiveWell wins" can mean "wins on
# average but the shrimp tail could dwarf it". A Monte-Carlo over the same
# distributions the means summarise gives P(org is the argmax) — the confidence
# a worldview's ranking deserves. Deterministic (fixed seed) so generated files
# stay byte-stable.
DALYS_PER_LIFE = 30.0  # DALYs from averting one young-child death (age-weighted;
#                        matches the ALLFED BOTEC's dalyPerLife). wDALY are
#                        already welfare-range-scaled, so a "life-equivalent" is
#                        a human life's worth of averted welfare loss.


def _sample_scalar(spec, rng):
    """Draw one value from a MORAL-factor sampler spec (the discount, the
    suffering asymmetry, …). Botec factors sample themselves; this handles the
    dict-based moral factors registered via lognormal_factor / beta_factor."""
    kind = spec[0]
    if kind == "point":
        return spec[1]
    if kind == "lognormal":
        lo, hi = spec[1], spec[2]
        mu = (math.log(lo) + math.log(hi)) / 2
        sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
        return math.exp(mu + sigma * standard_normal(rng))
    if kind == "uniform":
        return spec[1] + (spec[2] - spec[1]) * rng.random()
    if kind == "beta":
        a, b, u = spec[1], spec[2], rng.random()
        if a == 1:   # inverse-CDF of beta(1, b) — the only shape the chain uses
            return 1.0 - (1.0 - u) ** (1.0 / b)
        if b == 1:
            return u ** (1.0 / a)
        raise NotImplementedError("only beta(1, b) / beta(a, 1) are sampled stably")
    raise ValueError(f"unknown sampler {kind!r}")


def _shared_botec_factors():
    """{name: Factor} for direct-effect factors flagged shared across botecs
    (futureDalysAtStake), so the Monte-Carlo draws each ONCE per world-state and
    applies the same draw to every org that carries it — ALLFED and AI safety
    then move together on the shared future, as they should."""
    shared = {}
    for org in SLATE:
        shared.update(org_botec(org).shared_factor_specs())
    return shared


def argmax_confidences(n=10000, seed=0):
    """{org name: P(this org is the single best buy)} under this worldview, by
    Monte-Carlo over the chain's full distributions. Uncertain factors shared by
    name — moral (the discount, the suffering asymmetry) and empirical
    (futureDalysAtStake) — are drawn ONCE per world-state and applied to every
    org that carries them; each botec's un-shared direct factors are drawn
    independently per org, matching the generated model."""
    rng = random.Random(seed)
    # per-org: structural-only coefficient, externality, and the names of the
    # uncertain moral factors it carries.
    specs = []
    shared = {}
    for org in SLATE:
        fs = uncertain_factors(org)
        struct = coefficient(org)
        for f in fs:
            struct /= f["mean"]
            shared.setdefault(f["name"], f["sampler"])
        specs.append((org, struct, externality_coefficient(org),
                      [f["name"] for f in fs]))
    shared_botec = _shared_botec_factors()
    counts = {org["name"]: 0 for org in SLATE}
    for _ in range(n):
        fdraw = {name: _sample_scalar(s, rng) for name, s in shared.items()}
        bdraw = {name: fac.sample(rng) for name, fac in shared_botec.items()}
        best_name, best_val = None, -math.inf
        for org, struct, ext, fnames in specs:
            fac = 1.0
            for fn in fnames:
                fac *= fdraw[fn]
            val = org_botec(org).sample(rng, bdraw) * (struct * fac + ext)
            if val > best_val:
                best_val, best_name = val, org["name"]
        counts[best_name] += 1
    return {name: c / n for name, c in counts.items()}


# ---- Squiggle generation -----------------------------------------------------
# The chain's end product: `squiggle()` renders one standalone Squiggle model
# (no imports, playground-ready) whose `worldviewEv` is the expected value of
# this worldview — E[wDALY/$] of its best buy under its accumulated coefficients.
def _camel(s):
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def squiggle_var(org):
    return _camel(org["id"]) + "DalyPerUsd"


def botec_model_relpath(org):
    """Where the org's full-derivation botec model lives (linked from the
    worldview model, generated by generate.py)."""
    return f"squiggle/botecs/{org['botec_id']}.squiggle"


def squiggle_dist_lines(org):
    """The org's direct-effect distribution as a SINGLE moment-matched lognormal
    SUMMARY (mean AND variance equal to the full botec's), plus a link to the
    standalone derivation. Keeping the full factor derivation out of every one
    of the 73 worldview models is what stops each model from exploding as the
    empirical mechanisms get richer; the derivation lives once, in the botec
    model, and is edited there."""
    var = squiggle_var(org)
    b = org_botec(org)
    link = botec_model_relpath(org)
    summ = b.summary_lognormal()
    if summ is None:  # degenerate botec (no variance): pin to the mean
        return [f"{var} = {_sq_num(b.mean())}  // {b.id} botec (pinned); "
                f"full derivation: {link}"]
    return [f"{var} = {_sym_lognormal(*summ)}  // moment-matched summary of the "
            f"{b.id} botec (mean & variance exact); full derivation: {link}"]


def squiggle_mean_expr(org):
    """Exact E[direct effect] as Squiggle source: the mean of the summary
    lognormal, which is constructed to equal the full botec's mean to float
    precision — the same value direct_daly_per_usd returns in Python."""
    return f"mean({squiggle_var(org)})"


def squiggle_prelude():
    """Squiggle lines before the slate: one named distribution per uncertain
    moral parameter the chain has registered (deduplicated, in chain order),
    so the model shows every parameter as a distribution, not a baked point."""
    factors, names = [], set()
    for org in SLATE:
        for f in uncertain_factors(org):
            if f["name"] not in names:
                names.add(f["name"])
                factors.append(f)
    if not factors:
        return []
    lines = ["// Uncertain moral parameters this chain applies. Sym.lognormal({p5, p95})",
             "// is a 90% CI; Sym.beta is a probability, bounded to [0, 1]. Factors are",
             "// independent, so each org's E[wDALY/$] below factorises exactly into the",
             "// product of the means."]
    for f in factors:
        lines.append(f"{f['name']} = {f['dist']}  // {f['comment']}")
    lines.append("")
    return lines


def _value_expr(org, expectation):
    """Assemble the org's Squiggle expression:
    direct × (structural coefficient × factors + externality).
    With expectation=True every distribution is wrapped in mean(...) — the
    exact analytic expectation the ranking sorts by (factors are independent,
    so the expectation factorises; no sampling noise can reorder heavy-tailed
    orgs between runs). With expectation=False the same expression is left as
    a full distribution, so the playground shows the spread and the tails."""
    head = squiggle_mean_expr(org) if expectation else squiggle_var(org)
    factors = uncertain_factors(org)
    structural = coefficient(org)
    for f in factors:
        structural /= f["mean"]
    if structural == 0:
        factors = []  # outside the circle: no factor can rescue a zero weight
    core = f"{structural:.6g}"
    for f in factors:
        ref = f["name"] if (f["point"] or not expectation) else f"mean({f['name']})"
        core += f" * {ref}"
    ext = externality_coefficient(org)
    if ext:
        return f"{head} * ({core} + ({ext:.6g}))"
    return f"{head} * {core}"


def value_expression(org):
    """Squiggle expression for the org's exact E[wDALY/$] under this worldview.
    The override assumptions at the end of the line redefine this wholesale."""
    return _value_expr(org, expectation=True)


def dist_expression(org):
    """Squiggle expression for the org's full wDALY/$ DISTRIBUTION under this
    worldview — the same product as `value_expression`, with every uncertain
    term left as a distribution."""
    return _value_expr(org, expectation=False)


def squiggle(header=""):
    """Render this worldview's standalone Squiggle model."""
    lines = []
    if header:
        lines += [header.rstrip("\n"), ""]
    lines += squiggle_prelude()
    lines += ["// Direct effect on each org's primary beneficiary, BEFORE moral",
              "// weighting, as a moment-matched lognormal SUMMARY of that org's worked",
              "// botec (mean AND variance exact). The full factor-by-factor derivation —",
              "// with each factor's provenance and source — lives in the linked",
              "// squiggle/botecs/<id>.squiggle model, so it is edited in ONE place and",
              "// read by every worldview, rather than inlined into all 73."]
    for org in SLATE:
        lines += squiggle_dist_lines(org)
    lines += ["",
              "// Each org: `dist` is its full wDALY/$ distribution under this worldview",
              "// (direct effect × moral coefficient, externalities correlated with the",
              "// same direct-effect draw); `wdalyPerUsd` is the exact analytic mean of",
              "// `dist`, which is what the ranking sorts by.",
              "scored = ["]
    for org in SLATE:
        lines.append(f'  {{ name: "{org["name"]}", dist: {dist_expression(org)}, '
                     f"wdalyPerUsd: {value_expression(org)} }},")
    lines += ["]",
              "",
              "ranking = List.reverse(List.sortBy(scored, {|x| x.wdalyPerUsd}))",
              "best = ranking[0]",
              "",
              "// The expected value of THIS worldview: what its best buy achieves.",
              "worldviewEv = best.wdalyPerUsd"]
    return "\n".join(lines) + "\n"
