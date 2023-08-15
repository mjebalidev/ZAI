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

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout
import speech_recognition
from gtts import gTTS #Google Text To Speech
from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv
import audiofile as af

# Lade die Umgebungsvariablen.
load_dotenv()

class ChatApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()  # Initialisiere die Benutzeroberfläche (UI)
        self.init_llm()  # Initialisiere das Language Model (LLM)
        self.dialogue = []  # Liste für den gesamten Dialog

    def init_ui(self):
        # Setze Fenster-Eigenschaften
        self.setWindowTitle("Chatbot")
        self.setFixedSize(800, 500)  # Setze die feste Größe des Fensters

        # Setze Eigenschaften des Chatfensters
        self.chat_history = QTextEdit(self)
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet("QTextEdit { border: 1px solid gray; border-radius: 10px; padding: 10px; }")

        # Setze Eigenschaften der Eingabebox
        #self.input_box = QLineEdit(self)
        #self.input_box.setPlaceholderText("Tippe deine Nachricht hier ein und drücke Enter zum Senden...")
        #self.input_box.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 10px; padding: 5px; }")
        #self.input_box.returnPressed.connect(self.on_send_button_clicked)

        # Set set button with hold
        self.send_button = QPushButton("Start listening", self)
        self.send_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 10px; padding: 5px; }")
        self.send_button.clicked.connect(self.on_send_button_clicked)

        # Set stop button
        self.stop_button = QPushButton("Stop listening", self)
        self.stop_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 10px; padding: 5px; }")
        self.stop_button.clicked.connect(self.on_stop_button_clicked)

        # Set exit button
        self.exit_button = QPushButton("Exit", self)
        self.exit_button.setStyleSheet("QPushButton { border: 1px solid gray; border-radius: 10px; padding: 5px; }")
        self.exit_button.clicked.connect(self.exit)

        #chat_input_layout = QHBoxLayout()
        #chat_input_layout.addWidget(self.input_box)

        send_button_layout = QVBoxLayout()
        send_button_layout.addWidget(self.send_button)

        stop_button_layout = QVBoxLayout()
        stop_button_layout.addWidget(self.stop_button)

        exit_button_layout = QVBoxLayout()
        exit_button_layout.addWidget(self.exit_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.chat_history)
        #main_layout.addLayout(chat_input_layout)
        main_layout.addLayout(send_button_layout)
        main_layout.addLayout(stop_button_layout)
        main_layout.addLayout(exit_button_layout)
        self.setLayout(main_layout)

    def init_llm(self):
        template = """<|prompter|>{question}<|endoftext|><|assistant|>
        """
        prompt = PromptTemplate(template=template, input_variables=["question"])

        # Initialisiere das Language Model (LLM) von Hugging Face
        llm = HuggingFaceHub(repo_id="OpenAssistant/oasst-sft-4-pythia-12b-epoch-3.5", model_kwargs={"max_new_tokens": 1200})

        # Initialisiere die LLM-Kette (LLMChain) mit dem vorher erstellten LLM und dem vorgegebenen Prompt
        self.llm_chain = LLMChain(
            llm=llm,
            prompt=prompt
        )

    def on_send_button_clicked(self):
        # Old chat implementation
        #user_input = self.input_box.text()[:512]  # Begrenze die Eingabe auf 512 Zeichen
        #self.input_box.clear()
        # Speichere das aktuelle Dialogfragment
        #self.dialogue.append(("Du", user_input))
        # Sende die Benutzereingabe an das LLM-Modell zur Verarbeitung
        #self.append_to_chat_history("Du: " + user_input)
        #response = self.generate_response(self.dialogue)
        #self.append_to_chat_history("Chatbot: " + response)
        
        # Audio implementation
        query = self.user_speech()
        self.dialogue.append(("Du", query))
        self.append_to_chat_history("Du: " + query)
        response = self.generate_response(self.dialogue)
        self.append_to_chat_history("Chatbot: " + response)
        self.speak(response)
        
    def on_stop_button_clicked(self):
        self.append_to_chat_history("Aufnahme gestoppt")

    def exit(self):
        self.close()

    def generate_response(self, dialogue):
        # Aneinanderhängen von vorherigen Dialogfragmente zu einem Gespräch
        conversation = " ".join(f"{sender}: {message}" for sender, message in dialogue)

        # Führe die LLM-Kette aus, um die Antwort des Chatbots zu generieren
        response = self.llm_chain.run(conversation)

        # Extrahiere die letzte Benutzereingabe aus dem Dialog und speichere sie in der Variablen "last_user_input"
        last_user_input = dialogue[-1][1] if dialogue else ""

        # Füge das letzte Benutzerfragment und die Antwort des Modells zum Dialog hinzu
        dialogue.append(("Chatbot", response))
        dialogue.append(("Du", last_user_input))

        return response

    def append_to_chat_history(self, message):
        self.chat_history.append(message)
    
    # Speech to text
    def user_speech(self):
        recognizer = speech_recognition.Recognizer()
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            text = recognizer.recognize_google(audio, language="en-US")
            text_lower = text.lower()
            print(f"Recognized {text_lower}")
        return text_lower
    
    # Translate text to sound with gTTS (Google Text To Speech) and play it with ffplay
    # This is the best sounding solution for now
    def speak(self, text):
        sound = gTTS(text, lang='en')
        sound.save("voice.mp3")
        os.system("ffplay -autoexit -loglevel quiet voice.mp3")
        #af.read("voice.mp3")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
