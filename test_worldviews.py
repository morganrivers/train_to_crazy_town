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
    assert sorted(W.ASSUMPTIONS) == list(range(12))


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
    """REQUIRES/EXCLUDES/TERMINAL cut 2^11 subsets down to a plausible few."""
    assert len(VIEWS) == 39, f"expected 39 worldviews, got {len(VIEWS)}"
    assert not W.is_valid({2}), "animals person must also count far-away humans"
    assert not W.is_valid({1, 4}), "no-discounting requires the discounting stop first"
    assert not W.is_valid({1, 2, 7, 8}), "net-negative lives requires animals_matter_a_lot"
    assert not W.is_valid({1, 2, 3, 4, 5, 7}), \
        "the meat-eater problem is a near-term stop, not combined with no-discounting"
    assert not W.is_valid({1, 3, 4, 9, 10, 11}), "the two overrides exclude each other"
    assert not W.is_valid({1, 2, 3, 4, 5, 9, 10}), "overrides only ride their minimal chain"
    assert W.is_valid({1, 3, 4, 9, 10})


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
    assert BY_ID["w1_3"]["top_pick"] == "GiveWell top charity (AMF)"
    assert BY_ID["w1_3_4"]["top_pick"] == "AI safety (Redwood Research)"
    assert BY_ID["w1_2_5"]["top_pick"] == "Wild insects (humane pesticides)"


def test_overrides_go_flat():
    """The end of the line: anti-realism sets every value to 0; the Boltzmann
    brain collapses everything to one equal pleasant thought."""
    assert set(BY_ID["w1_3_4_9_10"]["evs"].values()) == {0.0}
    assert set(BY_ID["w1_3_4_9_11"]["evs"].values()) == {1e-6}


def test_meat_eater_and_net_negative_lives():
    """The two animal-side externality assumptions. The meat-eater problem
    charges human orgs for their beneficiaries' diets; net-negative lives has no
    meat channel of its own but amplifies that penalty into net-harmful territory."""
    amf = "GiveWell top charity (AMF)"
    # meat-eater alone shaves human value but (under neuron weights) keeps it positive
    assert 0 < BY_ID["w1_2_7"]["evs"][amf] < BY_ID["w1_2"]["evs"][amf]
    # net-negative lives alone touches no human org (it only boosts animal work)
    assert BY_ID["w1_2_5_8"]["evs"][amf] == BY_ID["w1_2_5"]["evs"][amf]
    # both together, under heavy animal weight, drive human charities net-negative
    assert BY_ID["w1_2_5_7_8"]["evs"][amf] < 0
    assert BY_ID["w1_2_5_7_8"]["evs"]["Local soup kitchen"] < 0


def test_playground_links_roundtrip():
    """The draw.io node links carry the whole model; decoding must reproduce it."""
    sys.path.insert(0, os.path.join(ROOT, "diagram"))
    from squiggle_playground import encode_playground_url, decode_playground_url
    src = BY_ID["w1_2_5"]["squiggle_source"]
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
