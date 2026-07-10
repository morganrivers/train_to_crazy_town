"""Assumption 13 — you are probably a Boltzmann brain.

The last stop: if you are more likely a fleeting thermal fluctuation than an
embodied agent, nothing matters except the brief moments of how you happen to
feel. This assumption REDEFINES `expected_values`, `value_expression` and
`squiggle_prelude`: every charity collapses to the same tiny pleasant-thought
level, so there is nothing to choose between them.

It is TERMINAL: it invalidates every assumption before it, so only one
worldview is generated for it (on its minimal chain).
"""

NAME = "boltzmann_brain"
LABEL = "Boltzmann brain\n(hedonic solipsism)"
EDGE_LABEL = "only this moment's feeling is real"
FIGURES = ["Ludwig Boltzmann"]
REQUIRES = ["living_in_simulation"]
EXCLUDES = ["morality_is_not_real"]
TERMINAL = True
DESC = (
    "If you are more likely a momentary Boltzmann brain than a person with a "
    "past and a future, the only thing that registers is whatever you happen "
    "to feel right now. Every charity collapses to the same low "
    "pleasant-thought level of value; the ranking goes flat and no donation "
    "beats any other."
)

BOLTZMANN_LEVEL = 1e-6      # one fleeting pleasant thought, in wDALY/$
_BOLTZMANN_LEVEL_SQ = "1e-6"  # the same constant as Squiggle source
assert float(_BOLTZMANN_LEVEL_SQ) == BOLTZMANN_LEVEL


def expected_values():
    """REDEFINED: every org yields the same brief pleasant thought."""
    return {org["name"]: BOLTZMANN_LEVEL for org in SLATE}  # noqa: F821


def squiggle_prelude():
    """REDEFINED: the generated model needs the pleasant-thought constant."""
    return [f"boltzmannLevel = {_BOLTZMANN_LEVEL_SQ}  // one fleeting pleasant thought, in wDALY/$", ""]


def value_expression(org):
    """REDEFINED: nothing matters except how this moment happens to feel."""
    return "boltzmannLevel"


def dist_expression(org):
    """REDEFINED: the same fleeting constant — there is no uncertainty left to
    have a distribution over."""
    return "boltzmannLevel"
