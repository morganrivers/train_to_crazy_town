#!/usr/bin/env python3
"""
render_diagram.py — STUB. Turn the editable train_tree.drawio into PNG/SVG.

The heavy lifting (a local .drawio -> SVG/PNG renderer that needs no draw.io app)
already exists in morganrivers/iati_webapp at docs/diagram/drawio_to_png.py.
Rather than duplicate ~400 lines here, this stub just shells out to it if it's
importable, and otherwise tells you what to install.

Rendered PNG/SVG are build artifacts and are .gitignored - do NOT commit them.
Only train_tree.json + the .py generators (and, if you like, the .drawio) live
in git.

Usage:  python render_diagram.py [train_tree.drawio]
"""
import os, sys, subprocess

DRAWIO = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), 'train_tree.drawio')

# TODO: wire to iati_webapp/docs/diagram/drawio_to_png.py once its path is known,
# e.g. `python /path/to/drawio_to_png.py train_tree.drawio --svg train_tree.svg`.
CONVERTER = os.environ.get('DRAWIO_TO_PNG')  # path to iati_webapp's drawio_to_png.py

if CONVERTER and os.path.exists(CONVERTER):
    sys.exit(subprocess.call([sys.executable, CONVERTER, DRAWIO]))

print(__doc__)
print("stub: set DRAWIO_TO_PNG=/path/to/iati_webapp/docs/diagram/drawio_to_png.py, "
      "or open %s in the draw.io desktop/web app and export." % os.path.basename(DRAWIO))
