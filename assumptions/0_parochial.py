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

import math  # noqa: E402  (assumption files run via exec, in chain order)

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
     "botec": {"people_helped_per_usd": [0.05, 0.5],
               "wellbeing_gain_daly": [0.001, 0.01],
               "counterfactual_bank_value": 0.3}},
    {"id": "gd", "name": "GiveDirectly", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "GiveWell cash benchmark; ~1/10 of top charities per $",
     "source_url": "https://www.givewell.org/international/technical/programs/cash-transfers",
     "daly_per_usd": [0.0004, 0.002]},
    {"id": "amf", "name": "GiveWell top charity (AMF)", "domain": "global_human",
     "animal": False, "averts_intense_suffering": True, "neurons": 8.6e10,
     "source": "GiveWell CEA; mean ~0.00994 DALY/$ (Grilo's GiveWell baseline)",
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
     "source": "Saulius 9-120 chicken-years/$ x welfare improvement; Grilo ~1.67-14.3 DALY/$; "
               "at RP chicken welfare range 0.332 reproduces ~4.6 DALY/$ (~460x GiveWell)",
     "source_url": "https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken",
     "daly_per_usd": [1.2, 47]},
    {"id": "swp", "name": "Shrimp Welfare Project", "domain": "invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "source": "Grilo HSI 639 DALY/$ = 64.3k x GiveWell; at RP shrimp welfare range 0.031 "
               "this direct figure reproduces that human-equivalent number",
     "source_url": "https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane",
     "daly_per_usd": [1200, 74000]},
    {"id": "wildbugs", "name": "Wild insects (humane pesticides)", "domain": "wild_invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "source": "Grilo 236 DALY/$ = 23.7k x GiveWell (5.74M insects/$); at an insect welfare "
               "range ~0.01 this direct figure reproduces that human-equivalent number",
     "source_url": "https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane",
     "daly_per_usd": [1600, 82000]},
    {"id": "allfed", "name": "ALLFED", "domain": "future_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "Resilient foods for global catastrophes; NEAR-TERM cost-effectiveness "
               "~$400-20000 per life (Denkenberger & Pearce). Its astronomical far-future "
               "upside is unlocked only by the resilient_foods_beat_agi assumption.",
     "source_url": "https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176",
     "daly_per_usd": [0.002, 0.5]},
    {"id": "redwood", "name": "AI safety (Redwood Research)", "domain": "xrisk_future",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "Linch's ~$100M per 0.01% x-risk reduction (~1e-12/$) x the undiscounted "
               "future at stake (Bostrom astronomical waste; Cotra AI timelines/takeover)",
     "source_url": "https://forum.effectivealtruism.org/posts/cKPkimztzKoCkZ75r/how-many-ea-2021-usds-would-you-trade-off-against-a-0-01",
     "daly_per_usd": [0.2, 20000]},
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


def direct_daly_per_usd(org):
    """Point estimate of the org's direct effect, before moral weighting."""
    if "botec" in org:
        b = org["botec"]
        return (lognormal_mean(*b["people_helped_per_usd"])
                * lognormal_mean(*b["wellbeing_gain_daly"])
                * (1 - b["counterfactual_bank_value"]))
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
    symbolically so its mean stays analytic), or a pinned point when lo == hi."""
    return {"name": name, "mean": lognormal_mean(lo, hi), "point": lo == hi,
            "dist": _sq_num(lo) if lo == hi else _sym_lognormal(lo, hi),
            "comment": comment}


def beta_factor(name, a, b, comment):
    """An uncertain PROBABILITY factor, beta(a, b) — properly bounded to [0, 1]
    where a lognormal would leak past 1. Mean is exactly a/(a+b)."""
    return {"name": name, "mean": a / (a + b), "point": False,
            "dist": f"Sym.beta({_sq_num(a)}, {_sq_num(b)})", "comment": comment}


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


def squiggle_dist_lines(org):
    """Squiggle lines defining the org's direct-effect distribution."""
    var = squiggle_var(org)
    if "botec" in org:
        b, p = org["botec"], _camel(org["id"])
        return [
            f"{p}PeopleHelpedPerUsd = {_sym_lognormal(*b['people_helped_per_usd'])}",
            f"{p}WellbeingGainDaly = {_sym_lognormal(*b['wellbeing_gain_daly'])}",
            f"{p}CounterfactualBankValue = {_sq_num(b['counterfactual_bank_value'])}",
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
        p = _camel(org["id"])
        return (f"(mean({p}PeopleHelpedPerUsd) * mean({p}WellbeingGainDaly)"
                f" * (1 - {p}CounterfactualBankValue))")
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
