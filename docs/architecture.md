# Deepfake Shield Architecture

This document describes the high-level architecture of the Deepfake Shield web application, built for competition and hackathon standards.

## Tech Stack Overview
- **Backend**: Python 3 with FastAPI. Chosen for high performance, asynchronous request handling, and deep learning framework compatibility (PyTorch/TensorFlow).
- **Frontend**: Vanilla HTML5, CSS3, and JavaScript. Avoids heavy frameworks to maintain a lightweight, fast, and easily understandable codebase.
- **Database**: SQLite via SQLAlchemy. An embedded, serverless database ideal for local hackathon deployments and prototyping.

## Directory Structure
```
deepfake_shield/
│
├── backend/                  # Python FastAPI Backend
│   ├── app.py                # Main application entry point and CORS setup
│   ├── api/
│   │   ├── routes.py         # REST API endpoints (Analyze, History)
│   │   └── models.py         # Pydantic schemas for request/response typing
│   ├── database/
│   │   └── sqlite.py         # SQLAlchemy ORM definitions
│   ├── models/
│   │   ├── dummy_model.py    # Placeholder AI inference model
│   │   └── video_processing.py # OpenCV video frame extraction
│   └── utils/
│       ├── security.py       # Rate limiting using SlowAPI
│       └── validation.py     # File size and mime-type security
│
├── frontend/                 # Client-side UI
│   ├── index.html            # Main interface
│   ├── css/styles.css        # Premium styling with dark mode
│   └── js/app.js             # API communications and UI logic
│
├── docs/                     # Project Documentation
├── tests/                    # Pytest test suites
└── uploads/                  # Temporary cache for uploaded media
```

## Security & Reliability
1. **Rate Limiting**: `SlowAPI` intercepts requests at the router level, limiting `POST /api/analyze` to 5 requests per minute per IP to prevent DoS attacks.
2. **Strict Validation**: All files are checked against allowed extensions (`.jpg`, `.png`, `.mp4`) *and* expected MIME types to prevent malicious code execution.
3. **Payload Limits**: Max file size is capped at 50MB before the payload is loaded entirely into memory.
4. **Filename Sanitization**: Uploaded files use securely sanitized filenames appended with UUIDs to prevent directory traversal attacks.
