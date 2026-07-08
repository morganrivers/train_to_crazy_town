"""
squiggle_playground.py — turn a node's Squiggle model into a temporary,
no-account Squiggle *playground* link.

Clicking a node in the diagram should open its model, live and editable, with no
Squiggle Hub account. The on-disk node files (squiggle/nodes/*.squiggle) can't be
opened directly for that: they `import "hub:morganrivers/..."`, and those imports
only resolve once the models are published to a Hub account. So for each node we
build ONE self-contained source — base_model inlined, and the node's PARENT
import chain resolved to a flat `coeffs` record — which runs and stays editable on
its own, then pack it into the playground URL hash.

URL format is byte-for-byte what Squiggle's own playground.ts produces:

    JSON.stringify({defaultCode: code})   # compact
      -> deflate (zlib stream; == Python zlib.compress / pako deflate)
      -> base64                            # standard alphabet
      -> encodeURIComponent                # == urllib.parse.quote(..., safe="")
    https://www.squiggle-language.com/playground#code=<that>

so decoding a link reproduces the source exactly (see roundtrip() / the CLI at
the bottom). Nothing is persisted to any account: the whole model travels in the
link.
"""
import base64
import json
import os
import sys
import urllib.parse
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BASE_MODEL = os.path.join(ROOT, "squiggle", "base_model.squiggle")

# data/model.py is the single source of truth for the coefficient chain.
sys.path.insert(0, os.path.join(ROOT, "data"))
import model as M  # noqa: E402

PLAYGROUND = "https://www.squiggle-language.com/playground"


# ---- Squiggle playground URL codec (mirrors playground.ts) ------------------
def encode_playground_url(code, base=PLAYGROUND):
    """code (Squiggle source) -> shareable playground URL. See module docstring
    for why this matches Squiggle's own encoder exactly."""
    payload = json.dumps({"defaultCode": code}, separators=(",", ":"))
    compressed = zlib.compress(payload.encode("utf-8"))
    b64 = base64.b64encode(compressed).decode("ascii")
    return base + "#code=" + urllib.parse.quote(b64, safe="")


def decode_playground_url(url):
    """Inverse of encode_playground_url: a playground URL -> its Squiggle source."""
    frag = url.split("#code=", 1)[1]
    compressed = base64.b64decode(urllib.parse.unquote(frag))
    return json.loads(zlib.decompress(compressed).decode("utf-8"))["defaultCode"]


# ---- self-contained source per node -----------------------------------------
def _sq(v):
    """Render a resolved-coeff scalar as Squiggle source."""
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, str):
        return f'"{v}"'
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return repr(v)


def _base_model_inline():
    """base_model.squiggle as inline source: its top-level `export`s become plain
    bindings so `defaults`/`evaluate` are usable directly (no `base.` prefix)."""
    text = open(BASE_MODEL).read()
    return "\n".join(
        line[len("export "):] if line.startswith("export ") else line
        for line in text.splitlines()
    )


def self_contained_source(node_id):
    """The full, import-free Squiggle source for one node id: base_model inlined
    plus this stop's resolved coefficient record and the ranking call. Runs as-is
    in the playground or via `node run.mjs` — identical ranking to the Hub-import
    version, just with the parent chain already merged."""
    stop = M.stop_by_id(node_id)
    coeffs = M.resolved_coeffs(stop)
    headline = " ".join(stop["label"].split("\n"))
    coeff_lines = "\n".join(f"  {k}: {_sq(v)}," for k, v in coeffs.items())
    return (
        f"// === Train to crazy town — {headline} (Stop {stop['stop']}) ===\n"
        f"// Self-contained playground copy of squiggle/nodes/{node_id}.squiggle:\n"
        f"// base_model is inlined and this stop's PARENT import chain is already\n"
        f"// resolved into the flat `coeffs` record below, so it runs and stays\n"
        f"// editable with NO Squiggle Hub account. Edit any coefficient (or a slate\n"
        f"// BOTEC) and the ranking re-ranks live. Generated from data/model.json.\n"
        f"\n"
        f"{_base_model_inline()}\n"
        f"\n"
        f"// ---- this stop's resolved coefficients (parent chain already merged) ----\n"
        f"coeffs = {{\n"
        f"{coeff_lines}\n"
        f"}}\n"
        f"\n"
        f"ranking = evaluate(coeffs)\n"
    )


def playground_url(node):
    """A node dict (from train_tree.json) -> its playground URL, or None if the
    node has no Squiggle model (e.g. the soil-animal branch has no published
    BOTEC to copy yet)."""
    if not node.get("squiggle"):
        return None
    return encode_playground_url(self_contained_source(node["id"]))


# ---- self-test --------------------------------------------------------------
def roundtrip(node_id):
    """encode -> decode reproduces the source byte-for-byte (local guarantee)."""
    src = self_contained_source(node_id)
    return decode_playground_url(encode_playground_url(src)) == src


if __name__ == "__main__":
    for s in M.squiggle_stops():
        url = encode_playground_url(self_contained_source(s["id"]))
        assert roundtrip(s["id"]), f"roundtrip failed for {s['id']}"
        print(f"{s['id']:16} {len(url):5d} chars  {url[:72]}…")
    print("\nall links round-trip (decode reproduces the source byte-for-byte)")
