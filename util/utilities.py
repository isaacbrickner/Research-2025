import pandas as pd   
import json
import uuid

def add_column_to_csv():
    # Load the CSV file
    df = pd.read_csv('test_datasets/test_bb.csv')

    # Add a new column with default value False
    df['processing_status'] = False

    # Save the updated DataFrame back to CSV
    df.to_csv('test_datasets/test_bb_new.csv', index=False)
    
def csv_to_json():
    # Load the CSV file
    df = pd.read_csv('test_datasets/hot100_test.csv')

    # Save the updated DataFrame back to JSON
    df.to_json('test_datasets/hot100_test.json', orient='records')

# Load the JSON file
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Save JSON back to the file
def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Assign unique ID and value
def update_json_objects(data, start_id=1):
    for index, obj in enumerate(data):
        obj['id'] = start_id + index  # Incremental ID
    return data


def build_uuid_json_file():
    output_dir = "test_datasets/split_files/"
    
    # Iterate over each chunk file
    for i in range(100):
        chunk_file_path = f"{output_dir}hot100_test_chunk_{i + 1}.json"
        
        # Process the JSON
        data = load_json(chunk_file_path)
        updated_data = update_json_objects(data)
        save_json(chunk_file_path, updated_data)
        print(f"Chunk {i + 1} updated successfully!")
    
def split_json_file():
    file_path = "test_datasets/hot100_test.json"
    output_dir = "test_datasets/split_files/"
    
    # Load the JSON data
    data = load_json(file_path)
    
    # Calculate the size of each chunk
    chunk_size = len(data) // 100
    if len(data) % 100 != 0:
        chunk_size += 1
    
    # Split the data into chunks and save each chunk to a new file
    for i in range(100):
        chunk = data[i * chunk_size:(i + 1) * chunk_size]
        chunk_file_path = f"{output_dir}hot100_test_chunk_{i + 1}.json"
        save_json(chunk_file_path, chunk)
        print(f"Chunk {i + 1} saved to {chunk_file_path}")

    # Uncomment the following line to call the function
    # split_json_file()

def main():
    # build_uuid_json_file()
    # add_column_to_csv()
    # csv_to_json()
    # split_json_file()
    build_uuid_json_file()
    
if __name__ == "__main__":
    main()


