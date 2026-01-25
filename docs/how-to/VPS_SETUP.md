# VPS Hardening, Docker Swarm & GitHub Actions Deployment Guide

This guide provides comprehensive instructions for configuring Ubuntu VPS machines for our infrastructure. We maintain two separate environments: Production (PROD) and Development (DEV). The setup process is identical for both environments, with the primary distinction being the environment-specific secrets deployed to each machine.

---

## 1. Create a Non-Root Admin User

Create a regular user and grant sudo access:

```bash
adduser myuser
usermod -aG sudo myuser
```

Log out and log back in as the new user.

---

## 2. Install OpenSSH Server

Update packages and install SSH:

```bash
apt update
apt install openssh-server -y
```

Verify SSH is running:

```bash
systemctl status ssh
```

---

## 3. Secure SSH Configuration (Key-Only Authentication)

Edit the SSH daemon configuration:

```bash
sudo nano /etc/ssh/sshd_config
```

Ensure the following settings are present or updated:

```
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
MaxSessions 2
```

Restart SSH to apply changes:

```bash
sudo systemctl restart ssh
```

Cloud-init can override SSH settings, so disable password auth there as well:

```bash
sudo nano /etc/ssh/sshd_config.d/50-cloud-init.conf
```

Set:

```
PasswordAuthentication no
```

Verify effective configuration:

```bash
sudo grep -ri PasswordAuthentication /etc/ssh/
```

---

## 4. Add SSH Public Key Authentication

On your local machine, display your public key:

```bash
cat ~/.ssh/id_ed25519.pub
```

On the VPS, create the SSH directory and authorized keys file:

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
nano ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

Paste the public key into the `authorized_keys` file.

---

## 5. Configure UFW Firewall

Reset any existing rules:

```bash
sudo ufw --force reset
```

Set default policies:

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

Allow required services:

```bash
sudo ufw allow OpenSSH
sudo ufw allow http
sudo ufw allow https
```

Allow Docker Swarm ports:

```bash
sudo ufw allow 2377/tcp
sudo ufw allow 7946/tcp
sudo ufw allow 7946/udp
sudo ufw allow 4789/udp
```

Enable firewall and verify:

```bash
sudo ufw enable
sudo ufw status verbose
```

Expected output should display `Status: active` along with configured rules.

---

## 6. Install and Configure Fail2Ban

Install Fail2Ban:

```bash
sudo apt update
sudo apt install fail2ban -y
sudo systemctl enable --now fail2ban
```

Create a local jail configuration:

```bash
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
```

Enable the SSH jail:

```
[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log
maxretry = 5
```

Restart Fail2Ban:

```bash
sudo systemctl restart fail2ban
```

---

## 7. Enable Automatic Security Updates

Install unattended upgrades:

```bash
sudo apt install unattended-upgrades -y
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

---

## 8. Install Docker Engine

Remove old Docker versions:

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

Install dependencies:

```bash
sudo apt update
sudo apt install ca-certificates curl gnupg -y
```

Add Docker GPG key:

```bash
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

Add Docker repository:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker Engine and plugins:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Add user to the Docker group:

```bash
sudo usermod -aG docker myuser
exit
```

Log back in for group changes to apply.

---

## 9. Initialize Docker Swarm

Initialize Swarm mode:

```bash
docker swarm init
docker node ls
```

Ignore join tokens unless adding additional nodes.

---

## 10. Create Deployment User for GitHub Actions

Create a dedicated deploy user:

```bash
sudo adduser deploy
sudo usermod -aG docker deploy
```

Generate an SSH key for GitHub Actions:

```bash
ssh-keygen -t ed25519 -C "gh-actions-deploy" -f gh_actions_deploy_key
```

Add the PRIVATE key to GitHub Secrets:

- `DEV_DEPLOY_SSH_PRIVATE_KEY`

or

- `PROD_DEPLOY_SSH_PRIVATE_KEY`

Install the public key on the VPS:

```bash
sudo mkdir -p /home/deploy/.ssh
sudo nano /home/deploy/.ssh/authorized_keys
sudo chown -R deploy:deploy /home/deploy/.ssh
sudo chmod 700 /home/deploy/.ssh
sudo chmod 600 /home/deploy/.ssh/authorized_keys
```

---

## 11. Create Docker Swarm Secrets

Create secrets directly on the VPS (not in GitHub):

```bash
echo "mongodb+srv://USER:PASS@HOST/DB" | sudo docker secret create db-url -
openssl rand -hex 32 | sudo docker secret create secret-key -
openssl rand -hex 32 | sudo docker secret create secret-auth-key -
echo "RESEND_API_KEY_HERE" | sudo docker secret create resend-api-key -
```

Verify secrets:

```bash
sudo docker secret ls
```

Secrets are mounted inside containers at `/run/secrets/<secret-name>`.

---

## End result

Server is locked down for unathorized people:

- SSH access is key-only (no passwords, no root login)
- UFW firewall blocks unwanted traffic
- Fail2Ban protects against brute-force attacks
- Security patches install automatically
- Docker Swarm handles container orchestration
- GitHub Actions can deploy via the dedicated deploy user
- All sensitive data lives in Docker Swarm secrets, not code
