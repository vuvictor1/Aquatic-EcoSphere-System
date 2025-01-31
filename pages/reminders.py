# Authors: Jordan Morris and Victor Vu
# File: reminders.py
# Description: Reminders page for aquarium maintenance tasks with notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

# Note: Current implementation is of reminder data is missing notification and does not update on the dashboard.
import time
import json
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

DATA_FILE = 'reminders_data.json' # file to store reminders data locally

def load_data(): # Load data from file
    try:
        with open(DATA_FILE, 'r') as file: # parse the data
            return json.load(file) 
    except FileNotFoundError: 
        return []
 
def save_data(rows): # Save data to file
    with open(DATA_FILE, 'w') as file: # write the data
        json.dump(rows, file) # dump the data into json file

upcoming_task = None # global variable for the upcoming task
def get_upcoming_task(rows): # Task with the least amount of days for dashboard
    filtered_rows = [row for row in rows if int(row['frequency']) != 99] # ignore the example task

    if not filtered_rows: # If no tasks
        return None
    return min(filtered_rows, key=lambda x: int(x['frequency'])) 
 
def reminders_page(): # Renders the reminders page
    eco_header()
    inject_style()

    columns = [ # Columns for the table to sort the task
        {'name': 'task', 'label': 'Task', 'field': 'task', 'required': True}, 
        {'name': 'frequency', 'label': 'Frequency (Days)', 'field': 'frequency', 'sortable': True}, 
    ] 
    rows = load_data() # Load data from file

    with ui.column().style('align-items: center; width: 100%;'): # Center the column
        # Create the table
        with ui.table(title='Maintenance Tasks', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-96') as table:
            with table.add_slot('top-right'): # Add a search bar to search for task
                with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                    ui.icon('search') 

            with table.add_slot('bottom-row'): # Add a row to add new task
                with table.row():
                    with table.cell(): # Button for new tasks
                        ui.button(on_click=lambda: (
                            add_new_task(table, rows, new_task.value, new_frequency.value)
                        ), icon='add').props('flat fab-mini') 
                        
                    with table.cell(): # Input for new task
                        new_task = ui.input('Task')

                    with table.cell(): # Input for new frequency
                        new_frequency = ui.input('Frequency')
        ui.button('Remove', on_click=lambda: (
            table.remove_rows(table.selected), 
            update_task(rows), 
            save_data(rows) # save data to file
        )) # take out items 
    eco_footer() # add footer

    def add_new_task(table, rows, task, frequency):
        if task and frequency: # Check if task and frequency are not empty
            table.add_row({'id': time.time(), 'task': task, 'frequency': frequency})
            new_task.set_value(None) # default value none
            new_frequency.set_value(None)
            update_task(rows) # update the least days label
            save_data(rows) # save data to file
        else: 
            ui.notify('Error: Please use valid inputs.', type='negative', position='center')

    def update_task(rows): # Function to update the label with the task with the least amount of days left
        global upcoming_task 
        least_days_task = get_upcoming_task(rows) # store the task with the least amount of days
        upcoming_task = least_days_task # update the global variable
    update_task(rows) # update the label

@ui.page('/reminders') # Route for reminders page
def reminders():
    reminders_page()