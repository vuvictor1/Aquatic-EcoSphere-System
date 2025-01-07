# Authors: Jordan Morris and Victor Vu
# File: encyclopedia.py
# Description: Encyclopedia page for the web interface 
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

column_style = 'background-color: #2C2C2C; padding: 50px; border-radius: 10px; width: 100%; max-width: 600px;' # style for column

def encyclopedia_page(): # Encyclopedia page
    eco_header() # header menu
    inject_style() # inject CSS for background

    with ui.row().style(f'justify-content: center; width: 100%; margin-top: 20px; background-color: #3B3B3B;'): # Center the encyclopedia title
        with ui.column().classes('mail').style(f'align-items: center; background-color: #2C2C2C; padding: 20px; border-radius: 10px;'): # Column for the encyclopedia
            ui.label('Encyclopedia').style(f'font-size: 32px; color: white;') 
            ui.label('This is a placeholder for the Encyclopedia page. Content will be added soon.').style(f'font-size: 20px; color: white;') # placeholder text
    eco_footer() # footer function

@ui.page('/encyclopedia') # Route to encyclopedia page
def encyclopedia():
    encyclopedia_page()
