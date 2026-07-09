"""Assumption 2 — nonhuman animals count, somewhat.

Extend the moral circle to farmed vertebrates. This assumption REDEFINES
`moral_weight` (farmed animals enter the circle), ADDS a new function
`neuron_count_exponent`, and REDEFINES `welfare_range` to use it: an animal's
welfare range scales like (neurons / human neurons) ^ exponent. Sweeping the
exponent from 0 to 2 swings animal welfare ranges across many orders of
magnitude — the train's first big instability.
"""

NAME = "animals_somewhat"
LABEL = "Animals count\n(neuron-weighted)"
EDGE_LABEL = "add an animal welfare range"
FIGURES = ["Peter Singer", "Lewis Bollard"]
REQUIRES = ["far_away_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Farmed vertebrates enter the circle, weighted by a sentience-adjusted "
    "welfare range (neuron-count exponent). Corporate welfare campaigns avert "
    "enormous suffering per dollar and overtake human global health under most "
    "welfare-range estimates. An animals person won't think only people in "
    "their community matter, so this assumption requires far_away_humans."
)

_humans_only_moral_weight = moral_weight  # noqa: F821


def neuron_count_exponent():
    """NEW parameter: how fast moral weight falls off with brain size."""
    return 0.5


def moral_weight(domain):
    """REDEFINED: farmed animals are inside the circle."""
    if domain == "farmed_animal":
        return 1.0
    return _humans_only_moral_weight(domain)


def welfare_range(org):
    """REDEFINED: animals count in proportion to (neurons/humanNeurons)^exp."""
    if not org["animal"]:
        return 1.0
    return (org["neurons"] / HUMAN_NEURONS) ** neuron_count_exponent()  # noqa: F821
