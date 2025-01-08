from fastapi import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from nicegui import app, ui

# Dummy user database
# This dictionary stores usernames as keys and their corresponding passwords as values.
passwords = {'user1': 'pass1', 'user2': 'pass2'}

# Unrestricted routes
# This set contains routes that do not require authentication.
unrestricted_routes = {'/login'}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Check if the user is authenticated
        if not app.storage.user.get('authenticated', False):
            # If the request path is not for NiceGUI internal routes and not in unrestricted routes
            if not request.url.path.startswith('/_nicegui') and request.url.path not in unrestricted_routes:
                # Store the original path the user was trying to access
                app.storage.user['/'] = request.url.path
                # Redirect the user to the login page
                return RedirectResponse('/login')
        # If authenticated, proceed with the request
        return await call_next(request)


# Add the authentication middleware to the app
app.add_middleware(AuthMiddleware)


@ui.page('/login')
def login_page():
    def authenticate():
        # Get the username and password from the input fields
        username, password = username_input.value, password_input.value
        # Check if the username exists in the passwords dictionary and if the password matches
        if passwords.get(username) == password:
            # Update the user's storage to indicate they are authenticated
            app.storage.user.update(
                {'authenticated': True, 'username': username})
            # Notify the user of successful login
            ui.notify("Login successful!", color='positive')
            # Navigate to the home page
            ui.navigate.to('/')
        else:
            # Notify the user of invalid credentials
            ui.notify("Invalid username or password!", color='negative')
    # Create an input field for the username
    username_input = ui.input('Username').on('keydown.enter', authenticate)
    # Create an input field for the password with hidden text
    password_input = ui.input('Password', password=True).on(
        'keydown.enter', authenticate)
    # Create a login button that triggers the authenticate function when clicked
    ui.button('Login', on_click=authenticate)
