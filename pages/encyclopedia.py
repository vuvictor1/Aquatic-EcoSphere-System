# File: encyclopedia.py
# Description: Encyclopedia page for the web interface
from nicegui import ui, html
from web_functions import inject_style, eco_header, eco_footer

species_data = [  # Sample data for aquatic species
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


def filter_species(query):  # Filter species based on search query
    query = query.lower()  # convert query to lowercase
    return [species for species in species_data if query in species["name"].lower()]


def display_species(species_list):  # Display species based on search query
    results.clear()  # clear previous results
    with results:  #
        for species in species_list:  # loop through species
            with ui.column().classes("w-full sm:w-1/2 md:w-1/4 lg:w-1/6 p-1"):
                with ui.card().classes(
                    "outline_label w-full mb-2 bg-gray-700 text-white"
                ):  # Card for each species
                    with ui.row():  # Row for species information
                        html.img(src="https://placehold.co/120")  # placeholder image
                    ui.label(species["name"]).classes("text-base font-bold")
                    ui.label(species["description"]).classes("text-xs")
                    ui.label(
                        f"Tolerance Levels: {species['tolerance_levels']}"
                    ).classes("text-xs text-gray-500")


def search(e):  # Search for species based on user input
    filtered_species = filter_species(e.value)
    display_species(filtered_species)


def encyclopedia_page():  # Encyclopedia page
    eco_header()  # header menu
    inject_style()  # inject CSS for background

    with ui.row().classes(
        "justify-center w-full mt-5"
    ):  # Center the encyclopedia title
        with ui.column().classes(
            "outline_label items-center bg-gray-800 p-5 rounded-lg w-full max-w-2xl"
        ):
            ui.label("Aquatic Species Encyclopedia").classes(
                "text-4xl text-white font-bold"
            )

            global search_field  # search bar
            search_field = (
                ui.input(placeholder="Search for species...")
                .props('autofocus outlined rounded item-aligned input-class="ml-3"')
                .classes("w-96 self-center mt-6 transition-all")
                .on("change", search)
                .style(
                    "width: 100%; margin-bottom: 20px; padding: 10px; border-radius: 25px; border: 1px solid #ccc; font-size: 16px; background-color: #e0e0e0;"
                )
            )

    global results  # results container
    results = ui.row().classes(
        "w-full mt-4 flex flex-wrap justify-center"
    )  # results container
    display_species(species_data)  # display all species initially
    eco_footer()  # footer function


@ui.page("/encyclopedia")  # Route to encyclopedia page
def encyclopedia():
    encyclopedia_page()
