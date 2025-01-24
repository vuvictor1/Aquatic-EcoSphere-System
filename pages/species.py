from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

# Helper function to create a card for a species
def card(species):
    with ui.card().classes('p-2').props('draggable="true"') as card_container:
        ui.label(species['title']).classes('p-2').on('dragstart', lambda e: e.args['event'].dataTransfer.setData('species', species['title']))

# Helper function to create a column with a title
def column(title, species_list, on_drop):
    with ui.column().classes('p-2'):
        ui.label(title).classes('text-lg mb-2')
        # Create a droppable container using ui.element
        droppable_area = ui.element('div').classes('border p-4 min-h-[200px]').on('drop', on_drop).on('dragover', lambda e: e.prevent_default())

        for species in species_list:
            with droppable_area:
                card(species)

# Drop handler for moving species between available and tank
def on_drop(event, available_species, tank_species):
    species_name = event.args['event'].dataTransfer.getData('species')

    # Check if the species exists in available_species or tank_species, and move it accordingly
    source_list = available_species if any(species['title'] == species_name for species in available_species) else tank_species
    target_list = tank_species if source_list == available_species else available_species

    # Move species between lists
    for species in source_list:
        if species['title'] == species_name:
            source_list.remove(species)
            target_list.append(species)
            break

    # Re-render the page to update the lists
    ui.clear()
    species_page()

# Species page definition
def species_page() -> None:
    inject_style()
    eco_header()
    # Sample data for fish species
    available_species = [
        {'title': 'Goldfish'},
        {'title': 'Betta'},
        {'title': 'Guppy'},
        {'title': 'Angelfish'},
    ]

    tank_species = [
        {'title': 'Tetra'},
        {'title': 'Molly'},
    ]

    # Create columns for available species and tank species
    with ui.row():
        # Column for available species
        column('Available Species', available_species, 
               lambda e: on_drop(e, available_species, tank_species))

        # Column for tank species
        column('Tank Species', tank_species, 
               lambda e: on_drop(e, available_species, tank_species))

    eco_footer()
# Route for species page
@ui.page('/species')
def species():
    species_page()
