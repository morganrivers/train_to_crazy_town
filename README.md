# Train to Crazy Town

How far down the effective-altruism reasoning train should you ride — and what
should you donate to at each stop?

This repo answers that with a **worldview explorer**: a zoomable tree of
"get-off points" where every node is a worldview, every worldview ranks the
same nine donation targets by expected value, and the winner changes as you
accept one more assumption. Click any node and its full cost-effectiveness
model opens in a live, editable [Squiggle](https://www.squiggle-language.com)
playground — no account needed — so you can change any number and watch the
ranking re-rank.

[![Train to crazy town — worldview tree](diagram/train_tree.png)](https://viewer.diagrams.net/?lightbox=1&nav=1&chrome=0#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fmorganrivers%2Ftrain_to_crazy_town%2Fmain%2Fdiagram%2Ftrain_tree.drawio)

**[Open the interactive diagram](https://viewer.diagrams.net/?lightbox=1&nav=1&chrome=0#Uhttps%3A%2F%2Fraw.githubusercontent.com%2Fmorganrivers%2Ftrain_to_crazy_town%2Fmain%2Fdiagram%2Ftrain_tree.drawio)**
(read-only draw.io viewer, no account, pan/zoom; hover a node for its story,
click it for its live model — draw.io serves the committed `train_tree.drawio`
straight from its raw GitHub URL). Also available as
[PNG](https://raw.githubusercontent.com/morganrivers/train_to_crazy_town/main/diagram/train_tree.png)
/ [SVG](https://raw.githubusercontent.com/morganrivers/train_to_crazy_town/main/diagram/train_tree.svg)
(the SVG is clickable too).

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

## How to read the tree

- **A node is a worldview** — a chain of numbered assumptions (the `[1+2+5]`
  tag), with the donation target that worldview ranks first and the public
  figures who most prominently articulate its latest assumption.
- **An edge accepts exactly one more assumption.**
- **A band (STOP 0–11) is how far down the line a worldview rides** — its
  craziest accepted assumption, coloured calm slate at the top to override
  violet at the bottom.
- **The decision rule never changes.** Every worldview maximizes expected
  welfare-adjusted DALYs averted per dollar (`wDALY/$` — a DALY scaled by a
  species' welfare range, so one unit covers human health, animals, and future
  minds). Only the assumptions change; the same optimizer returns different
  winners.

## The assumptions (ordered by how crazy they are)

The root worldview is parochial: only my family and local community count, and
a soup kitchen wins. Each numbered assumption modifies the worldview before it:

1. **far-away humans count** — distance is not morally relevant → global health
2. **animals count, somewhat** — neuron-weighted welfare → corporate campaigns
3. **future humans matter, discounted** — heavily discounted → global health holds
4. **no discounting the future** — astronomical stakes → AI safety
5. **animals matter a lot** — Rethink Priorities welfare ranges, invertebrates,
   the ~10^19 soil animals → wild-insect welfare
6. **suffering-focused ethics** — averting suffering beats creating happiness
7. **the meat-eater problem** — a saved human eats animals for a lifetime, so
   human charities are charged for the factory farming they cause
8. **net-negative animal lives** — farmed and wild lives aren't worth living;
   with the meat-eater problem, human charities come out net-harmful
9. **living in a simulation** — the far future only counts if it keeps running
10. **morality is not real** — every value goes to 0; keep your money
11. **Boltzmann brain** — only this moment's feeling is real; nothing to choose

Not every combination is a coherent person — an animals person won't think only
their own community matters, and the near-term meat-eater bookkeeping is moot
once astronomical stakes dominate — so compatibility rules prune 2,048 possible
chains to **39 worldviews**. The ladder, the rules, and how chains compose are
documented in [`assumptions/README.md`](assumptions/README.md).

## What's in the repo

- **[`assumptions/`](assumptions/README.md)** — the single source of truth: ten
  numbered Python assumption files that compose into the 39 worldviews.
- **[`squiggle/`](squiggle/README.md)** — one standalone Squiggle model per
  worldview (generated), each exporting its ranking and `worldviewEv`, the
  expected value of that worldview. Runnable locally, in the playground links,
  or on Squiggle Hub.
- **[`diagram/`](diagram/README.md)** — the Graphviz → draw.io / PNG / SVG
  pipeline that draws the tree and wires every node to its playground link.
- **`allocate.py`** — a worldview-diversified donation allocator:

  ```bash
  python3 allocate.py --center w1_2_5 --diversification 2
  ```

  prints each org's expected cost-effectiveness (as a multiple of GiveWell top
  charities) and its share of a portfolio. `--center` is the worldview you lean
  toward (`--list` shows all 23); `--diversification 0` goes all-in on its
  single winner, higher values spread credence across nearby worldviews and
  fund the best org in each.
- **`generate.py` / `test_worldviews.py`** — regenerate every derived file from
  the assumptions and assert (in CI) that nothing has drifted.

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
- *The meat-eater problem* — EA Forum topic —
  https://forum.effectivealtruism.org/topics/meat-eater-problem
- Brian Tomasik, *The Importance of Wild-Animal Suffering* —
  https://reducing-suffering.org/the-importance-of-wild-animal-suffering/
- *Cost-effectiveness of corporate campaigns for chicken welfare* — EA Forum —
  https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken
- *Cost-effectiveness of the Shrimp Welfare Project's Humane Slaughter
  Initiative* — EA Forum —
  https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane
- *Cost-effectiveness of paying farmers to use more humane pesticides* — EA
  Forum —
  https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane
