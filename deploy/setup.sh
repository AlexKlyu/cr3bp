#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/opt/spacerocketlauncher"

echo "=== CR3BP Simulator — Server Setup ==="

# Swap: a 1 GB VPS with two always-on Python services has no headroom for
# spikes, and without swap the kernel OOM-kills instead of slowing down.
if ! swapon --show | grep -q /swapfile; then
    echo "Creating 2G swapfile..."
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile >/dev/null
    sudo swapon /swapfile
    grep -q '^/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab >/dev/null
fi

# Webroot for ACME HTTP-01 challenges (referenced by nginx.conf).
sudo mkdir -p /var/www/certbot/.well-known/acme-challenge
sudo chown -R www-data:www-data /var/www/certbot

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
# NOTE: nginx.conf references /etc/letsencrypt/live/rocketlauncher.space/.
# On a brand new host obtain the certificate first, otherwise `nginx -t` fails:
#   certbot certonly --webroot -w /var/www/certbot -d rocketlauncher.space \
#           -d www.rocketlauncher.space --agree-tos --register-unsafely-without-email
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
