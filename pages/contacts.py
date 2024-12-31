# Authors: Victor Vu 
# File: contacts.py
# Description: Contacts page for the web interface
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import *

def contacts_page(): # Function to display the contacts page
    eco_header() # header menu
    inject_style() # inject css for background
    with ui.card().style('padding: 20px; background-color: #FFFFFF;'): # Contact Form Card
        ui.label('Contact Us').style('font-size: 24px; font-weight: bold;')
        ui.input('Name').style('margin-bottom: 10px;')
        ui.input('Email').style('margin-bottom: 10px;')  
        ui.textarea('Message').style('margin-bottom: 10px;')
        ui.button('Submit', on_click=submit_form).style('background-color: #4CAF50; color: white;')
    eco_footer() # footer menu

def submit_form(): # Function to notify form submission
    ui.notify('Form submitted successfully!', position='top-right') # test notification

@ui.page('/contacts') # Route to contacts page
def contacts():
    contacts_page()
