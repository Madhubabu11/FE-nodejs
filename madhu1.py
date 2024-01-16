import sys
import boto3
from prettytable import PrettyTable

def fetch_dynamodb_data(table_name, region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response.get('Items', [])

    return items

def print_all_attributes_table(items):
    if not items:
        print("No items found.")
        return

    table = PrettyTable()
    field_names_set = set(['ItemId'])

    for item in items:
        field_names_set.update(item.keys())

    table.field_names = list(field_names_set)

    for item in items:
        row_values = [item.get('ItemId')] + [item.get(attribute) for attribute in field_names_set if attribute != 'ItemId']
        table.add_row(row_values)

    print(table)

if __name__ == "__main__":
    # Replace 'your_table_name' and 'your_region' with your actual DynamoDB table name and region
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        item_id = sys.argv[1]
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        filtered_data = [item for item in dynamodb_data if item.get('ItemId') == item_id]
        print_all_attributes_table(filtered_data)

    except Exception as e:
        print(f"Error: {e}")