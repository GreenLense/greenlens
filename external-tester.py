import os
import torch
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data.dataloader import DataLoader
from torchvision.utils import make_grid
from torchvision.datasets import ImageFolder
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path
import sys

def main(fileName):
    data_dir  = './garbage-classification/garbage-classification/Garbage-classification'

    transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

    dataset = ImageFolder(data_dir, transform = transformations)

    def accuracy(outputs, labels):
        _, preds = torch.max(outputs, dim=1)
        return torch.tensor(torch.sum(preds == labels).item() / len(preds))

    class ImageClassificationBase(nn.Module):
        def training_step(self, batch):
            images, labels = batch 
            out = self(images)                  # Generate predictions
            loss = F.cross_entropy(out, labels) # Calculate loss
            return loss
        
        def validation_step(self, batch):
            images, labels = batch 
            out = self(images)                    # Generate predictions
            loss = F.cross_entropy(out, labels)   # Calculate loss
            acc = accuracy(out, labels)           # Calculate accuracy
            return {'val_loss': loss.detach(), 'val_acc': acc}
            
        def validation_epoch_end(self, outputs):
            batch_losses = [x['val_loss'] for x in outputs]
            epoch_loss = torch.stack(batch_losses).mean()   # Combine losses
            batch_accs = [x['val_acc'] for x in outputs]
            epoch_acc = torch.stack(batch_accs).mean()      # Combine accuracies
            return {'val_loss': epoch_loss.item(), 'val_acc': epoch_acc.item()}

    class ResNet(ImageClassificationBase):
        def __init__(self):
            super().__init__()
            # Use a pretrained model
            self.network = models.resnet50(pretrained=True)
            # Replace last layer
            num_ftrs = self.network.fc.in_features
            self.network.fc = nn.Linear(num_ftrs, len(dataset.classes))
        
        def forward(self, xb):
            return torch.sigmoid(self.network(xb))

    def get_default_device():
        """Pick GPU if available, else CPU"""
        if torch.cuda.is_available():
            return torch.device('cuda')
        else:
            return torch.device('cpu')
        
    def to_device(data, device):
        """Move tensor(s) to chosen device"""
        if isinstance(data, (list,tuple)):
            return [to_device(x, device) for x in data]
        return data.to(device, non_blocking=True)

    device = get_default_device()

    model = to_device(ResNet(), device)

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

    loaded_model = to_device(ResNet(), device)
    loaded_model.load_state_dict(torch.load('garbage-classifier.pth', weights_only=True))
    loaded_model.eval()

    def predict_external_image(image_name):
        image = Image.open(Path('./' + image_name))

        transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

        example_image = transformations(image)
        plt.imshow(example_image.permute(1, 2, 0))
        print("The image we are testing is " + image_name)
        print("The image resembles", predict_image(example_image, loaded_model) + ".\n")
    
    # predict image given
    predict_external_image('./testing/' + fileName)
        
if __name__ == "__main__":
    main(sys.argv[1])