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
def register(username, passward):
    session = boto3.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    )
    item = session.resource("dynamodb").Table("userinfo").query(
    KeyConditionExpression=Key('username').eq(username))['Items']
    if len(item) > 0:
        return False
    else:
        session.resource("dynamodb").Table("userinfo").put_item(Item={'username': username, 'password': passward})
        return True