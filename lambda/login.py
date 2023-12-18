import json
import boto3
from boto3.dynamodb.conditions import Key

def login(username, passward):
    session = boto3.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    )
    item = session.resource("dynamodb").Table("userinfo").query(
    KeyConditionExpression=Key('username').eq(username))['Items']
    if len(item) > 0 and item[0]['password'] == passward:
        return True
    else:
        return False
def lambda_handler(event, context):
    username = event["username"]
    password = event["password"]
    if(login(username, password)):
    # TODO implement
        return {
            'statusCode': 200,
            'body': json.dumps('Success')
        }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('False')
        }