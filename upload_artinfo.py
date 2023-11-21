import csv

def read_csv_and_format_for_dynamodb(csv_path):
    formatted_data = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # Formatting each field as a string for DynamoDB
            dynamodb_item = {key: {"S": str(value)} for key, value in row.items()}
            formatted_data.append(dynamodb_item)
    return formatted_data

# Replace with your actual CSV file path
csv_file_path = 'ArtRetrieval/van_gogh_paintings.csv'
dynamodb_data = read_csv_and_format_for_dynamodb(csv_file_path)

# This will contain the formatted data
import subprocess, json
from tqdm import tqdm
table_name = 'ArtInfo'

for item in tqdm(dynamodb_data):
    item_json = json.dumps(item)
    subprocess.run(['aws', 'dynamodb', 'put-item', '--table-name', table_name, '--item', item_json], check=True)
