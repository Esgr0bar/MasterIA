# Troubleshooting Guide

This guide helps you resolve common issues when using MasterIA. If you encounter problems not covered here, please [create an issue](https://github.com/Esgr0bar/MasterIA/issues) on GitHub.

## Installation Issues

### Python Version Problems

**Error**: `ModuleNotFoundError` or compatibility issues

**Solution**:
```bash
# Check Python version
python --version

# MasterIA requires Python 3.8+
# Install Python 3.8 or higher if needed
```

### Dependencies Installation Failed

**Error**: `pip install -r requirements.txt` fails

**Common Solutions**:

1. **Update pip**:
   ```bash
   python -m pip install --upgrade pip
   ```

2. **Install system dependencies** (Ubuntu/Debian):
   ```bash
   sudo apt-get update
   sudo apt-get install python3-dev libsndfile1-dev ffmpeg
   ```

3. **Install system dependencies** (macOS):
   ```bash
   brew install libsndfile ffmpeg
   ```

4. **Install system dependencies** (Windows):
   ```bash
   # Install Visual C++ Build Tools
   # Download from Microsoft website
   ```

### Virtual Environment Issues

**Error**: Package conflicts or import errors

**Solution**:
```bash
# Create clean virtual environment
python -m venv venv_new
source venv_new/bin/activate  # On Windows: venv_new\Scripts\activate
pip install -r requirements.txt
```

## Audio Loading Problems

### File Format Issues

**Error**: `librosa.load()` fails to load audio

**Common Causes and Solutions**:

1. **Unsupported format**:
   ```python
   # Convert to WAV using FFmpeg
   import subprocess
   subprocess.run(['ffmpeg', '-i', 'input.mp3', 'output.wav'])
   ```

2. **Corrupted file**:
   ```python
   # Check file integrity
   import librosa
   try:
       audio, sr = librosa.load('file.wav', sr=None)
       print(f"File loaded successfully: {len(audio)} samples at {sr} Hz")
   except Exception as e:
       print(f"Error loading file: {e}")
   ```

3. **File path issues**:
   ```python
   import os
   
   # Check if file exists
   if not os.path.exists('path/to/file.wav'):
       print("File not found")
   
   # Use absolute paths
   abs_path = os.path.abspath('path/to/file.wav')
   ```

### Sample Rate Issues

**Error**: Inconsistent sample rates across files

**Solution**:
```python
# Resample all files to consistent rate
import librosa

def resample_audio(input_file, output_file, target_sr=44100):
    audio, sr = librosa.load(input_file, sr=None)
    if sr != target_sr:
        audio_resampled = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
        librosa.output.write_wav(output_file, audio_resampled, target_sr)
    else:
        # Copy file if already correct sample rate
        import shutil
        shutil.copy(input_file, output_file)
```

### Memory Issues with Large Files

**Error**: `MemoryError` when loading large audio files

**Solution**:
```python
# Process files in chunks
def process_large_file(filename, chunk_duration=30):
    """Process large audio file in chunks"""
    import librosa
    
    # Get file duration
    duration = librosa.get_duration(filename=filename)
    
    results = []
    for start in range(0, int(duration), chunk_duration):
        # Load chunk
        audio, sr = librosa.load(filename, 
                                offset=start, 
                                duration=chunk_duration,
                                sr=None)
        
        # Process chunk
        chunk_features = extract_basic_features({f"chunk_{start}": audio})
        results.append(chunk_features)
    
    return results
```

## Feature Extraction Problems

### NaN Values in Features

**Error**: `ValueError` or `NaN` values in extracted features

**Solution**:
```python
import numpy as np

def clean_features(features):
    """Clean features by removing NaN values"""
    cleaned = {}
    for filename, feature_dict in features.items():
        cleaned[filename] = {}
        for key, value in feature_dict.items():
            if np.isnan(value):
                cleaned[filename][key] = 0.0  # Replace NaN with 0
            else:
                cleaned[filename][key] = value
    return cleaned

# Use in your workflow
features = extract_basic_features(audio_data)
features = clean_features(features)
```

### Empty or Silent Audio

**Error**: Features extracted from silent audio

**Solution**:
```python
def detect_silence(audio, threshold=0.01):
    """Detect if audio is mostly silent"""
    rms = np.sqrt(np.mean(audio**2))
    return rms < threshold

# Filter out silent files
filtered_audio = {}
for filename, audio in audio_data.items():
    if not detect_silence(audio):
        filtered_audio[filename] = audio
    else:
        print(f"Skipping silent file: {filename}")
```

### Feature Extraction Slow

**Problem**: Feature extraction takes too long

**Solutions**:

1. **Parallel processing**:
   ```python
   from multiprocessing import Pool
   import functools
   
   def extract_features_parallel(audio_data, n_processes=4):
       with Pool(n_processes) as pool:
           extract_func = functools.partial(extract_basic_features)
           # Split audio_data into chunks
           chunks = list(chunk_dict(audio_data, len(audio_data)//n_processes))
           results = pool.map(extract_func, chunks)
       return merge_results(results)
   ```

2. **Reduce feature complexity**:
   ```python
   # Use fewer MFCC coefficients
   mfcc_features = extract_mfcc(audio_data, n_mfcc=8)  # Instead of 13
   ```

3. **Cache results**:
   ```python
   import pickle
   
   def cache_features(features, cache_file):
       with open(cache_file, 'wb') as f:
           pickle.dump(features, f)
   
   def load_cached_features(cache_file):
       try:
           with open(cache_file, 'rb') as f:
               return pickle.load(f)
       except FileNotFoundError:
           return None
   ```

## Model Training Issues

### Insufficient Training Data

**Error**: Model performance is poor or training fails

**Solution**:
```python
# Check data distribution
import pandas as pd
from collections import Counter

def analyze_data_distribution(y):
    """Analyze label distribution in training data"""
    label_counts = Counter(y)
    
    print("Label distribution:")
    for label, count in label_counts.items():
        print(f"  {label}: {count} samples")
    
    # Check for class imbalance
    min_count = min(label_counts.values())
    max_count = max(label_counts.values())
    
    if max_count / min_count > 10:
        print("Warning: Significant class imbalance detected")
    
    return label_counts

# Analyze your data
label_counts = analyze_data_distribution(y)

# Minimum recommended samples per class
if any(count < 10 for count in label_counts.values()):
    print("Warning: Some classes have fewer than 10 samples")
```

### Memory Error During Training

**Error**: `MemoryError` or system runs out of memory

**Solution**:
```python
# Use batch training for large datasets
from sklearn.model_selection import train_test_split

def train_model_in_batches(X, y, batch_size=1000):
    """Train model in batches to save memory"""
    from sklearn.ensemble import RandomForestClassifier
    
    # Initialize model
    model = RandomForestClassifier(n_estimators=100, warm_start=True)
    
    # Train in batches
    for i in range(0, len(X), batch_size):
        X_batch = X[i:i+batch_size]
        y_batch = y[i:i+batch_size]
        
        # Fit model (incrementally)
        model.fit(X_batch, y_batch)
    
    return model
```

### Model Overfitting

**Problem**: High training accuracy but poor test performance

**Solution**:
```python
# Use cross-validation
from sklearn.model_selection import cross_val_score, StratifiedKFold

def evaluate_model_robustly(X, y, model):
    """Evaluate model with cross-validation"""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy')
    
    print(f"Cross-validation scores: {scores}")
    print(f"Mean CV score: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
    
    return scores

# Regularization techniques
from sklearn.ensemble import RandomForestClassifier

# Reduce complexity
model = RandomForestClassifier(
    n_estimators=50,  # Reduce from 100
    max_depth=10,     # Limit tree depth
    min_samples_split=10,  # Increase minimum samples
    min_samples_leaf=5     # Increase minimum leaf samples
)
```

### Slow Model Training

**Problem**: Training takes too long

**Solutions**:

1. **Reduce model complexity**:
   ```python
   # Use fewer estimators
   model = RandomForestClassifier(n_estimators=50)  # Instead of 100
   ```

2. **Use parallel processing**:
   ```python
   # Use all CPU cores
   model = RandomForestClassifier(n_jobs=-1)
   ```

3. **Feature selection**:
   ```python
   from sklearn.feature_selection import SelectKBest, f_classif
   
   # Select top K features
   selector = SelectKBest(score_func=f_classif, k=50)
   X_selected = selector.fit_transform(X, y)
   ```

## Inference Problems

### Model Loading Errors

**Error**: `FileNotFoundError` or model loading fails

**Solution**:
```python
import os
import joblib

def safe_load_model(model_path):
    """Safely load model with error handling"""
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

# Use in your code
model = safe_load_model("models/trained_model.pkl")
if model is None:
    print("Please train a model first")
```

### Prediction Errors

**Error**: Shape mismatch or prediction fails

**Solution**:
```python
def validate_input_shape(X, expected_features):
    """Validate input data shape"""
    if X.shape[1] != expected_features:
        raise ValueError(f"Expected {expected_features} features, got {X.shape[1]}")

# Save feature information with model
def save_model_with_metadata(model, feature_names, model_path):
    """Save model with feature metadata"""
    model_data = {
        'model': model,
        'feature_names': feature_names,
        'n_features': len(feature_names)
    }
    joblib.dump(model_data, model_path)

def load_model_with_metadata(model_path):
    """Load model with feature metadata"""
    model_data = joblib.load(model_path)
    return model_data['model'], model_data['feature_names']
```

## Performance Issues

### Slow Audio Processing

**Problem**: Audio processing is too slow

**Solutions**:

1. **Optimize audio loading**:
   ```python
   # Load only necessary duration
   audio, sr = librosa.load(filename, 
                           duration=30,  # Only load 30 seconds
                           sr=22050)     # Lower sample rate
   ```

2. **Use faster feature extraction**:
   ```python
   # Use hop_length to reduce computation
   mfccs = librosa.feature.mfcc(y=audio, 
                               sr=sr, 
                               n_mfcc=13,
                               hop_length=1024)  # Increase hop_length
   ```

3. **Batch processing**:
   ```python
   def process_files_in_batches(file_list, batch_size=10):
       """Process files in batches"""
       for i in range(0, len(file_list), batch_size):
           batch = file_list[i:i+batch_size]
           # Process batch
           yield process_batch(batch)
   ```

### High Memory Usage

**Problem**: Application uses too much memory

**Solutions**:

1. **Clear variables**:
   ```python
   import gc
   
   # Clear large variables
   del large_audio_data
   gc.collect()
   ```

2. **Use generators**:
   ```python
   def audio_data_generator(file_list):
       """Generate audio data on demand"""
       for filename in file_list:
           audio, sr = librosa.load(filename, sr=None)
           yield filename, audio
   
   # Use generator instead of loading all files
   for filename, audio in audio_data_generator(file_list):
       # Process one file at a time
       pass
   ```

## Documentation and Development

### MkDocs Build Errors

**Error**: Documentation build fails

**Solution**:
```bash
# Install dependencies
pip install mkdocs mkdocs-material mkdocstrings

# Check for syntax errors
mkdocs build --strict

# Common fixes
# 1. Fix markdown syntax errors
# 2. Check file paths in navigation
# 3. Verify code block syntax
```

### Jupyter Notebook Issues

**Error**: Notebooks won't run or display errors

**Solutions**:

1. **Kernel issues**:
   ```bash
   # Install kernel
   python -m ipykernel install --user --name=masterai
   
   # Restart kernel in notebook
   # Kernel -> Restart & Clear Output
   ```

2. **Missing dependencies**:
   ```bash
   # Install in notebook
   !pip install missing_package
   ```

3. **Path issues**:
   ```python
   # Add project root to path
   import sys
   sys.path.append('../')
   ```

## Getting Help

### Before Asking for Help

1. **Check this troubleshooting guide**
2. **Search existing issues** on GitHub
3. **Try the minimal example** to isolate the problem
4. **Check your Python and library versions**

### Creating a Good Bug Report

When reporting issues, include:

1. **System information**:
   ```python
   import sys
   import librosa
   import sklearn
   import tensorflow
   
   print(f"Python: {sys.version}")
   print(f"LibROSA: {librosa.__version__}")
   print(f"Scikit-learn: {sklearn.__version__}")
   print(f"TensorFlow: {tensorflow.__version__}")
   ```

2. **Minimal reproduction example**:
   ```python
   # Provide the smallest code that reproduces the issue
   from src.data_processing import load_audio_files
   
   # This fails
   audio_data = load_audio_files("path/to/files")
   ```

3. **Error traceback**: Copy the complete error message

4. **Expected vs actual behavior**: Describe what should happen vs what happens

### Community Resources

- **GitHub Issues**: [Report bugs and request features](https://github.com/Esgr0bar/MasterIA/issues)
- **GitHub Discussions**: [Ask questions and share ideas](https://github.com/Esgr0bar/MasterIA/discussions)
- **Documentation**: [Read the full documentation](https://esgr0bar.github.io/MasterIA/)
- **Examples**: Check the `notebooks/` directory for working examples

## Common Workflow Issues

### "No module named 'src'"

**Solution**:
```python
# Add project root to Python path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Or use relative imports
from .src.data_processing import load_audio_files
```

### "Model file not found"

**Solution**:
```python
# Check model directory
import os
if not os.path.exists("models/"):
    os.makedirs("models/")

# Train model if not exists
if not os.path.exists("models/trained_model.pkl"):
    print("Training new model...")
    # Train and save model
```

### "Feedback file not found"

**Solution**:
```python
# Create empty feedback file
import json
if not os.path.exists("feedback.json"):
    with open("feedback.json", "w") as f:
        pass  # Create empty file
```

Remember: Most issues are common and solvable! Don't hesitate to ask for help in the community forums.