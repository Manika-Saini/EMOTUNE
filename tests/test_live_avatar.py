
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import cv2
import numpy as np

from src.vision.face_landmarks import FaceLandmarkTracker
from src.vision.expression_analyzer import analyze_expressions
from src.avatar.avatar_renderer import create_avatar


def main():
    tracker = FaceLandmarkTracker()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        tracker.close()
        raise RuntimeError("Could not open webcam.")

    avatar_style = "Anime Girl"
    action = "Idle"
    manual_expression = None

    print("\n===== EMOTUNE LIVE AVATAR =====")
    print("G - Anime Girl")
    print("B - Anime Boy")
    print("W - Wave")
    print("D - Dance")
    print("L - Laugh")
    print("C - Cry")
    print("T - Talk")
    print("I - Idle")
    print("A - Automatic expression")
    print("Q - Quit")
    print("===============================\n")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read webcam frame.")
                break

            frame = cv2.flip(frame, 1)

            result = tracker.detect(frame)
            detected_expression = "Neutral"

            if result["face_detected"]:
                signals = analyze_expressions(result["blendshapes"])
                detected_expression = signals["expression"]

                cv2.putText(
                    frame,
                    f"Detected: {detected_expression}",
                    (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )
            else:
                cv2.putText(
                    frame,
                    "No face detected",
                    (15, 35),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            expression = manual_expression or detected_expression

            avatar = create_avatar(
                expression=expression,
                style=avatar_style,
                action=action,
                size=(320, 400),
            )

            avatar_frame = cv2.cvtColor(
                np.array(avatar), cv2.COLOR_RGB2BGR
            )

            frame_height = 400
            frame_width = int(
                frame.shape[1] * frame_height / frame.shape[0]
            )

            camera_frame = cv2.resize(
                frame, (frame_width, frame_height)
            )

            cv2.putText(
                avatar_frame,
                avatar_style,
                (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 0, 0),
                2,
            )

            cv2.putText(
                avatar_frame,
                f"Action: {action}",
                (10, 390),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 0, 0),
                2,
            )

            combined = np.hstack([camera_frame, avatar_frame])

            cv2.imshow("EMOTUNE - Live Avatar Studio", combined)

            key = cv2.waitKey(1) & 0xFF
            key = chr(key).lower() if key != 255 else ""

            if key == "q":
                break

            elif key == "g":
                avatar_style = "Anime Girl"

            elif key == "b":
                avatar_style = "Anime Boy"

            elif key == "w":
                action = "Wave"

            elif key == "d":
                action = "Dance"

            elif key == "l":
                action = "Idle"
                manual_expression = "Laughing"

            elif key == "c":
                action = "Cry"
                manual_expression = "Sad"

            elif key == "t":
                action = "Talk"
                manual_expression = "Talking"

            elif key == "i":
                action = "Idle"
                manual_expression = None

            elif key == "a":
                action = "Idle"
                manual_expression = None

    finally:
        camera.release()
        cv2.destroyAllWindows()
        tracker.close()


if __name__ == "__main__":
    main()
