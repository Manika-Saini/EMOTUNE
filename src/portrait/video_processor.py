
import os
import tempfile

import cv2

from src.portrait.cartoon_filters import create_cartoon


MAX_VIDEO_SIZE = 50 * 1024 * 1024
MAX_VIDEO_DURATION = 120


def process_video(video_bytes: bytes) -> bytes:
    """
    Process an uploaded video frame by frame using EMOTUNE's
    cartoon filter and return an MP4 video as bytes.

    Note: This initial version does not preserve audio.
    """

    if not video_bytes:
        raise ValueError("The uploaded video is empty.")

    if len(video_bytes) > MAX_VIDEO_SIZE:
        raise ValueError("Video size must be 50 MB or less.")

    input_path = None
    output_path = None
    capture = None
    writer = None

    try:
        # OpenCV needs a file path for reliable video decoding.
        with tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=False,
        ) as temp_input:
            temp_input.write(video_bytes)
            input_path = temp_input.name

        with tempfile.NamedTemporaryFile(
            suffix=".mp4",
            delete=False,
        ) as temp_output:
            output_path = temp_output.name

        capture = cv2.VideoCapture(input_path)

        if not capture.isOpened():
            raise ValueError(
                "Could not open this video. "
                "Try another MP4 video."
            )

        fps = capture.get(cv2.CAP_PROP_FPS)
        frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if width <= 0 or height <= 0:
            raise ValueError("Invalid video dimensions.")

        if fps <= 0 or fps > 120:
            fps = 25.0

        duration = frame_count / fps if frame_count > 0 else 0

        if duration > MAX_VIDEO_DURATION:
            raise ValueError(
                "Videos must be 120 seconds or shorter."
            )

        # Use a broadly supported MP4 video codec.
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

        writer = cv2.VideoWriter(
            output_path,
            fourcc,
            fps,
            (width, height),
        )

        if not writer.isOpened():
            raise RuntimeError(
                "Could not create the output video."
            )

        processed_frames = 0

        while True:
            success, frame = capture.read()

            if not success:
                break

            cartoon_frame = create_cartoon(frame)

            writer.write(cartoon_frame)
            processed_frames += 1

        capture.release()
        capture = None

        writer.release()
        writer = None

        if processed_frames == 0:
            raise ValueError(
                "No readable frames were found in this video."
            )

        with open(output_path, "rb") as output_file:
            result = output_file.read()

        if not result:
            raise RuntimeError(
                "The processed video could not be saved."
            )

        return result

    finally:
        if capture is not None:
            capture.release()

        if writer is not None:
            writer.release()

        for path in (input_path, output_path):
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except OSError:
                    pass