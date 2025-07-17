# Jupyter Notebooks

## Overview

The Jupyter notebooks included in this project are designed for data exploration, model training, and experimentation. They provide an interactive environment where you can test different approaches, visualize results, and understand the inner workings of the AI system.

### Available Notebooks

#### 1. EDA.ipynb - Exploratory Data Analysis
**Purpose**: Comprehensive exploration of audio data and metadata

**Contents**:
- **Audio Data Loading**: Load and inspect various audio formats
- **Waveform Visualization**: Plot time-domain audio signals
- **Spectral Analysis**: Frequency domain analysis and spectrograms
- **Feature Distribution**: Statistical analysis of extracted features
- **Metadata Exploration**: Analyze effect parameters and labels
- **Data Quality Assessment**: Identify missing or corrupted data
- **Genre Comparison**: Compare audio characteristics across genres

**Key Outputs**:
- Audio visualizations (waveforms, spectrograms, mel-spectrograms)
- Feature correlation matrices
- Statistical summaries and distributions
- Data quality reports

#### 2. Model_Training.ipynb - Machine Learning Model Development
**Purpose**: Build, train, and evaluate AI models for audio processing

**Contents**:
- **Feature Engineering**: Create and select optimal features
- **Model Architecture**: Design ensemble models (CNN + RF + SVM)
- **Training Pipeline**: Cross-validation and hyperparameter tuning
- **Performance Evaluation**: Metrics, confusion matrices, and validation
- **Model Comparison**: Compare different algorithms and architectures
- **Feedback Integration**: Incorporate user feedback into training
- **Model Deployment**: Save and version trained models

**Key Outputs**:
- Trained models (.pkl files)
- Performance metrics and reports
- Learning curves and validation plots
- Feature importance analysis

## 🚀 Getting Started

### Prerequisites

Before running the notebooks, ensure you have the required dependencies installed:

```bash
# Install core dependencies
pip install -r requirements.txt

# Install Jupyter if not already installed
pip install jupyter notebook jupyterlab

# Optional: Install additional visualization libraries
pip install seaborn plotly ipywidgets
```

### Launching Notebooks

1. **Start Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

2. **Or use JupyterLab** (recommended):
   ```bash
   jupyter lab
   ```

3. **Navigate to the notebooks directory**:
   ```bash
   cd notebooks/
   ```

### Running the Notebooks

#### Option 1: Sequential Execution
1. Start with `EDA.ipynb` to understand your data
2. Proceed to `Model_Training.ipynb` for model development
3. Use the trained models for inference

#### Option 2: Focused Exploration
- Jump directly to specific sections based on your needs
- Use the table of contents in each notebook for navigation
- Modify parameters and experiment with different approaches

## 📊 EDA Notebook Details

### Data Loading and Inspection
```python
# Load audio data with metadata
audio_data, metadata = load_audio_files_with_metadata("../data/audio_with_metadata/")

# Display basic information
print(f"Total tracks: {len(audio_data)}")
print(f"Sample rate: {librosa.get_samplerate(list(audio_data.keys())[0])}")
```

### Visualization Examples
```python
# Waveform visualization
plt.figure(figsize=(12, 4))
plt.plot(audio_data['track1.wav'][0])
plt.title('Waveform')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

# Spectrogram
D = librosa.stft(audio_data['track1.wav'][0])
plt.figure(figsize=(12, 6))
librosa.display.specshow(librosa.amplitude_to_db(np.abs(D)), sr=sr, x_axis='time', y_axis='hz')
plt.colorbar()
plt.title('Spectrogram')
```

### Feature Analysis
```python
# Extract and analyze features
features = extract_basic_features(audio_data)

# Create feature distribution plots
feature_df = pd.DataFrame(features).T
feature_df.hist(bins=20, figsize=(15, 10))
plt.tight_layout()
plt.show()
```

## 🤖 Model Training Notebook Details

### Feature Engineering
```python
# Extract comprehensive features
mfcc_features = extract_mfcc(audio_data, n_mfcc=13)
spectral_features = extract_basic_features(audio_data)

# Combine features
combined_features = combine_features(mfcc_features, spectral_features)
```

### Model Training
```python
# Prepare data for training
X, y = prepare_data_for_training(combined_features, metadata)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train ensemble model
model = train_model(X_train, y_train)

# Evaluate performance
accuracy = model.score(X_test, y_test)
print(f"Model accuracy: {accuracy:.3f}")
```

### Model Evaluation
```python
# Generate predictions
y_pred = model.predict(X_test)

# Create confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('Confusion Matrix')
plt.ylabel('Actual')
plt.xlabel('Predicted')
```

## 🎯 Best Practices

### Data Preparation
1. **Consistent Format**: Ensure all audio files have the same sample rate
2. **Quality Check**: Verify audio files are not corrupted
3. **Metadata Validation**: Check that metadata matches audio files
4. **Balanced Dataset**: Ensure good representation across genres/effects

### Model Training
1. **Cross-validation**: Use k-fold cross-validation for robust evaluation
2. **Hyperparameter Tuning**: Use GridSearchCV for optimal parameters
3. **Feature Selection**: Remove redundant or low-importance features
4. **Early Stopping**: Monitor validation loss to prevent overfitting

### Experimentation
1. **Version Control**: Save different model versions for comparison
2. **Documentation**: Add markdown cells explaining your approach
3. **Reproducibility**: Set random seeds for consistent results
4. **Visualization**: Create plots to understand model behavior

## 🔧 Customization

### Adding New Features
```python
def extract_custom_features(audio_data):
    """Extract custom audio features"""
    features = {}
    for filename, (audio, _) in audio_data.items():
        # Your custom feature extraction logic
        custom_feature = your_feature_function(audio)
        features[filename] = custom_feature
    return features
```

### Creating New Visualizations
```python
def plot_feature_importance(model, feature_names):
    """Plot feature importance from trained model"""
    importances = model.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title("Feature Importance")
    plt.bar(range(len(importances)), importances[indices])
    plt.xticks(range(len(importances)), [feature_names[i] for i in indices], rotation=45)
    plt.tight_layout()
```

### Experiment Tracking
```python
# Track experiments
experiment_results = {
    'model_type': 'ensemble',
    'features': ['mfcc', 'spectral'],
    'accuracy': accuracy,
    'parameters': model.get_params(),
    'timestamp': datetime.now()
}

# Save results
with open('experiment_log.json', 'a') as f:
    json.dump(experiment_results, f)
    f.write('\n')
```

## 📈 Performance Monitoring

### Key Metrics to Track
- **Accuracy**: Overall model performance
- **Precision/Recall**: Class-specific performance
- **F1-Score**: Balanced performance metric
- **Training Time**: Model efficiency
- **Memory Usage**: Resource consumption

### Visualization Tools
- **Learning Curves**: Track training progress
- **Validation Plots**: Monitor overfitting
- **Feature Importance**: Understand model decisions
- **Confusion Matrices**: Detailed performance analysis

## 🚨 Troubleshooting

### Common Issues

**Memory Error**:
```python
# Solution: Process data in batches
batch_size = 32
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    # Process batch
```

**Slow Training**:
```python
# Solution: Use fewer features or smaller models
selected_features = select_k_best_features(X, y, k=50)
```

**Poor Performance**:
```python
# Solution: Feature engineering or more data
# Check data quality and feature distributions
```

## 💡 Tips for Success

1. **Start Simple**: Begin with basic features and simple models
2. **Iterate Quickly**: Make small changes and test frequently
3. **Document Everything**: Keep notes on what works and what doesn't
4. **Visualize Results**: Use plots to understand your data and models
5. **Collaborate**: Share notebooks with team members for feedback

## 🔗 Additional Resources

- **[LibROSA Documentation](https://librosa.org/doc/latest/index.html)**: Audio analysis library
- **[scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)**: Machine learning library
- **[TensorFlow Tutorials](https://www.tensorflow.org/tutorials)**: Deep learning framework
- **[Jupyter Documentation](https://jupyter.org/documentation)**: Notebook platform

Explore the notebooks to get hands-on experience with the data and the models! Each notebook is designed to be educational and practical, helping you understand both the theory and implementation of AI-based audio processing.