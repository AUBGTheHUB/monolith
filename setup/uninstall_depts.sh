#!/bin/bash

# Ensure gum is used for the confirmation if available
CONFIRM_CMD="read -p"
if command -v gum &> /dev/null; then
    gum confirm "Are you sure you want to uninstall all dev tools (pyenv, poetry, node, gum)?" && confirmed=yes
else
    read -p "Are you sure you want to uninstall all dev tools? (y/N): " confirmed
fi

if [[ ! $confirmed =~ ^[Yy]$ && $confirmed != "yes" ]]; then
    echo "Aborted."
    exit 0
fi

echo "🗑️ Starting uninstallation..."

OS_TYPE="$(uname)"
SHELL_CONFIG="$HOME/.bashrc"
[[ "$SHELL" == */zsh ]] && SHELL_CONFIG="$HOME/.zshrc"

# 1. Remove Folders & Binaries
echo "Removing tool directories..."
rm -rf "$HOME/.pyenv"
rm -rf "$HOME/.local/share/pypoetry/"
rm -rf "$HOME/.local/bin/poetry"
# Remove project-specific virtual environments
find . -name ".venv" -type d -exec rm -rf {} + 2>/dev/null || true

# 2. Linux Specific Cleanup
if [[ "$OS_TYPE" == "Linux" ]]; then
    echo "Removing system packages (requires sudo)..."
    sudo apt-get remove -y gum nodejs
    sudo rm -f /etc/apt/sources.list.d/charm.list /etc/apt/sources.list.d/nodesource.list
    sudo rm -f /etc/apt/keyrings/charm.gpg
fi

# 3. macOS Specific Cleanup
if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "Removing Homebrew packages..."
    brew uninstall gum pyenv poetry node 2>/dev/null || true
fi

# 4. Shell Config Cleanup (The most important part)
echo "Cleaning up $SHELL_CONFIG..."
if [[ "$OS_TYPE" == "Darwin" ]]; then
    # macOS sed requires an empty string for the -i flag
    sed -i '' '/PYENV_ROOT/d' "$SHELL_CONFIG"
    sed -i '' '/pyenv init/d' "$SHELL_CONFIG"
    sed -i '' '/.local\/bin/d' "$SHELL_CONFIG"
else
    # Linux sed
    sed -i '/PYENV_ROOT/d' "$SHELL_CONFIG"
    sed -i '/pyenv init/d' "$SHELL_CONFIG"
    sed -i '/.local\/bin/d' "$SHELL_CONFIG"
fi

echo "✅ Uninstallation complete."
echo "⚠️  Please run 'source $SHELL_CONFIG' or restart your terminal to finalize."
