import threading

import av
import cv2
import numpy as np
from streamlit_webrtc import VideoProcessorBase

from src.vision.face_landmarks import FaceLandmarkTracker
from src.vision.expression_analyzer import analyze_expressions
from src.avatar.avatar_renderer import create_avatar


class AvatarVideoProcessor(VideoProcessorBase):
    def __init__(self, settings):
        self.settings = settings
        self.settings_lock = threading.Lock()
        self.tracker = FaceLandmarkTracker()

    def recv(self, frame):
        camera_frame = frame.to_ndarray(format="bgr24")
        camera_frame = cv2.flip(camera_frame, 1)

        with self.settings_lock:
            style = self.settings.get("style", "Anime Girl")
            action = self.settings.get("action", "Idle")
            expression_mode = self.settings.get(
                "expression_mode", "Automatic"
            )
            manual_expression = self.settings.get(
                "manual_expression", "Happy"
            )

        detected_expression = "Neutral"
        face_detected = False

        try:
            result = self.tracker.detect(camera_frame)

            if result["face_detected"]:
                face_detected = True
                signals = analyze_expressions(result["blendshapes"])
                detected_expression = signals["expression"]

        except Exception:
            detected_expression = "Neutral"

        if expression_mode == "Manual":
            expression = manual_expression
        else:
            expression = detected_expression

            if action == "Cry":
                expression = "Sad"
            elif action == "Talk":
                expression = "Talking"

        avatar = create_avatar(
            expression=expression,
            style=style,
            action=action,
            size=(320, 400),
        )

        avatar_bgr = cv2.cvtColor(
            np.array(avatar),
            cv2.COLOR_RGB2BGR,
        )

        camera_height = 400
        camera_width = int(
            camera_frame.shape[1]
            * camera_height
            / camera_frame.shape[0]
        )

        camera_frame = cv2.resize(
            camera_frame,
            (camera_width, camera_height),
        )

        status = (
            f"Expression: {detected_expression}"
            if face_detected
            else "No face detected"
        )

        cv2.putText(
            camera_frame,
            status,
            (12, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (100, 255, 150),
            2,
        )

        combined = np.hstack([camera_frame, avatar_bgr])

        return av.VideoFrame.from_ndarray(
            combined,
            format="bgr24",
        )
