import queue
import sounddevice as sd
import json
import subprocess
import datetime
import os
import tempfile
import sys
import webbrowser
from difflib import SequenceMatcher
from vosk import Model, KaldiRecognizer

# ==============================
# GLOBAL STATE
# ==============================
speaking = False   # True when bot is talking

# ==============================
# CONFIG
# ==============================
ESPEAK_PATH = "/usr/bin/espeak-ng"
MODEL_PATH = "hindi_model"
SAMPLE_RATE = 16000

FUZZY_THRESHOLD = 0.85
OPEN_WORDS = ["खोलो", "ओपन", "open", "start"]

# ==============================
# LOAD MODEL
# ==============================
print("Loading Hindi model...")
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
print("Model loaded.")

# ==============================
# AUDIO QUEUE
# ==============================
q = queue.Queue()


def callback(indata, frames, time, status):
    global speaking

    if status:
        print(status, file=sys.stderr)

    # Ignore mic input while speaking
    if speaking:
        return

    q.put(bytes(indata))


# ==============================
# BLOCKING TEXT TO SPEECH
# ==============================
def speak(text):
    global speaking

    if not text:
        return

    speaking = True

    print("Bot:", text)

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".txt",
        mode="w",
        encoding="utf-8"
    ) as f:
        f.write(text)
        filename = f.name

    try:
        # Blocking speak (wait until finished)
        subprocess.run([
            ESPEAK_PATH,
            "-v", "hi",
            "-s", "120",
            "-a", "200",
            "-f", filename
        ])
    finally:
        if os.path.exists(filename):
            os.remove(filename)

        speaking = False   # Allow listening again


# ==============================
# FUZZY MATCHING
# ==============================
def fuzzy_match(text, keyword):

    if keyword in text:
        return True

    words = text.split()
    kw_words = keyword.split()
    kw_len = len(kw_words)

    for i in range(len(words) - kw_len + 1):

        window = " ".join(words[i:i + kw_len])

        ratio = SequenceMatcher(None, window, keyword).ratio()

        if ratio >= FUZZY_THRESHOLD:
            return True

    return False


def match_any(text, keywords):
    return any(fuzzy_match(text, kw) for kw in keywords)


# ==============================
# WEBSITE / APP DATA
# ==============================
WEBSITES = {
    ("यूट्यूब", "youtube"): "https://www.youtube.com",
    ("गूगल", "google"): "https://www.google.com",
    ("व्हाट्सएप", "whatsapp"): "https://web.whatsapp.com",
    ("फेसबुक", "facebook"): "https://www.facebook.com",
    ("ट्विटर", "twitter"): "https://www.twitter.com",
    ("जीमेल", "gmail"): "https://mail.google.com",
    ("मौसम", "weather"): "https://weather.com",
    ("न्यूज़", "news"): "https://news.google.com",
    ("wikipedia", "विकिपीडिया"): "https://hi.wikipedia.org",
}

APPS = {
    ("नोटपैड", "notepad"): "notepad",
    ("कैलकुलेटर", "calculator", "calc"): "calc",
}


# ==============================
# OPEN FUNCTIONS
# ==============================
def try_open_website(text):

    if not match_any(text, OPEN_WORDS):
        return None

    for keywords, url in WEBSITES.items():

        if match_any(text, list(keywords)):
            webbrowser.open(url)
            return f"{keywords[0]} खोल दिया गया है।"

    return None


def try_open_app(text):

    if not match_any(text, OPEN_WORDS):
        return None

    for keywords, app_cmd in APPS.items():

        if match_any(text, list(keywords)):

            try:
                os.system(f"start {app_cmd}")
                return f"{keywords[0]} खोल दिया गया है।"

            except Exception:
                return "ऐप नहीं खुल सका।"

    return None


# ==============================
# CHATBOT RESPONSES
# ==============================
RESPONSES = [

    (["नमस्ते", "हेलो", "हाय"],
     "नमस्ते! मैं आपकी मदद के लिए तैयार हूँ।"),

    (["कैसे हो", "क्या हाल"],
     "मैं बिल्कुल ठीक हूँ।"),

    (["नाम क्या है", "आपका नाम"],
     "मेरा नाम ऑफलाइन सहायक है।"),

    (["समय", "टाइम"],
     lambda: "अभी समय है " +
     datetime.datetime.now().strftime("%H:%M")),

    (["तारीख", "तारिक", "दिनांक"],
     lambda: "आज की तारीख है " +
     datetime.datetime.now().strftime("%d %B %Y")),

    (["धन्यवाद", "thanks"],
     "आपका स्वागत है।"),

    (["बाय", "अलविदा", "bye"],
     "__EXIT__"),
]


# ==============================
# CHATBOT LOGIC
# ==============================
def chatbot_response(text):

    text = text.lower().strip()

    web = try_open_website(text)
    if web:
        return web

    app = try_open_app(text)
    if app:
        return app

    for keywords, response in RESPONSES:

        if match_any(text, keywords):

            if callable(response):
                return response()

            return response

    return None


# ==============================
# MAIN LOOP
# ==============================

print("\n🎤 Voice Assistant Started\n")

# Welcome
speak("नमस्ते! मैं तैयार हूँ। आप बोल सकते हैं।")


with sd.RawInputStream(
    samplerate=SAMPLE_RATE,
    blocksize=4096,
    dtype="int16",
    channels=1,
    latency="high",
    callback=callback
):

    try:

        while True:

            # Wait for voice
            data = q.get()

            if recognizer.AcceptWaveform(data):

                result = json.loads(recognizer.Result())
                text = result.get("text", "")

                if len(text.strip()) >= 3:

                    print("You:", text)

                    reply = chatbot_response(text)

                    if reply == "__EXIT__":

                        speak("अलविदा! फिर मिलेंगे।")
                        break

                    elif reply:

                        speak(reply)

    except KeyboardInterrupt:

        print("\nAssistant stopped.")