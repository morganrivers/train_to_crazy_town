"""Assumption 6 — suffering-focused ethics.

Reducing intense suffering matters more than creating happiness. This
assumption ADDS a new function `suffering_multiplier` and WRAPS `coefficient`
with it: orgs whose work averts intense suffering are weighted up, orgs whose
case rests on creating future flourishing are weighted down.
"""

NAME = "suffering_focused"
LABEL = "Suffering-focused\nethics"
EDGE_LABEL = "weight suffering over happiness"
FIGURES = ["Brian Tomasik", "David Pearce"]
REQUIRES = ["animals_somewhat"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Asymmetry: averting intense suffering takes priority over creating "
    "happiness. Factory farming, malaria and the worst wild-animal conditions "
    "weigh up; speculative future-flourishing bets weigh down. Arises most "
    "naturally from taking animal suffering seriously, so it requires "
    "animals_somewhat."
)

_symmetric_coefficient = coefficient  # noqa: F821


def suffering_multiplier(org):
    """NEW: the suffering/happiness asymmetry, per org."""
    return 3.0 if org["averts_intense_suffering"] else 0.3


def coefficient(org):
    """WRAPPED: the symmetric coefficient times the asymmetry."""
    return _symmetric_coefficient(org) * suffering_multiplier(org)
