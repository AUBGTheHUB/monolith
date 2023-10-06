#!/bin/bash

VM_IP=""
VM_PSWD=""
DISCORD_WH=""

echo "-----------------------------------------"
echo "     Starting deployment of services     "
echo "-----------------------------------------"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --ip)
      VM_IP="$2"
      shift 2
      ;;
    --pswd)
      VM_PSWD="$2"
      shift 2
      ;;
    --discordwh)
      DISCORD_WH="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [--ip <IP>] [--pswd <Password>] [--discordwh <Webhook>]"
      exit 0
      ;;
    *)
      echo "Invalid option: $1" >&2
      exit 1
      ;;
  esac
done

# Check for required options and provide default values if not set
if [ -z "$VM_IP" ]; then
  echo "Error: Missing required option --ip."
  exit 1
fi

if [ -z "$VM_PSWD" ]; then
  echo "Error: Missing required option --pswd."
  exit 1
fi

if [ -z "$DISCORD_WH" ]; then
  echo "Error: Missing required option --discordwh."
  exit 1
fi

# echo "VM_IP: $VM_IP"
# echo "VM_PSWD: $VM_PSWD"
# echo "DISCORD_WH: $DISCORD_WH"
