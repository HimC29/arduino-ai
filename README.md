# Arduino AI-Gemini

[![Arduino-AI](https://img.shields.io/badge/Arduino-AI-blue)](https://github.com/HimC29/arduino-ai)

Arduino AI-Gemini is a Python-based bridge that connects the Gemini 3 Flash to physical hardware. It allows you to control an Arduino using natural language, translating your typed intent into precise serial commands automatically.

Check it out on GitHub: [Arduino AI Repository](https://github.com/HimC29/arduino-ai)

> ⚠️ **Early Release / In Development** 
> This project is currently in the prototype stage. Many features may not be here yet.

---

## Features

- **Natural Language Parsing** – Ask Gemini to toggle pins or set states without writing code.
- **Machine-Readable Protocol** – Automatically converts AI conversational text into compact [pin][state] codes.
- **Dynamic Port Selection** – Automatically lists and connects to available Serial/COM ports.
- **Token-Optimized** – Uses specialized system instructions to minimize API costs and latency.
- **Error Handling** – Built-in logic to handle API timeouts and malformed serial data.

---

## How to Use

Follow these steps to get started:

- Upload a the sketch [provided](arduino/main/main.ino) at to your Arduino.
- Install dependencies: `pip install pyserial google-genai python-dotenv`.
- Add your own .env file in [here](python/) with a variable called API_KEY that contains your Gemini API key.
- Select your Arduino's port and start typing commands like "Set pin 2 to high."

You will need a valid Google Gemini API key to use the natural language features.

---

## Contributing

Want to make Arduino AI-Gemini better? Contributions are welcome!

- Make the TUI look and feel better.
- And more

---

## Future Plans

- Support for Analog PWM (e.g., "Set pin 3 brightness to 50%").
- Sensor Feedback loops (AI interprets temperature/distance data).

---

## License

MIT License – feel free to use and modify this project.

---

## Credits / Third-Party Assets

- Powered by **Google Gemini 3 Flash**