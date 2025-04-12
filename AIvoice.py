import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pyjokes
import pywhatkit
import tkinter as tk
from tkinter import simpledialog, scrolledtext
import threading
import os
import subprocess
import ctypes
import pyautogui

# Initialize the speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Speak function with lock
speak_lock = threading.Lock()

def speak(text):
    chat_log.insert(tk.END, f"Assistant: {text}\n")
    chat_log.see(tk.END)
    with speak_lock:
        engine.say(text)
        engine.runAndWait()

# Greet the user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")
    speak("I am your assistant. How can I help you today?")

# Take voice input
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language="en-in")
        chat_log.insert(tk.END, f"You (voice): {query}\n")
        chat_log.see(tk.END)
    except Exception:
        speak("Sorry, I didn't catch that.")
        return None
    return query.lower()

# Send WhatsApp message via GUI
def send_whatsapp_gui():
    number = simpledialog.askstring("Phone Number", "Enter number with country code (e.g., +911234567890):")
    message = simpledialog.askstring("Message", "Enter the message:")
    if number and message:
        try:
            speak(f"Sending WhatsApp message to {number}")
            pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10)
        except Exception as e:
            speak("Something went wrong.")
            print(e)
    else:
        speak("Number or message not entered.")

# Process user command
def process_query(query):
    if query is None:
        return

    if "time" in query:
        strTime = datetime.datetime.now().strftime("%H:%M")
        speak(f"The time is {strTime}")

    elif "date" in query:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    elif "wikipedia" in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia:")
            speak(results)
        except:
            speak("Couldn't find anything on Wikipedia.")

    elif "open youtube" in query:
        webbrowser.open("https://youtube.com")

    elif "open google" in query:
        webbrowser.open("https://google.com")

    elif "search" in query:
        query = query.replace("search", "").strip()
        speak(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    elif "youtube search" in query or "play" in query:
        query = query.replace("youtube search", "").replace("play", "").strip()
        speak(f"Searching YouTube for {query}")
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")

    elif "joke" in query:
        joke = pyjokes.get_joke()
        speak(joke)

    elif "how are you" in query:
        speak("I'm great! Ready to help you.")

    elif "who are you" in query:
        speak("I am your personal assistant, created with Python.")

    elif "version control" in query:
        speak("My version control is managed by you.")

    elif "send whatsapp message" in query:
        send_whatsapp_gui()

    elif "open file explorer" in query:
        speak("Opening File Explorer")
        subprocess.Popen("explorer")

    elif "open notepad" in query:
        speak("Opening Notepad")
        subprocess.Popen("notepad.exe")

    elif "open calculator" in query:
        speak("Opening Calculator")
        subprocess.Popen("calc.exe")

    elif "lock the pc" in query or "lock computer" in query:
        speak("Locking the computer")
        ctypes.windll.user32.LockWorkStation()

    elif "shut down" in query or "shutdown" in query:
        speak("Shutting down the computer")
        os.system("shutdown /s /t 1")

    elif "restart" in query:
        speak("Restarting the computer")
        os.system("shutdown /r /t 1")

    elif "sleep" in query:
        speak("Putting the computer to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "take screenshot" in query:
        speak("Taking screenshot")
        screenshot = pyautogui.screenshot()
        path = "screenshot.png"
        screenshot.save(path)
        speak(f"Screenshot saved as {path}")

    elif "mute" in query:
        speak("Muting volume")
        pyautogui.press("volumemute")

    elif "unmute" in query:
        speak("Unmuting volume")
        pyautogui.press("volumemute")

    elif "help" in query:
        speak("Here are some things you can ask me: search Google, play music on YouTube, open Notepad, lock PC, take screenshot, or tell a joke.")

    elif "stop" in query or "exit" in query or "bye" in query:
        speak("Goodbye! Have a great day.")
        app.destroy()

    else:
        speak("Sorry, I didn't understand that.")

# Voice command in background thread
def handle_voice_command():
    threading.Thread(target=lambda: process_query(take_command()), daemon=True).start()

# Text command handler
def handle_text_command():
    query = text_entry.get()
    if query:
        chat_log.insert(tk.END, f"You (typed): {query}\n")
        chat_log.see(tk.END)
        text_entry.delete(0, tk.END)
        process_query(query.lower())

# --- GUI Setup ---
app = tk.Tk()
app.title("My Personal AI Voice Assistant")
app.geometry("550x600")
app.configure(bg="#e6f2ff")

# Title Label
title_label = tk.Label(app, text="🤖 AI Voice Assistant", font=("Helvetica", 18, "bold"), bg="#e6f2ff", fg="#003366")
title_label.pack(pady=10)

# Chat log
chat_log = scrolledtext.ScrolledText(app, wrap=tk.WORD, font=("Arial", 12), height=20, width=65, bg="white", bd=2, relief=tk.GROOVE)
chat_log.pack(padx=10, pady=10)

# Input frame
frame = tk.Frame(app, bg="#e6f2ff")
frame.pack(pady=10)

text_entry = tk.Entry(frame, font=("Arial", 14), width=30, bd=2, relief=tk.GROOVE)
text_entry.grid(row=0, column=0, padx=5)

send_btn = tk.Button(frame, text="Send", command=handle_text_command, font=("Arial", 12, "bold"), bg="#3399ff", fg="white", width=8)
send_btn.grid(row=0, column=1, padx=5)

voice_btn = tk.Button(frame, text="Speak", command=handle_voice_command, font=("Arial", 12, "bold"), bg="#33cc33", fg="white", width=8)
voice_btn.grid(row=0, column=2, padx=5)

# Action Buttons Frame
action_frame = tk.Frame(app, bg="#e6f2ff")
action_frame.pack(pady=10)

whatsapp_btn = tk.Button(action_frame, text=" WhatsApp", command=send_whatsapp_gui, font=("Arial", 12, "bold"), bg="#25D366", fg="white", width=15)
whatsapp_btn.grid(row=0, column=0, padx=10)

exit_btn = tk.Button(action_frame, text=" Exit", command=app.destroy, font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white", width=15)
exit_btn.grid(row=0, column=1, padx=10)

# Start assistant
greet()
app.mainloop()
