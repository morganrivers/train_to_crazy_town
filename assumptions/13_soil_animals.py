"""Assumption 13 — count soil animals.

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

This assumption does two things:
  1. it WRAPS `uncertain_factors` to boost wild-invertebrate work — the
     slate's proxy for interventions acting on the vast soil-animal population
     — by a distribution whose exact mean feeds the ranking; and
  2. it WRAPS `externality_coefficient` to charge cropland-expanding human orgs
     for the soil-animal suffering their beneficiaries' extra food demand
     causes.

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
    "net-negative, that makes GiveWell's top charities net-harmful, and "
    "soil/wild-invertebrate work dominates the slate. Only enters once "
    "invertebrates already count, so it requires animals_matter_a_lot."
)

# Grilo, "Cost-effectiveness accounting for soil nematodes, mites, and
# springtails" and "GiveWell may have made 1 billion dollars of harmful grants..."
# (https://forum.effectivealtruism.org/posts/Rjutj7Jd2v2KHvDyA ). He estimates
# GiveWell top charities cause ~1.11 kQALY/$ of soil-animal welfare change; at
# their ~0.00994 human DALY/$ that is ~1.1e5 units of soil-animal welfare per
# human DALY of benefit. Soil lives taken as net-negative (Grilo: ~55-59% chance
# negative for nematodes/mites/springtails), so the sign is a harm. A 90% CI
# spanning more than an order of magnitude each way around his central figure
# (cropland-per-DALY, soil density and welfare-per-animal are all uncertain),
# calibrated so its lognormal MEAN reproduces his ~1.1e5 central estimate.
SOIL_WELFARE_PER_HUMAN_DALY_CI = (2e4, 3e5)
SOIL_WELFARE_PER_HUMAN_DALY = lognormal_mean(*SOIL_WELFARE_PER_HUMAN_DALY_CI)  # noqa: F821
_MEAT_EATING_DOMAINS = ("local_human", "global_human")

# Soil/wild invertebrates are the largest affected population, so wild-invert
# work (the slate's proxy for acting on them) is scaled up over farmed inverts
# — a 90% CI (mean ~5.1) rather than a point, since the scale-up inherits the
# soil-population and welfare-density uncertainty above.
SOIL_SCALE_BOOST_CI = (1.4, 12)

_pre_soil_uncertain_factors = uncertain_factors  # noqa: F821
_pre_soil_externality_coefficient = externality_coefficient  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: wild-invertebrate work stands in for the dominant soil-animal
    population and is scaled up accordingly — the full distribution in the
    model, its exact mean in the ranking."""
    fs = _pre_soil_uncertain_factors(org)
    if org["domain"] == "wild_invertebrate":
        fs.append(lognormal_factor(  # noqa: F821
            "soilScaleBoost", *SOIL_SCALE_BOOST_CI,
            "wild-invert work proxies the ~10^19 soil animals (Grilo)"))
    return fs


def externality_coefficient(org):
    """WRAPPED: cropland-expanding human orgs are charged for the net-negative
    soil-animal welfare their beneficiaries' extra food demand causes, PER
    direct human DALY — the charge rides the org's own uncertain direct-effect
    distribution (Grilo's accounting is itself proportional to the human
    benefit delivered)."""
    ext = _pre_soil_externality_coefficient(org)
    if org["domain"] in _MEAT_EATING_DOMAINS:
        ext -= SOIL_WELFARE_PER_HUMAN_DALY
    return ext
