# Authors: Jordan Morris and Victor Vu
# File: reminders.py
# Description: Reminders page for aquarium maintenance tasks with notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html

# Note: Current implementation is of reminder data is not persistent.-------------------
import time
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

def get_task_with_least_days(rows): # Task with the least amount of days for dashboard
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
        with ui.table(title='Aquarium Maintenance Tasks', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-96') as table:
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
                            update_least_days_label(rows) # update the least days label
                        ), icon='add').props('flat fab-mini') 
                        
                    with table.cell(): # Input for new task
                        new_task = ui.input('Task')
                    with table.cell(): # Input for new frequency
                        new_frequency = ui.input('Frequency')

        ui.button('Remove', on_click=lambda: (
            table.remove_rows(table.selected),
            update_least_days_label(rows) # Update the least days label
        )) # take out items 
    eco_footer() # add footer

    # Function to update the label with the task with the least amount of days left --------send tto the dashbaord later
    def update_least_days_label(rows):
        least_days_task = get_task_with_least_days(rows)
        if least_days_task:
            least_days_label.set_text(f"Task with the least days left: {least_days_task['task']} ({least_days_task['frequency']} days)")
        else:
            least_days_label.set_text("You have no urgent tasks")

    # Initial display of the task with the least amount of days left
    least_days_label = ui.label()
    update_least_days_label(rows)

@ui.page('/reminders') # Route for reminders page
def reminders():
    reminders_page()