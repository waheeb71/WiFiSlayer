# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║               WiFiSlayerTool v3.0                        ║
║               Developer: waheeb Al-Humaeri                  ║
║               GitHub: github.com/waheeb71                   ║
║               Telegram: @SyberSc71                          ║
╚══════════════════════════════════════════════════════════════╝

A professional WiFi security auditing tool for ethical hackers
and penetration testers. Built for Kali Linux.

Usage:
    sudo python3 main.py
"""

import sys
import os
import platform

# ─── Ensure we can import our packages ───────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config
from config import get_text, set_language


def check_dependencies():
    """Check and report missing Python dependencies."""
    missing = []
    try:
        import rich  # noqa: F401
    except ImportError:
        missing.append("rich")
    try:
        import termcolor  # noqa: F401
    except ImportError:
        missing.append("termcolor")

    if missing:
        print(f"\n  [!] Missing Python packages: {', '.join(missing)}")
        print(f"  [*] Install with: pip3 install {' '.join(missing)}")
        print(f"  [*] Or run: pip3 install -r requirements.txt\n")
        sys.exit(1)


def check_platform():
    """Warn if not running on Linux."""
    if platform.system() != "Linux":
        try:
            from core.ui import console, print_warning
            print_warning(get_text("not_linux"))
            print_warning("Some features require Linux + aircrack-ng suite")
            console.print()
        except Exception:
            print("  [!] Warning: This tool is designed for Linux")


def check_root():
    """Check for root privileges."""
    try:
        if os.geteuid() != 0:
            try:
                from core.ui import print_error
                print_error(get_text("root_required"))
                print_error("Run with: sudo python3 main.py")
            except Exception:
                print("  [!] Run as root: sudo python3 main.py")
            sys.exit(1)
    except AttributeError:
        # Windows doesn't have geteuid
        pass


def select_language():
    """Prompt user to select language at startup."""
    from core.ui import console, print_language_selector

    print_language_selector()
    choice = console.input("\n  [bold bright_cyan]➤ Choose / اختر (1/2):[/] ").strip()

    if choice == "1":
        set_language("ar")
    else:
        set_language("en")


def check_system_packages():
    """Check if required system packages are installed."""
    from core.network import check_package_installed
    from core.ui import print_info, print_warning, print_success

    missing = []
    for pkg in config.REQUIRED_PACKAGES:
        if not check_package_installed(pkg):
            missing.append(pkg)

    if missing:
        print_warning(f"Missing packages: {', '.join(missing)}")
        print_info("Install with: sudo bash install.sh")
    else:
        print_success("All system packages are installed ✓")


def main():
    """Main application entry point."""

    # ─── Pre-flight Checks ───────────────────────────────────
    check_dependencies()

    from core.ui import (
        console, print_banner, print_status_bar, print_main_menu,
        get_menu_choice, print_info, print_success, print_error,
        print_section,
    )
    from core.network import get_wireless_interfaces
    from core.logger import log
    from modules.scanner import scanner_menu
    from modules.handshake import handshake_menu, crack_menu
    from modules.attacker import attacker_menu
    from modules.traffic import traffic_menu
    from modules.wordlist import wordlist_menu
    from modules.mac_spoof import mac_spoof_menu
    from modules.advanced import advanced_menu

    # ─── Clear screen & show banner ──────────────────────────
    os.system("clear" if os.name != "nt" else "cls")
    print_banner()

    # ─── Language Selection ──────────────────────────────────
    select_language()

    # ─── Platform & Root ─────────────────────────────────────
    check_platform()
    # check_root()  # Uncomment on production Kali

    # ─── System Check ────────────────────────────────────────
    console.print()
    print_section("System Check")
    check_system_packages()

    # ─── Auto-detect Interface ───────────────────────────────
    interfaces = get_wireless_interfaces()
    current_interface = None
    current_mode = None

    if interfaces:
        current_interface = interfaces[0]["name"]
        current_mode = interfaces[0].get("mode", "Managed")
        print_success(
            f"Auto-detected interface: [bold]{current_interface}[/] "
            f"({current_mode})"
        )
    else:
        from core.ui import print_warning
        print_warning(get_text("no_interfaces"))

    log.info(f"Tool started. Interface={current_interface}, Lang={config.LANGUAGE}")

    # ═════════════════════════════════════════════════════════
    #  MAIN LOOP
    # ═════════════════════════════════════════════════════════
    while True:
        console.print()
        print_status_bar(current_interface, current_mode, config.LANGUAGE)
        print_main_menu()

        choice = get_menu_choice()

        if choice == 1:
            # Scanner
            result = scanner_menu(current_interface)
            if result:
                current_interface = result
                current_mode = "Monitor" if "mon" in result else "Managed"

        elif choice == 2:
            # Capture Handshake
            handshake_menu(current_interface)

        elif choice == 3:
            # Crack Password
            crack_menu()

        elif choice == 4:
            # Traffic Analysis
            traffic_menu(current_interface)

        elif choice == 5:
            # Deauth Attacks
            attacker_menu(current_interface)

        elif choice == 6:
            # Wordlist Generator
            wordlist_menu()

        elif choice == 7:
            # MAC Spoofing
            mac_spoof_menu(current_interface)

        elif choice == 8:
            # Advanced Attacks
            advanced_menu(current_interface)

        elif choice == 9:
            # Settings
            settings_menu(current_interface)

        elif choice == 0:
            # Exit
            console.print()
            log.info("Tool exited by user")
            print_info("Goodbye! Stay ethical, stay legal. 🛡️")
            console.print()
            break


def settings_menu(current_interface=None):
    """Settings sub-menu."""
    from core.ui import console, print_sub_menu, print_success, print_error, print_info
    from core.network import get_wireless_interfaces

    while True:
        console.print()
        if get_text("choose") == "اختر":
            options = [
                ("1", "🌐", "تغيير اللغة"),
                ("2", "📡", "تغيير الواجهة"),
                ("3", "📋", "فحص الحزم المثبتة"),
                ("4", "📂", "فتح مجلد السجلات"),
            ]
        else:
            options = [
                ("1", "🌐", "Change Language"),
                ("2", "📡", "Change Interface"),
                ("3", "📋", "Check Installed Packages"),
                ("4", "📂", "Open Logs Directory"),
            ]

        print_sub_menu("⚙️  " + get_text("menu_settings"), options)
        choice = console.input(
            f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] "
        ).strip()

        if choice == "1":
            select_language()
            print_success("Language updated ✓")
        elif choice == "2":
            from core.ui import select_interface
            interfaces = get_wireless_interfaces()
            iface = select_interface(interfaces)
            if iface:
                print_success(f"Interface set to: {iface}")
        elif choice == "3":
            check_system_packages()
        elif choice == "4":
            print_info(f"Logs directory: {config.LOGS_DIR}")
            os.system(f"ls -la {config.LOGS_DIR} 2>/dev/null || echo 'No logs yet'")
        elif choice == "0":
            break
        else:
            print_error(get_text("invalid_choice"))


# ═════════════════════════════════════════════════════════════
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Interrupted. Goodbye! 👋\n")
        sys.exit(0)
