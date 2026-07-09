"""Assumption 10 — two-envelope skepticism about invertebrate welfare ranges.

A counter-move you meet once you are deep in animal prioritisation: Rethink
Priorities' mainline welfare ranges are expectations taken over deep uncertainty
about whether tiny-brained animals are sentient at all, and cross-species
comparisons of "one unit of welfare" run into the two-envelope problem — which
way you normalise (in human units or animal units) swings the answer by orders
of magnitude. Nuño Sempere's Bayesian adjustment argues the mainline point
estimates are inflated for the smallest, least-understood animals and should be
shrunk by one to two orders of magnitude, most of all for invertebrates.

This assumption REDEFINES `welfare_range`, wrapping the RP table from
assumption 5 with a per-domain Bayesian shrink. Chickens (vertebrate,
comparatively well-evidenced) are barely touched; shrimp and insects are pulled
down ~2 orders of magnitude, which flips the animal winner from the Shrimp
Welfare Project / wild insects back to corporate chicken campaigns.

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
# point estimate: vertebrate farmed animals are comparatively well-evidenced so
# they keep their range; the smallest, most sentience-uncertain animals take the
# largest (~2 order-of-magnitude) haircut.
WELFARE_RANGE_SHRINK = {
    "farmed_animal": 1.0,        # chickens: well-evidenced, negligible adjustment
    "invertebrate": 0.005,       # shrimp: ~2 orders of magnitude down
    "wild_invertebrate": 0.002,  # insects: even less certain, larger haircut
}

_rp_welfare_range = welfare_range  # noqa: F821  (assumption 5's RP table)


def welfare_range(org):
    """REDEFINED: RP welfare range times a per-domain Bayesian shrink."""
    wr = _rp_welfare_range(org)
    if not org["animal"]:
        return wr
    return wr * WELFARE_RANGE_SHRINK.get(org["domain"], 1.0)
