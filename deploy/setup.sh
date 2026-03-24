#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/spacerocketlauncher"

echo "=== CR3BP Simulator — Server Setup ==="

# Create deploy user if needed
if ! id -u deploy &>/dev/null; then
    echo "Creating deploy user..."
    sudo useradd -r -m -s /bin/bash deploy
fi

# Ensure app directory ownership
sudo chown -R deploy:deploy "$APP_DIR"

# Create Python venv and install deps
echo "Setting up Python environment..."
cd "$APP_DIR"
if [ ! -d .venv ]; then
    python3 -m venv .venv
fi
.venv/bin/pip install --upgrade pip
.venv/bin/pip install -r requirements.txt

# Install nginx config
echo "Configuring nginx..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/spacerocketlauncher
sudo ln -sf /etc/nginx/sites-available/spacerocketlauncher /etc/nginx/sites-enabled/spacerocketlauncher
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t

# Install and enable systemd services
echo "Installing systemd services..."
sudo cp deploy/streamlit-simulator.service /etc/systemd/system/
sudo cp deploy/streamlit-lagrange.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable streamlit-simulator streamlit-lagrange
sudo systemctl restart streamlit-simulator streamlit-lagrange

# Reload nginx
sudo systemctl reload nginx

echo "=== Setup complete ==="
echo "Landing page: http://$(hostname -I | awk '{print $1}')/"
