import boto3
import sys

def fetch_dynamodb_data(table_name, region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response.get('Items', [])

    return items

def print_availability_cidr_blocks(items):
    if not items:
        print("No items found.")
        return

    availability_items = [item.get('CIDRBlock') for item in items if item.get('status', '').lower() == 'availability']

    if not availability_items:
        print("No items found with the status 'Availability'.")
        return

    print("DynamoDB Data: Available CIDR Blocks")
    print(", ".join(availability_items))

def choose_cidr_block(items):
    print("\nChoose a CIDR Block:")
    
    availability_items = [item.get('CIDRBlock') for item in items if item.get('status', '').lower() == 'availability']
    
    if not availability_items:
        print("No items found with the status 'Availability'.")
        return None

    for index, cidr_block in enumerate(availability_items, start=1):
        print(f"{index}. {cidr_block}")

    try:
        choice_index = int(input("Enter the index of the CIDR block you want to choose: "))
        chosen_cidr_block = availability_items[choice_index - 1]
        return chosen_cidr_block
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid index.")
        return None

if __name__ == "__main__":
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        print_availability_cidr_blocks(dynamodb_data)

        chosen_cidr_block = choose_cidr_block(dynamodb_data)
        
        if chosen_cidr_block:
            print(f"Chosen CIDR Block: {chosen_cidr_block}")

    except Exception as e:
        print(f"Error: {e}")
