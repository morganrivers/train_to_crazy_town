"""Assumption 5 — animals matter a lot.

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

# Rethink Priorities-style median welfare ranges (fraction of a human's),
# https://rethinkpriorities.org/research-area/welfare-range-estimates/ —
# chickens ~0.332, shrimp ~0.031; the insect/soil figure is an illustrative
# nematode-weighted placeholder in the published spirit.
RP_WELFARE_RANGE = {
    "thl": 0.332,
    "swp": 0.031,
    "wildbugs": 0.01,
}

_neuron_proxy_moral_weight = moral_weight  # noqa: F821


def moral_weight(domain):
    """REDEFINED: invertebrates — farmed and wild/soil — are inside the circle."""
    if domain in ("invertebrate", "wild_invertebrate"):
        return 1.0
    return _neuron_proxy_moral_weight(domain)


def welfare_range(org):
    """REDEFINED (replacing assumption 2's neuron-count proxy): RP welfare-range
    point estimates per represented species."""
    if not org["animal"]:
        return 1.0
    return RP_WELFARE_RANGE.get(org["id"], 0.1)
