# Bayanatak

Saudi-flavored fake test data for local product development.

Bayanatak is a tiny local CLI that generates safe fake records for Saudi-facing products:
Arabic names, Saudi cities and neighborhoods, addresses, checkout payloads, SAR totals, VAT,
payment methods, and form fixtures.

No API. No scraping. No database. No LLM. No real personal data.

## Demo

![Bayanatak demo](docs/assets/mara-bayanatak-demo.gif)

## Install

```bash
python3 -m pip install -e .
```

## Quick Start

```bash
bayanatak user --count 5
bayanatak checkout --city riyadh --seed 7
bayanatak form --type signup --format json
bayanatak form --type checkout --format csv --output checkout.csv
```

Run without installing:

```bash
PYTHONPATH=src python3 -m bayanatak.cli user --count 5
```

## What It Generates

- Fake Arabic names and safe `example.test` emails.
- Saudi cities, neighborhoods, and local-looking addresses.
- Checkout records with SAR totals, VAT, shipping, and payment methods.
- Signup, checkout, and waitlist form payloads.
- Stable records when you pass `--seed`.
- An `is_fake` flag on every record.

## Safety

Phone numbers are intentionally not dialable by default:

```text
05X0000001
```

Use digits-only values only when testing local validators:

```bash
bayanatak user --phone-mode digits
```

Do not call, text, upload, or treat generated values as real customer data.

## Output

```bash
bayanatak user --format table
bayanatak user --format json
bayanatak user --format csv
bayanatak checkout --city jeddah --count 10 --seed 42
```

Use the output for mock screens, backend seeds, QA CSV files, snapshot tests, and product demos.

## Development

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
python3 -m compileall src tests
```

## Scope

Bayanatak is not a legal identity generator, production data source, or replacement for real user
research. It is a development utility for teams building Saudi-facing products without using real
Saudi people as test data.

## About

Maintained by [mara](https://github.com/mara-org). Created by [@gqnxx](https://github.com/gqnxx).
