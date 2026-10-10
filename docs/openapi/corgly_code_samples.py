"""UE-5: Corg.ly Onboarding API — Bhatti-ийн 5 зарчмаар засварласан code sample-ууд.

Ажиллуулах (репогийн root-оос):
    export CORGLY_API_TOKEN=your_corgly_api_token
    python docs/openapi/corgly_code_samples.py

Mock сервер дээр шалгах (CI-д ийм байдлаар ажилладаг):
    npx @stoplight/prism-cli mock docs/openapi/corgly.yaml -p 4010
    CORGLY_BASE_URL=http://127.0.0.1:4010 python docs/openapi/corgly_code_samples.py
"""
import os

import requests

# Production URL; тест хийхдээ CORGLY_BASE_URL-аар mock сервер рүү чиглүүлнэ.
BASE_URL = os.getenv("CORGLY_BASE_URL", "https://api.corg.ly/v1")

# Токеноо Corg.ly dashboard → Settings → API Tokens хэсгээс авна.
auth_token = os.getenv("CORGLY_API_TOKEN", "your_corgly_api_token")
auth_header = {"Authorization": f"Bearer {auth_token}"}


# ---------------------------------------------------------------
# 1. POST /v1/pets/upload-photo
# ---------------------------------------------------------------
# Нохойн JPEG зургийг multipart/form-data хэлбэрээр байршуулж, шинэ
# профайл үүсгэнэ. Хариунд ирэх pet_id-г дараагийн 2 хүсэлтэд ашиглана.
def upload_pet_photo(pet_photo_path: str, pet_name: str, breed: str) -> requests.Response:
    with open(pet_photo_path, "rb") as pet_photo_file:
        photo_response = requests.post(
            f"{BASE_URL}/pets/upload-photo",
            headers=auth_header,
            files={"photo": (os.path.basename(pet_photo_path), pet_photo_file, "image/jpeg")},
            data={"pet_name": pet_name, "breed": breed},
        )
    photo_response.raise_for_status()
    return photo_response


# ---------------------------------------------------------------
# 2. POST /v1/audio/translate-bark
# ---------------------------------------------------------------
# Хуцах дууны WAV бичлэгийг (16 kHz, ≤30 сек) илгээж, утгыг нь
# орчуулна. confidence нь 0–1 хооронд байх ба 0.8-аас дээш бол найдвартай.
def translate_pet_bark(bark_audio_path: str, pet_id: str) -> requests.Response:
    with open(bark_audio_path, "rb") as bark_audio_file:
        translation_response = requests.post(
            f"{BASE_URL}/audio/translate-bark",
            headers=auth_header,
            files={"audio": (os.path.basename(bark_audio_path), bark_audio_file, "audio/wav")},
            data={"pet_id": pet_id},
        )
    translation_response.raise_for_status()
    return translation_response


# ---------------------------------------------------------------
# 3. POST /v1/webhooks/subscribe
# ---------------------------------------------------------------
# Орчуулга бэлэн болох үед Corg.ly таны HTTPS endpoint руу POST илгээдэг
# webhook бүртгэнэ. Амжилттай бол 201 Created буцаана.
def subscribe_pet_webhook(pet_id: str, callback_url: str, event_names: list[str]) -> requests.Response:
    subscription_response = requests.post(
        f"{BASE_URL}/webhooks/subscribe",
        headers=auth_header,
        json={"pet_id": pet_id, "callback_url": callback_url, "events": event_names},
    )
    subscription_response.raise_for_status()
    return subscription_response


# ===============================================================
# Ашиглах жишээ: 3 хүсэлтийг дарааллаар нь ажиллуулна
# ===============================================================
if __name__ == "__main__":
    photo_response = upload_pet_photo("samples/photos/einstein_corgi.jpg", "Einstein", "Pembroke Welsh Corgi")
    pet_profile = photo_response.json()
    print(photo_response.status_code, pet_profile)
    # 200 {'pet_id': 'corgi_98231', 'pet_name': 'Einstein', 'breed': 'Pembroke Welsh Corgi',
    #      'photo_url': 'https://media.corg.ly/photos/einstein.jpg', 'status': 'uploaded'}

    translation_response = translate_pet_bark("samples/audio/einstein_bark_sample.wav", pet_profile["pet_id"])
    print(translation_response.status_code, translation_response.json())
    # 200 {'pet_id': 'corgi_98231', 'translation': 'I am hungry, please feed me.',
    #      'confidence': 0.92, 'detected_emotion': 'hungry'}

    subscription_response = subscribe_pet_webhook(
        pet_profile["pet_id"],
        "https://petcare.example.com/webhooks/corgly",
        ["translation.completed"],
    )
    print(subscription_response.status_code, subscription_response.json())
    # 201 {'webhook_id': 'hook_41ac9', 'callback_url': 'https://petcare.example.com/webhooks/corgly',
    #      'events': ['translation.completed'], 'status': 'active'}
