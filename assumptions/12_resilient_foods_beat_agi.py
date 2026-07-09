"""Assumption 12 — resilient foods beat AGI safety on the margin.

A reallocation WITHIN longtermism rather than a step further from common sense.
Denkenberger & Pearce model the long-run cost-effectiveness of resilient foods
for global catastrophes (nuclear winter, abrupt sunlight reduction) against
artificial-general-intelligence safety and find ~98-99% confidence that a
marginal dollar to resilient foods does more far-future good than a marginal
dollar to AGI safety — resilience is more neglected, more tractable and buys a
robust slice of the same astronomical future.

This assumption REDEFINES `expected_values`, `value_expression` and
`dist_expression` for ALLFED: its far-future value is unlocked and set to a
multiple of AI safety's marginal value (rather than its modest near-term GCR
figure) — the multiple being a distribution over the marginal ratio, carried
by name in the generated model — which flips the longtermist winner from AI
safety to ALLFED.

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
# confidence. The advantage is therefore a DISTRIBUTION over the marginal
# ratio, not a point: this 90% CI is calibrated so P(ratio > 1) ~= 98% —
# reproducing the paper's own confidence statement — with mean ~3.4.
RESILIENT_FOODS_VS_AGI_CI = (1.25, 6.9)
RESILIENT_FOODS_VS_AGI = lognormal_mean(*RESILIENT_FOODS_VS_AGI_CI)  # noqa: F821

_AI_SAFETY = "AI safety (Redwood Research)"

_prev_expected_values = expected_values  # noqa: F821
_prev_value_expression = value_expression  # noqa: F821
_prev_dist_expression = dist_expression  # noqa: F821
_prev_squiggle_prelude = squiggle_prelude  # noqa: F821


def _redwood():
    return next(o for o in SLATE if o["id"] == "redwood")  # noqa: F821


def expected_values():
    """REDEFINED: ALLFED's far-future value is a multiple of AI safety's — the
    exact mean of the ratio distribution times AI safety's expected value."""
    ev = _prev_expected_values()
    ev["ALLFED"] = RESILIENT_FOODS_VS_AGI * ev[_AI_SAFETY]
    return ev


def squiggle_prelude():
    """WRAPPED: the model carries the marginal-ratio distribution by name."""
    return _prev_squiggle_prelude() + [
        "// Marginal cost-effectiveness of resilient foods over AGI safety, as a",
        "// distribution calibrated so P(ratio > 1) ~= 98% (Denkenberger & Pearce).",
        f"resilientFoodsVsAgi = {_sym_lognormal(*RESILIENT_FOODS_VS_AGI_CI)}",  # noqa: F821
        "",
    ]


def value_expression(org):
    """REDEFINED for ALLFED: render it as a multiple of AI safety's expression so
    the standalone Squiggle model matches the Python ranking exactly."""
    if org["id"] == "allfed":
        return f"mean(resilientFoodsVsAgi) * ({_prev_value_expression(_redwood())})"
    return _prev_value_expression(org)


def dist_expression(org):
    """REDEFINED for ALLFED: the full ratio distribution, applied to AI safety's
    full distribution."""
    if org["id"] == "allfed":
        return f"resilientFoodsVsAgi * ({_prev_dist_expression(_redwood())})"
    return _prev_dist_expression(org)
