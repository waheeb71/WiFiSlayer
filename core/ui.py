# -*- coding: utf-8 -*-
"""
WiFi Hacking Tool v3.0 — Rich UI Module
Professional terminal user interface using the Rich library.
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich import box
from rich.prompt import Prompt, Confirm
from rich.align import Align
import config
from config import get_text

# ─── Global Console ──────────────────────────────────────────
console = Console()


# الفن الأصلي (تم حفظه كما هو)
GHOST_ART = r"""
    ⠀⠀⠀⠀⠀⠀⠀⠀⠀                           ⠀⣀⡠⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⠟⠃⠀⠀⠙⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⠋⠀⠀⠀⠀⠀⠀⠘⣆⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠾⢛⠒⠀⠀⠀⠀⠀⠀⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣶⣄⡈⠓⢄⠠⡀⠀⠀⠀⣄⣷⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⣷⠀⠈⠱⡄⠑⣌⠆⠀⠀⡜⢻⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡿⠳⡆⠐⢿⣆⠈⢿⠀⠀⡇⠘⡆⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣷⡇⠀⠀⠈⢆⠈⠆⢸⠀⠀⢣⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣿⣿⣿⣧⠀⠀⠈⢂⠀⡇⠀⠀⢨⠓⣄⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣦⣤⠖⡏⡸⠀⣀⡴⠋⠀⠈⠢⡀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⠁⣹⣿⣿⣿⣷⣾⠽⠖⠊⢹⣀⠄⠀⠀⠀⠈⢣⡀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡟⣇⣰⢫⢻⢉⠉⠀⣿⡆⠀⠀⡸⡏⠀⠀⠀⠀⠀⠀⢇
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⡇⡇⠈⢸⢸⢸⠀⠀⡇⡇⠀⠀⠁⠻⡄⡠⠂⠀⠀⠀⠘
⢤⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠓⡇⠀⠸⡆⢸⠀⢠⣿⠀⠀⠀⠀⣰⣿⣵⡆⠀⠀⠀⠀
⠈⢻⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⡿⣦⣀⡇⠀⢧⡇⠀⠀⢺⡟⠀⠀⠀⢰⠉⣰⠟⠊⣠⠂⠀⡸
⠀⠀⢻⣿⣿⣷⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⢧⡙⠺⠿⡇⠀⠘⠇⠀⠀⢸⣧⠀⠀⢠⠃⣾⣌⠉⠩⠭⠍⣉⡇
⠀⠀⠀⠻⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣞⣋⠀⠈⠀⡳⣧⠀⠀⠀⠀⠀⢸⡏⠀⠀⡞⢰⠉⠉⠉⠉⠉⠓⢻⠃
⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⢀⣀⠠⠤⣤⣤⠤⠞⠓⢠⠈⡆⠀⢣⣸⣾⠆⠀⠀⠀⠀⠀⢀⣀⡼⠁⡿⠈⣉⣉⣒⡒⠢⡼⠀
⠀⠀⠀⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣎⣽⣶⣤⡶⢋⣤⠃⣠⡦⢀⡼⢦⣾⡤⠚⣟⣁⣀⣀⣀⣀⠀⣀⣈⣀⣠⣾⣅⠀⠑⠂⠤⠌⣩⡇⠀
⠀⠀⠀⠀⠀⠀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⡁⣺⢁⣞⣉⡴⠟⡀⠀⠀⠀⠁⠸⡅⠀⠈⢷⠈⠏⠙⠀⢹⡛⠀⢉⠀⠀⠀⣀⣀⣼⡇⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣽⣿⡟⢡⠖⣡⡴⠂⣀⣀⣀⣰⣁⣀⣀⣸⠀⠀⠀⠀⠈⠁⠀⠀⠈⠀⣠⠜⠋⣠⠁⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⡟⢿⣿⣿⣷⡟⢋⣥⣖⣉⠀⠈⢁⡀⠤⠚⠿⣷⡦⢀⣠⣀⠢⣄⣀⡠⠔⠋⠁⠀⣼⠃⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⣿⣿⡄⠈⠻⣿⣿⢿⣛⣩⠤⠒⠉⠁⠀⠀⠀⠀⠀⠉⠒⢤⡀⠉⠁⠀⠀⠀⠀⠀⢀⡿⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣤⣤⠴⠟⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠑⠤⠀⠀⠀⠀⠀⢩⠇⠀⠀
    """.strip()

# ═════════════════════════════════════════════════════════════
#  BANNER
# ═════════════════════════════════════════════════════════════
def print_banner():
    """Display the main tool banner with a scary, terrifying look."""
    # بانر أصغر ليناسب العرض الجانبي
    small_banner = r"""

     _       _     ___       ___    _                              
( )  _  ( ) _ (  _`\  _ (  _`\ (_ )                            
| | ( ) | |(_)| (_(_)(_)| (_(_) | |    _ _  _   _    __   _ __ 
| | | | | || ||  _)  | |`\__ \  | |  /'_` )( ) ( ) /'__`\( '__)
| (_/ \_) || || |    | |( )_) | | | ( (_| || (_) |(  ___/| |   
`\___x___/'(_)(_)    (_)`\____)(___)`\__,_)`\__, |`\____)(_)   
                                           ( )_| |             
                                           `\___/'             
     """.strip()

    # تنظيف المسافات الفارغة (البرايل) من الشبح الأصلي ليصبح أصغر
    ghost_lines = GHOST_ART.replace('⠀', ' ').split('\n')
    valid_lines = [l for l in ghost_lines if l.strip()]
    if valid_lines:
        min_indent = min(len(l) - len(l.lstrip()) for l in valid_lines)
        clean_ghost = '\n'.join(l[min_indent:] for l in valid_lines)
    else:
        clean_ghost = ""

    # تحضير النصوص
    b_text = Text(small_banner, style="bold bright_red")
    g_text = Text(clean_ghost, style="bold bright_red")

    # وضع البانر والشبح جنباً إلى جنب مع توسيط عمودي
    cols = Columns([
        Align(b_text, align="center", vertical="middle"),
        Align(g_text, align="center", vertical="middle")
    ], expand=True)

    # طباعة العرض المزدوج
    console.print(cols)

    # فاصل أنيق قبل صندوق المعلومات
    console.rule("[dim]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━[/]")

    # صندوق المعلومات
    info = Text()

    info.append(f"\n {config.TOOL_NAME} ", style="bold bright_white")
    info.append(f"v{config.TOOL_VERSION}", style="bold bright_red")
    info.append(f"  │  ", style="dim white")
    info.append(f"{config.DEVELOPER}", style="bright_yellow")
    info.append(f"  │  ", style="dim white")
    info.append(f"{config.TELEGRAM}\n", style="bright_cyan")
    info.append(f"  telegram : @run_kernel", style="bold green")
    info.append(f"  │  ", style="dim white")
    info.append(f"GitHub : https://github.com/waheeb71/WiFiSlayer\n", style="bold blue")

    panel = Panel(
        Align.center(info),
        border_style="red",
        box=box.DOUBLE_EDGE,
        padding=(0, 2),
    )
    console.print(panel)

# ═════════════════════════════════════════════════════════════
#  STATUS BAR
# ═════════════════════════════════════════════════════════════
def print_status_bar(interface=None, mode=None, lang=None):
    """Display a compact status bar showing current state."""
    status = Table(show_header=False, box=box.SIMPLE_HEAVY, border_style="dim cyan",
                   expand=True, padding=(0, 1))
    status.add_column(ratio=1, justify="center")
    status.add_column(ratio=1, justify="center")
    status.add_column(ratio=1, justify="center")

    iface_str = f"📡 Interface: [bold bright_green]{interface}[/]" if interface else "📡 Interface: [dim]Auto[/]"
    mode_str = f"🔒 Mode: [bold bright_yellow]{mode}[/]" if mode else "🔒 Mode: [dim]—[/]"
    lang_str = f"🌐 [bold]{'العربية' if lang == 'ar' else 'English'}[/]"

    status.add_row(iface_str, mode_str, lang_str)
    console.print(status)


# ═════════════════════════════════════════════════════════════
#  MAIN MENU
# ═════════════════════════════════════════════════════════════
def print_main_menu():
    """Display the main interactive menu."""
    menu_items = [
        ("1", "🔍", get_text("menu_scan"), "bright_cyan"),
        ("2", "🤝", get_text("menu_handshake"), "bright_green"),
        ("3", "🔓", get_text("menu_crack"), "bright_yellow"),
        ("4", "📡", get_text("menu_traffic"), "bright_magenta"),
        ("5", "⚡", get_text("menu_deauth"), "bright_red"),
        ("6", "📝", get_text("menu_wordlist"), "blue"),
        ("7", "🎭", get_text("menu_mac"), "bright_blue"),
        ("8", "🔥", get_text("menu_advanced"), "bright_red"),
        ("9", "⚙️ ", get_text("menu_settings"), "dim white"),
        ("0", "🚪", get_text("menu_exit"), "dim red"),
    ]

    table = Table(
        show_header=False,
        box=box.ROUNDED,
        border_style="bright_cyan",
        expand=True,
        padding=(0, 2),
    )
    table.add_column("Opt", width=5, justify="center")
    table.add_column("Icon", width=4, justify="center")
    table.add_column("Description", ratio=1)

    for num, icon, desc, color in menu_items:
        table.add_row(
            f"[bold {color}]{num}[/]",
            icon,
            f"[{color}]{desc}[/]",
        )

    console.print(table)


def get_menu_choice(max_choice=9):
    """Get a validated menu choice from the user."""
    while True:
        try:
            choice = console.input(f"\n  [bold bright_cyan]➤ {get_text('choose')}:[/] ")
            choice = choice.strip()
            if choice in [str(i) for i in range(0, max_choice + 1)]:
                return int(choice)
            console.print(f"  [red]✗ {get_text('invalid_choice')}[/]")
        except (KeyboardInterrupt, EOFError):
            return 0


# ═════════════════════════════════════════════════════════════
#  SUB-MENUS
# ═════════════════════════════════════════════════════════════
def print_sub_menu(title, options):
    """
    Display a sub-menu.
    options: list of (key, icon, description) tuples.
    """
    table = Table(
        title=f"[bold bright_cyan]{title}[/]",
        show_header=False,
        box=box.ROUNDED,
        border_style="cyan",
        expand=True,
        padding=(0, 2),
    )
    table.add_column("Opt", width=5, justify="center")
    table.add_column("Icon", width=4, justify="center")
    table.add_column("Description", ratio=1)

    for key, icon, desc in options:
        table.add_row(
            f"[bold bright_cyan]{key}[/]",
            icon,
            f"[white]{desc}[/]",
        )
    # Always add back option
    table.add_row("[bold dim]0[/]", "↩️ ", f"[dim]{get_text('back')}[/]")

    console.print(table)


# ═════════════════════════════════════════════════════════════
#  INTERFACE SELECTION
# ═════════════════════════════════════════════════════════════
def display_interfaces(interfaces):
    """Display detected wireless interfaces in a nice table."""
    if not interfaces:
        console.print(
            Panel(
                f"[bold red]✗ {get_text('no_interfaces')}[/]",
                border_style="red",
            )
        )
        return

    table = Table(
        title=f"[bold bright_cyan]📡 {get_text('detected_interfaces')}[/]",
        box=box.ROUNDED,
        border_style="cyan",
    )
    table.add_column("#", width=3, justify="center", style="bold bright_yellow")
    table.add_column("Interface", style="bold bright_green")
    table.add_column("Mode", style="bright_white")

    for i, iface in enumerate(interfaces, 1):
        mode_color = "bright_green" if iface["mode"].lower() == "monitor" else "bright_white"
        table.add_row(str(i), iface["name"], f"[{mode_color}]{iface['mode']}[/]")

    console.print(table)


def select_interface(interfaces):
    """Let user select an interface from detected ones or enter manually."""
    display_interfaces(interfaces)
    console.print()

    if interfaces:
        choice = console.input(
            f"  [cyan]➤ {get_text('select_interface')} (1-{len(interfaces)}) "
            f"[dim]or type name manually[/]: [/]"
        )
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(interfaces):
                return interfaces[idx]["name"]
        except ValueError:
            pass
        # Manual entry fallback
        return choice.strip() if choice.strip() else None
    else:
        return console.input(f"  [cyan]➤ {get_text('enter_interface')}: [/]").strip() or None


# ═════════════════════════════════════════════════════════════
#  UTILITY DISPLAY FUNCTIONS
# ═════════════════════════════════════════════════════════════
def print_success(message):
    """Display a success message."""
    console.print(f"  [bold bright_green]✓ {message}[/]")


def print_error(message):
    """Display an error message."""
    console.print(f"  [bold red]✗ {message}[/]")


def print_warning(message):
    """Display a warning message."""
    console.print(f"  [bold bright_yellow]⚠ {message}[/]")


def print_info(message):
    """Display an info message."""
    console.print(f"  [bold bright_cyan]ℹ {message}[/]")


def print_section(title):
    """Display a section header."""
    console.print(f"\n  [bold bright_magenta]{'─' * 3} {title} {'─' * 40}[/]\n")


def confirm_action(message):
    """Ask for user confirmation before a dangerous action."""
    try:
        answer = console.input(f"  [bold bright_yellow]⚠ {message} (y/n): [/]")
        return answer.strip().lower() in ("y", "yes", "نعم")
    except (KeyboardInterrupt, EOFError):
        return False


def print_language_selector():
    """Display language selection prompt."""
    console.print()
    panel = Panel(
        "[bold bright_cyan]  1 │ العربية  (Arabic)\n"
        "  2 │ English[/]",
        title="[bold bright_white]🌐 Language / اللغة[/]",
        border_style="bright_cyan",
        box=box.ROUNDED,
    )
    console.print(panel)
