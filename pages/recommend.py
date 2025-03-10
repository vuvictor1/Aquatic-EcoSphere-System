# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style

# List to store chat messages
messages: List[Tuple[str, str, str, str]] = []


def display_messages(user_id: str) -> None:
    # Clear the messages container
    messages_container.clear()
    if messages:
        for msg_user_id, avatar, text, timestamp in messages:
            ui.chat_message(
                text=text, stamp=timestamp, avatar=avatar, sent=user_id == msg_user_id
            ).classes("message")
    else:
        ui.label("No messages yet").classes("mx-auto my-2 bg-gray-800 text-white p-2 rounded")


def recommend_page(): # Function to display the recommend page
    eco_header()  # inject the CSS styles
    inject_style()  # inject additional styles

    user_id = str(uuid4()) # generate a random user id
    avatar = f"https://robohash.org/{user_id}?bgset=bg2" # generate a random avatar

    with ui.row().classes('justify-center w-full mt-0'):
        ui.label('Recommendations').classes('text-3xl sm:text-5xl text-white mt-0')

    with ui.row().classes('justify-center w-full mt-0'):
        with ui.avatar().on("click", lambda: ui.navigate.to(main)):
            ui.image(avatar)

    global messages_container 
    messages_container = ui.column().classes("mt-0")
    display_messages(user_id)
    eco_footer()  # inject the CSS styles


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()
