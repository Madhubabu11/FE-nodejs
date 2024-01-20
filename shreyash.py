import boto3
import sys

def fetch_dynamodb_data(table_name, region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    response = table.scan()
    items = response.get('Items', [])

    return items

def print_available_cidr(items):
    if not items:
        print("No items found.")
        return

    available_items = [item.get('cidr') for item in items if item.get('status', '').lower() == 'available']

    if not available_items:
        print("No items found with the status 'Available'.")
        return

    print("DynamoDB Data: Available CIDR")
    print(", ".join(available_items))

def choose_cidr(items):
    print("\nChoose a CIDR :")
    
    available_items = [item.get('cidr') for item in items if item.get('status', '').lower() == 'available']
    
    if not available_items:
        print("No items found with the status 'Available'.")
        return None

    for index, cidr in enumerate(available_items, start=1):
        print(f"{index}. {cidr}")

    try:
        choice_index = int(input("Enter the index of the CIDR you want to choose: "))
        chosen_cidr = available_items[choice_index - 1]
        return chosen_cidr
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid index.")
        return None

if __name__ == "__main__":
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        print_available_cidr(dynamodb_data)

        chosen_cidr = choose_cidr(dynamodb_data)
        
        if chosen_cidr:
            print(f"Chosen CIDR: {chosen_cidr}")

    except Exception as e:
        print(f"Error: {e}")
