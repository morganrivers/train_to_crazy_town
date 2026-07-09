"""Assumption 8 — animals' lives are net-negative.

The net-negative-lives hypothesis: for factory-farmed and wild animals alike,
a typical life contains more suffering than wellbeing, so the life is not worth
living. This assumption does two things:

  1. it CHANGES A PARAMETER — redefines `farmed_suffering_per_life_year_ci()`
     (the hook the meat-eater problem reads) to a much larger CI, so IF this
     chain also holds the meat-eater problem, creating a farmed life is a
     severe harm and human charities are driven firmly net-negative; and
  2. it WRAPS `coefficient` to boost suffering-reducing animal work — averting
     suffering in a life that is ALL suffering is worth more than nudging a
     decent life, and the effect is largest for the vast net-negative wild
     invertebrate populations.

Requires `animals_matter_a_lot`: taking wild and invertebrate lives seriously
enough to call them net-negative presupposes counting them in the first place.
"""

NAME = "net_negative_animal_lives"
LABEL = "Net-negative lives\n(animal suffering dominates)"
EDGE_LABEL = "hold that animal lives aren't worth living"
FIGURES = ["Brian Tomasik", "David Benatar"]
REQUIRES = ["animals_matter_a_lot"]
EXCLUDES = ["no_discounting_future_humans"]
TERMINAL = False
DESC = (
    "The net-negative-lives hypothesis: factory-farmed and wild animals endure "
    "more suffering than wellbeing, so their lives are not worth living. "
    "Reducing that suffering is worth more per dollar (you are mitigating a "
    "catastrophe, not improving a good life), most of all for the astronomical "
    "wild-invertebrate populations. Combined with the meat-eater problem it "
    "drives human charities firmly net-negative — every human sustained means "
    "more net-negative farmed lives. Presupposes counting wild/invertebrate "
    "animals, so it requires animals_matter_a_lot; and like the meat-eater "
    "problem it is a near-term animal get-off point, not combined with "
    "astronomical-stakes longtermism (no_discounting_future_humans)."
)

# How much worse than "neutral" a net-negative life-year is, replacing the
# meat-eater problem's milder default: a farmed life is now dominated by
# suffering (a whole DALY-plus of it per life-year in expectation; the 90% CI
# has mean ~2.1). The net-negative-lives hypothesis for farmed and wild
# animals is Tomasik's
# (https://reducing-suffering.org/the-importance-of-wild-animal-suffering/),
# with the philosophical asymmetry from Benatar ("Better Never to Have Been",
# 2006: an absent good is not bad, an absent harm is good); the CI is an
# order-of-magnitude stand-in for how far past "not worth living" a caged
# life falls.
_NET_NEGATIVE_SUFFERING_PER_LIFE_YEAR_CI = (0.6, 5)

# Extra value on suffering-reduction once the baseline life is net-negative,
# by domain — largest for the vast wild-invertebrate populations. These are
# RELATIVE weightings between domains (like the welfare-range table), not
# independent empirical quantities, so they stay point values by design.
_SUFFERING_REDUCTION_BOOST = {
    "farmed_animal": 2.0,
    "invertebrate": 3.0,
    "wild_invertebrate": 5.0,
}

_pre_net_negative_coefficient = coefficient  # noqa: F821


def farmed_suffering_per_life_year_ci():
    """PARAMETER CHANGED: a farmed life-year is now severely net-negative. Read
    by the meat-eater externality (if this chain holds it), so the penalty on
    human charities grows accordingly."""
    return _NET_NEGATIVE_SUFFERING_PER_LIFE_YEAR_CI


def coefficient(org):
    """WRAPPED: averting suffering in net-negative lives is worth more."""
    return _pre_net_negative_coefficient(org) * _SUFFERING_REDUCTION_BOOST.get(org["domain"], 1.0)
