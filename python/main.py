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
instructions = ("Arduino Controller. " 
                "Protocol: 'o'[pin][h/l] for output, 'i'[pin] for input. "
                "Format: [1 sentence confirmation]\n[code] [code]... "
                "Constraints: Codes must be on the last line. Space-separated. No trailing text. "
                "Example: Toggling pin 2 and reading pin 3. o2h i3"
)

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
        if(contents == "developer"): 
            print("\nDeveloper mode - control with raw serial cmds")
            print('Type "exit" to exit developer mode.')
            while True:
                raw_input = input("\nSerial: ")
                
                if(raw_input.lower() == "exit"): break

                cmds_array = raw_input.split(" ")

                for cmd in cmds_array:
                    if not cmd: continue

                    type = cmd[0].lower()
                    if(type == "o"):
                        af.send_data(cmd.lower() + "\n")
                    elif(type == "i"):
                        print(af.send_and_read(cmd.lower() + "\n"))
                    
                    time.sleep(0.05)
            continue

        ai_response = get_ai_response(contents)
        clean_response = ai_response.strip()

        lines = clean_response.split("\n")
        
        cmds_array = lines[-1].split(" ")

        message = "\n".join(lines[:-1])

        print(f"Gemini: {message}")

        for cmd in cmds_array:
            type = list(cmd)[0]
            if(type == "o"):
                af.send_data(cmd.lower() + "\n")
            elif(type == "i"):
                print(af.send_and_read(cmd.lower() + "\n"))
            time.sleep(0.05)
            
if(__name__ == "__main__"):
    main()