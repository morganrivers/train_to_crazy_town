"""Assumption 3 — nature has intrinsic value.

Ecosystems and species matter for their own sake, not only as habitat or
resources for sentient beings. This is one of the LEAST crazy assumptions on the
train — most people say they believe it — which is why it sits early, right after
animals count somewhat.

It is NOT a claim that ecosystems are sentient (they are not, so they cannot
carry welfare directly). The model does what an economist does: it estimates the
value people who hold nature intrinsically valuable actually place on it — a
plausible RANGE — from non-market existence-value / willingness-to-pay studies
(contingent valuation of habitat protection), and converts that to wDALY so it
can be ranked on the same axis as everything else. This is entirely in keeping
with the repo's rule: we are making objective expected-value calculations under
clear assumptions, and we want the believer's NUMBERS (what nature is worth to
them), not their opinion. The revealed personal sacrifice environmental
movements make to protect habitat is a cross-check on that range, not the
headline method.

This assumption REDEFINES `moral_weight` (the `nature` domain enters the circle)
and WRAPS `uncertain_factors` to attach the wDALY-per-hectare exchange rate to
the conservation org — a full distribution in the generated model, its exact
mean in the ranking. Requires `far_away_humans`: valuing distant ecosystems is a
global, impartial stance, not a parochial one.
"""

NAME = "nature_intrinsic_value"
LABEL = "Nature has\nintrinsic value"
EDGE_LABEL = "value ecosystems for their own sake"
FIGURES = ["Aldo Leopold", "Arne Naess"]
REQUIRES = ["far_away_humans"]
EXCLUDES = ["no_discounting_future_humans"]
TERMINAL = False
DESC = (
    "Ecosystems and species have value in themselves, not only as habitat for "
    "sentient beings — a belief most people say they hold, so it rides early on "
    "the train. Not a sentience claim: the value is what non-market "
    "existence-value / willingness-to-pay studies say people who hold nature "
    "intrinsically valuable place on it (cross-checked by the sacrifice "
    "environmental movements make), converted to wDALY. Where animals do not "
    "dominate the circle, habitat protection (Rainforest Trust) can win."
)

# wDALY-equivalent per hectare of habitat durably protected (present value of
# ~perpetual protection). A wide 90% CI: contingent-valuation existence-value
# estimates for tropical habitat span orders of magnitude, and the $-to-wDALY
# conversion (via a value-of-a-DALY) adds more spread. The mean (~0.5 wDALY/ha)
# makes Rainforest Trust a real contender — beating global-health cash where
# animals are not weighted heavily — without dominating the slate.
NATURE_WDALY_PER_HECTARE_CI = (0.01, 2.0)

_pre_nature_moral_weight = moral_weight            # noqa: F821
_pre_nature_uncertain_factors = uncertain_factors  # noqa: F821


def moral_weight(domain):
    """REDEFINED: ecosystems are inside the circle."""
    if domain == "nature":
        return 1.0
    return _pre_nature_moral_weight(domain)


def uncertain_factors(org):
    """WRAPPED: the conservation org's hectares/$ are converted to wDALY by the
    intrinsic-value exchange rate — the full distribution in the model, its
    exact mean in the ranking."""
    fs = _pre_nature_uncertain_factors(org)
    if org["domain"] == "nature":
        fs.append(lognormal_factor(  # noqa: F821
            "natureWdalyPerHectare", *NATURE_WDALY_PER_HECTARE_CI,
            "wDALY-equivalent per hectare protected: non-market existence-value / "
            "WTP for habitat, converted to wDALY (cross-checked by revealed "
            "environmental-movement sacrifice)"))
    return fs
