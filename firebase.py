import firebase_admin
from firebase_admin import credentials, messaging
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(
    "config/aquatic-ecosphere-firebase-adminsdk-fbsvc-d66639d5a5.json")
firebase_admin.initialize_app(cred, {
    # Get the private key from .env
    'vapid_private_key': os.getenv('FIREBASE_VAPID_PRIVATE_KEY'),
})


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
