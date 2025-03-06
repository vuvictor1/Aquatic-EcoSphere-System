# File: encyclopedia.py
# Description: Encyclopedia page for the web interface
from nicegui import ui, html
from web_functions import inject_style, eco_header, eco_footer
import requests


# FishBase API Endpoint
FISHBASE_API_URL = "https://fishbase.ropensci.org/species"

# Sample data for aquatic species
species_data = [
    {"name": "Clownfish", "description": "Clownfish are small, brightly colored fish found in warm waters.",
        "tolerance_levels": "Temperature: 24-27°C, pH: 7.8-8.4, Salinity: 1.020-1.025", "image_url": "https://www.aquariumofpacific.org/images/made_new/images-uploads-clownfish_400_q85.jpg"},
    {"name": "Neon Tetra", "description": "Neon Tetras are small, colorful fish that are popular in home aquariums.",
        "tolerance_levels": "Temperature: 20-26°C, pH: 6.0-7.0"},
    {"name": "Guppy", "description": "Guppies are small, colorful fish that are easy to care for and breed.",
        "tolerance_levels": "Temperature: 22-28°C, pH: 7.0-8.0"},
    {"name": "Betta Fish", "description": "Betta Fish are known for their vibrant colors and long, flowing fins.",
        "tolerance_levels": "Temperature: 24-30°C, pH: 6.5-7.5"},
    {"name": "Angelfish", "description": "Angelfish are elegant fish with long fins and a distinctive shape.",
        "tolerance_levels": "Temperature: 24-28°C, pH: 6.8-7.8"},
    {"name": "Goldfish", "description": "Goldfish are hardy fish that come in a variety of colors and shapes.",
        "tolerance_levels": "Temperature: 10-24°C, pH: 6.0-8.0"},
    {"name": "Molly Fish", "description": "Molly Fish are versatile fish that can live in both freshwater and saltwater.",
        "tolerance_levels": "Temperature: 24-28°C, pH: 7.5-8.5"},
    {"name": "Zebra Danio", "description": "Zebra Danios are small, active fish with distinctive horizontal stripes.",
        "tolerance_levels": "Temperature: 18-24°C, pH: 6.5-7.5"},
    {"name": "Corydoras Catfish", "description": "Corydoras Catfish are small, bottom-dwelling fish that are great for cleaning the tank.",
        "tolerance_levels": "Temperature: 22-26°C, pH: 6.0-7.5"},
    {"name": "Cherry Shrimp", "description": "Cherry Shrimp are small, colorful shrimp that are great for planted tanks.",
        "tolerance_levels": "Temperature: 22-28°C, pH: 6.5-8.0"},
]


def fetch_fishbase_data(species_name: str):
    """Query FishBase API for species data."""
    params = {"Genus": species_name.split(
    )[0], "Species": species_name.split()[-1]}
    response = requests.get(FISHBASE_API_URL, params=params)
    if response.status_code == 200:
        data = response.json()["data"]
        return data[0] if data else None
    return None


def query_fishbase(species_name: str, results_container: ui.row):
    """Query FishBase API and update the offline database."""
    species_data_fetched = fetch_fishbase_data(species_name)

    if species_data_fetched:
        new_species = {
            "name": f"{species_data_fetched['Genus']} {species_data_fetched['Species']}",
            "description": f"Family: {species_data_fetched['Family']}, Habitat: {species_data_fetched['Habitat']}",
            "tolerance_levels": f"Temperature: {species_data_fetched.get('TempMin', 'Unknown')}°C - {species_data_fetched.get('TempMax', 'Unknown')}°C",
        }
        species_data.append(new_species)
        ui.notify(f"✅ {species_name} added to database!", type="success")
    else:
        ui.notify(f"❌ {species_name} not found.", type="error")

    display_species(species_data, results_container)


def filter_species(query: str) -> list:
    """Filter species based on the query."""
    query = query.lower().strip()
    filtered = [species for species in species_data if
                query in species["name"].lower() or
                query in species["description"].lower() or
                query in species["tolerance_levels"].lower()]
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


def encyclopedia_page() -> None:
    """
    Encyclopedia page.
    """

    eco_header()
    inject_style()

    with ui.row().classes("justify-center w-full mt-5"):
        with ui.column().classes("outline_label items-center bg-gray-800 p-5 rounded-lg w-full max-w-2xl"):
            ui.label("Aquatic Species Encyclopedia").classes(
                "text-4xl text-white font-bold")

            search_field = (
                ui.input(placeholder="Search for species...")
                .props('autofocus outlined rounded item-aligned input-class="ml-3"')
                .classes("w-96 self-center mt-6 transition-all")
                .on_value_change(lambda e: display_species(filter_species(e.value), results))
                .style("width: 100%; margin-bottom: 20px; padding: 10px; border-radius: 25px; border: 1px solid #ccc; font-size: 16px; background-color: #e0e0e0;")
            )

            # Add a button to query FishBase
            # Make it look nice
            query_button = ui.button(
                "Query Fishbase", on_click=lambda: query_fishbase(search_field.value, results))

    results = ui.row().classes("w-full mt-4 flex flex-wrap justify-center")
    display_species(species_data, results)
    eco_footer()


@ui.page("/encyclopedia")
def encyclopedia() -> None:
    encyclopedia_page()
