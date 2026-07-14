import re
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class SerialCandidate:
    value: str
    score: int
    contains_letters: bool
    contains_digits: bool


# Generic example.
# Replace this with the actual serial-number specification from the client.
SERIAL_PATTERN = re.compile(r"^[A-Z0-9][A-Z0-9-]{4,19}$")


def normalize_serial(value: str) -> str:
    """
    Normalize OCR output without automatically replacing ambiguous characters.

    Do not automatically convert O to 0 or I to 1 because doing so could
    generate a serial number that does not exist.
    """
    value = value.upper().strip()
    value = value.replace("–", "-")
    value = value.replace("—", "-")
    value = re.sub(r"\s+", "", value)
    value = re.sub(r"[^A-Z0-9-]", "", value)

    return value.strip("-")


def calculate_candidate_score(value: str) -> int:
    score = 0

    contains_letters = bool(re.search(r"[A-Z]", value))
    contains_digits = bool(re.search(r"\d", value))

    if 5 <= len(value) <= 20:
        score += 3

    if contains_letters:
        score += 1

    if contains_digits:
        score += 2

    if contains_letters and contains_digits:
        score += 2

    if "-" in value:
        score += 1

    # Penalize values resembling common years.
    if re.fullmatch(r"(19|20)\d{2}", value):
        score -= 5

    return score


def extract_serial_candidates(
    full_text: str,
    detected_elements: list[dict],
) -> list[dict]:
    raw_values = []

    # Preserve individual OCR detections.
    for element in detected_elements:
        raw_values.append(element["text"])

    # Also inspect tokens from the complete OCR result.
    raw_values.extend(
        re.findall(r"[A-Za-z0-9][A-Za-z0-9\-–— ]{3,30}", full_text)
    )

    candidates: dict[str, SerialCandidate] = {}

    for raw_value in raw_values:
        normalized = normalize_serial(raw_value)

        if not SERIAL_PATTERN.fullmatch(normalized):
            continue

        candidate = SerialCandidate(
            value=normalized,
            score=calculate_candidate_score(normalized),
            contains_letters=bool(re.search(r"[A-Z]", normalized)),
            contains_digits=bool(re.search(r"\d", normalized)),
        )

        existing = candidates.get(normalized)

        if existing is None or candidate.score > existing.score:
            candidates[normalized] = candidate

    sorted_candidates = sorted(
        candidates.values(),
        key=lambda candidate: candidate.score,
        reverse=True,
    )

    return [asdict(candidate) for candidate in sorted_candidates]