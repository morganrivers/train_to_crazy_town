"""worldviews.py — compose assumption files into worldviews.

The single source of truth for the train to crazy town is the numbered Python
ASSUMPTION files in this directory (`0_parochial.py` … `9_boltzmann_brain.py`).
An assumption modifies, in a simple way, the chain of assumptions before it: it
adds new functions, redefines functions, or changes parameters to functions.

A WORLDVIEW (a node in the tree) is a chain of assumptions: this module `exec`s
the chain's files, in numeric (craziness) order, into ONE shared namespace, so
each file sees — and may capture, wrap, or replace — everything defined so far.
The composed namespace's `squiggle()` renders a standalone Squiggle model whose
`worldviewEv` is the expected value of that worldview; `expected_values()` is
its Python-side twin (used for top picks and the allocator).

Combinatorics are limited by each assumption's metadata, so only chains a real
person could plausibly hold are generated:
  REQUIRES — assumptions that must already be in the chain (an animals person
             won't think only people in their community matter);
  EXCLUDES — assumptions that cannot be held together;
  TERMINAL — the assumption invalidates everything before it (override), so it
             is only generated on its minimal REQUIRES-closure chain — any
             larger chain would produce an identical model.

Every worldview's parent is the same chain minus its craziest (highest-numbered)
assumption, so the graph is a tree and each edge adds exactly one assumption.
"""
import ast
import os
import re
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
FILE_RE = re.compile(r"^(\d+)_([a-z0-9_]+)\.py$")

_META_KEYS = ("NAME", "LABEL", "EDGE_LABEL", "DESC", "FIGURES",
              "REQUIRES", "EXCLUDES", "TERMINAL")


class Assumption:
    def __init__(self, number, path, source, meta):
        self.number = number
        self.path = path
        self.source = source
        for k in _META_KEYS:
            setattr(self, k.lower(), meta[k])

    def __repr__(self):
        return f"<Assumption {self.number}_{self.name}>"


def _metadata(source, path):
    """Pull the module-level UPPERCASE literal assignments out of an assumption
    file WITHOUT executing it (files past the root reference names that only
    exist once the chain is composed, so a bare exec would NameError)."""
    meta = {}
    for node in ast.parse(source, path).body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1 \
                and isinstance(node.targets[0], ast.Name) \
                and node.targets[0].id in _META_KEYS:
            meta[node.targets[0].id] = ast.literal_eval(node.value)
    missing = [k for k in _META_KEYS if k not in meta]
    if missing:
        raise ValueError(f"{path} is missing metadata: {', '.join(missing)}")
    return meta


def load_assumptions():
    """{number: Assumption} for every numbered file, checked for a linear
    0..N numbering (no doubling, no gaps) and resolvable metadata."""
    found = {}
    for fn in sorted(os.listdir(HERE)):
        m = FILE_RE.match(fn)
        if not m:
            continue
        n = int(m.group(1))
        if n in found:
            raise ValueError(f"assumption number {n} is doubled: "
                             f"{os.path.basename(found[n].path)} and {fn}")
        path = os.path.join(HERE, fn)
        with open(path) as f:
            source = f.read()
        meta = _metadata(source, path)
        if meta["NAME"] != m.group(2):
            raise ValueError(f"{fn}: NAME {meta['NAME']!r} != filename")
        found[n] = Assumption(n, path, source, meta)
    numbers = sorted(found)
    if numbers != list(range(len(numbers))):
        raise ValueError(f"assumption numbers must run 0..N with no gaps, got {numbers}")
    by_name = {a.name: a for a in found.values()}
    for a in found.values():
        for dep in a.requires + a.excludes:
            if dep not in by_name:
                raise ValueError(f"{a!r} references unknown assumption {dep!r}")
        for dep in a.requires:
            if by_name[dep].number >= a.number:
                raise ValueError(f"{a!r} requires {dep!r}, which is not less crazy")
    return found


ASSUMPTIONS = load_assumptions()
_BY_NAME = {a.name: a for a in ASSUMPTIONS.values()}
BASE = ASSUMPTIONS[0]


def compose(numbers):
    """Exec the chain (base + the given assumption numbers, in order) into one
    namespace and return it."""
    ns = {}
    for n in [0] + sorted(set(numbers) - {0}):
        a = ASSUMPTIONS[n]
        exec(compile(a.source, a.path, "exec"), ns)
    return ns


def closure(numbers):
    """The REQUIRES-closure of a set of assumption numbers."""
    todo = set(numbers)
    out = set()
    while todo:
        n = todo.pop()
        out.add(n)
        for dep in ASSUMPTIONS[n].requires:
            d = _BY_NAME[dep].number
            if d not in out:
                todo.add(d)
    return frozenset(out)


def is_valid(numbers):
    """Could one person plausibly hold exactly this set of assumptions?"""
    s = frozenset(numbers) - {0}
    if closure(s) != s:                    # a required assumption is missing
        return False
    for n in s:
        for ex in ASSUMPTIONS[n].excludes:
            if _BY_NAME[ex].number in s:   # mutually exclusive assumptions
                return False
    for n in s:
        if ASSUMPTIONS[n].terminal and s != closure({n}):
            return False                   # overrides only ride their minimal chain
    return True


def _wid(numbers):
    return "w0" if not numbers else "w" + "_".join(str(n) for n in sorted(numbers))


def enumerate_sets():
    """Every valid assumption set (excluding the implicit base), root first."""
    pool = sorted(n for n in ASSUMPTIONS if n > 0)
    out = []
    for r in range(len(pool) + 1):
        for combo in combinations(pool, r):
            if is_valid(combo):
                out.append(frozenset(combo))
    return out


def build_worldview(numbers):
    """One worldview record: identity, tree position, composed results."""
    s = sorted(numbers)
    chain = [ASSUMPTIONS[n] for n in [0] + s]
    last = chain[-1]
    wid = _wid(s)
    ns = compose(s)
    evs = ns["expected_values"]()
    flat = max(evs.values()) == min(evs.values())
    top_pick = "nothing — ranking flat" if flat else max(evs, key=evs.get)

    chain_str = " → ".join(f"{a.number} {a.name}" for a in chain)
    header = "\n".join([
        f"// === Train to crazy town — worldview {wid} (stop {last.number}) ===",
        f"// Assumption chain: {chain_str}",
        "// Each assumption is a Python file in assumptions/ that adds, redefines or",
        "// re-parameterises the chain's functions; composing the chain rendered this",
        "// standalone model. `worldviewEv` is the expected value of this worldview.",
        f"// Best buy under these assumptions: {top_pick}.",
        "// GENERATED by generate.py — edit assumptions/*.py, not this file.",
    ])
    lbl = last.label if not s else f"{last.label}\n[{'+'.join(str(n) for n in s)}]"
    return {
        "id": wid,
        "numbers": s,
        "chain": [a.name for a in chain],
        "parent": None if not s else _wid(s[:-1]),
        "stop": last.number,          # how far down the line this worldview rides
        "depth": len(s),              # how many assumptions it accepts
        "label": last.label,
        "lbl": lbl,
        "file": " + ".join(a.name for a in chain),
        "figures": last.figures,
        "edge_label": last.edge_label,
        "edge_kind": "override" if last.terminal else "expand",
        "desc": last.desc + " || Chain: " + chain_str,
        "top_pick": top_pick,
        "evs": evs,
        "coefficients": {org["name"]: ns["coefficient"](org) for org in ns["SLATE"]},
        "squiggle_source": ns["squiggle"](header),
    }


def worldviews():
    """All worldview records, ordered by (stop, depth, id)."""
    out = [build_worldview(s) for s in enumerate_sets()]
    out.sort(key=lambda w: (w["stop"], w["depth"], w["id"]))
    by_id = {w["id"]: w for w in out}
    for w in out:
        assert w["parent"] is None or w["parent"] in by_id, \
            f"{w['id']}: parent {w['parent']} is not itself a valid worldview"
    return out


def slate():
    """The fixed donation slate (from the base assumption)."""
    return compose([])["SLATE"]
