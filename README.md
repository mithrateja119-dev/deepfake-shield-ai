This project currently uses a simulated deepfake detection model for demonstration purposes.

The architecture allows integration of real deepfake models such as:

FaceForensics++
DFDC models
CNN based artifact detectors

# Deepfake Shield AI

Deepfake Shield is an AI-powered web application designed to detect manipulated media such as deepfake images and videos.

## Features
- Image and video deepfake detection
- Explainability heatmap visualization
- Confidence scoring
- Scan history tracking
- API based backend using FastAPI

## Architecture

User Upload
      ↓
Frontend UI
      ↓
FastAPI Backend
      ↓
Deepfake Detection Pipeline
      ↓
Explainability Map
      ↓
Detection Result

## How to Run

Install dependencies:

pip install -r requirements.txt

Start the server:

uvicorn backend.app:app --host 0.0.0.0 --port 8000

Then open:

http://localhost:8000