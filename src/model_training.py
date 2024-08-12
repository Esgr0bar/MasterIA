from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

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
