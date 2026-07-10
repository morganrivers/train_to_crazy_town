"""botecs/future.py — the astronomical future at stake, SHARED.

The single biggest EV lever in the whole model, and the one most often smuggled
in as a bare stipulation. It is defined ONCE, here, and referenced by both
future-facing botecs (ALLFED and AI safety), so a longtermist comparison of the
two reduces to their x-risk-reduced-per-dollar — arithmetic on the SAME future,
not two independently-chosen astronomical numbers. The confidence Monte-Carlo
draws this factor once per world-state (`shared=True`) and applies the same draw
to both orgs; previously each drew its own, which spuriously decorrelated them.

Provenance is `expert-judgment` at this stop: a five-order-of-magnitude Bostrom
stipulation with no derivation. `ai_xrisk`/`allfed`'s decomposition step
replaces the reference with a worked Newberry-style estimate (expected duration
x population per century) carrying an explicit background-extinction rate.
"""
from botecs.base import Factor

# P5..P95 spanning Bostrom's "Astronomical Waste": ~1e11 for a short Earth-bound
# biological future up to ~1e16+ with long-lived space settlement. Undiscounted
# DALYs preserved if an existential catastrophe is averted.
FUTURE_DALYS_AT_STAKE = Factor(
    "futureDalysAtStake", "lognormal", (1e11, 1e16),
    provenance="expert-judgment",
    comment="astronomical DALYs preserved if extinction is averted (Bostrom, "
            "Astronomical Waste); shared by ALLFED and AI safety",
    source="https://www.nickbostrom.com/astronomical/waste.html",
    shared=True,
)
