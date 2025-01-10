from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import app, ui
from web_functions import inject_style

# Dummy user database -------------------------------------------------
passwords = {'user1': 'pass1', 'user2': 'pass2'} # dummy user database

@ui.page('/register') # Register page route
def register_page():
    inject_style() # inject the CSS styles

    def register():
        username, password = username_input.value, password_input.value # get username & password from input
        if username in passwords: # If username already exists
            ui.notify("Username already exists!", color='negative', position='center')
        else:
            passwords[username] = password # Add new user to the database
            ui.notify("Registration successful!", color='positive', position='center')
            ui.navigate.to('/login') # navigate to login page

    with ui.column().style('justify-content: center; align-items: center; width: 100%; height: 75vh;'): # Register page layout
        ui.label('Create a new account').style('color: #FFFFFF; font-size: 32px;')
        with ui.element('div').classes('mail').style('padding: 50px'): # Register form
            username_input = ui.input('User').style('background-color: #FFFFFF;') # input user
            password_input = ui.input('Pass', password=True, password_toggle_button=True).style('background-color: #FFFFFF;') # pass & toggle
            ui.button('Register', on_click=register).style('margin-top: 20px;') # create a register button
            ui.button('Back to Login', on_click=lambda: ui.navigate.to('/login')).style('margin-top: 20px; margin-left: 20px;') # create a button to go back to login page