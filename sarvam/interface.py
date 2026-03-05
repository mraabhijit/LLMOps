from sarvam.stt import transcribe_audio
from sarvam.translate import english_to_vernacular, vernacular_to_english


def process_voice_request(audio_bytes: bytes, language: str = "english") -> dict:
    data = transcribe_audio(audio_bytes, language)
    vernacular_recipe = process_text_request(data["text"], language)
    return {
        "text": vernacular_recipe,
        "language_code": data["language_code"],
    }


def process_text_request(text: str, language: str = "english") -> dict:
    translated_text_in_english = vernacular_to_english(text, language)
    recipe_placeholder = f"Here is a recipe for {translated_text_in_english}..."

    recipe_translated_to_vernacular = english_to_vernacular(
        recipe_placeholder, language
    )
    return {"text": recipe_translated_to_vernacular}


if __name__ == "__main__":
    from pathlib import Path

    audio_file = Path("audio/test.wav")
    with open(audio_file, "rb") as f_in:
        audio_bytes = f_in.read()

    print(process_voice_request(audio_bytes, "bengali"))
