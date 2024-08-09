"""
Data processing utilities for audio files.

This module provides functions to load and split audio files into segments.

Author: Esgr0bar
"""

import librosa

def load_audio(file_path, sr=44100):
    """
    Load an audio file.

    Args:
        file_path (str): Path to the audio file.
        sr (int): Sample rate for loading audio.

    Returns:
        tuple: Tuple containing the audio time series (numpy.ndarray) and sample rate (int).
    """
    y, sr = librosa.load(file_path, sr=sr)
    return y, sr

def split_tracks(file_path, segment_length=5):
    """
    Split an audio track into smaller segments.

    Args:
        file_path (str): Path to the audio file.
        segment_length (int): Length of each segment in seconds.

    Returns:
        list: A list of audio segments (numpy.ndarray).
    """
    y, sr = load_audio(file_path)
    segments = [y[i:i + sr * segment_length] for i in range(0, len(y), sr * segment_length)]
    return segments

