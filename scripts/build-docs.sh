#!/usr/bin/env sh
# public/ хавтсанд Redoc (унших) ба Swagger UI (sandbox) хувилбаруудыг угсарна.
set -e
REDOCLY="npx -y @redocly/cli@2.4.0"

$REDOCLY lint docs/openapi/openapi.yaml docs/openapi/corgly.yaml

mkdir -p public
$REDOCLY build-docs docs/openapi/openapi.yaml -o public/index.html
$REDOCLY build-docs docs/openapi/corgly.yaml -o public/corgly.html

cp docs/openapi/openapi.yaml docs/openapi/corgly.yaml public/
cp -r site/. public/
touch public/.nojekyll
