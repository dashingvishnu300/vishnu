import tkinter as tk
import os
import speech_recognition as sr
import pyttsx3

# Function to open applications based on the command
def open_application(app_name):
    try:
        if app_name.lower() == "notepad":
            os.system("notepad.exe")
        elif app_name.lower() == "chrome":
            os.system("start chrome")
        elif app_name.lower() == "word":
            os.system("start winword")
        elif app_name.lower() == "spotify":
            os.system("start spotify")
        elif app_name.lower() == "calculator":
            os.system("calc")
        elif app_name.lower() == "vscode":
            os.system("code")
        elif app_name.lower() == "brave":
            os.system(r'"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"')
        else:
            update_response("Sorry, I can't open",app_name)
            speak(f"Sorry, I can't open {app_name}.")
    except Exception as e:
        update_response(f"Error: {e}", "error")
        speak(f"Error: {e}")

# Function to handle text-to-speech feedback
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed of speech
    engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)
    engine.say(text)
    engine.runAndWait()

# Function to listen for a voice command
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_response("Listening for command...", "info")
        speak("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        try:
            audio = recognizer.listen(source, timeout=5)  # Listen with a timeout
            command = recognizer.recognize_google(audio)  # Convert speech to text
            print(f"Command received: {command}")
            if "open" in command.lower():
                app_name = command.split("open")[-1].strip()  # Extract the app name
                open_application(app_name)  # Open the app
                update_response(f"Opening {app_name}...", "success")
                speak(f"Opening {app_name}...")
            else:
                update_response("I can only open apps based on voice commands.", "error")
                speak("I can only open apps based on voice commands.")
        except sr.UnknownValueError:
            update_response("Sorry, I couldn't understand your speech.", "error")
            speak("Sorry, I couldn't understand your speech.")
        except sr.RequestError as e:
            update_response(f"Google Speech Recognition service error: {e}", "error")
            speak(f"Google Speech Recognition service error: {e}")
        except Exception as e:
            update_response(f"Error: {e}", "error")
            speak(f"Error: {e}")

# Function to update the response label with styles
def update_response(message, status):
    if status == "success":
        response_label.config(text=message, fg="green")
    elif status == "error":
        response_label.config(text=message, fg="red")
    elif status == "info":
        response_label.config(text=message, fg="blue")
    else:
        response_label.config(text=message, fg="black")

# Create the main window for the GUI
root = tk.Tk()
root.title("Interactive Desktop App Chatbot")
root.geometry("500x600")  # Set the window size
root.resizable(False, False)  # Disable resizing

# Add a title label
title_label = tk.Label(root, text="Interactive Desktop App Chatbot", font=("Arial", 16, "bold"), pady=10)
title_label.pack()

# Add a label to display chatbot feedback
response_label = tk.Label(root, text="How can I help you?", font=("Arial", 12), width=50, height=2, fg="black")
response_label.pack(pady=10)

# Function to create the app buttons dynamically
def create_app_buttons():
    apps = [
        ("Notepad", "notepad"),
        ("Chrome", "chrome"),
        ("Microsoft Word", "word"),
        ("Spotify", "spotify"),
        ("Calculator", "calculator"),
        ("VS Code", "vscode"),
        ("Brave","brave")
    ]

    for app_name, command in apps:
        button = tk.Button(root, text=f"Open {app_name}", width=20, height=2, font=("Arial", 10),
                           bg="#4CAF50", fg="white", activebackground="#45a049",
                           command=lambda app=command: open_application(app))
        button.pack(pady=5)

# Add voice command button
voice_button = tk.Button(root, text=" Listen for Command", width=20, height=2, font=("Arial", 10, "bold"),
                         bg="#008CBA", fg="white", activebackground="#007bb5",
                         command=listen_for_command)
voice_button.pack(pady=20)

# Call the function to create app buttons
create_app_buttons()


# Run the GUI event loop
root.mainloop()
