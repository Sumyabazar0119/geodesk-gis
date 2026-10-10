// Swagger UI "Try it out"-д зориулсан хөтөч доторх mock сервер.
// ./mock/<api>/v1/* руу явсан хүсэлтийг барьж аваад, тухайн spec-ийн
// жишээ хариуг (Prism-тэй адил дүрмээр) буцаана. GitHub Pages статик
// хостинг тул backend байхгүй үед sandbox ажиллах боломжийг олгоно.
importScripts("https://cdnjs.cloudflare.com/ajax/libs/js-yaml/4.1.0/js-yaml.min.js");

const SPEC_FILES = { geodesk: "openapi.yaml", corgly: "corgly.yaml" };
const specCache = {};

self.addEventListener("install", () => self.skipWaiting());
self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

self.addEventListener("fetch", (event) => {
  // Харьцангуй server URL-ыг spec эсвэл хуудасны байршлаас аль алинаас нь
  // тооцож болох тул ".../mock/<api>/v1/..." хэлбэртэй бүх замыг барина.
  const requestUrl = new URL(event.request.url);
  const mockMatch = requestUrl.pathname.match(/\/mock\/([a-z]+)\/v1(\/.*)$/);
  if (requestUrl.origin !== self.location.origin || !mockMatch) return;

  const [, apiName, requestPath] = mockMatch;
  event.respondWith(mockResponse(event.request, apiName, requestPath));
});

async function loadSpec(apiName) {
  if (!specCache[apiName]) {
    const specResponse = await fetch(new URL(SPEC_FILES[apiName], self.registration.scope));
    specCache[apiName] = jsyaml.load(await specResponse.text());
  }
  return specCache[apiName];
}

function findOperation(spec, method, requestPath) {
  for (const [pathTemplate, pathItem] of Object.entries(spec.paths)) {
    const pathPattern = new RegExp("^" + pathTemplate.replace(/\{[^}]+\}/g, "[^/]+") + "$");
    if (pathPattern.test(requestPath) && pathItem[method]) return pathItem[method];
  }
  return null;
}

function resolveRef(spec, node) {
  if (!node || !node.$ref) return node;
  return node.$ref.slice(2).split("/").reduce((current, key) => current[key], spec);
}

function exampleFor(spec, response) {
  const media = (resolveRef(spec, response).content || {})["application/json"];
  if (!media) return null;
  if (media.example !== undefined) return media.example;
  if (media.examples) return resolveRef(spec, Object.values(media.examples)[0]).value;
  return null;
}

function jsonResponse(status, body) {
  return new Response(JSON.stringify(body, null, 2), {
    status,
    headers: { "Content-Type": "application/json", "X-Mock-Server": "geodesk-sandbox" },
  });
}

async function mockResponse(request, apiName, requestPath) {
  if (request.method === "OPTIONS") return new Response(null, { status: 204 });
  if (!SPEC_FILES[apiName]) return jsonResponse(404, { error_code: "UNKNOWN_API", message: `No mock for '${apiName}'.` });

  const spec = await loadSpec(apiName);
  const operation = findOperation(spec, request.method.toLowerCase(), requestPath);
  if (!operation) {
    return jsonResponse(404, { error_code: "NO_PATH_MATCHED", message: `${request.method} ${requestPath} is not in the spec.` });
  }

  const requiresAuth = (operation.security || spec.security || []).length > 0;
  const authorization = request.headers.get("Authorization") || "";
  if (requiresAuth && !/^Bearer\s+\S+/.test(authorization) && operation.responses["401"]) {
    return jsonResponse(401, exampleFor(spec, operation.responses["401"]));
  }

  const successStatus = Object.keys(operation.responses).filter((status) => status.startsWith("2")).sort()[0];
  return jsonResponse(Number(successStatus), exampleFor(spec, operation.responses[successStatus]));
}
