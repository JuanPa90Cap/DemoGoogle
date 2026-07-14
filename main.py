import json
import sys

from src.google_vision_ocr import detect_text
from src.serial_validator import extract_serial_candidates


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <image_path>")
        raise SystemExit(1)

    image_path = sys.argv[1]

    try:
        ocr_result = detect_text(image_path)

        candidates = extract_serial_candidates(
            full_text=ocr_result["full_text"],
            detected_elements=ocr_result["detections"],
        )

        result = {
            "image": image_path,
            "raw_text": ocr_result["full_text"],
            "serial_candidates": candidates,
            "recommended_serial": (
                candidates[0]["value"] if candidates else None
            ),
            "requires_user_confirmation": True,
        }

        print(json.dumps(result, indent=2))

    except Exception as error:
        print(
            json.dumps(
                {
                    "error": str(error),
                    "image": image_path,
                },
                indent=2,
            )
        )
        raise SystemExit(1) from error


if __name__ == "__main__":
    main()