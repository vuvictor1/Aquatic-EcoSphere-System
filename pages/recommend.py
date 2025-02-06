# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

# Note: Placeholder for the recommend algorithm.
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import ui

# List to store chat messages
messages: List[Tuple[str, str, str, str]] = []

def display_messages(user_id: str) -> None:
    # Clear the messages container
    messages_container.clear()
    if messages:
        for msg_user_id, avatar, text, timestamp in messages:
            ui.chat_message(text=text, stamp=timestamp, avatar=avatar, sent=user_id == msg_user_id).classes('message')
    else:
        ui.label('No messages yet').classes('mx-auto my-36')

def recommend_page():
    def send_message() -> None:
        timestamp = datetime.now().strftime('%X')
        messages.append((user_id, avatar, message_input.value, timestamp))
        message_input.value = ''
        display_messages(user_id)

    user_id = str(uuid4())
    avatar = f'https://robohash.org/{user_id}?bgset=bg2'

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full flex-nowrap items-center'):
            with ui.avatar().on('click', lambda: ui.navigate.to(main)):
                ui.image(avatar)
            message_input = ui.input(placeholder='message').on('keydown.enter', send_message) \
                .props('rounded outlined input-class=mx-3').classes('flex-grow')

    global messages_container
    messages_container = ui.column()
    display_messages(user_id)

@ui.page('/recommend')  # Route for recommend page
def recommend():
    recommend_page()