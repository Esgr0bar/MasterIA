# Inference Script Documentation

## Overview

The `inference.py` script is designed to perform inference on new audio data using a pre-trained machine learning model. It suggests actions and creative cuts to be applied to the audio tracks.

## Functions

### `load_model(model_path)`
- **Description**: Loads the pre-trained machine learning model from the specified path.
- **Arguments**:
  - `model_path` (str): Path to the model file.
- **Returns**: The loaded model.

### `predict_actions(model, audio_data)`
- **Description**: Predicts the actions and cuts for the given audio data using the pre-trained model.
- **Arguments**:
  - `model`: The pre-trained machine learning model.
  - `audio_data` (dict): Dictionary where keys are filenames and values are audio data.
- **Returns**: A dictionary with suggested actions and cuts for each audio file.

### `run_inference(model_path, audio_data)`
- **Description**: The main function that runs the inference process. It loads the model, predicts the actions, and returns the results.
- **Arguments**:
  - `model_path` (str): Path to the pre-trained model file.
  - `audio_data` (dict): Dictionary where keys are filenames and values are audio data.
- **Returns**: A dictionary with suggested actions and cuts for each audio file.

## Usage

```bash
python inference.py --model_path "path/to/saved/model.pkl" --audio_data "path/to/audio/files"
