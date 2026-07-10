"""Assumption 4 — climate damages are civilizational-scale (tipping points).

Take the planetary-boundaries / tipping-points literature at face value:
anthropogenic warming is not a marginal externality but a civilizational-scale
welfare loss within the century. Two published anchors make this a number
rather than a mood:

  * the MORTALITY channel — Bressler's "mortality cost of carbon" (Nature
    Communications, 2021): ~2.26e-4 excess deaths 2020-2100 per tonne CO2 on
    the baseline emissions path (1 death per ~4,434 t), ~6.8e-3 DALY/tCO2 at
    ~30 DALYs per death;
  * the INCOME channel — Kotz, Levermann & Wenz (PIK; Nature, 2024): committed
    damages of ~19% of global income by 2049 (~$38T/yr), falling hardest on
    poor countries; converted to welfare via a log-income (GiveWell-style)
    exchange rate this is the same order as the mortality channel or larger.

On top of the smooth damage functions sits the tipping-point amplification
(Rockström's planetary boundaries; Armstrong McKay et al., Science 2022):
several elements — Greenland/WAIS, AMOC, Amazon dieback, permafrost — have
plausible triggers inside the Paris range, and cascades multiply expected
damages beyond what smooth GDP curves capture.

This assumption REDEFINES `moral_weight` (the `climate` domain enters the
circle) and WRAPS `uncertain_factors` twice: the climate org's tCO2e/$ (its
botec, a measured advocacy cost like Rainforest Trust's hectares/$) is
converted to wDALY by a damage exchange rate plus a tipping multiplier; and —
the interaction with `nature_intrinsic_value`, when a chain holds both — the
conservation org picks up a co-benefit multiplier, because standing tropical
forest IS a tipping element (Amazon dieback) and avoided deforestation is
mitigation. Requires `far_away_humans` (climate damages land mostly on distant
strangers); excludes `no_discounting_future_humans` for the same reason nature
does — under astronomical stakes a within-century damage total, however grim,
is swamped by the far future, so the climate-first worldview is a stop a real
person rides BEFORE the astronomical move, not alongside it.
"""

NAME = "climate_tipping_points"
LABEL = "Climate damages are\ncivilizational-scale"
EDGE_LABEL = "take tipping-point climate damages at face value"
FIGURES = ["Johan Rockström", "Ottmar Edenhofer"]
REQUIRES = ["far_away_humans"]
EXCLUDES = ["no_discounting_future_humans"]
TERMINAL = False
DESC = (
    "Climate change is a civilizational-scale welfare loss, not a marginal "
    "externality: Bressler's mortality cost of carbon (~1 death per 4,434 "
    "tCO2), PIK's committed ~19% income loss by 2049 (Kotz, Levermann & Wenz), "
    "and Rockström / Armstrong McKay tipping-element cascades amplifying both. "
    "Advocacy that cheaply averts emissions (Clean Air Task Force) enters the "
    "slate; where the chain also holds nature's intrinsic value, protecting "
    "tropical forest — itself a tipping element — picks up the co-benefit."
)

# wDALY per tonne CO2e averted, combining the two published channels: Bressler's
# mortality cost of carbon (~6.8e-3 DALY/t central) and the PIK income channel
# (Kotz/Levermann/Wenz ~19% income by 2049, log-income converted). The 90% CI
# spans "mortality only, damages adapt away" to "income channel dominates".
CLIMATE_DALY_PER_TCO2_CI = (2e-3, 2e-2)

# Multiplier for tipping-point amplification beyond smooth damage functions
# (Rockström planetary boundaries; Armstrong McKay et al. 2022: several
# elements plausibly trigger inside the Paris range; cascades compound). The
# low end (~1) is "no amplification"; the upper tail is a cascade.
TIPPING_POINT_MULTIPLIER_CI = (1.0, 6.0)

# Co-benefit multiplier on habitat protection when the chain ALSO values nature
# intrinsically: standing tropical forest is a tipping element (Amazon dieback)
# and a carbon stock, so a protected hectare buys climate insurance on top of
# its existence value.
FOREST_TIPPING_COBENEFIT_CI = (1.0, 4.0)

_pre_climate_moral_weight = moral_weight            # noqa: F821
_pre_climate_uncertain_factors = uncertain_factors  # noqa: F821


def moral_weight(domain):
    """REDEFINED: climate beneficiaries (mostly distant and near-future
    strangers) are inside the circle."""
    if domain == "climate":
        return 1.0
    return _pre_climate_moral_weight(domain)


def uncertain_factors(org):
    """WRAPPED: the climate org's tCO2e/$ is converted to wDALY by the damage
    exchange rate and the tipping multiplier; the conservation org (only when a
    chain that values nature holds it — weight is 0 otherwise) picks up the
    forest-as-tipping-element co-benefit. Full distributions in the model,
    exact means in the ranking."""
    fs = _pre_climate_uncertain_factors(org)
    if org["domain"] == "climate":
        fs.append(lognormal_factor(  # noqa: F821
            "climateDalyPerTco2", *CLIMATE_DALY_PER_TCO2_CI,
            "wDALY per tCO2e averted: Bressler mortality cost of carbon "
            "(~6.8e-3 DALY/t) + PIK income channel (Kotz/Levermann/Wenz ~19% "
            "by 2049, log-income converted)"))
        fs.append(lognormal_factor(  # noqa: F821
            "tippingPointMultiplier", *TIPPING_POINT_MULTIPLIER_CI,
            "tipping-point amplification beyond smooth damages (Rockström "
            "boundaries; Armstrong McKay et al. 2022 cascades)"))
    if org["domain"] == "nature" and moral_weight("nature") > 0:
        fs.append(lognormal_factor(  # noqa: F821
            "forestTippingCobenefit", *FOREST_TIPPING_COBENEFIT_CI,
            "climate co-benefit on protected tropical forest: Amazon dieback "
            "is a tipping element, so a hectare also buys climate insurance"))
    return fs
