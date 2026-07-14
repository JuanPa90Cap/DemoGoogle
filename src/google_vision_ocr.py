from pathlib import Path
from typing import Any

from google.cloud import vision


class GoogleVisionOCRError(RuntimeError):
    """Raised when Google Cloud Vision cannot process an image."""


def detect_text(image_path: str | Path) -> dict[str, Any]:
    """
    Detect text in a local image using Google Cloud Vision.

    Args:
        image_path: Path to a JPG, PNG, WEBP, or other supported image.

    Returns:
        Dictionary containing the complete OCR text and individual detections.
    """
    path = Path(image_path)

    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    if not path.is_file():
        raise ValueError(f"The path is not a file: {path}")

    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=path.read_bytes())

    image_context = vision.ImageContext(
        language_hints=["en"]
    )

    response = client.text_detection(
        image=image,
        image_context=image_context,
    )

    if response.error.message:
        raise GoogleVisionOCRError(
            f"Google Cloud Vision error: {response.error.message}"
        )

    annotations = response.text_annotations

    if not annotations:
        return {
            "full_text": "",
            "detections": [],
        }

    full_text = annotations[0].description.strip()

    detections = []

    # The first annotation contains the full detected text.
    # The remaining annotations normally represent individual text elements.
    for annotation in annotations[1:]:
        vertices = [
            {
                "x": vertex.x,
                "y": vertex.y,
            }
            for vertex in annotation.bounding_poly.vertices
        ]

        detections.append(
            {
                "text": annotation.description,
                "bounding_box": vertices,
            }
        )

    return {
        "full_text": full_text,
        "detections": detections,
    }