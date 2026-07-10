"""Assumption 13 — a societal collapse would degrade the future for good.

The opposite reading of a survivable collapse: rather than teaching, it locks in
a permanently worse trajectory. Survivors, traumatised by the technologies that
nearly killed them, become durably tech-averse and stagnate; institutions and
accumulated knowledge do not recover; a smaller, poorer, more brutal world
persists indefinitely. On this view a survivable collapse is far WORSE than a
naive "civilization bounces back" model assumes — closer in badness to
extinction — so PREVENTING it (resilient-food work) is worth much MORE.

This WRAPS `uncertain_factors` with a far-future trajectory multiplier ABOVE 1
on ALLFED (domain `future_human`). It is the mutually exclusive twin of
`collapse_teaches_better_future`. Enough upward revaluation flips the longtermist
best buy from AI safety to ALLFED — the winner is arithmetic on this fork, not a
thumb on the scale. Requires `no_discounting_future_humans`.
"""

NAME = "collapse_degrades_future"
LABEL = "Collapse reroll:\nsurvivors stagnate"
EDGE_LABEL = "a survivable collapse locks in a worse future, so preventing it is worth more"
FIGURES = ["Nick Bostrom", "Toby Ord"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = ["collapse_teaches_better_future", "resilience_undermines_deterrence"]
TERMINAL = False
DESC = (
    "Collapse-as-reroll, pessimistic: survivors become durably tech-averse and "
    "stagnate, locking in a permanently degraded future close in badness to "
    "extinction — so preventing a survivable collapse is worth much more, and "
    "resilient foods (ALLFED) can overtake AI safety. The opposite of "
    "collapse_teaches_better_future. Requires the undiscounted far future."
)

# Multiplier on ALLFED's (collapse-averting) far-future value under the
# pessimistic reroll: a 90% CI above 1 (mean ~15), since a locked-in worse
# trajectory makes averting collapse far more valuable. The upper tail treats a
# permanently degraded future as approaching the badness of extinction.
COLLAPSE_DEGRADES_CI = (2.0, 50.0)

_pre_collapse_degrades_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: ALLFED's collapse-averting value is inflated by the pessimistic
    reroll multiplier — full distribution in the model, exact mean in the ranking."""
    fs = _pre_collapse_degrades_uncertain_factors(org)
    if org["domain"] == "future_human":
        fs.append(lognormal_factor(  # noqa: F821
            "collapseFutureMultiplier", *COLLAPSE_DEGRADES_CI,
            "far-future value of averting a survivable collapse, pessimistic "
            "reroll (survivors stagnate): >1, a locked-in worse world"))
    return fs
