#!/usr/bin/env python3
"""
Code generator: turn data/model.json (the single source of truth) into the three
derived representations, so no number lives in more than one place.

Writes / overwrites:
  - diagram/train_tree.json                (node/edge graph the diagram builds from)
  - squiggle/base_model.squiggle           (the GENERATED SLATE block only)
  - squiggle/nodes/*.squiggle              (one per stop that has a Squiggle model)

Usage:
  python3 data/generate.py            # regenerate everything
  python3 data/generate.py --check    # exit non-zero if anything is stale (no writes)

data/test_sync.py wraps --check so CI fails when a generated file drifts from the
model. Squiggle numbers are order-of-magnitude BOTECs; the model.json comment and
each org's `source` keep their provenance.
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import model as M  # noqa: E402

TRAIN_TREE = os.path.join(ROOT, "diagram", "train_tree.json")
BASE_MODEL = os.path.join(ROOT, "squiggle", "base_model.squiggle")
NODES_DIR = os.path.join(ROOT, "squiggle", "nodes")
HUB_OWNER = "morganrivers"

SLATE_START = "// >>> GENERATED SLATE"
SLATE_END = "// <<< GENERATED SLATE"


# ---- number formatting for Squiggle ----------------------------------------
def sq_num(n):
    """Render a JSON number as compact Squiggle source (drop trailing .0)."""
    if isinstance(n, bool):
        return "true" if n else "false"
    if isinstance(n, int):
        return str(n)
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return repr(n)


def sq_neurons(n):
    if math.isclose(n, M.CONSTANTS["human_neurons"]):
        return "humanNeurons"
    return sq_num(n)


# ---- diagram/train_tree.json ------------------------------------------------
def build_train_tree():
    nodes = []
    for s in M.STOPS:
        pick = s["top_pick"]
        if s.get("top_pick_note"):
            pick = f'{pick}  ({s["top_pick_note"]})'
        node = {
            "id": s["id"],
            "stop": s["stop"],
            "branch": s["branch"],
            "file": s["file"],
            "lbl": s["label"],
            "top_pick": pick,
            "figures": s["figures"],
            "squiggle": (f'squiggle/nodes/{s["id"]}.squiggle'
                         if s.get("squiggle", True) else None),
        }
        if s.get("subgraph"):
            node["subgraph"] = True
        node["desc"] = s["desc"]
        nodes.append(node)

    tree = {
        "_comment": ("GENERATED from data/model.json by data/generate.py - do not edit "
                     "by hand. Nodes are get-off points (a fixed set of moral assumptions); "
                     "edges are crucial-consideration flips. Every node ranks the SAME "
                     "donation slate; only the assumptions change, so 'top_pick' changes as "
                     "you ride down. 'figures' names the public people who most prominently "
                     "articulate that stop's worldview. The tree forks at s3_inverts into a "
                     "soil-animal branch (A) and a longtermist branch (F)."),
        "slate": [o["name"] for o in M.ORGS],
        "nodes": nodes,
        "edges": M.EDGES,
    }
    return json.dumps(tree, indent=2, ensure_ascii=False) + "\n"


# ---- squiggle/base_model.squiggle (slate block) -----------------------------
def build_slate_block():
    lines = ["slate = ["]
    for o in M.squiggle_orgs():
        dom = M.DOMAINS[o["domain"]]["squiggle"]
        lo, hi = o["daly_per_usd"]
        lines.append(
            f'  {{ name: "{o["name"]}", domain: "{dom}", '
            f'daly_per_usd: {sq_num(lo)} to {sq_num(hi)}, neurons: {sq_neurons(o["neurons"])} }},'
        )
    lines.append("]")
    return "\n".join(lines)


def build_base_model(existing):
    lines = existing.splitlines()
    try:
        i = next(k for k, l in enumerate(lines) if l.startswith(SLATE_START))
        j = next(k for k, l in enumerate(lines) if l.startswith(SLATE_END))
    except StopIteration:
        raise SystemExit(f"markers {SLATE_START!r}/{SLATE_END!r} not found in {BASE_MODEL}")
    out = lines[:i + 1] + build_slate_block().splitlines() + lines[j:]
    return "\n".join(out) + "\n"


# ---- squiggle/nodes/*.squiggle ----------------------------------------------
def build_node(s):
    w = M.weights_from_circle(s["circle"])
    figs = ", ".join(s["figures"])
    headline = " ".join(s["label"].split("\n"))
    pick = s["top_pick"] + (f' ({s["top_pick_note"]})' if s.get("top_pick_note") else "")
    weight_line = ", ".join(f"{k}: {v}" for k, v in w.items())
    return (
        f"// Stop {s['stop']} ({s['branch']}) - {headline}. Exemplar(s): {figs}.\n"
        f"// Expected winner: {pick}.\n"
        f"// GENERATED from data/model.json by data/generate.py - do not edit by hand.\n"
        f'import "hub:{HUB_OWNER}/base_model" as base\n'
        f"\n"
        f"assumptions = {{\n"
        f"  {weight_line},\n"
        f"  neuron_exponent: {sq_num(s['neuron_exponent'])},\n"
        f"  accept_tiny_prob: {str(s['accept_tiny_prob']).lower()},\n"
        f"}}\n"
        f"\n"
        f"ranking = base.evaluate(assumptions)\n"
    )


# ---- driver -----------------------------------------------------------------
def targets():
    """Return {path: desired_content} for every generated file."""
    out = {TRAIN_TREE: build_train_tree()}
    with open(BASE_MODEL) as f:
        out[BASE_MODEL] = build_base_model(f.read())
    for s in M.squiggle_stops():
        out[os.path.join(NODES_DIR, f"{s['id']}.squiggle")] = build_node(s)
    return out


def main():
    ap = argparse.ArgumentParser(description="Generate derived files from data/model.json.")
    ap.add_argument("--check", action="store_true",
                    help="report stale/missing files and exit non-zero; write nothing")
    args = ap.parse_args()

    stale = []
    for path, content in targets().items():
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

    if args.check:
        if stale:
            print("STALE (run `python3 data/generate.py`):")
            for rel in stale:
                print(f"  {rel}")
            sys.exit(1)
        print("all generated files are up to date")
    elif not stale:
        print("nothing to do; all generated files already current")


if __name__ == "__main__":
    main()
