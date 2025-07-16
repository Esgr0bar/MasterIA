# API Reference

This section contains the detailed API documentation for the project's Python modules. Each module provides specific functionality for audio processing, machine learning, and user interaction.

## Quick Start

```python
from src.data_processing import load_audio_files_with_metadata
from src.feature_extraction import extract_basic_features
from src.model_training import train_model, prepare_data_for_training
from src.inference import run_inference

# Load and process audio data
audio_data, metadata = load_audio_files_with_metadata("data/audio_with_metadata/")
features = extract_basic_features(audio_data)

# Train a model
X, y = prepare_data_for_training(features, metadata)
model = train_model(X, y)

# Run inference
suggested_actions, suggested_cuts = run_inference("models/trained_model.pkl", audio_data)
```

## Modules Overview

### Data Processing (`src.data_processing`)
Functions for loading and preprocessing audio data from various formats.

**Key Functions:**
- `load_audio_files_with_metadata(directory)` - Load audio files with JSON metadata
- `load_audio_files(directory)` - Load audio files without metadata
- `split_tracks(audio_data, segment_length=5)` - Split audio into segments

### Feature Extraction (`src.feature_extraction`)
Methods to extract meaningful features from audio data for machine learning.

**Key Functions:**
- `extract_basic_features(audio_data)` - Extract spectral and temporal features
- `extract_mfcc(audio_data, n_mfcc=13)` - Extract MFCC coefficients
- `extract_spectrogram(audio_data)` - Extract mel-scale spectrograms

### Model Training (`src.model_training`)
Scripts for building, training, and evaluating machine learning models.

**Key Functions:**
- `prepare_data_for_training(features, metadata)` - Prepare data for ML training
- `train_model(X, y)` - Train ensemble model (CNN + RF + SVM)
- `train_action_prediction_model(X, y)` - Train action-specific model

### Inference (`src.inference`)
Functions for running trained models on new audio data.

**Key Functions:**
- `load_model(model_path)` - Load pre-trained model
- `predict_actions(model, audio_data)` - Predict actions and cuts
- `run_inference(model_path, audio_data)` - Complete inference pipeline

### Action Suggestions (`src.action_suggestion`)
Functions for generating and processing AI-suggested audio modifications.

**Key Functions:**
- `suggest_actions(model, features)` - Generate action suggestions
- `suggest_cuts(model, features)` - Generate creative cut suggestions
- `print_suggested_actions(actions)` - Display suggestions

### Feedback System (`src.feedback`)
Functions for collecting and processing user feedback.

**Key Functions:**
- `collect_user_feedback(actions, cuts)` - Collect user feedback
- `save_feedback(feedback, filename)` - Save feedback to file
- `incorporate_feedback_into_training(features, labels, feedback_file)` - Retrain with feedback

## Complete Usage Example

```python
import os
from src.data_processing import load_audio_files_with_metadata
from src.feature_extraction import extract_basic_features
from src.model_training import train_model, prepare_data_for_training
from src.inference import run_inference
from src.feedback import collect_user_feedback, save_feedback

# 1. Load training data
audio_data, metadata = load_audio_files_with_metadata("data/training/")

# 2. Extract features
features = extract_basic_features(audio_data)

# 3. Prepare and train model
X, y = prepare_data_for_training(features, metadata)
model = train_model(X, y)

# 4. Save model
import joblib
joblib.dump(model, "models/my_model.pkl")

# 5. Run inference on new data
new_audio_data, _ = load_audio_files_with_metadata("data/new_tracks/")
actions, cuts = run_inference("models/my_model.pkl", new_audio_data)

# 6. Collect feedback
feedback = collect_user_feedback(actions, cuts)
save_feedback(feedback)

# 7. Display results
print("Suggested Actions:")
for filename, action_list in actions.items():
    print(f"  {filename}: {action_list}")

print("\nSuggested Cuts:")
for filename, cut_list in cuts.items():
    print(f"  {filename}: {cut_list}")
```

## Error Handling

All functions include proper error handling:

```python
try:
    audio_data, metadata = load_audio_files_with_metadata("data/audio/")
except FileNotFoundError:
    print("Audio directory not found")
except Exception as e:
    print(f"Error loading audio: {e}")

try:
    model = load_model("models/trained_model.pkl")
except FileNotFoundError:
    print("Model file not found - please train a model first")
```

## Performance Tips

1. **Batch Processing**: Process multiple files together
2. **Caching**: Cache extracted features to avoid recomputation
3. **Memory Management**: Use generators for large datasets
4. **Parallel Processing**: Use multiprocessing for CPU-intensive tasks

```python
# Example of efficient batch processing
def process_batch(file_list, batch_size=32):
    for i in range(0, len(file_list), batch_size):
        batch = file_list[i:i+batch_size]
        # Process batch
        yield process_files(batch)
```

## Configuration

Most functions accept optional parameters for customization:

```python
# Feature extraction with custom parameters
features = extract_basic_features(audio_data)
mfcc_features = extract_mfcc(audio_data, n_mfcc=25)  # More detailed features

# Model training with custom parameters
model = train_model(X, y, n_estimators=200, test_size=0.3)
```

For detailed function signatures and examples, see the individual module documentation in the Reference section.
