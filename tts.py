from gtts import gTTS
from langdetect import detect
import os
from pydub import AudioSegment
import uuid

def detect_language(text):
    lang = detect(text)
    return 'hi' if 'hi' in lang else 'en'

def text_to_speech(text):
    lang = detect_language(text)
    tts = gTTS(text, lang=lang)
    filename = f"{uuid.uuid4()}.mp3"
    tts.save(filename)
    # Convert to OGG for Telegram
    sound = AudioSegment.from_mp3(filename)
    ogg_file = filename.replace(".mp3", ".ogg")
    sound.export(ogg_file, format="ogg")
    os.remove(filename)
    return ogg_file
