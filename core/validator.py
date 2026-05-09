# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Input Validator
Validates all user inputs to prevent crashes and command injection.
"""

import re
import os


def validate_mac(mac_address):
    """
    Validate a MAC address format (XX:XX:XX:XX:XX:XX).
    Returns (True, cleaned_mac) or (False, error_message).
    """
    mac_address = mac_address.strip().upper()
    # Accept both : and - separators
    mac_address = mac_address.replace("-", ":")
    pattern = r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$"
    if re.match(pattern, mac_address):
        return True, mac_address
    return False, "Invalid MAC address format. Use XX:XX:XX:XX:XX:XX"


def validate_interface(name):
    """
    Validate a network interface name.
    Returns (True, cleaned_name) or (False, error_message).
    """
    name = name.strip()
    if not name:
        return False, "Interface name cannot be empty"
    # Typical interface names: wlan0, wlan1, wlp2s0, eth0, mon0, wlan0mon
    pattern = r"^[a-zA-Z][a-zA-Z0-9_-]{0,15}$"
    if re.match(pattern, name):
        return True, name
    return False, "Invalid interface name format"


def validate_channel(channel):
    """
    Validate a WiFi channel number (1-196).
    Returns (True, channel_int) or (False, error_message).
    """
    try:
        ch = int(channel)
        if 1 <= ch <= 196:
            return True, ch
        return False, "Channel must be between 1 and 196"
    except (ValueError, TypeError):
        return False, "Channel must be a number"


def validate_ip(ip_address):
    """
    Validate an IPv4 address.
    Returns (True, cleaned_ip) or (False, error_message).
    """
    ip_address = ip_address.strip()
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if re.match(pattern, ip_address):
        parts = ip_address.split(".")
        if all(0 <= int(p) <= 255 for p in parts):
            return True, ip_address
    return False, "Invalid IP address format. Use X.X.X.X"


def validate_file_path(path):
    """
    Validate that a file path exists.
    Returns (True, abs_path) or (False, error_message).
    """
    path = path.strip()
    expanded = os.path.expanduser(path)
    if os.path.isfile(expanded):
        return True, os.path.abspath(expanded)
    return False, f"File not found: {path}"


def validate_duration(duration):
    """
    Validate attack duration (0 = infinite, or positive int).
    Returns (True, duration_int) or (False, error_message).
    """
    try:
        d = int(duration)
        if d >= 0:
            return True, d
        return False, "Duration must be 0 or positive"
    except (ValueError, TypeError):
        return False, "Duration must be a number"


def validate_crunch_range(range_str):
    """
    Validate crunch range format (e.g., '8 8' or '4 12').
    Returns (True, (min, max)) or (False, error_message).
    """
    try:
        parts = range_str.strip().split()
        if len(parts) != 2:
            return False, "Format: MIN MAX (e.g., 8 12)"
        min_len, max_len = int(parts[0]), int(parts[1])
        if min_len < 1:
            return False, "Minimum length must be at least 1"
        if max_len < min_len:
            return False, "Maximum length must be >= minimum length"
        if max_len > 32:
            return False, "Maximum length cannot exceed 32"
        return True, (min_len, max_len)
    except (ValueError, TypeError):
        return False, "Range values must be numbers"


def sanitize_command_arg(arg):
    """
    Sanitize a string to be safely used as a command argument.
    Removes shell-dangerous characters.
    """
    # Allow only safe characters
    return re.sub(r"[^a-zA-Z0-9_\-\.:/~]", "", arg.strip())


def safe_input(prompt, validator=None, console=None):
    """
    Get user input with optional validation and crash protection.
    Uses Rich console if provided, falls back to built-in input().
    
    Args:
        prompt: The prompt text to display.
        validator: Optional validation function that returns (bool, value_or_error).
        console: Optional Rich Console instance.
        
    Returns:
        The validated input value, or raw input if no validator.
    """
    while True:
        try:
            if console:
                value = console.input(f"[cyan]  ➤ {prompt}: [/]")
            else:
                value = input(f"  ➤ {prompt}: ")

            value = value.strip()
            if not value:
                msg = "Input cannot be empty"
                if console:
                    console.print(f"  [red]✗ {msg}[/]")
                else:
                    print(f"  ✗ {msg}")
                continue

            if validator:
                is_valid, result = validator(value)
                if is_valid:
                    return result
                else:
                    if console:
                        console.print(f"  [red]✗ {result}[/]")
                    else:
                        print(f"  ✗ {result}")
            else:
                return value

        except (KeyboardInterrupt, EOFError):
            print()
            return None
