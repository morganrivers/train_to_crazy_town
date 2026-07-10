"""botecs/future.py — the astronomical future at stake, SHARED and DECOMPOSED.

The single biggest EV lever in the whole model, and the one most often smuggled
in as a bare stipulation. Rather than one opaque `futureDalysAtStake` CI
spanning five orders of magnitude (Bostrom's "Astronomical Waste"), it is a
worked product with an EXPLICIT background-extinction lever (Newberry, "How many
lives does the future hold?"):

    futureDalysAtStake = humansPerCentury          (how many people per century)
                       * expectedFutureCenturies   (~ 1 / background-extinction
                                                      hazard — the lever)
                       * dalyPerFutureLife          (welfare per life)

The three factors are defined ONCE here and shared by BOTH future-facing botecs
(ALLFED and AI safety), so a longtermist comparison of the two is arithmetic on
their x-risk-reduced-per-dollar against the SAME future — not two independently
chosen astronomical numbers. The confidence Monte-Carlo draws each shared factor
once per world-state (`shared=True`) and applies the same draw to both orgs;
previously each org drew its own future, spuriously decorrelating them.

Making `expectedFutureCenturies` explicit is the point: it is ~1/hazard, so the
whole astronomical case rides on the background per-century extinction rate — a
number people's intuitions handle badly (Thorstad's time-of-perils skepticism
lives at the low end, long biological + space-settlement futures at the high
end). Editing that one factor sweeps the future by orders of magnitude, exactly
as it should.
"""
from botecs.base import Factor

# People alive per century. Newberry anchors ~1.1e10/century; the CI spans
# plausible long-run population levels.
HUMANS_PER_CENTURY = Factor(
    "humansPerCentury", "lognormal", (7e9, 2e10),
    provenance="empirical-anchor",
    comment="people alive per century (Newberry ~1.1e10; Our World in Data)",
    source="https://www.globalprioritiesinstitute.org/wp-content/uploads/Toby-Newberry_How-many-lives-does-the-future-hold.pdf",
    shared=True)

# THE LEVER. Expected surviving centuries ~ 1 / background per-century extinction
# hazard (a geometric horizon). ~5 centuries if the hazard stays ~20%/century
# (Thorstad's time-of-perils pessimism, no "time of perils" exit); ~5e4 if it
# falls to ~2e-5/century once a long biological future and early space settlement
# lock in. The astronomical case for x-risk work lives or dies on this factor.
EXPECTED_FUTURE_CENTURIES = Factor(
    "expectedFutureCenturies", "lognormal", (5, 5e4),
    provenance="worked-internal",
    comment="expected surviving centuries ~ 1/(background extinction hazard): "
            "~5 (Thorstad time-of-perils, ~20%/century) to ~5e4 (long biological "
            "+ space future, ~2e-5/century) — the background-risk lever",
    source="https://globalprioritiesinstitute.org/existential-risk-pessimism-and-the-time-of-perils-david-thorstad/",
    shared=True)

# DALYs of welfare per future life lived.
DALY_PER_FUTURE_LIFE = Factor(
    "dalyPerFutureLife", "lognormal", (30, 100),
    provenance="empirical-anchor",
    comment="DALYs of welfare per future life (life-years lived)",
    shared=True)

# The shared far-future term, appended to each future-facing botec's risk term.
FUTURE_TERM = ("humansPerCentury", "expectedFutureCenturies", "dalyPerFutureLife")
FUTURE_FACTORS = {f.name: f for f in
                  (HUMANS_PER_CENTURY, EXPECTED_FUTURE_CENTURIES, DALY_PER_FUTURE_LIFE)}
