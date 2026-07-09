"""Assumption 1 — far-away humans count.

Peter Singer's famine argument: distance is not morally relevant, so drop the
nationality discount. This assumption REDEFINES `moral_weight`, wrapping the
parochial definition it finds already in the chain's namespace: everything stays
the same except that the whole present generation is now inside the circle.
"""

NAME = "far_away_humans"
LABEL = "All present humans\ncount equally"
EDGE_LABEL = "drop the nationality discount"
FIGURES = ["Alexander Berger", "Peter Singer"]
REQUIRES = []
EXCLUDES = []
TERMINAL = False
DESC = (
    "A life saved abroad counts like a life saved at home, so cheap, measurable "
    "global-health and cash interventions dominate. Alexander Berger is the "
    "prominent exemplar of deliberately getting off the train here and staying "
    "with robust, evidence-backed global health & wellbeing. The soup kitchen's "
    "agreed BOTEC is still carried through untouched; it is simply no longer "
    "the best buy."
)

_parochial_moral_weight = moral_weight  # noqa: F821  (defined earlier in the chain)


def moral_weight(domain):
    """REDEFINED: people count wherever they live."""
    if domain == "global_human":
        return 1.0
    return _parochial_moral_weight(domain)
