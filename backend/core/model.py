import torch
import torch.nn as nn
from torchvision.models import efficientnet_b4, EfficientNet_B4_Weights

def get_model(num_classes=4, pretrained=True):
    """
    Loads EfficientNet-B4.
    If pretrained is True, it loads ImageNet weights and replaces the classifier head.
    """
    if pretrained:
        weights = EfficientNet_B4_Weights.IMAGENET1K_V1
        model = efficientnet_b4(weights=weights)
    else:
        model = efficientnet_b4(weights=None)
        
    # Get the number of in_features for the classifier
    in_features = model.classifier[1].in_features
    
    # Replace the classifier head for 4 classes
    # Optional: add a dropout layer for better generalization
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_features, num_classes)
    )
    
    return model

def freeze_base_model(model):
    """
    Freezes all layers except the classifier head.
    """
    for param in model.parameters():
        param.requires_grad = False
        
    # Unfreeze the classifier head
    for param in model.classifier.parameters():
        param.requires_grad = True
        
    return model

def unfreeze_last_blocks(model, num_blocks_to_unfreeze=3):
    """
    Unfreezes the last `num_blocks_to_unfreeze` blocks of EfficientNet's features.
    EfficientNet features are stored in model.features.
    """
    # First, make sure the classifier is unfrozen
    for param in model.classifier.parameters():
        param.requires_grad = True
        
    # model.features contains several sequential blocks.
    # The number of blocks varies. In EfficientNet-B4, len(model.features) is 9.
    total_blocks = len(model.features)
    
    start_unfreeze_idx = max(0, total_blocks - num_blocks_to_unfreeze)
    
    for i in range(start_unfreeze_idx, total_blocks):
        for param in model.features[i].parameters():
            param.requires_grad = True
            
    return model

if __name__ == "__main__":
    # Test model definition
    model = get_model(num_classes=4, pretrained=True)
    
    # Test freezing base
    model = freeze_base_model(model)
    trainable_params_frozen = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Trainable params (frozen base): {trainable_params_frozen:,}")
    
    # Test unfreezing last 3 blocks
    model = unfreeze_last_blocks(model, num_blocks_to_unfreeze=3)
    trainable_params_unfrozen = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Trainable params (unfrozen last 3 blocks): {trainable_params_unfrozen:,}")
    
    # Test forward pass
    dummy_input = torch.randn(2, 3, 224, 224)
    output = model(dummy_input)
    print(f"Output shape: {output.shape}")
