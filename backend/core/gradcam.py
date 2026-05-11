import torch
import numpy as np
import cv2
from PIL import Image
from pytorch_grad_cam import GradCAM
from pytorch_grad_cam.utils.image import show_cam_on_image

def get_target_layer(model):
    """
    Returns the target layer for GradCAM.
    For EfficientNet-B4, the features are in model.features.
    We target the last convolutional block for the best high-level features.
    """
    # model.features contains the sequential blocks.
    # We take the last block's last normalization or activation layer,
    # or just the entire last block.
    # In torchvision's EfficientNet, features[-1] is typically a Conv2dNormActivation block.
    return [model.features[-1]]

def generate_heatmap(model, input_tensor, original_image, target_class=None):
    """
    Generates a GradCAM heatmap and overlays it on the original image.
    
    Args:
        model: PyTorch model (EfficientNet-B4).
        input_tensor: Preprocessed tensor image of shape (1, 3, 224, 224).
        original_image: PIL Image or numpy array (RGB) of the original image.
        target_class: Optional class index to generate the heatmap for. 
                      If None, the highest scoring category is used.
                      
    Returns:
        heatmap_overlay: PIL Image containing the original image with the heatmap overlaid.
    """
    target_layers = get_target_layer(model)
    
    # Initialize GradCAM
    # use_cuda will automatically move the model/tensor if needed, 
    # but since our tensors are already managed by the caller, we match their device.
    cam = GradCAM(model=model, target_layers=target_layers)
    
    # Generate the grayscale CAM (Shape: 224x224)
    # Note: target_category can be specified. If None, it uses the argmax of the model output.
    grayscale_cam = cam(input_tensor=input_tensor, targets=target_class)[0, :]
    
    # Convert original image to float32 numpy array in range [0, 1] for show_cam_on_image
    if isinstance(original_image, Image.Image):
        # Resize original image to match tensor size if necessary
        original_image = original_image.resize((224, 224))
        rgb_img = np.array(original_image, dtype=np.float32) / 255.0
    elif isinstance(original_image, np.ndarray):
        rgb_img = cv2.resize(original_image, (224, 224))
        if rgb_img.max() > 1.0:
            rgb_img = rgb_img.astype(np.float32) / 255.0
    else:
        raise ValueError("original_image must be a PIL Image or numpy array")

    # Overlay the heatmap (50% opacity = image_weight 0.5)
    # The default colormap is cv2.COLORMAP_JET
    visualization = show_cam_on_image(rgb_img, grayscale_cam, use_rgb=True, image_weight=0.5)
    
    # Convert back to PIL Image
    heatmap_overlay = Image.fromarray(visualization)
    
    return heatmap_overlay

if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.abspath('..'))
    
    from backend.core.model import get_model
    
    # Dummy test to ensure imports and initialization work
    model = get_model(num_classes=4, pretrained=False)
    target_layers = get_target_layer(model)
    print(f"Target layer selected: {target_layers[0]}")
