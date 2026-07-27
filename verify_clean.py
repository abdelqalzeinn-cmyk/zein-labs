import subprocess, time, urllib.request, json, urllib.parse, urllib.error, os
STORE=r"C:\Users\abdel\agilebot-business\store"; PORT=7874
sek=open(r"C:\Users\abdel\agilebot-business\secrets.env",encoding="utf-8").read()
JINA=[l for l in sek.splitlines() if l.startswith("JINA_API_KEY=")][0].split("=",1)[1].strip()
env=dict(os.environ, JINA_API_KEY=JINA)
srv=subprocess.Popen([r"/tmp/zeinverify_venv/Scripts/python.exe","-m","uvicorn","main:app","--host","127.0.0.1",f"--port={PORT}"], cwd=STORE, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(8)
def get(q):
    try: return urllib.request.urlopen(f"http://127.0.0.1:{PORT}{q}",timeout=30).read().decode("utf-8","replace")
    except urllib.error.HTTPError as e: return f"HTTPERR{e.code}"
    except Exception as e: return f"ERR{e}"
h=get("/health"); print("HEALTH:",h); assert json.loads(h)["ok"]
r=get("/search/u?u="+urllib.parse.quote("https://en.wikipedia.org/wiki/Roblox")); print("READER_OK:",'"Title: Roblox"' in r); assert '"Title: Roblox"' in r
q=get("/search/q?q="+urllib.parse.quote("free crypto payment gateway egypt")); print("WEBSEARCH_OK:","results" in q and len(q)>200); assert "results" in q and len(q)>200
co=json.loads(get("/checkout/pack1")); oid=co.get("order_id",""); dl=get(f"/dl/pack1?order={oid}"); print("DL_BYTES:",len(dl)); assert len(dl)>1000
srv.terminate(); print("AD-HOC VERIFY: reader+websearch+download-gating PASS on current main.py + secrets.env (clean venv)")
