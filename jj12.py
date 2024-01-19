import boto3
import sys
import json
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
    field_names_set = set(['ItemId', 'status', 'CIDRBlock'])

    for item in items:
        field_names_set.update(item.keys())

    table.field_names = list(field_names_set)

    for item in items:
        row_values = [item.get('ItemId'), item.get('status'), item.get('CIDRBlock')] + [item.get(attribute) for attribute in field_names_set if attribute not in ['ItemId', 'status', 'CIDRBlock']]
        table.add_row(row_values)

    print(table)

def choose_cidr_block(items):
    print("\nChoose a CIDRBlock and ItemId:")
    
    availability_items = [item for item in items if item.get('status', '').lower() == 'availability']
    
    if not availability_items:
        print("No items found with the status 'Availability'.")
        return None

    for index, item in enumerate(availability_items, start=1):
        print(f"{index}. CIDRBlock: {item.get('CIDRBlock')}, ItemId: {item.get('ItemId')}")

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

def fetch_dynamodb_data(table_name, region):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

# Add your AWS credentials here
    aws_access_key = "AKIAXGT5ACVCT6YWAK5E"
    aws_secret_key = "sYXnfjxG2CqxbGolRjqhh0qEbzd7fMjJrWvNgK2o"

    # Use the provided credentials
    credentials = boto3.Session(aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key).get_credentials()
    # Print AWS credentials
    credentials = boto3.Session().get_credentials()
    print("AWS Access Key:", credentials.access_key)
    print("AWS Secret Key:", credentials.secret_key)

    response = table.scan()
    return response['Items']

def generate_cidr_choices():
    dynamodb_data = fetch_dynamodb_data('blankcidr', 'ap-south-1')

    cidr_choices = [{'value': f"{item['CIDRBlock']}:{item['ItemId']}", 'name': f"{item['CIDRBlock']} - {item['ItemId']}"} for item in dynamodb_data]

    print(json.dumps(cidr_choices))

if __name__ == "__main__":
    args = sys.argv[1:]

    if args and args[0] == "generate_cidr_choices":
        generate_cidr_choices()
    else:
        table_name = 'blankcidr'
        region = 'ap-south-1'

        try:
            dynamodb_data = fetch_dynamodb_data(table_name, region)
            print("DynamoDB Data:")
            print_all_attributes_table(dynamodb_data)

            chosen_option = get_user_choice()

            if chosen_option.lower() == 'availability':
                chosen_item = choose_cidr_block(dynamodb_data)
                if chosen_item:
                    print(f"Chosen CIDRBlock: {chosen_item.get('CIDRBlock')}")
                    print(f"Chosen ItemId: {chosen_item.get('ItemId')}")
            else:
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
