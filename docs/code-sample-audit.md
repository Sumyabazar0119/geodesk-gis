# Code Sample Audit Scorecard (US-5.2)

Bhatti et al., *Docs for Developers*, Ch. 5 (pp. 86–94)-ийн 5 зарчмаар бүх code sample-ыг 1–5 одоор үнэлэв.
"Trustworthy" баганын бүх sample-ыг `tests/test_code_samples.py` нь Prism mock сервер дээр CI-д ажиллуулж,
хэвлэсэн гаралтыг баримт дахь тайлбартай харьцуулдаг (Bhatti p. 96).

## UE-5: Corg.ly Onboarding API (`docs/openapi/corgly_code_samples.py`)

| Sample | Explained | Concise | Clear | Usable | Trustworthy | Дундаж |
|---|---|---|---|---|---|---|
| `POST /v1/pets/upload-photo` | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ (foo/bar байхгүй, `samples/photos/einstein_corgi.jpg`) | ★★★★★ (200, payload = spec example) | 4.8 |
| `POST /v1/audio/translate-bark` | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ (бодит аудио зам; fixture нь чимээгүй WAV) | ★★★★★ (200, translation шалгагдсан) | 4.6 |
| `POST /v1/webhooks/subscribe` | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ (домэйн hook URL) | ★★★★★ (Status 201 verified) | 5.0 |

## GeoDesk GIS API (`x-codeSamples` in `docs/openapi/openapi.yaml`)

| Sample | Explained | Concise | Clear | Usable | Trustworthy | Дундаж |
|---|---|---|---|---|---|---|
| `POST /layers/import` | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★★ | 4.6 |
| `POST /projects/{project_id}/layers/merge` | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ | 4.8 |
| `GET /wms/layers` | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | 5.0 |
| `POST /terrain/contours` | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ | 4.8 |
| `POST /terrain/watershed` | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ | 4.8 |
| `POST /layers/{layer_id}/convert` | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ | 4.8 |

**Нийт дундаж: 4.80 / 5.0 (96%)** (216 / 225 од) — DoD шаардлага ≥ 4.0 (80%) хангагдсан.

## Оноо хасагдсан шалтгаан

- **Concise 4★ (upload-photo, translate-bark, import):** multipart-д `(filename, file, mime_type)` tuple шаардлагатай тул нэг мөр илүү boilerplate үлдсэн.
- **Usable 4★ (translate-bark):** репод байгаа WAV fixture нь чимээгүй бичлэг; бодит сервер `422 NO_BARK_DETECTED` буцаах магадлалтай. Хэрэглэгч өөрийн бичлэгээр солих ёстой.
- **Usable 4★ (GeoDesk merge/contours/watershed/convert/import):** `layer_7f3a21`, `layer_dem_44c1` зэрэг ID нь өмнөх импортын алхмаас ирдэг тул дангаар нь хуулж ажиллуулахад өөрийн ID-аар солих шаардлагатай.

## Draft → Final засвар (Bhatti-ийн зарчмаар)

| Draft-д байсан асуудал | Зарчим | Засвар |
|---|---|---|
| `file`, `data`, `url`, `response`, `e` гэх ерөнхий нэр | Clear (p. 92) | `pet_photo_file`, `bark_audio_file`, `photo_response`, `subscription_response` |
| `yourapp.example.com` callback | Usable (p. 93) | `petcare.example.com/webhooks/corgly` (домэйн утгатай) |
| Хариуны JSON-ыг гараар бичсэн, `breed` талбар дутуу | Trustworthy (p. 94) | Prism mock-оос гарсан бодит гаралтыг тайлбарт оруулж, CI-д тулгадаг |
| Webhook-ын 201 статус зөвхөн тайлбарт | Trustworthy (p. 94) | Функц `Response` буцааж, `status_code`-ыг хэвлэж, тестээр 201-ийг баталгаажуулна |
| Sample бүрийн өмнө тайлбар 1 мөр | Explained (p. 87) | Юу хийх, ямар оролт шаардах, дараагийн алхамд юу ашиглахыг 2 өгүүлбэрээр |
