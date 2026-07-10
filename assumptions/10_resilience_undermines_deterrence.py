"""Assumption 10 — resilient food undermines nuclear deterrence.

The Peltzman-effect critique of civil defence, applied to resilient foods: if a
nuclear war is more survivable, its deterrent terror is weaker, so the
probability of war rises. A marginal resilient-food dollar therefore buys some
lives-fed-if-catastrophe but also nudges up the chance of the catastrophe it is
insuring against — partly self-defeating. This is a genuine, durable
disagreement about deterrence psychology (no citable determinate answer), so it
is a worldview fork rather than a botec input.

It WRAPS `uncertain_factors` to attach a net-of-deterrence multiplier to ALLFED
(the resilient-food org, domain `future_human`), giving an ALTERNATIVE, lower
estimate of its value. The multiplier is anchored to Rodriguez's ~0.4%/yr
US-Russia nuclear-war estimate (the same figure the `nuclear` view re-derives
ALLFED's catastrophe probability from): the more real the baseline war risk, the
more a deterrence nudge matters.

Requires `no_discounting_future_humans`: ALLFED's value (and any second-order
adjustment to it) only becomes decision-relevant once the far future is
undiscounted; under a positive discount present global health wins regardless.
One of three mutually exclusive nuclear second-order forks (with the two
collapse-reroll readings).
"""

NAME = "resilience_undermines_deterrence"
LABEL = "Resilience erodes\nnuclear deterrence"
EDGE_LABEL = "resilient food weakens deterrence, raising P(war)"
FIGURES = ["Sam Peltzman", "Luisa Rodriguez"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = ["collapse_teaches_better_future", "collapse_degrades_future"]
TERMINAL = False
DESC = (
    "Peltzman effect for civil defence: making nuclear war survivable weakens "
    "deterrence and raises the chance of war, so a resilient-food dollar partly "
    "insures against a catastrophe it also makes marginally likelier. An "
    "alternative, lower estimate for ALLFED, anchored to Rodriguez's ~0.4%/yr "
    "US-Russia war probability. Requires future people to be in the circle."
)

# Fraction of ALLFED's naive expected value that survives once deterrence
# erosion is priced in — a 90% CI, mean ~0.4. Mostly attenuating (the erosion
# cancels much of the benefit); the tail above 1 is the perverse case where a
# higher war probability means more catastrophes for resilient food to mitigate.
DETERRENCE_NET_MULTIPLIER_CI = (0.1, 1.1)

_pre_deterrence_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: ALLFED's value is scaled by the net-of-deterrence multiplier —
    the full distribution in the model, its exact mean in the ranking."""
    fs = _pre_deterrence_uncertain_factors(org)
    if org["domain"] == "future_human":
        fs.append(lognormal_factor(  # noqa: F821
            "deterrenceNetMultiplier", *DETERRENCE_NET_MULTIPLIER_CI,
            "share of ALLFED's benefit surviving deterrence erosion (Peltzman; "
            "Rodriguez ~0.4%/yr US-Russia war); tail >1 is the perverse "
            "more-catastrophes-to-mitigate case"))
    return fs
