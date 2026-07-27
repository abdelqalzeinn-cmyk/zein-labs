#!/usr/bin/env bash
# Drop this on the VPS. Run once after installing Hermes CLI + Nous config.
set -e

# 1. Create the working dir + reports log
mkdir -p ~/business/reports
cp secrets.env.example ~/business/secrets.env
#   -> operator fills secrets.env for real

# 2. Install Hermes CLI (already done on the VPS before this script)
#    hermes config set provider nous
#    hermes config set model tencent/hy3:free
#    hermes config set fallback_models "tencent/hy3:free,..."

# 3. Copy steer.md + state.json init
cp steer.md ~/business/steer.md
echo '{"revenue_today":0,"revenue_total":0,"actions":[],"issues":[]}' > ~/business/state.json

# 4. Start Hermes as a persistent service (survives SSH drop)
#    Either: systemd unit, or:
tmux new-session -d -s hermes 'hermes run' || true

# 5. Schedule the daily autopilot cron (cron fires the business-autopilot skill)
#    This is created from the desktop app / VPS via the cronjob tool:
#    schedule daily, prompt = "Run business-autopilot: read ~/business/secrets.env
#    and ~/business/steer.md, execute the daily loop, report to Telegram."

echo "Launch kit ready. Fill ~/business/secrets.env, then start the cron."
