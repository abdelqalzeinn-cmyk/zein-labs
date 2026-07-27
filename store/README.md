# Zein Labs — agent-facing products & micro-API

FastAPI storefront that sells digital products (crypto checkout) and a per-call
Luau syntax-check API (agent customers). Modeled on Fabler Labs: the customers
are other AIs, not people. Region-adapted: crypto instead of Stripe (Egypt block).

## Endpoints
- `GET /health` — status
- `GET /catalog` — product list
- `POST /checkout/{pid}` — start crypto checkout (demo auto-pays when CRYPTO_ENABLED=0)
- `GET /dl/{pid}?order=` — download file after payment (403 without valid order)
- `GET /search/q?q=` — web search via jina + DuckDuckGo
- `GET /search/u?u=` — read/extract any URL via jina reader
- `POST /v1/luau-check` (header `X-API-Key`) — Luau/Lua syntax check (real luau-ast if present, else brace-balance fallback)
- `GET /buy-api-key` — mint an API key (demo auto-issues; real mode attaches crypto checkout)

## Env (HF Space secrets)
- `JINA_API_KEY` — jina.ai research
- `CRYPTO_ENABLED` — "1" to arm real Coinbase Commerce checkout
- `COINBASE_COMMERCE_KEY` — Coinbase Commerce API key
- `LUAU_AST_PATH` — optional path to luau-ast.exe for real Luau parse

## Deploy
Dockerfile-based HF Space (SDK: Docker). Push files, set secrets, live.

## Local test
```
pip install -r requirements.txt
CRYPTO_ENABLED=0 JINA_API_KEY=... uvicorn main:app --port 7860
```
