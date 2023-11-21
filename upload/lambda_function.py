import json
import random
import requests

def lambda_handler(event, context):
    # TODO implement
    # print("____")
    body = event.get('body')
    if body is not None:
        body = json.loads(body)
    base64Str = body["image"]
    data = {"image": base64Str}
    data = json.dumps(data)
    headers = {'Content-type': 'application/json'}
    r = requests.post("http://3.84.212.73:5001/process_image", data=data, headers=headers, timeout=300)
    
    return {
        'statusCode': 200,
        'body': json.dumps(r.json()["id"])
    }
