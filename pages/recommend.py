# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

# Note: Placeholder for the recommend algorithm.
from datetime import datetime
from typing import List, Tuple
from uuid import uuid4
from nicegui import ui
from web_functions import eco_header, eco_footer

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
    def send_message() -> None:
        timestamp = datetime.now().strftime("%X")
        messages.append((user_id, avatar, message_input.value, timestamp))
        message_input.value = ""
        display_messages(user_id)

    user_id = str(uuid4()) # generate a random user id
    avatar = f"https://robohash.org/{user_id}?bgset=bg2" # generate a random avatar

    with ( # Display the chat interface
        ui.footer().classes("bg-gray-100 mt-0"),
        ui.column().classes("w-full max-w-3xl mx-auto my-2"),
    ):
        with ui.row().classes("w-full flex-nowrap items-center mt-0"): #
            with ui.avatar().on("click", lambda: ui.navigate.to(main)):
                ui.image(avatar) 
            message_input = ( # Input field for the message
                ui.input(placeholder="message")
                .on("keydown.enter", send_message)
                .props("rounded outlined input-class=mx-3")
                .classes("flex-grow mt-0")
            )

    global messages_container 
    messages_container = ui.column().classes("mt-0")
    display_messages(user_id)
    eco_footer()  # inject the CSS styles


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()
