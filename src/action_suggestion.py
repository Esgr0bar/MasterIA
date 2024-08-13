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
