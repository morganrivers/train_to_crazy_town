"""Assumption 11 — count soil animals.

The far end of the animal train. Vasco Grilo argues that once invertebrates
count, the dominant welfare effect of almost any intervention runs through SOIL
animals — nematodes, mites and springtails, ~10^19 of them — whose numbers dwarf
every farmed or directly-affected animal. Human global-health charities keep
people alive and richer, which raises food demand and cropland: Grilo estimates
GiveWell's top charities increase cropland ~137 m^2-year per dollar, translating
to ~1.11 kQALY per dollar of soil-animal welfare change. With soil-animal lives
net-negative (his central case), that dollar of global health causes far more
soil-animal suffering than human benefit, so GiveWell's top charities come out
firmly net-negative — the "GiveWell may have made harmful grants" conclusion.

This assumption WRAPS `externality` to charge cropland-expanding human orgs for
the net-negative soil-animal welfare their beneficiaries' extra food demand
causes. Whether that flips a human charity to net-negative is then arithmetic on
Grilo's cropland figure, not a chosen result.

Requires `animals_matter_a_lot`: soil animals only enter once invertebrates are
already in the moral circle with real welfare ranges.
"""

NAME = "soil_animals"
LABEL = "Count soil animals\n(~10^19 nematodes)"
EDGE_LABEL = "count the ~10^19 soil invertebrates"
FIGURES = ["Vasco Grilo"]
REQUIRES = ["animals_matter_a_lot"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Grilo's soil-animal accounting: ~10^19 soil nematodes, mites and "
    "springtails dominate the welfare effects of almost anything. Global-health "
    "charities raise food demand and cropland (~137 m^2-yr/$ for GiveWell top "
    "charities, ~1.11 kQALY/$ of soil-animal welfare change); with soil lives "
    "net-negative, the arithmetic makes GiveWell's top charities net-harmful. "
    "Only enters once invertebrates already count, so it requires "
    "animals_matter_a_lot."
)

# Grilo, "Cost-effectiveness accounting for soil nematodes, mites, and
# springtails" and "GiveWell may have made 1 billion dollars of harmful grants..."
# (https://forum.effectivealtruism.org/posts/Rjutj7Jd2v2KHvDyA ). He estimates
# GiveWell top charities cause ~1.11 kQALY/$ of soil-animal welfare change; at
# their ~0.00994 human DALY/$ that is ~1.1e5 units of soil-animal welfare per
# human DALY of benefit. Soil lives taken as net-negative (Grilo: ~55-59% chance
# negative for nematodes/mites/springtails), so the sign is a harm.
SOIL_WELFARE_PER_HUMAN_DALY = 1.1e5
_MEAT_EATING_DOMAINS = ("local_human", "global_human")

_pre_soil_externality = externality  # noqa: F821


def externality(org):
    """WRAPPED: cropland-expanding human orgs are charged for the net-negative
    soil-animal welfare their beneficiaries' extra food demand causes. This is
    the whole content of the assumption — an EMPIRICAL externality grounded in
    Grilo's cropland figure, not a thumb on the scale for any org: whether it
    makes human charities net-negative is arithmetic once you accept the ~1.11
    kQALY/$ estimate."""
    ext = _pre_soil_externality(org)
    if org["domain"] in _MEAT_EATING_DOMAINS:
        ext -= direct_daly_per_usd(org) * SOIL_WELFARE_PER_HUMAN_DALY  # noqa: F821
    return ext
