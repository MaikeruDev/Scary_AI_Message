# Windows Event Log Analyzer - Spooky Edition

## Description
This Python project is a Windows Event Log Analyzer that fetches and analyzes recent event logs from the "Application" log type. The project also incorporates OpenAI's GPT-3.5 language model to generate spooky messages based on user prompts and system activity. To add to the eerie atmosphere, the project utilizes the pyttsx3 library to convert the text into a creepy voice.

## Features
- Fetch and analyze recent event logs from the "Application" log type on a Windows system.
- Generate scary messages using OpenAI's GPT-3.5 language model, providing a haunting experience.
- Convert the generated spooky message into an eerie voice using the pyttsx3 text-to-speech engine.
- Write the spooky message to a file named "youre_hacked.txt" on the user's desktop.

## Dependencies
- `win32evtlog`: A library for accessing the Windows Event Log.
- `requests`: A library for making HTTP requests to interact with the OpenAI GPT-3 API.
- `openai`: Python library for interfacing with OpenAI's GPT-3.5 language model.
- `pyttsx3`: Text-to-speech (TTS) engine for creating creepy voice output.
- `os`: Provides a way of interacting with the operating system.
- `time`: For introducing a delay to simulate spooky effects.

## Usage
1. Ensure that the required dependencies are installed.
2. Run the Python script to fetch event logs, generate a scary message, write the message to the file "youre_hacked.txt" on the user's desktop, and play the spooky message using TTS.
3. The generated message will be based on the user's provided prompts and the system's recent activity.

## Important
- Do not forget to insert your API Key
- The project requires an OpenAI API key to access the GPT-3.5 language model. Make sure to obtain the correct API key for seamless execution. 
- Please use the spooky features of the script responsibly and only for appropriate and non-harmful purposes.

*For more details and code snippets, please refer to the provided Python script. Happy spooky coding! 🎃👻*
