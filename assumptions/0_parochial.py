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
    # ALLFED and AI safety are WORKED BOTECs (like the soup kitchen), not opaque
    # ranges: their value is COMPUTED from mechanistic inputs, so which one wins
    # among longtermists is math under stated assumptions, not a chosen result.
    # Both share the same astronomical `futureDalysAtStake`, so the comparison
    # reduces to their x-risk-reduced-per-dollar — exactly what Denkenberger &
    # Pearce and Linch estimate. On these central inputs AI safety edges ahead
    # (~1.7x); Denkenberger's more pessimistic recovery-from-collapse estimates
    # flip it to ALLFED. Neither is forced — change an input and the ranking moves.
    {"id": "allfed", "name": "ALLFED", "domain": "future_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "Resilient foods for nuclear-winter / abrupt-sunlight-reduction "
               "catastrophes: near-term lives fed PLUS the far-future value of "
               "averting a civilization-ending collapse (Denkenberger & Pearce)",
     "source_url": "https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176",
     "botec": {
        "factors": [
            # P(nuclear-winter-scale agricultural catastrophe this century)
            # = ~0.1-1%/yr full-scale nuclear war x ~10% conditional winter.
            ("pAgriculturalCatastrophePerCentury", [0.003, 0.05]),
            # Denkenberger alternate-food cost-effectiveness GIVEN the catastrophe:
            # lives saved per dollar of prepared resilient-food capacity.
            ("livesSavedPerDollarIfCatastrophe", [0.02, 2]),
            ("dalyPerLife", 30),
            # Far future: the chance the catastrophe is permanently civilization-
            # ending, the astronomical future it would cost, and the fraction of
            # that risk a marginal resilient-food dollar removes.
            ("pCivilizationEndingGivenCatastrophe", [0.005, 0.1]),
            ("riskShareRemovedPerDollar", [1e-10, 1e-9]),
            ("futureDalysAtStake", [1e11, 1e16]),
        ],
        # near-term lives fed + far-future collapse averted
        "expr": ("pAgriculturalCatastrophePerCentury * livesSavedPerDollarIfCatastrophe * dalyPerLife"
                 " + pAgriculturalCatastrophePerCentury * pCivilizationEndingGivenCatastrophe"
                 " * riskShareRemovedPerDollar * futureDalysAtStake"),
     }},
    {"id": "redwood", "name": "AI safety (Redwood Research)", "domain": "xrisk_future",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "Linch's ~$100M-$1B per 0.01% (1e-4) x-risk reduction x the same "
               "astronomical future at stake (Bostrom astronomical waste; Cotra timelines)",
     "source_url": "https://forum.effectivealtruism.org/posts/cKPkimztzKoCkZ75r/how-many-ea-2021-usds-would-you-trade-off-against-a-0-01",
     "botec": {
        "factors": [
            ("xRiskReducedPerDollar", [1e-13, 1e-12]),   # Linch's bar
            ("futureDalysAtStake", [1e11, 1e16]),        # same future as ALLFED
        ],
        "expr": "xRiskReducedPerDollar * futureDalysAtStake",
     }},
]


# ---- point estimates (mirror Squiggle's mean of a lognormal 90% CI) ----------
def lognormal_mean(lo, hi):
    """E[X] for the lognormal whose 90% CI is [lo, hi] — exactly what Squiggle's
    mean(lo to hi) returns, so the Python-side ranking agrees with the model."""
    mu = (math.log(lo) + math.log(hi)) / 2
    sigma = (math.log(hi) - math.log(lo)) / (2 * 1.6448536269514722)
    return math.exp(mu + sigma * sigma / 2)


def _botec_value(factor):
    """A worked-BOTEC factor is either a scalar constant or a [lo, hi] 90% CI;
    reduce it to the point estimate the model uses (Squiggle's mean(lo to hi))."""
    if isinstance(factor, (list, tuple)):
        return lognormal_mean(*factor)
    return float(factor)


def direct_daly_per_usd(org):
    """Point estimate of the org's direct effect, before moral weighting.

    A `botec` is a worked calculation. New form: an ordered list of named
    `factors` (each a scalar or [lo, hi]) plus an `expr` that combines them, so a
    BOTEC can add and multiply terms (e.g. ALLFED's near-term lives + far-future
    collapse averted). Old form: the soup kitchen's people x wellbeing x (1-bank).
    """
    if "botec" in org:
        b = org["botec"]
        if "factors" in b:
            env = {name: _botec_value(f) for name, f in b["factors"]}
            return eval(b["expr"], {"__builtins__": {}}, env)  # trusted, in-repo expr
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


def coefficient(org):
    """The whole moral coefficient this worldview puts on an org: every later
    assumption changes the answer by redefining or wrapping the functions this
    multiplies together (or `coefficient` itself)."""
    return moral_weight(org["domain"]) * welfare_range(org)


def externality(org):
    """Additive wDALY/$ term beyond the org's direct effect × coefficient — a
    downstream SIDE EFFECT of funding it. Zero at the root; the meat-eater
    problem redefines this to charge human-welfare orgs for the factory farming
    their beneficiaries' diets cause."""
    return 0.0


def expected_values():
    """{org name: E[wDALY averted per $]} under this worldview — the Python-side
    twin of the generated Squiggle model's `scored` list."""
    return {org["name"]: direct_daly_per_usd(org) * coefficient(org) + externality(org)
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


def _sq_factor(factor):
    """Render a worked-BOTEC factor as Squiggle: `lo to hi`, or a scalar."""
    if isinstance(factor, (list, tuple)):
        return f"{_sq_num(factor[0])} to {_sq_num(factor[1])}"
    return _sq_num(factor)


def squiggle_dist(org):
    """Squiggle source for the org's direct-effect distribution."""
    if "botec" in org:
        b = org["botec"]
        if "factors" in b:
            lines = ["{"]
            for name, factor in b["factors"]:
                lines.append(f"  {name} = {_sq_factor(factor)}")
            lines.append(f"  {b['expr']}")
            lines.append("}")
            return "\n".join(lines)
        return "\n".join([
            "{",
            f"  peopleHelpedPerUsd = {_sq_num(b['people_helped_per_usd'][0])} to {_sq_num(b['people_helped_per_usd'][1])}",
            f"  wellbeingGainDaly = {_sq_num(b['wellbeing_gain_daly'][0])} to {_sq_num(b['wellbeing_gain_daly'][1])}",
            f"  counterfactualBankValue = {_sq_num(b['counterfactual_bank_value'])}",
            "  peopleHelpedPerUsd * wellbeingGainDaly * (1 - counterfactualBankValue)",
            "}",
        ])
    lo, hi = org["daly_per_usd"]
    return f"{_sq_num(lo)} to {_sq_num(hi)}"


def squiggle_prelude():
    """Extra Squiggle lines an assumption needs before the slate (none yet)."""
    return []


def value_expression(org):
    """Squiggle expression for the org's E[wDALY/$] under this worldview: its
    direct effect times the moral coefficient, plus any additive externality.
    The override assumptions at the end of the line redefine this wholesale."""
    expr = f"mean({squiggle_var(org)}) * {coefficient(org):.6g}"
    ext = externality(org)
    if ext:
        expr += f" + ({ext:.6g})"
    return expr


def squiggle(header=""):
    """Render this worldview's standalone Squiggle model."""
    lines = []
    if header:
        lines += [header.rstrip("\n"), ""]
    lines += squiggle_prelude()
    lines += ["// Direct effect on each org's primary beneficiary, BEFORE moral",
              "// weighting. `lo to hi` is a lognormal 90% CI (order-of-magnitude BOTEC)."]
    for org in SLATE:
        lines.append(f"{squiggle_var(org)} = {squiggle_dist(org)}")
    lines += ["",
              "// E[wDALY averted per $]: each org's direct effect times the moral",
              "// coefficient this worldview's assumption chain puts on it.",
              "scored = ["]
    for org in SLATE:
        lines.append(f'  {{ name: "{org["name"]}", wdalyPerUsd: {value_expression(org)} }},')
    lines += ["]",
              "",
              "ranking = List.reverse(List.sortBy(scored, {|x| x.wdalyPerUsd}))",
              "best = ranking[0]",
              "",
              "// The expected value of THIS worldview: what its best buy achieves.",
              "worldviewEv = best.wdalyPerUsd"]
    return "\n".join(lines) + "\n"
