import json

def collect_user_feedback(suggested_actions, suggested_cuts):
    """Collect user feedback on the suggested actions and cuts.

    Args:
        suggested_actions (dict): The actions suggested by the AI.
        suggested_cuts (dict): The cuts suggested by the AI.

    Returns:
        list: A list of feedback entries, where each entry is a dictionary.
    """
    feedback = []

    print("Please rate the following AI suggestions (1-5, where 5 is very good and 1 is very bad):")

    for track_name, actions in suggested_actions.items():
        print(f"\nFeedback for track: {track_name}")
        for action in actions:
            print(f"Suggested {action['effect']} on {action['target']} with level {action['level']}")
            rating = int(input(f"Rate this suggestion (1-5): "))
            feedback.append({
                'track_name': track_name,
                'suggestion_type': 'action',
                'effect': action['effect'],
                'target': action['target'],
                'level': action['level'],
                'rating': rating
            })
        
        if track_name in suggested_cuts:
            print("\nSuggested Cuts/Creative Edits:")
            for cut in suggested_cuts[track_name]:
                print(f"{cut['action']} at {cut['location']}: {cut['description']}")
                rating = int(input(f"Rate this suggestion (1-5): "))
                feedback.append({
                    'track_name': track_name,
                    'suggestion_type': 'cut',
                    'action': cut['action'],
                    'location': cut['location'],
                    'description': cut['description'],
                    'rating': rating
                })

    return feedback

def save_feedback(feedback, filename="feedback.json"):
    """Saves user feedback to a JSON file.

    Args:
        feedback (list): List of feedback entries.
        filename (str): The name of the file where feedback will be saved.
    """
    try:
        with open(filename, 'a') as f:
            for entry in feedback:
                f.write(json.dumps(entry) + "\n")
        print(f"Feedback saved to {filename}")
    except Exception as e:
        print(f"Error saving feedback: {e}")
