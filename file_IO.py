import json

def save_data(data, filepath):
    
    try:
        
        with open(filepath,'w') as file:
            json.dump(data, file, indent = 4)
        
        print(f"Success: Data saved successfully to '{filepath}'.")

    except Exception as e:
        print(f"Error: Failed to save data. System message: {e}")

def load_data(filepath):

    try:

        with open(filepath,'r') as file:
            data = json.load(file)
            return data
        
    except FileNotFoundError:
        print(f"Warning: File '{filepath}' not found. Returning an empty database.")
        return[]
    
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' is corrupted or empty. Returning an empty database to prevent crash.")
        return []
    
    except Exception as e:
        print(f"Error: Unknown issue while reading '{filepath}'. System message: {e}")
        return[]


# Test Block

if __name__ == "__main__":
    test_file = 'text_transaction.json'
    
    print('\n--- Test 1: Loading a non-existent file ---')
    my_data = load_data(test_file)
    print("Current data in memory:", my_data)
    
    print("\n--- Test 2: Saving new data ---")
    test_transaction = {
        "date": "2026-04-05",
        "amount": 30.0,
        "category": "Food",
        "description": "Ate a burger."
    }
    my_data.append(test_transaction)
    save_data(my_data, test_file)

    print("\n--- Test 3: Loading the saved file ---")
    reloaded_data = load_data(test_file)
    print("Data loaded from hard drive:", reloaded_data)


            
    


