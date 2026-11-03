# Supplier Scorecard CLI

A local-first command-line tool to score resale suppliers (eBay, Amazon, wholesale, liquidation) on **price**, **speed (lead time)**, and **quality**. Data lives in a local JSON file. Export results to CSV. No API keys, no accounts, no cloud.

Built and maintained by **Asdale Dynamics, LLC** (Indiana, formed October 2026) — beginner-friendly AI education, practical tools, and small-business templates. Learn more at dylanasdale.github.io.

## What it does

- Add suppliers with unit price, quoted lead time (days), and quality rating (1-5)
- Score every supplier 0-100 using weighted criteria (default: price 40%, speed 35%, quality 25%)
- Track actual lead times per supplier over time (quoted vs actual)
- Rank suppliers by overall score
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

## Usage

Add a supplier:

```bash
supplier-scorecard add --name "Vintage Wholesale Co" --price 12.50 --lead-time 5 --quality 4 --notes "Books and media"
```

List and score suppliers:

```bash
supplier-scorecard list
```

Record an actual lead time (quoted defaults to the supplier's quoted lead time):

```bash
supplier-scorecard record --id a1b2c3d4 --actual 7 --reference PO-1001
```

Export to CSV:

```bash
supplier-scorecard export --output scorecard.csv
```

Use a different storage file:

```bash
supplier-scorecard --storage my_suppliers.json list
```

## Scoring

Each criterion is normalized 0-100 against the suppliers currently in your file:

- **Price**: lower is better (cheapest = 100)
- **Speed**: lower quoted lead time is better (fastest = 100)
- **Quality**: higher is better (5 = 100, 1 = 0)

Overall score = `0.40 × price + 0.35 × speed + 0.25 × quality`. Weights can be adjusted in `supplier_scorecard/scoring.py`.

## Tests

```bash
python3 -m unittest discover -s tests
```

## License

MIT. Copyright (c) 2026 Asdale Dynamics, LLC. See LICENSE.

## About

Asdale Dynamics, LLC is a registered Indiana LLC founded by Dylan Asdale, a registered nurse turned AI author and founder. His book *The Massive AI Manual* and hub site dylanasdale.github.io explain AI "like a friend would": plain English, step by step, never condescending. This tool is part of the LLC's small-business and author tooling line.
