# Author: Victor Vu and Jordan Morris
# File: web_functions.py
# Description: Provides style and functions for the web interface
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui

# Define constants for colors
background_color = "#3B3B3B"
header_footer_color = "#3AAFA9"


# Injects Tailwind CSS and custom styles
def inject_style():
    ui.add_head_html(f"""
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <style>
        body {{
            background-color: {background_color};
            min-height: 100vh; /* ensure body takes at least full viewport height */
            display: flex;
            flex-direction: column;
        }}
        main {{
            flex: 1; /* allow main content to grow and take available space */
            /* Reduce unnecessary margin space */
            margin-top: -60px;
            margin-bottom: -65px;
        }}
        @media (max-width: 768px) {{
            main {{
                margin-top: -150px; /* further reduce top margin on mobile devices */
            }}
        }}
        .outline_label {{
            border: 2px solid transparent;
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}
        .outline_label:hover {{
            transform: scale(1.05);
            border-color: {header_footer_color};
        }}
    </style>
    """)


# Injects Lottie player script
def inject_lottie():
    ui.add_body_html(
        '<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>'
    )


# Header for the web interface
def eco_header():
    with (
        ui.header()
        .classes("justify-center flex-wrap static p-4")
        .style(f"background-color: {header_footer_color}")
    ):
        ui.link("🌊 Home", "/").classes("text-white text-2xl no-underline mb-2 md:mb-0")
        ui.label("|").classes("text-white text-2xl hidden md:inline-block")
        ui.link("Graphs", "/graphs").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )
        ui.link("Reminders", "/reminders").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )
        ui.link("Predictions", "/predictions").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )
        ui.link("Recommend", "/recommend").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )
        ui.link("Encyclopedia", "/encyclopedia").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )
        ui.link("Contacts", "/contacts").classes(
            "text-white text-2xl no-underline mb-2 md:mb-0"
        )

        with ui.row().classes("gap-2 mt-2 md:mt-0"):  # Buttons for account and settings
            ui.button(  # account redirect
                "account",
                icon="account_circle",
                on_click=lambda: ui.navigate.to("/login"),
            )
            with ui.dropdown_button(  # Settings dropdown 2 options
                icon="settings", auto_close=True
            ):
                ui.item(  # settings redirect
                    "Thresholds", on_click=lambda: ui.navigate.to("/settings")
                )


# Footer for the web interface
def eco_footer():
    with (
        ui.footer()
        .classes("justify-center flex-wrap static p-4")
        .style(f"background-color: {header_footer_color}")
    ):
        ui.label("Copyright (C) 2025 | Victor Vu & Jordan Morris").classes(
            "text-white text-xl text-center mb-2 md:mb-0"
        )
