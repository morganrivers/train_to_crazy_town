"""
squiggle_playground.py — turn a worldview's Squiggle model into a temporary,
no-account Squiggle *playground* link.

Clicking a node in the diagram opens its model, live and editable, with no
Squiggle Hub account. The generated models (squiggle/worldviews/*.squiggle) are
STANDALONE — the assumption chain is composed in Python before the Squiggle is
rendered, so there are no imports to resolve — which means the file content can
be packed straight into the playground URL hash.

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
import urllib.parse
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

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


def playground_url(node):
    """A node dict (from train_tree.json) -> its playground URL, or None if the
    node carries no Squiggle model path."""
    if not node.get("squiggle"):
        return None
    with open(os.path.join(ROOT, *node["squiggle"].split("/"))) as f:
        return encode_playground_url(f.read())


# ---- self-test --------------------------------------------------------------
def roundtrip(node):
    """encode -> decode reproduces the source byte-for-byte (local guarantee)."""
    with open(os.path.join(ROOT, *node["squiggle"].split("/"))) as f:
        src = f.read()
    return decode_playground_url(encode_playground_url(src)) == src


if __name__ == "__main__":
    tree = json.load(open(os.path.join(HERE, "train_tree.json")))
    for node in tree["nodes"]:
        url = playground_url(node)
        assert roundtrip(node), f"roundtrip failed for {node['id']}"
        print(f"{node['id']:16} {len(url):5d} chars  {url[:72]}…")
    print("\nall links round-trip (decode reproduces the source byte-for-byte)")
