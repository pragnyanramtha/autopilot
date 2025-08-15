#!/bin/bash

# Kira System Detection Script
# This script gathers comprehensive system information for Kira AI

echo "🔍 Detecting system information..."

# Create JSON output
cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "system": {
    "hostname": "$(hostname)",
    "username": "$(whoami)",
    "home_directory": "$HOME",
    "current_directory": "$(pwd)",
    "shell": "$SHELL",
    "shell_version": "$(bash --version | head -n1)",
    "terminal": "$TERM",
    "display": "$DISPLAY"
  },
  "os": {
    "kernel": "$(uname -s)",
    "kernel_version": "$(uname -r)",
    "architecture": "$(uname -m)",
    "platform": "$(uname -p)",
    "os_release": $(cat /etc/os-release 2>/dev/null | grep -E '^(NAME|VERSION|ID|VERSION_ID|PRETTY_NAME)=' | sed 's/^/    "/' | sed 's/=/":" /' | sed 's/$/",/' | sed '$ s/,$//' | tr '\n' ' ' | sed 's/ *$//' || echo '{}')
  },
  "hardware": {
    "cpu_info": "$(lscpu | grep 'Model name' | cut -d':' -f2 | xargs)",
    "cpu_cores": "$(nproc)",
    "memory_total": "$(free -h | grep '^Mem:' | awk '{print $2}')",
    "memory_available": "$(free -h | grep '^Mem:' | awk '{print $7}')",
    "disk_usage": "$(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)"}')"
  },
  "package_managers": {
    "apt": $(command -v apt >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "apt-get": $(command -v apt-get >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "yum": $(command -v yum >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "dnf": $(command -v dnf >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "pacman": $(command -v pacman >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "zypper": $(command -v zypper >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "apk": $(command -v apk >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "snap": $(command -v snap >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "flatpak": $(command -v flatpak >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "npm": $(command -v npm >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "pip": $(command -v pip >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "pip3": $(command -v pip3 >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "cargo": $(command -v cargo >/dev/null 2>&1 && echo 'true' || echo 'false')
  },
  "development_tools": {
    "git": $(command -v git >/dev/null 2>&1 && echo '"'$(git --version)'"' || echo 'false'),
    "node": $(command -v node >/dev/null 2>&1 && echo '"'$(node --version)'"' || echo 'false'),
    "python": $(command -v python >/dev/null 2>&1 && echo '"'$(python --version 2>&1)'"' || echo 'false'),
    "python3": $(command -v python3 >/dev/null 2>&1 && echo '"'$(python3 --version 2>&1)'"' || echo 'false'),
    "docker": $(command -v docker >/dev/null 2>&1 && echo '"'$(docker --version)'"' || echo 'false'),
    "code": $(command -v code >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "vim": $(command -v vim >/dev/null 2>&1 && echo '"'$(vim --version | head -1)'"' || echo 'false'),
    "nano": $(command -v nano >/dev/null 2>&1 && echo '"'$(nano --version | head -1)'"' || echo 'false'),
    "emacs": $(command -v emacs >/dev/null 2>&1 && echo '"'$(emacs --version | head -1)'"' || echo 'false')
  },
  "desktop_environment": {
    "desktop_session": "$DESKTOP_SESSION",
    "xdg_current_desktop": "$XDG_CURRENT_DESKTOP",
    "gdm_session": "$GDMSESSION",
    "kde_session_version": "$KDE_SESSION_VERSION",
    "gnome_desktop_session_id": "$GNOME_DESKTOP_SESSION_ID"
  },
  "network": {
    "hostname_fqdn": "$(hostname -f 2>/dev/null || hostname)",
    "ip_address": "$(hostname -I | awk '{print $1}' 2>/dev/null || echo 'unknown')",
    "internet_connection": $(ping -c 1 8.8.8.8 >/dev/null 2>&1 && echo 'true' || echo 'false')
  },
  "paths": {
    "path": "$PATH",
    "ld_library_path": "$LD_LIBRARY_PATH",
    "config_dirs": "$XDG_CONFIG_DIRS",
    "data_dirs": "$XDG_DATA_DIRS"
  }
}
EOF