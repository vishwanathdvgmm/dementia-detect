import os
import json
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.core.report_generator import generate_pdf_report

router = APIRouter()

HEATMAP_DIR = os.path.join("backend", "static", "heatmaps")
UPLOAD_DIR = os.path.join("backend", "static", "uploads")
REPORTS_DIR = os.path.join("backend", "static", "reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

@router.get("/report/{filename}")
async def get_report(filename: str):
    """
    Generates and returns the PDF report for a given scan filename.
    """
    # Filename might be the raw uuid + ext
    orig_image_path = os.path.join(UPLOAD_DIR, filename)
    heatmap_image_path = os.path.join(HEATMAP_DIR, f"heatmap_{filename}")
    json_path = os.path.join(HEATMAP_DIR, f"{filename}.json")
    
    if not os.path.exists(json_path) or not os.path.exists(orig_image_path):
        raise HTTPException(status_code=404, detail="Prediction data or scan not found. Please run prediction first.")
        
    try:
        with open(json_path, 'r') as f:
            prediction_data = json.load(f)
            
        pdf_filename = f"report_{filename}.pdf"
        output_path = os.path.join(REPORTS_DIR, pdf_filename)
        
        # Extract the raw ID without extension for display
        scan_id = os.path.splitext(filename)[0]
        
        # Generate the PDF
        generate_pdf_report(
            scan_id=scan_id,
            prediction_data=prediction_data,
            orig_image_path=orig_image_path,
            heatmap_image_path=heatmap_image_path,
            output_path=output_path
        )
        
        return FileResponse(
            path=output_path, 
            filename=pdf_filename,
            media_type='application/pdf'
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")
