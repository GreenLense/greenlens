import os
import torch
import torchvision
from torch.utils.data import random_split
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
def main():
    data_dir  = './garbage-classification/garbage-classification/Garbage-classification'
    
    classes = os.listdir(data_dir)
    print(classes)

    from torchvision.datasets import ImageFolder
    import torchvision.transforms as transforms

    transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

    dataset = ImageFolder(data_dir, transform = transformations)

    import matplotlib.pyplot as plt

    def show_sample(img, label):
        print("Label:", dataset.classes[label], "(Class No: "+ str(label) + ")")
        plt.imshow(img.permute(1, 2, 0))

    img, label = dataset[12]
    show_sample(img, label)

    random_seed = 42
    torch.manual_seed(random_seed)

    train_ds, val_ds, test_ds = random_split(dataset, [10166, 635, 1906])
    print(len(train_ds), len(val_ds), len(test_ds))

    from torch.utils.data.dataloader import DataLoader
    batch_size = 32

    train_dl = DataLoader(train_ds, batch_size, shuffle = True, num_workers = 4, pin_memory = True)
    val_dl = DataLoader(val_ds, batch_size*2, num_workers = 4, pin_memory = True)

    from torchvision.utils import make_grid

    def show_batch(dl):
        for images, labels in dl:
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(make_grid(images, nrow = 16).permute(1, 2, 0))
            break

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
        
        def epoch_end(self, epoch, result):
            print("Epoch {}: train_loss: {:.4f}, val_loss: {:.4f}, val_acc: {:.4f}".format(
                epoch+1, result['train_loss'], result['val_loss'], result['val_acc']))

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

    model = ResNet()

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

    class DeviceDataLoader():
        """Wrap a dataloader to move data to a device"""
        def __init__(self, dl, device):
            self.dl = dl
            self.device = device
            
        def __iter__(self):
            """Yield a batch of data after moving it to device"""
            for b in self.dl: 
                yield to_device(b, self.device)

        def __len__(self):
            """Number of batches"""
            return len(self.dl)

    device = get_default_device()
    print(device)

    train_dl = DeviceDataLoader(train_dl, device)
    val_dl = DeviceDataLoader(val_dl, device)
    to_device(model, device)

    @torch.no_grad()
    def evaluate(model, val_loader):
        model.eval()
        outputs = [model.validation_step(batch) for batch in val_loader]
        return model.validation_epoch_end(outputs)

    def fit(epochs, lr, model, train_loader, val_loader, opt_func=torch.optim.SGD):
        print("Running Fit")
        history = []
        optimizer = opt_func(model.parameters(), lr)
        for epoch in range(epochs):
            print("Running epoch ", epoch)
            # Training Phase 
            model.train()
            train_losses = []
            b = 0
            for batch in train_loader:
                print("Running batch ", b, "In epoch ", epoch)
                b += 1
                loss = model.training_step(batch)
                train_losses.append(loss)
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            # Validation phase
            result = evaluate(model, val_loader)
            result['train_loss'] = torch.stack(train_losses).mean().item()
            model.epoch_end(epoch, result)
            history.append(result)
            print(result)
        return history

    model = to_device(ResNet(), device)

    print(evaluate(model, val_dl))

    num_epochs = 8
    opt_func = torch.optim.Adam
    lr = 5.5e-5

    path = 'garbage-classifier.pth'
    if not os.path.exists(path):
        history = fit(num_epochs, lr, model, train_dl, val_dl, opt_func)
        torch.save(model.state_dict(), 'garbage-classifier.pth')

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

    from PIL import Image
    from pathlib import Path

    def predict_external_image(image_name):
        image = Image.open(Path('./' + image_name))

        transformations = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor()])

        example_image = transformations(image)
        plt.imshow(example_image.permute(1, 2, 0))
        print("The image we are testing is " + image_name)
        print("The image resembles", predict_image(example_image, loaded_model) + ".\n")
    predict_external_image('./testing/alan.jpg')
    directory = './testing/'
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        predict_external_image(f)
        
if __name__ == "__main__":
    main()
