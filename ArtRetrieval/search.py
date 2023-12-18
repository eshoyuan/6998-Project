import random
from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from opensearchpy import OpenSearch, helpers
import random
import base64
import io


import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
model = models.resnet50(pretrained=True)
model = torch.nn.Sequential(*(list(model.children())[:-1]))  # Remove the last classification layer

# Check for CUDA availability for faster computation
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device)
model.eval()  # Set the model to evaluation mode
def extract_features(image_data):
    # Load a pre-trained ResNet-50 model
    # Define image transformations
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Load and preprocess the image
    image = Image.open(io.BytesIO(image_data))
    image = transform(image).unsqueeze(0)  # Add batch dimension
    image = image.to(device)

    # Extract features
    with torch.no_grad():
        features = features.view(features.size(0), -1)  # Flatten the features

    return features.cpu().numpy()


def image_to_base64(image_path):
    # Load the image using PIL
    image = Image.open(image_path)

    # Convert the image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    img_byte_arr = img_byte_arr.getvalue()

    # Encode bytes to base64 string
    base64_string = base64.b64encode(img_byte_arr)
    return base64_string.decode('utf-8')  # Convert bytes to string
# Example usage
def base2id(base64_string):
  #  print("___")
    service = 'es'
    region = 'us-west-1'
    awsauth = AWS4Auth("", "",
                    region, service)
 #   print("__2")
    # Decode the base64 string to bytes
    image_data = base64.b64decode(base64_string)
#    print("3")
    # Extract features
    features = extract_features(image_data)[0]

    client = OpenSearch(
        hosts=[{'host': "search-art2-jakzhg46lmikwfyciqxkijxmui.aos.us-west-1.on.aws", 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=300
    )

    search_query = {"query": {"knn": {"values": {"vector": features, "k": 1}}}, "size": 1}
    results = client.search(index="art-index", body=search_query)
    id = results["hits"]["hits"][0]["_source"]["id"]
    score = results["hits"]["hits"][0]["_score"]
    if score < 0.002:
        return -1
    else:
        return id

from flask import Flask, request, jsonify
import json
import base64
import io
# 导入其他所需库

import io
# 导入其他所需库

app = Flask(__name__)

# 你的其他函数（如 extract_features, image_to_base64 等）保持不变

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.get_json()

    if not data or 'image' not in data:
        return jsonify({"error": "No image data provided"}), 400

    try:
        image_base64 = data['image']

        id = base2id(image_base64)  # 确保此函数接受图像数据而不是路径
        return jsonify({"id": id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':

    app.run(debug=False, host='0.0.0.0', port=5001)