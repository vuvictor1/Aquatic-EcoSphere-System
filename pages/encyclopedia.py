# File: encyclopedia.py
# Description: Encyclopedia page for the web interface
from nicegui import ui, html
from web_functions import inject_style, eco_header, eco_footer
import requests
import json
import os


# Load the species data from the JSON file
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
parent_dir_path = os.path.dirname(current_dir_path)
species_data_path = os.path.join(parent_dir_path, 'data', 'species_data.json')

with open(species_data_path, 'r') as file:
    species_data = json.load(file)


def filter_species(query: str) -> list:
    """Filter species based on the query."""
    query = query.lower().strip()
    filtered = [
        species
        for species in species_data
        if query in species["name"].lower()
        or query in species["description"].lower()
        or query in species["tolerance_levels"].lower()
    ]
    print(f"🔍 Filtering with query: '{query}', Found {len(filtered)} species")
    return filtered


def display_species(species_list: list, results_container: ui.row) -> None:
    """
    Update the displayed species list dynamically.

    Args:
        species_list (list): A list of species data.
        results_container (ui.row): The container to display the species list.

    Returns:
        None
    """

    # Clear the results container
    results_container.clear()

    # Define the card classes
    card_classes = "sm:w-64 md:w-80 lg:w-96 m-2 p-3 bg-gray-700 text-white hover:scale-105 transition duration-300 ease-in-out"

    # Define the image styles
    image_styles = "width: 120px; height: 120px; border-radius: 10px;"

    # Display each species in the list
    with results_container:
        for species in species_list:
            # Create a card for the species
            with ui.card().classes(card_classes):
                # Display the species image
                html.img(src=species.get(
                    "image_url", "https://placehold.co/120"), style=image_styles)

                # Display the species name
                ui.label(species["name"]).classes("text-lg font-bold")

                # Display the species description
                ui.label(species["description"]).classes(
                    "text-sm text-gray-300")

                # Display the species tolerance levels
                ui.label(f"Tolerance: {species['tolerance_levels']}").classes(
                    "text-xs text-gray-500")

# Function to add custom species


def add_custom_species(name, description, tolerance_levels, image_url, results, add_species_form):
    # Create a new species dictionary
    new_species = {
        "name": name,
        "description": description,
        "tolerance_levels": tolerance_levels,
        "image_url": image_url
    }

    # Add the new species to the species data
    species_data.append(new_species)

    # Save the updated species data to the JSON file
    with open(species_data_path, 'w', encoding='utf-8') as file:
        json.dump(species_data, file, ensure_ascii=False, indent=4)

    # Update the displayed species list
    display_species(species_data, results)

    ui.notify(f"Added {name} to the encyclopedia!", type="positive")

    # Close the add custom species form
    add_species_form.close()


def encyclopedia_page() -> None:
    """
    Encyclopedia page.
    """

    eco_header()
    inject_style()

    with ui.row().classes("justify-center w-full mt-0"):
        with ui.column().classes(
            "outline_label items-center bg-gray-800 p-5 rounded-lg w-full max-w-2xl"
        ):
            ui.label("Aquatic Species Encyclopedia").classes(
                "text-4xl text-white font-bold"
            )

            search_field = (
                ui.input(placeholder="Search for species...")
                .props('autofocus outlined rounded item-aligned input-class="ml-3"')
                .classes("w-96 self-center mt-0 transition-all")
                .on_value_change(
                    lambda e: display_species(filter_species(e.value), results)
                )
                .style(
                    "width: 100%; padding: 10px; border-radius: 25px; border: 1px solid #ccc; font-size: 16px; background-color: #e0e0e0;"
                )
            )

            # Button to show the add species form
            ui.button("Add Species", on_click=lambda: add_custom_species_form.open()).classes(
                "mt-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded")

    results = ui.row().classes("w-full mt-4 flex flex-wrap justify-center")
    display_species(species_data, results)

    # Define common props for inputs
    common_input_props = 'label-color="white" input-class="text-white"'

    # Dialog to add custom species
    with ui.dialog() as add_custom_species_form:
        with ui.card().classes("p-5 bg-gray-800 text-white rounded-lg"):
            ui.label("Add Custom Species").classes("text-xl font-bold mb-4")

            name_input = ui.input(label="Name:").props(common_input_props)

            description_input = ui.textarea(
                label="Description:").props(common_input_props)
            tolerance_levels_input = ui.textarea(
                label="Tolerance Levels:").props(common_input_props)
            image_url_input = ui.input(
                label="Image URL:").props(common_input_props)

            ui.button("Add", on_click=lambda: add_custom_species(
                name_input.value, description_input.value, tolerance_levels_input.value, image_url_input.value, results, add_custom_species_form
            )).classes("mt-2 bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded")

    eco_footer()


@ui.page("/encyclopedia")
def encyclopedia() -> None:
    encyclopedia_page()
