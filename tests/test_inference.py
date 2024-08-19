# test/test_inference.py
import unittest
from inference import load_model, predict_actions, run_inference

class TestInference(unittest.TestCase):

    def setUp(self):
        """Set up test dependencies and variables."""
        self.model_path = "path/to/saved/model.pkl"
        self.audio_data = {
            "sample1.wav": np.random.rand(44100),
            "sample2.wav": np.random.rand(44100)
        }
    
    def test_load_model(self):
        """Test model loading functionality."""
        model = load_model(self.model_path)
        self.assertIsNotNone(model)
    
    def test_predict_actions(self):
        """Test action prediction functionality."""
        model = load_model(self.model_path)
        suggested_actions, suggested_cuts = predict_actions(model, self.audio_data)
        self.assertIsInstance(suggested_actions, dict)
        self.assertIsInstance(suggested_cuts, dict)

    def test_run_inference(self):
        """Test the full inference process."""
        results = run_inference(self.model_path, self.audio_data)
        self.assertIsInstance(results, tuple)

if __name__ == "__main__":
    unittest.main()
