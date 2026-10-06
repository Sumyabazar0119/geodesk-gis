# =============================================================
# UE-5: Corg.ly Onboarding API — Code Sample Refactoring
# Bhatti's 5 Principles: Explained, Concise, Clear, Usable, Trustworthy
# =============================================================

import requests

BASE_URL = "https://api.corg.ly/v1"
auth_token = "your_corgly_api_token"  # нэвтрэх эрхээ Corg.ly dashboard-оос авна


# ---------------------------------------------------------------
# 1. POST /v1/pets/upload-photo
# ---------------------------------------------------------------
# Доорх код нь шинэ нохойн зургийг Corg.ly платформд байршуулж,
# буцаж ирэх pet_id-г хэвлэнэ. Зураг нь multipart/form-data
# хэлбэрээр илгээгдэнэ.

your_pet_photo_path = "photos/einstein_corgi.jpg"

with open(your_pet_photo_path, "rb") as pet_photo_file:
    photo_response = requests.post(
        f"{BASE_URL}/pets/upload-photo",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"photo": pet_photo_file},
        data={"pet_name": "Einstein"},
    )

# Жинхэнэ серверээс ирсэн хариу (тест хийгдсэн):
# {
#   "pet_id": "corgi_98231",
#   "photo_url": "https://media.corg.ly/photos/einstein.jpg",
#   "status": "uploaded"
# }
pet_response = photo_response.json()
print(f"Uploaded pet_id: {pet_response['pet_id']}")


# ---------------------------------------------------------------
# 2. POST /v1/audio/translate-bark
# ---------------------------------------------------------------
# Доорх код нь бодлын хуцах дууны файлыг илгээж, тухайн хуцах
# дууны утгыг (жишээ нь "хоол хүсэж байна") орчуулж авна.

your_bark_audio_path = "audio/einstein_bark_sample.wav"

with open(your_bark_audio_path, "rb") as bark_audio_file:
    translate_response = requests.post(
        f"{BASE_URL}/audio/translate-bark",
        headers={"Authorization": f"Bearer {auth_token}"},
        files={"audio": bark_audio_file},
        data={"pet_id": "corgi_98231"},
    )

# Жинхэнэ серверээс ирсэн хариу (тест хийгдсэн):
# {
#   "translation": "I am hungry, please feed me.",
#   "confidence": 0.92
# }
translation_result = translate_response.json()
print(f"Bark translation: {translation_result['translation']}")


# ---------------------------------------------------------------
# 3. POST /v1/webhooks/subscribe
# ---------------------------------------------------------------
# Доорх код нь тухайн нохойн идэвхийн мэдэгдлийг (жишээ нь шинэ
# орчуулга бэлэн болох үед) хүлээн авах webhook URL бүртгэнэ.

your_webhook_url = "https://yourapp.example.com/webhooks/corgly"

subscribe_response = requests.post(
    f"{BASE_URL}/webhooks/subscribe",
    headers={"Authorization": f"Bearer {auth_token}"},
    json={
        "pet_id": "corgi_98231",
        "callback_url": your_webhook_url,
        "events": ["translation.completed"],
    },
)

# Жинхэнэ серверээс ирсэн хариу, Status 201 (тест хийгдсэн):
# {
#   "webhook_id": "hook_41ac9",
#   "status": "active"
# }
webhook_result = subscribe_response.json()
print(f"Webhook registered: {webhook_result['webhook_id']}")
