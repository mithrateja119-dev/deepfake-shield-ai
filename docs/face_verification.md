# Face Verification Module

Deepfake Shield V2 implements a secure facial verification module utilizing the `face_recognition` library.
This module verifies whether two distinct images contain the exact same person. It does **not** identify the person, rather it calculates the similarity distance between their biometric facial embeddings.

## Pipeline Architecture

1. **Uploads**: The endpoint `POST /verify-face` expects a `reference_image` and `test_image`.
2. **Detection**: OpenCV and DLIB models are utilized through `face_recognition` to scan for human faces. If multiple faces exist or none are found, the pipeline raises an HTTP 400 error.
3. **Embeddings (Encodings)**: Deep learning creates a 128-dimensional embedding space representing the geometric markers (eyes, jawline, nose) of the detected face invariant to lighting or angle.
4. **Euclidean Distance**: We compute the distance between the two vectors.
5. **Similarity Check**: Measurements under `0.6` dictate a strict biometric match. The score is returned to the user alongside the Boolean `match: true` result.

## Example Usage

```bash
curl -X POST "http://localhost:8000/verify-face" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "reference_image=@john_doe_id.jpg" \
  -F "test_image=@john_doe_webcam.png"
```

**Response**:
```json
{
  "similarity_score": 0.89,
  "match": true
}
```
