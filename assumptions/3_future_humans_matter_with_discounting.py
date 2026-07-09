"""Assumption 3 — future humans matter, with discounting.

Future people enter the circle, but a pure-time discount keeps them from
dominating. This assumption REDEFINES `moral_weight` (future humans enter the
circle), ADDS a new function `future_discount`, and WRAPS `coefficient` so the
discount multiplies every future-facing org.
"""

NAME = "future_humans_matter_with_discounting"
LABEL = "Future humans count\n(discounted)"
EDGE_LABEL = "count future people, discounted"
FIGURES = ["Frank Ramsey", "Tyler Cowen"]
REQUIRES = ["far_away_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Future people are inside the circle, but with a positive pure-time "
    "discount rate — the moderate longtermist position. A modest discount is "
    "enough to keep present, measurable global health competitive with "
    "future-protecting work; remove it (the next assumption) and the "
    "astronomical numbers take over."
)

_present_only_moral_weight = moral_weight  # noqa: F821
_undiscounted_coefficient = coefficient    # noqa: F821


def future_discount():
    """NEW parameter: the pure-time discount on future people. Even a heavy
    discount leaves them IN the circle — dropping it is a separate assumption.
    0.01 stands for the aggregate attenuation a moderate positive pure-time
    preference plus catastrophe/extinction hazard puts on far-future value
    (Ramsey and Stern argue the pure rate should be ~0; Cowen/Nordhaus defend a
    positive one — the moderate-longtermist compromise keeps the far future
    counting but not dominating)."""
    return 0.01


def moral_weight(domain):
    """REDEFINED: future humans are inside the circle."""
    if domain == "future_human":
        return 1.0
    return _present_only_moral_weight(domain)


def coefficient(org):
    """WRAPPED: future-facing value is discounted."""
    c = _undiscounted_coefficient(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        c *= future_discount()
    return c
