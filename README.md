# GeoDesk GIS — API Documentation (Sprint 05)

Software Project Documentation, Week 05: OpenAPI 3.0, Bhatti code samples, Swagger UI & Redoc.
Гүйцэтгэсэн: С.Сумъяабазар (21B1NUM0119)

## Онлайн хувилбар

| Хэрэглээ | URL |
|---|---|
| Redoc — олон нийтэд унших (GeoDesk) | https://sumyabazar0119.github.io/geodesk-gis/ |
| Redoc — Corg.ly UE-5 | https://sumyabazar0119.github.io/geodesk-gis/corgly.html |
| Swagger UI — sandbox "Try it out" | https://sumyabazar0119.github.io/geodesk-gis/swagger/ |

Swagger UI дээр **Servers → Sandbox mock** сонгож, **Authorize**-д дурын токен оруулна.
`public/mock-sw.js` service worker нь `/mock/<api>/v1/*` хүсэлтийг барьж, spec-ийн жишээ хариуг буцаана (токенгүй бол 401).

## Бүтэц

```
docs/openapi/openapi.yaml           GeoDesk GIS API — 6 endpoint, BearerAuth, x-codeSamples
docs/openapi/corgly.yaml            Corg.ly Onboarding API — UE-5-ын 3 endpoint
docs/openapi/corgly_code_samples.py UE-5 Python code samples
docs/code-sample-audit.md           Bhatti 5 зарчмын scorecard (US-5.2)
docs/decision-report.md             Swagger UI vs Redoc, 100 үг (US-5.4)
tests/test_code_samples.py          Бүх sample-ыг Prism mock дээр ажиллуулдаг тест
site/                               Swagger UI хуудас ба sandbox mock (эх)
public/                             Build хийгдсэн сайт (GitHub Pages)
```

## Локалаар ажиллуулах

```sh
# 1. Spec шалгах (zero errors)
npx @redocly/cli lint docs/openapi/openapi.yaml docs/openapi/corgly.yaml

# 2. Code sample-уудыг mock сервер дээр шалгах
npx @stoplight/prism-cli mock docs/openapi/corgly.yaml  -p 4010 &
npx @stoplight/prism-cli mock docs/openapi/openapi.yaml -p 4011 &
pip install requests pyyaml pytest
pytest tests -v

# 3. Redoc + Swagger UI-г public/ руу build хийх
sh scripts/build-docs.sh
python -m http.server -d public 8000   # http://localhost:8000/swagger/

# Эсвэл Swagger UI-г Docker-оор
docker run -p 8080:8080 -e SWAGGER_JSON=/spec/openapi.yaml -v "$(pwd)/docs/openapi:/spec" swaggerapi/swagger-ui
```

## CI/CD

`.github/workflows/docs.yml` нь push бүрт: Prism mock асаах → `pytest` (10 тест) → `redocly lint` → Redoc build →
`public/`-ыг GitHub Pages руу deploy хийнэ. Анх удаа: **Settings → Pages → Source: GitHub Actions** болгоно.
