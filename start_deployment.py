#!/usr/bin/env python
import sys

import paramiko

VM_IP = ""
VM_PSWD = ""
DISCORD_WH = ""
VM_USER = "root"
BRANCH = ""

print("-----------------------------------------")
print("     Starting deployment of services     ")
print("-----------------------------------------")

args = sys.argv[1:]
while args:
    if args[0] == "--ip":
        VM_IP = args[1]
        args.pop(0)
        args.pop(0)
    elif args[0] == "--pswd":
        VM_PSWD = args[1]
        args.pop(0)
        args.pop(0)
    elif args[0] == "--discordwh":
        DISCORD_WH = args[1]
        args.pop(0)
        args.pop(0)
    elif args[0] == "--user":
        VM_USER = args[1]
        args.pop(0)
        args.pop(0)
    elif args[0] == "--branch":
        BRANCH = args[1]
        args.pop(0)
        args.pop(0)
    elif args[0] in ["-h", "--help"]:
        print(
            "Usage: python script.py [--ip <IP>] [--pswd <Password>] [--discordwh <Webhook>] [--user <User>] [--branch <Branch>]",
        )
        sys.exit(0)
    else:
        print(f"Invalid option: {args[0]}", file=sys.stderr)
        sys.exit(1)

# Check for required options and provide default values if not set
if not VM_IP:
    print("Error: Missing required option --ip.", file=sys.stderr)
    sys.exit(1)

if not VM_PSWD:
    print("Error: Missing required option --pswd.", file=sys.stderr)
    sys.exit(1)

if not DISCORD_WH:
    print("Error: Missing required option --discordwh.", file=sys.stderr)
    sys.exit(1)

if not BRANCH:
    print("Error: Missing required option --branch.", file=sys.stderr)
    sys.exit(1)

ssh_client = paramiko.SSHClient()

try:
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=VM_IP, username=VM_USER, password=VM_PSWD)

    CURRENT_BRANCH = f"cd ~/monolith && git rev-parse --abbrev-ref HEAD"
    _, stdout, _ = ssh_client.exec_command(CURRENT_BRANCH)
    current_branch = stdout.read().strip().decode('utf-8')
    if current_branch != BRANCH:
        PULL_ALL_BRANCHES = f"cd ~/monolith && git pull --all"
        _, _, _ = ssh_client.exec_command(PULL_ALL_BRANCHES)

    CHECKOUT_BRANCH = f"cd ~/monolith && git checkout -f {BRANCH} && git reset --hard origin/{BRANCH} && git pull"
    _, _, _ = ssh_client.exec_command(CHECKOUT_BRANCH)

    RUN_DEPLOYMENT_SCRIPT = f"cd ~/monolith && nohup ./deployment.sh {BRANCH} {DISCORD_WH} > deployment.logs 2>&1 &"
    _, _, _ = ssh_client.exec_command(RUN_DEPLOYMENT_SCRIPT)
    # print(err.read())

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
finally:
    ssh_client.close()
