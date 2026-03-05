from typing import Iterator

import requests

from config import (
    LANGUAGE_MAP,
    MODELS,
    SARVAM_API_KEY,
    SARVAM_BASE_URL,
    SARVAM_CHUNK_SIZE,
)


def _chunk_text(text: str, max_chars: int = SARVAM_CHUNK_SIZE) -> list[str]:
    """Splits long text into chunks of at most mac_chars,
    trying to split by paragraphs first."""

    if len(text) <= max_chars:
        return [text]

    chunks = []
    current_chunk = ""

    # Split the recipe by paragraphs first
    paragraphs = text.split("\n\n")

    for paragraph in paragraphs:
        # If adding the next paragraph exceeds the limit, push the current chunk
        if len(current_chunk) + len(paragraph) + 2 > max_chars:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""

            # If a single paragraph is somehow huge,
            # slice it for safety
            if len(paragraph) > max_chars:
                for i in range(0, len(paragraph), max_chars):
                    chunks.append(paragraph[i : i + max_chars])
                continue

        current_chunk += paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def _translate_chunk(
    chunk: str, url: str, headers: dict[str, str], source_lang: str, target_lang: str
) -> dict:
    payload = {
        "input": chunk.strip(),
        "source_language_code": LANGUAGE_MAP.get(source_lang),
        "target_language_code": LANGUAGE_MAP.get(target_lang),
        "speaker_gender": "Male",
        "model": MODELS.get("sarvam-translate", {}).get("model_name"),
        "mode": "formal",
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code > 299:
        raise Exception(response.text)

    return response.json()


def _translate(text: str, source_lang: str, target_lang: str) -> str:
    url = f"{SARVAM_BASE_URL}/translate"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }

    # 1. Chunk the test
    chunks = _chunk_text(text)
    translated_chunks = []

    # 2. Generate translation for each chunk
    for chunk in chunks:
        if not chunk.strip():
            continue

        data = _translate_chunk(chunk, url, headers, source_lang, target_lang)
        translated_chunks.append(data["translated_text"])

    # Return stitched chunks
    return "\n\n".join(translated_chunks)


def _translate_stream(text: str, source_lang: str, target_lang: str) -> Iterator[str]:
    url = f"{SARVAM_BASE_URL}/translate"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }

    # 1. Chunk the test
    chunks = _chunk_text(text)

    for chunk in chunks:
        # Skip empty chunks
        if not chunk.strip():
            continue

        data = _translate_chunk(chunk, url, headers, source_lang, target_lang)
        yield data["translated_text"] + "\n\n"


def vernacular_to_english(text: str, source_lang: str = "bengali") -> str:
    return _translate(text, source_lang, "english")


def english_to_vernacular(text: str, target_lang: str = "bengali") -> str:
    return _translate(text, "english", target_lang)


def english_to_vernacular_stream(text: str, target_lang: str = "english"):
    return _translate_stream(text, "english", target_lang)


if __name__ == "__main__":
    text = "আমার কাছে মাংস আছে, আদা আছে, রসুন আছে, লেবু আছে।"
    english_text = vernacular_to_english(text)
    print(english_text)

    print()
    bengali_text = english_to_vernacular(english_text)
    print(bengali_text)
