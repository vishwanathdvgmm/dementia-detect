import os
from pathlib import Path
from PIL import Image
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms

class AlzheimerDataset(Dataset):
    def __init__(self, file_paths, labels, transform=None):
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        img_path = self.file_paths[idx]
        image = Image.open(img_path).convert('RGB')
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label

def get_data_splits(dataset_dir: str, test_size: float = 0.15, val_size: float = 0.15, random_state: int = 42):
    """
    Reads the dataset directory, extracts file paths and labels, 
    and splits them into train, validation, and test sets.
    """
    dataset_path = Path(dataset_dir)
    classes = sorted([d.name for d in dataset_path.iterdir() if d.is_dir()])
    class_to_idx = {cls_name: i for i, cls_name in enumerate(classes)}
    
    file_paths = []
    labels = []
    
    for cls_name in classes:
        cls_dir = dataset_path / cls_name
        for img_path in cls_dir.glob('*.jpg'):
            file_paths.append(str(img_path))
            labels.append(class_to_idx[cls_name])
            
    # First split into train+val and test
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        file_paths, labels, test_size=test_size, random_state=random_state, stratify=labels
    )
    
    # Calculate relative validation size
    relative_val_size = val_size / (1.0 - test_size)
    
    # Split train+val into train and val
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, test_size=relative_val_size, random_state=random_state, stratify=y_train_val
    )
    
    return (X_train, y_train), (X_val, y_val), (X_test, y_test), class_to_idx

def get_transforms():
    """
    Returns the torchvision transforms for preprocessing.
    Resizes to 224x224 and normalizes using ImageNet statistics.
    """
    train_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(10),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    val_test_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    
    return train_transform, val_test_transform

def get_dataloaders(dataset_dir: str, batch_size: int = 32, num_workers: int = 4):
    """
    Creates PyTorch DataLoaders for train, validation, and test sets.
    """
    (X_train, y_train), (X_val, y_val), (X_test, y_test), class_to_idx = get_data_splits(dataset_dir)
    train_transform, val_test_transform = get_transforms()
    
    train_dataset = AlzheimerDataset(X_train, y_train, transform=train_transform)
    val_dataset = AlzheimerDataset(X_val, y_val, transform=val_test_transform)
    test_dataset = AlzheimerDataset(X_test, y_test, transform=val_test_transform)
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    
    return train_loader, val_loader, test_loader, class_to_idx

if __name__ == "__main__":
    # Test the preprocessing logic
    dataset_dir = "dataset/Alzheimer_Dataset_V3/Unaugmented"
    if os.path.exists(dataset_dir):
        (X_train, y_train), (X_val, y_val), (X_test, y_test), class_to_idx = get_data_splits(dataset_dir)
        print(f"Classes: {class_to_idx}")
        print(f"Train size: {len(X_train)}, Val size: {len(X_val)}, Test size: {len(X_test)}")
        
        train_loader, val_loader, test_loader, _ = get_dataloaders(dataset_dir, batch_size=16, num_workers=0)
        images, labels = next(iter(train_loader))
        print(f"Batch image shape: {images.shape}, Labels shape: {labels.shape}")
        print(f"Image min: {images.min().item():.3f}, max: {images.max().item():.3f}")
    else:
        print(f"Dataset directory not found at: {dataset_dir}")
