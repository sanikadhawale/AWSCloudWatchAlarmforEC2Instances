import boto3

def lambda_handler(event, context):
    # Extract the alarm details from the event
    alarm_name = event['detail']['alarmName']
    alarm_description = event['detail']['alarmDescription']
    alarm_state = event['detail']['state']['value']
    alarm_timestamp = event['time']

    # Create a DynamoDB client
    dynamodb = boto3.client('dynamodb')

    # Store the alarm data in DynamoDB
    table_name = 'CloudwatchAlarmDetails'  # Replace with your DynamoDB table name
    item = {
        'AlarmName': {'S': alarm_name},
        'AlarmDescription': {'S': alarm_description},
        'AlarmState': {'S': alarm_state},
        'Timestamp': {'S': alarm_timestamp}
    }

    try:
        response = dynamodb.put_item(TableName=table_name, Item=item)
        print(f"Data stored in DynamoDB. Response: {response}")
    except Exception as e:
        print(f"Error storing data in DynamoDB: {e}")
