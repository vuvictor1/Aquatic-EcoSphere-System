# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style


def recommend_page():  # Function to display the recommend page
    eco_header()  # Inject the header
    inject_style()  # Inject additional styles

    # Use fixed user IDs
    avatar = "https://robohash.org/user1?bgset=bg2"  # Fixed avatar
    avatar2 = "https://robohash.org/user2?bgset=bg2"  # Fixed avatar
    avatar3 = "https://robohash.org/user3?bgset=bg2"  # Fixed avatar

    # Title
    with ui.row().classes("justify-center w-full mt-4"):
        ui.label("Recommendations").classes("text-white text-4xl font-bold text-center")

    # Recommendation Cards
    with ui.row().classes("justify-center items-center flex-wrap gap-6 mt-6"):
        with ui.column().classes(
            "items-center text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar).classes("w-24 h-24 rounded-full mx-auto")
            ui.label("Hi, I am the TDS advisor.").classes("text-white text-base mt-4")

        with ui.column().classes(
            "items-center text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar2).classes("w-24 h-24 rounded-full mx-auto")
            ui.label("Hello, I am the turbidity advisor.").classes(
                "text-white text-base mt-4"
            )

        with ui.column().classes(
            "items-center text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar3).classes("w-24 h-24 rounded-full mx-auto")
            ui.label("Hey, I am the temperature advisor.").classes(
                "text-white text-base mt-4"
            )

    eco_footer()  # Inject the footer


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()
