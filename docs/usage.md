# Usage Guide

## Installation and Setup

### Prerequisites

Before using MasterIA, ensure you have Python 3.8+ installed on your system.

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Esgr0bar/MasterIA.git
   cd MasterIA
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Quick Start

#### 1. Basic Usage - Command Line

Run the main application:
```bash
python main.py
```

This will:
- Load audio data from `data/audio_with_metadata/`
- Extract features and train an initial model
- Run inference on new audio files from `data/new_audio/`
- Display suggested actions and cuts
- Collect user feedback for model improvement

#### 2. Using Individual Components

**Data Processing:**
```python
from src.data_processing import load_audio_files_with_metadata

# Load audio files with metadata
data_dir = "data/audio_with_metadata/"
audio_data, metadata = load_audio_files_with_metadata(data_dir)
```

**Feature Extraction:**
```python
from src.feature_extraction import extract_basic_features, extract_mfcc

# Extract basic features
features = extract_basic_features(audio_data)

# Extract MFCC features
mfcc_features = extract_mfcc(audio_data, n_mfcc=13)
```

**Model Training:**
```python
from src.model_training import prepare_data_for_training, train_model

# Prepare data for training
X, y = prepare_data_for_training(features, metadata)

# Train the model
model = train_model(X, y)
```

**Inference:**
```python
from src.inference import run_inference

# Run inference on new audio data
model_path = "models/trained_model.pkl"
suggested_actions, suggested_cuts = run_inference(model_path, new_audio_data)
```

## Data Preparation

### Audio File Format

MasterIA expects audio files in WAV format with accompanying JSON metadata files:

```
data/audio_with_metadata/
├── track1.wav
├── track1.json
├── track2.wav
├── track2.json
└── ...
```

### Metadata Format

Each audio file should have a corresponding JSON metadata file:

```json
{
  "title": "Track Name",
  "artist": "Artist Name",
  "genre": "Hip-hop",
  "bpm": 120,
  "key": "C major",
  "effects": [
    {
      "effect": "EQ",
      "target": "vocals",
      "level": 0.7
    },
    {
      "effect": "Reverb",
      "target": "drums",
      "level": 0.3
    }
  ]
}
```

## Advanced Usage

### Custom Model Training

You can train custom models for specific genres or use cases:

```python
from src.model_training import train_model
from src.feature_extraction import extract_basic_features

# Extract features for your specific dataset
features = extract_basic_features(genre_specific_data)

# Train a genre-specific model
model = train_model(features, genre_labels)

# Save the model
model.save("models/genre_specific_model.pkl")
```

### Batch Processing

Process multiple audio files at once:

```python
from src.data_processing import load_audio_files
from src.inference import run_inference

# Load multiple audio files
audio_files = load_audio_files("data/batch_processing/")

# Process all files
results = {}
for filename, audio_data in audio_files.items():
    actions, cuts = run_inference("models/trained_model.pkl", {filename: audio_data})
    results[filename] = {"actions": actions, "cuts": cuts}
```

### Interactive Mode

Use the tool interactively to get real-time feedback:

```python
from src.feedback import collect_user_feedback, save_feedback

# Get AI suggestions
actions, cuts = run_inference(model_path, audio_data)

# Collect user feedback
feedback = collect_user_feedback(actions, cuts)

# Save feedback for model improvement
save_feedback(feedback)
```

## Configuration

### Environment Variables

Set these environment variables to customize behavior:

```bash
export MASTERAI_DATA_DIR="/path/to/your/data"
export MASTERAI_MODEL_DIR="/path/to/your/models"
export MASTERAI_OUTPUT_DIR="/path/to/output"
```

### Model Parameters

Adjust model parameters in your code:

```python
# For ensemble model training
model = train_model(
    features, 
    labels,
    n_estimators=200,  # Random Forest estimators
    cnn_epochs=20,     # CNN training epochs
    test_size=0.2      # Train/test split ratio
)
```

## Output Format

### Suggested Actions

The AI outputs suggested actions in the following format:

```python
{
  "track1.wav": [
    {
      "effect": "EQ",
      "target": "vocals",
      "level": 0.8,
      "frequency": "high"
    },
    {
      "effect": "Compression",
      "target": "drums",
      "level": 0.6,
      "ratio": "4:1"
    }
  ]
}
```

### Suggested Cuts

Creative cuts and edits are suggested as:

```python
{
  "track1.wav": [
    {
      "action": "Cut",
      "location": "Chorus Start",
      "description": "Introduce a glitch effect",
      "timestamp": "0:45"
    },
    {
      "action": "Slice",
      "location": "Verse Mid",
      "description": "Add a stutter effect",
      "timestamp": "1:23"
    }
  ]
}
```

## Troubleshooting

### Common Issues

**1. Audio file not loading:**
```
Error: Could not load audio file
Solution: Ensure the file is in WAV format and not corrupted
```

**2. Model training fails:**
```
Error: Insufficient training data
Solution: Ensure you have at least 10 audio files with metadata
```

**3. Memory issues:**
```
Error: Out of memory during feature extraction
Solution: Process files in smaller batches or reduce audio length
```

### Performance Tips

1. **Use smaller audio segments** (5-10 seconds) for faster processing
2. **Preprocess audio files** to consistent sample rates (44.1kHz recommended)
3. **Use GPU acceleration** for CNN model training (if available)
4. **Cache extracted features** to avoid recomputation

## Examples

### Example 1: Basic Rap Track Processing

```python
# Load a rap track
audio_data, metadata = load_audio_files_with_metadata("data/rap_tracks/")

# Extract features
features = extract_basic_features(audio_data)

# Get AI suggestions
actions, cuts = run_inference("models/rap_model.pkl", audio_data)

# Print suggestions
for track, track_actions in actions.items():
    print(f"Track: {track}")
    for action in track_actions:
        print(f"  - Apply {action['effect']} to {action['target']} at level {action['level']}")
```

### Example 2: Custom Effect Analysis

```python
# Analyze specific effects in your tracks
from src.feature_extraction import extract_mfcc

# Extract detailed features
mfcc_features = extract_mfcc(audio_data, n_mfcc=25)

# Train a model specifically for effect recognition
effect_model = train_model(mfcc_features, effect_labels)

# Use the model to suggest similar effects
suggestions = effect_model.predict(new_track_features)
```

For more examples, check out the Jupyter notebooks in the `notebooks/` directory.