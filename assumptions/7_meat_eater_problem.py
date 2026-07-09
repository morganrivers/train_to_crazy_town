"""Assumption 7 — the meat-eater problem.

Bringing a human into the world (or keeping one alive, or making one richer)
carries a hidden cost: over a lifetime that person eats animals, and factory
farming those animals causes suffering. So a human-welfare dollar buys human
DALYs AND a stream of farmed-animal life-years. This assumption ADDS the
empirical externality functions and REDEFINES the base `externality` hook to
charge every present-human org for the factory farming its beneficiaries'
diets cause — an ADDITIVE negative term, not just a haircut, so a human charity
can come out net-negative once animals carry enough weight.

Requires `animals_somewhat`: the meat only counts against you once animals are
in the moral circle at all.
"""

NAME = "meat_eater_problem"
LABEL = "Meat-eater problem\n(saved humans eat animals)"
EDGE_LABEL = "charge humans for the meat they eat"
FIGURES = ["Michael Dickens", "Vasco Grilo"]
REQUIRES = ["animals_somewhat"]
EXCLUDES = ["no_discounting_future_humans"]
TERMINAL = False
DESC = (
    "The meat-eater problem: a dollar of human global health also buys decades "
    "of that person's meat consumption, and factory farming it causes suffering "
    "the animal circle now counts. Each present-human org is charged an additive "
    "penalty — farmed-animal life-years caused per human DALY, times the "
    "suffering per factory-farmed life-year, times the animal's welfare range. "
    "Under a heavy animal welfare range the penalty can exceed the human benefit, "
    "so saving human lives looks net-harmful. Only bites once animals count, so "
    "it requires animals_somewhat; and it is a near-term human-vs-animal get-off "
    "point, not combined with astronomical-stakes longtermism "
    "(no_discounting_future_humans), where x-risk dominates and the meat "
    "bookkeeping is moot."
)

# Empirical order-of-magnitude BOTECs (deliberately illustrative):
# a person's diet keeps a handful of farmed land animals (mostly chickens) alive
# on their behalf at any time, so a human life-year drags this many
# farmed-animal life-years behind it. Order-of-magnitude; Grilo's meat-eater
# analysis ("GiveWell may have made 1 billion dollars of harmful grants...",
# https://forum.effectivealtruism.org/posts/FqioYEr97eoCQMxhk ) runs higher once
# fish and shrimp are added, which would only sharpen the sign flip.
FARMED_LIFE_YEARS_PER_HUMAN_DALY = 4.0

# Present-human domains whose beneficiaries go on to eat meat. (Future/x-risk
# orgs are about preventing catastrophe, not sustaining concrete present diets,
# so they are left out of the externality.)
_MEAT_EATING_DOMAINS = ("local_human", "global_human")


def farmed_suffering_per_life_year():
    """Net suffering in one factory-farmed life-year, as a fraction of a human
    DALY BEFORE cross-species welfare scaling. Positive = bad. Modest here (a
    farmed life is bad but not maximally so); `net_negative_animal_lives`
    replaces this with a far larger value."""
    return 0.5


def _representative_farmed():
    """The slate's farmed-animal org, used for the welfare range and moral
    weight the eaten animals carry under the current animal assumption."""
    return next(o for o in SLATE if o["domain"] == "farmed_animal")  # noqa: F821


def externality(org):
    """REDEFINED: present-human orgs pay for the factory farming their
    beneficiaries' diets cause (negative = harm), scaled by however much the
    chain weights a farmed animal."""
    if org["domain"] not in _MEAT_EATING_DOMAINS:
        return 0.0
    farmed = _representative_farmed()
    animal_value = (farmed_suffering_per_life_year()
                    * welfare_range(farmed)              # noqa: F821
                    * moral_weight("farmed_animal"))     # noqa: F821
    return -direct_daly_per_usd(org) * FARMED_LIFE_YEARS_PER_HUMAN_DALY * animal_value  # noqa: F821
