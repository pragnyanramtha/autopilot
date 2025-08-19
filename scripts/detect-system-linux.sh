#!/bin/bash

# Enhanced Linux System Detection Script
# Collects comprehensive system information for AI analysis

echo "{"

# Basic system information
echo "  \"timestamp\": \"$(date -Iseconds)\","
echo "  \"platform\": \"linux\","

# OS Release information
echo "  \"os_release\": {"
if [ -f /etc/os-release ]; then
    while IFS='=' read -r key value; do
        if [[ $key && $value ]]; then
            # Remove quotes from value
            value=$(echo "$value" | sed 's/^"//;s/"$//')
            echo "    \"$key\": \"$value\","
        fi
    done < /etc/os-release | sed '$ s/,$//'
fi
echo "  },"

# System information
echo "  \"system\": {"
echo "    \"hostname\": \"$(hostname)\","
echo "    \"kernel\": \"$(uname -s)\","
echo "    \"kernel_version\": \"$(uname -r)\","
echo "    \"architecture\": \"$(uname -m)\","
echo "    \"uptime\": \"$(uptime -p 2>/dev/null || uptime)\","
echo "    \"shell\": \"$SHELL\","
echo "    \"user\": \"$(whoami)\","
echo "    \"home\": \"$HOME\""
echo "  },"

# Hardware information
echo "  \"hardware\": {"
echo "    \"cpu_model\": \"$(grep 'model name' /proc/cpuinfo | head -1 | cut -d: -f2 | sed 's/^ *//')\","
echo "    \"cpu_cores\": \"$(nproc)\","
echo "    \"memory_total\": \"$(free -h | grep '^Mem:' | awk '{print $2}')\","
echo "    \"memory_available\": \"$(free -h | grep '^Mem:' | awk '{print $7}')\","
echo "    \"disk_usage\": \"$(df -h / | tail -1 | awk '{print $3 \"/\" $2 \" (\" $5 \" used)\"}')\""
echo "  },"

# Package managers detection
echo "  \"package_managers\": {"
managers=("apt" "yum" "dnf" "pacman" "zypper" "apk" "snap" "flatpak" "brew")
first=true
for manager in "${managers[@]}"; do
    if ! $first; then echo ","; fi
    first=false
    if command -v "$manager" >/dev/null 2>&1; then
        version=$(${manager} --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || "unknown")
        echo -n "    \"$manager\": {\"available\": true, \"version\": \"$version\"}"
    else
        echo -n "    \"$manager\": {\"available\": false}"
    fi
done
echo ""
echo "  },"

# Development tools
echo "  \"development_tools\": {"
tools=("git" "node" "npm" "python3" "pip3" "docker" "curl" "wget" "vim" "nano" "code")
first=true
for tool in "${tools[@]}"; do
    if ! $first; then echo ","; fi
    first=false
    if command -v "$tool" >/dev/null 2>&1; then
        version=$(${tool} --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || "installed")
        echo -n "    \"$tool\": {\"available\": true, \"version\": \"$version\"}"
    else
        echo -n "    \"$tool\": {\"available\": false}"
    fi
done
echo ""
echo "  },"

# Network information
echo "  \"network\": {"
echo "    \"hostname_fqdn\": \"$(hostname -f 2>/dev/null || hostname)\","
echo "    \"ip_address\": \"$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K\S+' || echo 'unknown')\","
echo "    \"internet_connection\": $(ping -c 1 8.8.8.8 >/dev/null 2>&1 && echo "true" || echo "false")"
echo "  },"

# Distribution-specific information
echo "  \"distribution\": {"
if [ -f /etc/debian_version ]; then
    echo "    \"family\": \"debian\","
    echo "    \"version\": \"$(cat /etc/debian_version)\","
    echo "    \"primary_package_manager\": \"apt\""
elif [ -f /etc/redhat-release ]; then
    echo "    \"family\": \"redhat\","
    echo "    \"version\": \"$(cat /etc/redhat-release)\","
    if command -v dnf >/dev/null 2>&1; then
        echo "    \"primary_package_manager\": \"dnf\""
    else
        echo "    \"primary_package_manager\": \"yum\""
    fi
elif [ -f /etc/arch-release ]; then
    echo "    \"family\": \"arch\","
    echo "    \"version\": \"rolling\","
    echo "    \"primary_package_manager\": \"pacman\""
elif [ -f /etc/alpine-release ]; then
    echo "    \"family\": \"alpine\","
    echo "    \"version\": \"$(cat /etc/alpine-release)\","
    echo "    \"primary_package_manager\": \"apk\""
else
    echo "    \"family\": \"unknown\","
    echo "    \"version\": \"unknown\","
    echo "    \"primary_package_manager\": \"unknown\""
fi
echo "  }"

echo "}"