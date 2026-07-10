"""Assumption 16 — we are probably living in a simulation.

Bostrom's simulation argument, taken seriously. This assumption ADDS a new
parameter `simulation_continuation_beta` and WRAPS `uncertain_factors`: the
astronomical future only pays off if the simulation keeps running long enough
for it to happen, so every future-facing org is multiplied by that probability
— a beta distribution (a probability belongs in [0, 1], where a lognormal
would leak past 1), with its exact mean in the Python ranking. Only someone
already reasoning expected-value-style about the undiscounted far future ends
up here, so it requires no_discounting_future_humans.
"""

NAME = "living_in_simulation"
LABEL = "Living in\na simulation"
EDGE_LABEL = "take the simulation argument seriously"
FIGURES = ["Nick Bostrom"]
REQUIRES = ["no_discounting_future_humans"]
EXCLUDES = []
TERMINAL = False
DESC = (
    "If most observers like us are simulated, the astronomical future that "
    "justified x-risk work probably gets switched off long before it happens. "
    "The same expected-value reasoning that bought astronomical stakes now "
    "attenuates them: future-facing value is multiplied by the probability the "
    "simulation keeps running, and the ranking slides back toward the present."
)

_basement_reality_uncertain_factors = uncertain_factors  # noqa: F821

# P(the simulation runs long enough for the astronomical future to happen),
# as beta(1, 9): mean exactly 0.1, mode at 0, long right tail — most credence
# on early shutdown, real weight up to ~0.3. Bostrom's simulation argument
# ("Are You Living in a Computer Simulation?", Philosophical Quarterly 2003,
# https://www.simulation-argument.com/simulation.pdf) motivates the shutdown
# risk; his "Astronomical Waste" reply notes simulated futures are cheap to
# terminate. No published point estimate exists, which is precisely why this
# is a distribution and not a number.
SIMULATION_CONTINUATION_BETA = (1, 9)


def simulation_continuation_beta():
    """NEW parameter: beta(a, b) over P(the simulation keeps running long
    enough for the far future); mean = a/(a+b) = 0.1."""
    return SIMULATION_CONTINUATION_BETA


def uncertain_factors(org):
    """WRAPPED: future-facing value only counts if the simulation continues —
    the full beta distribution in the model, its exact mean in the ranking."""
    fs = _basement_reality_uncertain_factors(org)
    if org["domain"] in ("future_human", "xrisk_future"):
        fs.append(beta_factor(  # noqa: F821
            "simulationContinues", *simulation_continuation_beta(),
            "P(simulation runs long enough for the far future) — Bostrom 2003"))
    return fs
