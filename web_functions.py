# Author: Victor Vu and Jordan Morris
# File: web_functions.py
# Description: Provides style and functions for the web interface
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui

def eco_header(): # Header for the web interface
    with ui.header().style('background-color: #3AAFA9; padding: 10px 20px; position: static;'): 
        ui.link('🌊 Home', '/').style('color: #FFFFFF; font-size: 24px; text-decoration: none;')
        ui.link('Graphs', '/graphs').style('color: #FFFFFF; font-size: 24px; text-decoration: none;')
        ui.link('Reminders', '/reminders').style('color: #FFFFFF; font-size: 24px; text-decoration: none;')
        ui.link('Encyclopedia', '/encyclopedia').style('color: #FFFFFF; font-size: 24px; text-decoration: none;')
        ui.link('Contacts', '/contacts').style('color: #FFFFFF; font-size: 24px; text-decoration: none;')

        with ui.row().style('gap: 10px;'): # Buttons style
            ui.button('account', icon='account_circle', on_click=lambda: ui.navigate.to('/login')) # account redirect
            with ui.dropdown_button(icon='settings', auto_close=True): # settings dropdown 2 options
                ui.item('Thresholds', on_click=lambda: ui.navigate.to('/settings')) # settings redirect
                ui.item('Species', on_click=lambda: ui.navigate.to('/species')) # species redirect

def inject_style(): # Injects CSS style in web interface
    ui.add_head_html("""
    <style>
        body {
            background-color: #3B3B3B;
        }
        .card, .mail {
            background-color: #2C2C2C;
            padding: 20px;
            border-radius: 10px;
            margin: 10px;
            border: 2px solid #2C2C2C;
            transition: border-color 0.3s ease, transform 0.3s ease;
        }
        .card {
            width: 100%;
            max-width: 300px;
        }
        .mail {
            width: 100%;
            max-width: 600px;
        }
        .card:hover {
            border-color: #F5A623;
            transform: scale(1.05);
        }
        @media (max-width: 600px) {
            .card, .mail {
                width: 100%;
                margin: 5px;
            }
            .card {
                max-width: none;
            }
            .mail {
                max-width: none;
            }
        }
    </style>
    """)

def inject_lottie(): # Injects Lottie animation in web interface
    ui.add_body_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

def eco_footer(): # Footer for the web interface
    with ui.footer().style('background-color: #3AAFA9; justify-content: center; padding: 10px; position: static;'):
        ui.label('Copyright (C) 2025 | Victor Vu & Jordan Morris').style('color: #FFFFFF; font-size: 18px;')