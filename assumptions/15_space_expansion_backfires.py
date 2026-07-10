"""Assumption 15 — early space expansion re-arms the hazard (sweet-spot view).

The pessimistic reading of the same hazard curve, and the direct rebuttal to
`time_of_perils_exit`: a civilization technologically able to settle another
planet is, by the same capability, able to move asteroids, wage interplanetary
rivalry, and export unresolved geopolitics off-world. Deudney (Dark Skies,
2020) argues space expansionism under anything like current nationalism
CREATES more existential risk than it retires — orbital and asteroid-deflection
infrastructure is inherently dual-use, and inter-settlement anarchy is a harder
security dilemma than the terrestrial one. The Weinersmiths (A City on Mars,
2023; 80,000 Hours podcast #187) add the empirical half: genuinely
self-sufficient, decorrelated settlements — the thing that would actually close
the window — are much further away than the settlement boosterism assumes, so
the "exit" stays open for centuries while the new capability risks arrive
early.

The upshot is a SWEET-SPOT argument, not doom: below some large number of
genuinely independent settlements the marginal planet adds correlated risk
rather than insurance, so accelerating the technology BEFORE geopolitics
matures is net-negative, and the right policy is to slow-walk expansion until
it isn't. For the slate that means the perils window is much LONGER than the
optimistic fork assumes and the expected future correspondingly smaller —
x-risk work still matters (the window still has to be survived), but its
astronomical multiplier is trimmed rather than inflated.

WRAPS `uncertain_factors` with a <1 multiplier on the shared astronomical
future of BOTH future-facing orgs, mirror-image of `time_of_perils_exit`
(mutually exclusive). Requires `no_discounting_future_humans`.
"""

NAME = "space_expansion_backfires"
LABEL = "Early space expansion\nre-arms the hazard"
EDGE_LABEL = "settling space too early creates more risk than it retires"
FIGURES = ["Daniel Deudney", "Kelly & Zach Weinersmith"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = ["time_of_perils_exit"]
TERMINAL = False
DESC = (
    "The sweet-spot view: the capability that settles planets also moves "
    "asteroids and exports nationalism off-world (Deudney, Dark Skies), and "
    "genuinely decorrelated self-sufficient settlements are far further away "
    "than boosterism assumes (Weinersmiths, A City on Mars) — so below a large "
    "number of independent settlements, expansion ADDS anthropogenic risk, and "
    "accelerating it before geopolitics matures is net-negative. The perils "
    "window stays open far longer, the expected future shrinks, and x-risk "
    "work keeps its urgency but loses most of its astronomical multiplier. "
    "Mutually exclusive with the time-of-perils-exit reading."
)

# Multiplier on the shared astronomical future under the backfire reading: the
# window stays open for a long interplanetary-anarchy era, so the expected
# future sits well below the baseline. 90% CI, mean ~0.19 — trimmed, not
# zeroed: the window still has to be survived, and once enough settlements are
# genuinely independent the exit eventually arrives.
SPACE_BACKFIRE_MULTIPLIER_CI = (0.02, 0.6)

_pre_space_backfire_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: both future-facing orgs' astronomical future is trimmed by the
    backfire multiplier — the full distribution in the model, its exact mean
    in the ranking."""
    fs = _pre_space_backfire_uncertain_factors(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        fs.append(lognormal_factor(  # noqa: F821
            "spaceBackfireMultiplier", *SPACE_BACKFIRE_MULTIPLIER_CI,
            "trim on the expected future while early expansion re-arms the "
            "hazard (Deudney's dual-use asteroid/orbital infrastructure; "
            "Weinersmiths on how far off real self-sufficiency is)"))
    return fs
