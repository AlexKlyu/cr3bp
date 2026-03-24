# Deployment Guide

## Architecture

```
nginx (port 80/443)
  ├── /                → index.html (landing page)
  ├── /simulator       → simulator.html (static)
  ├── /docs/           → PDF documents (static)
  ├── /streamlit/      → proxy → localhost:8501 (Streamlit simulator)
  └── /lagrange/       → proxy → localhost:8502 (Streamlit Lagrange)
```

## Current production

- **VPS:** 83.222.17.113 (Ubuntu 24.04)
- **Domain:** rocketlauncher.space
- **HTTPS:** Let's Encrypt, auto-renews
- **Repo:** github.com/AlexKlyu/cr3bp (private)

## Prerequisites

- Ubuntu 22.04+ VPS
- Domain with an **A record** pointing to the VPS IP (configure in DNS panel, e.g. reg.ru)
- GitHub personal access token with `repo` scope (for cloning private repo)

## First-time setup

### 1. Install system packages

```bash
apt update && apt install -y nginx python3 python3-venv git
```

### 2. Clone the repo

```bash
git clone https://<GITHUB_TOKEN>@github.com/AlexKlyu/cr3bp.git /opt/spacerocketlauncher
```

Replace `<GITHUB_TOKEN>` with a personal access token (Settings → Developer settings → Personal access tokens → Tokens (classic), scope: `repo`).

### 3. Run setup script

```bash
cd /opt/spacerocketlauncher
bash deploy/setup.sh
```

This will:
- Create a `deploy` system user
- Create a Python venv at `/opt/spacerocketlauncher/.venv` and install dependencies
- Copy nginx config to `/etc/nginx/sites-available/` and symlink it
- Install and enable both systemd services
- Reload nginx

### 4. Set up HTTPS with certbot

```bash
apt install -y certbot python3-certbot-nginx
certbot --nginx -d rocketlauncher.space --non-interactive --agree-tos -m YOUR_EMAIL
```

Certificate auto-renews via systemd timer.

### 5. Security hardening

**SSH — disable password login:**

```bash
cat > /etc/ssh/sshd_config.d/99-hardening.conf << 'EOF'
PermitRootLogin prohibit-password
PasswordAuthentication no
EOF
sshd -t && systemctl reload ssh
```

**Firewall — allow only SSH, HTTP, HTTPS:**

```bash
ufw default deny incoming
ufw default allow outgoing
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable
```

This blocks direct access to Streamlit ports (8501/8502) from outside. The Streamlit services are also bound to `127.0.0.1` (configured in the systemd units), so they are only reachable through nginx.

**Already installed on the current VPS:**
- `fail2ban` — brute-force SSH protection
- `unattended-upgrades` — automatic security patches

## Updating the site

SSH into the VPS and run:

```bash
cd /opt/spacerocketlauncher
git pull origin main
```

If Python dependencies changed:

```bash
.venv/bin/pip install -r requirements.txt
```

If Streamlit code changed:

```bash
sudo systemctl restart streamlit-simulator streamlit-lagrange
```

If nginx config changed:

```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/spacerocketlauncher
sudo nginx -t && sudo systemctl reload nginx
```

If systemd service files changed:

```bash
sudo cp deploy/streamlit-simulator.service deploy/streamlit-lagrange.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl restart streamlit-simulator streamlit-lagrange
```

## CI/CD with GitHub Actions (optional)

The workflow at `.github/workflows/deploy.yml` auto-deploys on push to `main` using a self-hosted runner.

### Setting up the self-hosted runner

1. Go to GitHub → repo Settings → Actions → Runners → New self-hosted runner
2. Follow GitHub's instructions to install the runner on the VPS
3. Grant the runner user sudo access for systemctl:

```bash
# /etc/sudoers.d/github-runner
github-runner ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart streamlit-simulator, /usr/bin/systemctl restart streamlit-lagrange, /usr/bin/systemctl reload nginx
```

## Service management

```bash
# Check status
systemctl status streamlit-simulator
systemctl status streamlit-lagrange

# Restart
systemctl restart streamlit-simulator
systemctl restart streamlit-lagrange

# View logs (live)
journalctl -u streamlit-simulator -f
journalctl -u streamlit-lagrange -f

# Reload nginx after config changes
nginx -t && systemctl reload nginx
```

## File locations on VPS

| Path | Contents |
|------|----------|
| `/opt/spacerocketlauncher/` | Application code |
| `/etc/nginx/sites-available/spacerocketlauncher` | nginx config (managed by certbot) |
| `/etc/systemd/system/streamlit-simulator.service` | Streamlit simulator unit |
| `/etc/systemd/system/streamlit-lagrange.service` | Lagrange viz unit |
| `/etc/letsencrypt/live/rocketlauncher.space/` | SSL certificates |
| `/etc/ssh/sshd_config.d/99-hardening.conf` | SSH hardening |

## Ports

| Port | Service | External access |
|------|---------|----------------|
| 22 | SSH | Yes (key-only) |
| 80 | nginx → redirects to 443 | Yes |
| 443 | nginx (HTTPS) | Yes |
| 8501 | Streamlit simulator | No (localhost only) |
| 8502 | Streamlit Lagrange | No (localhost only) |
