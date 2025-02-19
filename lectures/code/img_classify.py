import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
from torchvision import utils
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Load the VGG16 model pre-trained on ImageNet data
vgg16 = models.vgg16(pretrained=True)
vgg16.eval()  # Set the model to evaluation mode

# Define a function to classify an image
def classify_image(image_path, class_labels_file):
    # Load and preprocess the image
    img = Image.open(image_path)
    preprocess = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    img = preprocess(img).unsqueeze(0)  # Add a batch dimension

    # Perform inference
    with torch.no_grad():
        output = vgg16(img)

    # Load the class labels from the text file
    with open(class_labels_file, 'r') as f:
        class_labels = [line.strip() for line in f.readlines()]

    # Get the class label with the highest probability
    _, predicted_class_idx = torch.max(output, 1)
    predicted_class = class_labels[predicted_class_idx]

    return predicted_class