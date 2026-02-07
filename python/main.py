import serial
import serial.tools.list_ports
import arduino_funcs as af
import os
from dotenv import load_dotenv
from google import genai
import time

def select_arduino_port():
    # Lists available serial ports and prompts the user to select one.
    # Get a list of available ports
    available_ports = [
        p for p in serial.tools.list_ports.comports()
        if p.description and p.description.lower() != "n/a"
    ]
    
    if not available_ports:
        print("No serial ports found.")
        return None

    print("Available serial ports:")
    # Display ports with an index number
    for i, port in enumerate(available_ports):
        # Using port.device for a reliable identifier
        print(f"{i + 1}: {port.device} - {port.description}")

    while True:
        try:
            # Prompt user for input
            choice = input("Port number: ")

            # Convert input to integer index
            port_index = int(choice) - 1

            # Validate the choice
            if 0 <= port_index < len(available_ports):
                selected_port = available_ports[port_index].device
                print(f"Selected port: {selected_port}")
                return selected_port
            else:
                print("Invalid input.")
        
        except ValueError:
            # Handle non-integer input
            print("Invalid input.")

load_dotenv()
api_key = os.getenv("API_KEY")
if(api_key):
    client = genai.Client(api_key=api_key)
else:
    print("ERROR: Could not get API_KEY from .env")
instructions = "Arduino Assistant. Format: [Confirmation sentence].\n[pin][h/l] Constraint: Always end with the code. No extra text after code. Example: Pin 2 HIGH.\n2h"

def get_ai_response(contents):
    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            config={
                "system_instruction": instructions,
            },
            contents=contents
        )
        return response.text
    except Exception as e:
        return "ERROR: ", e

def main():
    print("== Arduino AI-Gemini ==")
    print("Talk to Gemini 3 Flash to help you control your Arduino!\n")

    port = select_arduino_port()
    try:
        af.set_arduino(serial.Serial(port=port, baudrate=9600, timeout=.1))
    except:
        print("\nERROR: Could not connect to Arduino")

    print("\nConnecting to Arduino...")
    time.sleep(2)
    print("Successfully connected to Arduino!")
    print('Type "exit" to exit this program.')
    
    while True:
        contents = input("\nAsk Gemini: ")

        if(contents.lower() == "exit"): exit()

        ai_response = get_ai_response(contents)
        clean_response = ai_response.strip()
        lines = clean_response.split("\n")
        last_line = lines[-1]
        message = "\n".join(lines[:-1])

        print("Gemini: ")
        print(message)
        af.send_data(last_line)
            
if(__name__ == "__main__"):
    main()