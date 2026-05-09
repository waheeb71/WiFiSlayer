# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Network Utilities
Auto-detects wireless interfaces and manages monitor mode.
"""

import subprocess
import re

from core.logger import log


def get_wireless_interfaces():
    """
    Auto-detect all wireless network interfaces.
    Returns a list of dicts: [{"name": "wlan0", "mode": "Managed", "driver": "..."}]
    """
    interfaces = []
    try:
        result = subprocess.run(
            ["iw", "dev"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            current_iface = None
            for line in result.stdout.splitlines():
                line = line.strip()
                if line.startswith("Interface"):
                    current_iface = {"name": line.split()[-1], "mode": "Unknown", "driver": ""}
                elif line.startswith("type") and current_iface:
                    current_iface["mode"] = line.split()[-1].capitalize()
                    interfaces.append(current_iface)
                    current_iface = None

        # Fallback: scan /sys/class/net
        if not interfaces:
            result2 = subprocess.run(
                ["bash", "-c", "ls /sys/class/net/*/wireless 2>/dev/null"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result2.returncode == 0:
                for path in result2.stdout.strip().splitlines():
                    # /sys/class/net/wlan0/wireless
                    parts = path.split("/")
                    if len(parts) >= 5:
                        iface_name = parts[4]
                        interfaces.append(
                            {"name": iface_name, "mode": "Managed", "driver": ""}
                        )

        log.info(f"Detected {len(interfaces)} wireless interface(s): "
                 f"{[i['name'] for i in interfaces]}")

    except FileNotFoundError:
        log.warning("'iw' command not found. Install with: sudo apt install iw")
    except subprocess.TimeoutExpired:
        log.warning("Interface detection timed out")
    except Exception as e:
        log.error(f"Error detecting interfaces: {e}")

    return interfaces


def enable_monitor_mode(interface):
    """
    Enable monitor mode on the given interface.
    Returns the new monitor interface name (e.g., wlan0mon).
    """
    try:
        log.info(f"Enabling monitor mode on {interface}")

        # Kill interfering processes
        subprocess.run(
            ["sudo", "airmon-ng", "check", "kill"],
            capture_output=True,
            timeout=15,
        )

        # Start monitor mode
        result = subprocess.run(
            ["sudo", "airmon-ng", "start", interface],
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode == 0:
            # Try to detect the new monitor interface name
            output = result.stdout
            # Look for pattern: (mac80211 monitor mode vif enabled on wlan0mon)
            match = re.search(r"enabled on\s+(\S+)", output, re.IGNORECASE)
            if match:
                mon_iface = match.group(1).rstrip(")")
                log.info(f"Monitor mode enabled: {mon_iface}")
                return mon_iface

            # Fallback: append "mon"
            mon_iface = f"{interface}mon"
            log.info(f"Monitor mode enabled (assumed): {mon_iface}")
            return mon_iface
        else:
            log.error(f"airmon-ng failed: {result.stderr}")
            return None

    except FileNotFoundError:
        log.error("airmon-ng not found. Install aircrack-ng suite.")
        return None
    except subprocess.TimeoutExpired:
        log.error("Monitor mode activation timed out")
        return None
    except Exception as e:
        log.error(f"Error enabling monitor mode: {e}")
        return None


def disable_monitor_mode(interface):
    """Disable monitor mode and restore managed mode."""
    try:
        log.info(f"Disabling monitor mode on {interface}")
        result = subprocess.run(
            ["sudo", "airmon-ng", "stop", interface],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            log.info("Monitor mode disabled successfully")
            return True
        else:
            log.error(f"Failed to disable monitor mode: {result.stderr}")
            return False
    except Exception as e:
        log.error(f"Error disabling monitor mode: {e}")
        return False


def check_root():
    """Check if the tool is running with root privileges."""
    import os
    return os.geteuid() == 0


def check_package_installed(package_name):
    """Check if a system package is installed."""
    try:
        result = subprocess.run(
            ["dpkg", "-l", package_name],
            capture_output=True,
            timeout=5,
        )
        return result.returncode == 0
    except Exception:
        return False


def install_package(package_name):
    """Install a system package using apt."""
    try:
        log.info(f"Installing package: {package_name}")
        result = subprocess.run(
            ["sudo", "apt", "install", "-y", package_name],
            timeout=120,
        )
        return result.returncode == 0
    except Exception as e:
        log.error(f"Failed to install {package_name}: {e}")
        return False
