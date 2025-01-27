import pandas as pd

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

def main():
    pass

if __name__ == "__main__":
    main()
    # add_column_to_csv()
    # csv_to_json()

