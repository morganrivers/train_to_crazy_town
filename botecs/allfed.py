"""botecs/allfed.py — resilient foods for global catastrophe (ALLFED).

Value = near-term lives fed if a nuclear-winter-scale catastrophe strikes,
PLUS the far-future value of averting a civilization-ending collapse:

    P(catastrophe) * livesSaved/$ * DALYs/life
  + P(catastrophe) * P(civ-ending | catastrophe) * riskShareRemoved/$
                   * futureDalysAtStake

The far-future term shares `futureDalysAtStake` with AI safety, so the
longtermist ALLFED-vs-AI-safety comparison is arithmetic on the two orgs'
x-risk-reduced-per-dollar, not a chosen result (Denkenberger & Pearce vs Linch).

This is the STRUCTURAL derivation. Its inputs are improved in place — the
`nuclear` botec below re-derives P(catastrophe) from Rodriguez's per-year
nuclear-war estimate rather than a conference-survey range, and is offered as an
alternative estimate for this org's headline probability.
"""
from botecs.base import Botec, Factor, register
from botecs.future import FUTURE_TERM, FUTURE_FACTORS

register(Botec(
    "allfed",
    terms=[
        ("allfedPCatastrophePerCentury", "allfedLivesSavedPerDollarIfCatastrophe",
         "allfedDalyPerLife"),
        ("allfedPCatastrophePerCentury", "allfedPCivEndGivenCatastrophe",
         "allfedRiskShareRemovedPerDollar") + FUTURE_TERM,
    ],
    factors={
        "allfedPCatastrophePerCentury": Factor(
            "allfedPCatastrophePerCentury", "lognormal", (0.003, 0.05),
            "expert-judgment",
            "P(nuclear-winter-scale ag catastrophe this century). Assumption 10 "
            "(resilience_undermines_deterrence) re-anchors this to Rodriguez's "
            "~0.4%/yr US-Russia estimate as an alternative, higher figure.",
            source="https://rethinkpriorities.org/research-area/how-likely-is-a-nuclear-exchange-between-the-us-and-russia/"),
        "allfedLivesSavedPerDollarIfCatastrophe": Factor(
            "allfedLivesSavedPerDollarIfCatastrophe", "lognormal", (0.02, 2),
            "worked-external",
            "Denkenberger & Pearce alternate-food lives saved per $ GIVEN the catastrophe",
            source="https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176"),
        "allfedDalyPerLife": Factor(
            "allfedDalyPerLife", "point", (30,),
            "empirical-anchor", "DALYs per life saved (age-weighted young life)"),
        "allfedPCivEndGivenCatastrophe": Factor(
            "allfedPCivEndGivenCatastrophe", "lognormal", (0.005, 0.1),
            "expert-judgment",
            "chance the catastrophe is permanently civilization-ending"),
        "allfedRiskShareRemovedPerDollar": Factor(
            "allfedRiskShareRemovedPerDollar", "lognormal", (1e-10, 1e-9),
            "expert-judgment",
            "fraction of that x-risk a marginal resilient-food $ removes"),
        **FUTURE_FACTORS,
    },
    doc="Resilient foods for nuclear-winter / abrupt-sunlight-reduction "
        "catastrophes (Denkenberger & Pearce). Worked BOTEC; central mean "
        "~3.5k undiscounted DALY/$.",
    source_url="https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176"))
