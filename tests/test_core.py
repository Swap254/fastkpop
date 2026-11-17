from fastkpop.core import artists_frame


def test_artists_frame_has_stable_columns():
    frame = artists_frame([{"source": "test", "name": "Example"}])
    assert "source" in frame.columns
    assert "name" in frame.columns
    assert frame.loc[0, "name"] == "Example"
    assert len(frame.columns) == 10
