# AI-Based Audio Mixing and Mastering

This project aims to develop an AI that can perform automated audio mixing and mastering based on user-defined preferences or by analyzing reference tracks.

## Project Structure
data may be stored locally due to large size of files
- `data/`: Contains all datasets and related metadata.
  - `raw/`: Raw audio data and metadata.
    - `tracks/`: Subdirectory for individual songs, each containing separate tracks (e.g., vocals, drums) and the final mix.
    - `metadata/`: Metadata files for each song, containing information about applied effects.
  - `processed/`: Processed data such as extracted features and trained models.
    - `features/`: Extracted audio features (e.g., MFCCs, spectrograms).
    - `models/`: Saved models for mixing and mastering.

- `src/`: Source code for data processing, feature extraction, model training, and inference.
  - `data_processing.py`: Scripts for processing raw audio data.
  - `feature_extraction.py`: Scripts for extracting features like MFCCs and spectrograms.
  - `model_training.py`: Scripts for training the AI models.
  - `inference.py`: Scripts to run the trained models on new data.

- `tests/`: Unit tests for all modules.

- `notebooks/`: Jupyter notebooks for exploratory data analysis (EDA) and model development.

- `.github/workflows/`: CI/CD workflows using GitHub Actions.

- `README.md`: This document.

- `requirements.txt`: Python dependencies for the project.

- `setup.py`: Package setup script.

## Data Format Guidelines

### 1. Raw Audio Data

- **Audio Format**: All raw audio files should be in WAV format with a sample rate of 44.1kHz or higher.
- **Directory Structure**: 
  - Each song should have its own directory inside `data/raw/tracks/`.
  - Inside each song directory, include:
    - `vocals.wav`: Isolated vocals track.
    - `drums.wav`: Isolated drums track.
    - `bass.wav`: Isolated bass track.
    - `mix.wav`: The final mixed track.

### 2. Metadata

- **Format**: JSON files.
- **Structure**:
  - Each song should have a corresponding metadata file in `data/raw/metadata/` named `songname_metadata.json`.
  - The JSON file should contain details about the applied effects, such as EQ settings, compression ratios, reverb parameters, etc.
  
  Example structure:
  ```json
  {
    "vocals": {
      "eq": {"low_cut": 100, "high_cut": 10000},
      "compression": {"threshold": -20, "ratio": 4}
    },
    "drums": {
      "eq": {"low_cut": 50, "high_cut": 15000},
      "compression": {"threshold": -15, "ratio": 3}
    },
    ...
  }
