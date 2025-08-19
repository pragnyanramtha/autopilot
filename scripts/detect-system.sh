#!/bin/bash

# AP System Detection Script
# This script gathers comprehensive system information for AP AI (Linux & macOS)

echo "🔍 Detecting system information..."

# Detect OS type
OS_TYPE="$(uname -s)"

# Get hostname (with fallback)
get_hostname() {
  if command -v hostname >/dev/null 2>&1; then
    hostname 2>/dev/null || echo "unknown"
  elif [ "$OS_TYPE" = "Darwin" ]; then
    scutil --get ComputerName 2>/dev/null || echo "unknown"
  else
    cat /proc/sys/kernel/hostname 2>/dev/null || echo "unknown"
  fi
}

# macOS-specific functions
get_macos_cpu_info() {
  if [ "$OS_TYPE" = "Darwin" ]; then
    sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "unknown"
  else
    echo "unknown"
  fi
}

get_macos_memory() {
  if [ "$OS_TYPE" = "Darwin" ]; then
    echo "$(( $(sysctl -n hw.memsize 2>/dev/null || echo 0) / 1024 / 1024 / 1024 ))GB"
  else
    echo "unknown"
  fi
}

get_macos_cores() {
  if [ "$OS_TYPE" = "Darwin" ]; then
    sysctl -n hw.ncpu 2>/dev/null || echo "unknown"
  else
    echo "unknown"
  fi
}

# Create JSON output
cat << EOF
{
  "timestamp": "$(date -Iseconds)",
  "system": {
    "hostname": "$(get_hostname)",
    "username": "$(whoami)",
    "home_directory": "$HOME",
    "current_directory": "$(pwd)",
    "shell": "$SHELL",
    "shell_version": "$(bash --version 2>/dev/null | head -n1 || echo 'unknown')",
    "terminal": "$TERM",
    "display": "$DISPLAY",
    "os_type": "$OS_TYPE"
  },
  "os": {
    "kernel": "$(uname -s)",
    "kernel_version": "$(uname -r)",
    "architecture": "$(uname -m)",
    "platform": "$(uname -p 2>/dev/null || uname -m)",
    "os_release": $(if [ "$OS_TYPE" = "Darwin" ]; then
      echo '{"NAME": "macOS", "VERSION": "'$(sw_vers -productVersion 2>/dev/null || echo 'unknown')'", "ID": "macos", "PRETTY_NAME": "macOS '$(sw_vers -productVersion 2>/dev/null || echo 'unknown')'"}'
    else
      cat /etc/os-release 2>/dev/null | grep -E '^(NAME|VERSION|ID|VERSION_ID|PRETTY_NAME)=' | sed 's/^/    "/' | sed 's/=/":" /' | sed 's/$/",/' | sed '$ s/,$//' | tr '\n' ' ' | sed 's/ *$//' || echo '{}'
    fi)
  },
  "hardware": {
    "cpu_info": "$(if [ "$OS_TYPE" = "Darwin" ]; then get_macos_cpu_info; else lscpu | grep 'Model name' | cut -d':' -f2 | xargs 2>/dev/null || echo 'unknown'; fi)",
    "cpu_cores": "$(if [ "$OS_TYPE" = "Darwin" ]; then get_macos_cores; else nproc 2>/dev/null || echo 'unknown'; fi)",
    "memory_total": "$(if [ "$OS_TYPE" = "Darwin" ]; then get_macos_memory; else free -h | grep '^Mem:' | awk '{print $2}' 2>/dev/null || echo 'unknown'; fi)",
    "memory_available": "$(if [ "$OS_TYPE" = "Darwin" ]; then echo 'N/A'; else free -h | grep '^Mem:' | awk '{print $7}' 2>/dev/null || echo 'unknown'; fi)",
    "disk_usage": "$(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " used)")' 2>/dev/null || echo 'unknown')"
  },
  "package_managers": {
    "brew": $(command -v brew >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "port": $(command -v port >/dev/null 2>&1 && echo 'true' || echo 'false'),
    "mas": $(command -v mas >/dev/null 2>&1 && echo 'true' || echo 'false'),
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
    "vim": $(command -v vim >/dev/null 2>&1 && echo '"'$(vim --version 2>/dev/null | head -1)'"' || echo 'false'),
    "nano": $(command -v nano >/dev/null 2>&1 && echo '"'$(nano --version 2>/dev/null | head -1)'"' || echo 'false'),
    "emacs": $(command -v emacs >/dev/null 2>&1 && echo '"'$(emacs --version 2>/dev/null | head -1)'"' || echo 'false'),
    "xcode": $(if [ "$OS_TYPE" = "Darwin" ]; then command -v xcodebuild >/dev/null 2>&1 && echo '"'$(xcodebuild -version | head -1)'"' || echo 'false'; else echo 'false'; fi)
  },
  "desktop_environment": {
    "desktop_session": "$DESKTOP_SESSION",
    "xdg_current_desktop": "$XDG_CURRENT_DESKTOP",
    "gdm_session": "$GDMSESSION",
    "kde_session_version": "$KDE_SESSION_VERSION",
    "gnome_desktop_session_id": "$GNOME_DESKTOP_SESSION_ID"
  },
  "network": {
    "hostname_fqdn": "$(hostname -f 2>/dev/null || get_hostname)",
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