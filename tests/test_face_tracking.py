
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

import cv2

from src.vision.face_landmarks import FaceLandmarkTracker
from src.vision.expression_analyzer import analyze_expressions


def main():
    tracker = FaceLandmarkTracker()
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        tracker.close()
        raise RuntimeError(
            "Camera could not open. Check camera permissions."
        )

    print("EMOTUNE expression tracking started. Press Q to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success:
                print("Could not read camera frame.")
                break

            result = tracker.detect(frame)

            if result["face_detected"]:
                height, width = frame.shape[:2]

                for x, y, _ in result["landmarks"]:
                    px = int(x * width)
                    py = int(y * height)

                    cv2.circle(
                        frame,
                        (px, py),
                        1,
                        (0, 255, 0),
                        -1,
                    )

                signals = analyze_expressions(
                    result["blendshapes"]
                )

                cv2.putText(
                    frame,
                    f"Expression: {signals['expression']}",
                    (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )

                cv2.putText(
                    frame,
                    f"Smile: {signals['smile']:.2f}",
                    (15, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    f"Blink: {signals['blink']:.2f}",
                    (15, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

                cv2.putText(
                    frame,
                    f"Mouth: {signals['mouth_open']:.2f}",
                    (15, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 255),
                    2,
                )

            else:
                cv2.putText(
                    frame,
                    "No face detected",
                    (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow(
                "EMOTUNE - Live Expression Tracking",
                frame,
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        camera.release()
        cv2.destroyAllWindows()
        tracker.close()


if __name__ == "__main__":
    main()