from opensearchpy import OpenSearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3
from opensearchpy import OpenSearch, helpers
import random
client = boto3.client('opensearch')
service = 'es'
region = 'us-west-1'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth("AKIA3FZTEQHNARSVAVO3", "52N9Ob+O/aJmTVT8YIADYsybWNi2veovWz6gug2b",
                   region, service, session_token=credentials.token)
import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from torch.nn import AdaptiveAvgPool2d

# Function to extract 2048 features using ResNet-50
def extract_features(image_path):
    # Load a pre-trained ResNet-50 model
    model = models.resnet50(pretrained=True)
    model = torch.nn.Sequential(*(list(model.children())[:-1]))  # Remove the last classification layer

    # Check for CUDA availability for faster computation
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()  # Set the model to evaluation mode

    # Define image transformations
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Load and preprocess the image
    image = Image.open(image_path)
    image = transform(image).unsqueeze(0)  # Add batch dimension
    image = image.to(device)

    # Extract features
    with torch.no_grad():
        features = model(image)
        features = AdaptiveAvgPool2d((1, 1))(features)
        features = features.view(features.size(0), -1)  # Flatten the features

    return features.cpu().numpy()
import os
# get all the image paths in ./database
def get_all_image_paths():
    image_paths = []
    for root, dirs, files in os.walk('./database'):
        for file in files:
            if file.endswith('.jpg'):
                image_paths.append(os.path.join(root, file))
    return image_paths
# Example usage (replace 'path_to_your_image.jpg' with your image path)
ids = []
features = []
from tqdm import tqdm
for path in tqdm(get_all_image_paths()[:]):
    ids.append(path.split('/')[-2])
    features.append(list(extract_features(path)[0]))

client = OpenSearch(
    hosts=[{'host': "search-art2-jakzhg46lmikwfyciqxkijxmui.aos.us-west-1.on.aws", 'port': 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=300
)

# # check whether an index exists
index_name = "art-index"
dimensions = 2048

client.indices.create(
    index_name,
    body={
        "settings": {"index.knn": True},
        "mappings": {
            "properties": {
                "values": {"type": "knn_vector", "dimension": dimensions},
            }
        },
    },
)

# # index data
vectors=[]
for i in range(len(ids)):

    vectors.append(
        {
            "_index": index_name,
            "id": ids[i],
            "values": features[i],
        }
    )

# # bulk index
helpers.bulk(client, vectors)

# client.indices.refresh(index=index_name)

