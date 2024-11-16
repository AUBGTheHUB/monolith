#!/bin/bash

# Step 1: Determine the appropriate login shell config file
for config_file in ~/.bash_profile ~/.profile ~/.zprofile ~/.login; do
  if [ -f "$config_file" ]; then
    SHELL_CONFIG="$config_file"
    break
  fi
done

# If no config file was found, default to .bash_profile
if [ -z "$SHELL_CONFIG" ]; then
  SHELL_CONFIG=~/.bash_profile
  touch "$SHELL_CONFIG"
  echo "No existing login shell config file found. Created ~/.bash_profile."
else
  echo "Using $SHELL_CONFIG as the shell config file."
fi

# Step 2: Define ssh-agent auto-start code block
SSH_AGENT_BLOCK="# Auto-start ssh-agent
if [ -z \"\$SSH_AUTH_SOCK\" ]; then
  # Check for a currently running instance of the agent
  RUNNING_AGENT=\"\$(ps -ax | grep 'ssh-agent -s' | grep -v grep | wc -l | tr -d '[:space:]')\"
  if [ \"\$RUNNING_AGENT\" = \"0\" ]; then
    # Launch a new instance of the agent
    ssh-agent -s &> ~/.ssh/ssh-agent
  fi
  eval \$(cat ~/.ssh/ssh-agent) > /dev/null
  ssh-add ~/.ssh/id_ed25519 2> /dev/null
fi"

# Step 3: Check if the block already exists in the config file
block_present=true

# Split the block into lines and check each line
while IFS= read -r line; do
  if ! grep -Fxq "$line" "$SHELL_CONFIG"; then
    block_present=false
    break
  fi
done <<< "$SSH_AGENT_BLOCK"

# Add ssh-agent code to config file if it's not already present
if [ "$block_present" = false ]; then
  echo "$SSH_AGENT_BLOCK" >> "$SHELL_CONFIG"
  echo "Added ssh-agent auto-start code to $SHELL_CONFIG."
  # Step 4: Reload the shell configuration
  source "$SHELL_CONFIG"
  echo "Configuration loaded! Please reopen your terminal to finalize setup."
else
  echo "ssh-agent auto-start code is already present in $SHELL_CONFIG."
  echo "You are all set!"
fi
