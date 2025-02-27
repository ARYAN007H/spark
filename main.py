from os import system
import speech_recognition as sr
import whisper
import numpy as np
import sys
import ffmpeg
import os
import warnings
import time
import openai

def load_audio(audio):
    """
    Load audio using ffmpeg and convert it to a normalized numpy array.
    """
    try:
        out, _ = (
            ffmpeg.input(audio, threads=0)
            .output("-", format="s16le", acodec="pcm_s16le", ac=1, ar=16000)
            .run(capture_stdout=True, capture_stderr=True)
        )
    except Exception as e:
        print("Error in load_audio:", e)
        return None
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

# Wake word variable for GPT only
GPT_WAKE_WORD = "gpt"

# Initialize the OpenAI API (be sure to secure your API key)
openai.api_key = ["Enter your OpenAI API key here"]

r = sr.Recognizer()
tiny_model = whisper.load_model('tiny')
base_model = whisper.load_model('base')
listening_for_wake_word = True
source = sr.Microphone() 
warnings.filterwarnings("ignore", category=UserWarning, module='whisper.transcribe', lineno=114)

if sys.platform != 'darwin':
    import pyttsx3
    engine = pyttsx3.init()

def speak(text):
    if sys.platform == 'darwin':
        ALLOWED_CHARS = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?!-_$:+-/ ")
        clean_text = ''.join(c for c in text if c in ALLOWED_CHARS)
        system(f"say '{clean_text}'")
    else:
        engine.say(text)
        engine.runAndWait()

def listen_for_wake_word(audio):
    global listening_for_wake_word
    # Save the audio data to a file for processing
    with open("wake_detect.wav", "wb") as f:
        f.write(audio.get_wav_data())
    try:
        result = tiny_model.transcribe('wake_detect.wav')
        text_input = result['text'].lower()
    except Exception as e:
        print(f"Error during transcription: {e}")
        listening_for_wake_word = True
        return
    if GPT_WAKE_WORD in text_input:
        print("Speak your prompt to GPT 3.5 Turbo.")
        speak("Listening")
        listening_for_wake_word = False
    else:
        print("Wake word not detected. Please say 'gpt' to activate.")

def prompt_gpt(audio):
    global listening_for_wake_word
    try:
        with open("prompt.wav", "wb") as f:
            f.write(audio.get_wav_data())
        result = base_model.transcribe('prompt.wav')
        prompt_text = result['text']
        if not prompt_text.strip():
            print("Empty prompt. Please speak again.")
            speak("Empty prompt. Please speak again.")
            listening_for_wake_word = True
        else:
            print("User: " + prompt_text)
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt_text},
                ],
                temperature=0.5,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                n=1,
                stop=["\nUser:"],
            )
            bot_response = response["choices"][0]["message"]["content"]
            print("GPT: " + bot_response)
            speak(bot_response)
            print('\nSay "gpt" to wake me up.\n')
            listening_for_wake_word = True
    except Exception as e:
        print("Prompt error: ", e)
        listening_for_wake_word = True

def callback(recognizer, audio):
    global listening_for_wake_word
    if listening_for_wake_word:
        listen_for_wake_word(audio)
    else:
        prompt_gpt(audio)

def start_listening():
    with source as s:
        r.adjust_for_ambient_noise(s, duration=2)
    print('\nSay "gpt" to wake me up.\n')
    r.listen_in_background(source, callback)
    while True:
        time.sleep(1) 

if __name__ == '__main__':
    start_listening()
