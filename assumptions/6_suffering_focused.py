"""Assumption 6 — suffering-focused ethics.

Reducing intense suffering matters more than creating happiness. This
assumption WRAPS `uncertain_factors` with the suffering/happiness asymmetry:
orgs whose work averts intense suffering are weighted up, orgs whose case
rests on creating future flourishing are weighted down — each as a
distribution over the asymmetry's magnitude, not a point.
"""

NAME = "suffering_focused"
LABEL = "Suffering-focused\nethics"
EDGE_LABEL = "weight suffering over happiness"
FIGURES = ["Brian Tomasik", "David Pearce"]
REQUIRES = ["animals_somewhat"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "Asymmetry: averting intense suffering takes priority over creating "
    "happiness. Factory farming, malaria and the worst wild-animal conditions "
    "weigh up; speculative future-flourishing bets weigh down. Arises most "
    "naturally from taking animal suffering seriously, so it requires "
    "animals_somewhat."
)

# The asymmetry magnitude (suffering-reduction weighted ~10x above
# happiness-creation in expectation) follows the suffering-focused tradition —
# Tomasik's and Vinding's case that intense suffering is not offsettable by
# comparable pleasure (https://reducing-suffering.org ; Vinding,
# "Suffering-Focused Ethics: Defense and Implications", 2020,
# https://centerforreducingsuffering.org/research/suffering-focused-ethics-defense-and-implications/ ).
# The tradition spans everything from a mild priority to near-lexicality,
# which is why both sides of the split are 90% CIs rather than points: the
# means (~3.1 up, ~0.32 down) preserve the strong-but-not-lexical reading the
# old 3.0 / 0.3 points stood for.
SUFFERING_PRIORITY_CI = (1.1, 6.5)      # weight on averting intense suffering
FLOURISHING_DISCOUNT_CI = (0.08, 0.8)   # weight on creating happiness/flourishing

_symmetric_uncertain_factors = uncertain_factors  # noqa: F821


def uncertain_factors(org):
    """WRAPPED: every org carries one side of the suffering/happiness
    asymmetry — the full distribution in the model, its exact mean in the
    ranking."""
    fs = _symmetric_uncertain_factors(org)
    if org["averts_intense_suffering"]:
        fs.append(lognormal_factor(  # noqa: F821
            "sufferingPriority", *SUFFERING_PRIORITY_CI,
            "extra weight on averting intense suffering (Tomasik; Vinding 2020)"))
    else:
        fs.append(lognormal_factor(  # noqa: F821
            "flourishingDiscount", *FLOURISHING_DISCOUNT_CI,
            "reduced weight on creating happiness (Tomasik; Vinding 2020)"))
    return fs
