# Supplier Scorecard CLI

A local-first command-line tool to score resale suppliers (eBay, Amazon, wholesale, liquidation) on **price**, **speed (lead time)**, and **quality**. Data lives in a local JSON file. Export results to CSV. No API keys, no accounts, no cloud.

Built and maintained by **Asdale Dynamics, LLC** (Indiana, formed October 2026) — beginner-friendly AI education, practical tools, and small-business templates. Learn more at dylanasdale.github.io.

## What it does

- Add suppliers with unit price, quoted lead time (days), and quality rating (1–5)
- Score every supplier 0–100 using weighted criteria (default: price 40%, speed 35%, quality 25%)
- Track actual lead times per supplier over time (quoted vs. actual)
- View detailed supplier info including lead-time history and score breakdown
- Rank suppliers by overall score
- Remove suppliers you no longer track
- Export the scorecard to CSV
- Store everything in a local JSON file (`suppliers.json` by default)

## Install

```bash
git clone <this-repo>
cd supplier-scorecard-cli
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Or run without installing:

```bash
python3 -m supplier_scorecard.cli --help
```

## Quick Start

```bash
# Add a few suppliers
supplier-scorecard add --name "Vintage Wholesale Co" --price 12.50 --lead-time 5 --quality 4 --notes "Books and media"
supplier-scorecard add --name "Beta Distributors" --price 20.00 --lead-time 10 --quality 2
supplier-scorecard add --name "QuickShip Liquidation" --price 15.00 --lead-time 3 --quality 3

# See them ranked by score
supplier-scorecard list

# Record an actual delivery (tracks quoted vs actual)
supplier-scorecard record --id <VINTAGE_ID> --actual 7 --reference PO-1001

# View full details including lead-time history
supplier-scorecard show --id <VINTAGE_ID>

# Export to CSV for spreadsheets
supplier-scorecard export --output my-scorecard.csv

# Remove a supplier you no longer use
supplier-scorecard remove --id <BETA_ID>
```

## Commands

| Command | Description |
|---------|-------------|
| `add` | Add a new supplier |
| `list` | List all suppliers ranked by score |
| `show` | Show detailed info for one supplier (scores + lead-time history) |
| `record` | Record an actual lead time for a supplier |
| `remove` | Remove a supplier |
| `export` | Export scored suppliers to CSV |

### Global Options

- `--storage PATH` — Use a different JSON storage file (default: `suppliers.json`)

### `add` — Add a Supplier

```bash
supplier-scorecard add --name "Name" --price 12.50 --lead-time 5 --quality 4 [--notes "..."]
```

- `--name` (required): Supplier name
- `--price` (required): Unit cost (float)
- `--lead-time` (required): Quoted lead time in days (int)
- `--quality` (required): Quality rating 1–5 (float, e.g., 4.5)
- `--notes`: Optional free-text notes

### `list` — Ranked Scorecard

```bash
supplier-scorecard list
```

Outputs a table with Rank, ID, Name, Price, Lead Time, Quality, and Overall Score.

### `show` — Supplier Details

```bash
supplier-scorecard show --id <ID>
```

Shows full details: all attributes, individual criterion scores, overall rank, and complete lead-time history with on-time/early/late status.

### `record` — Log Actual Lead Time

```bash
supplier-scorecard record --id <ID> --actual 7 [--quoted 5] [--reference PO-1001]
```

- `--actual` (required): Actual days received
- `--quoted`: Override quoted days (defaults to supplier's quoted lead time)
- `--reference`: PO or order reference number

### `remove` — Delete a Supplier

```bash
supplier-scorecard remove --id <ID>
```

Permanently removes a supplier from the JSON file.

### `export` — CSV Export

```bash
supplier-scorecard export [--output scorecard.csv]
```

Exports: rank, id, name, price, quoted_lead_time, quality, price_score, speed_score, quality_score, overall_score.

## Scoring

Each criterion is normalized 0–100 against the suppliers currently in your file:

- **Price**: lower is better (cheapest = 100)
- **Speed**: lower quoted lead time is better (fastest = 100)
- **Quality**: higher is better (5 = 100, 1 = 0)

Overall score = `0.40 × price + 0.35 × speed + 0.25 × quality`.

Weights can be adjusted in `supplier_scorecard/scoring.py` (`DEFAULT_WEIGHTS`).

> **Note:** Scores are *cohort-relative*. Adding or removing a supplier re-normalizes all scores.

## Data Storage

- Single JSON file: `suppliers.json` (or custom path via `--storage`)
- Human-readable, plain text — easy to back up, version-control, or edit manually
- No database, no cloud, no accounts

Example `suppliers.json`:

```json
[
  {
    "id": "a1b2c3d4",
    "name": "Vintage Wholesale Co",
    "price": 12.5,
    "quoted_lead_time": 5,
    "quality": 4.0,
    "lead_times": [
      {"date": "2026-11-03", "quoted_days": 5, "actual_days": 7, "reference": "PO-1001"}
    ],
    "notes": "Books and media"
  }
]
```

## Tests

```bash
python3 -m unittest discover -s tests
```

All tests use the standard library (`unittest`) — no extra dependencies.

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See [LICENSE](LICENSE).

## About

Asdale Dynamics, LLC is a registered Indiana LLC founded by Dylan Asdale, a registered nurse turned AI author and founder. His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending. This tool is part of the LLC's small-business and author tooling line.