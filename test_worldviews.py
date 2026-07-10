#!/usr/bin/env python3
"""
Tests for the assumption-chain pipeline: assumptions/*.py is the single source
of truth, and every derived representation must stay in sync with it.

Runnable two ways:
  python3 test_worldviews.py     # plain, no deps
  pytest test_worldviews.py

Core guarantee: every generated file (diagram/train_tree.json,
squiggle/worldviews/*.squiggle) is byte-identical to what generate.py would
produce right now, so a hand edit to a generated file cannot land silently.
On top of that: the combination rules really limit the combinatorics, the tree
is well-formed (each edge adds exactly one assumption), and the composed
worldviews behave (circles only grow until an override; overrides go flat).
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

import generate                            # noqa: E402
from assumptions import worldviews as W    # noqa: E402

VIEWS = W.worldviews()
BY_ID = {w["id"]: w for w in VIEWS}


def test_generated_files_are_current():
    """diagram + squiggle files match the generator output (no manual drift)."""
    stale = []
    desired = generate.targets()
    for path, content in desired.items():
        rel = os.path.relpath(path, ROOT)
        current = open(path).read() if os.path.exists(path) else None
        if current != content:
            stale.append(rel)
    stale += [os.path.relpath(p, ROOT) + " (orphan)"
              for p in generate.orphans(set(desired))]
    assert not stale, ("stale generated files (run `python3 generate.py`): "
                       + ", ".join(stale))


def test_numbering_is_linear():
    """Assumption files are numbered 0..N with no doubling and no gaps
    (load_assumptions raises otherwise; assert the expected ladder here)."""
    assert sorted(W.ASSUMPTIONS) == list(range(21))


def test_each_edge_adds_exactly_one_assumption():
    """Every worldview's parent is the same chain minus its craziest assumption,
    so the graph is a tree of single-assumption steps."""
    for w in VIEWS:
        if w["parent"] is None:
            assert w["id"] == "w0"
            continue
        parent = BY_ID[w["parent"]]
        assert parent["numbers"] == w["numbers"][:-1], \
            f'{w["id"]}: parent {parent["id"]} is not chain-minus-craziest'


def test_combination_rules_limit_the_explosion():
    """REQUIRES/EXCLUDES/TERMINAL cut 2^20 subsets down to a plausible few."""
    assert len(VIEWS) == 411, f"expected 411 worldviews, got {len(VIEWS)}"
    assert not W.is_valid({2}), "animals person must also count far-away humans"
    assert not W.is_valid({1, 6}), "no-discounting requires the discounting stop first"
    assert not W.is_valid({1, 2, 9, 10}), "net-negative lives requires animals_matter_a_lot"
    assert not W.is_valid({1, 2, 5, 6, 7, 9}), \
        "the meat-eater problem is a near-term stop, not combined with no-discounting"
    assert not W.is_valid({1, 2, 17}), "person-affecting view requires no-discounting"
    assert not W.is_valid({1, 2, 18}), "soil animals requires animals_matter_a_lot"
    assert not W.is_valid({1, 2, 5, 6, 7, 18}), \
        "soil animals is a near-term stop, not combined with no-discounting"
    assert not W.is_valid({1, 5, 6, 16, 19, 20}), "the two overrides exclude each other"
    assert not W.is_valid({1, 2, 5, 6, 7, 16, 19}), "overrides only ride their minimal chain"
    assert W.is_valid({1, 5, 6, 16, 19})
    # nature intrinsic value: requires far-away humans, moot under astronomical stakes
    assert not W.is_valid({3}), "nature requires far_away_humans"
    assert not W.is_valid({1, 3, 5, 6}), "nature excludes no_discounting (moot under astronomical stakes)"
    assert W.is_valid({1, 3}) and W.is_valid({1, 2, 3, 5})
    # climate tipping points: requires far-away humans, moot under astronomical stakes
    assert not W.is_valid({4}), "climate requires far_away_humans"
    assert not W.is_valid({1, 4, 5, 6}), "climate excludes no_discounting (moot under astronomical stakes)"
    assert W.is_valid({1, 4}) and W.is_valid({1, 3, 4})
    # nuclear second-order forks: require the undiscounted future, mutually exclusive
    assert not W.is_valid({1, 5, 11}), "deterrence fork requires no_discounting"
    assert not W.is_valid({1, 5, 6, 12, 13}), "the two collapse-reroll forks exclude each other"
    assert not W.is_valid({1, 5, 6, 11, 12}), "deterrence and collapse forks are mutually exclusive"
    assert W.is_valid({1, 5, 6, 13}), "collapse_degrades rides a longtermist chain"
    # space second-order forks: two readings of the hazard curve, mutually exclusive
    assert not W.is_valid({1, 5, 14}), "perils-exit fork requires no_discounting"
    assert not W.is_valid({1, 5, 6, 14, 15}), "the two space forks exclude each other"
    assert W.is_valid({1, 5, 6, 15}), "space-backfire rides a longtermist chain"
    assert W.is_valid({1, 5, 6, 13, 14}), "a nuclear fork and a space fork combine"


def test_moral_circle_only_grows():
    """A child worldview never zeroes an org its parent counted — the circle
    only grows down the train, until a TERMINAL override invalidates it all."""
    for w in VIEWS:
        if w["parent"] is None or w["edge_kind"] == "override":
            continue
        parent = BY_ID[w["parent"]]
        for org, c in parent["coefficients"].items():
            assert not (c > 0 and w["coefficients"][org] == 0), \
                f'{w["id"]} drops {org} from its parent\'s circle'


def test_top_picks_are_real_orgs_or_flat():
    names = {o["name"] for o in W.slate()}
    for w in VIEWS:
        flat = min(w["evs"].values()) == max(w["evs"].values())
        if flat:
            assert w["top_pick"] == "nothing — ranking flat"
        else:
            assert w["top_pick"] in names, f'{w["id"]} top_pick {w["top_pick"]!r}'


def test_the_train_actually_moves():
    """The narrative anchor points: the winner changes as assumptions accumulate."""
    assert BY_ID["w0"]["top_pick"] == "Local soup kitchen"
    assert BY_ID["w1"]["top_pick"] == "GiveWell top charity (AMF)"
    assert BY_ID["w1_2"]["top_pick"] == "The Humane League"
    assert BY_ID["w1_5"]["top_pick"] == "GiveWell top charity (AMF)"
    assert BY_ID["w1_5_6"]["top_pick"] == "AI safety (Redwood Research)"
    assert BY_ID["w1_2_7"]["top_pick"] == "Shrimp Welfare Project"
    # nature intrinsic value wins where animals are NOT in the circle to dominate
    assert BY_ID["w1_3"]["top_pick"] == "Rainforest Trust"
    assert BY_ID["w1_2_3"]["top_pick"] == "The Humane League"  # animals still beat nature
    # the pessimistic collapse-reroll flips the longtermist best buy to ALLFED
    assert BY_ID["w1_5_6_13"]["top_pick"] == "ALLFED"
    assert BY_ID["w1_5_6_12"]["top_pick"] == "AI safety (Redwood Research)"
    # climate tipping points: CATF wins where neither animals nor nature dominate,
    # and the forest co-benefit keeps Rainforest Trust ahead when both are held
    assert BY_ID["w1_4"]["top_pick"] == "Clean Air Task Force"
    assert BY_ID["w1_3_4"]["top_pick"] == "Rainforest Trust"


def test_space_forks_scale_the_shared_future():
    """The two space forks are opposite multipliers on the SAME shared future:
    the perils-exit reading inflates both future orgs, the backfire reading
    trims both — and neither flips the AI-safety-vs-ALLFED race by itself."""
    ai, af = "AI safety (Redwood Research)", "ALLFED"
    base, exit_, backfire = (BY_ID["w1_5_6"]["evs"], BY_ID["w1_5_6_14"]["evs"],
                             BY_ID["w1_5_6_15"]["evs"])
    assert exit_[ai] > base[ai] and exit_[af] > base[af]
    assert backfire[ai] < base[ai] and backfire[af] < base[af]
    # same multiplier on both orgs: the race ratio is untouched by either fork
    for evs in (exit_, backfire):
        assert abs(evs[ai] / evs[af] - base[ai] / base[af]) < 1e-9
    # the backfire fork trims (mean ~0.19) but does not zero the window's value:
    # x-risk work still beats every near-term org under it
    assert backfire[ai] > backfire["GiveWell top charity (AMF)"]


def test_worked_botecs_decide_the_longtermist_race():
    """ALLFED and AI safety are worked BOTECs sharing the same astronomical
    future, so which wins is arithmetic on their x-risk-reduced-per-dollar, not a
    forced multiplier. On the slate's central inputs AI safety edges ALLFED."""
    ai = BY_ID["w1_5_6"]["evs"]["AI safety (Redwood Research)"]
    allfed = BY_ID["w1_5_6"]["evs"]["ALLFED"]
    assert ai > allfed > 0, "both far-future orgs positive, AI safety ahead here"
    assert 1.2 < ai / allfed < 3, f"expected a close race, got {ai/allfed:.2f}x"
    # a POSITIVE pure-time discount annihilates the astronomical future, so the
    # moderate longtermist (stop 5) still ranks present global health on top
    amf = "GiveWell top charity (AMF)"
    assert BY_ID["w1_5"]["evs"]["ALLFED"] < BY_ID["w1_5"]["evs"][amf]


def test_new_assumptions_flip_the_ranking():
    """Each added assumption changes an INPUT and the best buy moves; the
    animals-matter worldview reproduces Grilo's published multiples."""
    amf = "GiveWell top charity (AMF)"
    # soil animals: the cropland externality drives human charities net-negative
    assert BY_ID["w1_2_7"]["evs"][amf] > 0
    assert BY_ID["w1_2_7_18"]["evs"][amf] < 0
    # person-affecting view collapses the astronomical case; animal-inclusive
    # longtermism flips off AI safety back to the best animal buy
    assert BY_ID["w1_2_5_6_7"]["top_pick"] == "AI safety (Redwood Research)"
    assert BY_ID["w1_2_5_6_7_17"]["top_pick"] == "Shrimp Welfare Project"
    # the mirror: at RP welfare ranges, SWP reproduces Grilo's ~64k x GiveWell
    gw = BY_ID["w1_2_7"]["evs"][amf]
    swp = BY_ID["w1_2_7"]["evs"]["Shrimp Welfare Project"]
    assert 4e4 < swp / gw < 9e4, f"SWP is {swp/gw:.0f}x GiveWell, expected ~64k"


def test_calibration_reproduces_published_figures():
    """The slate's CIs are calibrated so their lognormal MEANS reproduce the
    published numbers each entry cites: Grilo's ~0.00994 DALY/$ GiveWell
    baseline, and (at RP welfare ranges, w1_2_7) his ~460x / ~64k x / ~24k x
    multiples for chickens, shrimp and wild insects."""
    amf = "GiveWell top charity (AMF)"
    gw = BY_ID["w1"]["evs"][amf]
    assert abs(gw - 0.00994) / 0.00994 < 0.02, f"GiveWell baseline drifted: {gw}"
    evs = BY_ID["w1_2_7"]["evs"]
    assert 300 < evs["The Humane League"] / gw < 700, "THL should be ~460x GiveWell"
    assert 4e4 < evs["Shrimp Welfare Project"] / gw < 9e4, "SWP should be ~64k x"
    assert 1.5e4 < evs["Wild insects (humane pesticides)"] / gw < 3.5e4, \
        "wild insects should be ~24k x"
    # Screwworm Free Future reproduces Grilo's ~1.67-4.59 human-equiv DALY/$
    assert 1.67 < evs["Screwworm Free Future"] < 4.59, \
        "screwworm should sit in Grilo's published band"
    # Rainforest Trust carries no welfare value until the nature assumption
    assert evs["Rainforest Trust"] == 0.0


def test_new_orgs_enter_at_the_right_stop():
    """Screwworm (wild vertebrate) is outside the circle until wild animals
    fully count; Rainforest Trust is outside every current worldview's circle."""
    assert BY_ID["w1_2"]["evs"]["Screwworm Free Future"] == 0.0     # before animals_matter_a_lot
    assert BY_ID["w1_2_7"]["evs"]["Screwworm Free Future"] > 0.0    # after
    # Rainforest Trust carries value exactly on the chains that hold nature (3)
    assert BY_ID["w1_3"]["evs"]["Rainforest Trust"] > 0.0
    for w in VIEWS:
        if w["edge_kind"] == "override":
            continue  # the terminal overrides flatten every org (0 or 1e-6)
        holds_nature = 3 in w["numbers"]
        assert (w["evs"]["Rainforest Trust"] > 0.0) == holds_nature, \
            f'{w["id"]}: Rainforest Trust value should track holding nature (3)'
        # Clean Air Task Force carries value exactly on the chains holding climate (4)
        holds_climate = 4 in w["numbers"]
        assert (w["evs"]["Clean Air Task Force"] > 0.0) == holds_climate, \
            f'{w["id"]}: CATF value should track holding climate (4)'


def test_models_carry_the_chains_distributions():
    """Every uncertain moral parameter an assumption registers appears as a
    NAMED DISTRIBUTION in the generated model of a chain that holds it — and
    assumption 6 visibly pins the discount to 1 rather than deleting it."""
    src = lambda wid: BY_ID[wid]["squiggle_source"]  # noqa: E731
    assert "futureDiscount = Sym.lognormal" in src("w1_5")
    assert "futureDiscount = 1" in src("w1_5_6")
    assert "simulationContinues = Sym.beta(1, 9)" in src("w1_5_6_16")
    assert "presentPeopleFraction = Sym.lognormal" in src("w1_2_5_6_7_17")
    assert "sufferingPriority = Sym.lognormal" in src("w1_2_8")
    assert "tippingPointMultiplier = Sym.lognormal" in src("w1_4")
    assert "perilsExitMultiplier = Sym.lognormal" in src("w1_5_6_14")
    assert "spaceBackfireMultiplier = Sym.lognormal" in src("w1_5_6_15")
    # the forest co-benefit only appears when the chain ALSO holds nature (3)
    assert "forestTippingCobenefit = Sym.lognormal" in src("w1_3_4")
    assert "forestTippingCobenefit" not in src("w1_4")
    # every model ships a full distribution next to its exact mean
    assert "dist:" in src("w1_2_7") and "wdalyPerUsd:" in src("w1_2_7")
    # ... and no model regressed to the sampled-mean `to` syntax
    for w in VIEWS:
        for line in w["squiggle_source"].splitlines():
            if "=" in line and not line.lstrip().startswith("//"):
                assert " to " not in line.split("//")[0], \
                    f'{w["id"]}: sampled `to` distribution in {line!r}'


def test_worldview_models_summarise_botecs_and_link_out():
    """Direct effects appear in worldview models as ONE moment-matched lognormal
    summary per org that links to its botec derivation — the full factor
    breakdown is NOT inlined into every worldview model."""
    src = BY_ID["w1_5_6"]["squiggle_source"]
    assert "allfedDalyPerUsd = Sym.lognormal" in src
    assert "full derivation: squiggle/botecs/allfed.squiggle" in src
    # the mechanistic factors live in the botec model, not the worldview model
    assert "allfedPCatastrophePerCentury" not in src
    assert "redwoodXRiskReducedPerDollar" not in src


def test_botec_models_carry_factors_and_provenance():
    """Each botec renders a standalone full-derivation model whose factors are
    tagged with provenance; the shared future factor is defined once and used by
    both far-future orgs."""
    import botecs
    src = {b.id: botecs.render_botec(b) for b in botecs.all_botecs()}
    assert "allfedPCatastrophePerCentury = Sym.lognormal" in src["allfed"]
    assert "[expert-judgment]" in src["allfed"]
    assert "pAICatastropheThisCentury = Sym.lognormal" in src["redwood"]
    # the shared future factors are the SAME objects in both far-future botecs,
    # and flagged shared so the Monte-Carlo draws them once per world-state
    for name in ("humansPerCentury", "expectedFutureCenturies", "dalyPerFutureLife"):
        assert botecs.get("allfed").factors[name] is botecs.get("redwood").factors[name]
        assert botecs.get("allfed").factors[name].shared
    # every factor's provenance is a known kind
    for b in botecs.all_botecs():
        for f in b.factors.values():
            assert f.provenance in botecs.PROVENANCE_KINDS


def test_botec_means_match_the_python_ranking():
    """A botec's analytic mean equals the direct-effect the ranking uses, and
    its moment-matched summary lognormal has that same mean to float precision
    (so the worldview model's displayed dist and its exact wdalyPerUsd agree)."""
    import botecs
    for b in botecs.all_botecs():
        summ = b.summary_lognormal()
        if summ is None:
            continue
        assert abs(botecs.lognormal_mean(*summ) - b.mean()) / b.mean() < 1e-9


def test_credences_are_a_distribution():
    """allocate.py's worldview credences are a proper distribution: they sum
    to 1 and peak on the chosen center."""
    import allocate
    for center, div in (("w1_2", 1.0), ("w1_2_7", 2.0), ("w1_5_6", 0.5)):
        cred = allocate.credences(BY_ID[center], div)
        assert abs(sum(cred.values()) - 1.0) < 1e-9
        assert cred[center] == max(cred.values())


def test_overrides_go_flat():
    """The end of the line: anti-realism sets every value to 0; the Boltzmann
    brain collapses everything to one equal pleasant thought."""
    assert set(BY_ID["w1_5_6_16_19"]["evs"].values()) == {0.0}
    assert set(BY_ID["w1_5_6_16_20"]["evs"].values()) == {1e-6}


def test_meat_eater_and_net_negative_lives():
    """The two animal-side externality assumptions. The meat-eater problem
    charges human orgs for their beneficiaries' diets; net-negative lives has no
    meat channel of its own but amplifies that penalty into net-harmful territory."""
    amf = "GiveWell top charity (AMF)"
    # meat-eater alone shaves human value but (under neuron weights) keeps it positive
    assert 0 < BY_ID["w1_2_9"]["evs"][amf] < BY_ID["w1_2"]["evs"][amf]
    # net-negative lives alone touches no human org (it only boosts animal work)
    assert BY_ID["w1_2_7_10"]["evs"][amf] == BY_ID["w1_2_7"]["evs"][amf]
    # both together, under heavy animal weight, drive human charities net-negative
    assert BY_ID["w1_2_7_9_10"]["evs"][amf] < 0
    assert BY_ID["w1_2_7_9_10"]["evs"]["Local soup kitchen"] < 0


def test_playground_links_roundtrip():
    """The draw.io node links carry the whole model; decoding must reproduce it."""
    sys.path.insert(0, os.path.join(ROOT, "diagram"))
    from squiggle_playground import encode_playground_url, decode_playground_url
    src = BY_ID["w1_2_7"]["squiggle_source"]
    assert decode_playground_url(encode_playground_url(src)) == src


def test_diagram_pages_are_bounded_and_cover_the_tree():
    """The render layout cuts the tree into bounded, clickable pages: every
    worldview is expanded on exactly one page, no page exceeds the cap, no
    split-off subtree is tiny, and every collapse stub points to a real page
    rooted at that stub."""
    import json
    sys.path.insert(0, os.path.join(ROOT, "diagram"))
    from partition import DEFAULT_MAX_PAGE, DEFAULT_MIN_PAGE
    tree = json.load(open(os.path.join(ROOT, "diagram", "train_tree.json")))
    pages = tree["pages"]
    by_page = {p["id"]: p for p in pages}

    roots = [p for p in pages if p["is_root"]]
    assert len(roots) == 1 and roots[0]["id"] == "train_tree"

    # each worldview is the expanded (non-stub) node on exactly one page
    expanded = [i for p in pages for i in p["nodes"] if i not in p["collapsed"]]
    assert sorted(expanded) == sorted(n["id"] for n in tree["nodes"])

    for p in pages:
        assert len(p["nodes"]) <= DEFAULT_MAX_PAGE, f'{p["id"]} exceeds the page cap'
        if not p["is_root"]:
            assert len(p["nodes"]) >= DEFAULT_MIN_PAGE, f'{p["id"]} is a tiny subtree'
        for boundary, meta in p["collapsed"].items():
            child = by_page.get(meta["child"])
            assert child and child["root"] == boundary and boundary in child["nodes"], \
                f'{boundary} stub does not point at its expanded page'


def test_allocate_uses_the_canonical_slate():
    """allocate.py ranks exactly the composed slate — same names, no extra copy."""
    import allocate
    _, ew, _ = allocate.allocate(BY_ID["w1_2"], 1.0, 1.0)
    assert set(ew) == {o["name"] for o in W.slate()}


def main():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for t in tests:
        t()
        print(f"ok  {t.__name__}")
    print(f"\n{len(tests)} checks passed - assumptions, diagram and squiggle are in sync")


if __name__ == "__main__":
    main()
