import boto3

def lambda_handler(event, context):
    # Extract itemid from the event
    itemid = event.get('itemid') or event.get('ITEM_ID')

    if itemid is not None:
        dynamodb = boto3.resource('dynamodb')
        table_name = 'blankcidr'
        table = dynamodb.Table(table_name)

        try:
            # Update the table status to 'in progress' for the specified itemid
            response = table.update_item(
                Key={'itemid': itemid},
                UpdateExpression='SET #status = :status',
                ExpressionAttributeNames={'#status': 'status'},
                ExpressionAttributeValues={':status': 'in progress'}
            )

            return {
                'statusCode': 200,
                'body': f'Successfully updated status to "in progress" for itemid: {itemid}'
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': f'Error updating status for itemid {itemid}: {str(e)}'
            }
    else:
        return {
            'statusCode': 400,
            'body': 'itemid is missing in the request'
        }
