# Authors: Victor Vu and Jordan Morris
# File: login.py
# Description: Login page using authentication middleware to prompt users if not authenticated. 
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui

# Dummy user database -------------------------------------------------
passwords = {'user1': 'pass1', 'user2': 'pass2'} # dummy user database

# Unrestricted routes that do not require authentication
unrestricted_routes = {'/login'}

class AuthMiddleware(BaseHTTPMiddleware): # Authentication middleware
    async def dispatch(self, request: Request, call_next): # Async dispatch function
        if not app.storage.user.get('authenticated', False): # Check if the user is not authenticated
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_routes: # If path is not unrestricted routes
                app.storage.user['/'] = request.url.path # store the original path the user was trying to access
                return RedirectResponse('/login') # redirect to login page
        return await call_next(request) # proceed with the request

# Add the authentication middleware to the app
app.add_middleware(AuthMiddleware)

@ui.page('/login') # Login page route
def login_page():
    def authenticate(): 
        username, password = username_input.value, password_input.value # get username & password from input 
        if passwords.get(username) == password: # If username exists and password matches
            app.storage.user.update({'authenticated': True, 'username': username}) # update user storage
            ui.navigate.to('/') # navigate to home page
        else: # If name or password is incorrect notify user
            ui.notify("Invalid username or password!", color='negative', position='center')

    def proceed_as_guest(): # Proceed as guest function
        app.storage.user.update({'authenticated': True, 'username': 'guest'}) # update user storage as guest
        ui.navigate.to('/')

    username_input = ui.input('Username').on('keydown.enter', authenticate) # create input field for username
    password_input = ui.input('Password', password=True).on('keydown.enter', authenticate) # create input field for password
    ui.button('Login', on_click=authenticate) # create a login button
    ui.button('Proceed as Guest', on_click=proceed_as_guest) # create a button to proceed as a guest
