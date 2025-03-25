# File: encyclopedia.py
# Description: Encyclopedia page for the web interface
from nicegui import ui, html
from web_functions import inject_style, eco_header, eco_footer
import requests
import json
import os
import urllib.parse

# TODO:
# Make the editing through the add species part better, either fill
# in information from the other fields automatically or a button to fill in the info
# Add different fields for the different tolerance levels ("Other" field)
# Remove a species feature

# Load the species data from the JSON file
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
parent_dir_path = os.path.dirname(current_dir_path)
species_data_path = os.path.join(parent_dir_path, 'data', 'species_data.json')
# Define common props for inputs
common_input_props = 'label-color="white" input-class="text-white"'


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

                # Add an edit icon to each card
                ui.button(icon='edit', on_click=lambda s=species: open_edit_species_form(s, results_container)).classes(
                    "absolute top-2 right-2 bg-transparent text-white hover:text-blue-400"
                )

# Function to add custom species


def add_custom_species(name, species_name, description, tolerance_levels, image_url, results, add_species_form):
    if not name and not species_name:
        ui.notify("Please provide at least one valid name", type="error")
        return

    # Placeholder URL
    PLACEHOLDER_URL = "https://placehold.co/120"

    # Validate the image URL
    if not image_url.startswith("http"):
        image_url = PLACEHOLDER_URL

    try:
        result = urllib.parse.urlparse(image_url)
        if not all([result.scheme, result.netloc]):
            image_url = PLACEHOLDER_URL

        response = requests.head(image_url)
        if response.status_code != 200:
            image_url = PLACEHOLDER_URL
    except (ValueError, requests.RequestException):
        image_url = PLACEHOLDER_URL

    # Check if a species with the provided name already exists
    existing_species = next((species for species in species_data if species.get(
        "species_name") == species_name or species.get("name") == name), None)

    tolerance_levels_dict = {}
    for tolerance_level in tolerance_levels:
        key, value = tolerance_level.split(": ")
        tolerance_levels_dict[key] = value

    if existing_species:
        # Update the existing species with the new information
        existing_species["name"] = name
        existing_species["species_name"] = species_name
        existing_species["description"] = description
        existing_species["tolerance_levels"] = tolerance_levels_dict
        existing_species["image_url"] = image_url
    else:
        # Create a new species dictionary
        new_species = {
            "name": name,
            "species_name": species_name,
            "description": description,
            "tolerance_levels": tolerance_levels_dict,
            "image_url": image_url
        }

    # Add the new species to the species data
    species_data.append(new_species)

    # Save the updated species data to the JSON file
    with open(species_data_path, 'w', encoding='utf-8') as file:
        json.dump(species_data, file, ensure_ascii=False, indent=4)

    # Update the displayed species list
    display_species(species_data, results)

    if existing_species:
        ui.notify(f"Updated {name} in the encyclopedia!", type="positive")
    else:
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

    # Dialog to add custom species
    with ui.dialog() as add_custom_species_form:
        with ui.card().classes("p-5 bg-gray-800 text-white rounded-lg"):
            ui.label("Add Custom Species").classes("text-xl font-bold mb-4")

            name_input = ui.input(label="Common Name:").props(
                common_input_props)

            optional_species_name_input = ui.input(
                label="Species Name", placeholder="(Optional) e.g: Pteris volantis").props(common_input_props)

            description_input = ui.textarea(
                label="Description:").props(common_input_props)

            ui.label("Tolerance Levels:")

            # Store dynamic tolerance levels
            tolerance_entries = []

            def add_tolerance_level():
                """Dynamically add a new tolerance input row."""
                with tolerance_levels_container:
                    tolerance_type = ui.input(
                        label="Type:").props(common_input_props)
                    tolerance_value = ui.input(
                        label="Value:").props(common_input_props)
                    # Keep track of the inputs to extract their values later
                    tolerance_entries.append((tolerance_type, tolerance_value))

            # Container to hold dynamic tolerance inputs
            with ui.column() as tolerance_levels_container:
                pass

            # Button to add more tolerance levels
            ui.button("➕ Add Tolerance Level", on_click=add_tolerance_level).classes(
                "mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            )

            image_url_input = ui.input(
                label="Image URL:").props(common_input_props)

            # Button to add more tolerance levels
            ui.button("Submit Species", on_click=lambda: add_custom_species(
                name_input.value,
                optional_species_name_input.value,
                description_input.value,
                [f"{tolerance_type.value}: {tolerance_value.value}" for tolerance_type,
                    tolerance_value in tolerance_entries],
                image_url_input.value,
                results,
                add_custom_species_form
            )).classes(
                "mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            )

    # Dialog to edit a species
    with ui.dialog() as edit_custom_species_form:
        with ui.card().classes("p-5 bg-gray-800 text-white rounded-lg"):
            ui.label("Add Custom Species").classes("text-xl font-bold mb-4")

            name_input = ui.input(label="Common Name:").props(
                common_input_props)

            optional_species_name_input = ui.input(
                label="Species Name", placeholder="(Optional) e.g: Pteris volantis").props(common_input_props)

            description_input = ui.textarea(
                label="Description:").props(common_input_props)

            ui.label("Tolerance Levels:")

            # Store dynamic tolerance levels
            tolerance_entries = []

            def add_tolerance_level():
                """Dynamically add a new tolerance input row."""
                with tolerance_levels_container:
                    tolerance_type = ui.input(
                        label="Type:").props(common_input_props)
                    tolerance_value = ui.input(
                        label="Value:").props(common_input_props)
                    # Keep track of the inputs to extract their values later
                    tolerance_entries.append((tolerance_type, tolerance_value))

            # Container to hold dynamic tolerance inputs
            with ui.column() as tolerance_levels_container:
                pass

            # Button to add more tolerance levels
            ui.button("➕ Add Tolerance Level", on_click=add_tolerance_level).classes(
                "mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            )

            image_url_input = ui.input(
                label="Image URL:").props(common_input_props)

            # Button to add more tolerance levels
            ui.button("Submit Species", on_click=lambda: add_custom_species(
                name_input.value,
                optional_species_name_input.value,
                description_input.value,
                [f"{tolerance_type.value}: {tolerance_value.value}" for tolerance_type,
                    tolerance_value in tolerance_entries],
                image_url_input.value,
                results,
                add_custom_species_form
            )).classes(
                "mb-4 bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            )

    eco_footer()


@ui.page("/encyclopedia")
def encyclopedia() -> None:
    encyclopedia_page()
