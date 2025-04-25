# Authors: Victor Vu and Jordan Morris
# File: firebase.py
# Description: Native Notify push notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
import requests

# Native Notify Push Notification API endpoint
NATIVE_NOTIFY_URL = "https://app.nativenotify.com/api/notification"

# Function to send a push notification
def send_push_notification(app_id, app_token, title, message):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "appId": app_id,
        "appToken": app_token,
        "title": title,
        "message": message,
    }
    response = requests.post(NATIVE_NOTIFY_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.text}")

# Define a new page for sending notifications
@ui.page("/notifications")
def notifications_page():
    ui.label("Send a Push Notification").classes("text-2xl mb-4")
    
    app_id_input = ui.input("App ID").classes("w-full mb-2")
    app_token_input = ui.input("App Token").classes("w-full mb-2")
    title_input = ui.input("Notification Title").classes("w-full mb-2")
    message_input = ui.input("Notification Message").classes("w-full mb-4")
    
    ui.button(
        "Send Notification",
        on_click=lambda: send_push_notification(
            app_id_input.value,
            app_token_input.value,
            title_input.value,
            message_input.value
        )
    ).classes("w-full bg-blue-500 text-white")