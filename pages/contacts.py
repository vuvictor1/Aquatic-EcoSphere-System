# Authors: Victor Vu 
# File: contacts.py
# Description: Contacts page for the web interface
# Copyright (C) 2024 Victor V. Vu and Jordan Morris
# License: GNU GPL v3 - See https://www.gnu.org/licenses/gpl-3.0.en.html
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer, inject_lottie

def contacts_page(): # Contacts page
    eco_header() # header menu
    inject_style() # inject CSS for background

    with ui.row().style(f'justify-content: center; width: 100%; margin-top: 20px; background-color: #3B3B3B;'): # Center the contacts title

        inject_lottie() # inject lottie animation
        lottie_url = 'https://lottie.host/39c13f90-cf6a-48cd-9991-b7786de51bff/4fkeUtAhp9.json' # lottie animation
        with ui.column().classes('mail').style(f'align-items: center; background-color: #2C2C2C; padding: 20px; border-radius: 10px;'): # Column for the contacts
            ui.html(f'''<lottie-player src="{lottie_url}" loop autoplay speed="0.25" style="height: 150px;"></lottie-player>''') # play file
            ui.label('Contact Us').style(f'font-size: 32px; color: white;') # Mail title
            # Create input fields for the form
            ui.html(f'''
                <form action="https://api.web3forms.com/submit" method="POST" style="width: 100%;">
                    <input type="hidden" name="access_key" value="5378da98-377b-464f-990d-f97e70c28023">
                    <input type="text" name="name" placeholder="Your Name" required style="font-size: 16px; width: 100%; margin-bottom: 10px; background-color: #3B3B3B; color: white; border: none; padding: 10px; border-radius: 5px;">
                    <input type="email" name="email" placeholder="Your Email (So we can contact you)" required style="font-size: 16px; width: 100%; margin-bottom: 10px; background-color: #3B3B3B; color: white; border: none; padding: 10px; border-radius: 5px;">
                    <textarea name="message" placeholder="Your Message" required style="font-size: 16px; width: 100%; height: 300px; margin-bottom: 10px; background-color: #3B3B3B; color: white; border: none; padding: 10px; border-radius: 5px;"></textarea>
                    <input type="checkbox" name="botcheck" class="hidden" style="display: none;">
                    <div style="text-align: center;">
                        <button type="submit" style="color: white; width: 25%; background-color: #5898D4; padding: 10px 20px; cursor: pointer; border-radius: 5px; font-size: 20px;">Send</button>
                    </div>
                </form>
            ''')
            ui.label('📬 Product Owner: vuvictor@csu.fullerton.edu').style(f'font-size: 20px; color: white;') # mail label
    eco_footer() # footer function

@ui.page('/contacts') # Route to contacts page
def contacts():
    contacts_page()