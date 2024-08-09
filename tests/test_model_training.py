
# test_model_training.py

import unittest
import os
import numpy as np
from src.model_training import build_model, train_model, save_model

class TestModelTraining(unittest.TestCase):

    def test_build_model(self):
        # Test model building
        input_shape = (64, 64, 1)  # Example input shape (e.g., spectrogram with 64x64 bins)
        model = build_model(input_shape)
        self.assertEqual(len(model.layers), 6)  # Example model with 6 layers

    def test_train_model(self):
        # Test model training
        X_train = np.random.randn(100, 64, 64, 1)  # Example training data
        y_train = np.random.randn(100, 64)  # Example labels
        model = build_model(X_train.shape[1:])
        history = train_model(model, X_train, y_train, epochs=2)
        self.assertIn('loss', history.history)
        self.assertIn('val_loss', history.history)

    def test_save_model(self):
        # Test model saving
        model = build_model((64, 64, 1))
        save_model(model, '../data/processed/models/test_model.h5')
        self.assertTrue(os.path.exists('../data/processed/models/test_model.h5'))

if __name__ == '__main__':
    unittest.main()
