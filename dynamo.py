import sys
import boto3

def update_dynamodb_status(table_name, region, item_id, new_status):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(table_name)

    try:
        # Update the table status to 'in progress' for the specified item_id
        response = table.update_item(
            Key={'ItemId': item_id},
            UpdateExpression='SET #status = :status',
            ExpressionAttributeNames={'#status': 'status'},
            ExpressionAttributeValues={':status': new_status}
        )

        print(f'Successfully updated status to "{new_status}" for ItemId: {item_id}')
    except Exception as e:
        print(f'Error updating status for ItemId {item_id}: {str(e)}')

if __name__ == "__main__":
    # Replace 'your_table_name' and 'your_region' with your actual DynamoDB table name and region
    table_name = 'blankcidr'
    region = 'ap-south-1'

    try:
        item_id = sys.argv[1]
        new_status = 'in progress'

        update_dynamodb_status(table_name, region, item_id, new_status)

    except IndexError:
        print("Error: Item ID not provided. Please provide Item ID as a command-line argument.")
    except Exception as e:
        print(f"Error: {e}")
