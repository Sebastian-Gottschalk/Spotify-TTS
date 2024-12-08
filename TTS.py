from gtts import gTTS
import os
from playsound import playsound
import time

def read_text(text):
    textobj = gTTS(text = text, lang = "en", slow = False)
    textobj.save("temp.mp3")
    time.sleep(0.2)
    playsound("temp.mp3")
    time.sleep(0.1)
    os.remove("temp.mp3")