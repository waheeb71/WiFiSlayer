# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — MAC Spoofing Module
Change the MAC address of network interfaces for anonymity.
"""

import os
import subprocess

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
)
from config import get_text
from core.network import get_wireless_interfaces


def mac_spoof_menu(current_interface=None):
    """MAC Spoofing sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🎲", "عنوان MAC عشوائي (Random)"),
                ("2", "✏️", "إدخال MAC مخصص (Custom)"),
                ("3", "🔄", "استعادة الـ MAC الأصلي (Restore Original)"),
                ("4", "ℹ️", "عرض حالة الـ MAC الحالي"),
            ]
        else:
            options = [
                ("1", "🎲", "Random MAC Address"),
                ("2", "✏️", "Custom MAC Address"),
                ("3", "🔄", "Restore Original MAC"),
                ("4", "ℹ️", "Show Current MAC Status"),
            ]

        title = "🎭 " + get_text("menu_mac")
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            change_mac(current_interface, mode="random")
        elif choice == "2":
            change_mac(current_interface, mode="custom")
        elif choice == "3":
            change_mac(current_interface, mode="restore")
        elif choice == "4":
            show_mac_status(current_interface)
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def _prepare_interface(interface):
    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
    return interface


def show_mac_status(interface=None):
    """Show current MAC using macchanger."""
    print_section(get_text("mac_status"))
    interface = _prepare_interface(interface)
    if not interface:
        print_error(get_text("no_interface"))
        return

    try:
        result = subprocess.run(["macchanger", "-s", interface], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"\n[bold bright_cyan]{result.stdout.strip()}[/]\n")
        else:
            print_error(f"Could not get MAC status: {result.stderr.strip()}")
    except FileNotFoundError:
        print_error(get_text("mac_not_installed"))


def change_mac(interface=None, mode="random"):
    """Change MAC address using macchanger."""
    print_section(f"Change MAC: {mode.capitalize()}")
    interface = _prepare_interface(interface)
    if not interface:
        print_error(get_text("no_interface"))
        return

    # Check if interface is in monitor mode, changing MAC on monitor interfaces
    # can be tricky, but we'll bring it down first.
    print_info(f"Taking down interface [bold]{interface}[/] ...")
    os.system(f"sudo ip link set {interface} down")

    if mode == "random":
        cmd = ["sudo", "macchanger", "-r", interface]
    elif mode == "restore":
        cmd = ["sudo", "macchanger", "-p", interface]
    elif mode == "custom":
        from core.validator import safe_input, validate_mac
        mac = safe_input(get_text("enter_mac"), validate_mac, console)
        if not mac:
            os.system(f"sudo ip link set {interface} up")
            return
        cmd = ["sudo", "macchanger", "-m", mac, interface]

    try:
        log.info(f"Changing MAC for {interface} (Mode: {mode})")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Bring interface back up
        print_info(f"Bringing interface [bold]{interface}[/] up ...")
        os.system(f"sudo ip link set {interface} up")

        if result.returncode == 0:
            print_success(get_text("mac_updated"))
            # Extract and show the new MAC from output
            for line in result.stdout.splitlines():
                if "New MAC:" in line or "Faked MAC:" in line:
                    console.print(f"  [bold bright_green]{line.strip()}[/]")
        else:
            print_error(f"{get_text('mac_failed')} {result.stderr.strip()}")

    except FileNotFoundError:
        os.system(f"sudo ip link set {interface} up")
        print_error(get_text("mac_not_installed"))
