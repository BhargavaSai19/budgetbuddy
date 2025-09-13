import json
def load_json(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {filepath}. Returning empty data.")
        return{}


def save_json(data, filepath):
    """Saves a dictionary to a JSON file."""
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Successfully saved data to {filepath}.")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")    