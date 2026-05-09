# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Wordlist Generator Module
Generate custom wordlists using crunch.
"""

import os
from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_info, print_sub_menu, confirm_action
)
from core.validator import safe_input, validate_crunch_range
from config import get_text


def wordlist_menu():
    """Wordlist generation sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🔢", "أرقام فقط (0-9)"),
                ("2", "🔤", "حروف صغيرة (a-z)"),
                ("3", "🔠", "حروف + أرقام"),
                ("4", "🎲", "مخصص (أدخل الأحرف)"),
            ]
        else:
            options = [
                ("1", "🔢", "Numbers Only (0-9)"),
                ("2", "🔤", "Lowercase Letters (a-z)"),
                ("3", "🔠", "Letters + Numbers"),
                ("4", "🎲", "Custom Characters"),
            ]
        print_sub_menu("📝 " + get_text("menu_wordlist"), options)
        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        charsets = {
            "1": "0123456789",
            "2": "abcdefghijklmnopqrstuvwxyz",
            "3": "abcdefghijklmnopqrstuvwxyz0123456789",
        }

        if choice in charsets:
            generate_wordlist(charsets[choice])
        elif choice == "4":
            chars = safe_input("Enter characters / أدخل الأحرف", console=console)
            if chars:
                generate_wordlist(chars)
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


def generate_wordlist(charset=None):
    """Generate a wordlist using crunch."""
    print_section("Generate Wordlist")

    range_str = safe_input(
        "Enter length range (MIN MAX, e.g. 8 12) / أدخل المدى",
        validate_crunch_range, console,
    )
    if not range_str:
        return
    min_len, max_len = range_str

    output = safe_input("Output file name / اسم ملف الحفظ", console=console)
    if not output:
        output = "wordlist.txt"
    if not output.endswith(".txt"):
        output += ".txt"

    output_path = output

    # Estimate size
    if charset:
        import math
        total = sum(len(charset) ** i for i in range(min_len, max_len + 1))
        size_mb = (total * (max_len + 1)) / (1024 * 1024)
        print_info(f"Estimated: ~{total:,} words, ~{size_mb:,.1f} MB")
        if size_mb > 1000:
            if not confirm_action(f"File may be {size_mb:,.0f} MB. Continue?"):
                return

    log.info(f"Generating wordlist: range={min_len}-{max_len}, output={output_path}")
    print_info(f"{get_text('generating_wordlist')} [bold]{output}[/] ...")
    console.print()

    if charset:
        os.system(f"crunch {min_len} {max_len} '{charset}' -o '{output_path}'")
    else:
        os.system(f"crunch {min_len} {max_len} -o '{output_path}'")

    if os.path.exists(output_path):
        size = os.path.getsize(output_path)
        size_str = f"{size / 1024 / 1024:.1f} MB" if size > 1024 * 1024 else f"{size / 1024:.1f} KB"
        print_success(f"Wordlist saved → [bold]{output}[/] ({size_str})")
    else:
        print_error("Wordlist file not found after generation")
