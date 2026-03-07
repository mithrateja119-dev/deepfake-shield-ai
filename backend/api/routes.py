import uuid
import json
import os
from fastapi import APIRouter, UploadFile, File, Depends, Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.database.sqlite import get_db, ScanResult
from backend.utils.validation import validate_file, sanitize_filename, MAX_FILE_SIZE
from backend.models.video_processing import extract_frames
from backend.models.dummy_model import run_inference
from backend.api.models import AnalyzeResponse, Explanation

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze", response_model=AnalyzeResponse)
@limiter.limit("5/minute")
async def analyze_media(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        # 1. Validation
        validate_file(file)
        
        file_bytes = await file.read()
        if len(file_bytes) > MAX_FILE_SIZE:
            return JSONResponse(status_code=400, content={"success": False, "error": "File exceeds 50MB limit"})
            
        # 2. Sanitization
        safe_name = sanitize_filename(file.filename)
        file_path = f"uploads/{uuid.uuid4()}_{safe_name}"
        
        with open(file_path, "wb") as f:
            f.write(file_bytes)
            
        # 3. Processing
        ext = safe_name.split(".")[-1].lower()
        duration = 0.0
        suspicious_frames = []
        
        if ext == "mp4":
            vid_stats = extract_frames(file_path)
            duration = vid_stats.get("duration", 0.0)
            indices = vid_stats.get("indices", [])
            first_frame = vid_stats.get("first_frame", None)
            # Pick a few specific frames as suspicious for demo purposes
            suspicious_frames = indices[1:4] if len(indices) >= 4 else indices
            
            # 4. Inference
            inference_result = run_inference(safe_name, duration, frame=first_frame)
        else:
            # Image inference
            inference_result = run_inference(safe_name, file_path=file_path)
        
        # 5. Explainability metadata
        ex_json = {
            "heatmap_base64": inference_result["heatmap_base64"],
            "suspicious_frames": suspicious_frames
        }
        
        # 6. Store
        scan_id = str(uuid.uuid4())
        db_result = ScanResult(
            scan_id=scan_id,
            filename=safe_name,
            confidence=inference_result["confidence"],
            result_label=inference_result["label"],
            timestamp=datetime.utcnow(),
            explanation_json=json.dumps(ex_json)
        )
        db.add(db_result)
        db.commit()
        
        # Cleanup
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return AnalyzeResponse(
            success=True,
            confidence=inference_result["confidence"],
            label=inference_result["label"],
            explanation=Explanation(**ex_json)
        )
        
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"success": False, "error": e.detail})
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})


@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    scans = db.query(ScanResult).order_by(ScanResult.timestamp.desc()).limit(15).all()
    history = []
    for s in scans:
        history.append({
            "scan_id": s.scan_id,
            "filename": s.filename,
            "confidence": s.confidence,
            "result_label": s.result_label,
            "timestamp": s.timestamp.isoformat()
        })
    return {"success": True, "history": history}

@router.get("/results")
def get_result(id: str, db: Session = Depends(get_db)):
    scan = db.query(ScanResult).filter(ScanResult.scan_id == id).first()
    if not scan:
        return JSONResponse(status_code=404, content={"success": False, "error": "Scan not found"})
        
    explanation = json.loads(scan.explanation_json) if scan.explanation_json else {}
    return {
        "success": True,
        "scan_id": scan.scan_id,
        "filename": scan.filename,
        "confidence": scan.confidence,
        "label": scan.result_label,
        "timestamp": scan.timestamp.isoformat(),
        "explanation": explanation
    }
