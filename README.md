# Bayanatak

Saudi test data, without using real Saudi people as test data.

If you are building for Saudi users and your demo still says `John Doe`, your test data is lying to you.

Arabic names break layouts differently. Saudi phone fields need different validation. Cities,
neighborhoods, addresses, VAT, payment flows, and Arabic form labels all expose bugs that generic
fake data will never catch.

Bayanatak is a tiny local CLI that generates Saudi-flavored fake data for product development,
frontend QA, backend seeds, demos, and test fixtures.

No API.
No scraping.
No database.
No LLM.
No real personal data.

Just deterministic fake records that look close enough to the local product reality to break the
things you actually need to fix.

## Install

For now, install from source:

```bash
python3 -m pip install -e .
```

Later, if the package earns it:

```bash
pip install bayanatak
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

- Fake Arabic names for testing.
- Safe emails under `example.test`.
- Saudi cities and neighborhoods.
- Local-looking addresses.
- Checkout records with SAR totals, VAT, shipping, and payment method.
- Form payloads for signup, checkout, and waitlist screens.
- A clear `is_fake` flag on every record.

## The Safety Bit

By default, phone numbers are intentionally not dialable:

```text
05X0000001
```

That is useful for UI, screenshots, demos, and documentation.

If you need digits-only values for local validators, opt in:

```bash
bayanatak user --phone-mode digits
```

Use digits mode for local testing only. Do not call, text, upload, or treat generated values as real
customer data.

## Output Formats

```bash
bayanatak user --format table
bayanatak user --format json
bayanatak user --format csv
```

The same generator can feed:

- Frontend mock screens.
- Backend seed files.
- QA CSV files.
- Snapshot tests.
- Product demos.

## How It Works

Bayanatak ships with small local datasets:

- Arabic test names.
- Fake test surnames.
- Saudi cities.
- Neighborhoods.
- Streets.
- Products.
- Payment methods.

The CLI combines those datasets with Python's local pseudo-random generator.

Add `--seed`, and the output becomes stable:

```bash
bayanatak checkout --city jeddah --count 10 --seed 42
```

Same command, same records. That makes it useful for tests and screenshots where random drift is a
waste of time.

## Examples

Generate users:

```bash
bayanatak user --count 3 --city riyadh
```

Generate checkout data:

```bash
bayanatak checkout --count 5 --city jeddah --format json
```

Generate signup form payloads:

```bash
bayanatak form --type signup --count 10 --format csv
```

## Development

```bash
python3 -m unittest discover -s tests
python3 -m compileall src tests
```

## Scope

This is not a legal identity generator, not a production data source, and not a replacement for real
user research.

It is a development utility for teams building Saudi-facing products and trying not to ship broken
Arabic forms.

## Roadmap

- More cities and neighborhoods.
- Arabic date and time scenarios.
- Saudi business records.
- UI fixture bundles for common product screens.
- A tiny web preview if the CLI proves useful.

## Contributing

PRs are welcome if they make the data more useful, safer, or more realistic without crossing into
real personal data.

Regards,
The CTO.
