"""MusicBrainz artist-search adapter."""

from __future__ import annotations

import os
import time
import httpx

API_ROOT = "https://musicbrainz.org/ws/2"


def fetch_artists(
    limit: int = 100,
    timeout: float = 30.0,
    pause_seconds: float = 1.1,
) -> list[dict[str, object]]:
    """Search MusicBrainz for South Korean artists whose type is Group.

    MusicBrainz requests should be throttled. This implementation makes one
    request (up to the API's page limit) and uses a descriptive User-Agent.
    """
    if not 1 <= limit <= 100:
        raise ValueError("limit must be between 1 and 100 for this first adapter")

    user_agent = os.getenv(
        "FASTKPOP_USER_AGENT",
        "fastkpop/0.1.0 (https://github.com/fastkpop/fastkpop)",
    )
    headers = {"User-Agent": user_agent, "Accept": "application/json"}
    params = {"query": "country:KR AND type:Group", "fmt": "json", "limit": limit}

    with httpx.Client(timeout=timeout, headers=headers) as client:
        response = client.get(f"{API_ROOT}/artist", params=params)
        response.raise_for_status()
        payload = response.json()

    records = []
    for artist in payload.get("artists", []):
        area = artist.get("area") or {}
        life_span = artist.get("life-span") or {}
        mbid = artist.get("id")
        records.append({
            "source": "musicbrainz",
            "source_id": mbid,
            "name": artist.get("name"),
            "name_native": artist.get("sort-name"),
            "artist_type": artist.get("type") or "Group",
            "country": area.get("name") or artist.get("country") or "KR",
            "formed": life_span.get("begin"),
            "disbanded": life_span.get("end") if life_span.get("ended") else None,
            "description": None,
            "source_url": f"https://musicbrainz.org/artist/{mbid}" if mbid else None,
        })
    if pause_seconds > 0:
        time.sleep(pause_seconds)
    return records
