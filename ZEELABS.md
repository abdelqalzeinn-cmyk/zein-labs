# Zein Labs — SIMPLIFIED plan (2026-07-27, Option #1)

Goal: dead-simple, $0-cost, passive-traffic web utility. No backend, no KYC to launch.

## The product: Luau Lab
Single-file HTML web utility for Roblox devs:
- **Beautify** — re-indents messy Luau/Lua.
- **Minify** — strips comments + whitespace to one line.
- **Stats** — lines / chars / tokens / function count.
- 100% client-side JS. No upload, no server, no payment processor needed to run.
- Money: **Buy Me a Coffee** button + (optional) AdSense slot (placeholder in HTML).

## Why this beats the Roblox-scripts product
- Zero KYC to go live (GitHub Pages is free, no Gumroad payout block).
- Passive traffic: Roblox devs search "luau beautifier" → SEO + your YouTube video.
- No inventory, no delivery, no support burden.

## Deploy (GitHub Pages, $0)
1. Repo already on GitHub (abdelqalzeinn-cmyk/zein-labs).
2. Settings → Pages → Source: main branch, /root → Save.
3. Live at https://abdelqalzeinn-cmyk.github.io/zein-labs/site/index.html
   (or move index.html to repo root for a cleaner URL).
4. Replace `REPLACE_WITH_BUYMEACOFFEE_URL` with your coffee link.
5. Paste the URL in your YouTube video description.

## Autonomous loop (unchanged)
- `business-daily` cron: reads steer.md, reports to reports/ + git push.
- Model: tencent/hy3:free (Nous) → $0 token cost.
- Net-positive bar: one $5 coffee = profitable forever at $0 cost.

## Dropped
- Gumroad product, HF Space Docker, crypto checkout, agent micro-API.
  (store/ code kept as backup, not the live funnel.)
