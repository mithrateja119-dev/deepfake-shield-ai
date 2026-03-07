# Detection Pipeline

This document explains the conceptual AI pipeline used in Deepfake Shield, and how to swap the current prototype dummy model with a real PyTorch model.

## Pipeline Overview

When a file hits the `POST /api/analyze` endpoint, it undergoes the following pipeline:
1. **Ingestion & Validation**: File type and size are validated.
2. **Extraction Stage**: 
   - If image: Passed directly to inference.
   - If video (`.mp4`): Processed via OpenCV. The backend steps through the video using `cv2.VideoCapture` and extracts `N` evenly spaced frames.
3. **Inference Stage**: The frames (or image) are passed to the model wrapper.
4. **Explainability Generation**: The model wrapper generates a heatmap using spatial activation maps to show *why* it made its decision.
5. **Result Aggregation**: A final confidence score and label (`fake` or `real`) are returned to the user.

## Current Dummy Model
The app currently uses a determinist dummy model (`backend/models/dummy_model.py`) optimized for hackathon demonstrations:
- Images with "deepfake" in the filename are guaranteed to return a `0.9+` confidence (FAKE).
- Videos exceeding 5 seconds in duration will return `0.65` confidence (FAKE).
- Other media heavily biases toward `0.15` (REAL).

## How to insert a real PyTorch Deepfake Detector

To upgrade from the dummy model to a state-of-the-art detector (e.g., an EfficientNet or VisionTransformer trained on the FaceForensics++ dataset):

1. **Install PyTorch**: `pip install torch torchvision`
2. **Add Model Weights**: Place your `.pt` or `.pth` weights file in `backend/models/weights/`.
3. **Update `dummy_model.py`**:
   - Rename to `inference.py`.
   - Load the model globally at app startup:
     ```python
     import torch
     model = torch.load("backend/models/weights/detector.pt")
     model.eval()
     ```
4. **Implement Transforms**: Convert the raw OpenCV frame into a typical PyTorch tensor.
   ```python
   from torchvision import transforms
   transform = transforms.Compose([
       transforms.ToTensor(),
       transforms.Resize((224, 224)),
       transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
   ])
   ```
5. **Generate Grad-CAM**: Use libraries like `pyimagesearch/gradcam` or `pytorch-grad-cam` to extract the last convolutional layer's activations and overlay it on the original image, encoding it as a Base64 string to perfectly match the existing frontend expectations.
