# Authors: Victor Vu 
# File: contacts.py
# Description: Contacts page for the web interface
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import *

def contacts_page(): # Function to display the contacts page
    eco_header()  # header menu
    inject_style()  # inject CSS for background

    with ui.row().style('justify-content: center; width: 100%;'):  # Center the content
        with ui.column().style('background-color: #2C2C2C; padding: 50px; border-radius: 10px; width: 100%; max-width: 600px;'):  # Adjust padding and column width
            ui.label('Contact Us').style('font-size: 24px; color: white; margin-bottom: 20px;')

            # Create input fields for the form
            name = ui.input('Name').style('width: 100%; padding: 10px; margin-bottom: 20px; color: #FFFFFF; background-color: #333333; border: 1px solid #555555; border-radius: 5px;')
            email = ui.input('Email').style('width: 100%; padding: 10px; margin-bottom: 20px; color: #FFFFFF; background-color: #333333; border: 1px solid #555555; border-radius: 5px;')
            message = ui.textarea('Message').style('width: 100%; height: 200px; padding: 10px; margin-bottom: 20px; color: #FFFFFF; background-color: #333333; border: 1px solid #555555; border-radius: 5px;')

            # Submit button to handle form submission
            ui.button('Send', on_click=lambda: submit_form(name.value, email.value, message.value))

    eco_footer()

def submit_form(name, email, message):  # Handle form submission here
    if name != '' or email != '' or message != '':  # Check if fields are not empty
        ui.notify('Thank you. Your message has been sent.', position='bottom', color='green')  # Notify message

@ui.page('/contacts')  # Route to contacts page
def contacts():
    contacts_page()
