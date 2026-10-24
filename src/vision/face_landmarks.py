
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MODEL_PATH = PROJECT_ROOT / "models" / "face_landmarker.task"


class FaceLandmarkTracker:
    def __init__(self):
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Face Landmarker model not found: {MODEL_PATH}"
            )

        options = vision.FaceLandmarkerOptions(
            base_options=python.BaseOptions(
                model_asset_path=str(MODEL_PATH)
            ),
            running_mode=vision.RunningMode.IMAGE,
            num_faces=1,
            output_face_blendshapes=True,
            output_facial_transformation_matrixes=True,
        )

        self.detector = vision.FaceLandmarker.create_from_options(
            options
        )

    def detect(self, frame_bgr: np.ndarray) -> dict:
        if (
            frame_bgr is None
            or not isinstance(frame_bgr, np.ndarray)
            or frame_bgr.size == 0
        ):
            raise ValueError("Please provide a valid image.")

        rgb_frame = cv2.cvtColor(
            frame_bgr,
            cv2.COLOR_BGR2RGB,
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=np.ascontiguousarray(rgb_frame),
        )

        result = self.detector.detect(mp_image)

        if not result.face_landmarks:
            return {
                "face_detected": False,
                "landmarks": [],
                "blendshapes": {},
            }

        landmarks = [
            (point.x, point.y, point.z)
            for point in result.face_landmarks[0]
        ]

        blendshapes = {}

        if result.face_blendshapes:
            blendshapes = {
                item.category_name: float(item.score)
                for item in result.face_blendshapes[0]
            }

        return {
            "face_detected": True,
            "landmarks": landmarks,
            "blendshapes": blendshapes,
        }

    def close(self):
        self.detector.close()