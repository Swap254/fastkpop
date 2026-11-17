# fastkpop

**An open-source Python toolkit for K-pop data research and analytics.**

fastkpop aims to make structured K-pop industry data easier to discover, validate,
analyze, and reuse. The long-term scope is historical coverage from 1992 to the
present, including groups, soloists, bands, members, agencies, releases, charts,
and industry metrics.

> **Status:** early development. The first release is a source-backed artist
> discovery prototype, not a complete or authoritative K-pop database.

## Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -e ".[dev]"
fastkpop-fetch --source wikidata --limit 100 --output data/raw/wikidata_artists.csv
```

MusicBrainz search:

```bash
fastkpop-fetch --source musicbrainz --limit 100 --output data/raw/musicbrainz_artists.csv
```

The MusicBrainz API requires a descriptive User-Agent. Set one with:

```bash
# Windows PowerShell
$env:FASTKPOP_USER_AGENT="fastkpop/0.1.0 (your-contact@example.com)"
# macOS/Linux
export FASTKPOP_USER_AGENT="fastkpop/0.1.0 (your-contact@example.com)"
```

## What this version does

- Queries Wikidata for South Korean musical-group candidates.
- Searches MusicBrainz for Korean artists of type `Group`.
- Normalizes both sources into a shared, conservative column layout.
- Exports results to CSV for inspection and later entity resolution.

## Important data-quality note

These are **candidate records**, not a verified list of K-pop acts. "South Korean
musical group" is broader than K-pop, and public knowledge graphs can be
incomplete or inconsistent. Later versions will add explicit genre evidence,
source provenance, human review, canonical `fk_id` identifiers, and change
tracking. Do not interpret missing records as proof that an artist did not exist.

## Data sources and terms

- Wikidata structured data is generally available under CC0; check individual
  statements and source references.
- MusicBrainz data is available under its published database and API terms.
- This project does not bundle lyrics, album artwork, promotional photographs,
  or other copyrighted media.
- Respect API rate limits and each provider's current terms. Do not scrape sites
  that prohibit automated access.

## Project principles

1. Provenance before aggregation: every record should retain its source.
2. Facts and calculated metrics must be distinguishable.
3. Uncertain data should be marked, not silently guessed.
4. Neutrality: no fan-war scoring or unsupported claims.
5. Small, tested releases before ambitious feature expansion.

## Unofficial project

fastkpop is an independent, unofficial project. It is not affiliated with,
endorsed by, or sponsored by any K-pop agency, artist, chart provider, or
streaming platform.
