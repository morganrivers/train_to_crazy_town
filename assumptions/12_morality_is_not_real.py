"""Assumption 12 — morality is not real.

Moral anti-realism (Mackie's error theory): there are no moral facts, so no
charity has any value at all. This assumption REDEFINES `coefficient` and
`value_expression` wholesale — every wDALY goes to 0 and the ranking goes flat.

It is TERMINAL: it invalidates every assumption before it, so only one
worldview is generated for it (on its minimal chain) — combining it with extra
assumptions would produce byte-identical all-zero models.
"""

NAME = "morality_is_not_real"
LABEL = "Morality is not real\n(anti-realism)"
EDGE_LABEL = "deny moral realism"
FIGURES = ["J. L. Mackie"]
REQUIRES = ["living_in_simulation"]
EXCLUDES = ["boltzmann_brain"]
TERMINAL = True
DESC = (
    "Off the end of the line: if moral realism is false there is no "
    "stance-independent reason to help anyone. Every DALY is set to 0 — the "
    "moral circle, welfare ranges, discounting and simulation probabilities "
    "all stop mattering, and the ranking goes flat. The consistent "
    "recommendation is to keep the money."
)


def coefficient(org):
    """REDEFINED: no moral facts, no moral value."""
    return 0.0


def value_expression(org):
    """REDEFINED: sets all DALYs to 0."""
    return "0"


def dist_expression(org):
    """REDEFINED: no moral facts, no distribution over moral value either."""
    return "0"
