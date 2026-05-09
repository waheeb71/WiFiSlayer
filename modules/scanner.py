# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Network Scanner Module
Scan nearby networks, display results, and manage monitor mode.
"""

import subprocess
import os

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
    confirm_action,
)
from core.validator import safe_input, validate_channel, validate_mac
from core.network import get_wireless_interfaces, enable_monitor_mode, disable_monitor_mode
from core.ascii_art import print_radar_art
from config import get_text


def scanner_menu(current_interface=None):
    """Display the scanner sub-menu and handle choices."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "📡", "عرض الشبكات القريبة (airodump-ng)"),
                ("2", "🔎", "عرض الأجهزة المتصلة بشبكة معينة"),
                ("3", "📻", "تفعيل وضع المراقبة (Monitor Mode)"),
                ("4", "📴", "إيقاف وضع المراقبة"),
                ("5", "📶", "تغيير القناة (Channel)"),
            ]
        else:
            options = [
                ("1", "📡", "Scan Nearby Networks (airodump-ng)"),
                ("2", "🔎", "Show Connected Devices on a Network"),
                ("3", "📻", "Enable Monitor Mode"),
                ("4", "📴", "Disable Monitor Mode"),
                ("5", "📶", "Change Channel"),
            ]

        title = "🔍 " + get_text("menu_scan")
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            scan_networks(current_interface)
        elif choice == "2":
            scan_specific_network(current_interface)
        elif choice == "3":
            new_iface = activate_monitor(current_interface)
            if new_iface:
                current_interface = new_iface
        elif choice == "4":
            deactivate_monitor(current_interface)
        elif choice == "5":
            change_channel(current_interface)
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))

    return current_interface


def scan_networks(interface=None):
    """Scan all nearby WiFi networks using airodump-ng."""
    os.system("clear" if os.name != "nt" else "cls")
    print_radar_art()
    print_section(get_text("menu_scan"))

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error(get_text("no_interface"))
            return

    print_info(f"{get_text('scanning_on')} [bold]{interface}[/]... {get_text('press_ctrl_c')}")
    console.print()

    try:
        os.system(f"sudo airodump-ng {interface}")
    except KeyboardInterrupt:
        console.print()
        print_info(get_text("scan_stopped"))

    log.info("Network scan completed")


def scan_specific_network(interface=None):
    """Scan a specific network to see connected devices."""
    print_section("Scan Specific Network")

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error("No interface selected")
            return

    mac = safe_input(get_text("enter_mac"), validate_mac, console)
    if not mac:
        return

    channel = safe_input(get_text("enter_channel"), validate_channel, console)
    if not channel:
        return

    log.info(f"Scanning network {mac} on channel {channel} via {interface}")
    print_info(f"Monitoring [bold]{mac}[/] on channel [bold]{channel}[/] ...")
    console.print()

    try:
        os.system(f"sudo airodump-ng -c {channel} --bssid {mac} {interface}")
    except KeyboardInterrupt:
        console.print()
        print_info("Scan stopped")


def activate_monitor(interface=None):
    """Enable monitor mode on an interface."""
    os.system("clear" if os.name != "nt" else "cls")
    print_section(get_text("enabling_monitor"))

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error(get_text("no_interface"))
            return

    print_info(f"{get_text('enabling_monitor')} [bold]{interface}[/]...")
    mon_iface = enable_monitor_mode(interface)

    if mon_iface:
        print_success(f"{get_text('monitor_enabled')} [bold]{mon_iface}[/]")
        return mon_iface
    else:
        print_error(get_text("monitor_failed"))
        return None


def deactivate_monitor(interface=None):
    """Disable monitor mode."""
    print_section("Disable Monitor Mode")

    if not interface:
        iface_name = safe_input(get_text("enter_interface"), console=console)
        if not iface_name:
            return
        interface = iface_name

    if disable_monitor_mode(interface):
        print_success("Monitor mode disabled")
    else:
        print_error("Failed to disable monitor mode")


def change_channel(interface=None):
    """Change the wireless channel for an interface."""
    print_section("Change Channel")

    if not interface:
        iface_name = safe_input(get_text("enter_interface"), console=console)
        if not iface_name:
            return
        interface = iface_name

    channel = safe_input(get_text("enter_channel"), validate_channel, console)
    if not channel:
        return

    log.info(f"Changing {interface} to channel {channel}")

    try:
        result = subprocess.run(
            ["sudo", "iwconfig", interface, "channel", str(channel)],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            print_success(f"Channel changed to [bold]{channel}[/]")
        else:
            print_error(f"Failed: {result.stderr.strip()}")
    except Exception as e:
        print_error(f"Error: {e}")
