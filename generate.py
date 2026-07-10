#!/usr/bin/env python3
"""
Code generator: compose the assumption chains in assumptions/ (the single
source of truth) into every derived representation.

Writes / overwrites:
  - diagram/train_tree.json           (the worldview graph the diagram builds from)
  - squiggle/worldviews/*.squiggle    (one STANDALONE Squiggle model per worldview,
                                       rendered by running the chain's Python)

Usage:
  python3 generate.py            # regenerate everything
  python3 generate.py --check    # exit non-zero if anything is stale (no writes)

test_worldviews.py wraps --check so CI fails when a generated file drifts from
the assumptions. This is also what the GitHub Action runs: it looks at the
assumptions/ layout, runs the Python for each worldview, and the diagram +
draw.io link are built from the result.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "diagram"))
from assumptions import worldviews as W  # noqa: E402
import partition as P  # noqa: E402  (diagram/partition.py)

TRAIN_TREE = os.path.join(ROOT, "diagram", "train_tree.json")
SQUIGGLE_DIR = os.path.join(ROOT, "squiggle", "worldviews")


def squiggle_relpath(w):
    return f"squiggle/worldviews/{w['id']}.squiggle"


def build_train_tree(views):
    nodes = []
    edges = []
    for w in views:
        nodes.append({
            "id": w["id"],
            "stop": w["stop"],
            "depth": w["depth"],
            "parent": w["parent"],
            "assumptions": w["numbers"],
            "file": w["file"],
            "lbl": w["lbl"],
            "top_pick": w["top_pick"],
            "picks": w["picks"],
            "figures": w["figures"],
            "squiggle": squiggle_relpath(w),
            "desc": w["desc"],
        })
        if w["parent"] is not None:
            edges.append({"from": w["parent"], "to": w["id"],
                          "label": w["edge_label"], "kind": w["edge_kind"]})
    tree = {
        "_comment": ("GENERATED from assumptions/*.py by generate.py - do not edit by "
                     "hand. Each node is a WORLDVIEW: a chain of numbered assumptions, "
                     "composed by exec-ing the assumption files in craziness order. Each "
                     "edge adds exactly ONE assumption (the child's highest-numbered one). "
                     "'stop' is the craziest assumption the worldview accepts - how far "
                     "down the line it rides; 'depth' is how many assumptions it holds. "
                     "Every worldview ranks the SAME donation slate; 'top_pick' is the "
                     "Python-side argmax, matching the generated Squiggle model. REQUIRES/"
                     "EXCLUDES/TERMINAL metadata on the assumptions limits which chains a "
                     "real person could plausibly hold, so the combinatorial explosion "
                     "stays small. 'pages' is the render layout: the tree is cut into "
                     "bounded, clickable diagram pages (diagram/partition.py), each a "
                     "subtree; a subtree big enough for its own page is COLLAPSED on its "
                     "parent page to a boundary node linking to it."),
        "slate": [o["name"] for o in W.slate()],
        "nodes": nodes,
        "edges": edges,
        "pages": P.partition(nodes),
    }
    return json.dumps(tree, indent=2, ensure_ascii=False) + "\n"


def targets():
    """{path: desired_content} for every generated file."""
    views = W.worldviews()
    out = {TRAIN_TREE: build_train_tree(views)}
    for w in views:
        out[os.path.join(ROOT, *squiggle_relpath(w).split("/"))] = w["squiggle_source"]
    return out


def orphans(target_paths):
    """Committed .squiggle files no current worldview generates (stale ids)."""
    if not os.path.isdir(SQUIGGLE_DIR):
        return []
    return sorted(
        os.path.join(SQUIGGLE_DIR, f)
        for f in os.listdir(SQUIGGLE_DIR)
        if f.endswith(".squiggle") and os.path.join(SQUIGGLE_DIR, f) not in target_paths
    )


def main():
    ap = argparse.ArgumentParser(description="Generate derived files from assumptions/*.py.")
    ap.add_argument("--check", action="store_true",
                    help="report stale/missing/orphaned files and exit non-zero; write nothing")
    args = ap.parse_args()

    desired = targets()
    stale = []
    for path, content in desired.items():
        rel = os.path.relpath(path, ROOT)
        current = open(path).read() if os.path.exists(path) else None
        if current == content:
            continue
        stale.append(rel)
        if not args.check:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            print(f"wrote {rel}")

    extra = orphans(set(desired))
    for path in extra:
        rel = os.path.relpath(path, ROOT)
        if not args.check:
            os.remove(path)
            print(f"removed orphan {rel}")

    if args.check:
        if stale or extra:
            print("STALE (run `python3 generate.py`):")
            for rel in stale:
                print(f"  {rel}")
            for path in extra:
                print(f"  {os.path.relpath(path, ROOT)} (orphan)")
            sys.exit(1)
        print("all generated files are up to date")
    elif not stale and not extra:
        print("nothing to do; all generated files already current")


if __name__ == "__main__":
    main()
