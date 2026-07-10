"""Assumption 10 — two-envelope skepticism about invertebrate welfare ranges.

A counter-move you meet once you are deep in animal prioritisation: Rethink
Priorities' mainline welfare ranges are expectations taken over deep uncertainty
about whether tiny-brained animals are sentient at all, and cross-species
comparisons of "one unit of welfare" run into the two-envelope problem — which
way you normalise (in human units or animal units) swings the answer by orders
of magnitude. Nuño Sempere's Bayesian adjustment argues the mainline point
estimates are inflated for the smallest, least-understood animals and should be
shrunk by one to two orders of magnitude, most of all for invertebrates.

This assumption WRAPS `uncertain_factors` with a per-domain Bayesian shrink on
the RP table from assumption 5 — a distribution in the generated model (the
size of the shrink is itself deeply uncertain), its exact mean in the ranking.
Chickens (vertebrate, comparatively well-evidenced) are untouched; shrimp and
insects are pulled down ~2 orders of magnitude in expectation, which flips the
animal winner from the Shrimp Welfare Project / wild insects back to corporate
chicken campaigns.

Requires `animals_matter_a_lot`: there is nothing to be skeptical about until
the RP welfare ranges are on the table. Excludes the two assumptions that lean
the OTHER way on invertebrate sentience — you do not simultaneously discount
invertebrate welfare AND maximise it (`net_negative_animal_lives`) or count
~10^19 soil invertebrates (`soil_animals`).
"""

NAME = "two_envelope_welfare_skepticism"
LABEL = "Two-envelope welfare\nskepticism"
EDGE_LABEL = "Bayesian-shrink invertebrate welfare ranges"
FIGURES = ["Nuno Sempere"]
REQUIRES = ["animals_matter_a_lot"]
EXCLUDES = ["net_negative_animal_lives", "soil_animals"]
TERMINAL = False
DESC = (
    "Rethink Priorities' mainline welfare ranges are expectations over deep "
    "sentience uncertainty, and cross-species welfare comparisons hit the "
    "two-envelope problem. Nuno Sempere's Bayesian adjustment shrinks the "
    "smallest animals' welfare ranges by one to two orders of magnitude. "
    "Chickens are barely affected; shrimp and insects fall far enough that "
    "corporate chicken campaigns retake the top of the animal slate. Only "
    "bites once the RP welfare ranges are in play, so it requires "
    "animals_matter_a_lot."
)

# Nuno Sempere, "A Bayesian Adjustment to Rethink Priorities' Welfare Range
# Estimates" (https://nunosempere.com/blog/2023/02/19/bayesian-adjustment-to-
# rethink-priorities-welfare-range-estimates/). Per-domain shrink of the RP
# point estimate, each a 90% CI (the whole point of the adjustment is that the
# right shrink is itself deeply uncertain): vertebrate farmed animals are
# comparatively well-evidenced so they keep their range; the smallest, most
# sentience-uncertain animals take the largest haircut — ~2 orders of
# magnitude in expectation (means ~0.005 shrimp, ~0.002 insects).
WELFARE_RANGE_SHRINK_CI = {
    "invertebrate": (0.0008, 0.015),      # shrimp
    "wild_invertebrate": (0.0003, 0.006),  # insects: even less certain
}

_mainline_rp_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: invertebrate welfare ranges carry a Bayesian shrink — the full
    distribution in the model, its exact mean in the ranking. Chickens
    (well-evidenced vertebrates) are untouched."""
    fs = _mainline_rp_uncertain_factors(org)
    if org["domain"] == "invertebrate":
        fs.append(lognormal_factor(  # noqa: F821
            "invertWelfareShrink", *WELFARE_RANGE_SHRINK_CI["invertebrate"],
            "Bayesian shrink on RP's shrimp welfare range (Sempere 2023)"))
    elif org["domain"] == "wild_invertebrate":
        fs.append(lognormal_factor(  # noqa: F821
            "wildInvertWelfareShrink", *WELFARE_RANGE_SHRINK_CI["wild_invertebrate"],
            "Bayesian shrink on RP's insect welfare range (Sempere 2023)"))
    return fs
