#!/bin/bash

# Enhanced macOS System Detection Script
# Collects comprehensive system information for AI analysis

echo "{"

# Basic system information
echo "  \"timestamp\": \"$(date -Iseconds)\","
echo "  \"platform\": \"darwin\","

# macOS version information using sw_vers
echo "  \"os_release\": {"
echo "    \"PRETTY_NAME\": \"$(sw_vers -productName) $(sw_vers -productVersion)\","
echo "    \"NAME\": \"$(sw_vers -productName)\","
echo "    \"VERSION\": \"$(sw_vers -productVersion)\","
echo "    \"BUILD_ID\": \"$(sw_vers -buildVersion)\","
echo "    \"ID\": \"macos\""
echo "  },"

# System information
echo "  \"system\": {"
echo "    \"hostname\": \"$(hostname)\","
echo "    \"kernel\": \"$(uname -s)\","
echo "    \"kernel_version\": \"$(uname -r)\","
echo "    \"architecture\": \"$(uname -m)\","
echo "    \"uptime\": \"$(uptime | sed 's/.*up //' | sed 's/, [0-9]* user.*//')\","
echo "    \"shell\": \"$SHELL\","
echo "    \"user\": \"$(whoami)\","
echo "    \"home\": \"$HOME\""
echo "  },"

# Hardware information using system_profiler
echo "  \"hardware\": {"
echo "    \"cpu_model\": \"$(sysctl -n machdep.cpu.brand_string)\","
echo "    \"cpu_cores\": \"$(sysctl -n hw.ncpu)\","
echo "    \"memory_total\": \"$(echo \"$(sysctl -n hw.memsize) / 1024 / 1024 / 1024\" | bc)GB\","
echo "    \"memory_available\": \"$(vm_stat | grep 'Pages free' | awk '{print int($3 * 4096 / 1024 / 1024)}')MB\","
echo "    \"disk_usage\": \"$(df -h / | tail -1 | awk '{print $3 \"/\" $2 \" (\" $5 \" used)\"}')\""
echo "  },"

# Package managers detection (focus on macOS-specific ones)
echo "  \"package_managers\": {"
managers=("brew" "port" "npm" "pip3" "gem" "cargo")
first=true
for manager in "${managers[@]}"; do
    if ! $first; then echo ","; fi
    first=false
    if command -v "$manager" >/dev/null 2>&1; then
        case $manager in
            "brew")
                version=$(brew --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || "unknown")
                ;;
            "port")
                version=$(port version 2>/dev/null | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || "unknown")
                ;;
            *)
                version=$(${manager} --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || "unknown")
                ;;
        esac
        echo -n "    \"$manager\": {\"available\": true, \"version\": \"$version\"}"
    else
        echo -n "    \"$manager\": {\"available\": false}"
    fi
done
echo ""
echo "  },"

# Development tools
echo "  \"development_tools\": {"
tools=("git" "node" "npm" "python3" "pip3" "docker" "curl" "wget" "vim" "nano" "code" "xcode-select")
first=true
for tool in "${tools[@]}"; do
    if ! $first; then echo ","; fi
    first=false
    if command -v "$tool" >/dev/null 2>&1; then
        case $tool in
            "xcode-select")
                if xcode-select -p >/dev/null 2>&1; then
                    version="installed"
                else
                    version="not_installed"
                fi
                ;;
            *)
                version=$(${tool} --version 2>/dev/null | head -1 | grep -oE '[0-9]+\.[0-9]+(\.[0-9]+)?' | head -1 || "installed")
                ;;
        esac
        echo -n "    \"$tool\": {\"available\": true, \"version\": \"$version\"}"
    else
        echo -n "    \"$tool\": {\"available\": false}"
    fi
done
echo ""
echo "  },"

# Network information
echo "  \"network\": {"
echo "    \"hostname_fqdn\": \"$(hostname)\","
echo "    \"ip_address\": \"$(route get default 2>/dev/null | grep interface | awk '{print $2}' | xargs ifconfig 2>/dev/null | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | head -1 || echo 'unknown')\","
echo "    \"internet_connection\": $(ping -c 1 8.8.8.8 >/dev/null 2>&1 && echo "true" || echo "false")"
echo "  },"

# macOS-specific information
echo "  \"distribution\": {"
echo "    \"family\": \"darwin\","
echo "    \"version\": \"$(sw_vers -productVersion)\","
if command -v brew >/dev/null 2>&1; then
    echo "    \"primary_package_manager\": \"brew\","
    echo "    \"homebrew_prefix\": \"$(brew --prefix)\","
    echo "    \"homebrew_installed\": true"
elif command -v port >/dev/null 2>&1; then
    echo "    \"primary_package_manager\": \"port\","
    echo "    \"homebrew_installed\": false"
else
    echo "    \"primary_package_manager\": \"none\","
    echo "    \"homebrew_installed\": false"
fi
echo "  }"

echo "}"