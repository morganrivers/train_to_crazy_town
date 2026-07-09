"""Assumption 11 — person-affecting population ethics.

The standard objection that gets people OFF the longtermist train even after
they accept an undiscounted future: adding a happy person who would not
otherwise have existed is not, on person-affecting views, a benefit ("we are in
favour of making people happy, but neutral about making happy people",
Narveson). If merely-possible future people carry no positive weight, the
astronomical case for existential-risk reduction collapses — almost all of that
value was in the vast number of extra future lives extinction would prevent, not
in harm to people who exist regardless.

This assumption WRAPS `coefficient`: future-facing value (x-risk and future
humans) is multiplied by the small fraction that accrues to present and
near-future people who exist either way, rather than to possible future
populations. That knocks AI safety down by ~4-5 orders of magnitude, so the
animal-inclusive longtermist worldviews flip back to near-term animal welfare,
and x-risk stops being astronomically dominant.

Requires `no_discounting_future_humans`: person-affecting neutrality is only
interesting as a response to the undiscounted astronomical-stakes argument; it
is the main population-ethics premise that argument needs.
"""

NAME = "person_affecting_view"
LABEL = "Person-affecting\nview"
EDGE_LABEL = "give merely-possible future people no weight"
FIGURES = ["Jan Narveson", "Melinda Roberts"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Person-affecting population ethics: making happy people is neutral, so the "
    "astronomical case for x-risk reduction — which rests on the sheer number of "
    "extra future lives saved from extinction — loses almost all its force. Only "
    "the harm to people who exist regardless still counts. This is the standard "
    "premise longtermism's critics deny (discussed as the key objection in "
    "Greaves & MacAskill's 'The Case for Strong Longtermism'). It requires "
    "no_discounting_future_humans, the astronomical-stakes move it pushes back on."
)

# Fraction of the value of averting a global catastrophe that accrues to people
# who exist regardless (present + near-future generations) rather than to
# merely-possible future people. Order of magnitude: present life-years at stake
# (~8e9 people x ~40 yr ~ 3e11) over the astronomical future's life-years
# (~1e15-1e16, Bostrom's conservative biological estimate) ~ 3e-5.
PRESENT_PEOPLE_FRACTION = 3e-5

_impersonal_coefficient = coefficient  # noqa: F821


def coefficient(org):
    """WRAPPED: future-facing value keeps only the share going to people who
    exist either way; merely-possible future people carry no weight."""
    c = _impersonal_coefficient(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        c *= PRESENT_PEOPLE_FRACTION
    return c
