# Data Handling

## Data Structure

The project works with audio data stored in a specific directory structure:

- **Raw Data**: Unprocessed audio files, typically in `.wav` format.
  - `data/raw/tracks/`: Contains folders for each track (e.g., `song1/`, `song2/`).
  - Example: `data/raw/tracks/song1/vocals.wav`

- **Processed Data**: Feature files and preprocessed data ready for model input.
  - `data/processed/features/`: Contains extracted features like MFCCs and spectrograms.
  - Example: `data/processed/features/song1_vocals_mfcc.npy`

## Data Collection

- **Source Audio**: Collect raw audio files for different tracks (vocals, instruments, etc.).
- **Reference Tracks**: Include mixed and mastered tracks for the AI to learn from.

### Data Processing Workflow

1. **Loading Audio**:
   - Use the `load_audio()` function from `src/data_processing.py` to load audio files into numpy arrays.

2. **Splitting Tracks**:
   - Use the `split_tracks()` function to divide longer audio files into manageable segments.

3. **Feature Extraction**:
   - Use `extract_mfcc()` and `extract_spectrogram()` from `src/feature_extraction.py` to extract features for model training.

4. **Saving Processed Data**:
   - Save extracted features as `.npy` files in the `data/processed/features/` directory.

Ensure your data is properly organized before starting model training.
