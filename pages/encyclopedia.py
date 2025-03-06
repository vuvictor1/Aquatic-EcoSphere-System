# File: encyclopedia.py
# Description: Encyclopedia page for the web interface
from nicegui import ui, html
from web_functions import inject_style, eco_header, eco_footer

# Sample data for aquatic species
species_data = [
    {
        "name": "Clownfish",
        "description": "Clownfish are small, brightly colored fish found in warm waters.",
        "tolerance_levels": "Temperature: 24-27°C, pH: 7.8-8.4, Salinity: 1.020-1.025",
    },
    {
        "name": "Neon Tetra",
        "description": "Neon Tetras are small, colorful fish that are popular in home aquariums.",
        "tolerance_levels": "Temperature: 20-26°C, pH: 6.0-7.0",
    },
    {
        "name": "Guppy",
        "description": "Guppies are small, colorful fish that are easy to care for and breed.",
        "tolerance_levels": "Temperature: 22-28°C, pH: 7.0-8.0",
    },
    {
        "name": "Betta Fish",
        "description": "Betta Fish are known for their vibrant colors and long, flowing fins.",
        "tolerance_levels": "Temperature: 24-30°C, pH: 6.5-7.5",
    },
    {
        "name": "Angelfish",
        "description": "Angelfish are elegant fish with long fins and a distinctive shape.",
        "tolerance_levels": "Temperature: 24-28°C, pH: 6.8-7.8",
    },
    {
        "name": "Goldfish",
        "description": "Goldfish are hardy fish that come in a variety of colors and shapes.",
        "tolerance_levels": "Temperature: 10-24°C, pH: 6.0-8.0",
    },
    {
        "name": "Molly Fish",
        "description": "Molly Fish are versatile fish that can live in both freshwater and saltwater.",
        "tolerance_levels": "Temperature: 24-28°C, pH: 7.5-8.5",
    },
    {
        "name": "Zebra Danio",
        "description": "Zebra Danios are small, active fish with distinctive horizontal stripes.",
        "tolerance_levels": "Temperature: 18-24°C, pH: 6.5-7.5",
    },
    {
        "name": "Corydoras Catfish",
        "description": "Corydoras Catfish are small, bottom-dwelling fish that are great for cleaning the tank.",
        "tolerance_levels": "Temperature: 22-26°C, pH: 6.0-7.5",
    },
    {
        "name": "Cherry Shrimp",
        "description": "Cherry Shrimp are small, colorful shrimp that are great for planted tanks.",
        "tolerance_levels": "Temperature: 22-28°C, pH: 6.5-8.0",
    },
]


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
    """Update the displayed species list dynamically."""
    print(f"📢 Updating UI with {len(species_list)} species")
    results_container.clear()
    with results_container:
        for species in species_list:
            with ui.card().classes("w-64 my-2 p-3 bg-gray-700 text-white"):
                html.img(src="https://placehold.co/120")
                ui.label(species["name"]).classes("text-lg font-bold")
                ui.label(species["description"]).classes("text-sm text-gray-300")
                ui.label(f"Tolerance: {species['tolerance_levels']}").classes(
                    "text-xs text-gray-500"
                )
    ui.update()


def encyclopedia_page() -> None:
    """Encyclopedia page."""
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

    results = ui.row().classes("w-full mt-0 flex flex-wrap justify-center")
    display_species(species_data, results)
    eco_footer()


@ui.page("/encyclopedia")
def encyclopedia() -> None:
    encyclopedia_page()
