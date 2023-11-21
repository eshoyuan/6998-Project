import boto3
from boto3.dynamodb.conditions import Key

session = boto3.Session(
aws_access_key_id="AKIA3FZTEQHNARSVAVO3",
aws_secret_access_key="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",
)
item = session.resource("dynamodb").Table("ArtInfo").query(
KeyConditionExpression=Key('art_id').eq('1'))["Items"][0]

info = {"title": item["Title"], "description": item["Description"]}
