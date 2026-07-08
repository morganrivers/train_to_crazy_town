#!/usr/bin/env python3
"""
Code generator: turn data/model.json (the single source of truth) into the three
derived representations, so no number lives in more than one place.

Writes / overwrites:
  - diagram/train_tree.json                (node/edge graph the diagram builds from)
  - squiggle/base_model.squiggle           (the GENERATED SOUP KITCHEN BOTEC, SLATE
                                            and DEFAULTS blocks only)
  - squiggle/nodes/*.squiggle              (one per stop that has a Squiggle model;
                                            each imports its PARENT node and merges
                                            its one-line `sets` delta)

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


# ---- number / value formatting for Squiggle --------------------------------
def sq_num(n):
    """Render a JSON number as compact Squiggle source (drop trailing .0)."""
    if isinstance(n, bool):
        return "true" if n else "false"
    if isinstance(n, int):
        return str(n)
    if isinstance(n, float) and n.is_integer():
        return str(int(n))
    return repr(n)


def sq_val(v):
    """Render a JSON scalar (number/bool/string) as Squiggle source."""
    if isinstance(v, str):
        return f'"{v}"'
    return sq_num(v)


def sq_neurons(n):
    if math.isclose(n, M.CONSTANTS["human_neurons"]):
        return "humanNeurons"
    return sq_num(n)


def camel(s):
    """snake_case / id -> camelCase Squiggle identifier."""
    parts = s.split("_")
    return parts[0] + "".join(p.capitalize() for p in parts[1:])


def botec_var(org):
    return camel(org["id"]) + "DalyPerUsd"


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
            "parent": s.get("parent"),
            "file": s["file"],
            "lbl": s["label"],
            "top_pick": pick,
            "sets": s.get("sets", {}),
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
                     "by hand. Nodes are get-off points (a coefficient record); each edge "
                     "flips ONE crucial consideration, recorded in the child's `sets`. Every "
                     "node ranks the SAME donation slate; only the coefficients change, so "
                     "'top_pick' changes as you ride down. 'parent' is the node whose coeffs "
                     "this one inherits and merges its `sets` onto. 'figures' names the public "
                     "people who most prominently articulate that stop's worldview. The tree "
                     "forks at s3_inverts (soil branch A / longtermist branch F), forks again "
                     "at s4_future (discount / nuclear / astronomical), and ends past s5_astro "
                     "in the two override stops (Boltzmann brain B, moral anti-realism R)."),
        "slate": [o["name"] for o in M.ORGS],
        "nodes": nodes,
        "edges": M.EDGES,
    }
    return json.dumps(tree, indent=2, ensure_ascii=False) + "\n"


# ---- squiggle/base_model.squiggle (three generated blocks) ------------------
def build_soup_botec_block():
    """The soup-kitchen worked BOTEC, rendered from the org's `botec` inputs."""
    org = next(o for o in M.ORGS if o.get("botec"))
    b = org["botec"]
    plo, phi = b["people_helped_per_usd"]
    wlo, whi = b["wellbeing_gain_daly"]
    cf = b["counterfactual_bank_value"]
    return "\n".join([
        f"{botec_var(org)} = {{",
        f"  peopleHelpedPerUsd = {sq_num(plo)} to {sq_num(phi)}",
        f"  wellbeingGainDaly = {sq_num(wlo)} to {sq_num(whi)}",
        f"  counterfactualBankValue = {sq_num(cf)}",
        f"  peopleHelpedPerUsd * wellbeingGainDaly * (1 - counterfactualBankValue)",
        f"}}",
    ])


def build_slate_block():
    lines = ["slate = ["]
    for o in M.squiggle_orgs():
        dom = M.DOMAINS[o["domain"]]["squiggle"]
        if o.get("botec"):
            daly = botec_var(o)
        else:
            lo, hi = M.org_daly_per_usd(o)
            daly = f"{sq_num(lo)} to {sq_num(hi)}"
        lines.append(
            f'  {{ name: "{o["name"]}", domain: "{dom}", '
            f'daly_per_usd: {daly}, neurons: {sq_neurons(o["neurons"])} }},'
        )
    lines.append("]")
    return "\n".join(lines)


def build_defaults_block():
    lines = ["export defaults = {"]
    for k, v in M.COEFF_DEFAULTS.items():
        lines.append(f"  {k}: {sq_val(v)},")
    lines.append("}")
    return "\n".join(lines)


REGIONS = [
    ("// >>> GENERATED SOUP KITCHEN BOTEC", "// <<< GENERATED SOUP KITCHEN BOTEC", build_soup_botec_block),
    ("// >>> GENERATED SLATE", "// <<< GENERATED SLATE", build_slate_block),
    ("// >>> GENERATED DEFAULTS", "// <<< GENERATED DEFAULTS", build_defaults_block),
]


def replace_region(lines, start_marker, end_marker, inner):
    try:
        i = next(k for k, l in enumerate(lines) if l.startswith(start_marker))
        j = next(k for k, l in enumerate(lines) if l.startswith(end_marker))
    except StopIteration:
        raise SystemExit(f"markers {start_marker!r}/{end_marker!r} not found in {BASE_MODEL}")
    return lines[:i + 1] + inner.splitlines() + lines[j:]


def build_base_model(existing):
    lines = existing.splitlines()
    for start, end, builder in REGIONS:
        lines = replace_region(lines, start, end, builder())
    return "\n".join(lines) + "\n"


# ---- squiggle/nodes/*.squiggle (import-chain, one delta per node) -----------
def build_node(s):
    figs = ", ".join(s["figures"])
    headline = " ".join(s["label"].split("\n"))
    pick = s["top_pick"] + (f' ({s["top_pick_note"]})' if s.get("top_pick_note") else "")
    parent = s.get("parent")
    delta = s.get("sets", {})
    delta_src = "{ " + ", ".join(f"{k}: {sq_val(v)}" for k, v in delta.items()) + " }"

    imports = f'import "hub:{HUB_OWNER}/base_model" as base\n'
    if parent:
        imports += f'import "hub:{HUB_OWNER}/{parent}" as parent\n'
        inherited = "parent.coeffs"
        inherit_note = f"inherits {parent}"
    else:
        inherited = "base.defaults"
        inherit_note = "starts from base.defaults (the parochial root)"

    if delta:
        coeffs_line = f"export coeffs = Dict.merge({inherited}, {delta_src})"
        adds = "adds " + ", ".join(f"{k}={sq_val(v)}" for k, v in delta.items())
    else:
        coeffs_line = f"export coeffs = {inherited}"
        adds = "adds nothing (the root baseline)"

    return (
        f"// Stop {s['stop']} ({s['branch']}) - {headline}. Exemplar(s): {figs}.\n"
        f"// This node {inherit_note} and {adds}.\n"
        f"// Winner (illustrative): {pick}.\n"
        f"// GENERATED from data/model.json by data/generate.py - do not edit by hand.\n"
        f"{imports}"
        f"\n"
        f"{coeffs_line}\n"
        f"\n"
        f"ranking = base.evaluate(coeffs)\n"
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
