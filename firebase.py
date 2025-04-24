# Authors: Victor Vu and Jordan Morris
# File: firebase.py
# Description: Expo push notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
import requests

# Expo Push Notification API endpoint
EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

# Expo Push Notification API endpoint
EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

# Function to send a push notification
def send_push_notification(expo_push_token, title, message):
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    payload = {
        "to": expo_push_token,
        "title": title,
        "body": message,
        "sound": "default",
    }
    response = requests.post(EXPO_PUSH_URL, json=payload, headers=headers)
    if response.status_code == 200:
        print("Notification sent successfully!")
    else:
        print(f"Failed to send notification: {response.text}")

# Define a new page for sending notifications
@ui.page("/notifications")
def notifications_page():
    ui.label("Send a Push Notification").classes("text-2xl mb-4")
    
    expo_token_input = ui.input("Expo Push Token").classes("w-full mb-2")
    title_input = ui.input("Notification Title").classes("w-full mb-2")
    message_input = ui.input("Notification Message").classes("w-full mb-4")
    
    ui.button(
        "Send Notification",
        on_click=lambda: send_push_notification(
            expo_token_input.value,
            title_input.value,
            message_input.value
        )
    ).classes("w-full bg-blue-500 text-white")
