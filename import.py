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
    field_names_set = set(['ItemId', 'status', 'CIDRBlock'])  # Include ItemId, status, and CIDRBlock in the field names

    for item in items:
        field_names_set.update(item.keys())

    table.field_names = list(field_names_set)

    for item in items:
        row_values = [item.get('ItemId'), item.get('status'), item.get('CIDRBlock')] + [item.get(attribute) for attribute in field_names_set if attribute not in ['ItemId', 'status', 'CIDRBlock']]
        table.add_row(row_values)

    print(table)

def choose_cidr_block(items):
    print("\nChoose a CIDRBlock and ItemId:")
    
    # Display the list of items with 'Availability' status
    availability_items = [item for item in items if item.get('status', '').lower() == 'availability']
    
    if not availability_items:
        print("No items found with the status 'Availability'.")
        return None

    for index, item in enumerate(availability_items, start=1):
        print(f"{index}. CIDRBlock: {item.get('CIDRBlock')}, ItemId: {item.get('ItemId')}")

    # Prompt user to choose an item by index
    try:
        choice_index = int(input("Enter the index of the item you want to choose: "))
        chosen_item = availability_items[choice_index - 1]
        return chosen_item
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid index.")
        return None

def get_user_choice():
    status_values = {'1': 'Availability', '2': 'InUse'}
    prompt = f"Choose Option:\n1. Availability\n2. InUse\nEnter the option number (1 or 2): "
    
    user_choice = input(prompt)
    while user_choice not in status_values.keys():
        print("Invalid choice. Please choose a valid option number.")
        user_choice = input(prompt)

    return status_values[user_choice]

if __name__ == "__main__":
    # Replace 'your_table_name' and 'your_region' with your actual DynamoDB table name and region
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        print("DynamoDB Data:", dynamodb_data)  # Print DynamoDB Data for inspection
        print_all_attributes_table(dynamodb_data)

        # Get user choice for Option
        chosen_option = get_user_choice()

        if chosen_option.lower() == 'availability':
            chosen_item = choose_cidr_block(dynamodb_data)
            if chosen_item:
                print(f"Chosen CIDRBlock: {chosen_item.get('CIDRBlock')}")
                print(f"Chosen ItemId: {chosen_item.get('ItemId')}")
        else:
            # Find the item with the chosen Status (case-insensitive)
            chosen_status = get_user_choice()

            chosen_item = next((item for item in dynamodb_data if item.get('status', '').lower() == chosen_status.lower()), None)

            if chosen_item:
                print(f"Chosen Status: {chosen_item.get('status')}")
                print(f"CIDRBlock Value: {chosen_item.get('CIDRBlock')}")
                print(f"ItemId: {chosen_item.get('ItemId')}")
            else:
                print(f"No item found with the chosen Status: {chosen_status}")

    except Exception as e:
        print(f"Error: {e}")

root@ip-10-0-23-34:~# cat hh.py 
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
    field_names_set = set(['ItemId', 'status', 'CIDRBlock'])  # Include ItemId, status, and CIDRBlock in the field names

    for item in items:
        field_names_set.update(item.keys())

    table.field_names = list(field_names_set)

    for item in items:
        row_values = [item.get('ItemId'), item.get('status'), item.get('CIDRBlock')] + [item.get(attribute) for attribute in field_names_set if attribute not in ['ItemId', 'status', 'CIDRBlock']]
        table.add_row(row_values)

    print(table)

def choose_cidr_block(items):
    print("\nChoose a CIDRBlock and ItemId:")
    
    # Display the list of items with 'Availability' status
    availability_items = [item for item in items if item.get('status', '').lower() == 'availability']
    
    if not availability_items:
        print("No items found with the status 'Availability'.")
        return None

    for index, item in enumerate(availability_items, start=1):
        print(f"{index}. CIDRBlock: {item.get('CIDRBlock')}, ItemId: {item.get('ItemId')}")

    # Prompt user to choose an item by index
    try:
        choice_index = int(input("Enter the index of the item you want to choose: "))
        chosen_item = availability_items[choice_index - 1]
        return chosen_item
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid index.")
        return None

def get_user_choice():
    status_values = {'1': 'Availability', '2': 'InUse'}
    prompt = f"Choose Option:\n1. Availability\n2. InUse\nEnter the option number (1 or 2): "
    
    user_choice = input(prompt)
    while user_choice not in status_values.keys():
        print("Invalid choice. Please choose a valid option number.")
        user_choice = input(prompt)

    return status_values[user_choice]

if __name__ == "__main__":
    # Replace 'your_table_name' and 'your_region' with your actual DynamoDB table name and region
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        print("DynamoDB Data:", dynamodb_data)  # Print DynamoDB Data for inspection
        print_all_attributes_table(dynamodb_data)

        # Get user choice for Option
        chosen_option = get_user_choice()

        if chosen_option.lower() == 'availability':
            chosen_item = choose_cidr_block(dynamodb_data)
            if chosen_item:
                print(f"Chosen CIDRBlock: {chosen_item.get('CIDRBlock')}")
                print(f"Chosen ItemId: {chosen_item.get('ItemId')}")
        else:
            # Find the item with the chosen Status (case-insensitive)
            chosen_status = get_user_choice()

            chosen_item = next((item for item in dynamodb_data if item.get('status', '').lower() == chosen_status.lower()), None)

            if chosen_item:
                print(f"Chosen Status: {chosen_item.get('status')}")
                print(f"CIDRBlock Value: {chosen_item.get('CIDRBlock')}")
                print(f"ItemId: {chosen_item.get('ItemId')}")
            else:
                print(f"No item found with the chosen Status: {chosen_status}")

    except Exception as e:
        print(f"Error: {e}")