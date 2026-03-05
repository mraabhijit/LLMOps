import requests

from config import LANGUAGE_MAP, MODELS, SARVAM_API_KEY, SARVAM_BASE_URL


def _translate(text: str, source_lang: str, target_lang: str) -> str:
    url = f"{SARVAM_BASE_URL}/translate"
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "source_language_code": LANGUAGE_MAP.get(source_lang),
        "target_language_code": LANGUAGE_MAP.get(target_lang),
        "speaker_gender": "Male",
        "model": MODELS.get("sarvam-translate", {}).get("model_name"),
        "mode": "formal",
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code > 299:
        raise Exception(response.text)

    data = response.json()
    return data["translated_text"]


def vernacular_to_english(text: str, source_lang: str = "bengali") -> str:
    return _translate(text, source_lang, "english")


def english_to_vernacular(text: str, target_lang: str = "bengali") -> str:
    return _translate(text, "english", target_lang)


if __name__ == "__main__":
    text = "আমার কাছে মাংস আছে, আদা আছে, রসুন আছে, লেবু আছে।"
    english_text = vernacular_to_english(text)
    print(english_text)

    print()
    bengali_text = english_to_vernacular(english_text)
    print(bengali_text)
