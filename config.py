# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — Configuration & Environment
Central configuration for paths, tools, UI, and translation strings.
"""

import os
from pathlib import Path

# ─── Tool Meta ────────────────────────────────────────────────
TOOL_NAME = "WiFiSlayer"
TOOL_VERSION = "3.0"
DEVELOPER = "waheeb Al-Humaeri"
TELEGRAM = "@run_kernel"

# ─── Paths ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAPS_DIR = os.path.join(BASE_DIR, "caps")
WORDLISTS_DIR = os.path.join(BASE_DIR, "wordlists")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
ARCHIVE_DIR = os.path.join(BASE_DIR, "archive")
HANDSHAKE_DIR = os.path.join(CAPS_DIR, "handshakes")

# Ensure required directories exist
for d in [CAPS_DIR, WORDLISTS_DIR, LOGS_DIR, ARCHIVE_DIR, HANDSHAKE_DIR]:
    os.makedirs(d, exist_ok=True)

# ─── Required System Packages ───────────────────────────────
REQUIRED_PACKAGES = [
    "aircrack-ng",
    "bettercap",
    "iw",
    "crunch",
    "macchanger",
    "reaver",
    "pixiewps",
    "hcxdumptool",
    "hcxtools",
    "mdk4",
    "hostapd",
    "dnsmasq"
]

# ─── Colors (for reference / fallback) ──────────────────────
# Most coloring is handled natively by Rich.
RED = "\033[1;31m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
PURPLE = "\033[1;35m"
CYAN = "\033[1;36m"
NC = "\033[0m"

# ─── Constants ──────────────────────────────────────────────
DEFAULT_WORDLISTS = [
    "/usr/share/wordlists/rockyou.txt",
    "/usr/share/wordlists/fasttrack.txt",
]

# ─── Global Language State ──────────────────────────────────
# Default language is English ("en"). User can change it.
LANGUAGE = "en"

def set_language(lang_code):
    global LANGUAGE
    LANGUAGE = lang_code if lang_code in TRANSLATIONS else "en"

# ─── Translation Dictionaries ───────────────────────────────
TRANSLATIONS = {
    "ar": {
        "welcome": "مرحباً بك في أداة اختراق الواي فاي",
        "choose_lang": "اختر لغة الواجهة:",
        "choose": "اختر",
        "back": "رجوع",
        "invalid_choice": "خيار غير صالح، حاول مرة أخرى.",
        "press_enter": "اضغط Enter للعودة...",
        "no_interfaces": "لم يتم اكتشاف أي واجهة شبكة لاسلكية.",
        "detected_interfaces": "الواجهات المكتشفة",
        "select_interface": "اختر واجهة شبكة",
        "enter_interface": "أدخل اسم الواجهة يدوياً",
        "not_linux": "تحذير: هذه الأداة مصممة لنظام Linux.",
        "root_required": "يجب تشغيل الأداة بصلاحية root (sudo).",
        "enter_duration": "أدخل مدة الهجوم بعدد الحزم (0 = لا نهائي)",
        "attack_cancelled": "تم إلغاء الهجوم بواسطة المستخدم.",
        
        "menu_scan": "فحص الشبكات",
        "menu_handshake": "مصافحة و كسر",
        "menu_crack": "كسر كلمة المرور",
        "menu_traffic": "تحليل حركة المرور",
        "menu_deauth": "هجمات إلغاء المصادقة",
        "menu_wordlist": "توليد قائمة كلمات",
        "menu_advanced": "🔥 هجمات متقدمة (WPS, PMKID, Evil Twin)",
        "menu_mac": "🎭 تغيير عنوان الماك (MAC Spoofing)",
        "menu_settings": "الإعدادات",
        "menu_exit": "خروج",
        
        "enter_mac": "أدخل الـ MAC للشبكة أو الجهاز",
        "enter_ip": "أدخل عنوان الـ IP الهدف",
        "enter_channel": "أدخل رقم القناة (Channel)",
        "enter_wordlist": "أدخل مسار قائمة الكلمات",
        "enter_handshake": "أدخل اسم أو مسار ملف المصافحة",
        "confirm_attack": "هل أنت متأكد من بدء هذا الهجوم؟",
        
        # New Internal Messages
        "no_interface": "لم يتم تحديد كارت شبكة.",
        "scan_stopped": "توقف الفحص.",
        "target": "الهدف:",
        "attack": "الهجوم:",
        "starting_attack": "بدء الهجوم...",
        "attack_stopped": "توقف الهجوم بواسطة المستخدم.",
        "generating_wordlist": "جاري إنشاء قائمة الكلمات...",
        "wordlist_saved": "تم حفظ قائمة الكلمات في:",
        "wordlist_error": "لم يتم العثور على ملف قائمة الكلمات بعد الإنشاء.",
        "estimated_size": "الحجم التقديري:",
        "probing_on": "جاري الفحص على",
        "sniff_started": "بدء التقاط حزم البيانات... (اضغط Ctrl+C للإيقاف)",
        "scanning_on": "جاري الفحص على",
        "monitoring_on": "جاري مراقبة الشبكة...",
        "enabling_monitor": "تفعيل وضع المراقبة (Monitor Mode)...",
        "monitor_enabled": "تم تفعيل وضع المراقبة بنجاح:",
        "monitor_failed": "فشل تفعيل وضع المراقبة.",
        "disabling_monitor": "إلغاء وضع المراقبة...",
        "monitor_disabled": "تم إيقاف وضع المراقبة.",
        "monitor_disable_failed": "فشل إيقاف وضع المراقبة.",
        "channel_changed": "تم تغيير القناة بنجاح إلى:",
        "channel_failed": "فشل تغيير القناة:",
        "capture_handshake": "التقاط مصافحة (Handshake)",
        "press_ctrl_c": "(اضغط Ctrl+C للإيقاف)",
        "handshake_saved": "تم حفظ ملف المصافحة:",
        "handshake_not_found": "لم يتم العثور على ملف المصافحة. قد يكون تم التقاطه في الخلفية.",
        "no_wordlists": "لا توجد قوائم كلمات افتراضية في النظام.",
        "cracking_with": "جاري الكسر باستخدام:",
        "password_found": "تم العثور على كلمة المرور! تحقق من المخرجات.",
        "converting_hccapx": "جاري تحويل الملف إلى صيغة hccapx...",
        "starting_hashcat": "بدء أداة Hashcat...",
        "mac_status": "حالة عنوان الماك (MAC Status)",
        "mac_not_installed": "أداة macchanger غير مثبتة.",
        "mac_updated": "تم تحديث عنوان الماك بنجاح!",
        "mac_failed": "فشل تغيير عنوان الماك:",
        "wps_scan": "فحص شبكات WPS",
        "pmkid_capture": "التقاط PMKID",
        "pmkid_warning": "هذا الهجوم يتطلب أن يدعم كارت الشبكة وضع المراقبة والحقن.",
        "pmkid_saved": "تم حفظ ملف الالتقاط:",
        "pmkid_failed": "فشل إنشاء ملف الالتقاط.",
        "pmkid_convert": "تحويل ملف PMKID إلى Hashcat",
        "pmkid_converted": "تم التحويل بنجاح:",
        "pmkid_convert_failed": "فشل التحويل. قد لا يحتوي الملف على هاش PMKID صالح.",
        "flood_warning": "هذا الهجوم سيقوم ببث مئات الشبكات الوهمية في المنطقة.",
        "flooding_started": "جاري إغراق المنطقة بالشبكات الوهمية...",
        "flooding_stopped": "توقف الإغراق.",
        "eviltwin_req": "هذا الهجوم يتطلب:",
        "eviltwin_req1": "1. كارت شبكة لبث الشبكة الوهمية (يدعم وضع AP).",
        "eviltwin_req2": "2. (اختياري) كارت شبكة آخر في وضع المراقبة لفصل الأجهزة.",
        "eviltwin_started": "تم تشغيل نقطة الاتصال الوهمية وخادم DHCP/DNS!",
        "eviltwin_portal": "بدء خادم بوابة تسجيل الدخول على المنفذ 80... (انتظر اتصال الضحية)",
        "eviltwin_stopping": "إيقاف هجوم التوأم الشرير...",
        "eviltwin_cleaned": "تم تنظيف واجهات الشبكة.",
        "autopwn_steps": "الطيار الآلي سيقوم بالخطوات التالية تلقائياً:",
        "autopwn_step1": "1. فحص محيطك للبحث عن أهداف (15 ثانية)",
        "autopwn_step2": "2. اختيار أقوى شبكة موجودة",
        "autopwn_step3": "3. إرسال حزم الطرد لفصل أجهزة الضحايا",
        "autopwn_step4": "4. التقاط مصافحة WPA/WPA2",
        "autopwn_step5": "5. التحقق من صلاحية المصافحة",
        "autopwn_step6": "6. محاولة الكسر باستخدام القوائم الافتراضية",
        "autopwn_confirm": "هل تريد بدء هجوم الطيار الآلي؟",
        "autopwn_scanning": "الخطوة 1: جاري الفحص عن أهداف لمدة 15 ثانية...",
        "autopwn_scan_failed": "فشل الفحص. لم يتم التقاط بيانات.",
        "autopwn_no_targets": "لم يتم العثور على شبكات WPA/WPA2.",
        "autopwn_target_found": "تم العثور على أفضل هدف:",
        "autopwn_capturing": "الخطوتين 3 و 4: جاري الالتقاط وإرسال حزم الطرد...",
        "autopwn_sending_deauth": "جاري إرسال حزم الطرد (Deauth)...",
        "autopwn_waiting": "انتظار 15 ثانية لالتقاط المصافحة...",
        "autopwn_validating": "الخطوة 5: التحقق من المصافحة...",
        "autopwn_failed_cap": "فشل إنشاء ملف الالتقاط .cap.",
        "autopwn_invalid_cap": "فشل الطيار الآلي: لم يتم التقاط مصافحة صالحة. ربما لا يوجد أجهزة متصلة بالهدف.",
        "autopwn_valid_cap": "تم التقاط مصافحة صالحة لـ",
        "autopwn_cracking": "الخطوة 6: محاولة الكسر بالقوائم الافتراضية...",
        "autopwn_pwned": "تم الاختراق! كلمة المرور للشبكة",
        "autopwn_saved": "تم حفظ ملف المصافحة للكسر لاحقاً بقائمة مخصصة.",
        "validating_handshake": "جاري فحص المصافحة...",
        "handshake_valid": "تم العثور على مصافحة صالحة! (Valid Handshake)",
        "handshake_invalid": "لم يتم التقاط مصافحة صالحة في هذا الملف.",
    },
    "en": {
        "welcome": "Welcome to WiFiSlayerTool",
        "choose_lang": "Select UI Language:",
        "choose": "Choose",
        "back": "Back",
        "invalid_choice": "Invalid choice, please try again.",
        "press_enter": "Press Enter to return...",
        "attack_cancelled": "Attack cancelled by user.",
        "no_interfaces": "No wireless interfaces detected.",
        "detected_interfaces": "Detected Interfaces",
        "select_interface": "Select interface",
        "enter_interface": "Enter interface name manually",
        "not_linux": "Warning: This tool is designed for Linux.",
        "root_required": "Must run as root (sudo).",
        "enter_duration": "Enter attack duration in packets (0 = infinite)",
        
        "menu_scan": "Scan Networks",
        "menu_handshake": "Handshake & Crack",
        "menu_crack": "Crack Password",
        "menu_traffic": "Traffic Analysis",
        "menu_deauth": "Deauthentication Attacks",
        "menu_wordlist": "Generate Wordlist",
        "menu_advanced": "🔥 Advanced Attacks (WPS, PMKID, Evil Twin)",
        "menu_mac": "🎭 MAC Spoofing",
        "menu_settings": "Settings",
        "menu_exit": "Exit",
        
        "enter_mac": "Enter target MAC (BSSID)",
        "enter_ip": "Enter target IP address",
        "enter_channel": "Enter channel number",
        "enter_wordlist": "Enter wordlist path",
        "enter_handshake": "Enter handshake file name or path",
        "confirm_attack": "Are you sure you want to start this attack?",

        # New Internal Messages
        "no_interface": "No interface selected.",
        "scan_stopped": "Scan stopped.",
        "target": "Target:",
        "attack": "Attack:",
        "starting_attack": "Starting attack...",
        "attack_stopped": "Attack stopped by user.",
        "generating_wordlist": "Generating wordlist...",
        "wordlist_saved": "Wordlist saved:",
        "wordlist_error": "Wordlist file not found after generation.",
        "estimated_size": "Estimated size:",
        "probing_on": "Probing on",
        "sniff_started": "Starting sniff session... (Press Ctrl+C to stop)",
        "scanning_on": "Scanning on",
        "monitoring_on": "Monitoring network...",
        "enabling_monitor": "Activating monitor mode...",
        "monitor_enabled": "Monitor mode active:",
        "monitor_failed": "Failed to enable monitor mode.",
        "disabling_monitor": "Disabling monitor mode...",
        "monitor_disabled": "Monitor mode disabled.",
        "monitor_disable_failed": "Failed to disable monitor mode.",
        "channel_changed": "Channel changed successfully to:",
        "channel_failed": "Failed to change channel:",
        "capture_handshake": "Capture Handshake",
        "press_ctrl_c": "(Press Ctrl+C to stop)",
        "handshake_saved": "Handshake saved:",
        "handshake_not_found": "Handshake file not detected. It may still have been captured.",
        "no_wordlists": "No default wordlists found on this system.",
        "cracking_with": "Cracking with:",
        "password_found": "Password found! Check output above.",
        "converting_hccapx": "Converting .cap to .hccapx format ...",
        "starting_hashcat": "Starting hashcat ...",
        "mac_status": "MAC Status",
        "mac_not_installed": "macchanger is not installed.",
        "mac_updated": "MAC Address updated successfully!",
        "mac_failed": "Failed to change MAC:",
        "wps_scan": "Scan WPS Networks (wash)",
        "pmkid_capture": "Capture PMKID",
        "pmkid_warning": "This attack requires the interface to support Monitor Mode and Injection.",
        "pmkid_saved": "Capture file saved:",
        "pmkid_failed": "Failed to create capture file.",
        "pmkid_convert": "Convert PMKID to Hashcat Format",
        "pmkid_converted": "Successfully converted to:",
        "pmkid_convert_failed": "Conversion failed. The file may not contain valid PMKID hashes.",
        "flood_warning": "This attack will broadcast hundreds of fake WiFi networks.",
        "flooding_started": "Flooding area with fake APs ...",
        "flooding_stopped": "Flooding stopped",
        "eviltwin_req": "This attack requires:",
        "eviltwin_req1": "1. An interface for the fake AP (managed mode, supports AP).",
        "eviltwin_req2": "2. (Optional) A second interface in monitor mode for deauth.",
        "eviltwin_started": "Fake AP and DHCP/DNS running!",
        "eviltwin_portal": "Starting Captive Portal Server on port 80... (Waiting for victim)",
        "eviltwin_stopping": "Stopping Evil Twin Attack...",
        "eviltwin_cleaned": "Cleaned up network interfaces.",
        "autopwn_steps": "Auto-Pwn will perform the following steps automatically:",
        "autopwn_step1": "1. Scan for targets (15 seconds)",
        "autopwn_step2": "2. Select the strongest network",
        "autopwn_step3": "3. Send Deauth packets to disconnect clients",
        "autopwn_step4": "4. Capture the WPA/WPA2 Handshake",
        "autopwn_step5": "5. Validate the handshake",
        "autopwn_step6": "6. Attempt to crack with default wordlists",
        "autopwn_confirm": "Do you want to start the Auto-Pwn sequence?",
        "autopwn_scanning": "STEP 1: Scanning for targets for 15 seconds...",
        "autopwn_scan_failed": "Scan failed. No data captured.",
        "autopwn_no_targets": "No WPA/WPA2 targets found.",
        "autopwn_target_found": "Best target found:",
        "autopwn_capturing": "STEP 3 & 4: Capturing handshake and sending deauth...",
        "autopwn_sending_deauth": "Sending Deauth packets...",
        "autopwn_waiting": "Waiting for handshake capture (15 seconds)...",
        "autopwn_validating": "STEP 5: Validating Handshake...",
        "autopwn_failed_cap": "Failed to generate .cap file.",
        "autopwn_invalid_cap": "Auto-Pwn failed: No valid handshake captured. Target might not have active clients.",
        "autopwn_valid_cap": "Valid handshake captured for",
        "autopwn_cracking": "STEP 6: Cracking with default wordlists...",
        "autopwn_pwned": "🔥 PWNED! Password cracked for",
        "autopwn_saved": "Handshake saved to file. Run custom crack later.",
        "validating_handshake": "Validating handshake...",
        "handshake_valid": "Valid handshake found! (WPA/WPA2)",
        "handshake_invalid": "No valid handshake captured in this file.",
    },
}

def get_text(key):
    """Retrieve a translation string based on the current global language."""
    return TRANSLATIONS.get(LANGUAGE, TRANSLATIONS["en"]).get(key, key)
