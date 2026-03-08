\# Deepfake Shield AI
## Demo

Upload media and analyze authenticity using Deepfake Shield AI.


Deepfake Shield AI is a web-based AI security tool designed to analyze digital media and detect potential deepfake manipulations while also verifying whether two images belong to the same person.



This project demonstrates an explainable AI architecture for media authenticity analysis.



---



\## Version



Current Version: \*\*v2\*\*



Version 2 introduces \*\*Face Verification\*\* alongside the Deepfake Detection pipeline.



---



\## Features



\### Deepfake Detection

\- Upload image or video

\- Analyze media for manipulation artifacts

\- Generate confidence score

\- Visualize suspicious areas using an explainability heatmap



\### Face Verification

\- Upload two images

\- Detect faces

\- Compare face embeddings

\- Return similarity score and match result



\### Scan History

\- Stores previous scan results in a database

\- Allows review of earlier analysis



\### API Backend

\- Built with \*\*FastAPI\*\*

\- REST-based architecture

\- Modular AI pipeline



---



\## System Architecture
User Upload

↓

Frontend Interface (HTML + JS)

↓

FastAPI Backend

↓

AI Processing Modules

├ Deepfake Detection

└ Face Verification



---



\## Project Structure

deepfake-shield-ai

│

├── backend

│ ├── api

│ ├── models

│ ├── utils

│ └── app.py

│

├── frontend

│ ├── css

│ ├── js

│ └── index.html

│

├── docs

│ ├── architecture.md

│ └── face\_verification.md

│

├── tests

│

├── requirements.txt

├── scan\_history.db

└── README.md





---



\## Installation



Clone the repository:





git clone https://github.com/mithrateja119-dev/deepfake-shield-ai





Navigate to the project:





cd deepfake-shield-ai





Install dependencies:





pip install -r requirements.txt





---



\## Run the Server





uvicorn backend.app:app --host 0.0.0.0 --port 8000





Open in browser:





http://localhost:8000





---



\## Notes



The current system uses \*\*prototype AI models for demonstration purposes\*\*.



The architecture allows integration of real models such as:



\- CNN deepfake detectors

\- EfficientNet classifiers

\- FaceNet / ArcFace embeddings



---



\## Technologies Used



\- Python

\- FastAPI

\- OpenCV

\- SQLAlchemy

\- JavaScript

\- HTML / CSS



---



\## Future Improvements



\- Integration of real deepfake detection models

\- Advanced explainability techniques

\- Media metadata analysis

\- Improved face verification models



---



\## License



MIT License







