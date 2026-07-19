#!/usr/bin/env bash
# fetch.sh — download the directly-downloadable cost-effectiveness models
# catalogued in README.md into ./downloaded/.
#
# Why this script exists: the collection in ./models/ was vendored from an
# environment whose egress policy only allowed GitHub. Google Sheets, OSF,
# and the orgs' own sites were unreachable there, so those files could not be
# committed automatically. Run this on a normal machine to pull them all.
#
# Requires: git, curl. Run from this directory:  bash fetch.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p downloaded
cd downloaded

gh_clone () { # url dir
  if [ ! -d "$2" ]; then git clone --depth 1 "$1" "$2"; else echo "have $2"; fi
}
gsheet () { # SHEET_ID out.xlsx
  curl -sSL -o "$2" "https://docs.google.com/spreadsheets/d/$1/export?format=xlsx" \
    && echo "saved $2"
}
get () { # url out
  curl -sSL -o "$2" "$1" && echo "saved $2"
}

echo "== Rethink Priorities =="
gh_clone https://github.com/rethinkpriorities/cross-cause-cost-effectiveness-model-public.git ccm
gh_clone https://github.com/rethinkpriorities/public_moral_weight_and_sentience.git moral_weights
gh_clone https://github.com/rethinkpriorities/updated_moral_weights.git updated_moral_weights
gh_clone https://github.com/rethinkpriorities/farmfish_stunning_cea.git farmfish_stunning_cea

echo "== GiveWell replications (code) =="
gh_clone https://github.com/karthiktadepalli1/givewell-reallocation.git givewell_reallocation

echo "== ALLFED — resilient foods vs AGI safety (Denkenberger et al. 2022) =="
# OSF preprint PDF (open access). If OSF blocks the automated download, open in a browser:
#   https://osf.io/vrmpf/
get "https://osf.io/download/vrmpf/" allfed_resilient_foods_vs_agi_safety.pdf || \
  echo "  -> OSF blocked automated download; get it at https://osf.io/vrmpf/"

echo
echo "== Google-Sheets-backed CEAs (fill in IDs from the linked posts) =="
echo "The following live in public Google Sheets. Open the EA Forum / org post"
echo "in README.md, copy the Sheet's ID from its URL, and run e.g.:"
echo "    gsheet <SHEET_ID> grilo_shrimp_welfare.xlsx"
echo "Sources to grab this way:"
echo "  - Vasco Grilo — every CEA post links a Sheet (shrimp, chicken campaigns,"
echo "    humane pesticides, screwworm, meat-eater/soil, Founders Pledge climate, ops)"
echo "  - CEARCH — master 'cause evaluation' Sheet + per-cause Sheets"
echo "    (hypertension, diabetes, and the rest) from exploratory-altruism.org"
echo "  - Happier Lives Institute — StrongMinds / psychotherapy WELLBY Sheets"
echo "  - GiveWell — official versioned CEA workbooks (.xlsx) from"
echo "    givewell.org/how-we-work/our-criteria/cost-effectiveness/cost-effectiveness-models"
echo
echo "Done. See README.md for the annotated catalogue and every source link."
