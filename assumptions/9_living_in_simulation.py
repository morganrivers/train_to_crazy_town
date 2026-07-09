"""Assumption 9 — we are probably living in a simulation.

Bostrom's simulation argument, taken seriously. This assumption ADDS a new
function `simulation_continuation_prob` and WRAPS `coefficient`: the
astronomical future only pays off if the simulation keeps running long enough
for it to happen, so every future-facing org is multiplied by that probability.
Only someone already reasoning expected-value-style about the undiscounted far
future ends up here, so it requires no_discounting_future_humans.
"""

NAME = "living_in_simulation"
LABEL = "Living in\na simulation"
EDGE_LABEL = "take the simulation argument seriously"
FIGURES = ["Nick Bostrom"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "If most observers like us are simulated, the astronomical future that "
    "justified x-risk work probably gets switched off long before it happens. "
    "The same expected-value reasoning that bought astronomical stakes now "
    "attenuates them: future-facing value is multiplied by the probability the "
    "simulation keeps running, and the ranking slides back toward the present."
)

_basement_reality_coefficient = coefficient  # noqa: F821


def simulation_continuation_prob():
    """NEW parameter: P(the simulation runs long enough for the far future)."""
    return 0.1


def coefficient(org):
    """WRAPPED: future-facing value only counts if the simulation continues."""
    c = _basement_reality_coefficient(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        c *= simulation_continuation_prob()
    return c
