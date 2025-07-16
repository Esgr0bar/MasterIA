# Usage Guide

## Getting Started

This guide will help you use the AI-Based Audio Mixing and Mastering tool effectively.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Esgr0bar/MasterIA.git
   cd MasterIA
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Basic Usage

The main entry point is the `main.py` script:

```bash
python main.py
```

### Processing Audio Files

1. **Prepare your audio data**:
   - Place raw audio files in the `data/raw/tracks/` directory
   - Each track should be in its own subdirectory

2. **Extract features**:
   - Use the feature extraction module to process your audio files
   - Features will be saved in `data/processed/features/`

3. **Train models**:
   - Use the model training module to create your AI models
   - Models will be saved in `data/processed/models/`

4. **Run inference**:
   - Use the inference module to apply effects to new audio files

### Advanced Usage

For more advanced usage, refer to the API Reference section and the Jupyter notebooks in the `notebooks/` directory.