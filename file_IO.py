import json


def save_data(data, filepath):
    try:
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Success: Data saved successfully to '{filepath}'.")
    except Exception as e:
        print(f"Error: Failed to save data. System message: {e}")


def load_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: File '{filepath}' not found. Returning an empty database.")
        return []
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is corrupted or empty. Returning an empty database to prevent crash.")
        return []
    except Exception as e:
        print(f"Error: Unknown issue while reading '{filepath}'. System message: {e}")
        return []


def save_rules(rules, filepath):
    try:
        with open(filepath, 'w') as file:
            json.dump(rules, file, indent=4)
        print(f"Success: Rules saved to '{filepath}'.")
    except Exception as e:
        print(f"Error: Failed to save rules. System message: {e}")


def load_rules(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Error: '{filepath}' is corrupted. Returning empty rules.")
        return []
    except Exception as e:
        print(f"Error: Could not read '{filepath}'. System message: {e}")
        return []
