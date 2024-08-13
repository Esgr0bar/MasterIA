def suggest_actions(model, features):
    """Suggests actions based on model predictions.

    Args:
        model: Trained model.
        features: Extracted features from new audio.

    Returns:
        dict: Suggested actions for each track.
    """
    actions = {}
    for filename, feature_values in features.items():
        prediction = model.predict([list(feature_values.values())])
        actions[filename] = prediction[0]  # Assuming the prediction is a list of actions
    return actions
    
def suggest_cuts(model, features):
    """Suggests creative cuts or glitches in the beats.

    Args:
        model: Trained machine learning model.
        features (dict): Extracted features from new audio tracks.

    Returns:
        dict: Suggested cuts or modifications.
    """
    cuts = {}
    for track_name, track_features in features.items():
        cuts[track_name] = []
        prediction = model.predict(track_features.T)
        
        # Example of suggesting cuts based on prediction
        if prediction == 1:  # Assuming 1 means take creative liberty
            cuts[track_name].append({
                'action': 'Cut',
                'location': 'Chorus Start',
                'description': 'Introduce a glitch effect'
            })
            cuts[track_name].append({
                'action': 'Slice',
                'location': 'Verse Mid',
                'description': 'Add a stutter effect'
            })

    return cuts

def print_suggested_actions(actions):
    """Prints out the suggested actions for each track.

    Args:
        actions (dict): Suggested actions dictionary.
    """
    for filename, action in actions.items():
        print(f"Track: {filename}")
        for act in action:
            print(f" - Suggested Action: {act}")
        print()
