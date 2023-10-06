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

ATTACH_TMUX = f"tmux attach || tmux"
RUN_DEPLOYMENT_SCRIPT_CMD = f"cd ~/monolith && git reset --hard origin/{BRANCH} && ./deployment.sh && tmux detach"

ssh_client = paramiko.SSHClient()

try:
    # Automatically add the server's host key (this is insecure and should be improved)
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Connect to the SSH server
    ssh_client.connect(hostname=VM_IP, username=VM_USER, password=VM_PSWD)

    # Execute the command
    _, stdout, stderr = ssh_client.exec_command(ATTACH_TMUX)

    print(stdout.read().decode('utf-8'))
    _, stdout, stderr = ssh_client.exec_command(RUN_DEPLOYMENT_SCRIPT_CMD)

    # Print the command's output
    print(stderr.read().decode('utf-8'))

except paramiko.AuthenticationException:
    print("Authentication failed. Please check your credentials.")
    sys.exit(1)
except paramiko.SSHException as e:
    print("SSH connection failed:", str(e))
    sys.exit(1)

ssh_client.close()
print("Execution of deployment script started")
