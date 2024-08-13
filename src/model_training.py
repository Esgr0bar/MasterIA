from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
import numpy as np

# Function to create a simple CNN model
def create_cnn(input_shape):
    model = Sequential()
    model.add(Conv1D(64, kernel_size=3, activation='relu', input_shape=input_shape))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(128, kernel_size=3, activation='relu'))
    model.add(MaxPooling1D(pool_size=2))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))  # Assuming binary classification
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

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
    """Trains an ensemble model on multiple audio tracks with CNN and voting classifier.

    Args:
        feature_data (dict): Dictionary of features where keys are filenames.
        labels (dict): Dictionary of labels corresponding to the features.

    Returns:
        model: Trained ensemble model.
    """
    all_features = []
    all_labels = []
    
    for filename in feature_data.keys():
        features = feature_data[filename]
        all_features.extend(features.T)  # Transpose to get feature vectors
        all_labels.extend([labels[filename]] * features.shape[1])

    X_train, X_test, y_train, y_test = train_test_split(np.array(all_features), np.array(all_labels), test_size=0.2)

    # Reshape the data for CNN input (if using 1D audio data, not spectrograms)
    X_train_cnn = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
    X_test_cnn = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

    # Create the CNN model
    cnn_model = KerasClassifier(build_fn=create_cnn, input_shape=(X_train_cnn.shape[1], 1), epochs=10, batch_size=32, verbose=0)

    # Create other models
    rf_model = RandomForestClassifier(n_estimators=100)
    svm_model = SVC(probability=True)

    # Combine models in a voting classifier
    ensemble_model = VotingClassifier(estimators=[
        ('cnn', cnn_model),
        ('rf', rf_model),
        ('svm', svm_model)
    ], voting='soft')  # 'soft' voting uses predicted probabilities

    # Hyperparameter tuning using GridSearchCV
    param_grid = {
        'rf__n_estimators': [100, 200],
        'svm__C': [0.1, 1, 10],
    }

    grid = GridSearchCV(ensemble_model, param_grid, cv=3, n_jobs=-1)
    grid.fit(X_train_cnn, y_train)

    best_model = grid.best_estimator_

    # Evaluate the best model on the test set
    y_pred = best_model.predict(X_test_cnn)
    print(classification_report(y_test, y_pred))
    
    return best_model
