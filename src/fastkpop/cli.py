"""Command-line interface for initial source discovery."""

from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from fastkpop.core import artists_frame
from fastkpop.sources import musicbrainz, wikidata


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch public K-pop artist candidates.")
    parser.add_argument("--source", choices=["wikidata", "musicbrainz"], required=True)
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output", default="data/raw/artists.csv")
    args = parser.parse_args()

    if args.source == "wikidata":
        records = wikidata.fetch_artists(args.limit)
    else:
        records = musicbrainz.fetch_artists(args.limit)

    frame = artists_frame(records)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(output, index=False)
    print(f"Saved {len(frame)} candidate records to {output}")


if __name__ == "__main__":
    main()
