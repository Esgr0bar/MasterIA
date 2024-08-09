# test_feature_extraction.py

import unittest
import numpy as np
from src.feature_extraction import extract_mfcc, extract_spectrogram

class TestFeatureExtraction(unittest.TestCase):

    def test_extract_mfcc(self):
        # Test MFCC extraction
        y = np.random.randn(44100 * 5)  # Simulated 5-second audio
        sr = 44100
        mfccs = extract_mfcc(y, sr)
        self.assertEqual(mfccs.shape, (13, 431))  # Example shape (n_mfcc, frames)

    def test_extract_spectrogram(self):
        # Test spectrogram extraction
        y = np.random.randn(44100 * 5)  # Simulated 5-second audio
        sr = 44100
        spectrogram = extract_spectrogram(y, sr)
        self.assertEqual(spectrogram.shape[0], 1025)  # 1025 frequency bins for default FFT

if __name__ == '__main__':
    unittest.main()

