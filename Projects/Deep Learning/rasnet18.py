# -*- coding: utf-8 -*-
"""RasNet18.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17CrvcU9e4KTGsB-Vr0_ZYCH4ovzSGhhZ
"""

import torch
import torchvision
import torchvision.transforms as transforms

# Load the patternet dataset
train_dataset = torchvision.datasets.PatternNet('path/to/data', train=True, download=True, transform=transforms.ToTensor())
test_dataset = torchvision.datasets.PatternNet('path/to/data', train=False, download=True, transform=transforms.ToTensor())

# Split the dataset into training and validation sets
train_size = int(0.8 * len(train_dataset))
val_size = len(train_dataset) - train_size
train_dataset, val_dataset = torch.utils.data.random_split(train_dataset, [train_size, val_size])

# Load the pre-trained ResNet18 model and modify its last layer
model = torchvision.models.resnet18(pretrained=True)
num_classes = 4  # Replace with the actual number of classes in your dataset
model.fc = torch.nn.Linear(model.fc.in_features, num_classes)

# Define the loss function and optimizer
criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Train the model on the training set
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=32, shuffle=True)
for epoch in range(10):
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

# Evaluate the model on the validation set
val_loader = torch.utils.data.DataLoader(val_dataset, batch_size=32, shuffle=False)
correct = 0
total = 0
with torch.no_grad():
    for images, labels in val_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

accuracy = correct / total
print(f'Validation accuracy: {accuracy:.2f}')