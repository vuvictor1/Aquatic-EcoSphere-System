# Authors: Victor Vu and Jordan Morris
# File: firebase.py
# Description: Firebase push notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import firebase_admin
from firebase_admin import credentials, messaging
from collect_database import env_reuse
import os

env_reuse() # reuse loaded .env instead of recreating in other files

# Initialize Firebase Admin SDK
cred = credentials.Certificate(
    "config/aquatic-ecosphere-firebase-adminsdk-fbsvc-d66639d5a5.json"
)
firebase_admin.initialize_app(
    cred,
    {
        # Get the private key from .env
        "vapid_private_key": os.getenv("FIREBASE_VAPID_PRIVATE_KEY"),
    },
)


def send_push_notification(token, title, body):
    # Create a message to send
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        token=token,  # FCM token from the frontend
    )

    # Send the message
    response = messaging.send(message)
    print("Successfully sent message:", response)
