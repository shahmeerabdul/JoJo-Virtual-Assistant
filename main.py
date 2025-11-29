import speech_recognition as sr
import pyttsx3
import webbrowser
import time
import musicLibrary
import google.generativeai as genai

# gemini
genai.configure(api_key="YOUR-API-KEY")  # Replace with your Gemini API key
model = genai.GenerativeModel("gemini-1.5-flash")


def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


#query
def ask_gemini(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error with Gemini API: {e}"

# command
def processCommand(command):
    command = command.lower()

    if "open google" in command:
        webbrowser.open("https://google.com")
    elif "open facebook" in command:
        webbrowser.open("https://facebook.com")
    elif "open linkedin" in command:
        webbrowser.open("https://linkedin.com")
    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
    elif command.startswith("play"):
        song = command.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak("Song not found.")
    else:
        # If command doesn't match predefined ones, ask Gemini
        speak("Let me think...")
        answer = ask_gemini(command)
        # print("JoJo:", answer)
        speak(answer)

def main():
    speak("Initializing JoJo...")
    recognizer = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)
                print(f"Heard: {word}")

            if word.lower() == "jojo":
                print("Jojo detected.")
                time.sleep(0.1)  # Small delay
                speak("Ya")

                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = recognizer.listen(source, timeout=5)
                    command = recognizer.recognize_google(audio)
                    print(f"Command: {command}")
                    processCommand(command)

        except sr.WaitTimeoutError:
            print("Timeout - no input.")
        except sr.UnknownValueError:
            print("Could not understand.")
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
        except Exception as e:
            print(f"General error: {e}")

if __name__ == "__main__":
    main()
