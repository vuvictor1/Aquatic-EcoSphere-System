# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

from datetime import datetime
from uuid import uuid4
from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style


def recommend_page():  # Function to display the recommend page
    eco_header()  # inject the CSS styles
    inject_style()  # inject additional styles

    user_id = str(uuid4())  # generate a random user id
    avatar = f"https://robohash.org/{user_id}?bgset=bg2"  # generate a random avatar

    # Generate two more random avatars
    user_id2 = str(uuid4())
    avatar2 = f"https://robohash.org/{user_id2}?bgset=bg2"

    user_id3 = str(uuid4())
    avatar3 = f"https://robohash.org/{user_id3}?bgset=bg2"

    with ui.row().classes("justify-center w-full mt-0"):
        ui.label("Recommendations").classes("text-3xl sm:text-5xl text-white mt-0")

    with ui.row().classes("justify-center w-full mt-0"):
        with ui.column().classes("items-center mx-4"):
            ui.avatar().on("click", lambda: ui.navigate.to(main))
            ui.image(avatar)
            ui.label("Hi, I am the TDS advisor.").classes(
                "mx-auto my-2 bg-gray-800 text-white p-2 rounded"
            )
        with ui.column().classes("items-center mx-4"):
            ui.avatar().on("click", lambda: ui.navigate.to(main))
            ui.image(avatar2)
            ui.label("Hello, I am the turbidty advisor.").classes(
                "mx-auto my-2 bg-gray-800 text-white p-2 rounded"
            )
        with ui.column().classes("items-center mx-4"):
            ui.avatar().on("click", lambda: ui.navigate.to(main))
            ui.image(avatar3)
            ui.label("Hey, I am the temperature advisor.").classes(
                "mx-auto my-2 bg-gray-800 text-white p-2 rounded"
            )

    global messages_container
    messages_container = ui.column().classes("mt-0")
    eco_footer()  # inject the CSS styles


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()
