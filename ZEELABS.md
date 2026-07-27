# Zein Labs — SIMPLIFIED plan (2026-07-27 revision)

Goal: prove a free-model AI can run a profitable micro-business. Keep it DEAD SIMPLE
so revenue actually flows.

## The easy money model
1. **One product**: AgileBot Companion Pack #1 (5 Roblox Studio Lua utilities, zip built + verified).
2. **One payment processor**: Gumroad — handles payments, tax, delivery. Already drafted
   (product ID XXkE-lCm-jgCmds6n7mA6Q==, file attached). Blocked only on payout KYC.
3. **One traffic source**: the YouTube video about this experiment + Roblox/AgileBot audience.
4. **One landing page**: `site/index.html` (GitHub Pages, $0) → "Buy on Gumroad" button.

## Dropped (over-engineering)
- HF Space Docker deployment
- Crypto Coinbase Commerce checkout
- Agent-facing micro-API (/v1/luau-check, /buy-api-key)
These were interesting but added friction with no buyer. The customer is a human Roblox
dev, not another AI. Keep the store code in `store/` as a backup, but the live funnel is
Gumroad + simple page.

## Operator to-do (the only human step)
- Complete Gumroad payout details (KYC) → product goes live.
- Put the live Gumroad product URL into `site/index.html` (replace REPLACE_WITH_YOUR_GUMROAD_PRODUCT_URL).
- Enable GitHub Pages on the repo (main branch, / root) so the landing page is public.
- Paste the video link in YouTube description.

## Autonomous loop (unchanged)
- `business-daily` cron reads steer.md, reports to reports/ + git push.
- Model: tencent/hy3:free (Nous) → $0 token cost.
- Net-positive bar: one $9 sale clears ~2 months of any cost. Trivial.
