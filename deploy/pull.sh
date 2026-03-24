#!/usr/bin/env bash
set -euo pipefail

VPS="root@83.222.17.113"

echo "Pulling latest code..."
ssh "$VPS" "cd /opt/spacerocketlauncher && git pull origin main"

echo "Restarting Streamlit services..."
ssh "$VPS" "systemctl restart streamlit-simulator streamlit-lagrange"

echo "Reloading nginx..."
ssh "$VPS" "systemctl reload nginx"

echo "Done."
