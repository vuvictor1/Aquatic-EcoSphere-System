# Authors: Jordan Morris and Victor Vu
# File: reminders.py
# Description: Reminders page for aquarium maintenance tasks with notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

# Note: Current implementation is of reminder data is not persistent, is missing notification and cannot update on the dashboard.
import time
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

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
    rows = [ # Rows for the table to display task
        {'id': 0, 'task': 'Example Task', 'frequency': '99'},
    ]

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
                            table.add_row({'id': time.time(), 'task': new_task.value, 'frequency': new_frequency.value}), 
                            new_task.set_value(None), # default value none
                            new_frequency.set_value(None),
                            update_task(rows) # update the least days label
                        ), icon='add').props('flat fab-mini') 
                        
                    with table.cell(): # Input for new task
                        new_task = ui.input('Task')

                    with table.cell(): # Input for new frequency
                        new_frequency = ui.input('Frequency')
        ui.button('Remove', on_click=lambda: (table.remove_rows(table.selected), update_task(rows))) # take out items 
    eco_footer() # add footer

    def update_task(rows): # Function to update the label with the task with the least amount of days left
        global upcoming_task 
        least_days_task = get_upcoming_task(rows) # store the task with the least amount of days
        upcoming_task = least_days_task # update the global variable
    update_task(rows) # update the label

@ui.page('/reminders') # Route for reminders page
def reminders():
    reminders_page()