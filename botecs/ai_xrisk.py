"""botecs/ai_xrisk.py — AI existential-risk reduction (Redwood Research).

Value = x-risk-reduced-per-dollar * futureDalysAtStake, sharing the SAME
astronomical future as ALLFED.

This is the STRUCTURAL derivation. The single load-bearing input,
`redwoodXRiskReducedPerDollar`, is the model's most consequential
`expert-judgment` number — Linch's aggregation of forecaster intuitions on
"$ per 0.01% x-risk", not a mechanism. The `ai_xrisk_decomposed` botec below
re-derives it from Carlsmith's six-premise decomposition of P(AI catastrophe)
and a marginal-risk-per-dollar of alignment funding, so the number becomes
editable at the level of its parts.
"""
from botecs.base import Botec, Factor, register
from botecs.future import FUTURE_DALYS_AT_STAKE

register(Botec(
    "redwood",
    terms=[("redwoodXRiskReducedPerDollar", "futureDalysAtStake")],
    factors={
        "redwoodXRiskReducedPerDollar": Factor(
            "redwoodXRiskReducedPerDollar", "lognormal", (1e-13, 1e-12),
            "expert-judgment",
            "Linch's ~$100M-$1B per 0.01% x-risk bar (forecaster aggregate). "
            "See `ai_xrisk_decomposed` for a Carlsmith-based worked alternative.",
            source="https://forum.effectivealtruism.org/posts/cKPkimztzKoCkZ75r/how-many-ea-2021-usds-would-you-trade-off-against-a-0-01"),
        "futureDalysAtStake": FUTURE_DALYS_AT_STAKE,
    },
    doc="Linch's ~$100M-$1B per 0.01% x-risk reduction x the SAME astronomical "
        "future as ALLFED (Bostrom; Cotra timelines). Worked BOTEC; central "
        "mean ~5.8k undiscounted DALY/$.",
    source_url="https://forum.effectivealtruism.org/posts/cKPkimztzKoCkZ75r/how-many-ea-2021-usds-would-you-trade-off-against-a-0-01"))
