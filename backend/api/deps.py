import torch
import os
from backend.core.model import get_model
from backend.core.preprocessing import get_transforms

_model = None

def get_device():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def get_inference_model():
    """
    Loads and caches the trained EfficientNet-B4 model for inference.
    """
    global _model
    if _model is None:
        device = get_device()
        print(f"Loading model on {device}...")
        
        # Initialize model architecture
        model = get_model(num_classes=4, pretrained=False)
        
        # Load weights
        weights_path = os.path.join("backend", "models", "efficientnet_adni.pth")
        if not os.path.exists(weights_path):
            raise FileNotFoundError(f"Model weights not found at {weights_path}. Please complete Phase 2.")
            
        model.load_state_dict(torch.load(weights_path, map_location=device))
        model.to(device)
        model.eval() # Set to evaluation mode
        
        _model = model
        print("Model loaded successfully.")
        
    return _model

def get_inference_transforms():
    """
    Returns the transforms needed for preprocessing a single image for inference.
    """
    _, val_test_transform = get_transforms()
    return val_test_transform
