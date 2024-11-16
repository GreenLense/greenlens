# python imports
import os
from tqdm import tqdm

# torch imports
import torch
import torch.nn as nn
import torch.optim as optim

# helper functions for computer vision
import torchvision
import torchvision.transforms as transforms


class Trash(nn.Module):
    def __init__(self, input_shape=(32, 32), num_classes=100):
        super(Trash, self).__init__()
        self.conv1 = nn.Conv2d(3, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        units = 16 * 5 * 5
        self.fc1 = nn.Linear(units, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, num_classes)

    def forward(self, x):
        #shape_dict = {}
        c1 = nn.functional.relu(self.conv1(x))
        s2 = nn.functional.max_pool2d(c1, 2, 2)
        #shape_dict[1] = s2.shape
        c3 = nn.functional.relu(self.conv2(s2))
        s4 = nn.functional.max_pool2d(c3, 2, 2)
        #shape_dict[2] = s4.shape
        flat = torch.flatten(s4, 1)
        #shape_dict[3] = flat.shape
        f5 = nn.functional.relu(self.fc1(flat))
        #shape_dict[4] = f5.shape
        f6 = nn.functional.relu(self.fc2(f5))
        #shape_dict[5] = f6.shape
        out = self.fc3(f6)
        #shape_dict[6] = out.shape
        return out#, shape_dict
    
def train_model(model, train_loader, optimizer, criterion, epoch):
    """
    model (torch.nn.module): The model created to train
    train_loader (pytorch data loader): Training data loader
    optimizer (optimizer.*): A instance of some sort of optimizer, usually SGD
    criterion (nn.CrossEntropyLoss) : Loss function used to train the network
    epoch (int): Current epoch number
    """
    model.train()
    train_loss = 0.0
    for input, target in tqdm(train_loader, total=len(train_loader)):
        # 1) zero the parameter gradients
        optimizer.zero_grad()
        # 2) forward + backward + optimize
        output, _ = model(input)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        # Update the train_loss variable
        # .item() detaches the node from the computational graph
        train_loss += loss.item()

    train_loss /= len(train_loader)
    print('[Training set] Epoch: {:d}, Average loss: {:.4f}'.format(epoch+1, train_loss))

    return train_loss


def test_model(model, test_loader, epoch):
    model.eval()
    correct = 0
    with torch.no_grad():
        for input, target in test_loader:
            output, _ = model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

    test_acc = correct / len(test_loader.dataset)
    print('[Test set] Epoch: {:d}, Accuracy: {:.2f}%\n'.format(
        epoch+1, 100. * test_acc))

    return test_acc

