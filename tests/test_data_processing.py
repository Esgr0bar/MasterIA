# test_data_processing.py

import unittest
import os
import numpy as np
from src.data_processing import load_audio, split_tracks

class TestDataProcessing(unittest.TestCase):

    def test_load_audio(self):
        # Test that the function loads audio correctly
        audio_path = '../data/raw/tracks/song1/vocals.wav'
        y, sr = load_audio(audio_path)
        self.assertIsInstance(y, np.ndarray)
        self.assertIsInstance(sr, int)

    def test_split_tracks(self):
        # Test that tracks are split into the correct number of segments
        audio_path = '../data/raw/tracks/song1/vocals.wav'
        segments = split_tracks(audio_path, segment_length=5)
        self.assertEqual(len(segments), 12)  # Assuming a 60-second track
        self.assertEqual(segments[0].shape[0], 5 * 44100)  # 5 seconds * 44100 sample rate

if __name__ == '__main__':
    unittest.main()

