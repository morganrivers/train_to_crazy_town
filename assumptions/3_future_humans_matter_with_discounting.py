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
    """NEW parameter: the pure-time discount applied to far-future value. Future
    people are still IN the circle — dropping the discount is a separate
    assumption — but almost all of the astronomical future's value sits millions
    of years out, and ANY positive pure-time rate, compounded over that span,
    drives its present value to nearly zero. So a moderate longtermist who keeps
    a positive rate finds the far future heavily attenuated and present global
    health still on top; ~1e-6 stands for that near-total suppression. This is
    exactly why strong longtermism needs a pure rate of ~0 (Ramsey, Stern,
    Greaves & MacAskill) — the next assumption drops it to 1."""
    return 1e-6


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
