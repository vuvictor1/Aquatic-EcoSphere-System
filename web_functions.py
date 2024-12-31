# Authors: Victor Vu 
# File: web_functions.py
# Description: Provides style and functions for the web interface
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui

def eco_header(): # Header menu
    with ui.header().style('background-color: #3AAFA9; padding: 10px 300px;'): # Adjusted padding to maintain space around content
        ui.link('🌊 Home', '/').style('color: #FFFFFF; font-size: 24px; text-decoration: none;') # make home a link
        ui.link('Contacts', '/contacts').style('color: #FFFFFF; font-size: 24px; text-decoration: none;') # make contacts a link
        ui.label('|').style('color: #FFFFFF; font-size: 24px; ') # add separator
        with ui.row().style('gap: 10px;'): # add gaps between buttons
            ui.button(icon='account_circle') # add account button
            ui.button(icon='menu') # add menu button

def inject_style(): # Inject html with css for background 
    ui.add_head_html("""
    <style>
        body {
            background-color: #3B3B3B; /* change to gray */
        }
    </style>  
    """)

def eco_footer(): # Footer menu
    with ui.footer().style('background-color: #3AAFA9; justify-content: center;'):
        ui.label('Copyright (C) 2024 | Victor Vu & Jordan Morris').style('color: #FFFFFF; font-size: 18px;')