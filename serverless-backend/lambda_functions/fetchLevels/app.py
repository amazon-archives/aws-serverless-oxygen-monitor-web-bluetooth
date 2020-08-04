import os
import json, decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

tableName = os.environ.get('LEVELS_TABLE_NAME')

def handler(event, context):
  client = boto3.resource('dynamodb')

  table = client.Table(tableName)

  print(table.table_status)
  print(event)

  user_data = event['requestContext']['authorizer']['claims']

  res = table.scan(FilterExpression=Key('username').eq(user_data['cognito:username']))

  data = res['Items']

  while 'LastEvaluatedKey' in res:
      res = table.scan(ExclusiveStartKey=res['LastEvaluatedKey'])
      data.extend(res['Items'])

  def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError
  
  data = json.dumps(data, default=decimal_default)
  
  oxygen_levels = []
  timestamps = []
  pulse_rates = []

  for entry in json.loads(data): 
    oxygen_levels.append(entry['oxygen_level'])
    timestamps.append(entry['timestamp'])
    pulse_rates.append(entry['bpm'])

  body = {
    'oxygen_levels': oxygen_levels,
    'timestamps': timestamps,
    'pulse_rates': pulse_rates
  }

  response = {
    "statusCode": 200,
    "body": json.dumps(body),
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "*"
    }
  }

  print(response)
  return response