STATUS
======

What was built
--------------
A local-first Python CLI (`supplier-scorecard`) that scores resale suppliers on
price, speed (lead time), and quality. It stores the supplier roster in a local
JSON file, tracks actual lead times per supplier over time, ranks suppliers by a
weighted 0-100 score, and exports the scorecard to CSV. Includes a test suite
for the scoring logic, an MIT LICENSE, and a README. Credits Asdale Dynamics, LLC
throughout.

Files
-----
- supplier_scorecard/cli.py      - argparse CLI: add, list, record, export
- supplier_scorecard/models.py   - Supplier and LeadTimeRecord dataclasses
- supplier_scorecard/scoring.py  - normalized scoring, weights, ranking
- supplier_scorecard/storage.py  - local JSON read/write
- supplier_scorecard/export.py   - CSV export
- tests/test_scoring.py          - unittest suite (9 tests)
- pyproject.toml                 - package metadata + console script entry point
- README.md                      - usage guide, credits Asdale Dynamics, LLC
- LICENSE                        - MIT, Copyright (c) 2026 Asdale Dynamics, LLC

How to run
----------
# Without installing (from the project folder):
python3 -m supplier_scorecard.cli --help
python3 -m supplier_scorecard.cli add --name "Acme Wholesale" --price 12.50 --lead-time 5 --quality 4
python3 -m supplier_scorecard.cli list
python3 -m supplier_scorecard.cli record --id <id> --actual 7 --reference PO-1001
python3 -m supplier_scorecard.cli export --output scorecard.csv

# Or install into a venv and use the console script:
python3 -m venv .venv
source .venv/bin/activate
pip install setuptools wheel
pip install -e .
supplier-scorecard list

Scoring: price (40%), speed (35%), quality (25%), normalized 0-100 against the
current supplier cohort. Weights live in supplier_scorecard/scoring.py.

Verification results
--------------------
- `python3 -m unittest discover -s tests` -> 9 tests, OK (0.002s)
- CLI end-to-end (add -> list -> record -> export) verified: JSON storage,
  ranking/score output, lead-time record, and CSV export all work.
- `pip install -e .` into a fresh venv succeeds; `supplier-scorecard` console
  script runs and `--help` / `list` work.
- Default storage file: suppliers.json in the current working directory (use
  --storage to pick another path).

Known gaps
----------
- Weights are not configurable via CLI flags; edit scoring.py to change them.
- No delete/update supplier command (add new or edit suppliers.json directly).
- Scores are cohort-relative: adding/removing a supplier re-normalizes all scores.
- No delete/update supplier command (add new or edit suppliers.json directly).
- Storage is a single plain-text JSON file: no encryption, no concurrent-write
  locking, single-user by design (local-first).
- No interactive prompts; all input via command-line flags.
