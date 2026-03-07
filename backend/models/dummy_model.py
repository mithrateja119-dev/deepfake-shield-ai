import base64
import os
import cv2
import numpy as np
from typing import Dict, Any, Optional

def generate_dummy_heatmap(image_path: Optional[str] = None, frame: Optional[np.ndarray] = None) -> str:
    """
    Generates an overlaid heatmap using OpenCV face detection.
    Real AI models use Grad-CAM to generate these maps.
    """
    if frame is not None:
        img = frame.copy()
    elif image_path and os.path.exists(image_path):
        img = cv2.imread(image_path)
    else:
        img = np.zeros((400, 400, 3), dtype=np.uint8)

    if img is None:
        img = np.zeros((400, 400, 3), dtype=np.uint8)

    height, width = img.shape[:2]
    heatmap = np.zeros((height, width, 3), dtype=np.uint8)

    # Face detection using Haar Cascades
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) > 0:
        for (x, y, w, h) in faces:
            center = (x + w//2, y + h//2)
            radius = int(max(w, h) * 0.6)
            cv2.circle(heatmap, center, radius, (0, 0, 255), -1)
    else:
        cv2.circle(heatmap, (width//2, height//2), min(width, height)//4, (0, 0, 255), -1)

    heatmap = cv2.GaussianBlur(heatmap, (101, 101), 0)
    
    # Overlay heatmap on original image
    alpha = 0.5
    overlaid = cv2.addWeighted(heatmap, alpha, img, 1 - alpha, 0)
    
    _, buffer = cv2.imencode('.jpg', overlaid)
    b64_str = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{b64_str}"

def run_inference(filename: str, video_duration: float = 0.0, file_path: str = None, frame: np.ndarray = None) -> Dict[str, Any]:
    """
    Dummy AI Inference logic to meet hackathon requirements.
    Rules:
    - filename contains "deepfake" -> confidence 0.9
    - video longer than 5 seconds -> confidence 0.65
    - otherwise -> confidence 0.15
    """
    lname = filename.lower()
    if "deepfake" in lname:
        confidence = 0.90
    elif video_duration > 5.0:
        confidence = 0.65
    else:
        confidence = 0.15

    label = "fake" if confidence > 0.5 else "real"
    heatmap = generate_dummy_heatmap(image_path=file_path, frame=frame)

    return {
        "confidence": confidence,
        "label": label,
        "heatmap_base64": heatmap
    }
