# `assumptions/` — the single source of truth

Every worldview on the train is composed from the numbered Python **assumption
files** in this directory, and every derived representation is generated from
them; nothing lives twice:

```
                 assumptions/*.py  (0_parochial … 13_boltzmann_brain)
                          │  composed per worldview by worldviews.py
                          │  (exec the chain, in craziness order, in one namespace)
        ┌─────────────────┼───────────────────────────┐
        │ reads           │ generate.py writes         │ generate.py writes
        ▼                 ▼                            ▼
   allocate.py    diagram/train_tree.json      squiggle/worldviews/*.squiggle
   (portfolio)    → build_diagram.py → .drawio  (one standalone model per node)
```

Edit an assumption file, run `python3 generate.py`, and the graph JSON and
every Squiggle model move together; `python3 test_worldviews.py` (run in CI,
`.github/workflows/sync.yml`) fails if any generated copy drifts. An assumption modifies, in a simple way, the chain
of assumptions before it — each file does one (or more) of exactly three
things:

1. **adds new functions** — e.g. `3_…` introduces `future_discount_ci()`,
   `9_…` introduces `simulation_continuation_beta()`;
2. **redefines functions** — e.g. `1_…` redefines `moral_weight` (capturing and
   wrapping the parochial one), `5_…` throws away the neuron-count
   `welfare_range` and replaces it with an RP welfare-range table;
3. **changes parameters to functions** — e.g. `4_…` collapses
   `future_discount_ci()` from a 90% CI to exactly `1` and touches nothing else.

A parameter that is genuinely uncertain is stated as a **distribution**, not a
point: assumptions register it through the base `uncertain_factors` hook (a
`lognormal_factor` 90% CI, or a `beta_factor` for probabilities, which belong
in [0, 1]). The generated model then carries the named distribution in its
prelude, while the Python ranking uses its exact mean — factors are independent,
so the expectation of the product is the product of the expectations, and the
two representations agree to float precision. Structural weights (who is in the
circle, relative weightings like the RP welfare-range table) stay points by
design.

## How composition works

A **worldview** (a node in the tree) is a chain of assumptions.
[`worldviews.py`](worldviews.py) `exec`s the chain's files **in numeric order**
into one shared namespace — effectively a string of Python imports where each
later file sees, and may capture/wrap/replace, everything defined so far:

```
w1_2_5  =  0_parochial.py  ∘  1_far_away_humans.py  ∘  2_animals_somewhat.py  ∘  5_animals_matter_a_lot.py
```

The composed namespace ends with two products:

- `expected_values()` — `{org: E[wDALY averted/$]}`, the Python-side ranking
  (drives `top_pick` in the diagram and `allocate.py`); each org's value is
  `E[direct effect] × (coefficient + externality_coefficient)`, so downstream
  side effects (the meat-eater and soil-animal charges) scale with the same
  uncertain direct effect that causes them;
- `squiggle()` — renders **one standalone Squiggle model** whose `worldviewEv`
  is the expected value of that worldview. Each scored org carries both `dist`
  (its full wDALY/$ distribution) and `wdalyPerUsd` (the exact analytic mean of
  that distribution, which the ranking sorts by — matching `expected_values()`
  to float precision). `generate.py` writes it to
  `squiggle/worldviews/<id>.squiggle`, and the diagram links each node to that
  model in a temporary playground.

The numbered files are deliberately *not* importable modules (their names start
with the craziness digit); only `worldviews.py` runs them, always in order,
always on top of `0_parochial.py`.

## The metric and the slate

The unit every worldview optimizes is **expected welfare-adjusted DALYs averted
per dollar** (`wDALY/$`): the native unit of global-health cost-effectiveness
(WHO/GBD, GiveWell-adjacent), generalized by scaling a DALY by a species'
sentience-adjusted welfare range (Rethink Priorities / Bob Fischer) so one unit
covers human health, animals, and future minds. One human DALY = 1 wDALY.

The donation slate is fixed across every worldview and lives once, on
`0_parochial.py`, each org with its direct-effect BOTEC (a lognormal 90% CI) and
a source URL. Only the coefficients change as assumptions accumulate. Each
org's *direct* figure is in its beneficiary's own welfare units, before the
moral circle / welfare range / discount the chain applies; the numbers are
calibrated so that the **animals-matter-a-lot worldview (`w1_2_5`) reproduces
Vasco Grilo's published cost-effectiveness figures** and the GiveWell baseline
reproduces his ~0.00994 DALY/$, so `allocate.py`'s "x GiveWell" column reads his
own multiples:

| Target | Cause | Direct figure grounded in | ≈ x GiveWell at RP welfare ranges |
|---|---|---|---|
| **Local soup kitchen** | Community / present neighbours | worked subjective-wellbeing BOTEC | — (root) |
| **GiveDirectly** | Global poor, direct cash | GiveWell cash benchmark (~1/10 of top) | 0.1x |
| **GiveWell top charity (AMF)** | Global health, lives saved | GiveWell CEA / Grilo ~0.00994 DALY/$ | 1x (baseline) |
| **AIM / Charity Entrepreneurship** | Incubation, higher variance | GiveWell-level target, high variance | ~2x |
| **The Humane League** | Farmed vertebrates | Saulius chicken-years/$ × Grilo DALY/$ | ~460x |
| **Shrimp Welfare Project** | Invertebrates | Grilo HSI 639 DALY/$ | ~64,000x |
| **Wild insects (humane pesticides)** | Wild / soil invertebrates | Grilo 236 DALY/$ | ~24,000x |
| **ALLFED** | Global catastrophic risk / resilience | worked nuclear-winter BOTEC (Denkenberger & Pearce) | future-gated |
| **AI safety (Redwood Research)** | Existential risk, astronomical waste | worked BOTEC: Linch's $100M/0.01% × Bostrom/Cotra future | future-gated |

The parochial root's soup-kitchen value is a worked BOTEC — people made happier
per dollar × their wellbeing gain, netted against the counterfactual of the
money sitting in a bank — and every worldview downstream carries that agreed
number unchanged.

ALLFED and AI safety are **worked BOTECs too**, not opaque ranges. ALLFED's value
is computed from a nuclear-war probability (~0.1%/yr full-scale × ~10% conditional
nuclear winter), Denkenberger & Pearce's lives-fed-per-dollar, and a far-future
term for averting civilization-ending collapse; AI safety's from Linch's
~$100M-per-0.01%-x-risk bar. Both carry the *same* astronomical `futureDalysAtStake`,
so which one a longtermist funds is arithmetic on their x-risk-reduced-per-dollar,
**not** a chosen result. On the central inputs AI safety edges ahead (~1.7×);
more pessimistic recovery-from-collapse inputs flip it to ALLFED. A positive
pure-time discount (`future_discount_ci`, mean ~8e-7 at stop 3) annihilates the
mostly-aeons-away future, so moderate longtermists still rank present global
health first; collapsing it to 1 (stop 4) lets the astronomical future dominate.

## The ladder (ordered by how crazy they are)

| # | assumption | what it does to the chain |
|---|---|---|
| 0 | `parochial` | the base: slate, the `moral_weight`/`welfare_range`/`coefficient`/`uncertain_factors`/`externality_coefficient` hooks, `squiggle()` |
| 1 | `far_away_humans` | redefines `moral_weight`: all present humans |
| 2 | `animals_somewhat` | adds `neuron_count_exponent()`; redefines `welfare_range` |
| 3 | `future_humans_matter_with_discounting` | adds `future_discount_ci()` (90% CI, mean ~8e-7); registers it as a factor on future-facing orgs |
| 4 | `no_discounting_future_humans` | collapses `future_discount_ci()` → exactly 1; x-risk enters the circle |
| 5 | `animals_matter_a_lot` | replaces `welfare_range` with RP welfare ranges (Fischer et al.); invertebrates enter |
| 6 | `suffering_focused` | registers the suffering/happiness asymmetry as per-org factor CIs (Tomasik, Vinding) |
| 7 | `meat_eater_problem` | redefines `externality_coefficient`: charges human orgs, per direct DALY, for the meat their beneficiaries eat (Grilo) |
| 8 | `net_negative_animal_lives` | re-parameterises the farmed-suffering CI; wraps `coefficient` to boost suffering-reduction (Tomasik, Benatar) |
| 9 | `living_in_simulation` | adds `simulation_continuation_beta()` (beta(1, 9)); attenuates future value (Bostrom) |
| 10 | `person_affecting_view` | registers the present-people fraction (CI 3e-7 to 3e-4): merely-possible future people get ~no weight (Narveson) |
| 11 | `soil_animals` | wraps `externality_coefficient`: count ~10^19 soil animals; human orgs go net-negative (Grilo) |
| 12 | `morality_is_not_real` | override: redefines `coefficient` → 0 for everything (Mackie) |
| 13 | `boltzmann_brain` | override: everything collapses to one equal pleasant thought |

Two things are deliberately **not** on this ladder, because they are not
worldview forks. (1) **The resilient-foods-vs-AI-safety comparison** is decided
by the two orgs' *worked BOTECs* in the slate, not by an assumption that sets the
answer — see "The metric and the slate" above. (2) **Two-envelope skepticism
about RP's invertebrate welfare ranges** (Nuño Sempere) is a *methodological
correction*, not a value premise: whether to apply it has a determinate answer
given welfare-range realism + EV, so it is documented as a judgment call in
`5_animals_matter_a_lot.py` (we keep RP's published medians as the baseline and
flag the contention) rather than branched.

## Limiting the combinatorial explosion

Fourteen assumptions would naively give 2¹³ = 8,192 chains (the parochial base
is always present). Metadata on each file limits combinations to what one person
could plausibly hold at once:

- **`REQUIRES`** — an animals person won't think only people in their community
  matter, so `2` requires `1`; `4` modifies the discount `3` introduced, so it
  requires `3`; `5` upgrades `2`; `7` (meat-eater) needs animals in the circle
  (`2`); `8` (net-negative lives) and `11` (soil animals) presuppose the RP
  welfare ranges (`5`); `9` (simulation) and `10` (person-affecting) only make
  sense to someone already reasoning about the undiscounted far future (`4`).
- **`EXCLUDES`** — the two overrides (`12`, `13`) can't be held together; and
  the near-term animal-vs-human stops `7`/`8` are not combined with
  astronomical-stakes longtermism (`4`), where x-risk swamps the bookkeeping.
- **`TERMINAL`** — an override invalidates every assumption before it, so it is
  generated only on its minimal `REQUIRES`-closure chain; any larger chain
  would produce a byte-identical all-flat model.

That leaves **73 worldviews**. Every worldview's parent is the same chain minus
its craziest assumption, so the graph is a tree and every edge adds exactly one
assumption.

## Adding an assumption

1. Create `N_snake_case_name.py` with the metadata block (`NAME`, `LABEL`,
   `EDGE_LABEL`, `DESC`, `FIGURES`, `REQUIRES`, `EXCLUDES`, `TERMINAL`) —
   numbering must stay linear (0..N, no doubling, no gaps; renumber if you
   insert in the middle).
2. Have it add / redefine / re-parameterise functions from the chain. Capture a
   previous definition first (`_prev = coefficient`) if you want to wrap it.
   State any genuinely uncertain magnitude as a distribution: wrap
   `uncertain_factors` and register a `lognormal_factor` (90% CI) or
   `beta_factor` (probability), citing the source in its comment — the factor
   shows up by name in every generated model that holds the assumption.
3. `python3 generate.py` — regenerates `diagram/train_tree.json` and every
   `squiggle/worldviews/*.squiggle`.
4. `python3 test_worldviews.py` — asserts numbering, tree shape, and that
   nothing generated has drifted. CI runs the same check.
