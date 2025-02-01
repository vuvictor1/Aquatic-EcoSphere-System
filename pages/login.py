# File: login.py
# Description: Login page using authentication middleware to prompt users if not authenticated.

# Note for later: This page uses different margins than other pages so manually adjust the margins here and web functions
from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui
from web_functions import inject_style
from pages.register import register_page, passwords

# unrestricted routes without authentication
unrestricted_routes = {'/login', '/register'}


class AuthMiddleware(BaseHTTPMiddleware):  # Authentication middleware
    async def dispatch(self, request: Request, call_next):  # async dispatch function

        # Check if the user is not authenticated
        if not app.storage.user.get('authenticated', False):
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_routes:
                # store the original path the user was trying to access
                app.storage.user['/'] = request.url.path
                return RedirectResponse('/login')
        return await call_next(request)  # proceed with the request


app.add_middleware(AuthMiddleware)  # add authentication middleware to the app


@ui.page('/login')  # Login page route
def login_page():
    inject_style()

    def authenticate():
        # get username & password from input
        username, password = username_input.value, password_input.value
        if passwords.get(username) == password:
            # update user storage
            app.storage.user.update(
                {'authenticated': True, 'username': username})
            ui.navigate.to('/')  # navigate to home page

        else:  # If name or password is incorrect notify user
            ui.notify("Invalid username or password!",
                      color='negative', position='center')

    def proceed_as_guest():  # Proceed as guest function
        # update user storage as guest
        app.storage.user.update({'authenticated': True, 'username': 'guest'})
        ui.navigate.to('/')

    with ui.column().classes('flex justify-center items-center w-full h-screen p-4 md:h-3/4 md:mt-20'):  # Login page layout
        with ui.element('div').classes('p-6 md:p-12 bg-gray-800 rounded-lg shadow-lg w-full max-w-md'):  # Responsive container
            ui.label('Please login or register.').classes(
                'text-white text-2xl md:text-3xl mb-5 text-center')
            username_input = ui.input('Username').classes(
                'bg-gray-200 px-4 py-2 w-full mb-4').on('keydown.enter', authenticate)
            password_input = ui.input('Password', password=True, password_toggle_button=True
                                      ).classes('bg-gray-200 px-4 py-2 w-full mb-4').on('keydown.enter', authenticate)
            ui.button('Login', on_click=authenticate).classes(
                'w-full bg-blue-500 text-white py-2 rounded mb-4')  # create a login button
            ui.button('Proceed as Guest', on_click=proceed_as_guest
                      ).classes('w-full bg-gray-500 text-white py-2 rounded mb-4')  # create a button to proceed as a guest
            ui.button('No account? Register here', on_click=lambda: ui.navigate.to('/register')
                      ).classes('w-full bg-green-500 text-white py-2 rounded')  # create a button to navigate to the registration page
