import os
import torch
import torch.nn.functional as F
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from PIL import Image

from backend.api.deps import get_inference_model, get_inference_transforms, get_device
from backend.core.gradcam import generate_heatmap

router = APIRouter()

class PredictRequest(BaseModel):
    filename: str
    
HEATMAP_DIR = os.path.join("backend", "static", "heatmaps")
os.makedirs(HEATMAP_DIR, exist_ok=True)
UPLOAD_DIR = os.path.join("backend", "static", "uploads")

# Map index to class
CLASSES = ['MildDemented', 'ModerateDemented', 'NonDemented', 'VeryMildDemented']

@router.post("/predict")
async def predict_scan(request: PredictRequest):
    """
    Runs preprocessing, model inference, and GradCAM heatmap generation.
    Returns JSON with probabilities and the heatmap URL.
    """
    file_path = os.path.join(UPLOAD_DIR, request.filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Scan file not found")
        
    try:
        # 1. Load and preprocess image
        orig_img = Image.open(file_path).convert('RGB')
        transform = get_inference_transforms()
        input_tensor = transform(orig_img).unsqueeze(0)
        
        # 2. Inference
        device = get_device()
        model = get_inference_model()
        input_tensor = input_tensor.to(device)
        
        with torch.no_grad():
            output = model(input_tensor)
            probabilities = F.softmax(output, dim=1)[0].cpu().numpy().tolist()
            pred_idx = torch.argmax(output, 1).item()
            pred_class = CLASSES[pred_idx]
            confidence = probabilities[pred_idx]
            
        # 3. Generate GradCAM Heatmap
        # Ensure model is in eval mode with requires_grad=True on target layers
        # GradCAM library does this internally, but gradients are needed for input_tensor
        input_tensor.requires_grad_(True)
        heatmap_img = generate_heatmap(model, input_tensor, orig_img, target_class=None)
        
        # Save heatmap
        heatmap_filename = f"heatmap_{request.filename}"
        heatmap_path = os.path.join(HEATMAP_DIR, heatmap_filename)
        heatmap_img.save(heatmap_path)
        
        # Format response
        class_probs = {CLASSES[i]: round(prob, 4) for i, prob in enumerate(probabilities)}
        response_data = {
            "predicted_class": pred_class,
            "confidence": round(confidence, 4),
            "probabilities": class_probs,
            "heatmap_url": f"/static/heatmaps/{heatmap_filename}"
        }
        
        # Save prediction data for PDF generation later
        import json
        with open(os.path.join(HEATMAP_DIR, f"{request.filename}.json"), 'w') as f:
            json.dump(response_data, f)
        
        return JSONResponse(response_data)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")
