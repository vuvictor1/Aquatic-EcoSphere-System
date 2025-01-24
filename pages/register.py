# Authors: Victor Vu 
# File: register.py
# Description: Register using authentication middleware if not authenticated.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui
from web_functions import inject_style

passwords = {'user1': 'pass1'} # user database with dummy 
@ui.page('/register') # Register page route
def register_page():
    inject_style() # inject the CSS styles

    def register(): # Register in users function
        username, password = username_input.value, password_input.value # get username & password from input
        if not username or not password: # Check if fields are empty
            ui.notify("Username and password cannot be empty!", color='negative', position='center')
        elif username in passwords: # If username already exists
            ui.notify("Username already exists!", color='negative', position='center')
        else:
            passwords[username] = password # Add new user to the database
            ui.navigate.to('/login') # navigate to login page

    with ui.column().style('justify-content: center; align-items: center; width: 100%; height: 75vh;'): # Register page layout
        with ui.element('div').style('padding: 50px').classes('login-form'): # Register form
            ui.label('Create an account or return to login.').style('color: #FFFFFF; font-size: 32px; margin-bottom: 20px;')
            username_input = ui.input('Username').style('background-color: #FFFFFF; padding: 0px 20px;') # input user
            password_input = ui.input('Password', password=True, password_toggle_button=True).style('background-color: #FFFFFF; padding: 0px 20px;') # pass & toggle
            ui.button('Register', on_click=register).style('margin-top: 20px;') # create a register button
            ui.button('Back to Login', on_click=lambda: ui.navigate.to('/login')).style('margin-top: 20px; margin-left: 5px;') # create a button to go back to login page

    # CSS for mobile responsiveness
    ui.add_css('''
    @media (max-width: 600px) {
        .login-form button {
            padding: 10px 20px !important;
            font-size: 16px !important;
            width: 100% !important;
        }
    }
    ''')