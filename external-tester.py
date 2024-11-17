from PIL import Image
from pathlib import Path
import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
from GarbageClassifierModel import ResNet
from GarbageClassifierModel import to_device
from GarbageClassifierModel import device
from GarbageClassifierModel import dataset

model = ResNet()

loaded_model = torch.load('garbage-classifier.pth')
loaded_model.eval()

def predict_image(img, model):
        # Convert to a batch of 1
        xb = to_device(img.unsqueeze(0), device)
        # Get predictions from model
        yb = model(xb)
        # Pick index with highest probability
        prob, preds  = torch.max(yb, dim=1)
        # Retrieve the class label
        # print(dataset)
        return dataset.classes[preds[0].item()]

def predict_external_image(image_name):
    image = Image.open(Path('./' + image_name))

    transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

    example_image = transformations(image)
    # plt.imshow(example_image.permute(1, 2, 0))
    print("The image we are testing is " + image_name)
    print("The image resembles", predict_image(example_image, loaded_model) + ".\n")

directory = './testing/'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    predict_external_image(f)