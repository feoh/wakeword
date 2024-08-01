import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Keyword to activate the assistant
WAKE_WORD = "assistant"

def listen_for_command():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service.")
        return ""

def get_headlines():
    url = "https://news.google.com/news/rss"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features="xml")
    headlines = soup.findAll('title')[1:6]  # Get top 5 headlines
    return [headline.text for headline in headlines]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def main():
    print(f"Say '{WAKE_WORD}' to activate the assistant.")
    
    while True:
        command = listen_for_command()
        
        if WAKE_WORD in command:
            speak("How can I help you?")
            command = listen_for_command()
            
            if "headlines" in command:
                speak("Here are the top news headlines:")
                headlines = get_headlines()
                for headline in headlines:
                    speak(headline)
            elif "exit" in command or "quit" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I don't understand that command.")

if __name__ == "__main__":
    main()
