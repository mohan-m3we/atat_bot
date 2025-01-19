import pyttsx3
import speech_recognition as sr
from datetime import date, datetime, timedelta
import os
import json
import webbrowser
import requests
import keyboard  # For keyboard events
import tkinter as tk  # For the chatbot GUI
from threading import Thread
from app import ChatBot  # Import ChatBot from the app.py module

# ------------- Object Initialization ---------------
today = date.today()
r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)

appointments = []  # To store appointment details

# ------------- Functions ---------------

def reply(audio):
    """Respond with voice and GUI."""
    ChatBot.addAppMsg(audio)
    print(audio)
    engine.say(audio)
    engine.runAndWait()

def wish():
    """Wish the user based on the time of day."""
    hour = datetime.now().hour
    if hour < 12:
        reply("Good Morning!")
    elif hour < 18:
        reply("Good Afternoon!")
    else:
        reply("Good Evening!")
    reply("I am here to assist you. How may I help?")

def record_audio():
    """Capture voice input from the user."""
    with sr.Microphone() as source:
        r.pause_threshold = 0.8
        r.energy_threshold = 500
        reply("Listening...")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            return r.recognize_google(audio).lower()
        except sr.UnknownValueError:
            reply("Sorry, I didn't catch that. Could you repeat?")
            return ""
        except sr.RequestError:
            reply("Network error. Please check your internet connection.")
            return ""
        except Exception as e:
            reply(f"An error occurred: {e}")
            return ""

def book_appointment():
    """Handle appointment booking process."""
    reply("Sure, I can help with booking an appointment.")
    url = "https://dealer-locator.cars.tatamotors.com/location/karnataka/bangalore"
    try:
        webbrowser.open(url)
        reply("The Tata Motors Dealer Locator for Bangalore has been opened in your browser. Please choose a showroom and tell me the name.")
    except Exception as e:
        reply(f"Could not open the Tata Motors Dealer Locator page. Error: {e}")
        return

    reply("Please say the name of the showroom you chose.")
    location = record_audio()
    if location:
        appointment_date = today + timedelta(days=2)
        reply(f"Your appointment will be booked for {appointment_date.strftime('%B %d')}.")
        appointment_time = datetime.strptime("11:00 AM", "%I:%M %p").time()
        reply(f"Your appointment will be scheduled at {appointment_time.strftime('%I:%M %p')}.")
        appointment = {
            "location": location,
            "date": appointment_date.strftime("%Y-%m-%d"),
            "time": appointment_time.strftime("%H:%M:%S"),
        }
        appointments.append(appointment)
        save_appointments()
        reply(f"Your appointment has been booked at {location} on {appointment['date']} at {appointment['time']}.")
        reply("Is there anything else I can assist you with?")
    else:
        reply("Could not understand the showroom name. Please try again.")

def save_appointments():
    """Save appointments to a JSON file."""
    with open("appointments.json", "w") as f:
        json.dump(appointments, f)

def google_search(query):
    """Search Google for the given query."""
    reply(f"Searching for {query} on Google.")
    url = f"https://google.com/search?q={query}"
    try:
        webbrowser.open(url)
        reply("Here are the search results.")
    except Exception as e:
        reply(f"Could not open Google. Error: {e}")

def open_tata_motors():
    """Open the Tata Motors website."""
    reply("Opening the Tata Motors website.")
    try:
        webbrowser.open("https://www.tatamotors.com")
        reply("Here is the Tata Motors website.")
    except Exception as e:
        reply(f"Could not open the Tata Motors website. Error: {e}")

def tata_nexon_specifications():
    """Provide Tata Nexon specifications and competitive products."""
    specifications = (
        "The Tata Nexon is a compact SUV with the following specifications:\n"
        "- Engine: 1.2L Turbocharged Revotron Petrol Engine or 1.5L Turbocharged Revotorq Diesel Engine.\n"
        "- Transmission: 6-speed manual or 6-speed AMT.\n"
        "- Mileage: 17-24 km/l depending on the variant.\n"
        "- Safety: 5-star Global NCAP safety rating, ABS with EBD, and airbags.\n"
        "- Features: Touchscreen infotainment system, connected car technology, automatic climate control, and more.\n"
        "- Variants: XE, XM, XZ, XZ+, and XZ+(O).\n"
    )
    reply(specifications)

    # Open Tata Nexon specifications page
    try:
        url = "https://cars.tatamotors.com/suv/nexon"
        webbrowser.open(url)
        reply("The Tata Nexon specifications page is now open in your browser.")
    except Exception as e:
        reply(f"Could not open the Tata Nexon specifications page. Error: {e}")

    # Competitive Products Search
    competitors = [
        {"name": "Hyundai Venue", "url": "https://www.hyundai.com/in/en/find-a-car/venue"},
        {"name": "Kia Sonet", "url": "https://www.kia.com/in/sonet/"},
        {"name": "Maruti Suzuki Vitara Brezza", "url": "https://www.marutisuzuki.com/cars/vitara-brezza"},
        {"name": "Mahindra XUV300", "url": "https://auto.mahindra.com/suv/xuv300"},
        {"name": "Ford EcoSport", "url": "https://www.ford.com/in/suvs/ecosport"}
    ]

    comparison_message = "Here are some competitive products in the market:\n"
    for competitor in competitors:
        comparison_message += f"- {competitor['name']}: {competitor['url']}\n"
    
    reply(comparison_message)

def respond(voice_data):
    """Process user commands."""
    if "book an appointment" in voice_data:
        book_appointment()
    elif "search" in voice_data:
        query = voice_data.split("search", 1)[1].strip()
        google_search(input("Type which car u want to search:")
    elif "open tata motors website" in voice_data:
        open_tata_motors()
    elif "tata nexon" in voice_data:
        tata_nexon_specifications()
    elif "hello" in voice_data or "hi" in voice_data:
        wish()
    elif "bye" in voice_data or "exit" in voice_data:
        reply("Goodbye! Have a great day.")
        ChatBot.started = False  # Properly stopping the chatbot
        os._exit(0)
    else:
        reply("I'm not sure how to help with that.")

def on_keyboard_input(event):
    """Handle keyboard input in the GUI."""
    input_text = entry.get()  # Get text from input box
    if input_text:
        respond(input_text.lower())  # Process the command
        entry.delete(0, tk.END)  # Clear the input box

# ------------- GUI Setup ---------------

def setup_gui():
    """Set up the ChatBot GUI."""
    global entry
    root = tk.Tk()
    root.title("ChatBot Interface")
    
    # Create a Text Box to show ChatBot responses
    chat_box = tk.Text(root, height=15, width=50)
    chat_box.pack()

    # Create an Entry Box for user input
    entry = tk.Entry(root, width=50)
    entry.pack()

    # Button to send text input to the chatbot
    send_button = tk.Button(root, text="Send", width=20, command=lambda: respond(entry.get().lower()))
    send_button.pack()

    # Bind keyboard events
    entry.bind("<Return>", on_keyboard_input)

    root.mainloop()

# ------------- Main Driver Code ---------------

def stop_chatbot_on_keypress():
    """Monitor keyboard input to stop chatbot when any key is pressed."""
    while True:
        if keyboard.is_pressed():  # If any key is pressed
            reply("Stopping the chatbot. Goodbye!")
            ChatBot.started = False
            os._exit(0)  # Exit the program

def main():
    """Main function to initialize and run the chatbot."""
    # Start the ChatBot GUI in a separate thread
    t1 = Thread(target=ChatBot.start)
    t1.start()

    # Start the keypress monitoring in a separate thread
    t2 = Thread(target=stop_chatbot_on_keypress)
    t2.daemon = True  # Set as daemon so it exits when the main thread exits
    t2.start()

    # Initialize the GUI
    setup_gui()

if __name__ == "__main__":
    main()
