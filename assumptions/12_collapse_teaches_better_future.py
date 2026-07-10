"""Assumption 12 — a societal collapse would be a reroll toward a BETTER future.

One reasonable reading of civilizational collapse short of extinction: survivors
carry forward the lessons of the catastrophe and rebuild wiser — more
cooperative, more cautious about the technologies that nearly ended them. If so,
the far-future value of PREVENTING a survivable collapse is much smaller than it
naively looks (some of that value is clawed back by the better rebuild), so
resilient-food work aimed at averting collapse is worth less.

This WRAPS `uncertain_factors` with a far-future trajectory multiplier on ALLFED
(domain `future_human`, whose value is almost entirely its collapse-averting
term). It is one of two mutually exclusive readings of the same event; the other
(`collapse_degrades_future`) takes the opposite view, which is why the two
EXCLUDE each other. Requires `no_discounting_future_humans`: a claim about the
value of the far-future trajectory only bites once that trajectory is undiscounted.
"""

NAME = "collapse_teaches_better_future"
LABEL = "Collapse reroll:\nsurvivors rebuild wiser"
EDGE_LABEL = "a survivable collapse teaches, so preventing it is worth less"
FIGURES = ["Lewis Dartnell"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = ["collapse_degrades_future", "resilience_undermines_deterrence"]
TERMINAL = False
DESC = (
    "Collapse-as-reroll, optimistic: survivors of a near-collapse rebuild wiser "
    "and more cautious, so much of the value of preventing a survivable collapse "
    "is recovered by the better rebuild — resilient-food work aimed at averting "
    "collapse is worth less. The opposite of collapse_degrades_future, so the "
    "two cannot be held together. Requires the undiscounted far future."
)

# Multiplier on ALLFED's (collapse-averting) far-future value under the
# optimistic reroll: a 90% CI well below 1 (mean ~0.3), since a wiser rebuild
# claws back much of the loss; the low tail approaches "collapse was ~neutral".
COLLAPSE_TEACHES_CI = (0.02, 0.8)

_pre_collapse_teaches_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: ALLFED's collapse-averting value is discounted by the optimistic
    reroll multiplier — full distribution in the model, exact mean in the ranking."""
    fs = _pre_collapse_teaches_uncertain_factors(org)
    if org["domain"] == "future_human":
        fs.append(lognormal_factor(  # noqa: F821
            "collapseFutureMultiplier", *COLLAPSE_TEACHES_CI,
            "far-future value of averting a survivable collapse, optimistic "
            "reroll (survivors rebuild wiser): <1, claws back much of the loss"))
    return fs
