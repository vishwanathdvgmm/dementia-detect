import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

router = APIRouter()

UPLOAD_DIR = os.path.join("backend", "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_scan(file: UploadFile = File(...)):
    """
    Accepts an image file (JPG/PNG/DICOM).
    Saves it temporarily and returns a scan_id.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    
    # Generate unique ID for this scan session
    scan_id = str(uuid.uuid4())
    filename = f"{scan_id}{ext}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {e}")
        
    return JSONResponse({
        "message": "File uploaded successfully",
        "scan_id": scan_id,
        "filename": filename,
        "file_url": f"/static/uploads/{filename}"
    })
