import speech_recognition as sr
import keyboard
import TTS
import Spotify_API
import time
import os

recognizer = sr.Recognizer()

def listen():
    text_info = ['empty']
    with sr.Microphone() as source:
        print("Listening...")
        
        while keyboard.is_pressed('F13'):  # Listen while F12 is held down
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)  # Adjust the timeout and phrase_time_limit as needed
                print('Processing Audio')
                text = recognizer.recognize_google(audio)
                print("You said:", text)
                text_info = text.split(' ', 2)
            except sr.WaitTimeoutError:
                # Timeout if nothing was said
                continue
            except sr.UnknownValueError:
                TTS.read_text("I didn't understand you")
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                TTS.read_text("ERROR ERROR ERROR")
                print(f"Could not request results; {e}")
            time.sleep(0.1)  # Small delay to prevent high CPU usage

    print('Stopped listening')
    if text_info[0].lower() == 'spotify':
        if len(text_info)<3:
                print('Incomplete command')
                TTS.read_text('Something is missing')
        else:
            Spotify_API.use_command(text_info[1], text_info[2])
    if text_info[0].lower() == 'windows':
        # if text_info[1].lower() in ['shutdown','shut down']:
            os.system('shutdown -s -t 3')
            TTS.read_text('Shutting down')
         
        

print('Started the Programm')
while True:
    if keyboard.is_pressed('F13'):
        listen()
