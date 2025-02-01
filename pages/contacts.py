# File: contacts.py
# Description: Contacts page for the web interface
from nicegui import ui
from web_functions import inject_style, eco_header, eco_footer, inject_lottie

lottie_url = 'https://lottie.host/39c13f90-cf6a-48cd-9991-b7786de51bff/4fkeUtAhp9.json' # lottie animation

def contacts_page():  # Contacts page
    eco_header()  # header menu
    inject_style()  # inject CSS for background

    with ui.row().classes('justify-center w-full my-4 px-4'):  # Center the contacts title and add padding for mobile
        inject_lottie()  # inject lottie animation
        with ui.column().style('max-width: 90%;').classes('items-center text-center p-5 bg-gray-800 rounded-lg shadow-lg'):
            ui.html(f'''<lottie-player src="{lottie_url}" loop autoplay speed="0.25"></lottie-player>''').classes('w-48 mx-auto')  # play file
            ui.label('Contact Us').classes('text-white text-4xl font-bold')  # mail title
            # Create input fields for the form
            ui.html(f'''
                <form action="https://api.web3forms.com/submit" method="POST" class="w-full">
                    <input type="hidden" name="access_key" value="5378da98-377b-464f-990d-f97e70c28023">
                    <input type="text" name="name" placeholder="Your Name" required class="text-lg w-full mb-2 bg-gray-700 text-white border-none p-2 rounded-md">
                    <input type="email" name="email" placeholder="Your Email (So we can reply)" required class="text-lg w-full mb-2 bg-gray-700 text-white border-none p-2 rounded-md">
                    <textarea name="message" placeholder="Your Message" required class="text-lg w-full h-72 mb-2 bg-gray-700 text-white border-none p-2 rounded-md"></textarea>
                    <input type="checkbox" name="botcheck" class="hidden">
                    <div class="text-center">
                        <button type="submit" class="text-white w-full sm:w-1/2 p-2 cursor-pointer rounded-md text-xl" style="background-color: #5898D4;">Send Message</button>
                    </div>
                </form>
            ''')
            ui.label('📬 Product Owner: vuvictor@csu.fullerton.edu').classes('text-white text-lg')  # mail label
    eco_footer()  # footer function
ui.html('''<meta name="viewport" content="width=device-width, initial-scale=1">''') # meta tag for viewport settings

@ui.page('/contacts')  # Route to contacts page
def contacts():
    contacts_page()