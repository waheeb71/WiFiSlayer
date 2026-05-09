# -*- coding: utf-8 -*-
"""
WiFiSlayerTool v3.0 — ASCII Art Collection
Contains scary and professional ASCII art for different attack modules.
"""

from rich.console import Console
from rich.align import Align
from rich.text import Text

console = Console()

def print_dragon_art():
    """Andrax-style Dragon for Auto-Pwn."""
    art = r"""
        ,     ,
        )\___/(
       {(@)v(@)}
        {|~~~|}
        {/^^^\}
         `m-m`
      AUTO-PWN MODE
    """
    # A bigger dragon
    art_big = r"""
           _.-'~~~`-._
          /           \
         /   _     _   \
        |   (o)   (o)   |
        |      ^      |
         \    \_/    /
          `'-.____.-'`
       [ AUTO-PWN MODE ]
    """
    
    andrax_dragon = r"""
             ,;`
           ,;;;`  ,
         ,;;;;;;;;;;;,
       ,;;;;;;;;;;;;;;;,
      ;;;;;;;;;;;;;;;;;;;,      ,
     ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
    ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;`
     `;;;;;;;;;;;;;;;;;;;;;;;;`
        `;;;;;;;;;;;;;;;;;;;`
          `;;;;;;;;;;;;;;;`
             `;;;;;;;;;;`
    
      [ AUTO-PWN INITIATED ]
    """
    console.print(Align.center(f"[bold red]{andrax_dragon}[/]"))


def print_skull_art():
    """Skull for Deauthentication attacks."""
    art = r'''
                 uuuuuuu
             uu$$$$$$$$$$$uu
          uu$$$$$$$$$$$$$$$$$uu
         u$$$$$$$$$$$$$$$$$$$$$u
        u$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$$$$$$$$$$$$$$$$$$$$u
       u$$$$$$"   "$$$"   "$$$$$$u
       "$$$$"      u$u       $$$$"
        $$$u       u$u       u$$$
        $$$u      u$$$u      u$$$
         "$$$$uu$$$   $$$uu$$$$"
          "$$$$$$$"   "$$$$$$$"
            u$$$$$$$u$$$$$$$u
             u$"$"$"$"$"$"$u
  uuu        $$u$ $ $ $ $u$$       uuu
 u$$$$        $$$$$u$u$u$$$       u$$$$
  $$$$$uu      "$$$$$$$$$"     uu$$$$$$
u$$$$$$$$$$$uu    """""    uuuu$$$$$$$$$$
    '''
    console.print(Align.center(f"[bold red]{art}[/]"))


def print_radar_art():
    """Radar for Scanner."""
    art = r"""
          .
         . .
       .......
     ...........
    .............
    ... SCANNER ...
    """
    art2 = r"""
          _
       _-(_)-_
     .-(     )-.
    (_   SCAN   _)
      `-(   )-'
         `-'
    """
    console.print(Align.center(f"[bold bright_cyan]{art2}[/]"))


def print_handshake_art():
    """Keys/Handshake for WPA."""
    art = r"""
       .--.
      /.-. '----------.
      \'-' .--"--""-"-'
       '--'
    [ WPA HANDSHAKE ]
    """
    console.print(Align.center(f"[bold bright_green]{art}[/]"))


def print_eviltwin_art():
    """Devil/Evil for Evil Twin."""
    art = r"""
       \         /
        \       /
         \     /
       .-"`'V'//-.
      / ,   |// , \
     / /|   |/ /|  \
    | | |   | | |   |
    | | |   | | |   |
     \ \|   |/ /    /
      \ \   | /    /
       \ \  |/    /
        \ \ |    /
         \ \|   /
          \ |  /
           \| /
            V
    [ EVIL TWIN AP ]
    """
    console.print(Align.center(f"[bold magenta]{art}[/]"))


def print_flood_art():
    """Biohazard for Beacon Flood."""
    art = r"""
           _.-.
         ,'/ \'.
        / /   \ \
       | |     | |
        \ \   / /
         '.\_/.'
      [ BEACON FLOOD ]
    """
    art_bio = r"""
          .::.
         .::::.
    ...  ::::::  ...
    :::  ::::::  :::
    :::  ::::::  :::
    '::  ::::::  ::'
      '  ::::::  '
         '::::'
           ''
     [ MDK4 FLOOD ]
    """
    console.print(Align.center(f"[bold bright_yellow]{art_bio}[/]"))


def print_wps_art():
    """Lock/Key for WPS/PMKID."""
    art = r"""
      ______
     /      \
    |        |
    |  _  _  |
    | | || | |
    | |_||_| |
    |________|
   [ WPS / PMKID ]
    """
    console.print(Align.center(f"[bold bright_blue]{art}[/]"))


def print_eye_art():
    """Eye for Traffic/Sniffing."""
    art = r"""
       .-'''''-.
     .'  _   _  '.
    /   (o) (o)   \
   |               |
   |   \       /   |
    \   '.___.'   /
     '.         .'
       '-.....-'
    [ SNIFFING TRAFFIC ]
    """
    console.print(Align.center(f"[bold bright_magenta]{art}[/]"))
