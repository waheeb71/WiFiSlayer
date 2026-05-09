# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Advanced Attacks Menu
Placeholder and router for advanced attacks (WPS, PMKID, Evil Twin, Auto-Pwn).
"""

from core.ui import console, print_sub_menu, print_error, print_warning
from config import get_text
from modules.wps import wps_menu
from modules.pmkid import pmkid_menu
from modules.flood import flood_menu
from modules.eviltwin import eviltwin_menu
from modules.autopwn import autopwn_menu


def advanced_menu(current_interface=None):
    """Advanced Attacks sub-menu."""
    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🔓", "هجوم WPS (Pixie Dust / Reaver)"),
                ("2", "📡", "هجوم PMKID (Client-less)"),
                ("3", "🌪️", "إغراق الشبكات (Beacon Flooding)"),
                ("4", "🎣", "التوأم الشرير (Evil Twin)"),
                ("5", "🤖", "الطيار الآلي (Auto-Pwn)"),
            ]
        else:
            options = [
                ("1", "🔓", "WPS Attack (Pixie Dust / Reaver)"),
                ("2", "📡", "PMKID Attack (Client-less)"),
                ("3", "🌪️", "Beacon Flooding (mdk4)"),
                ("4", "🎣", "Evil Twin Attack"),
                ("5", "🤖", "Auto-Pwn Mode"),
            ]

        title = "🔥 " + get_text("menu_advanced")
        print_sub_menu(title, options)

        choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ").strip()

        if choice == "1":
            wps_menu(current_interface)
        elif choice == "2":
            pmkid_menu(current_interface)
        elif choice == "3":
            flood_menu(current_interface)
        elif choice == "4":
            eviltwin_menu(current_interface)
        elif choice == "5":
            autopwn_menu(current_interface)
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))
