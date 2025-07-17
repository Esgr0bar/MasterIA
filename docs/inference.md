# Inference Guide

## 🎯 Overview

The inference system is the core of MasterIA's real-time audio processing capabilities. It takes trained machine learning models and applies them to new audio tracks to generate intelligent mixing suggestions, mastering recommendations, and creative enhancement ideas.

## 🔧 Core Functions

### `load_model(model_path)`
Loads a pre-trained machine learning model from the specified path.

**Parameters:**
- `model_path` (str): Path to the model file (usually `.pkl` format)

**Returns:**
- `model`: The loaded scikit-learn model object

**Example:**
```python
from src.inference import load_model

# Load a trained model
model = load_model("models/trained_model.pkl")
print(f"Model loaded successfully: {type(model)}")
```

**Error Handling:**
```python
import os
from src.inference import load_model

def safe_load_model(model_path):
    """Safely load model with error handling"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        model = load_model(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None
```

### `predict_actions(model, audio_data)`
Predicts mixing actions and creative cuts for given audio data using a pre-trained model.

**Parameters:**
- `model`: Pre-trained machine learning model
- `audio_data` (dict): Dictionary where keys are filenames and values are audio arrays

**Returns:**
- `tuple`: (suggested_actions, suggested_cuts)
  - `suggested_actions`: Dictionary of mixing suggestions per track
  - `suggested_cuts`: Dictionary of creative cut suggestions per track

**Example:**
```python
from src.inference import predict_actions
from src.data_processing import load_audio_files_with_metadata

# Load audio and model
audio_data, metadata = load_audio_files_with_metadata("data/test_tracks/")
model = load_model("models/trained_model.pkl")

# Get predictions
actions, cuts = predict_actions(model, audio_data)

# Display results
print("Suggested Actions:")
for track, action_list in actions.items():
    print(f"  {track}:")
    for action in action_list:
        print(f"    - {action}")
```

### `run_inference(model_path, audio_data)`
Complete inference pipeline that loads the model and generates predictions.

**Parameters:**
- `model_path` (str): Path to the pre-trained model file
- `audio_data` (dict): Dictionary where keys are filenames and values are audio arrays

**Returns:**
- `tuple`: (suggested_actions, suggested_cuts)

**Example:**
```python
from src.inference import run_inference

# Complete inference in one step
actions, cuts = run_inference("models/trained_model.pkl", audio_data)
```

## 🎵 Understanding AI Suggestions

### Action Suggestions Format
```python
{
  "track1.wav": [
    {
      "effect": "EQ",
      "target": "vocals",
      "level": 0.8,
      "frequency": "high",
      "confidence": 0.92
    },
    {
      "effect": "Compression",
      "target": "drums",
      "level": 0.6,
      "ratio": "4:1",
      "confidence": 0.87
    }
  ]
}
```

### Cut Suggestions Format
```python
{
  "track1.wav": [
    {
      "action": "Glitch",
      "location": "Chorus Start",
      "timestamp": "0:45",
      "duration": "0.2",
      "confidence": 0.75
    },
    {
      "action": "Stutter",
      "location": "Verse Mid",
      "timestamp": "1:23",
      "duration": "0.5",
      "confidence": 0.82
    }
  ]
}
```

## 🚀 Advanced Inference Techniques

### 1. Batch Processing
Process multiple files efficiently:

```python
def batch_inference(model_path, file_list, batch_size=10):
    """Process multiple files in batches"""
    model = load_model(model_path)
    results = {}
    
    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i+batch_size]
        
        # Load batch of audio files
        batch_audio = {}
        for filename in batch:
            audio, sr = librosa.load(filename, sr=22050)
            batch_audio[filename] = audio
        
        # Process batch
        batch_actions, batch_cuts = predict_actions(model, batch_audio)
        
        # Store results
        results.update({
            'actions': batch_actions,
            'cuts': batch_cuts
        })
        
        # Clear memory
        del batch_audio
    
    return results
```

### 2. Real-time Processing
For live audio processing:

```python
import threading
import queue

class RealTimeInference:
    """Real-time inference processor"""
    
    def __init__(self, model_path):
        self.model = load_model(model_path)
        self.audio_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.processing_thread = None
        self.running = False
    
    def start(self):
        """Start real-time processing"""
        self.running = True
        self.processing_thread = threading.Thread(target=self._process_loop)
        self.processing_thread.start()
    
    def stop(self):
        """Stop real-time processing"""
        self.running = False
        if self.processing_thread:
            self.processing_thread.join()
    
    def add_audio(self, filename, audio_data):
        """Add audio for processing"""
        self.audio_queue.put((filename, audio_data))
    
    def get_results(self):
        """Get processing results"""
        results = []
        while not self.result_queue.empty():
            results.append(self.result_queue.get())
        return results
    
    def _process_loop(self):
        """Processing loop for real-time inference"""
        while self.running:
            try:
                filename, audio_data = self.audio_queue.get(timeout=1)
                actions, cuts = predict_actions(self.model, {filename: audio_data})
                self.result_queue.put({
                    'filename': filename,
                    'actions': actions,
                    'cuts': cuts
                })
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Processing error: {e}")
```

### 3. Confidence-based Filtering
Filter suggestions based on confidence scores:

```python
def filter_by_confidence(suggestions, min_confidence=0.7):
    """Filter suggestions by confidence threshold"""
    filtered = {}
    
    for track, actions in suggestions.items():
        filtered[track] = []
        for action in actions:
            if action.get('confidence', 0) >= min_confidence:
                filtered[track].append(action)
    
    return filtered

# Usage
actions, cuts = run_inference("models/trained_model.pkl", audio_data)
high_confidence_actions = filter_by_confidence(actions, min_confidence=0.8)
```

### 4. Custom Post-processing
Apply custom logic to suggestions:

```python
def post_process_suggestions(actions, user_preferences):
    """Apply user preferences to suggestions"""
    processed = {}
    
    for track, action_list in actions.items():
        processed[track] = []
        
        for action in action_list:
            # Apply user preferences
            if action['effect'] in user_preferences['allowed_effects']:
                # Adjust level based on user preference
                preference_factor = user_preferences.get('effect_intensity', 1.0)
                action['level'] *= preference_factor
                processed[track].append(action)
    
    return processed

# Example user preferences
user_prefs = {
    'allowed_effects': ['EQ', 'Compression', 'Reverb'],
    'effect_intensity': 0.8,
    'max_suggestions': 5
}

actions, cuts = run_inference("models/trained_model.pkl", audio_data)
customized_actions = post_process_suggestions(actions, user_prefs)
```

## 🎛️ Model-Specific Inference

### Genre-Specific Models
Use different models for different genres:

```python
def genre_specific_inference(audio_data, genre):
    """Run inference with genre-specific model"""
    model_paths = {
        'hip-hop': 'models/hip_hop_model.pkl',
        'electronic': 'models/electronic_model.pkl',
        'rock': 'models/rock_model.pkl',
        'default': 'models/general_model.pkl'
    }
    
    model_path = model_paths.get(genre, model_paths['default'])
    return run_inference(model_path, audio_data)

# Usage
actions, cuts = genre_specific_inference(audio_data, 'hip-hop')
```

### Ensemble Model Inference
Combine predictions from multiple models:

```python
def ensemble_inference(audio_data, model_paths, weights=None):
    """Combine predictions from multiple models"""
    if weights is None:
        weights = [1.0] * len(model_paths)
    
    all_actions = []
    all_cuts = []
    
    for model_path, weight in zip(model_paths, weights):
        actions, cuts = run_inference(model_path, audio_data)
        all_actions.append((actions, weight))
        all_cuts.append((cuts, weight))
    
    # Combine results with weighted averaging
    final_actions = combine_weighted_actions(all_actions)
    final_cuts = combine_weighted_cuts(all_cuts)
    
    return final_actions, final_cuts

def combine_weighted_actions(weighted_actions):
    """Combine multiple action predictions with weights"""
    combined = {}
    
    for track in weighted_actions[0][0].keys():
        combined[track] = []
        action_scores = {}
        
        # Collect all actions with their weights
        for actions, weight in weighted_actions:
            for action in actions[track]:
                action_key = f"{action['effect']}_{action['target']}"
                if action_key not in action_scores:
                    action_scores[action_key] = []
                action_scores[action_key].append((action, weight))
        
        # Average the actions
        for action_key, action_weight_pairs in action_scores.items():
            if len(action_weight_pairs) >= 2:  # At least 2 models agree
                combined_action = average_actions(action_weight_pairs)
                combined[track].append(combined_action)
    
    return combined
```

## 📊 Performance Monitoring

### Inference Performance Metrics
Track inference performance:

```python
import time
import psutil

class InferenceProfiler:
    """Profile inference performance"""
    
    def __init__(self):
        self.metrics = {
            'inference_times': [],
            'memory_usage': [],
            'cpu_usage': []
        }
    
    def profile_inference(self, model_path, audio_data):
        """Profile single inference run"""
        # Monitor system resources
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        start_time = time.time()
        cpu_before = psutil.cpu_percent(interval=None)
        
        # Run inference
        actions, cuts = run_inference(model_path, audio_data)
        
        # Calculate metrics
        inference_time = time.time() - start_time
        cpu_after = psutil.cpu_percent(interval=None)
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Store metrics
        self.metrics['inference_times'].append(inference_time)
        self.metrics['memory_usage'].append(final_memory - initial_memory)
        self.metrics['cpu_usage'].append(cpu_after - cpu_before)
        
        return actions, cuts
    
    def get_stats(self):
        """Get performance statistics"""
        stats = {}
        for metric, values in self.metrics.items():
            if values:
                stats[metric] = {
                    'mean': np.mean(values),
                    'std': np.std(values),
                    'min': np.min(values),
                    'max': np.max(values)
                }
        return stats
```

## 🛠️ Troubleshooting Inference Issues

### Common Problems and Solutions

#### 1. Model Loading Errors
```python
def diagnose_model_loading(model_path):
    """Diagnose model loading issues"""
    import os
    import joblib
    
    if not os.path.exists(model_path):
        print(f"❌ Model file not found: {model_path}")
        return False
    
    try:
        model = joblib.load(model_path)
        print(f"✅ Model loaded successfully: {type(model)}")
        
        # Check model attributes
        if hasattr(model, 'n_features_in_'):
            print(f"Expected features: {model.n_features_in_}")
        
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False
```

#### 2. Feature Dimension Mismatch
```python
def check_feature_compatibility(model, audio_data):
    """Check if audio features match model expectations"""
    from src.feature_extraction import extract_basic_features
    
    features = extract_basic_features(audio_data)
    
    # Get feature dimensions
    sample_features = next(iter(features.values()))
    n_features = len(sample_features)
    
    # Check model expectations
    if hasattr(model, 'n_features_in_'):
        expected_features = model.n_features_in_
        if n_features != expected_features:
            print(f"❌ Feature mismatch: got {n_features}, expected {expected_features}")
            return False
    
    print(f"✅ Feature dimensions compatible: {n_features}")
    return True
```

#### 3. Memory Issues During Inference
```python
def memory_efficient_inference(model_path, audio_data, max_memory_mb=1000):
    """Run inference with memory monitoring"""
    import gc
    import psutil
    
    process = psutil.Process()
    
    # Check initial memory
    initial_memory = process.memory_info().rss / 1024 / 1024
    
    if initial_memory > max_memory_mb:
        print(f"⚠️ High initial memory usage: {initial_memory:.2f} MB")
    
    # Process in smaller batches if needed
    if len(audio_data) > 5:  # Process in batches
        results_actions = {}
        results_cuts = {}
        
        for i, (filename, audio) in enumerate(audio_data.items()):
            single_audio = {filename: audio}
            actions, cuts = run_inference(model_path, single_audio)
            
            results_actions.update(actions)
            results_cuts.update(cuts)
            
            # Clear memory
            del single_audio, actions, cuts
            gc.collect()
            
            # Check memory usage
            current_memory = process.memory_info().rss / 1024 / 1024
            if current_memory > max_memory_mb:
                print(f"⚠️ Memory usage high: {current_memory:.2f} MB")
        
        return results_actions, results_cuts
    else:
        return run_inference(model_path, audio_data)
```

## 🔍 Example Usage Scenarios

### Scenario 1: Single Track Processing
```python
# Process a single track
filename = "my_track.wav"
audio, sr = librosa.load(filename, sr=22050)
audio_data = {filename: audio}

# Get suggestions
actions, cuts = run_inference("models/trained_model.pkl", audio_data)

# Display results
print(f"Suggestions for {filename}:")
for action in actions[filename]:
    print(f"  - Apply {action['effect']} to {action['target']} at level {action['level']}")
```

### Scenario 2: Album Processing
```python
# Process entire album
album_path = "data/album_tracks/"
audio_files = glob.glob(f"{album_path}*.wav")

# Process all tracks
all_actions = {}
all_cuts = {}

for audio_file in audio_files:
    audio, sr = librosa.load(audio_file, sr=22050)
    actions, cuts = run_inference("models/trained_model.pkl", {audio_file: audio})
    
    all_actions.update(actions)
    all_cuts.update(cuts)

# Save results
with open("album_suggestions.json", "w") as f:
    json.dump({"actions": all_actions, "cuts": all_cuts}, f, indent=2)
```

### Scenario 3: Live Performance Setup
```python
# Set up for live performance
live_processor = RealTimeInference("models/live_model.pkl")
live_processor.start()

# Simulate live audio input
for i in range(10):
    # Get audio from live source (microphone, line in, etc.)
    audio_chunk = get_live_audio_chunk()  # Your implementation
    live_processor.add_audio(f"live_chunk_{i}", audio_chunk)
    
    # Get and apply suggestions
    results = live_processor.get_results()
    for result in results:
        apply_suggestions_live(result['actions'])  # Your implementation
    
    time.sleep(0.1)  # Process every 100ms

live_processor.stop()
```

## 📋 Best Practices

### 1. Model Selection
- Use **genre-specific models** for best results
- **Ensemble models** for robust predictions
- **Custom models** for specific use cases

### 2. Performance Optimization
- **Cache loaded models** for repeated use
- **Process in batches** for multiple files
- **Monitor memory usage** for large datasets

### 3. Quality Control
- **Filter by confidence** scores
- **Apply user preferences** to suggestions
- **Validate suggestions** before applying

### 4. Error Handling
- **Check model compatibility** before inference
- **Handle missing files** gracefully
- **Monitor system resources** during processing

---

## 🔗 Related Documentation

- [**Usage Guide**](usage.md) - Getting started with MasterIA
- [**Performance Guide**](performance.md) - Optimization techniques
- [**API Reference**](api_reference.md) - Complete function documentation
- [**Troubleshooting**](troubleshooting.md) - Common issues and solutions

---

*For more advanced inference techniques and examples, check the [Jupyter notebooks](notebooks.md) in the project repository.*
