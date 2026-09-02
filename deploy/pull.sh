#!/usr/bin/env bash
set -euo pipefail

# vdsina VPS (migrated from 83.222.17.113 on 2026-09-02)
VPS="root@146.103.99.163"

echo "Pulling latest code..."
ssh "$VPS" "cd /opt/spacerocketlauncher && git pull origin main && chown -R deploy:deploy /opt/spacerocketlauncher"

echo "Restarting Streamlit services..."
ssh "$VPS" "systemctl restart streamlit-simulator streamlit-lagrange"

echo "Reloading nginx..."
ssh "$VPS" "systemctl reload nginx"

echo "Done."
