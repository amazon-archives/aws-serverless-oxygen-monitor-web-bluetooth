import os
import json
import boto3

tableName = os.environ.get('ACCESS_TABLE_NAME')

def handler(event, context):
  client = boto3.resource('dynamodb')

  table = client.Table(tableName)

  print(table.table_status)
  print(event)

  user_data = event['requestContext']['authorizer']['claims']
  timestamp = event['requestContext']['requestTimeEpoch']
  body = json.loads(event['body'])
  
  if body['action'] == 'share':
    table.put_item(Item= {
      'username': body['shared_user'],
      'shared_user': user_data['cognito:username']
      })
  
  if body['action'] == 'revoke':
    table.delete_item(Key= {
      'username': body['shared_user'],
      'shared_user': user_data['cognito:username'],
      })

  response = {
    "statusCode": 200,
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
    }
  }
  return response