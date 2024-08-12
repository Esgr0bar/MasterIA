import os
import pytest
from src.data_processing import load_audio_files, split_tracks

def test_load_audio_files():
    directory = "test_data/raw/tracks"
    audio_data = load_audio_files(directory)
    assert len(audio_data) > 0
    for filename, audio in audio_data.items():
        assert audio is not None
        assert len(audio) > 0

def test_split_tracks():
    directory = "test_data/raw/tracks"
    audio_data = load_audio_files(directory)
    segmented_data = split_tracks(audio_data, segment_length=5)
    assert len(segmented_data) > 0
    for filename, segments in segmented_data.items():
        assert len(segments) > 0
        for segment in segments:
            assert len(segment) > 0
