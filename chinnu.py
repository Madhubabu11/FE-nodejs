import boto3
import time

# Your DynamoDB table name and AWS region
table_name = 'blankcidr'
region = 'ap-south-1'

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

    available_cidr_items = [f"{item.get('cidr')} (S.No: {item.get('s.no')})" for item in items if item.get('status', '').lower() == 'available']

    if not available_cidr_items:
        print("No items found with the status 'Available'.")
        return

    print("DynamoDB Data: Available CIDR")
    print(", ".join(available_cidr_items))

def choose_cidr(items):
    print("\nChoose a CIDR :")
    
    available_items = [item for item in items if item.get('status', '').lower() == 'available']
    
    if not available_items:
        print("No items found with the status 'Available'.")
        return None

    for index, item in enumerate(available_items, start=1):
        print(f"{index}. {item.get('cidr')} (S.No: {item.get('s.no')})")

    try:
        choice_index = int(input("Enter the index of the CIDR you want to choose: "))
        chosen_item = available_items[choice_index - 1]
        return chosen_item
    except (ValueError, IndexError):
        print("Invalid choice. Please enter a valid index.")
        return None

def create_vpc(item, region):
    ec2 = boto3.client('ec2', region_name=region)

    try:
        cidr = item.get('cidr')
        sno = item.get('s.no')

        # Update DynamoDB item status to 'In-Progress'
        update_dynamodb_status(sno, 'In-Progress')

        # Create VPC
        response = ec2.create_vpc(CidrBlock=cidr)
        vpc_id = response['Vpc']['VpcId']

        # Print the VPC ID
        print(f"VPC created with CIDR: {cidr}, VPC ID: {vpc_id}")

        # Introduce another delay (e.g., 5 seconds) before updating the status to 'InUse'
        time.sleep(5)

        # Update DynamoDB item with VPC ID and status to 'InUse' after successful creation
        update_dynamodb_status(sno, 'InUse', vpc_id)
        print(f"VPC creation completed for CIDR: {cidr}, VPC ID: {vpc_id}")

    except Exception as e:
        # If VPC creation fails, update status back to 'Available'
        print(f"VPC creation failed with error: {str(e)}")
        update_dynamodb_status(sno, 'Available')

def update_dynamodb_status(sno, new_status, vpc_id=None):
    # Update DynamoDB item status based on 's.no'
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    update_expression = "SET #status = :new_status"
    expression_attribute_names = {'#status': 'status'}
    expression_attribute_values = {':new_status': new_status}

    if vpc_id:
        update_expression += ", #vpc_id = :vpc_id"
        expression_attribute_names['#vpc_id'] = 'vpc_id'
        expression_attribute_values[':vpc_id'] = vpc_id

    try:
        table.update_item(
            Key={'s.no': sno},
            UpdateExpression=update_expression,
            ExpressionAttributeNames=expression_attribute_names,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        print(f"Updated status for S.No {sno} to {new_status}")
        if vpc_id:
            print(f"Updated VPC ID for S.No {sno} to {vpc_id}")

    except Exception as e:
        print(f"Error updating status for S.No {sno}: {e}")

if __name__ == "__main__":
    try:
        dynamodb_data = fetch_dynamodb_data(table_name, region)
        print_available_cidr(dynamodb_data)

        chosen_item = choose_cidr(dynamodb_data)
        
        if chosen_item:
            create_vpc(chosen_item, region)

    except Exception as e:
        print(f"Error: {e}")
