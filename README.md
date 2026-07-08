# Train to Crazy Town

An interactive, zoomable **tree of "get-off points"** for visualizing how far
different moral assumptions carry you down the effective-altruism reasoning
train — and how unstable the ride gets the further you go.

## The metaphor

The "train to crazy town" is Ajeya Cotra's image (80,000 Hours podcast #90,
*worldview diversification*). EA-style reasoning is a train:

> "a train going to crazy town, and the near-termist side is like, I'm going to
> get off the train before we get to the point where all we're focusing on is
> existential risk because of the astronomical waste argument."
> — Ajeya Cotra

Each **stop** is a point where accepting one more individually-plausible premise
carries you to a more counterintuitive conclusion. You are free to *get off* at
any stop. Near-termists get off early (measurable global health); longtermists
ride further (animals → invertebrates → future people → x-risk), "and there may
be further stops." The trigger for wanting off is when the reasoning "takes you
to a very weird unintuitive place — and, furthermore, wants you to give up all
of the other goals that... seem like they're worth pursuing."

Crucially, Cotra notes she "was more pro going all in on the astronomical waste
argument *before* thinking about some of the further weird things that come up as
the train keeps moving." A *later* stop can retroactively reframe an *earlier*
one. That retroactive destabilization is what this project renders.

## What this is

A visualization where:

- **The decision rule never changes.** Every node maximizes expected value —
  we keep the same cold, mathematical, expected-value style throughout. Nothing
  "irrational" happens as you ride the train.
- **What changes is the moral-parameter vector** — the *crucial considerations*:
  who counts (nation → all humans → animals → invertebrates → future/digital
  minds), how much each counts (welfare ranges, neuron-count exponents), how you
  treat time (pure discount rate) and uncertainty (whether tiny probabilities of
  huge payoffs count).
- **A "stop" / node** = a fixed set of those assumptions. **Getting off the
  train at a node** = endorsing that node's assumptions and donating to whatever
  it ranks first.
- **An edge** = flipping exactly one crucial consideration — one more step of
  moral expansion or one more bullet bitten.

So the train is not a slide from reason into madness. It is a walk through
parameter space where the *same* optimizer keeps returning different winners.

## The metric: expected value per dollar

**Use DALYs, not QALYs — but generalized.** Recommendation and rationale:

- **DALYs averted per dollar** is the native unit of global-health
  cost-effectiveness (WHO/GBD, GiveWell-adjacent analyses), so the "not crazy"
  root of the tree is already denominated in it. QALYs gained are numerically
  interchangeable (1 DALY averted ≈ 1 QALY gained) but carry health-economics
  (NICE) baggage and a "quality of a life lived" framing that travels less
  cleanly to animals and future minds.
- To ride the train we generalize to a **welfare-adjusted DALY** (call it
  `wDALY`): a DALY scaled by a species' *sentience-adjusted welfare range*
  (following the Rethink Priorities / Bob Fischer welfare-range literature). One
  human DALY = 1 wDALY by definition; a shrimp-DALY is worth its welfare range
  (Fischer's tentative point estimate ~8% of a human's, but anywhere from
  ~10⁻¹² to ~1× human under a neuron-count exponent from 0 to 2).
- This single unit spans the whole line: human health → farmed animals →
  invertebrates → (eventually) future and digital minds, all in expected
  `wDALY` averted per dollar, higher = better. The 12-orders-of-magnitude
  sensitivity of that welfare-range exponent *is* the instability we want to
  show.

Every node therefore reports, per donation target, an **E[wDALY averted per $]**
under that node's assumption vector, and ranks them.

## The donation slate (fixed across all nodes)

The same candidates appear at every stop; only their EV changes as assumptions
flip. Roughly ordered by how much moral expansion they reward:

| Target | Cause | Rides to about... |
|---|---|---|
| **Local Rotary Club** | Community / civic | the root (parochial) |
| **GiveDirectly** | Global poor, direct cash | moral circle = all present humans |
| **GiveWell top charity (AMF / bednets)** | Global health, lives saved | same, DALY-maximizing |
| **AIM / Charity Entrepreneurship** | Incubation across health, policy, animals | higher-variance, expanding scope |
| **Farm animal welfare (The Humane League)** | Farmed vertebrates | moral circle includes animals |
| **Shrimp Welfare Project** | Invertebrates | the exponent-sensitive stops |
| **ALLFED** | Global catastrophic risk / resilience | near–far bridge, future people |
| **AI safety (Redwood Research)** | Existential risk, astronomical waste | the far end of the line |

## The tree

- **Root** = the *least* crazy assumptions: only the people around me — my
  community and nation — have moral weight; heavy pure-time discounting; only
  near-certain, measurable effects count; only humans count. Under these
  assumptions the optimizer favors the local/civic option; foreigners, animals,
  and the future are discounted to near-zero. You can get off right here.
- **Each child relaxes or flips one crucial consideration** — one step of moral
  expansion (drop the nationality discount → all humans; add nonhuman animals
  with a welfare range → farmed-animal orgs jump; add invertebrates + a
  neuron-count exponent → Shrimp Welfare Project, and the ranking starts
  swinging; add future/digital minds + accept small-probability/large-payoff
  bets → x-risk). The winner changes as you descend.
- **Nested subgraphs.** Above a set node count, a node is a *summary* you click
  into: it expands into its own tree. E.g. the "invertebrates" node opens into
  the soil-animal sub-tree (macroarthropods / microarthropods / nematodes, each
  with its own conditions for whether welfare rises or falls); the "longtermism"
  node opens into a digital-minds / x-risk sub-tree. This keeps the top-level
  train legible while the crazy-town detail lives one zoom level down.
- **(Later) instability rendering.** Node heat / border = how much the ranking
  swings under a small perturbation of that node's newest parameter. Deeper
  nodes glow hotter — the same optimizer, ever less anchored.

## Branching — TBD (needs your call)

The node/edge *semantics* above are settled. What's undecided is the **branching
policy** — how one node spawns its children:

1. **Binary (accept / reject one consideration).** Each edge either bites one
   more bullet or doesn't → a clean binary tree, easy to read, but forces every
   consideration into yes/no.
2. **Multi-way per consideration.** A consideration with several defensible
   settings (e.g. the welfare-range exponent ∈ {0, 0.5, 1, 2}) fans into several
   children → richer and more honest about the instability, but wider and harder
   to lay out.
3. **Ordering of considerations.** Do we fix one canonical order of stops (the
   classic moral-expansion sequence), or does the *order itself* branch (you can
   accept animals before or after the time-discount question), producing many
   paths to the same worldview? Canonical order is far simpler; order-branching
   is more faithful but combinatorial.

My inclination: MVP with **fixed canonical ordering + binary edges** (options 1
+ single order), then introduce multi-way fan-out (option 2) exactly at the
exponent-sensitive invertebrate nodes, where the instability is the whole point.
Tell me which you want.

## Diagram pipeline (`diagram/`)

Stubbed graph-generation code, mirroring the Graphviz→draw.io setup in
`morganrivers/iati_webapp` (`docs/diagram/`):

- **`train_tree.json`** — the node/edge graph. Nodes are get-off points (one
  moral-assumption set each) with a `top_pick`, a **`squiggle`** model path, and
  a **`figures`** list — the public, famous-ish people who most prominently
  *articulate* that stop's worldview (Berger, Singer/Bollard, Tomasik,
  Cotra/Ord, Bostrom/Yudkowsky). These are exemplars of the view, not claims
  about where each person personally gets off. Edges are crucial-consideration
  flips. Currently one canonical spine (root → x-risk) plus a `subgraph`-flagged
  fork point; **branching is TBD** (above).
- **`graph_common.py`** — shared primitives (Graphviz `dot` run + plain-format
  parse, coordinate transform, node/edge/band/mxfile emission), adapted from
  iati's `drawio_common.py`.
- **`build_diagram.py`** — reads the JSON, lays the tree out top→bottom (least
  crazy at the top), colours nodes on a craziness gradient by stop, bands each
  stop, and writes an editable `.drawio`. Requires Graphviz `dot` on PATH.
- **`render_diagram.py`** — stub for `.drawio` → PNG/SVG (defers to iati's
  `drawio_to_png.py`). **PNG/SVG stay `.gitignore`d — never committed.**

**Public view link.** The repo is public, so the committed `train_tree.drawio`
is served read-only by draw.io straight from its raw GitHub URL — no account, no
export. `build_diagram.py` prints the ready-made link on each run
(`https://viewer.diagrams.net/?...&chrome=0#U<raw .drawio URL>`); override the
branch/ref with the `DIAGRAM_REF` env var.

**Rendered PNG / SVG (CI — untracked).** The workflow
`.github/workflows/diagram.yml` rebuilds the diagram on every push and publishes
the rendered images to GitHub Pages. **These PNG/SVG are generated fresh in CI
and deliberately never committed** (they stay `.gitignore`d; only the `.drawio` +
generators are in git). Once Pages is enabled (Settings → Pages → Source =
"GitHub Actions") and the workflow has run on the default branch, they live at:

- **SVG:** https://morganrivers.github.io/train_to_crazy_town/train_tree.svg
- **PNG:** https://morganrivers.github.io/train_to_crazy_town/train_tree.png
- index: https://morganrivers.github.io/train_to_crazy_town/

The `github-pages` environment is gated to the default branch by default, so the
public Pages URLs go live after this lands on `main`; on a feature branch the
same PNG/SVG are still downloadable from the workflow run's **Artifacts**.

**Per-node model = Squiggle (`squiggle/`).** The shared logic lives in
`squiggle/base_model.squiggle` (fixed slate + `E[wDALY averted/$]` formula +
`export evaluate(assumptions)`); each node is a tiny model in `squiggle/nodes/`
that imports the base and dials in its own assumptions. `build_diagram.model_link()`
turns each node's `squiggle` path into its clickable target — a raw GitHub link
by default, or a live Squiggle Hub model when `SQUIGGLE_HUB_OWNER` is set. The
models run and are validated against the Squiggle runtime (`cd squiggle &&
npm install && node run.mjs`), reproducing the intended winner at every stop
(Rotary → global health → THL → Shrimp → ALLFED → AI safety). See
[`squiggle/README.md`](squiggle/README.md). *We chose Squiggle over Guesstimate
because it's code — one shared `evaluate`, imported everywhere — rather than N
hand-cloned canvases that drift.*

## Scope

**MVP is a faithful visualizer of existing work — it invents nothing.** Every
number traces to a published estimate (GiveWell CEAs; Rethink Priorities /
Fischer welfare ranges; standard invertebrate and soil-animal
cost-effectiveness estimates; ALLFED and AI-risk back-of-envelope figures). The
contribution is the *arrangement* — showing them as one train under one
optimizer — not new moral claims.

**Not in the MVP:** autonomous agents. (A later version could let an ensemble of
worldview-subagents — Cotra's own alternative to naive EV maximization — each
ride to a different stop and reason down different branches under different
assumption vectors. Out of scope for now.)

## Sources

- Ajeya Cotra, *Worldview diversification and how big the future could be*,
  80,000 Hours Podcast #90 —
  https://80000hours.org/podcast/episodes/ajeya-cotra-worldview-diversification/
- Alexander Berger, *Improving global health and wellbeing in clear and direct
  ways*, 80,000 Hours Podcast —
  https://80000hours.org/podcast/episodes/alexander-berger-improving-global-health-wellbeing-clear-direct-ways/
- *When to get off the train to crazy town?* — EA Forum —
  https://forum.effectivealtruism.org/posts/feejxTPvBJY2cfXRp/when-to-get-off-the-train-to-crazy-town
- Bob Fischer / Rethink Priorities, moral-weights and welfare-range research
  (sentience-adjusted welfare ranges; neuron-count exponent sensitivity).
