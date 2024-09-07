import os
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import google.generativeai as genai
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3

load_dotenv()

API_KEY = os.getenv('GEMINI_API_KEY')

if not API_KEY:
    raise ValueError("API key not found. Please set the GEMINI_API_KEY environment variable.")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Define the function to handle the chatbot response
def get_response(user_input=None):
    if user_input is None:
        user_input = entry.get()
    if user_input.strip().lower() == 'exit':
        window.quit()
        return
    try:
        response = chat.send_message(user_input)
        chat_window.configure(state='normal')
        chat_window.insert(tk.END, "You: " + user_input + "\n")
        chat_window.insert(tk.END, "Bot: " + response.text + "\n\n")
        chat_window.configure(state='disabled')
        chat_window.see(tk.END)
        entry.delete(0, tk.END)
        
        # Speak the response
        engine.say(response.text)
        engine.runAndWait()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Define the function to handle voice input
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            user_input = recognizer.recognize_google(audio)
            print("You said:", user_input)
            get_response(user_input)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Could not understand audio")
        except sr.RequestError as e:
            messagebox.showerror("Error", f"Could not request results; {e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Create the main window
window = tk.Tk()
window.title("Chatbot")

# Create a scrolled text widget for the chat history
chat_window = scrolledtext.ScrolledText(window, wrap=tk.WORD, state='disabled')
chat_window.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create an entry widget for user input
entry = tk.Entry(window, width=100)
entry.pack(padx=10, pady=(0, 10), fill=tk.X, expand=True)
entry.bind("<Return>", lambda event: get_response())

# Create a button to send the message
send_button = tk.Button(window, text="Send", command=get_response)
send_button.pack(padx=10, pady=(0, 10))

# Create a button to use voice input
voice_button = tk.Button(window, text="Speak", command=get_voice_input)
voice_button.pack(padx=10, pady=(0, 10))

# Run the main loop
window.mainloop()
