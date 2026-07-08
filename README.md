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
longtermists ride further (animals → invertebrates → future people → x-risk). A
later stop can retroactively reframe an earlier one.

## What this is

- **The decision rule never changes.** Every node maximizes expected value.
- **What changes is the moral-parameter vector** — the crucial considerations:
  who counts (nation → all humans → animals → invertebrates → future minds), how
  much each counts (welfare ranges, neuron-count exponents), and how time and
  uncertainty are treated.
- **A node** = a fixed set of those assumptions. Getting off at a node =
  endorsing its assumptions and donating to whatever it ranks first.
- **An edge** = flipping one crucial consideration.

The same optimizer returns different winners as the assumptions change.

## The metric: expected welfare-adjusted DALYs per dollar

The unit is DALYs averted per dollar, the native unit of global-health
cost-effectiveness (WHO/GBD, GiveWell-adjacent). It generalizes to a
welfare-adjusted DALY (`wDALY`): a DALY scaled by a species' sentience-adjusted
welfare range (Rethink Priorities / Bob Fischer). One human DALY = 1 wDALY; a
shrimp-DALY is worth its welfare range, which spans ~10⁻¹² to ~1× a human's
under a neuron-count exponent from 0 to 2. One unit covers human health, animals,
and future minds. Each node reports `E[wDALY averted per $]` per target and ranks
them.

## The donation slate (fixed across all nodes)

The same candidates appear at every stop; only their EV changes as assumptions
flip. Ordered by how much moral expansion they reward:

| Target | Cause | Rides to about... |
|---|---|---|
| **Local Rotary Club** | Community / civic | the root (parochial) |
| **GiveDirectly** | Global poor, direct cash | moral circle = all present humans |
| **GiveWell top charity (AMF)** | Global health, lives saved | same, DALY-maximizing |
| **AIM / Charity Entrepreneurship** | Incubation across health, policy, animals | higher-variance, expanding scope |
| **The Humane League** | Farmed vertebrates | moral circle includes animals |
| **Shrimp Welfare Project** | Invertebrates | the exponent-sensitive stops |
| **Wild insects (humane pesticides)** | Wild / soil invertebrates | the soil-animal branch (A) |
| **ALLFED** | Global catastrophic risk / resilience | near–far bridge, future people |
| **AI safety (Redwood Research)** | Existential risk, astronomical waste | the far end of the line |

## The tree

- **Root** = the least crazy assumptions: only local humans count; heavy
  time-discounting; only near-certain, measurable effects; humans only. The
  optimizer favors the local/civic option.
- **Each child flips one crucial consideration** — drop the nationality discount
  → all humans; add animals with a welfare range → farm-animal orgs; add
  invertebrates plus a neuron-count exponent → Shrimp Welfare Project; add future
  people and accept small-probability/large-payoff bets → x-risk. The winner
  changes as you descend.
- **The tree forks** at the invertebrate stop into a soil-animal branch (**A**),
  where counting ~10¹⁹ soil animals reverses which human charities look good, and
  a longtermist branch (**F**), future people → astronomical stakes. Further
  nesting (the soil sub-tree of macroarthropods / microarthropods / nematodes; a
  digital-minds / x-risk sub-tree) is where a node later expands into its own
  child tree.

## Single source of truth (`data/`)

Every number lives once, in **[`data/model.json`](data/model.json)**: the orgs
(with sourced cost-effectiveness figures), the worldview/branch tree, and the
assumption knobs. `allocate.py` reads it directly; `diagram/train_tree.json` and
the Squiggle models are **generated** from it by `data/generate.py`; and
`data/test_sync.py` (run in CI) fails if any generated copy drifts. Edit
`model.json`, run `python3 data/generate.py`, and all three representations move
together. See [`data/README.md`](data/README.md).

## Diagram pipeline (`diagram/`)

Graph-generation code mirroring the Graphviz→draw.io setup in
`morganrivers/iati_webapp` (`docs/diagram/`):

- **`train_tree.json`** — the node/edge graph, **generated from
  `data/model.json`** (do not hand-edit). Nodes are get-off points with a
  `top_pick`, a `squiggle` model path, and a `figures` list — the public figures
  who most prominently articulate that stop's worldview (Berger; Singer /
  Bollard; Tomasik; Cotra / Ord; Bostrom / Yudkowsky). Edges are
  crucial-consideration flips.
- **`graph_common.py`** — shared primitives (Graphviz `dot` run + plain-format
  parse, coordinate transform, node/edge/band/mxfile emission), adapted from
  iati's `drawio_common.py`.
- **`build_diagram.py`** — reads the JSON, lays the tree top→bottom on a
  craziness gradient by stop, bands each stop, writes an editable `.drawio`, and
  prints a read-only draw.io view link. Requires Graphviz `dot` on PATH.
- **`render_diagram.py`** — renders `train_tree.json` → PNG/SVG directly with
  Graphviz (no draw.io app needed). These two images ARE committed and linked
  below via their raw GitHub URLs, so they never depend on GitHub Pages.

![Train to crazy town — worldview tree](diagram/train_tree.png)

The committed `train_tree.drawio` is served read-only by draw.io from its raw
GitHub URL (`build_diagram.py` prints the link). The rendered images are:

- PNG: https://raw.githubusercontent.com/morganrivers/train_to_crazy_town/main/diagram/train_tree.png
- SVG: https://raw.githubusercontent.com/morganrivers/train_to_crazy_town/main/diagram/train_tree.svg

These raw URLs work with no repo settings. The same images are also published to
GitHub Pages once it is enabled (Settings → Pages → Source = "GitHub Actions"):
`https://morganrivers.github.io/train_to_crazy_town/`.

Regenerate them with `python diagram/render_diagram.py`; CI
(`.github/workflows/diagram.yml`) re-renders on every change to confirm the
generator still works.

## Models (`squiggle/`)

The shared logic lives in `squiggle/base_model.squiggle` (fixed slate +
`E[wDALY averted/$]` formula + `export evaluate(assumptions)`). Each node is a
model in `squiggle/nodes/` that imports the base and sets its own assumptions.
`build_diagram.py` links each diagram node to its model's source file on GitHub
(`squiggle/nodes/<node-id>.squiggle`); run them locally with
`cd squiggle && npm install && node run.mjs`, or publish them to
[Squiggle Hub](https://squigglehub.org) for the interactive calculator. Numbers are placeholder
order-of-magnitude estimates traceable to published work (GiveWell CEAs; Rethink
Priorities / Fischer welfare ranges; invertebrate and x-risk estimates). See
[`squiggle/README.md`](squiggle/README.md).

## Bottom-line allocator (`allocate.py`)

`python3 allocate.py --center W --diversification D [--animal-weight M]` prints
each org's cost-effectiveness (as a multiple of GiveWell top charities) and its
share of a portfolio; `--list` shows the worldviews (`parochial`, `all_humans`,
`animals`, `inverts`, `soil`, `future`, `astro`). The worldview-diversification
coefficient sets the ordering: `D = 0` funds only the center worldview's single
best org (pure EV-max); higher `D` spreads credence across worldviews by depth
and funds the best org in each. The orgs, their figures and the worldview tree
are read from `data/model.json` (nothing is hard-coded here).

The tree forks after the invertebrate stop into a soil-animal branch — where the
sign of the effect on ~10¹⁹ nematodes reverses which human charities look good —
and a longtermist branch. Animal and invertebrate cost-effectiveness figures are
copied from published EA Forum cost-effectiveness analyses (cited in the file):
corporate campaigns ≈ 1.51×10³, Shrimp Welfare Project ≈ 6.43×10⁴, and wild-insect
humane pesticides ≈ 2.37×10⁴ times GiveWell top charities; counting soil animals
lifts GiveWell's own cropland effect to ≈ 1.11×10⁵× (sign uncertain). Human,
future and x-risk figures are placeholders. The digital-minds branch is omitted
for lack of comparable published numbers.

## Sources

- Ajeya Cotra, *Worldview diversification and how big the future could be*,
  80,000 Hours Podcast #90 —
  https://80000hours.org/podcast/episodes/ajeya-cotra-worldview-diversification/
- Alexander Berger, *Improving global health and wellbeing in clear and direct
  ways*, 80,000 Hours Podcast —
  https://80000hours.org/podcast/episodes/alexander-berger-improving-global-health-wellbeing-clear-direct-ways/
- *When to get off the train to crazy town?* — EA Forum —
  https://forum.effectivealtruism.org/posts/feejxTPvBJY2cfXRp/when-to-get-off-the-train-to-crazy-town
