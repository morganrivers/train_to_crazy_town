"""botecs/ai_xrisk.py — AI existential-risk reduction (Redwood Research), DECOMPOSED.

Value = x-risk-reduced-per-dollar * (the shared future). The old single input,
`redwoodXRiskReducedPerDollar`, was the model's most consequential
`expert-judgment` number — Linch's aggregation of forecaster intuitions on
"$ per 0.01% x-risk", with no mechanism. It is now a worked product:

    xRiskReducedPerDollar = pAICatastropheThisCentury      (Carlsmith six premises)
                          * fractionRiskAlignmentCanAvert   (how much is addressable)
                          * marginalRiskShareRemovedPerDollar (~ 1 / effective $)

so the number is editable at the level of its parts. Its central value lands
near Linch's elicited figure — an independent cross-check that the mechanism and
the intuition agree, not a coincidence engineered to match.
"""
from botecs.base import Botec, Factor, register
from botecs.future import FUTURE_TERM, FUTURE_FACTORS

_RISK_TERM = ("pAICatastropheThisCentury", "fractionRiskAlignmentCanAvert",
              "marginalRiskShareRemovedPerDollar")

_factors = {
    "pAICatastropheThisCentury": Factor(
        "pAICatastropheThisCentury", "lognormal", (0.03, 0.4),
        "worked-external",
        "P(existential catastrophe from power-seeking AI this century) — "
        "Carlsmith's six-premise decomposition, ~10% central (updated from 5%)",
        source="https://arxiv.org/abs/2206.13353"),
    "fractionRiskAlignmentCanAvert": Factor(
        "fractionRiskAlignmentCanAvert", "lognormal", (0.05, 0.5),
        "expert-judgment",
        "fraction of that risk marginal alignment/control work can counterfactually avert"),
    "marginalRiskShareRemovedPerDollar": Factor(
        "marginalRiskShareRemovedPerDollar", "lognormal", (1e-12, 5e-11),
        "worked-internal",
        "share of the avertable risk a marginal $ removes ~ 1/(effective spend "
        "to remove it): ~$20B-$1T; central lands near Linch's $100M-$1B per 0.01%"),
}

register(Botec(
    "redwood",
    terms=[_RISK_TERM + FUTURE_TERM],
    factors={**_factors, **FUTURE_FACTORS},
    doc="AI x-risk reduction: Carlsmith P(catastrophe) x addressable share x "
        "marginal risk removed per $, times the SAME astronomical future as "
        "ALLFED. Worked BOTEC; central x-risk-per-$ ~ Linch's aggregate.",
    source_url="https://arxiv.org/abs/2206.13353"))
