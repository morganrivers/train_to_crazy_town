# Train to Crazy Town

We are making objective probabilistic expected-value calculations under a set
of clear assumptions which construct coherent worldviews. The assumptions are
the moral premises — who counts, how much, under what discount — and they are
the *only* thing that varies; every empirical magnitude is an input with a
stated derivation or source to be checked, never an authority's opinion to be
trusted.

How far down the effective-altruism reasoning train should you ride — and what
should you donate to at each stop?

This repo answers that with a **worldview explorer**: a zoomable tree of
"get-off points" where every node is a worldview, every worldview ranks the
same twelve donation targets by expected value, and the winner changes as you
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
- **Each node reads out its best buy and its runner-up.** For the winner: its
  **lives-saved-equivalent per $1000** (`wDALY/$ × 1000 ÷ 30`, a human life ≈ 30
  welfare-adjusted DALYs) and a **confidence** — `P(it is actually the best buy)`
  from a Monte-Carlo over the full distributions. The runner-up is the strongest
  *challenger* (the org most likely to beat the winner) with its own confidence.
  When a winner leads only on a heavy tail its confidence is low and the
  challenger's is higher — e.g. under the person-affecting view the expected-value
  pick is AI safety (best just ~14% of the time) while GiveWell is best ~52%.
- **An edge accepts exactly one more assumption.**
- **A band (STOP 0–20) is how far down the line a worldview rides** — its
  craziest accepted assumption, coloured calm slate at the top to override
  violet at the bottom.
- **The decision rule never changes.** Every worldview maximizes expected
  welfare-adjusted DALYs averted per dollar (`wDALY/$` — a DALY scaled by a
  species' welfare range, so one unit covers human health, animals, and future
  minds). Only the assumptions change; the same optimizer returns different
  winners.
- **Every genuinely uncertain number is a distribution.** Direct effects are
  lognormal 90% CIs; uncertain moral parameters (the pure-time discount, the
  simulation-continuation probability, the suffering asymmetry, …) are named,
  cited distributions in each model's prelude. Rankings sort on exact analytic
  means, so the Python side and the Squiggle models agree to float precision —
  and editing any distribution in the playground re-ranks the slate live.
- **The tree is too big for one screen, so it's split into pages.** A branch
  large enough to deserve its own page is collapsed on its parent to a
  `▼ N more worldviews` node (dashed double border); click it to open that
  subtree's own page. The image above is the top page — the rest are one click
  in.

## The assumptions (ordered by how crazy they are)

The root worldview is parochial: only my family and local community count, and
a soup kitchen wins. Each numbered assumption modifies the worldview before it:

1. **far-away humans count** — distance is not morally relevant → global health
2. **animals count, somewhat** — neuron-weighted welfare → corporate campaigns
3. **nature has intrinsic value** — ecosystems matter for themselves, valued at
   what existence-value studies say they're worth to those who hold the belief →
   habitat protection (Rainforest Trust) wins where animals don't dominate
4. **climate damages are civilizational-scale** — Bressler's mortality cost of
   carbon, PIK's committed ~19% income loss by 2049, and Rockström tipping-point
   cascades → Clean Air Task Force (and, held together with nature, protecting
   tropical forest picks up the tipping-element co-benefit)
5. **future humans matter, discounted** — a positive pure-time rate annihilates
   the astronomical far future → global health still holds
6. **no discounting the future** — astronomical stakes → AI safety (which edges
   out ALLFED on the slate's worked BOTECs — a close, contestable race)
7. **animals matter a lot** — Rethink Priorities welfare ranges, invertebrates →
   shrimp welfare (this worldview reproduces Grilo's published numbers)
8. **suffering-focused ethics** — averting suffering beats creating happiness
9. **the meat-eater problem** — a saved human eats animals for a lifetime, so
   human charities are charged for the factory farming they cause (Grilo)
10. **net-negative animal lives** — farmed and wild lives aren't worth living;
    with the meat-eater problem, human charities come out net-harmful
11. **resilience undermines deterrence** — survivable nuclear war deters less, so
    resilient food partly self-defeats: an alternative, lower estimate for ALLFED
12. **collapse teaches (reroll better)** — survivors of a near-collapse rebuild
    wiser, so averting collapse is worth less → AI safety holds
13. **collapse degrades (reroll worse)** — survivors stagnate into a locked-in
    worse future, so averting collapse is worth far more → ALLFED overtakes AI safety
14. **time of perils, space exit** — hazard is high during the AI/nuclear
    transition but collapses once we are multiplanetary, so the expected future
    (and x-risk work during the window) scales up (Ord; the backup argument)
15. **early space expansion backfires** — the capability that settles planets
    also moves asteroids and exports nationalism (Deudney, *Dark Skies*; the
    Weinersmiths, *A City on Mars*), so below many independent settlements
    expansion *adds* risk: accelerate only after geopolitics matures, and the
    astronomical multiplier is trimmed — the sweet-spot rebuttal to 14
16. **living in a simulation** — the far future only counts if it keeps running
17. **person-affecting view** — making happy people is neutral, so the
    astronomical case for x-risk collapses (Narveson)
18. **count soil animals** — ~10^19 soil nematodes/mites; global health expands
    cropland and, on Grilo's figure, comes out net-harmful
19. **morality is not real** — every value goes to 0; keep your money
20. **Boltzmann brain** — only this moment's feeling is real; nothing to choose

Two things are deliberately *not* assumptions, because a worldview should change
what you *believe*, not force a result: **whether resilient foods beat AI
safety** is decided by the two orgs' worked BOTECs (change an input and the
ranking moves — Denkenberger & Pearce vs Linch), and **whether RP's invertebrate
welfare ranges are inflated** (the two-envelope critique) is a methodological
correction documented as a judgment call in the code, not a fork.

Not every combination is a coherent person — an animals person won't think only
their own community matters, and the near-term meat-eater bookkeeping is moot
once astronomical stakes dominate — so compatibility rules prune 1,048,576 possible
chains to **411 worldviews**. The ladder, the rules, and how chains compose are
documented in [`assumptions/README.md`](assumptions/README.md).

## What's in the repo

- **[`assumptions/`](assumptions/README.md)** — the MORAL axis and single source
  of truth: twenty-one numbered Python assumption files that compose into the 411
  worldviews. Only the moral premises fork; the empirical numbers do not.
- **`botecs/`** — the EMPIRICAL axis: one importable, worked derivation per org's
  direct effect, with each factor tagged by provenance (worked-internal /
  worked-external / empirical-anchor / expert-judgment). One true value per
  quantity, read by every worldview and improved in one place. The two
  load-bearing longtermist numbers are decomposed into mechanisms here (the AI
  x-risk figure from Carlsmith's premises, the future-at-stake from a Newberry
  decomposition with an explicit background-extinction lever), and
  [`PROVENANCE.md`](PROVENANCE.md) is a generated audit that lists every
  `expert-judgment` weak point.
- **[`squiggle/`](squiggle/README.md)** — one standalone Squiggle model per
  worldview (generated), each exporting its ranking and `worldviewEv`. Each org's
  direct effect appears as a single moment-matched lognormal summary linking to
  its full derivation in `squiggle/botecs/<id>.squiggle`, so a worldview model
  stays readable no matter how rich the mechanisms get. Runnable locally, in the
  playground links, or on Squiggle Hub.
- **[`diagram/`](diagram/README.md)** — the Graphviz → draw.io / PNG / SVG
  pipeline that draws the tree and wires every node to its playground link.
- **`allocate.py`** — a worldview-diversified donation allocator:

  ```bash
  python3 allocate.py --center w1_2_7 --diversification 2
  ```

  prints each org's expected cost-effectiveness (as a multiple of GiveWell top
  charities) and its share of a portfolio. `--center` is the worldview you lean
  toward (`--list` shows all 411); `--diversification 0` goes all-in on its
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
- Rethink Priorities, *Welfare range estimates* (Fischer et al.) —
  https://rethinkpriorities.org/research-area/welfare-range-estimates/
- *The meat-eater problem* — EA Forum topic —
  https://forum.effectivealtruism.org/topics/meat-eater-problem
- Brian Tomasik, *The Importance of Wild-Animal Suffering* —
  https://reducing-suffering.org/the-importance-of-wild-animal-suffering/
- Vasco Grilo, *Cost-effectiveness of corporate campaigns for chicken welfare*
  (~1.67–14.3 DALY/$, ~168–1,440× GiveWell) — EA Forum —
  https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken
- Saulius Šimčikas, *Corporate campaigns affect 9 to 120 years of chicken life
  per dollar spent* — Rethink Priorities —
  https://rethinkpriorities.org/research-area/corporate-campaigns-affect-9-to-120-years-of-chicken-life-per-dollar-spent/
- Vasco Grilo, *Cost-effectiveness of the Shrimp Welfare Project's Humane
  Slaughter Initiative* (639 DALY/$, ~64k× GiveWell) — EA Forum —
  https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane
- Vasco Grilo, *Cost-effectiveness of paying farmers to use more humane
  pesticides* (236 DALY/$, ~24k× GiveWell) — EA Forum —
  https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane
- Vasco Grilo, *GiveWell may have made 1 billion dollars of harmful grants...*
  (meat-eater / soil-animal accounting) — EA Forum —
  https://forum.effectivealtruism.org/posts/FqioYEr97eoCQMxhk/givewell-may-have-made-1-billion-dollars-of-harmful-grants
- Nuño Sempere, *A Bayesian Adjustment to Rethink Priorities' Welfare Range
  Estimates* —
  https://nunosempere.com/blog/2023/02/19/bayesian-adjustment-to-rethink-priorities-welfare-range-estimates/
- David Denkenberger & Joshua Pearce, *Long-term cost-effectiveness of resilient
  foods for global catastrophes compared to AGI safety* —
  https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176
- Linch Zhang, *How many EA 2021 $s would you trade off against a 0.01% chance
  of existential catastrophe?* — EA Forum —
  https://forum.effectivealtruism.org/posts/cKPkimztzKoCkZ75r/how-many-ea-2021-usds-would-you-trade-off-against-a-0-01
- Nick Bostrom, *Astronomical Waste* — https://www.nickbostrom.com/astronomical/waste.html
- Nick Bostrom, *Are You Living in a Computer Simulation?* (Philosophical
  Quarterly, 2003) — https://www.simulation-argument.com/simulation.pdf
- Ajeya Cotra, *Forecasting transformative AI: the "biological anchors" method* —
  https://www.cold-takes.com/forecasting-transformative-ai-the-biological-anchors-method-in-a-nutshell/
- Frank Ramsey, *A Mathematical Theory of Saving* (Economic Journal, 1928) —
  the classic case that a pure time preference is ethically indefensible
- Nicholas Stern et al., *The Stern Review on the Economics of Climate Change*
  (2006, pure rate δ ≈ 0.1%/yr) vs William Nordhaus, *A Review of the Stern
  Review* (JEL, 2007, ~1.5%/yr) — the published disagreement behind the
  discount-rate distribution in assumption 5
- Toby Ord, *The Precipice* (2020) — the ~1/6-per-century existential-risk
  estimate behind the catastrophe-hazard component of the discount
- Hilary Greaves & William MacAskill, *The Case for Strong Longtermism* (GPI
  working paper) — and the person-affecting objection assumption 17 encodes
- David Thorstad, *Existential risk pessimism and the time of perils* — the
  skeptical low end of the AI-safety entry's CI —
  https://globalprioritiesinstitute.org/existential-risk-pessimism-and-the-time-of-perils-david-thorstad/
- Magnus Vinding, *Suffering-Focused Ethics: Defense and Implications* (2020) —
  https://centerforreducingsuffering.org/research/suffering-focused-ethics-defense-and-implications/
- David Benatar, *Better Never to Have Been* (2006) — the asymmetry behind
  net-negative lives
- Our World in Data, *How many animals are farmed?* (FAOSTAT) — the ~26-33
  billion live chickens anchoring the meat-eater ratio —
  https://ourworldindata.org/how-many-animals-are-farmed
- Welfare Footprint Project — pain-track estimates behind the
  suffering-per-farmed-life-year CI — https://welfarefootprint.org
- Open Philanthropy, *2017 Report on Consciousness and Moral Patienthood* —
  https://www.openphilanthropy.org/research/2017-report-on-consciousness-and-moral-patienthood/
- Rethink Priorities, *Why Neuron Counts Shouldn't Be Used as Proxies for
  Moral Weight* —
  https://rethinkpriorities.org/publications/why-neuron-counts-shouldnt-be-used-as-proxies-for-moral-weight
- Joseph Carlsmith, *Is Power-Seeking AI an Existential Risk?* (Open
  Philanthropy; ~10% by 2070, six-premise decomposition behind the AI-safety
  BOTEC) — https://arxiv.org/abs/2206.13353
- Toby Newberry, *How many lives does the future hold?* (Global Priorities
  Institute — the population-per-century × expected-duration decomposition of
  the future at stake) —
  https://globalprioritiesinstitute.org/how-many-lives-does-the-future-hold-toby-newberry-future-of-humanity-institute-university-of-oxford/
- Luisa Rodriguez, *How likely is a nuclear exchange between the US and Russia?*
  (Rethink Priorities; ~0.38%/yr, the anchor for ALLFED's catastrophe
  probability and the deterrence-erosion fork) —
  https://rethinkpriorities.org/research-area/how-likely-is-a-nuclear-exchange-between-the-us-and-russia/
- Vasco Grilo, *Policy advocacy for eradicating screwworm looks remarkably
  cost-effective* (~1.67–4.59 human-equiv DALY/$, the Screwworm Free Future
  entry) —
  https://forum.effectivealtruism.org/posts/bT3WrFn6H4fpvLSk8/policy-advocacy-for-eradicating-screwworm-looks-remarkably
- Sam Peltzman, *The Effects of Automobile Safety Regulation* (JPE, 1975) — the
  risk-compensation / deterrence-erosion mechanism behind assumption 11
- Rainforest Trust — habitat protection cost-per-acre, the direct effect behind
  the nature entry — https://www.rainforesttrust.org/our-impact/our-approach/
- R. Daniel Bressler, *The mortality cost of carbon* (Nature Communications,
  2021; ~1 excess death per 4,434 tCO2 — the mortality channel of the climate
  exchange rate) — https://www.nature.com/articles/s41467-021-24487-w
- Maximilian Kotz, Anders Levermann & Leonie Wenz, *The economic commitment of
  climate change* (Nature, 2024; PIK — committed ~19% income loss by 2049, the
  income channel) — https://www.nature.com/articles/s41586-024-07219-0
- Johan Rockström et al., *A safe operating space for humanity* (Nature, 2009)
  and David Armstrong McKay et al., *Exceeding 1.5°C global warming could
  trigger multiple climate tipping points* (Science, 2022) — the tipping-point
  amplification behind assumption 4 —
  https://www.science.org/doi/10.1126/science.abn7950
- Founders Pledge, *Clean Air Task Force* (climate report; the ~$0.1–$10/tCO2e
  advocacy cost behind the CATF entry) —
  https://founderspledge.com/stories/clean-air-task-force
- Daniel Deudney, *Dark Skies: Space Expansionism, Planetary Geopolitics, and
  the Ends of Humanity* (2020) — the space-expansion-backfires fork: orbital
  and asteroid-deflection infrastructure is dual-use, and interplanetary
  anarchy is a harder security dilemma than the terrestrial one
- Kelly & Zach Weinersmith, *A City on Mars* (2023; and 80,000 Hours Podcast
  #187) — why genuinely self-sufficient, decorrelated settlements are much
  further away than settlement boosterism assumes —
  https://80000hours.org/podcast/episodes/zach-weinersmith-space-settlement/
- Toby Ord, *The Precipice* (2020), ch. "The Precipice" — the time-of-perils
  framing behind the perils-exit fork (also anchors the ~1/6-per-century
  estimate above)
