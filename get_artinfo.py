import boto3
from boto3.dynamodb.conditions import Key

session = boto3.Session(
aws_access_key_id="",
aws_secret_access_key="",
)
id="66"
item = session.resource("dynamodb").Table("ArtInfo").query(
KeyConditionExpression=Key('art_id').eq(id))["Items"][0]

info = {"title": item["Title"], "url": item["Image URL"], "description": item["Description"]}
print(info)
