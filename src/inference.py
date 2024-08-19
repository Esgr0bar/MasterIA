# inference.py
import numpy as np
import joblib
from src.feature_extraction import extract_basic_features
from src.action_suggestion import suggest_actions, suggest_cuts

def load_model(model_path):
    """Load the pre-trained machine learning model.

    Args:
        model_path (str): Path to the pre-trained model file.

    Returns:
        model: The loaded model object.
    """
    return joblib.load(model_path)

def predict_actions(model, audio_data):
    """Predicts the actions and cuts for the given audio data.

    Args:
        model: The pre-trained machine learning model.
        audio_data (dict): Dictionary where keys are filenames and values are audio data.

    Returns:
        dict: Suggested actions and cuts for each audio file.
    """
    features = extract_basic_features(audio_data)
    suggested_actions = suggest_actions(model, features)
    suggested_cuts = suggest_cuts(model, features)
    
    return suggested_actions, suggested_cuts

def run_inference(model_path, audio_data):
    """Run the inference process on the provided audio data.

    Args:
        model_path (str): Path to the pre-trained model file.
        audio_data (dict): Dictionary where keys are filenames and values are audio data.

    Returns:
        dict: Suggested actions and cuts for each audio file.
    """
    model = load_model(model_path)
    return predict_actions(model, audio_data)

