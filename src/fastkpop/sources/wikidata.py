"""Wikidata SPARQL adapter.

The query deliberately retrieves South Korean musical-group candidates rather
than claiming every returned entity is K-pop.
"""

from __future__ import annotations

import time
import httpx

ENDPOINT = "https://query.wikidata.org/sparql"
QUERY = """
SELECT ?item ?itemLabel ?itemDescription ?inception ?dissolved
WHERE {
  ?item wdt:P31/wdt:P279* wd:Q215380;
        wdt:P17 wd:Q884.
  OPTIONAL { ?item wdt:P571 ?inception. }
  OPTIONAL { ?item wdt:P576 ?dissolved. }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en,ko". }
}
ORDER BY ?itemLabel
LIMIT %d
"""


def fetch_artists(limit: int = 100, timeout: float = 45.0) -> list[dict[str, object]]:
    """Fetch South Korean musical-group candidates from Wikidata."""
    if not 1 <= limit <= 10000:
        raise ValueError("limit must be between 1 and 10000")

    headers = {
        "Accept": "application/sparql-results+json",
        "User-Agent": "fastkpop/0.1.0 (https://github.com/fastkpop/fastkpop)",
    }
    with httpx.Client(timeout=timeout, headers=headers) as client:
        response = client.get(ENDPOINT, params={"query": QUERY % limit})
        response.raise_for_status()
        bindings = response.json()["results"]["bindings"]

    records = []
    for row in bindings:
        uri = row.get("item", {}).get("value", "")
        records.append({
            "source": "wikidata",
            "source_id": uri.rsplit("/", 1)[-1],
            "name": row.get("itemLabel", {}).get("value"),
            "name_native": None,
            "artist_type": "musical_group_candidate",
            "country": "South Korea",
            "formed": row.get("inception", {}).get("value"),
            "disbanded": row.get("dissolved", {}).get("value"),
            "description": row.get("itemDescription", {}).get("value"),
            "source_url": uri,
        })
    return records
