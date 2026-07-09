# `assumptions/` — the single source of truth

Every worldview on the train is composed from the numbered Python **assumption
files** in this directory, and every derived representation is generated from
them; nothing lives twice:

```
                 assumptions/*.py  (0_parochial … 15_boltzmann_brain)
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

1. **adds new functions** — e.g. `3_…` introduces `future_discount()`,
   `6_…` introduces `suffering_multiplier(org)`;
2. **redefines functions** — e.g. `1_…` redefines `moral_weight` (capturing and
   wrapping the parochial one), `5_…` throws away the neuron-count
   `welfare_range` and replaces it with an RP welfare-range table;
3. **changes parameters to functions** — e.g. `4_…` redefines
   `future_discount()` from `0.01` to `1.0` and touches nothing else.

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
  (drives `top_pick` in the diagram and `allocate.py`);
- `squiggle()` — renders **one standalone Squiggle model** whose `worldviewEv`
  is the expected value of that worldview. `generate.py` writes it to
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
| **ALLFED** | Global catastrophic risk / resilience | Denkenberger & Pearce (near-term GCR) | future-gated |
| **AI safety (Redwood Research)** | Existential risk, astronomical waste | Linch's $100M/0.01% × Bostrom/Cotra | future-gated |

The parochial root's soup-kitchen value is a worked BOTEC — people made happier
per dollar × their wellbeing gain, netted against the counterfactual of the
money sitting in a bank — and every worldview downstream carries that agreed
number unchanged.

## The ladder (ordered by how crazy they are)

| # | assumption | what it does to the chain |
|---|---|---|
| 0 | `parochial` | the base: slate, the `moral_weight`/`welfare_range`/`coefficient`/`externality` hooks, `squiggle()` |
| 1 | `far_away_humans` | redefines `moral_weight`: all present humans |
| 2 | `animals_somewhat` | adds `neuron_count_exponent()`; redefines `welfare_range` |
| 3 | `future_humans_matter_with_discounting` | adds `future_discount()` (= 0.01); wraps `coefficient` |
| 4 | `no_discounting_future_humans` | re-parameterises `future_discount()` → 1.0; x-risk enters the circle |
| 5 | `animals_matter_a_lot` | replaces `welfare_range` with RP welfare ranges (Fischer et al.); invertebrates enter |
| 6 | `suffering_focused` | adds `suffering_multiplier(org)`; wraps `coefficient` (Tomasik, Vinding) |
| 7 | `meat_eater_problem` | redefines the `externality` hook: charges human orgs for the meat their beneficiaries eat (Grilo) |
| 8 | `net_negative_animal_lives` | re-parameterises the farmed-suffering penalty; wraps `coefficient` to boost suffering-reduction (Tomasik, Benatar) |
| 9 | `living_in_simulation` | adds `simulation_continuation_prob()`; attenuates future value (Bostrom) |
| 10 | `two_envelope_welfare_skepticism` | wraps `welfare_range`: Bayesian-shrinks invertebrate ranges (Nuño Sempere) |
| 11 | `person_affecting_view` | wraps `coefficient`: merely-possible future people get ~no weight (Narveson) |
| 12 | `resilient_foods_beat_agi` | redefines `expected_values`/`value_expression`: ALLFED = a multiple of AI safety (Denkenberger & Pearce) |
| 13 | `soil_animals` | wraps `coefficient`/`externality`: count ~10^19 soil animals; human orgs go net-negative (Grilo) |
| 14 | `morality_is_not_real` | override: redefines `coefficient` → 0 for everything (Mackie) |
| 15 | `boltzmann_brain` | override: everything collapses to one equal pleasant thought |

## Limiting the combinatorial explosion

Sixteen assumptions would naively give 2¹⁵ = 32,768 chains (the parochial base
is always present). Metadata on each file limits combinations to what one person
could plausibly hold at once:

- **`REQUIRES`** — an animals person won't think only people in their community
  matter, so `2` requires `1`; `4` modifies the discount `3` introduced, so it
  requires `3`; `5` upgrades `2`; `7` (meat-eater) needs animals in the circle
  (`2`); `8` (net-negative lives) and `10` (two-envelope skepticism) and `13`
  (soil animals) all presuppose the RP welfare ranges (`5`); `9` (simulation),
  `11` (person-affecting) and `12` (resilient foods vs AGI) only make sense to
  someone already reasoning about the undiscounted far future (`4`).
- **`EXCLUDES`** — the two overrides (`14`, `15`) can't be held together; the
  near-term animal-vs-human stops `7`/`8` are not combined with
  astronomical-stakes longtermism (`4`); and two-envelope skepticism (`10`)
  excludes the assumptions that bet the *other* way on invertebrates —
  net-negative lives (`8`) and counting soil animals (`13`).
- **`TERMINAL`** — an override invalidates every assumption before it, so it is
  generated only on its minimal `REQUIRES`-closure chain; any larger chain
  would produce a byte-identical all-flat model.

That leaves **125 worldviews**. Every worldview's parent is the same chain minus
its craziest assumption, so the graph is a tree and every edge adds exactly one
assumption.

## Adding an assumption

1. Create `N_snake_case_name.py` with the metadata block (`NAME`, `LABEL`,
   `EDGE_LABEL`, `DESC`, `FIGURES`, `REQUIRES`, `EXCLUDES`, `TERMINAL`) —
   numbering must stay linear (0..N, no doubling, no gaps; renumber if you
   insert in the middle).
2. Have it add / redefine / re-parameterise functions from the chain. Capture a
   previous definition first (`_prev = coefficient`) if you want to wrap it.
3. `python3 generate.py` — regenerates `diagram/train_tree.json` and every
   `squiggle/worldviews/*.squiggle`.
4. `python3 test_worldviews.py` — asserts numbering, tree shape, and that
   nothing generated has drifted. CI runs the same check.
