"""Assumption 14 — the time of perils has an exit, and space settlement is it.

The optimistic reading of the hazard curve: existential risk is high NOW (the
AI / nuclear transition) but collapses toward zero once humanity passes through
the bottleneck, and becoming durably multiplanetary is the mechanism that
closes the window — no single catastrophe can reach decorrelated,
self-sufficient settlements. If the window really closes, the expected future
is much longer than the background-hazard baseline assumes, so getting through
the bottleneck unlocks everything after it and reducing risk DURING the window
is worth correspondingly more (Ord's "time of perils" framing in The Precipice;
the Musk/Sagan multiplanetary-backup argument).

This is one of two mutually exclusive readings of what space-faring capability
does to the hazard curve; the other (`space_expansion_backfires`) holds that
the same capability re-arms the hazard, which is why the two EXCLUDE each
other. It WRAPS `uncertain_factors` with a >1 multiplier on the shared
astronomical future of BOTH future-facing orgs (ALLFED and AI safety), on top
of the baseline `expectedFutureCenturies` in botecs/future.py — the fork is a
belief about the hazard TRAJECTORY, so it scales the future both orgs buy,
leaving their race arithmetic untouched. Requires
`no_discounting_future_humans`: a claim about the far-future hazard curve only
bites once that future is undiscounted.
"""

NAME = "time_of_perils_exit"
LABEL = "Time of perils:\nspace settlement exits it"
EDGE_LABEL = "the hazard window closes once we are multiplanetary"
FIGURES = ["Toby Ord", "Elon Musk"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = ["space_expansion_backfires"]
TERMINAL = False
DESC = (
    "Time-of-perils optimism: hazard is high during the AI / nuclear "
    "transition but collapses once decorrelated, self-sufficient settlements "
    "exist — no single catastrophe reaches them all. The window closes, the "
    "expected future stretches far past the background-hazard baseline, and "
    "x-risk reduction during the window is what unlocks it (Ord, The "
    "Precipice; the multiplanetary-backup argument). Mutually exclusive with "
    "the view that early expansion re-arms the hazard."
)

# Multiplier on the shared astronomical future (both future-facing orgs) if the
# perils window genuinely closes after settlement: the baseline
# expectedFutureCenturies CI already spans Thorstad pessimism to long space
# futures, so this fork's belief — the exit is REAL and reachable — shifts
# credence toward (and past) that baseline's upper end. 90% CI, mean ~11.
PERILS_EXIT_MULTIPLIER_CI = (2.0, 30.0)

_pre_perils_exit_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: both future-facing orgs' astronomical future is scaled up by
    the perils-exit multiplier — the full distribution in the model, its exact
    mean in the ranking."""
    fs = _pre_perils_exit_uncertain_factors(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        fs.append(lognormal_factor(  # noqa: F821
            "perilsExitMultiplier", *PERILS_EXIT_MULTIPLIER_CI,
            "scale-up of the expected future if the hazard window closes "
            "after multiplanetary settlement (Ord's time of perils; "
            "decorrelated settlements end single-catastrophe risk)"))
    return fs
