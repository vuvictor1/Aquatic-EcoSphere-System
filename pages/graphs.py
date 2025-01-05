# Authors: Victor Vu 
# File: contacts.py
# Description: Graphing page for the web interface
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer
from data_functions import generate_graphs, get_all_data

def graphs_page(graph_container, labels): # Graphs page function
    eco_header() # header menu
    inject_style() # inject CSS for background

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'):
        ui.label('Graphing').style('font-size: 32px; color: white;') # Add title

    with ui.dialog() as date_dialog: # Date range selection dialog
        with ui.column().style('background-color: #2C2C2C; padding: 40px; border-radius: 10px;'): # Box container
            ui.label('Select Date Range:').style('color: #FFFFFF; font-size: 20px; background-color: #333333; padding: 20px;')
            date_input = ui.input('Date range').style('display: none;') # get date input but don't display to user
            date_picker = ui.date().props('range') # date picker menu

            def update_date_input(): # Update date input based on selected range
                selected_range = date_picker.value # get selected range
                date_input.value = f"{selected_range['from']} - {selected_range['to']}" if selected_range and 'from' in selected_range and 'to' in selected_range else None
            date_picker.on('update:model-value', update_date_input) # update date input based on calendar selection

            with ui.row().style('margin-top: 10px;'): # Filter data button
                ui.button('Filter Data', on_click=lambda: (
                    generate_graphs(graph_container, get_all_data(
                        *date_input.value.split(' - ')) if date_input.value else get_all_data()),
                    date_dialog.close()
                )).style('background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Select date range button
        ui.button('Select Date Range', on_click=lambda: date_dialog.open()).style(
            'background-color: #3AAFA9; color: #FFFFFF; margin-top: 10px;')

    graph_container = ui.row().style('justify-content: center; width: 100%;') # graph container
    generate_graphs(graph_container) # call generate graphs

    with ui.row().style('justify-content: center; width: 100%;'): # Refresh graphs button
        ui.button('Refresh Graphs', on_click=lambda: generate_graphs(
            graph_container)).style('background-color: #3AAFA9; color: #FFFFFF;')
    eco_footer() # footer menu
        
@ui.page('/graphs') # Route to graphs page
def graphs():
    from main_system import graph_container, labels # import globals
    graphs_page(graph_container, labels) # pass global to graphs page