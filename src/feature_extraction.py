"""
Feature extraction utilities for audio processing.

This module provides functions to extract features such as MFCCs and spectrograms.

Author: Esgr0bar
"""

import librosa
import numpy as np

def extract_mfcc(y, sr, n_mfcc=13):
    """
    Extract MFCC features from an audio signal.

    Args:
        y (numpy.ndarray): Audio time series.
        sr (int): Sample rate of the audio.
        n_mfcc (int): Number of MFCCs to return.

    Returns:
        numpy.ndarray: MFCC feature matrix.
    """
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=n_mfcc)
    return mfccs

def extract_spectrogram(y, sr, n_fft=2048, hop_length=512):
    """
    Extract spectrogram from an audio signal.

    Args:
        y (numpy.ndarray): Audio time series.
        sr (int): Sample rate of the audio.
        n_fft (int): Number of samples per FFT.
        hop_length (int): Number of samples between successive frames.

    Returns:
        numpy.ndarray: Spectrogram matrix.
    """
    S = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    return S

