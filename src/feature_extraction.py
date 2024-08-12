import numpy as np
import librosa

def extract_mfcc(audio_data, n_mfcc=13):
    """Extract MFCC features from multiple audio tracks.

    Args:
        audio_data (dict): Dictionary of audio data where keys are filenames.
        n_mfcc (int): Number of MFCCs to return.

    Returns:
        dict: A dictionary with MFCC features.
    """
    mfcc_features = {}
    for filename, audio in audio_data.items():
        mfccs = librosa.feature.mfcc(y=audio, sr=librosa.get_samplerate(filename), n_mfcc=n_mfcc)
        mfcc_features[filename] = mfccs
    return mfcc_features

def extract_spectrogram(audio_data):
    """Extract spectrogram features from multiple audio tracks.

    Args:
        audio_data (dict): Dictionary of audio data where keys are filenames.

    Returns:
        dict: A dictionary with spectrogram features.
    """
    spectrograms = {}
    for filename, audio in audio_data.items():
        D = np.abs(librosa.stft(audio))**2
        S = librosa.feature.melspectrogram(S=D, sr=librosa.get_samplerate(filename))
        spectrograms[filename] = S
    return spectrograms
