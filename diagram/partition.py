"""
partition.py — split the worldview tree into bounded, clickable render "pages".

The tree grows combinatorially, so a single flat diagram becomes unreadable.
Instead we cut it into pages: each page shows a bounded slice of the tree, and a
subtree that is large enough to deserve its own page is COLLAPSED on its parent
page to a single boundary node (a `▼ N more worldviews` badge) that links to the
page where it is the expanded root. The model/data are untouched — this is a
pure rendering decision, so `generate.py` bakes the page layout into
train_tree.json and both diagram builders read it.

Algorithm (greedy, largest-chunk-first):
  - size every node's subtree;
  - while a page exceeds `max_page`, cut the descendant whose subtree is the
    LARGEST that still fits `<= max_page` and is `>= min_page`, moving it to its
    own page (recursively re-split there); it stays on the parent page as a
    one-node stub;
  - taking the largest fitting chunk first keeps pages balanced instead of
    shaving off fragments, and the `min_page` floor forbids splitting off
    anything small. If only small subtrees remain (a pathologically wide fan),
    accept a soft overflow on the page rather than fragment it into tiny pages —
    "aim for not having really small subtrees".

Defaults (max_page=25, min_page=6) match the "collapse a subtree once it hits
25+ nodes" rule of thumb; the min-page floor is low enough that a narrow spine
whose branches have all been split off can still form its own small page rather
than overflow its parent. Override via the env vars or the function args.
"""
import os
from collections import defaultdict

DEFAULT_MAX_PAGE = int(os.environ.get("DIAGRAM_MAX_PAGE", "25"))
DEFAULT_MIN_PAGE = int(os.environ.get("DIAGRAM_MIN_PAGE", "6"))
ROOT_PAGE_ID = "train_tree"


def child_page_id(node_id):
    """The render-page id (and file basename) for the subtree rooted at a node."""
    return f"{ROOT_PAGE_ID}__{node_id}"


def partition(nodes, max_page=DEFAULT_MAX_PAGE, min_page=DEFAULT_MIN_PAGE):
    """Return a list of page dicts, root page first. Each page is
    {id, root, is_root, nodes: [ids in this page], collapsed: {boundary_id:
    {child, count}}}. `nodes` includes each collapsed boundary once (as a stub);
    that same boundary is the `root` of its own child page."""
    by_id = {n["id"]: n for n in nodes}
    children = defaultdict(list)
    root = None
    for n in nodes:
        parent = n.get("parent")
        if parent:
            children[parent].append(n["id"])
        else:
            root = n["id"]
    if root is None:
        raise ValueError("no root node (every node has a parent)")

    depth = {}
    for i in by_id:
        d, c = 0, by_id[i]
        while c.get("parent"):
            c = by_id[c["parent"]]
            d += 1
        depth[i] = d

    def is_ancestor(a, b):
        """True if node a is a strict ancestor of node b."""
        c = by_id[b]
        while c.get("parent"):
            c = by_id[c["parent"]]
            if c["id"] == a:
                return True
        return False

    full_size = {}

    def _size(i):
        full_size[i] = 1 + sum(_size(c) for c in children[i])
        return full_size[i]
    _size(root)

    pages = []
    worklist = [(root, True)]
    while worklist:
        r, is_root = worklist.pop(0)
        cuts, cuts_set = [], set()

        def subsize(v):
            return 1 + sum(0 if c in cuts_set else subsize(c) for c in children[v])

        def page_size():
            def sz(i):
                if i != r and i in cuts_set:
                    return 1
                return 1 + sum(sz(c) for c in children[i])
            return sz(r)

        def descendants():
            out = []

            def walk(i):
                for c in children[i]:
                    out.append(c)
                    if c not in cuts_set:
                        walk(c)
            walk(r)
            return out

        while page_size() > max_page:
            cands = [v for v in descendants() if v not in cuts_set]
            fit = [v for v in cands if min_page <= subsize(v) <= max_page]
            if fit:
                v = max(fit, key=lambda x: (subsize(x), -depth[x], x))
            else:
                bigs = [v for v in cands if subsize(v) > max_page]
                if not bigs:
                    break  # only small subtrees left: accept overflow, don't fragment
                v = max(bigs, key=lambda x: (subsize(x), -depth[x], x))
            # Cuts on a page must stay an ANTICHAIN. `subsize` measures v with its
            # already-cut descendants removed, so cutting a spine node whose big
            # branches were cut earlier is exactly how the residual spine gets
            # chunked off — but v then ABSORBS those descendant cuts: they belong
            # to v's own page now (which recursively re-splits them), so drop them
            # here to avoid duplicate, overlapping pages.
            absorbed = [c for c in cuts if is_ancestor(v, c)]
            for c in absorbed:
                cuts.remove(c)
                cuts_set.discard(c)
                worklist.remove((c, False))
            cuts.append(v)
            cuts_set.add(v)
            worklist.append((v, False))

        page_nodes = []

        def collect(i):
            page_nodes.append(i)
            if i in cuts_set:
                return
            for c in children[i]:
                collect(c)
        collect(r)

        pages.append({
            "id": ROOT_PAGE_ID if is_root else child_page_id(r),
            "root": r,
            "is_root": is_root,
            "nodes": page_nodes,
            "collapsed": {v: {"child": child_page_id(v), "count": full_size[v] - 1}
                          for v in cuts},
        })
    return pages


if __name__ == "__main__":
    import json
    here = os.path.dirname(os.path.abspath(__file__))
    tree = json.load(open(os.path.join(here, "train_tree.json")))
    pages = tree.get("pages") or partition(tree["nodes"])
    print(f"{len(pages)} page(s):")
    for p in pages:
        tag = "root" if p["is_root"] else f"under {p['root']}"
        opens = "".join(f"\n      ▼ {b} → {m['child']} (+{m['count']})"
                         for b, m in p["collapsed"].items())
        print(f"  {p['id']:<28} {len(p['nodes']):>3} nodes  ({tag}){opens}")
