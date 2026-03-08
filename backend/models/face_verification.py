import cv2
import numpy as np

def verify_faces(ref_img_path: str, test_img_path: str) -> dict:
    """
    Lightweight OpenCV-based face verification prototype.
    Uses Haar Cascades for detection and color histograms for similarity testing.
    This creates an instant, dependency-free prototype for hackathons.
    """
    ref_img = cv2.imread(ref_img_path)
    test_img = cv2.imread(test_img_path)

    if ref_img is None:
        raise ValueError("Could not load reference image")
    if test_img is None:
        raise ValueError("Could not load test image")

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def extract_face(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4)
        
        if len(faces) == 0:
            raise ValueError("No face detected")
        if len(faces) > 1:
            raise ValueError("Multiple faces detected")
        
        # Crop to the face
        x, y, w, h = faces[0]
        face_roi = img[y:y+h, x:x+w]
        # Standardize size for comparison
        face_resized = cv2.resize(face_roi, (150, 150))
        return face_resized

    # 1. Detection Step
    try:
        ref_face = extract_face(ref_img)
    except ValueError as e:
        raise ValueError(f"Reference image error: {e}")

    try:
        test_face = extract_face(test_img)
    except ValueError as e:
        raise ValueError(f"Test image error: {e}")

    # 2. Embedding/Feature Extraction Step (Using Histograms)
    # Calculate 3D color histograms for both faces
    ref_hist = cv2.calcHist([ref_face], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    test_hist = cv2.calcHist([test_face], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])

    cv2.normalize(ref_hist, ref_hist)
    cv2.normalize(test_hist, test_hist)

    # 3. Similarity Comparison (Correlation)
    correlation = cv2.compareHist(ref_hist, test_hist, cv2.HISTCMP_CORREL)
    
    # Ensure correlation is bounded 0 to 1
    similarity = max(0.0, min(1.0, float(correlation)))

    # A baseline threshold for color histogram matches on standard faces
    match = bool(similarity > 0.65)

    return {
        "similarity_score": round(similarity, 4),
        "match": match
    }
