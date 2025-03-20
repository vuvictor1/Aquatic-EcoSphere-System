# File: recommend.py
# Description: Recommend algorithm for users based on their preferences.

from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style


def recommend_page():  # Function to display the recommend page
    eco_header()  # inject the header
    inject_style()  # inject additional styles

    # Use fixed robot IDs
    avatar = "https://robohash.org/user1?bgset=bg2"
    avatar2 = "https://robohash.org/user2?bgset=bg2"
    avatar3 = "https://robohash.org/user3?bgset=bg2"

    # Title
    with ui.row().classes("justify-center w-full mt-4"):
        ui.label("Recommendations").classes("text-white text-4xl font-bold text-center")

    # Recommendation Cards
    with ui.row().classes("justify-center w-full mt-6"):
        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar).classes("w-24 h-24 rounded-full mx-auto")
            tds_label = ui.label("Hi, I am the TDS advisor.").classes("text-white text-base mt-4")
            tds_loading = ui.skeleton().classes("w-full h-4 mt-2 hidden")  # Hidden by default

        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar2).classes("w-24 h-24 rounded-full mx-auto")
            turbidity_label = ui.label("Hello, I am the turbidity advisor.").classes(
                "text-white text-base mt-4"
            )
            turbidity_loading = ui.skeleton().classes("w-full h-4 mt-2 hidden")  # Hidden by default

        with ui.column().classes(
            "text-center p-5 bg-gray-800 rounded-lg shadow-lg max-w-sm"
        ):
            ui.image(avatar3).classes("w-24 h-24 rounded-full mx-auto")
            temperature_label = ui.label("Hey, I am the temperature advisor.").classes(
                "text-white text-base mt-4"
            )
            temperature_loading = ui.skeleton().classes("w-full h-4 mt-2 hidden")  # Hidden by default

    # Button to trigger "Thinking..." and show loading screen
    def on_button_click():
        tds_label.set_text("Thinking...")
        turbidity_label.set_text("Thinking...")
        temperature_label.set_text("Thinking...")
        tds_loading.classes(remove="hidden")  # Show loading bar
        turbidity_loading.classes(remove="hidden")  # Show loading bar
        temperature_loading.classes(remove="hidden")  # Show loading bar

    # Add the button below the recommendation cards
    with ui.row().classes("justify-center w-full mt-6"):
        ui.button("Request advice", on_click=on_button_click).classes("bg-blue-500 text-white px-4 py-2 rounded")

    eco_footer()  # inject the footer


@ui.page("/recommend")  # Route for recommend page
def recommend():
    recommend_page()
