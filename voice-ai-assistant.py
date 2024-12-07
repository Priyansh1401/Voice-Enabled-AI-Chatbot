import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import subprocess
import datetime
import wikipedia
import wolframalpha
import pyautogui
import requests
import json
import threading
import openai
from plyer import notification


class VoiceAIAssistant:
    def __init__(self):
        # Speech Recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Text-to-Speech
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speaking rate
        
        # OpenAI Configuration (Replace with your API key)
        openai.api_key = 'openai-apikey'

        # WolframAlpha Configuration (Optional advanced calculations)
        self.wolframalpha_app_id = 'wolframealpha-api'

        # Initial setup
        self.wake_word = "hey assistant"
        self.commands = {
            "open website": self.open_website,
            "search wikipedia": self.search_wikipedia,
            "what time is it": self.tell_time,
            "open folder": self.open_folder,
            "calculate": self.calculate_wolfram,
            "take screenshot": self.take_screenshot,
            "send notification": self.send_desktop_notification,
            "chat": self.open_chat_gpt
        }

    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        """Listen for user voice input"""
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            self.speak("Listening...")
            audio = self.recognizer.listen(source)
            print(audio)
            try:
                command = self.recognizer.recognize_google(audio).lower()
                print(command)
                return command
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't catch that.")
                return None
            except sr.RequestError:
                self.speak("Sorry, my speech service is down.")
                return None

    def open_website(self, query):
        """Open websites via voice command"""
        sites = {
            "google": "https://www.google.com",
            "youtube": "https://www.youtube.com",
            "github": "https://www.github.com"
        }
        
        for site, url in sites.items():
            if site in query:
                webbrowser.open(url)
                self.speak(f"Opening {site}")
                return
        
        # If specific URL mentioned
        if "http" in query or "www" in query:
            webbrowser.open(query)
            self.speak("Opening website")

    def search_wikipedia(self, query):
        """Search and read Wikipedia summaries"""
        try:
            # Remove "search wikipedia" from query
            search_term = query.replace("search wikipedia", "").strip()
            results = wikipedia.summary(search_term, sentences=2)
            self.speak(results)
        except wikipedia.exceptions.DisambiguationError as e:
            self.speak(f"Multiple results found. Try being more specific. Options are: {e.options[:3]}")
        except Exception as e:
            self.speak("Sorry, couldn't find information")

    def tell_time(self, query=None):
        """Tell current time"""
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        self.speak(f"Current time is {current_time}")

    def open_folder(self, query):
        """Open local folders"""
        folders = {
            "documents": r"C:\Users\Priyansh Aggarwal\Documents",
            "downloads": r"C:\Users\Priyansh Aggarwal\Downloads",
            "desktop": r"C:\Users\Priyansh Aggarwal\Desktop"
        }
        
        for folder_name, path in folders.items():
            if folder_name in query:
                os.startfile(path)
                self.speak(f"Opening {folder_name} folder")
                return

    def calculate_wolfram(self, query):
        """Advanced calculations using WolframAlpha"""
        try:
            # Remove "calculate" from query
            calculation = query.replace("calculate", "").strip()
            client = wolframalpha.Client(self.wolframalpha_app_id)
            result = client.query(calculation)
            answer = next(result.results).text
            self.speak(f"The result is {answer}")
        except:
            self.speak("Sorry, I couldn't perform the calculation")

    def take_screenshot(self, query=None):
        """Take and save screenshot"""
        screenshot = pyautogui.screenshot()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        screenshot.save(filename)
        self.speak(f"Screenshot saved as {filename}")

    def send_desktop_notification(self, query):
        """Send desktop notifications"""
        notification.notify(
            title='AI Assistant Notification',
            message='Notification from your voice assistant',
            timeout=10
        )
        self.speak("Notification sent")

    def open_chat_gpt(self, query):
        """Interact with OpenAI's GPT model"""
        try:
            # Remove "chat" from query
            user_message = query.replace("chat", "").strip()
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_message}
                ]
            )
            ai_response = response.choices[0].message['content']
            self.speak(ai_response)
        except Exception as e:
            self.speak("Sorry, I couldn't process the chat request")

    def main_loop(self):
        """Main interaction loop"""
        self.speak("Voice AI Assistant activated. Say 'hey assistant' to start.")
        
        while True:
            command = self.listen()
            
            if command and self.wake_word in command:
                self.speak("Yes, how can I help you?")
                
                # Wait for next command
                task = self.listen()
                
                if task:
                    # Try to match command with predefined functions
                    matched = False
                    for key, function in self.commands.items():
                        if key in task:
                            function(task)
                            matched = True
                            break
                    
                    if not matched:
                        self.speak("Sorry, I don't understand that command")

def main():
    assistant = VoiceAIAssistant()
    assistant.main_loop()

if __name__ == "__main__":
    main()
