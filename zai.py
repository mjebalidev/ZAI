#!/bin/python3

#   ZAI is ZAI ARTIFICIAL INTELLIGENCE v1.0
#   ZAI is a chatbot that uses the OpenAI API to generate responses to user input.
#   The aim is to implement it on a Raspberry Pi 3B+.
#
#   made by Waldemar Friensen & Mehdi Jebali
#   Koblenz University of Applied Sciences
#
#   This program is free software: you can redistribute it and/or modify
#   under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


########################################
############## IMPORTS #################

from gtts import gTTS #Google Text To Speech
import os
import speech_recognition #Speech to text
import openai #ChatGPT
import pyttsx3
import pyaudio

########################################
############## VARIABLES ###############

# Set the OpenAI API key
openai.api_key = "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"

# Use the chat GPT model to generate a response
model_engine = "text-davinci-002"

# Set the user query to an empty string
query = ""

########################################
############## FUNCTIONS ###############

# Speech to text
def user_speech():
	recognizer = speech_recognition.Recognizer()
	with speech_recognition.Microphone() as mic:

		recognizer.adjust_for_ambient_noise(mic, duration=0.2)
		audio = recognizer.listen(mic)

		text = recognizer.recognize_google(audio)
		text_lower = text.lower()
	return text_lower

# Translate text to sound with gTTS (Google Text To Speech) and play it with ffplay
# This is the best sounding solution for now
def speak(text):
    sound = gTTS(text, lang='en')
    sound.save("voiceOfZAI.mp3")
    os.system("ffplay -autoexit -loglevel quiet voiceOfZAI.mp3")

# Translate text to sound with pyttsx3 and play it with pyaudio
# This is the faster solution, but sounds bad
def speak_py(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Set the voice to a female voice (index 1)
    engine.setProperty('voice', voices[1].id)

    engine.say(text)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=2250, output=True)
    engine.runAndWait()
    stream.stop_stream()
    stream.close()
    p.terminate()

# Send text to ChatGPT
def send_text(text):
    prompt = (f"User: {text}\nChatGPT:")
    completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.5)
    response = completions.choices[0].text
    response = response.replace(prompt, "").strip()
    return response

# Ask function
def ask(text):
    #text = input("Enter your text: ")
    response = send_text(text)
    return response

#######################################
############## MAIN ###################
def main():
    while True:
        try:
            query = user_speech()
            print(f"Your voice: {query}")
            speak(ask(query))
            #time.sleep(1)
		#interactions(input())
        except Exception as e:
            print(e)
            continue

if __name__ == "__main__":
    main()
