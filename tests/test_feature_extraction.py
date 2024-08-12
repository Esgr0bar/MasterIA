import os
import pytest
from src.data_processing import load_audio_files
from src.feature_extraction import extract_mfcc, extract_spectrogram

def test_extract_mfcc():
    directory = "test_data/raw/tracks"
    audio_data = load_audio_files(directory)
    mfcc_features = extract_mfcc(audio_data)
    assert len(mfcc_features) > 0
    for filename, mfcc in mfcc_features.items():
        assert mfcc is not None
        assert mfcc.shape[0] == 13  # Default number of MFCCs is 13

def test_extract_spectrogram():
    directory = "test_data/raw/tracks"
    audio_data = load_audio_files(directory)
    spectrograms = extract_spectrogram(audio_data)
    assert len(spectrograms) > 0
    for filename, S in spectrograms.items():
        assert S is not None
        assert S.shape[0] > 0
        assert S.shape[1] > 0
