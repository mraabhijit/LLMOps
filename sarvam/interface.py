from typing import Iterator

from pipeline import run_pipeline
from sarvam.stt import transcribe_audio
from sarvam.translate import (
    english_to_vernacular,
    english_to_vernacular_stream,
    vernacular_to_english,
)


def process_voice_request(audio_bytes: bytes, language: str = "english") -> dict:
    data = transcribe_audio(audio_bytes, language)
    recipe_response = process_text_request(data["text"], language)
    return {
        "text": recipe_response["text"],
        "language_code": data["language_code"],
        "is_safe": recipe_response["is_safe"],
        "warnings": recipe_response["warnings"],
    }


def process_voice_request_stream(
    audio_bytes: bytes, language: str = "english"
) -> Iterator[dict]:
    data = transcribe_audio(audio_bytes, language)
    yield {
        "type": "metadata",
        "language_code": data["language_code"],
    }

    for chunk in process_text_request_stream(data["text"], language):
        yield {
            "type": "chunk",
            "is_safe": chunk.get("is_safe", ""),
            "warnings": chunk.get("warnings", []),
            "error": chunk.get("error", ""),
            "text": chunk.get("text", ""),
        }


def process_text_request(text: str, language: str = "english") -> dict:
    is_english = language.lower() == "english"

    # Skip input translation if already English
    english_input = text if is_english else vernacular_to_english(text, language)

    recipe_response = run_pipeline(
        english_input=english_input,
        allergies=[],
    )
    if recipe_response["error"]:
        return {
            "text": f"ERROR: {recipe_response['error']}",
            "is_safe": recipe_response["is_safe"],
            "warnings": recipe_response["warnings"],
        }

    recipe = recipe_response["recipe"]

    # Skip output translation if target is English
    output_text = recipe if is_english else english_to_vernacular(recipe, language)
    return {
        "text": output_text,
        "is_safe": recipe_response["is_safe"],
        "warnings": recipe_response["warnings"],
    }


def process_text_request_stream(text: str, language: str = "english") -> Iterator[dict]:
    is_english = language.lower() == "english"

    # Skip input translation if already English
    english_input = text if is_english else vernacular_to_english(text, language)

    recipe_response = run_pipeline(
        english_input=english_input,
        allergies=[],
    )
    yield {
        "type": "metadata",
        "is_safe": recipe_response["is_safe"],
        "warnings": recipe_response["warnings"],
        "error": recipe_response["error"],
    }
    if recipe_response["error"]:
        yield {
            "type": "response",
            "text": f"ERROR: {recipe_response['error']}",
        }
        return

    if is_english:
        # Stream the English recipe directly without translation
        yield {
            "type": "chunk",
            "text": recipe_response["recipe"],
        }
    else:
        for chunk in english_to_vernacular_stream(recipe_response["recipe"], language):
            yield {
                "type": "chunk",
                "text": chunk,
            }


if __name__ == "__main__":
    from pathlib import Path

    audio_file = Path("audio/test.wav")
    with open(audio_file, "rb") as f_in:
        audio_bytes = f_in.read()

    stream = process_voice_request_stream(audio_bytes, "bengali")
    for item in stream:
        print(item)
