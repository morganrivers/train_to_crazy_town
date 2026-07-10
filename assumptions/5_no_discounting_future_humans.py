"""Assumption 4 — no discounting of future humans.

The full longtermist move: a person's moment in time is as morally irrelevant
as their location. This assumption CHANGES A PARAMETER — it collapses
`future_discount_ci` (added by assumption 4, a 90% CI with mean ~0.01) to
exactly 1 — and REDEFINES `moral_weight` so existential-risk work (which buys
the whole undiscounted future) enters the circle. Everything else in the chain
is untouched: assumption 4's factor still multiplies every future-facing org,
now pinned at 1 (and shown as such in the generated model).
"""

NAME = "no_discounting_future_humans"
LABEL = "No pure-time discount\n(astronomical stakes)"
EDGE_LABEL = "drop the pure-time discount"
FIGURES = ["Toby Ord", "Nick Bostrom"]
REQUIRES = ["future_humans_matter_with_discounting"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Accept that future people count exactly as much as present ones (Ord, "
    "MacAskill) and Bostrom's astronomical-waste argument follows: the expected "
    "size of the future dwarfs the present, and reducing existential risk "
    "dominates everything measurable. This is the stop Ajeya Cotra's "
    "near-termist deliberately gets off before."
)

_no_xrisk_moral_weight = moral_weight  # noqa: F821


def future_discount_ci():
    """PARAMETER CHANGED: assumption 4 gave a 90% CI with mean ~0.01; the
    moment in time a person lives is now as irrelevant as where they live, so
    the distribution collapses to exactly 1 — not an estimate any more but an
    ethical commitment (Ord, MacAskill), which is why it carries no
    uncertainty."""
    return (1.0, 1.0)


def moral_weight(domain):
    """REDEFINED: undiscounted future stakes put x-risk work inside the circle."""
    if domain == "xrisk_future":
        return 1.0
    return _no_xrisk_moral_weight(domain)
