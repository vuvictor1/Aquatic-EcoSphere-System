# Authors: Jordan Morris and Victor Vu
# File: reminders.py
# Description: Reminders page for aquarium maintenance tasks with notification system.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
import time
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer

def reminders_page(): # Renders the reminders page
    eco_header()
    inject_style()

    columns = [ # Columns for the table to sort the task
        {'name': 'task', 'label': 'Task', 'field': 'task', 'required': True}, 
        {'name': 'due_date', 'label': 'Due Date (Days)', 'field': 'due_date', 'sortable': True}, 
    ] 
    rows = [ # Rows for the table to display task
        {'id': 0, 'task': 'Ex. Feed Fish', 'due_date': '1'},
    ]

    with ui.column().style('align-items: center; width: 100%;'): # Center the column
        # Creat the table
        with ui.table(title='Aquarium Maintenance Tasks', columns=columns, rows=rows, selection='multiple', pagination=10).classes('w-96') as table:
            with table.add_slot('top-right'): # Add a search bar to search for task
                with ui.input(placeholder='Search').props('type=search').bind_value(table, 'filter').add_slot('append'):
                    ui.icon('search') 
            with table.add_slot('bottom-row'): # Add a row to add new task
                with table.row():
                    with table.cell(): # Button for new tasks
                        ui.button(on_click=lambda: (
                            table.add_row({'id': time.time(), 'task': new_task.value, 'due_date': new_due_date.value}),
                            new_task.set_value(None),
                            new_due_date.set_value(None),
                        ), icon='add').props('flat fab-mini')
                    with table.cell():
                        new_task = ui.input('Task')
                    with table.cell():
                        new_due_date = ui.input('Due Date')

        ui.button('Remove', on_click=lambda: table.remove_rows(table.selected)) # take out items 
    eco_footer() # add footer

@ui.page('/reminders') # Route for reminders page
def reminders():
    reminders_page()