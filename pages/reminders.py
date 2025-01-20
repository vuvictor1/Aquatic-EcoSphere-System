# Authors: Jordan Morris and Victor Vu
# File: reminders.py
# Description: Reminders page for aquarium maintenance tasks.
# Copyright (C) 2025 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer
from dataclasses import dataclass, field
from typing import List

@dataclass
class Reminder:
    label: str
    value: str

@dataclass
class ReminderList:
    reminders: List[Reminder] = field(default_factory=list)

    def add(self, label: str, value: str) -> None:
        self.reminders.append(Reminder(label, value))

    def remove(self, reminder: Reminder) -> None:
        self.reminders.remove(reminder)

reminder_list = ReminderList([
    Reminder('Water Change', 'Every 7 days'),
    Reminder('Filter Cleaning', 'Every 30 days'),
    Reminder('Check pH Levels', 'Every 14 days'),
    Reminder('Inspect Equipment', 'Every 30 days'),
])

def reminders_page(): # Renders the reminders page
    eco_header()
    inject_style()

    # Inject custom CSS styles
    ui.html("""
        <style>
            .q-field__native {
                color: white;
            }
            .q-field__label {
                color: white;
            }
            @media (max-width: 600px) {
                .q-field__native, .q-field__label {
                    font-size: 14px;
                }
                .q-field__label {
                    text-align: center;
                }
            }
        </style>
    """)

    with ui.card().style('background-color: #333333; padding: 20px; border-radius: 10px; width: 90%; max-width: 800px; margin: auto;'): # Main card
        with ui.row().style('justify-content: center; width: 100%; margin-top: 10px;'): # Title for the page
            ui.label('Reminders').style('font-size: 32px; color: white;')

        with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Reminder settings
            ui.label('Set Reminders').style('font-size: 24px; color: white;')

        for reminder in reminder_list.reminders: # Loop through input fields to display them
            with ui.row().style('justify-content: center; align-items: center; width: 100%; margin-top: 10px;'):
                ui.label(reminder.label).style('font-size: 18px; color: white; text-align: center;')
                input_field = ui.input(reminder.label, value=reminder.value).style(
                    'width: 200px; background-color: #333333; margin-left: 10px; margin-right: 10px;')
                ui.button('Remove', on_click=lambda r=reminder: remove_reminder(r)).style('background-color: #FF6F61; color: white;')

        with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Add new reminder
            new_label = ui.input('New Reminder Label').style('width: 200px; background-color: #333333; margin-right: 10px;')
            new_value = ui.input('New Reminder Value').style('width: 200px; background-color: #333333; margin-right: 10px;')
            ui.button('Add', on_click=lambda: add_reminder(new_label.value, new_value.value)).style('background-color: #3AAFA9; color: white;')

        with ui.row().style('justify-content: center; width: 100%; margin-top: 20px;'): # Save button
            ui.button('Save', on_click=save_reminders).style('background-color: #3AAFA9; color: white;')

    eco_footer() # add footer

def add_reminder(label, value):
    reminder_list.add(label, value)
    reminders_page()

def remove_reminder(reminder):
    reminder_list.remove(reminder)
    reminders_page()

def save_reminders(): # Save reminders to database or file (not implemented)
    for reminder in reminder_list.reminders:
        print(f'Saving reminder: {reminder.label}={reminder.value}')

@ui.page('/reminders') # Route for reminders page
def reminders():
    reminders_page()