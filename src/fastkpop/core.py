"""Small public helpers for working with fastkpop records."""

from collections.abc import Iterable, Mapping
import pandas as pd

from fastkpop.schema import ARTIST_COLUMNS


def artists_frame(records: Iterable[Mapping[str, object]]) -> pd.DataFrame:
    """Return artist records as a consistently ordered Pandas DataFrame."""
    frame = pd.DataFrame(list(records))
    for column in ARTIST_COLUMNS:
        if column not in frame.columns:
            frame[column] = pd.NA
    return frame[ARTIST_COLUMNS]
