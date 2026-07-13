"""Assumption 7 — animals matter a lot.

Take the Rethink Priorities moral-weight work at face value. This assumption
REDEFINES `welfare_range` wholesale — the neuron-count exponent from assumption
2 is thrown away and replaced by RP-style welfare-range point estimates — and
REDEFINES `moral_weight` so invertebrates (shrimp, insects, and the ~10^19 soil
animals: the significant nematode weight) enter the circle.
"""

NAME = "animals_matter_a_lot"
LABEL = "Animals matter a lot\n(RP welfare ranges)"
EDGE_LABEL = "adopt RP welfare ranges + invertebrates"
FIGURES = ["Bob Fischer", "Brian Tomasik"]
REQUIRES = ["animals_somewhat"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Replace the neuron-count proxy with Rethink Priorities' welfare-range "
    "estimates (Fischer et al.) and count invertebrates — shrimp, insects, and "
    "the ~10^19 soil animals. Under RP medians a chicken's welfare range is a "
    "third of a human's, not a fiftieth, and wild/soil invertebrates carry "
    "significant aggregate (nematode) weight, so invertebrate work dominates."
)

# Rethink Priorities median welfare ranges (fraction of a human's), from the
# Moral Weight Project (Fischer et al.):
# https://rethinkpriorities.org/research-area/welfare-range-estimates/
#   chickens 0.332, shrimp 0.031; RP's published insect medians bracket the
#   wild-insect entry — black soldier flies 0.013, silkworms 0.002, bees 0.044 —
#   so ~0.01 is a defensible representative insect welfare range (not a soil
#   nematode figure; assumption 18 handles soil animals explicitly).
#
# JUDGMENT CALL (documented, not a worldview fork). The RP mainline is contested.
# The two-envelope objection (Karnofsky; formalised by Nuno Sempere, "A Bayesian
# Adjustment to Rethink Priorities' Welfare Range Estimates") is that these are
# expectations over deep sentience uncertainty and that the direction you
# normalise cross-species welfare (in human vs animal units) swings the answer by
# orders of magnitude, inflating the smallest, least-understood animals; a
# Bayesian shrink would pull shrimp/insects down ~1-2 OOM. Rethink Priorities
# (Fischer) rebuts that they estimate on a fixed human=1 scale and so do not
# commit the error. Whether to apply the correction is NOT a matter of taste —
# it has a determinate answer given welfare-range realism + EV — but it is a
# METHODOLOGICAL correction, not a moral premise, so it is documented here as a
# judgment call rather than branched as a worldview. We keep the RP mainline
# medians as the baseline (the published, citable standard Grilo's CEAs use) and
# flag the reservation; shrink these values if you find the correction decisive.
RP_WELFARE_RANGE = {
    "thl": 0.332,
    "swp": 0.031,
    "wildbugs": 0.01,
    # wild vertebrates (screwworm hosts): a mammalian welfare range, ~RP pigs 0.515
    "screwworm": 0.5,
}

_neuron_proxy_moral_weight = moral_weight  # noqa: F821


def moral_weight(domain):
    """REDEFINED: wild animals — invertebrate (farmed/wild/soil) and vertebrate
    — are inside the circle."""
    if domain in ("invertebrate", "wild_invertebrate", "wild_vertebrate"):
        return 1.0
    return _neuron_proxy_moral_weight(domain)


def welfare_range(org):
    """REDEFINED (replacing assumption 2's neuron-count proxy): RP welfare-range
    point estimates per represented species."""
    if not org["animal"]:
        return 1.0
    return RP_WELFARE_RANGE.get(org["id"], 0.1)
