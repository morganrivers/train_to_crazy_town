# Train to Crazy Town

An interactive, zoomable tree of "get-off points" showing how far different
moral assumptions carry you down the effective-altruism reasoning train, and how
the ranking destabilizes the further you go.

## The metaphor

The "train to crazy town" is Ajeya Cotra's image (80,000 Hours podcast #90,
*worldview diversification*). EA-style reasoning is a train:

> "a train going to crazy town, and the near-termist side is like, I'm going to
> get off the train before we get to the point where all we're focusing on is
> existential risk because of the astronomical waste argument."
> — Ajeya Cotra

Each stop is a point where accepting one more individually-plausible premise
carries you to a more counterintuitive conclusion, and you are free to get off
at any stop. Near-termists get off early (measurable global health);
longtermists ride further. A later stop can retroactively reframe an earlier
one.

## What this is

- **The decision rule never changes.** Every worldview maximizes expected
  value.
- **What changes is the chain of assumptions behind it.** Each **assumption**
  is a numbered Python file in [`assumptions/`](assumptions/) — the number is
  how crazy it is (`1_far_away_humans` … `9_boltzmann_brain`). An assumption
  modifies, in a simple way, the chain before it: it **adds new functions**,
  **redefines functions**, or **changes parameters to functions** (a discount
  rate, a welfare-range table, a suffering multiplier).
- **A worldview** (a node in the tree) = a chain of assumptions, composed by
  running the assumption files in order in one shared Python namespace.
  Getting off at a node = endorsing exactly those assumptions and donating to
  whatever they rank first.
- **An edge** = accepting one more assumption (the child's craziest one).

The same optimizer returns different winners as the assumptions accumulate.

## The metric: expected welfare-adjusted DALYs per dollar

The unit is DALYs averted per dollar, the native unit of global-health
cost-effectiveness (WHO/GBD, GiveWell-adjacent). It generalizes to a
welfare-adjusted DALY (`wDALY`): a DALY scaled by a species' sentience-adjusted
welfare range (Rethink Priorities / Bob Fischer). One human DALY = 1 wDALY. One
unit covers human health, animals, and future minds. Each worldview's Python
chain renders a Squiggle model reporting `E[wDALY averted per $]` per target,
ranking them, and exporting `worldviewEv` — **the expected value of that
worldview** (what its best buy achieves per dollar).

## The donation slate (fixed across all worldviews)

The same candidates appear at every stop; only their coefficients change as
assumptions accumulate. Ordered by how much moral expansion they reward:

| Target | Cause | Rides to about... |
|---|---|---|
| **Local soup kitchen** | Community / present-generation neighbours | the root (parochial) |
| **GiveDirectly** | Global poor, direct cash | assumption 1 (all present humans) |
| **GiveWell top charity (AMF)** | Global health, lives saved | same, DALY-maximizing |
| **AIM / Charity Entrepreneurship** | Incubation, higher variance | same |
| **The Humane League** | Farmed vertebrates | assumption 2 (animals, neuron-weighted) |
| **Shrimp Welfare Project** | Invertebrates | assumption 5 (RP welfare ranges) |
| **Wild insects (humane pesticides)** | Wild / soil invertebrates | assumption 5 (nematode weight) |
| **ALLFED** | Global catastrophic risk / resilience | assumption 3–4 (future people) |
| **AI safety (Redwood Research)** | Existential risk, astronomical waste | assumption 4 (no discounting) |

## The assumptions (ordered by how crazy they are)

The root, `0_parochial`, has no real reusable functions — `moral_weight` says
"people near me", and that is the whole theory. It also owns the slate and the
worked soup-kitchen BOTEC (people made happier per dollar × their wellbeing
gain, netted against the money sitting in a bank), whose agreed value **every
worldview downstream carries unchanged**. Then, in craziness order:

1. **`far_away_humans`** — redefines `moral_weight`: distance is not morally
   relevant (Singer's famine argument; Berger gets off here).
2. **`animals_somewhat`** — adds a neuron-count exponent; redefines
   `welfare_range`: farmed animals count in proportion to brain size.
3. **`future_humans_matter_with_discounting`** — adds `future_discount()`
   (= 0.01) and wraps `coefficient`: future people count, heavily discounted.
4. **`no_discounting_future_humans`** — changes one parameter:
   `future_discount()` → 1.0. Astronomical stakes follow; x-risk work enters
   the circle (Ord, Bostrom).
5. **`animals_matter_a_lot`** — throws away the neuron proxy and redefines
   `welfare_range` with Rethink Priorities welfare ranges; invertebrates and
   the ~10^19 soil animals (significant nematode weight) enter the circle.
6. **`suffering_focused`** — adds `suffering_multiplier(org)`: averting intense
   suffering outweighs creating happiness (Tomasik, Pearce).
7. **`living_in_simulation`** — adds `simulation_continuation_prob()`: the
   astronomical future only pays off if the simulation keeps running (Bostrom).
8. **`morality_is_not_real`** — override: no moral facts, so every value is set
   to 0 and the ranking goes flat (Mackie). Keep your money.
9. **`boltzmann_brain`** — override: nothing matters except the brief moments
   of how you happen to feel; every charity collapses to one equal pleasant
   thought (the ranking goes flat).

## Limiting the combinatorial explosion

Chains are only generated if one person could plausibly hold them: each
assumption declares `REQUIRES` (an animals person won't think only people in
their community matter, so 2 requires 1; 4 re-parameterises the discount 3
introduced; 7 needs 4's expected-value-over-the-far-future style), `EXCLUDES`
(the two overrides are mutually exclusive), and `TERMINAL` (an override
invalidates everything before it, so it only rides its minimal chain). That
cuts 2⁹ = 512 possible chains down to **23 worldviews**. Every worldview's
parent is the same chain minus its craziest assumption, so the graph is a tree
and each edge adds exactly one assumption. See
[`assumptions/README.md`](assumptions/README.md).

## Single source of truth (`assumptions/`)

Everything is composed from the assumption files; nothing lives twice:

```
                 assumptions/*.py  (0_parochial … 9_boltzmann_brain)
                          │  composed per worldview by assumptions/worldviews.py
                          │  (exec the chain, in craziness order, in one namespace)
        ┌─────────────────┼───────────────────────────┐
        │ reads           │ generate.py writes         │ generate.py writes
        ▼                 ▼                            ▼
   allocate.py    diagram/train_tree.json      squiggle/worldviews/*.squiggle
   (portfolio)    → build_diagram.py → .drawio  (one standalone model per node)
```

Edit an assumption file, run `python3 generate.py`, and the graph JSON and
every Squiggle model move together; `python3 test_worldviews.py` (run in CI,
`.github/workflows/sync.yml`) fails if any generated copy drifts.

## Diagram pipeline (`diagram/`)

Graph-generation code mirroring the Graphviz→draw.io setup in
`morganrivers/iati_webapp` (`docs/diagram/`):

- **`train_tree.json`** — the worldview graph, **generated from
  `assumptions/`** (do not hand-edit). Nodes are worldviews with a `top_pick`,
  a `squiggle` model path, their accepted assumption numbers, and the public
  `figures` who most prominently articulate the latest assumption. Edges add
  one assumption each.
- **`graph_common.py`** — shared primitives (Graphviz `dot` run + plain-format
  parse, coordinate transform, node/edge/band/mxfile emission).
- **`build_diagram.py`** — reads the JSON, lays the tree top→bottom on a
  craziness gradient (a node's band = its craziest accepted assumption, STOP
  0–9), writes an editable `.drawio`, and prints a read-only draw.io view
  link. Requires Graphviz `dot` on PATH.
- **`render_diagram.py`** — renders `train_tree.json` → PNG/SVG directly with
  Graphviz. These two images ARE committed and linked below via their raw
  GitHub URLs.

The GitHub Action (`.github/workflows/diagram.yml`) looks at the
`assumptions/` layout, runs the Python chain for each worldview
(`generate.py --check`), rebuilds the diagram, and publishes it.

![Train to crazy town — worldview tree](diagram/train_tree.png)

The committed `train_tree.drawio` is served read-only by draw.io from its raw
GitHub URL (`build_diagram.py` prints the link). The rendered images are:

- PNG: https://raw.githubusercontent.com/morganrivers/train_to_crazy_town/main/diagram/train_tree.png
- SVG: https://raw.githubusercontent.com/morganrivers/train_to_crazy_town/main/diagram/train_tree.svg

These raw URLs work with no repo settings. The same images are also published to
GitHub Pages once it is enabled (Settings → Pages → Source = "GitHub Actions"):
`https://morganrivers.github.io/train_to_crazy_town/`.

## Models (`squiggle/`)

Each worldview's composed chain renders **one standalone Squiggle model** in
`squiggle/worldviews/` — no imports, no shared base file, because the
composition already happened in Python. Clicking a node in the diagram opens
its model in a **temporary Squiggle playground**, live and editable, with no
account (the whole model rides in the link's `#code=` hash;
`diagram/squiggle_playground.py` does the encoding). Run them locally with
`cd squiggle && npm install && node run.mjs`. Numbers are placeholder
order-of-magnitude estimates traceable to published work (GiveWell CEAs;
Rethink Priorities / Fischer welfare ranges; invertebrate and x-risk
estimates), with source URLs on each org in `assumptions/0_parochial.py`. See
[`squiggle/README.md`](squiggle/README.md).

## Bottom-line allocator (`allocate.py`)

`python3 allocate.py --center W --diversification D [--animal-weight M]` prints
each org's expected cost-effectiveness (as a multiple of GiveWell top
charities) and its share of a portfolio; `--list` shows the 23 worldviews by
id (`w0`, `w1_2`, `w1_2_5`, …). The worldview-diversification coefficient sets
the spread: `D = 0` funds only the center worldview's single best org (pure
EV-max); higher `D` spreads credence across worldviews by how many assumptions
they disagree about, funding the best org in each. The flat override
worldviews put their credence share on "— nothing (ranking flat)". The orgs
and the worldview tree are composed from `assumptions/` (nothing is hard-coded
here).

## Sources

- Ajeya Cotra, *Worldview diversification and how big the future could be*,
  80,000 Hours Podcast #90 —
  https://80000hours.org/podcast/episodes/ajeya-cotra-worldview-diversification/
- Alexander Berger, *Improving global health and wellbeing in clear and direct
  ways*, 80,000 Hours Podcast —
  https://80000hours.org/podcast/episodes/alexander-berger-improving-global-health-wellbeing-clear-direct-ways/
- *When to get off the train to crazy town?* — EA Forum —
  https://forum.effectivealtruism.org/posts/feejxTPvBJY2cfXRp/when-to-get-off-the-train-to-crazy-town
- Rethink Priorities, *Welfare range estimates* —
  https://rethinkpriorities.org/research-area/welfare-range-estimates/
