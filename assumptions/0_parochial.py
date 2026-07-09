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
# daly_per_usd = [lo, hi] lognormal 90% CI for the direct effect on the org's
# PRIMARY beneficiary, before any moral weighting. Order-of-magnitude BOTECs:
# the soup kitchen is a worked example; animal figures trace to published EA
# Forum CEAs (source_url); human/future/x-risk figures are placeholders.
SLATE = [
    {"id": "soup_kitchen", "name": "Local soup kitchen", "domain": "local_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "worked BOTEC",
     "botec": {"people_helped_per_usd": [0.05, 0.5],
               "wellbeing_gain_daly": [0.001, 0.01],
               "counterfactual_bank_value": 0.3}},
    {"id": "gd", "name": "GiveDirectly", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "placeholder", "daly_per_usd": [0.005, 0.02]},
    {"id": "amf", "name": "GiveWell top charity (AMF)", "domain": "global_human",
     "animal": False, "averts_intense_suffering": True, "neurons": 8.6e10,
     "source": "baseline", "daly_per_usd": [0.02, 0.1]},
    {"id": "aim", "name": "AIM / Charity Entrepreneurship", "domain": "global_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "placeholder", "daly_per_usd": [0.001, 0.1]},
    {"id": "thl", "name": "The Humane League", "domain": "farmed_animal",
     "animal": True, "averts_intense_suffering": True, "neurons": 2.2e8,
     "source": "published",
     "source_url": "https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken",
     "daly_per_usd": [1, 30]},
    {"id": "swp", "name": "Shrimp Welfare Project", "domain": "invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "source": "published",
     "source_url": "https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane",
     "daly_per_usd": [10, 5000]},
    {"id": "wildbugs", "name": "Wild insects (humane pesticides)", "domain": "wild_invertebrate",
     "animal": True, "averts_intense_suffering": True, "neurons": 1e5,
     "source": "published (order of magnitude; per-individual range is a placeholder)",
     "source_url": "https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane",
     "daly_per_usd": [50, 50000]},
    {"id": "allfed", "name": "ALLFED", "domain": "future_human",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "placeholder", "daly_per_usd": [0.01, 10]},
    {"id": "redwood", "name": "AI safety (Redwood Research)", "domain": "xrisk_future",
     "animal": False, "averts_intense_suffering": False, "neurons": 8.6e10,
     "source": "placeholder", "daly_per_usd": [0.001, 1e6]},
]


# ---- point estimates (mirror Squiggle's mean of a lognormal 90% CI) ----------
def lognormal_mean(lo, hi):
    """E[X] for the lognormal whose 90% CI is [lo, hi] — exactly what Squiggle's
    mean(lo to hi) returns, so the Python-side ranking agrees with the model."""
    mu = (math.log(lo) + math.log(hi)) / 2
    sigma = (math.log(hi) - math.log(lo)) / (2 * 1.6448536269514722)
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


def squiggle_dist(org):
    """Squiggle source for the org's direct-effect distribution."""
    if "botec" in org:
        b = org["botec"]
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
