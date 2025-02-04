# File: register.py
# Description: Register using authentication middleware if not authenticated.

# Note for later: This page uses different margins than other pages so manually adjust the margins here and web functions
from fastapi import Request
from fastapi.responses import RedirectResponse
from nicegui import ui
from web_functions import inject_style

passwords = {'user1': 'pass1'}  # user database with dummy


@ui.page('/register')  # Register page route
def register_page():
    inject_style()  # inject the CSS styles

    def register():  # Register in users function
        # get username & password from input
        username, password = username_input.value, password_input.value

        if not username or not password:  # Check if fields are empty
            ui.notify("Username and password cannot be empty!",
                      color='negative', position='center')

        elif username in passwords:  # If username already exists
            ui.notify("Username already exists!",
                      color='negative', position='center')
        else:
            passwords[username] = password  # Add new user to the database
            ui.navigate.to('/login')  # navigate to login page

    with ui.column().classes('flex justify-center items-center w-full h-screen p-4 md:h-3/4 md:mt-20'):  # Register page layout
        with ui.element('div').classes('outline_label p-6 md:p-12 bg-gray-800 rounded-lg shadow-lg w-full max-w-md'):  
            ui.label('Create an account or return to login.').classes(
                'text-white text-2xl md:text-3xl mb-5 text-center')
            username_input = ui.input('Username').classes(
                'bg-gray-200 px-4 py-2 w-full mb-4')  # input user
            password_input = ui.input('Password', password=True, password_toggle_button=True).classes(
                'bg-gray-200 px-4 py-2 w-full mb-4')  # pass & toggle
            ui.button('Register', on_click=register).classes(
                'w-full bg-blue-500 text-white py-2 rounded mb-4')  # create a register button
            ui.button('Back to Login', on_click=lambda: ui.navigate.to('/login')).classes(
                'w-full bg-gray-500 text-white py-2 rounded')  # create a button to go back to login page