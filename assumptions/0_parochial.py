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
import re      # noqa: E402

HUMAN_NEURONS = 8.6e10

# ---- the donation slate (fixed across EVERY worldview) -----------------------
# daly_per_usd = [lo, hi] lognormal 90% CI for the DIRECT effect on the org's
# PRIMARY beneficiary, in that beneficiary's OWN welfare units (a farmed-animal
# DALY for an animal org, an undiscounted future life-year for an x-risk org),
# BEFORE any moral weighting. The chain's `coefficient` supplies the moral
# circle, the species welfare range and any discount. So an animal org's
# published HUMAN-EQUIVALENT DALY/$ is reproduced HERE as (this direct figure)
# times the welfare range the animal assumption puts on it. The calibration is
# chosen so the "animals matter a lot" worldview (w1_2_5, Rethink Priorities
# welfare ranges) reproduces Vasco Grilo's PUBLISHED cost-effectiveness numbers,
# and the GiveWell (AMF) baseline reproduces his ~0.00994 DALY/$ for GiveWell
# top charities, so allocate.py's "x GiveWell" column reads his own multiples:
#   GiveWell top charities  ~0.00994 DALY/$  (Grilo's baseline)             = 1x
#   GiveDirectly            ~10x below top charities (GiveWell cash bar)    ~ 0.1x
#   Corporate chicken campaigns  ~9-120 chicken-years/$ (Saulius/RP);
#     ~1.67-14.3 human-equiv DALY/$ (Grilo)  -> ~4.6 DALY/$ at RP wr 0.332  ~ 460x
#   Shrimp Welfare Project HSI   639 DALY/$ (Grilo)                         ~ 64.3k x
#   Humane pesticides (wild insects) 236 DALY/$ (Grilo)                    ~ 23.7k x
#   x-risk / GCR  Linch's ~$100M per 0.01% x-risk reduction (~1e-12/$), x the
#     undiscounted future at stake (Bostrom astronomical waste; Cotra timelines).
SLATE = [
    {"id": "soup_kitchen", "name": "Local soup kitchen", "domain": "local_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "worked BOTEC (subjective-wellbeing scale of a hot-meal program)",
     # counterfactual_bank_value: the fraction of the donation's welfare value
     # the money would have produced anyway sitting in a bank (consumption
     # smoothing / eventual spending) — a uniform [lo, hi] with mean 0.3,
     # since a symmetric bounded fraction has no lognormal-style tail.
     "botec": {"people_helped_per_usd": [0.05, 0.5],
               "wellbeing_gain_daly": [0.001, 0.01],
               "counterfactual_bank_value": [0.1, 0.5]}},
    {"id": "gd", "name": "GiveDirectly", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "GiveWell cash benchmark; ~1/10 of top charities per $ "
               "(CI mean 0.00101 DALY/$ = 0.10x the AMF entry's mean)",
     "source_url": "https://www.givewell.org/international/technical/programs/cash-transfers",
     "daly_per_usd": [0.0004, 0.002]},
    {"id": "amf", "name": "GiveWell top charity (AMF)", "domain": "global_human",
     "animal": False, "averts_intense_suffering": True, "neurons": 8.6e10,
     "source": "GiveWell CEA; CI mean 0.00994 DALY/$ reproduces Grilo's GiveWell "
               "baseline exactly — the 1x every other multiple is read against",
     "source_url": "https://www.givewell.org/how-we-work/our-criteria/cost-effectiveness/cost-effectiveness-models",
     "daly_per_usd": [0.0035, 0.021]},
    {"id": "aim", "name": "AIM / Charity Entrepreneurship", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "AIM incubatees aim at GiveWell-level cost-effectiveness with high "
               "early-stage variance; expected value ~around (a bit under) the top-charity bar",
     "source_url": "https://www.charityentrepreneurship.com/",
     "daly_per_usd": [0.001, 0.025]},
    {"id": "thl", "name": "The Humane League", "domain": "farmed_animal",
     "animal": True, "averts_intense_suffering": True, "neurons": 2.2e8,
     "source": "Saulius 9-120 chicken-years/$ x the welfare delta of a reform; this "
               "chicken-DALY CI x RP welfare range 0.332 spans [0.4, 15.6], bracketing "
               "Grilo's published 1.67-14.3 human-equivalent DALY/$; CI mean 14.0 x "
               "0.332 = 4.6 DALY/$ = ~460x GiveWell, his central multiple",
     "source_url": "https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken",
     "daly_per_usd": [1.2, 47]},
    {"id": "swp", "name": "Shrimp Welfare Project", "domain": "invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "source": "Grilo HSI 639 DALY/$ = 64.3k x GiveWell; CI mean 20668 x RP shrimp "
               "welfare range 0.031 = 641 DALY/$, reproducing his figure",
     "source_url": "https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane",
     "daly_per_usd": [1200, 74000]},
    {"id": "wildbugs", "name": "Wild insects (humane pesticides)", "domain": "wild_invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "source": "Grilo 236 DALY/$ = 23.7k x GiveWell (5.74M insects/$); CI mean 23427 "
               "x insect welfare range 0.01 = 234 DALY/$, reproducing his figure",
     "source_url": "https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane",
     "daly_per_usd": [1600, 82000]},
    # ALLFED and AI safety are WORKED BOTECs, not opaque ranges: their value is
    # COMPUTED from mechanistic inputs, so which one a longtermist funds is math
    # under stated assumptions, not a chosen result. Both carry the SAME
    # astronomical `futureDalysAtStake`, so the comparison reduces to their
    # x-risk-reduced-per-dollar — exactly what Denkenberger & Pearce and Linch
    # estimate. On these central inputs AI safety edges ahead (~1.7x); more
    # pessimistic recovery-from-collapse inputs flip it to ALLFED. Neither is
    # forced — edit a factor in the playground and the ranking moves.
    {"id": "allfed", "name": "ALLFED", "domain": "future_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "Resilient foods for nuclear-winter / abrupt-sunlight-reduction "
               "catastrophes: near-term lives fed PLUS the far-future value of "
               "averting a civilization-ending collapse (Denkenberger & Pearce). "
               "Worked BOTEC; central mean ~3.5k undiscounted DALY/$.",
     "source_url": "https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176",
     "botec": {
        "factors": [
            {"name": "allfedPCatastrophePerCentury", "ci": [0.003, 0.05],
             "comment": "P(nuclear-winter-scale ag catastrophe this century): ~0.1-1%/yr full-scale nuclear war x ~10% winter"},
            {"name": "allfedLivesSavedPerDollarIfCatastrophe", "ci": [0.02, 2],
             "comment": "Denkenberger alternate-food lives saved per $ GIVEN the catastrophe"},
            {"name": "allfedDalyPerLife", "point": 30,
             "comment": "DALYs per life saved"},
            {"name": "allfedPCivEndGivenCatastrophe", "ci": [0.005, 0.1],
             "comment": "chance the catastrophe is permanently civilization-ending"},
            {"name": "allfedRiskShareRemovedPerDollar", "ci": [1e-10, 1e-9],
             "comment": "fraction of that x-risk a marginal resilient-food $ removes"},
            {"name": "allfedFutureDalysAtStake", "ci": [1e11, 1e16],
             "comment": "astronomical DALYs preserved if the collapse is averted (Bostrom)"},
        ],
        "expr": ("allfedPCatastrophePerCentury * allfedLivesSavedPerDollarIfCatastrophe * allfedDalyPerLife"
                 " + allfedPCatastrophePerCentury * allfedPCivEndGivenCatastrophe"
                 " * allfedRiskShareRemovedPerDollar * allfedFutureDalysAtStake"),
     }},
    {"id": "redwood", "name": "AI safety (Redwood Research)", "domain": "xrisk_future",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "Linch's ~$100M-$1B per 0.01% (1e-4) x-risk reduction x the SAME "
               "astronomical future at stake as ALLFED (Bostrom astronomical waste; "
               "Cotra timelines). Worked BOTEC; central mean ~5.8k undiscounted DALY/$.",
     "source_url": "https://forum.effectivealtruism.org/posts/cKPkimztzKoCkZ75r/how-many-ea-2021-usds-would-you-trade-off-against-a-0-01",
     "botec": {
        "factors": [
            {"name": "redwoodXRiskReducedPerDollar", "ci": [1e-13, 1e-12],
             "comment": "Linch's ~$100M-$1B per 0.01% x-risk bar"},
            {"name": "redwoodFutureDalysAtStake", "ci": [1e11, 1e16],
             "comment": "astronomical DALYs preserved if extinction is averted (Bostrom); same future as ALLFED"},
        ],
        "expr": "redwoodXRiskReducedPerDollar * redwoodFutureDalysAtStake",
     }},
]


# ---- point estimates (mirror Squiggle's mean of a lognormal 90% CI) ----------
# Squiggle's `lo to hi` is the lognormal whose 5th/95th percentiles are lo/hi;
# Z90 = Phi^-1(0.95) is the normal deviate of a two-sided 90% interval.
Z90 = 1.6448536269514722


def lognormal_mean(lo, hi):
    """E[X] for the lognormal whose two-sided 90% CI is [lo, hi]: with
    mu = (ln lo + ln hi)/2 and sigma = (ln hi - ln lo)/(2 Z90),
    E[X] = exp(mu + sigma^2/2) — exactly what Squiggle's mean(lo to hi)
    returns, so the Python-side ranking agrees with the generated model.
    Note the mean sits ABOVE the median exp(mu): wide order-of-magnitude
    CIs are right-skewed, and expectations are dominated by their upper tail."""
    if lo == hi:  # a degenerate "distribution": an assumption pinning the value
        return float(lo)
    mu = (math.log(lo) + math.log(hi)) / 2
    sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
    return math.exp(mu + sigma * sigma / 2)


def uniform_mean(lo, hi):
    """E[X] for uniform [lo, hi] — matches Squiggle's mean(Sym.uniform)."""
    return (lo + hi) / 2


def _botec_factor_mean(f):
    """E[factor] for a worked-BOTEC factor: a pinned scalar (`point`) or a
    lognormal 90% CI (`ci`)."""
    return float(f["point"]) if "point" in f else lognormal_mean(*f["ci"])


def direct_daly_per_usd(org):
    """Exact E[direct effect] of the org, before moral weighting: the factors
    are independent, so the expectation of the product is the product of the
    expectations (and E[1-X] = 1-E[X] by linearity).

    A `botec` is a worked calculation. General form: an ordered list of named,
    independent `factors` (each a `ci` 90% CI or a pinned `point`) combined by
    an `expr` of sums and products, so a BOTEC can add and multiply terms
    (e.g. ALLFED's near-term lives fed + far-future collapse averted). Because
    the factors are independent and the expr is multilinear, E[expr] is the expr
    evaluated at each factor's mean. Old form: the soup kitchen's
    people x wellbeing x (1 - bank)."""
    if "botec" in org:
        b = org["botec"]
        if "factors" in b:
            env = {f["name"]: _botec_factor_mean(f) for f in b["factors"]}
            return eval(b["expr"], {"__builtins__": {}}, env)  # trusted in-repo expr
        return (lognormal_mean(*b["people_helped_per_usd"])
                * lognormal_mean(*b["wellbeing_gain_daly"])
                * (1 - uniform_mean(*b["counterfactual_bank_value"])))
    return lognormal_mean(*org["daly_per_usd"])


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


def _standard_normal(rng):
    """One N(0,1) draw via Box-Muller, using ONLY rng.random() (the Mersenne
    Twister core, whose stream is identical across CPython versions) — so the
    confidence Monte-Carlo baked into generated files is byte-reproducible in CI,
    which random.gauss (an implementation that may change) would not guarantee."""
    u1 = rng.random() or 1e-300
    u2 = rng.random()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


def _sample_scalar(spec, rng):
    """Draw one value from a factor/direct sampler spec."""
    kind = spec[0]
    if kind == "point":
        return spec[1]
    if kind == "lognormal":
        lo, hi = spec[1], spec[2]
        mu = (math.log(lo) + math.log(hi)) / 2
        sigma = (math.log(hi) - math.log(lo)) / (2 * Z90)
        return math.exp(mu + sigma * _standard_normal(rng))
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


def _sample_direct(org, rng):
    """One draw of the org's direct effect, from the same distribution
    direct_daly_per_usd takes the mean of."""
    if "botec" in org:
        b = org["botec"]
        if "factors" in b:
            env = {f["name"]: (float(f["point"]) if "point" in f
                               else _sample_scalar(("lognormal", *f["ci"]), rng))
                   for f in b["factors"]}
            return eval(b["expr"], {"__builtins__": {}}, env)  # trusted in-repo expr
        return (_sample_scalar(("lognormal", *b["people_helped_per_usd"]), rng)
                * _sample_scalar(("lognormal", *b["wellbeing_gain_daly"]), rng)
                * (1 - _sample_scalar(("uniform", *b["counterfactual_bank_value"]), rng)))
    return _sample_scalar(("lognormal", *org["daly_per_usd"]), rng)


def argmax_confidences(n=10000, seed=0):
    """{org name: P(this org is the single best buy)} under this worldview, by
    Monte-Carlo over the chain's full distributions. Moral-parameter factors
    (the discount, the suffering asymmetry, …) are shared by name, so each is
    drawn ONCE per world-state and applied to every org that carries it; direct
    effects are independent per org, as in the generated model."""
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
    counts = {org["name"]: 0 for org in SLATE}
    for _ in range(n):
        fdraw = {name: _sample_scalar(s, rng) for name, s in shared.items()}
        best_name, best_val = None, -math.inf
        for org, struct, ext, fnames in specs:
            fac = 1.0
            for fn in fnames:
                fac *= fdraw[fn]
            val = _sample_direct(org, rng) * (struct * fac + ext)
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


def _sq_num(x):
    if isinstance(x, float) and x.is_integer():
        return str(int(x))
    return repr(x)


def squiggle_var(org):
    return _camel(org["id"]) + "DalyPerUsd"


def _sym_lognormal(lo, hi):
    """Squiggle source for the lognormal whose two-sided 90% CI is [lo, hi].
    The SYMBOLIC constructor, not `lo to hi`: the runtime samples `to`-built
    distributions even inside mean(), and with order-of-magnitude CIs the
    sampled mean of the heavy upper tail is biased low by several-fold. The
    symbolic form keeps every mean() analytic, so the generated model's
    numbers equal the Python ranking's exactly."""
    return f"Sym.lognormal({{p5: {_sq_num(lo)}, p95: {_sq_num(hi)}}})"


def _botec_factor_line(f):
    """Squiggle line defining one worked-BOTEC factor as a named distribution
    (or pinned scalar), with its cited justification."""
    rhs = _sq_num(f["point"]) if "point" in f else _sym_lognormal(*f["ci"])
    return f"{f['name']} = {rhs}  // {f['comment']}"


def _botec_mean_expr(b):
    """The BOTEC's `expr` with every DISTRIBUTION factor wrapped in mean() — its
    exact analytic expectation (pinned points are already their own mean)."""
    expr = b["expr"]
    for f in b["factors"]:
        if "point" not in f:
            expr = re.sub(rf"\b{re.escape(f['name'])}\b", f"mean({f['name']})", expr)
    return f"({expr})"


def squiggle_dist_lines(org):
    """Squiggle lines defining the org's direct-effect distribution."""
    var = squiggle_var(org)
    if "botec" in org:
        b, p = org["botec"], _camel(org["id"])
        if "factors" in b:
            return [_botec_factor_line(f) for f in b["factors"]] + [f"{var} = {b['expr']}"]
        cb_lo, cb_hi = b["counterfactual_bank_value"]
        return [
            f"{p}PeopleHelpedPerUsd = {_sym_lognormal(*b['people_helped_per_usd'])}",
            f"{p}WellbeingGainDaly = {_sym_lognormal(*b['wellbeing_gain_daly'])}",
            f"{p}CounterfactualBankValue = Sym.uniform({_sq_num(cb_lo)}, {_sq_num(cb_hi)})",
            f"{var} = {p}PeopleHelpedPerUsd * {p}WellbeingGainDaly"
            f" * (1 - {p}CounterfactualBankValue)",
        ]
    return [f"{var} = {_sym_lognormal(*org['daly_per_usd'])}"]


def squiggle_mean_expr(org):
    """Exact E[direct effect] as Squiggle source. mean() of a symbolic
    distribution is analytic; a product's mean factorises over its independent
    terms, so the BOTEC's expectation is the product of component means —
    the same computation direct_daly_per_usd performs in Python."""
    if "botec" in org:
        b, p = org["botec"], _camel(org["id"])
        if "factors" in b:
            return _botec_mean_expr(b)
        return (f"(mean({p}PeopleHelpedPerUsd) * mean({p}WellbeingGainDaly)"
                f" * (1 - mean({p}CounterfactualBankValue)))")
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
              "// weighting. Sym.lognormal({p5, p95}) is the lognormal whose two-sided",
              "// 90% CI is [p5, p95] — an order-of-magnitude BOTEC, symbolic so every",
              "// mean() below is analytic rather than sampled. Each org's figure is",
              "// grounded in the source cited on it."]
    for org in SLATE:
        if org.get("source_url"):
            lines.append(f"// {org['source_url']}")
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
