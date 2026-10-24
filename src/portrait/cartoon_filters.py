
import cv2
import numpy as np


def create_cartoon(image: np.ndarray) -> np.ndarray:
    """Convert a BGR image into a cartoon-style image."""

    if image is None or image.size == 0:
        raise ValueError("Input image is empty.")

    if image.ndim != 3 or image.shape[2] != 3:
        raise ValueError("Expected a 3-channel BGR image.")

    # Smooth colors while preserving major boundaries.
    smooth = cv2.bilateralFilter(image, 9, 200, 200)

    # Create a simplified edge mask.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 7)

    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        2,
    )

    # Combine smooth colors and dark cartoon outlines.
    edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cartoon = cv2.bitwise_and(smooth, edges)

    return cartoon