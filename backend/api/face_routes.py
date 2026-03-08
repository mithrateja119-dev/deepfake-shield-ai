import uuid
import os
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from backend.utils.validation import validate_file, sanitize_filename
from backend.models.face_verification import verify_faces

router = APIRouter()

@router.post("/verify-face")
async def verify_face_endpoint(reference_image: UploadFile = File(...), test_image: UploadFile = File(...)):
    try:
        # Validate files
        validate_file(reference_image)
        validate_file(test_image)

        # Sanitize and prepare save paths
        ref_ext = sanitize_filename(reference_image.filename).split('.')[-1]
        test_ext = sanitize_filename(test_image.filename).split('.')[-1]

        if ref_ext not in ["jpg", "jpeg", "png"] or test_ext not in ["jpg", "jpeg", "png"]:
            return JSONResponse(status_code=400, content={"success": False, "error": "Only JPG and PNG supported for faces"})

        ref_path = f"uploads/{uuid.uuid4()}_ref.{ref_ext}"
        test_path = f"uploads/{uuid.uuid4()}_test.{test_ext}"

        # Ensure uploads dir exists
        os.makedirs("uploads", exist_ok=True)

        # Save temporarily
        with open(ref_path, "wb") as f:
            f.write(await reference_image.read())
        with open(test_path, "wb") as f:
            f.write(await test_image.read())

        try:
            # Run verification (distance calculation)
            result = verify_faces(ref_path, test_path)
            status_code = 200
            content = result
        except ValueError as e:
            # Bad requests like "No face detected"
            status_code = 400
            content = {"success": False, "error": str(e)}
        except Exception as e:
            # Unforeseen issues
            status_code = 500
            content = {"success": False, "error": f"Internal Model Error: {str(e)}"}
        finally:
            # Cleanup temporary files
            if os.path.exists(ref_path):
                os.remove(ref_path)
            if os.path.exists(test_path):
                os.remove(test_path)

        return JSONResponse(status_code=status_code, content=content)

    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"success": False, "error": e.detail})
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"success": False, "error": f"Internal Server Error: {str(e)}"})
