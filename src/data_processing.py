import os
import numpy as np
import librosa
import json

def load_audio_files_with_metadata(directory):
    """Loads multiple audio files along with their metadata.

    Args:
        directory (str): Path to the directory containing audio files and metadata.

    Returns:
        dict: A dictionary where keys are filenames and values are tuples (audio data, metadata).
    """
    audio_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            file_path = os.path.join(directory, filename)
            audio, sr = librosa.load(file_path, sr=None)
            metadata_file = filename.replace('.wav', '.json')
            metadata_path = os.path.join(directory, metadata_file)
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                audio_data[filename] = (audio, metadata)
    return audio_data

def load_audio_files(directory):
    """Loads multiple audio files from a directory.

    Args:
        directory (str): Path to the directory containing audio files.

    Returns:
        dict: A dictionary where keys are filenames and values are numpy arrays of audio data.
    """
    audio_data = {}
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            file_path = os.path.join(directory, filename)
            audio, sr = librosa.load(file_path, sr=None)
            audio_data[filename] = audio
    return audio_data

def split_tracks(audio_data, segment_length=5):
    """Splits multiple audio tracks into segments.

    Args:
        audio_data (dict): Dictionary of audio data where keys are filenames.
        segment_length (int): Length of each segment in seconds.

    Returns:
        dict: A dictionary with segmented audio data.
    """
    segmented_data = {}
    for filename, audio in audio_data.items():
        segments = []
        sr = librosa.get_samplerate(filename)
        num_samples = sr * segment_length
        for start in range(0, len(audio), num_samples):
            segment = audio[start:start + num_samples]
            segments.append(segment)
        segmented_data[filename] = segments
    return segmented_data
