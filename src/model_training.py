"""
Model training utilities for AI-based audio processing.

This module provides functions to build, train, and save machine learning models.

Author: Esgr0bar
"""

from tensorflow.keras import layers, models

def build_model(input_shape):
    """
    Build a Convolutional Neural Network (CNN) model.

    Args:
        input_shape (tuple): Shape of the input data (height, width, channels).

    Returns:
        keras.Model: Compiled CNN model.
    """
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(1)  # Assuming regression output; modify for classification
    ])

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

def train_model(model, X_train, y_train, epochs=10, validation_split=0.2):
    """
    Train the CNN model on the provided data.

    Args:
        model (keras.Model): Compiled model.
        X_train (numpy.ndarray): Training data.
        y_train (numpy.ndarray): Target values.
        epochs (int): Number of epochs to train.
        validation_split (float): Fraction of data to use for validation.

    Returns:
        keras.callbacks.History: Training history.
    """
    history = model.fit(X_train, y_train, epochs=epochs, validation_split=validation_split)
    return history

def save_model(model, file_path):
    """
    Save the trained model to a file.

    Args:
        model (keras.Model): Trained model.
        file_path (str): Path to save the model.

    Returns:
        None
    """
    model.save(file_path)

