# File: reminders.py
# Description: Reminders page for aquarium maintenance tasks with notification system.

# Note: Current implementation is of reminder data is missing notification.
import time
import json
from nicegui import ui
from web_functions import eco_header, eco_footer, inject_style

DATA_FILE = "reminders_data.json"  # file to store reminders data locally


def load_data():  # Load data from file
    try:
        with open(DATA_FILE, "r") as file:  # parse the data
            return json.load(file)
    except FileNotFoundError:
        return []


def save_data(rows):  # Save data to file
    with open(DATA_FILE, "w") as file:  # write the data
        json.dump(rows, file)  # dump the data into json file


upcoming_task = None  # global variable for the upcoming task


def get_upcoming_task(rows):  # Task with the least amount of days for dashboard
    filtered_rows = [
        row for row in rows if int(row["priority"]) != 99
    ]  # ignore the example task

    if not filtered_rows:  # If no tasks
        return None
    return min(filtered_rows, key=lambda x: int(x["priority"]))


def reminders_page():  # Renders the reminders page
    eco_header()
    inject_style()

    columns = [  # Columns for the table to sort the task
        {"name": "task", "label": "Tasks", "field": "task", "required": True},
        {
            "name": "priority",
            "label": "Priority Level",
            "field": "priority",
            "sortable": True,
        },
    ]
    rows = load_data()  # Load data from file

    with ui.column().classes(
        "flex justify-center items-center w-full h-screen p-4 md:h-3/4 md:mt-20"
    ):  # Center the column
        with ui.element("div").classes(
            "outline_label p-6 md:p-12 bg-gray-800 rounded-lg shadow-lg w-full max-w-md"
        ):  # Responsive container
            ui.label("Reminders").classes(
                "text-white text-2xl md:text-3xl mb-5 text-center"
            )
            with ui.table(
                title="Maintenance Tasks",
                columns=columns,
                rows=rows,
                selection="multiple",
                pagination=10,
            ).classes("w-full mb-4") as table:
                with table.add_slot("top-right"):  # Add a search bar to search for task
                    with (
                        ui.input(placeholder="Search")
                        .props("type=search")
                        .bind_value(table, "filter")
                        .add_slot("append")
                    ):
                        ui.icon("search")

                with table.add_slot("bottom-row"):  # Add a row to add new task
                    with table.row():
                        with table.cell():  # Button for new tasks
                            ui.button(
                                on_click=lambda: (
                                    add_new_task(
                                        table, rows, new_task.value, new_priority.value
                                    )
                                ),
                                icon="add",
                            ).props("flat fab-mini")

                        with table.cell():  # Input for new task
                            new_task = ui.input("Task").classes(
                                "bg-gray-200 px-4 py-2 w-full mb-4"
                            )

                        with table.cell():  # Input for new priority
                            new_priority = ui.input("priority").classes(
                                "bg-gray-200 px-4 py-2 w-full mb-4"
                            )
            ui.button(
                "Remove",
                on_click=lambda: (
                    table.remove_rows(table.selected),
                    update_task(rows),
                    save_data(rows),  # save data to file
                ),
            ).classes(
                "w-full bg-red-500 text-white py-2 rounded mb-4"
            )  # take out items
    eco_footer()  # add footer

    def add_new_task(table, rows, task, priority):
        if task and priority:  # Check if task and priority are not empty
            table.add_row({"id": time.time(), "task": task, "priority": priority})
            new_task.set_value(None)  # default value none
            new_priority.set_value(None)
            update_task(rows)  # update the least days label
            save_data(rows)  # save data to file
        else:
            ui.notify(
                "Error: Please use valid inputs.", type="negative", position="center"
            )

    # Function to update the label with the task with the least amount of days left
    def update_task(rows):
        global upcoming_task
        # store the task with the least amount of days
        least_days_task = get_upcoming_task(rows)
        upcoming_task = least_days_task  # update the global variable

    update_task(rows)  # update the label


@ui.page("/reminders")  # Route for reminders page
def reminders():
    reminders_page()
