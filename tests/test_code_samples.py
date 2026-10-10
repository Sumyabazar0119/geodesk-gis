"""Bhatti p. 94 "Trustworthy" / p. 96 "Designing Code Samples":
бүх code sample-ыг Prism mock сервер дээр бодитоор ажиллуулж,
хэвлэсэн гаралт нь баримт дахь тайлбартай яг таарч байгааг шалгана.

Ажиллуулахаас өмнө (репогийн root-оос):
    npx @stoplight/prism-cli mock docs/openapi/corgly.yaml  -p 4010
    npx @stoplight/prism-cli mock docs/openapi/openapi.yaml -p 4011
"""
import contextlib
import importlib.util
import io
import os
import re
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
OPENAPI_DIR = REPO_ROOT / "docs" / "openapi"
CORGLY_MOCK_URL = os.getenv("CORGLY_MOCK_URL", "http://127.0.0.1:4010")
GEODESK_MOCK_URL = os.getenv("GEODESK_MOCK_URL", "http://127.0.0.1:4011")


@pytest.fixture(autouse=True)
def run_from_repo_root(monkeypatch):
    # Sample-ууд "samples/..." гэсэн харьцангуй замаар файл нээдэг.
    monkeypatch.chdir(REPO_ROOT)
    monkeypatch.setenv("CORGLY_API_TOKEN", "ci_corgly_token")
    monkeypatch.setenv("GEODESK_API_TOKEN", "ci_geodesk_token")


def spec_example(spec_file, path, method, status):
    spec = yaml.safe_load((OPENAPI_DIR / spec_file).read_text(encoding="utf-8"))
    media = spec["paths"][path][method]["responses"][status]["content"]["application/json"]
    return next(iter(media["examples"].values()))["value"]


def load_corgly_samples(monkeypatch):
    monkeypatch.setenv("CORGLY_BASE_URL", CORGLY_MOCK_URL)
    module_spec = importlib.util.spec_from_file_location("corgly_code_samples", OPENAPI_DIR / "corgly_code_samples.py")
    module = importlib.util.module_from_spec(module_spec)
    module_spec.loader.exec_module(module)
    return module


def test_upload_pet_photo_returns_profile(monkeypatch):
    samples = load_corgly_samples(monkeypatch)
    photo_response = samples.upload_pet_photo("samples/photos/einstein_corgi.jpg", "Einstein", "Pembroke Welsh Corgi")
    assert photo_response.status_code == 200
    assert photo_response.json() == spec_example("corgly.yaml", "/pets/upload-photo", "post", "200")


def test_translate_pet_bark_returns_translation(monkeypatch):
    samples = load_corgly_samples(monkeypatch)
    translation_response = samples.translate_pet_bark("samples/audio/einstein_bark_sample.wav", "corgi_98231")
    assert translation_response.status_code == 200
    assert translation_response.json()["translation"] == "I am hungry, please feed me."


def test_subscribe_pet_webhook_returns_201(monkeypatch):
    samples = load_corgly_samples(monkeypatch)
    subscription_response = samples.subscribe_pet_webhook(
        "corgi_98231", "https://petcare.example.com/webhooks/corgly", ["translation.completed"]
    )
    assert subscription_response.status_code == 201
    assert subscription_response.json() == spec_example("corgly.yaml", "/webhooks/subscribe", "post", "201")


def test_corgly_request_without_token_is_rejected(monkeypatch):
    samples = load_corgly_samples(monkeypatch)
    monkeypatch.setattr(samples, "auth_header", {})
    with pytest.raises(samples.requests.HTTPError) as http_error:
        samples.subscribe_pet_webhook("corgi_98231", "https://petcare.example.com/webhooks/corgly", ["translation.completed"])
    assert http_error.value.response.status_code == 401


def geodesk_code_samples():
    spec = yaml.safe_load((OPENAPI_DIR / "openapi.yaml").read_text(encoding="utf-8"))
    for path, path_item in spec["paths"].items():
        for method, operation in path_item.items():
            for code_sample in operation.get("x-codeSamples", []):
                yield pytest.param(code_sample["source"], id=f"{method.upper()} {path}")


@pytest.mark.parametrize("sample_source", list(geodesk_code_samples()))
def test_geodesk_code_sample_prints_documented_output(sample_source):
    # Мөр бүрийн "print(...)  # хүлээгдэж буй гаралт" тайлбарыг бодит гаралттай харьцуулна.
    expected_lines = re.findall(r"print\(.*\)\s+# (.+)$", sample_source, flags=re.MULTILINE)
    runnable_source = sample_source.replace("https://api.geodesk.mn/v1", GEODESK_MOCK_URL)

    captured_stdout = io.StringIO()
    with contextlib.redirect_stdout(captured_stdout):
        exec(compile(runnable_source, "<x-codeSample>", "exec"), {})

    assert expected_lines, "code sample must document its expected output"
    assert captured_stdout.getvalue().splitlines() == expected_lines
