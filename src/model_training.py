from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def prepare_data_for_training(features, audio_data):
    """Prepares data for training by associating features with metadata labels.

    Args:
        features (dict): Extracted features for each file.
        audio_data (dict): Audio data with corresponding metadata.

    Returns:
        X, y: Features matrix and label array for training.
    """
    X = []
    y = []
    for filename in features.keys():
        X.append(list(features[filename].values()))
        y.append(audio_data[filename][1]["effects"])  # Assume effects metadata is a list of actions
    return np.array(X), y

def train_action_prediction_model(X, y):
    """Trains a model to predict actions based on features.

    Args:
        X (array): Feature matrix.
        y (array): Label array.

    Returns:
        model: Trained classifier model.
    """
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)
    return model

def train_model(feature_data, labels):
    """Trains a model on multiple audio tracks.

    Args:
        feature_data (dict): Dictionary of features where keys are filenames.
        labels (dict): Dictionary of labels corresponding to the features.

    Returns:
        model: Trained machine learning model.
    """
    all_features = []
    all_labels = []
    
    for filename in feature_data.keys():
        features = feature_data[filename]
        all_features.extend(features.T)  # Transpose to get feature vectors
        all_labels.extend([labels[filename]] * features.shape[1])

    X_train, X_test, y_train, y_test = train_test_split(np.array(all_features), np.array(all_labels), test_size=0.2)
    
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model Accuracy: {score:.2f}")
    
    return model
