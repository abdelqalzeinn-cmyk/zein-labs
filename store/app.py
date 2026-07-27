import gradio as gr
import json, urllib.request

GUMROAD_TOKEN = ""  # injected at deploy from secrets.env, never committed

def list_products():
    if not GUMROAD_TOKEN:
        return [["(demo) Roblox UI Kit", "$9", "https://gumroad.com"],
                ["(demo) Animation Pack 50", "$14", "https://gumroad.com"]]
    req = urllib.request.Request(
        f"https://api.gumroad.com/v2/products?access_token={GUMROAD_TOKEN}",
        headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = json.load(urllib.request.urlopen(req, timeout=10))
        rows = []
        for p in data.get("products", []):
            url = p.get("url", "https://gumroad.com")
            rows.append([p.get("name", "?"), f"${p.get('price', 0)/100:.2f}", url])
        return rows if rows else [["(no products yet)", "", "https://gumroad.com"]]
    except Exception as e:
        return [["(error loading)", str(e), "https://gumroad.com"]]

with gr.Blocks(title="AgileBot Store") as demo:
    gr.Markdown("# AgileBot Store\nAI-generated Roblox assets, Studio tools & prompt packs.")
    table = gr.Dataframe(value=list_products(), headers=["Product", "Price", "Buy"], interactive=False)
    demo.load(fn=list_products, outputs=table)

demo.launch()
