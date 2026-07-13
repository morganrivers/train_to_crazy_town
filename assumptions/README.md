# `assumptions/` — the single source of truth

Every worldview on the train is composed from the numbered Python **assumption
files** in this directory (the MORAL axis), operating on the worked derivations
in the **`botecs/`** package (the EMPIRICAL axis). Every derived representation
is generated from them; nothing lives twice:

```
   botecs/*.py  (empirical: one worked derivation per org, provenance-tagged)
        │  imported (read, never forked) by
        ▼
   assumptions/*.py  (0_parochial … 20_boltzmann_brain — the moral premises)
        │  composed per worldview by worldviews.py
        │  (exec the chain, in craziness order, in one namespace)
   ┌────┼──────────────┬──────────────────────────┬─────────────────────┐
   │ reads            │ generate.py writes        │ writes               │ writes
   ▼                  ▼                           ▼                      ▼
 allocate.py   diagram/train_tree.json   squiggle/worldviews/*.squiggle  squiggle/botecs/*.squiggle
 (portfolio)   → build_diagram.py         (one summary model per node)   + PROVENANCE.md
```

The two axes never multiply into each other: moral premises fork into worldviews,
empirical magnitudes are shared and improved in ONE place. See `botecs/base.py`
for the contract and the provenance taxonomy.

Edit an assumption file, run `python3 generate.py`, and the graph JSON and
every Squiggle model move together; `python3 test_worldviews.py` (run in CI,
`.github/workflows/sync.yml`) fails if any generated copy drifts. An assumption modifies, in a simple way, the chain
of assumptions before it — each file does one (or more) of exactly three
things:

1. **adds new functions** — e.g. `5_…` introduces `future_discount_ci()`,
   `16_…` introduces `simulation_continuation_beta()`;
2. **redefines functions** — e.g. `1_…` redefines `moral_weight` (capturing and
   wrapping the parochial one), `7_…` throws away the neuron-count
   `welfare_range` and replaces it with an RP welfare-range table;
3. **changes parameters to functions** — e.g. `6_…` collapses
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
w1_2_7  =  0_parochial.py  ∘  1_far_away_humans.py  ∘  2_animals_somewhat.py  ∘  7_animals_matter_a_lot.py
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

The donation slate is fixed across every worldview. Its ORG identities live once
on `0_parochial.py`; each org's direct-effect BOTEC (its empirical derivation)
lives in the `botecs/` package, tagged with per-factor provenance and a source.
Only the moral coefficients change as assumptions accumulate. Each org's *direct*
figure is in its beneficiary's own welfare units, before the moral circle /
welfare range / discount the chain applies; the numbers are calibrated so that
the **animals-matter-a-lot worldview (`w1_2_7`) reproduces Vasco Grilo's published
cost-effectiveness figures** and the GiveWell baseline reproduces his ~0.00994
DALY/$, so `allocate.py`'s "x GiveWell" column reads his own multiples:

| Target | Cause | Direct figure grounded in | ≈ x GiveWell at RP welfare ranges |
|---|---|---|---|
| **Local soup kitchen** | Community / present neighbours | worked subjective-wellbeing BOTEC | — (root) |
| **GiveDirectly** | Global poor, direct cash | GiveWell cash benchmark (~1/10 of top) | 0.1x |
| **GiveWell top charity (AMF)** | Global health, lives saved | GiveWell CEA / Grilo ~0.00994 DALY/$ | 1x (baseline) |
| **AIM / Charity Entrepreneurship** | Incubation, higher variance | GiveWell-level target, high variance | ~2x |
| **The Humane League** | Farmed vertebrates | Saulius chicken-years/$ × Grilo DALY/$ | ~460x |
| **Shrimp Welfare Project** | Invertebrates | Grilo HSI 639 DALY/$ | ~64,000x |
| **Wild insects (humane pesticides)** | Wild / soil invertebrates | Grilo 236 DALY/$ | ~24,000x |
| **Screwworm Free Future** | Wild-vertebrate suffering (myiasis) | Grilo screwworm CEA ~1.67–4.59 DALY/$ | ~290x |
| **Rainforest Trust** | Ecosystems (intrinsic value) | hectares/$ × existence-value exchange rate | nature-gated |
| **Clean Air Task Force** | Climate mitigation advocacy | tCO2e/$ (Founders Pledge) × wDALY/tCO2e (Bressler + PIK) × tipping multiplier | climate-gated |
| **ALLFED** | Global catastrophic risk / resilience | worked nuclear-winter BOTEC (Denkenberger & Pearce) | future-gated |
| **AI safety (Redwood Research)** | Existential risk, astronomical waste | worked BOTEC: Carlsmith P(catastrophe) × future (≈ Linch's bar) | future-gated |

The parochial root's soup-kitchen value is a worked BOTEC — people made happier
per dollar × their wellbeing gain, netted against the counterfactual of the
money sitting in a bank — and every worldview downstream carries that agreed
number unchanged.

ALLFED and AI safety are **worked BOTECs** in the `botecs/` package (the
empirical axis), not opaque ranges. ALLFED's value is computed from a nuclear-war
probability (~0.1%/yr full-scale × ~10% conditional nuclear winter), Denkenberger
& Pearce's lives-fed-per-dollar, and a far-future term for averting
civilization-ending collapse; AI safety's from a decomposition of P(AI
catastrophe) (Carlsmith's six premises, ~10%) × the fraction alignment can avert
× marginal risk removed per dollar — whose central value lands on Linch's
independently-elicited ~$100M-per-0.01%-x-risk bar (a cross-check, not a fit).
Both carry the *same* astronomical `futureDalysAtStake` (itself decomposed into
population-per-century × expected-surviving-centuries × DALYs-per-life, with the
background-extinction rate an explicit lever), so which one a longtermist funds
is arithmetic on their x-risk-reduced-per-dollar, **not** a chosen result. On the
central inputs AI safety edges ahead (~1.8×); the pessimistic collapse-reroll fork
(`collapse_degrades_future`) flips it to ALLFED. A positive pure-time discount
(`future_discount_ci`, mean ~8e-7 at stop 5) annihilates the mostly-aeons-away
future, so moderate longtermists still rank present global health first;
collapsing it to 1 (stop 6) lets the astronomical future dominate.

## The ladder (ordered by how crazy they are)

| # | assumption | what it does to the chain |
|---|---|---|
| 0 | `parochial` | the base: slate, the `moral_weight`/`welfare_range`/`coefficient`/`uncertain_factors`/`externality_coefficient` hooks, `squiggle()` |
| 1 | `far_away_humans` | redefines `moral_weight`: all present humans |
| 2 | `animals_somewhat` | adds `neuron_count_exponent()`; redefines `welfare_range` |
| 3 | `nature_intrinsic_value` | redefines `moral_weight` (ecosystems enter); wraps `uncertain_factors` with a wDALY-per-hectare existence-value exchange rate on the conservation org |
| 4 | `climate_tipping_points` | redefines `moral_weight` (climate enters); wraps `uncertain_factors`: wDALY-per-tCO2e (Bressler mortality + PIK income channel) × a tipping multiplier (Rockström) on CATF, and a forest co-benefit on the conservation org when the chain also holds 3 |
| 5 | `future_humans_matter_with_discounting` | adds `future_discount_ci()` (90% CI, mean ~8e-7); registers it as a factor on future-facing orgs |
| 6 | `no_discounting_future_humans` | collapses `future_discount_ci()` → exactly 1; x-risk enters the circle |
| 7 | `animals_matter_a_lot` | replaces `welfare_range` with RP welfare ranges (Fischer et al.); invertebrates and wild vertebrates enter |
| 8 | `suffering_focused` | registers the suffering/happiness asymmetry as per-org factor CIs (Tomasik, Vinding) |
| 9 | `meat_eater_problem` | redefines `externality_coefficient`: charges human orgs, per direct DALY, for the meat their beneficiaries eat (Grilo) |
| 10 | `net_negative_animal_lives` | re-parameterises the farmed-suffering CI; wraps `coefficient` to boost suffering-reduction (Tomasik, Benatar) |
| 11 | `resilience_undermines_deterrence` | wraps `uncertain_factors`: a Peltzman deterrence-erosion multiplier on ALLFED (an alternative, lower estimate) |
| 12 | `collapse_teaches_better_future` | wraps `uncertain_factors`: a <1 far-future multiplier on ALLFED (survivors rebuild wiser) |
| 13 | `collapse_degrades_future` | wraps `uncertain_factors`: a >1 far-future multiplier on ALLFED (survivors stagnate); can flip the longtermist winner to ALLFED |
| 14 | `time_of_perils_exit` | wraps `uncertain_factors`: a >1 multiplier on BOTH future orgs' shared future — the hazard window closes once we are multiplanetary (Ord; the backup argument) |
| 15 | `space_expansion_backfires` | wraps `uncertain_factors`: a <1 multiplier on BOTH future orgs' shared future — early expansion re-arms the hazard (Deudney; Weinersmiths); the sweet-spot view |
| 16 | `living_in_simulation` | adds `simulation_continuation_beta()` (beta(1, 9)); attenuates future value (Bostrom) |
| 17 | `person_affecting_view` | registers the present-people fraction (CI 3e-7 to 3e-4): merely-possible future people get ~no weight (Narveson) |
| 18 | `soil_animals` | wraps `externality_coefficient`: count ~10^19 soil animals; human orgs go net-negative (Grilo) |
| 19 | `morality_is_not_real` | override: redefines `coefficient` → 0 for everything (Mackie) |
| 20 | `boltzmann_brain` | override: everything collapses to one equal pleasant thought |

Assumptions 11–13 are the **nuclear second-order forks** — three mutually
exclusive readings of resilient-food / civilizational-collapse value, each
riding a longtermist (undiscounted) chain and each a distinct, durable
disagreement rather than a botec input. Assumptions 14–15 are the **space
second-order forks**, the same move applied to the hazard curve itself: the
perils-exit reading (multiplanetary settlement closes the window, so the
future is bigger) versus the backfire reading (the capability that settles
planets also moves asteroids and exports nationalism, so below a large number
of genuinely independent settlements expansion adds risk and the window stays
open — accelerate only once geopolitics has matured). They are mutually
exclusive with each other but combine freely with the nuclear forks. 3
(`nature_intrinsic_value`) and 4 (`climate_tipping_points`) are present-world
values, so they exclude the astronomical branch (`no_discounting`), where a
few wDALY/$ from habitat or mitigation is swamped.

Two things are deliberately **not** on this ladder, because they are not
worldview forks. (1) **The resilient-foods-vs-AI-safety comparison** is decided
by the two orgs' *worked BOTECs* in the slate, not by an assumption that sets the
answer — see "The metric and the slate" above. (2) **Two-envelope skepticism
about RP's invertebrate welfare ranges** (Nuño Sempere) is a *methodological
correction*, not a value premise: whether to apply it has a determinate answer
given welfare-range realism + EV, so it is documented as a judgment call in
`6_animals_matter_a_lot.py` (we keep RP's published medians as the baseline and
flag the contention) rather than branched.

## Limiting the combinatorial explosion

Twenty-one assumptions would naively give 2²⁰ = 1,048,576 chains (the parochial
base is always present). Metadata on each file limits combinations to what one
person could plausibly hold at once:

- **`REQUIRES`** — an animals person won't think only people in their community
  matter, so `2` requires `1`; `3` (nature), `4` (climate) and `5` (discounted
  future) all require the impartial `1`; `6` (no discount) modifies the
  discount `5` introduced; `7` upgrades `2`; `9` (meat-eater) needs animals in
  the circle (`2`); `10` (net-negative lives) and `18` (soil animals)
  presuppose the RP welfare ranges (`7`); `16` (simulation) and `17`
  (person-affecting), the three nuclear forks `11`/`12`/`13`, and the two space
  forks `14`/`15`, only make sense to someone already reasoning about the
  undiscounted far future (`6`).
- **`EXCLUDES`** — the two overrides (`19`, `20`) can't be held together; the
  near-term animal-vs-human stops `9`/`10` are not combined with
  astronomical-stakes longtermism (`6`), where x-risk swamps the bookkeeping;
  `3` (nature) and `4` (climate), present-world values, are likewise excluded
  from `6`; the three nuclear second-order forks `11`/`12`/`13` are mutually
  exclusive — one nuclear nuance per worldview — and so are the two space
  forks `14`/`15` (one reading of the hazard curve per worldview).
- **`TERMINAL`** — an override invalidates every assumption before it, so it is
  generated only on its minimal `REQUIRES`-closure chain; any larger chain
  would produce a byte-identical all-flat model.

That leaves **411 worldviews**. Every worldview's parent is the same chain minus
its craziest assumption, so the graph is a tree and every edge adds exactly one
assumption (and the generator grows the tree incrementally — extending each
valid chain by one crazier assumption — rather than filtering the powerset, so
the enumeration stays linear in the number of worldviews as the ladder grows).

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
