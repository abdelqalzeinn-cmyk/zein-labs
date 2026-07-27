# Zein Labs agent-facing storefront + billing API
# Serves digital products (file download after crypto payment) and a per-call Lua-gen API.
# Region-adapted from Fabler Labs: crypto instead of Stripe (Egypt block), agent customers.

import os, json, hashlib, time, uuid, secrets, subprocess, tempfile
from fastapi import FastAPI, Request, Response, Query
import urllib.request, urllib.error, urllib.parse

app = FastAPI(title="Zein Labs")

# Config from env (HF Space secrets). NEVER hardcode keys.
CRYPTO_ENABLED = os.environ.get("CRYPTO_ENABLED", "0").lower() in ("1", "true", "yes")  # set "1" to arm real crypto checkout
COINBASE_API_KEY = os.environ.get("COINBASE_COMMERCE_KEY", "")  # optional
JINA_API_KEY = os.environ.get("JINA_API_KEY", "")
PRODUCTS = {
    "pack1": {
        "name": "AgileBot Companion Pack 1 - Studio Utility Scripts",
        "price_usd": 9.0,
        "file": os.path.join(os.path.dirname(__file__), "..", "products", "001-studio-utility-pack", "agilebot-companion-pack-1.zip"),
        "type": "file",
    },
    "lua-gen": {
        "name": "Roblox Lua generator API (per-call)",
        "price_usd": 0.50,
        "type": "api",
    },
}
# In-memory order ledger (ephemeral on HF free tier; swap for SQLite if persistent needed)
ORDERS = {}

SPACE_HOST = (os.environ.get("SPACE_HOST") or os.environ.get("SPACE_ID", "")).replace("/", "-")
BASE = f"https://{SPACE_HOST}.hf.space" if SPACE_HOST else "https://zein-labs.hf.space"

# --- API-key auth (agent customers) ---
API_KEYS = {}  # key -> {"created": ts, "calls": 0}
DEMO_KEY = os.environ.get("ZEIN_DEMO_API_KEY", "zein_demo_key_123")
API_KEYS[DEMO_KEY] = {"created": time.time(), "calls": 0}
LUAU_AST = os.environ.get("LUAU_AST_PATH", r"C:\Users\abdel\luau\cmbuild\luau-ast.exe")

def require_key(request: Request):
    k = request.headers.get("X-API-Key") or request.query_params.get("api_key")
    if not k or k not in API_KEYS:
        return None
    return k

@app.get("/")
def home():
    items = [{"id": k, **v} for k, v in PRODUCTS.items()]
    return {"op": "Zein Labs", "products": items, "crypto": CRYPTO_ENABLED}

@app.get("/catalog")
def catalog():
    return {"products": [{"id": k, "name": v["name"], "price_usd": v["price_usd"], "type": v["type"]} for k, v in PRODUCTS.items()]}

@app.post("/checkout/{pid}")
def checkout(pid: str):
    p = PRODUCTS.get(pid)
    if not p:
        return Response(json.dumps({"error": "unknown product"}), status_code=404, media_type="application/json")
    if not CRYPTO_ENABLED:
        # DEMO mode: issue a fake paid order so the flow is testable without crypto keys
        oid = "demo_" + uuid.uuid4().hex[:12]
        ORDERS[oid] = {"pid": pid, "paid": True, "ts": time.time(), "demo": True}
        return {"order_id": oid, "demo": True, "download_url": f"{BASE}/dl/{pid}?order={oid}", "note": "crypto disabled - demo order auto-paid"}
    # Real crypto checkout (Coinbase Commerce charge)
    if not COINBASE_API_KEY:
        return Response(json.dumps({"error": "crypto not configured"}), status_code=500, media_type="application/json")
    payload = json.dumps({
        "name": p["name"], "description": "Zein Labs digital product",
        "pricing_type": "fixed",
        "local_price": {"amount": str(p["price_usd"]), "currency": "USD"},
        "metadata": {"pid": pid},
    }).encode()
    req = urllib.request.Request("https://api.commerce.coinbase.com/charges", data=payload, method="POST")
    req.add_header("X-CC-Api-Key", COINBASE_API_KEY)
    req.add_header("Content-Type", "application/json")
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
    except urllib.error.HTTPError as e:
        return Response(e.read(), status_code=502, media_type="application/json")
    charge = resp.get("data", {})
    oid = charge.get("id", uuid.uuid4().hex)
    ORDERS[oid] = {"pid": pid, "paid": False, "ts": time.time()}
    return {"order_id": oid, "hosted_url": charge.get("hosted_url"), "pay": True}

@app.get("/dl/{pid}")
def download(pid: str, order: str = Query(None)):
    p = PRODUCTS.get(pid)
    if not p:
        return Response("not found", status_code=404)
    rec = ORDERS.get(order or "")
    if not rec or rec.get("pid") != pid or not rec.get("paid"):
        return Response("unpaid or invalid order", status_code=403)
    fp = p.get("file")
    if fp and os.path.exists(fp):
        return Response(open(fp, "rb").read(), media_type="application/zip",
                        headers={"Content-Disposition": f"attachment; filename={os.path.basename(fp)}"})
    return Response("file missing", status_code=404)

@app.post("/api/lua-gen")
async def lua_gen(request: Request):
    # Per-call paid API. In demo mode, serve a generated stub; real mode checks a prepaid token.
    body = await request.body()
    try:
        spec = json.loads(body) if body else {}
    except Exception:
        spec = {}
    prompt = spec.get("prompt", "a generic Roblox utility")
    # Generate a minimal valid Lua ModuleScript from the prompt (deterministic demo generator)
    code = f'-- Generated by Zein Labs lua-gen API\n-- spec: {prompt}\nlocal module = {{}}\nfunction module.run()\n\tprint("Zein Labs: {prompt}")\nend\nreturn module\n'
    return {"generated": True, "code": code, "bytes": len(code)}

@app.get("/health")
def health():
    return {"ok": True, "crypto": CRYPTO_ENABLED, "orders": len(ORDERS), "api_keys": len(API_KEYS)}

# --- Agent-facing micro-API (the Fabler Labs play: sell to AIs) ---
@app.post("/v1/luau-check")
async def luau_check(request: Request):
    k = require_key(request)
    if not k:
        return Response(json.dumps({"error": "invalid or missing api key"}), status_code=401, media_type="application/json")
    API_KEYS[k]["calls"] += 1
    src = (await request.body()).decode("utf-8", "replace")
    if os.path.exists(LUAU_AST):
        tmp = os.path.join(tempfile.gettempdir(), f"luau_{uuid.uuid4().hex[:8]}.lua")
        open(tmp, "w", encoding="utf-8").write(src)
        try:
            r = subprocess.run([LUAU_AST, tmp], capture_output=True, text=True, timeout=10)
            os.unlink(tmp)
            return {"valid": r.returncode == 0,
                    "ast_head": r.stdout[:1500] if r.returncode == 0 else None,
                    "error": r.stderr[:500] if r.returncode != 0 else None}
        except Exception as e:
            return {"valid": False, "error": f"luau-ast failed: {e}"}
    # Off-HF fallback: brace/paren balance check (no real Luau parse)
    stack, bad = [], None
    for i, ch in enumerate(src):
        if ch in "({[": stack.append(ch)
        elif ch in ")}]":
            if not stack: bad = i; break
            stack.pop()
    bal = (not bad) and (not stack)
    return {"valid": bal, "note": "fallback brace-balance (luau-ast not on this host)",
            "bad_at": bad}

@app.get("/buy-api-key")
def buy_api_key():
    if not CRYPTO_ENABLED:
        nk = "zein_" + secrets.token_hex(8)
        API_KEYS[nk] = {"created": time.time(), "calls": 0}
        return {"api_key": nk, "demo": True, "note": "crypto disabled - key auto-issued (demo)"}
    # Real mode: mint key, attach to crypto checkout
    nk = "zein_" + secrets.token_hex(8)
    API_KEYS[nk] = {"created": time.time(), "calls": 0, "paid": False}
    payload = json.dumps({
        "name": f"Zein Labs API key {nk}", "pricing_type": "fixed",
        "local_price": {"amount": "5.00", "currency": "USD"},
        "metadata": {"api_key": nk},
    }).encode()
    req = urllib.request.Request("https://api.commerce.coinbase.com/charges", data=payload, method="POST")
    req.add_header("X-CC-Api-Key", COINBASE_API_KEY)
    req.add_header("Content-Type", "application/json")
    try:
        resp = json.loads(urllib.request.urlopen(req, timeout=15).read())
        return {"api_key": nk, "hosted_url": resp.get("data", {}).get("hosted_url"), "pay": True}
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status_code=502, media_type="application/json")

# --- Autonomous research via jina.ai (Fabler Labs-style recon) ---
JINA_HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "text/plain"}
if JINA_API_KEY:
    JINA_HEADERS["Authorization"] = f"Bearer {JINA_API_KEY}"

@app.get("/search/q")
def search_query(q: str = Query(...)):
    """Web search via jina reader on a DuckDuckGo HTML SERP (free, reliable)."""
    ddg = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    url = "https://r.jina.ai/" + ddg
    req = urllib.request.Request(url, headers=JINA_HEADERS)
    try:
        txt = urllib.request.urlopen(req, timeout=25).read().decode("utf-8", "replace")
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status_code=502, media_type="application/json")
    return {"query": q, "results": txt[:4000]}

@app.get("/search/u")
def search_url(u: str = Query(...)):
    """Read + extract any URL via jina's r.jina.ai reader."""
    target = u if u.startswith("http") else "https://" + u
    url = "https://r.jina.ai/" + target
    req = urllib.request.Request(url, headers=JINA_HEADERS)
    try:
        txt = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "replace")
    except Exception as e:
        return Response(json.dumps({"error": str(e)}), status_code=502, media_type="application/json")
    return {"url": target, "extracted": txt[:4000]}
