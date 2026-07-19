# Cost-effectiveness analyses similar to this framework

A catalogue of external cost-effectiveness analyses (CEAs) that are structurally
the same object as this repo's `botecs/` entries: a **worked, probabilistic
estimate of one intervention's cost-effectiveness**, usually in DALYs / WELLBYs
/ welfare-adjusted units per dollar, often with a public model you can open and
edit (Squiggle, Guesstimate, a Google Sheet, an R/Python notebook, or a live
web tool).

Two things are in this folder:

1. **This catalogue** — every source I could find, with a link to the write-up
   and, where one exists, a **direct-download link** to the model itself.
2. **[`models/`](models/)** — the analyses I could actually download and commit
   here. In the environment this was assembled in, outbound network access was
   restricted to GitHub, so the committed set is the GitHub-hosted models with a
   redistributable license or published-data status. Everything else is
   catalogued with its download link and scripted in [`fetch.sh`](fetch.sh) so
   you (or an agent on an unrestricted machine) can pull the rest in one command.

> **Legend for "Model" column**
> 🟢 = committed under [`models/`](models/) &nbsp;·&nbsp;
> 🔵 = directly downloadable (GitHub / OSF / Sheet export) — in `fetch.sh` &nbsp;·&nbsp;
> ⚪ = model is a Google Sheet / web tool you download by hand from the linked post

---

## What's committed in `models/`

| Folder | Source | License | What it is |
|---|---|---|---|
| [`rp_farmfish_stunning_cea/`](models/rp_farmfish_stunning_cea/) | Rethink Priorities | MIT | R/Quarto CEA of electrical stunning commitments for farmed finfish in Europe |
| [`rp_moral_weights_welfare_ranges/`](models/rp_moral_weights_welfare_ranges/) | Rethink Priorities | published data | The species welfare-range CSVs (the "moral weights" this repo already uses) |

Run [`fetch.sh`](fetch.sh) to add the rest of the GitHub-hosted and OSF-hosted
models under `downloaded/`.

---

## Vasco Grilo

Grilo is the most prolific author of framework-style CEAs on the EA Forum; this
repo already reproduces several of his numbers. **Every CEA post links a public
Google Sheet** (open it, `File → Download → .xlsx`, or use the
`export?format=xlsx` trick in `fetch.sh`). He also keeps a running index of his
analyses on his [EA Forum profile](https://forum.effectivealtruism.org/users/vasco-grilo).

| Analysis | Headline result | Write-up | Model |
|---|---|---|---|
| Corporate campaigns for chicken welfare | ~1.67–14.3 DALY/$ (~168–1,440× GiveWell) | [post](https://forum.effectivealtruism.org/posts/8FqWSqv9AeLowgajn/cost-effectiveness-of-corporate-campaigns-for-chicken) | ⚪ Sheet |
| Shrimp Welfare Project — Humane Slaughter Initiative | ~639 DALY/$ (~64k× GiveWell); revisited at 433 DALY/$ | [post](https://forum.effectivealtruism.org/posts/EbQysXxofbSqkbAiT/cost-effectiveness-of-shrimp-welfare-project-s-humane) | ⚪ Sheet |
| Paying farmers to use more humane pesticides | ~236 DALY/$ (~24k× GiveWell) | [post](https://forum.effectivealtruism.org/posts/mgsiDB2Kkm3mDSWWP/cost-effectiveness-of-paying-farmers-to-use-more-humane) | ⚪ Sheet |
| Policy advocacy to eradicate the New World screwworm | ~1.67–4.59 human-equiv DALY/$ | [post](https://forum.effectivealtruism.org/posts/bT3WrFn6H4fpvLSk8/policy-advocacy-for-eradicating-screwworm-looks-remarkably) | ⚪ Sheet |
| "GiveWell may have made $1bn of harmful grants" (meat-eater + soil-animal accounting) | human GHD charities can come out net-negative | [post](https://forum.effectivealtruism.org/posts/FqioYEr97eoCQMxhk/givewell-may-have-made-1-billion-dollars-of-harmful-grants) | ⚪ Sheet |
| Saving human lives increases animal welfare more than chicken campaigns? (soil animals, neuron-count power law) | net sign flips on soil-animal assumptions | [post](https://forum.effectivealtruism.org/posts/WbmDhpqKcT8gjwpso/saving-human-lives-at-the-lowest-cost-increases-animal) | ⚪ Sheet |
| Founders Pledge Climate Change Fund | maybe > GiveWell top charities, ≪ chicken campaigns | [post](https://forum.effectivealtruism.org/posts/FzSqMzZpmHdMAft7z/founders-pledge-s-climate-change-fund-might-be-more-cost) | ⚪ Sheet |
| Long-term CE of Founders Pledge's Climate Fund | longtermist reframing of the above | [post](https://forum.effectivealtruism.org/posts/NbWeRmEsBEknNHqZP/longterm-cost-effectiveness-of-founders-pledge-s-climate) | ⚪ Sheet |
| Replication / breakdown of RP's animal-welfare CE ratings | explains the discrepancies across estimates | [post](https://forum.effectivealtruism.org/posts/qARKFgYhCqmKB2YpF/explaining-the-discrepancies-in-cost-effectiveness-ratings-a) | ⚪ Sheet |
| Cost-effectiveness of operations management in high-impact orgs | ops "multiplier" survey + model | [post](https://forum.effectivealtruism.org/posts/LWN6qFhCtPDEJJpeG/cost-effectiveness-of-operations-management-in-high-impact) | ⚪ Sheet |
| Cost-effectiveness of restricted donations | restricted vs unrestricted giving | [post](https://forum.effectivealtruism.org/posts/WQPskYuCaTq8aiBhX/cost-effectiveness-of-restricted-donations) | ⚪ Sheet |

He has also written CEAs on nuclear-winter / famine tail risk and on farmed-fish
stunning (the RP model committed here). This repo's README already cites his
chicken, shrimp, humane-pesticide, screwworm and meat-eater posts.

---

## Rethink Priorities

The single richest source of framework-style, **open-source** cross-cause CEAs.

| Analysis | What it estimates | Write-up | Model |
|---|---|---|---|
| **Cross-Cause Cost-Effectiveness Model (CCM)** | GHD vs animal welfare vs x-risk on one welfare scale; Monte-Carlo over user distributions — the closest analogue to this whole repo | [overview](https://forum.effectivealtruism.org/posts/pniDWyjc9vY5sjGre/rethink-priorities-cross-cause-cost-effectiveness-model) · [live tool](https://ccm.rethinkpriorities.org/) | 🔵 [repo](https://github.com/rethinkpriorities/cross-cause-cost-effectiveness-model-public) (Python + TS) |
| **Moral Weight Project — welfare ranges** | per-species welfare ranges (the moral weights this repo uses) | [research area](https://rethinkpriorities.org/research-area/welfare-range-estimates/) | 🟢 `models/rp_moral_weights_welfare_ranges/` · [repo](https://github.com/rethinkpriorities/public_moral_weight_and_sentience) |
| Updated Moral Weight Project | distributional sentience refinement of the above | — | 🔵 [repo](https://github.com/rethinkpriorities/updated_moral_weights) |
| **Farmed finfish stunning CEA** | electrical-stunning corporate commitments in Europe | [linkpost](https://forum.effectivealtruism.org/posts/hXH2KbPK29zxKBRGC/linkpost-prospective-cost-effectiveness-of-farmed-fish) | 🟢 `models/rp_farmfish_stunning_cea/` · [repo](https://github.com/rethinkpriorities/farmfish_stunning_cea) (MIT) |
| Corporate campaigns affect 9–120 years of chicken life per $ (Šimčikas) | the chicken-campaign anchor this repo cites | [research area](https://rethinkpriorities.org/research-area/corporate-campaigns-affect-9-to-120-years-of-chicken-life-per-dollar-spent/) | ⚪ Sheet in post |
| CURVE sequence — "Causes and Uncertainty: Rethinking Value in Expectation" | whether EV-maximisation robustly favours x-risk; alternatives to EV | [sequence intro](https://forum.effectivealtruism.org/posts/9ztTCGQqhpDpiomtn/causes-and-uncertainty-rethinking-value-in-expectation) | 🔵 (CCM repo) |
| How likely is a US–Russia nuclear exchange? (Rodriguez) | ~0.38%/yr — the anchor behind this repo's ALLFED catastrophe probability | [research area](https://rethinkpriorities.org/research-area/how-likely-is-a-nuclear-exchange-between-the-us-and-russia/) | ⚪ in post |

---

## ALLFED (Alliance to Feed the Earth in Disasters)

Resilient-foods-vs-x-risk CEAs — the empirical basis of this repo's ALLFED
entry and the "resilient food vs AI safety" race.

| Analysis | Headline result | Write-up | Model |
|---|---|---|---|
| **Long-term CE of resilient foods vs AGI safety** (Denkenberger, Sandberg, Tieman, Pearce, *Int. J. Disaster Risk Reduction* 73, 2022) | ~84–99% confidence marginal resilient-food $ beats marginal AGI-safety $ | [journal](https://www.sciencedirect.com/science/article/abs/pii/S2212420922000176) · **[OSF preprint](https://osf.io/vrmpf/)** | 🔵 OSF PDF (`fetch.sh`) |
| Interventions for loss of industry / electricity resilience vs AGI safety | resilience of industry as a GCR lever | [EA Forum](https://forum.effectivealtruism.org/posts/XA8QSCL7wZ973i6vr/agi-safety-and-losing-electricity-industry-resilience-cost) · [LessWrong](https://www.lesswrong.com/posts/qkvk22oc3YeEJpEfC/agi-safety-and-losing-electricity-industry-resilience-cost) | ⚪ in paper |
| ALLFED publications index | all their peer-reviewed CEAs / GCR papers | [allfed.info/papers](https://allfed.info/papers/) | ⚪ per-paper |

---

## CEARCH (Centre for Exploratory Altruism Research)

Systematic, spreadsheet-driven CEAs across a ~700-cause longlist, ~20 researched
in depth. Everything lives in public **Google Sheets** linked from each report.

| Analysis | What it estimates | Write-up | Model |
|---|---|---|---|
| **Master cause-evaluation spreadsheet** | headline DALYs/$ (× GiveWell) for every cause they've scored | [Research Findings](https://exploratory-altruism.org/research-findings/) | ⚪ master Sheet |
| Deep report — hypertension (salt-reduction policy) | a leading recommendation | [post](https://forum.effectivealtruism.org/posts/k7NjuGEKdRSrrJHmZ/deep-report-on-hypertension) | ⚪ Sheet |
| Deep report — diabetes (sugar-sweetened-beverage taxes) | a leading recommendation | [post](https://forum.effectivealtruism.org/posts/kWXCGiFvig5HemaoN/deep-report-on-diabetes) | ⚪ Sheet |
| Other deep reports (air pollution, road safety, etc.) | non-communicable-disease policy causes | linked from Research Findings | ⚪ Sheet |

Their CEA methodology is a close cousin of this repo's: one shared model per
cause, Monte-Carlo, results in multiples of GiveWell.

---

## Brian Tomasik / reducing-suffering.org

Suffering-focused CEAs, several with downloadable spreadsheets — the intellectual
root of this repo's assumptions 7–10 (invertebrate welfare, wild-animal
suffering, net-negative lives).

| Analysis | What it estimates | Link |
|---|---|---|
| Does the Against Malaria Foundation reduce invertebrate suffering? | ~10⁴ invertebrate-years affected per $ (sign ambiguous) | [essay](https://reducing-suffering.org/malaria-foundation-reduce-invertebrate-suffering/) |
| Why charities usually don't differ astronomically in expected CE | argues most differ ≤ ~10–100× | [essay](https://reducing-suffering.org/why-charities-dont-differ-astronomically-in-cost-effectiveness/) |
| The importance of wild-animal suffering | scale estimate this repo cites | [essay](https://reducing-suffering.org/the-importance-of-wild-animal-suffering/) |
| Covariance of wealth and cost-effectiveness | correction to naive CE comparisons | [essay](https://reducing-suffering.org/covariance-of-wealth-and-cost-effectiveness/) |

Many essays embed or link Google Sheets; download by hand from the essay.

---

## Happier Lives Institute (WELLBY-based CEAs)

CEAs denominated in **WELLBYs** (wellbeing-adjusted life-years) rather than
DALYs — a parallel unit to this repo's wDALYs, useful as a cross-check.

| Analysis | Headline result | Write-up | Model |
|---|---|---|---|
| StrongMinds / psychotherapy in LMICs | ~30 WELLBYs per $1,000 (95% CI 15–75) | [report](https://www.happierlivesinstitute.org/report/talking-through-depression-the-cost-effectiveness-of-psychotherapy-in-lmics-revised-and-expanded/) | ⚪ Sheet |
| Charity comparisons (cash vs therapy vs deworming vs AMF) | ranks interventions in WELLBYs | [charity evaluations](https://www.happierlivesinstitute.org/research/charity-evaluations/) | ⚪ Sheet |
| Living review of WELLBY cost-effectiveness analyses | meta-collection of WELLBY CEAs | [living review](https://www.happierlivesinstitute.org/research/living-review-of-wellby-cost-effectiveness-analyses/) | ⚪ links |

---

## GiveWell

The reference point ("× GiveWell") this whole repo is scaled against.

| Analysis | What it is | Link | Model |
|---|---|---|---|
| Official cost-effectiveness analyses | versioned multi-sheet Excel workbooks for every top charity | [CE models](https://www.givewell.org/how-we-work/our-criteria/cost-effectiveness/cost-effectiveness-models) | 🔵 .xlsx download |
| Interactive Squiggle replication | editable re-implementation of GiveWell's model | [post](https://forum.effectivealtruism.org/posts/7QM4krYmoPtvyH9Pd/interactive-replication-of-givewell-s-cost-effectiveness) | ⚪ Squiggle |
| Welfare effects of reallocating between top charities (Tadepalli) | R model of reallocation welfare effects | [repo](https://github.com/karthiktadepalli1/givewell-reallocation) | 🔵 repo (`fetch.sh`) |

---

## Founders Pledge

| Analysis | Headline result | Link |
|---|---|---|
| Clean Air Task Force (climate) | ~$0.10–$1 per tCO₂e averted — the anchor behind this repo's CATF entry | [research](https://www.founderspledge.com/research/clean-air-task-force) |
| Climate Change Fund CEA | portfolio-level climate CE (Colab model) | [climate research](https://founderspledge.com/research/fp-climate-change) |

---

## Other framework-adjacent tooling

| Source | What it is | Link |
|---|---|---|
| **QURI / Squiggle** | the probabilistic-estimation language this repo's models are written in; Squiggle Hub hosts many public CEAs | [squiggle-language.com](https://www.squiggle-language.com) · [GitHub](https://github.com/quantifieduncertainty/squiggle) |
| Nuño Sempere | Bayesian adjustment to RP welfare ranges (the two-envelope critique this repo documents) + many Fermi/CE estimates | [blog](https://nunosempere.com/blog/2023/02/19/bayesian-adjustment-to-rethink-priorities-welfare-range-estimates/) |
| AIM / Charity Entrepreneurship | CEA template + the incubation CEAs behind new charities; "Three structural patterns across eleven AIM CEAs" | [CE CEA method](https://www.charityentrepreneurship.com/cea.html) · [11-CEA review](https://forum.effectivealtruism.org/posts/WPmfbSsCCEynHwRwH/three-structural-patterns-across-eleven-aim-cost) |
| Squiggle / 80,000 Hours Quantification Challenge | a whole set of community CEAs, several framework-style | [winners post](https://forum.effectivealtruism.org/posts/hGdsgaRiF2zH3vX5M/winners-of-the-squiggle-experimentation-and-80-000-hours) |

---

## Notes on completeness & provenance

- Headline numbers are quoted from the linked write-ups / this repo's own
  README; open the source before relying on any figure — several (e.g. Grilo's
  shrimp estimate) have been revised by their authors.
- The committed `models/` snapshots are **source-only and lightweight** (large
  regenerable data / simulation outputs were left upstream). Each carries a
  `SOURCE.md` with the exact upstream repo, commit hash, retrieval date, and
  license.
- Only redistributable material is committed: `rp_farmfish_stunning_cea` is MIT;
  the moral-weights CSVs are published research *results*. Code from
  upstream repos with **no stated license** (e.g. the CCM) is **not** copied
  here — `fetch.sh` clones it from source instead.
- This catalogue was assembled 2026-07-19.
