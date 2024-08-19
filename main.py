import os
from src.data_processing import load_audio_files_with_metadata
from src.feature_extraction import extract_basic_features
from src.model_training import prepare_data_for_training, train_model, incorporate_feedback_into_training
from src.action_suggestion import print_suggested_actions
from src.feedback import collect_user_feedback, save_feedback
from inference import run_inference, load_model

def main():
    # Step 1: Load the data for initial training
    data_directory = "data/audio_with_metadata/"
    audio_data, metadata = load_audio_files_with_metadata(data_directory)

    # Step 2: Extract features
    features = extract_basic_features(audio_data)

    # Step 3: Prepare data and train the model
    X, y = prepare_data_for_training(features, metadata)
    model = train_model(X, y)  # Initial training
    
    # Save the model for later inference
    model_path = "models/trained_model.pkl"
    model.save_model(model_path)

    # Step 4: Use the model to suggest actions on new audio data through inference
    new_data_directory = "data/new_audio/"
    new_audio_data, _ = load_audio_files_with_metadata(new_data_directory)

    # Load the model for inference
    inference_model = load_model(model_path)
    
    # Run inference to get suggested actions and cuts
    suggested_actions, suggested_cuts = run_inference(model_path, new_audio_data)

    # Print the suggested actions and cuts
    print_suggested_actions(suggested_actions, suggested_cuts)

    # Step 5: Collect and save user feedback
    feedback = collect_user_feedback(suggested_actions, suggested_cuts)
    save_feedback(feedback)

    # Step 6: Retrain the model using the feedback
    model = incorporate_feedback_into_training(features, metadata)
    model.save_model(model_path)

if __name__ == "__main__":
    main()
