import pytest
from src.model_training import train_model
from src.feature_extraction import extract_mfcc
from src.data_processing import load_audio_files

def test_train_model():
    directory = "test_data/raw/tracks"
    audio_data = load_audio_files(directory)
    features = extract_mfcc(audio_data)
    labels = {filename: 1 for filename in features.keys()}  # Dummy labels for testing
    model = train_model(features, labels)
    assert model is not None
    assert hasattr(model, "predict")
