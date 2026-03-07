import cv2
import os
import numpy as np

def extract_frames(video_path: str, max_frames: int = 10) -> dict:
    """
    Extracts evenly spaced frames from a video.
    Returns indices, duration, and the first frame.
    """
    if not os.path.exists(video_path):
        return {}

    try:
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        duration = total_frames / fps if fps and fps > 0 else 0

        extracted_indices = []
        first_frame = None

        if total_frames > 0:
            step = max(1, total_frames // max_frames)
            for i in range(0, total_frames, step):
                if len(extracted_indices) >= max_frames:
                    break
                
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                if ret:
                    extracted_indices.append(i)
                    if first_frame is None:
                        first_frame = frame
                    
        cap.release()
        return {"indices": extracted_indices, "duration": duration, "total_frames": total_frames, "first_frame": first_frame}
    except Exception as e:
        print(f"Video extraction error: {e}")
        return {"indices": [], "duration": 0.0, "total_frames": 0}
