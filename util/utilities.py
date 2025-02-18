import pandas as pd   
import json
import uuid

def add_column_to_csv():
    df = pd.read_csv('test_datasets/test_bb.csv')

    df['processing_status'] = False

    df.to_csv('test_datasets/test_bb_new.csv', index=False)
    
def csv_to_json():
    df = pd.read_csv('test_datasets/hot100_test.csv')

    df.to_json('test_datasets/hot100_test.json', orient='records')

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(file_path, data):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def update_json_objects(data):
    for obj in data:
        unique_string = f"{obj['Song']}_{obj['Artist']}"
        obj['id'] = str(uuid.uuid5(uuid.NAMESPACE_DNS, unique_string))
    return data


def build_uuid_json_file():
    output_dir = "test_datasets/split_files/"
    
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
    
    data = load_json(file_path)
    
    chunk_size = len(data) // 100
    if len(data) % 100 != 0:
        chunk_size += 1
    
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


