import requests

from config import LANGUAGE_MAP, MODELS, SARVAM_API_KEY, SARVAM_BASE_URL


def transcribe_audio(raw_audio_bytes: bytes, language: str = "bengali"):
    url = f"{SARVAM_BASE_URL}/speech-to-text"
    headers = {"api-subscription-key": SARVAM_API_KEY}
    request = {
        "file": ("audio.wav", raw_audio_bytes, "audio/wav"),
    }
    response = requests.post(
        url=url,
        headers=headers,
        files=request,
        data={
            "model": MODELS.get("sarvam-audio", {}).get("model_name"),
            "language_code": LANGUAGE_MAP.get(language),
        },
    )
    if response.status_code > 299:
        raise Exception(response.text)

    data = response.json()

    return {
        "text": data["transcript"],
        "language_code": data["language_code"],
    }


if __name__ == "__main__":
    from pathlib import Path

    audio_file = Path("audio/test.wav")
    with open(audio_file, "rb") as f_in:
        audio_bytes = f_in.read()

    response = transcribe_audio(audio_bytes)
    print(response)
