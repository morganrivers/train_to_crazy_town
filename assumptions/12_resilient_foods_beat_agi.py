"""Assumption 12 — resilient foods beat AGI safety on the margin.

A reallocation WITHIN longtermism rather than a step further from common sense.
Denkenberger & Pearce model the long-run cost-effectiveness of resilient foods
for global catastrophes (nuclear winter, abrupt sunlight reduction) against
artificial-general-intelligence safety and find ~98-99% confidence that a
marginal dollar to resilient foods does more far-future good than a marginal
dollar to AGI safety — resilience is more neglected, more tractable and buys a
robust slice of the same astronomical future.

This assumption REDEFINES `expected_values` and `value_expression` for ALLFED:
its far-future value is unlocked and set to a multiple of AI safety's marginal
value (rather than its modest near-term GCR figure), which flips the longtermist
winner from AI safety to ALLFED.

Requires `no_discounting_future_humans`: the comparison only matters once the
undiscounted far future is what you are buying.
"""

NAME = "resilient_foods_beat_agi"
LABEL = "Resilient foods beat\nAGI safety"
EDGE_LABEL = "prefer resilient foods to AI safety on the margin"
FIGURES = ["David Denkenberger", "Joshua Pearce"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Denkenberger & Pearce estimate ~98-99% confidence that marginal funding "
    "for resilient foods (feeding everyone through nuclear winter or an abrupt "
    "sunlight-reduction catastrophe) does more far-future good than marginal "
    "AGI-safety funding — it is more neglected and more tractable while buying "
    "the same astronomical future. The longtermist winner flips from AI safety "
    "to ALLFED. A within-longtermism reallocation, so it requires "
    "no_discounting_future_humans."
)

# Denkenberger & Pearce, "Long term cost-effectiveness of resilient foods for
# global catastrophes compared to artificial general intelligence safety"
# (https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176):
# marginal resilient-food funding beats marginal AGI-safety funding with ~98-99%
# confidence. Representative central advantage on the margin:
RESILIENT_FOODS_VS_AGI = 3.0

_AI_SAFETY = "AI safety (Redwood Research)"

_prev_expected_values = expected_values  # noqa: F821
_prev_value_expression = value_expression  # noqa: F821


def expected_values():
    """REDEFINED: ALLFED's far-future value is a multiple of AI safety's."""
    ev = _prev_expected_values()
    ev["ALLFED"] = RESILIENT_FOODS_VS_AGI * ev[_AI_SAFETY]
    return ev


def value_expression(org):
    """REDEFINED for ALLFED: render it as a multiple of AI safety's expression so
    the standalone Squiggle model matches the Python ranking."""
    if org["id"] == "allfed":
        redwood = next(o for o in SLATE if o["id"] == "redwood")  # noqa: F821
        return f"{RESILIENT_FOODS_VS_AGI:g} * ({_prev_value_expression(redwood)})"
    return _prev_value_expression(org)
