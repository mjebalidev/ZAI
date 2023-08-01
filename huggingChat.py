import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QHBoxLayout

from langchain import PromptTemplate, HuggingFaceHub, LLMChain
from dotenv import load_dotenv

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
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Tippe deine Nachricht hier ein und drücke Enter zum Senden...")
        self.input_box.setStyleSheet("QLineEdit { border: 1px solid gray; border-radius: 10px; padding: 5px; }")

        self.input_box.returnPressed.connect(self.on_send_button_clicked)

        chat_input_layout = QHBoxLayout()
        chat_input_layout.addWidget(self.input_box)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.chat_history)
        main_layout.addLayout(chat_input_layout)

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
        user_input = self.input_box.text()[:512]  # Begrenze die Eingabe auf 512 Zeichen
        self.input_box.clear()

        # Speichere das aktuelle Dialogfragment
        self.dialogue.append(("Du", user_input))

        # Sende die Benutzereingabe an das LLM-Modell zur Verarbeitung
        self.append_to_chat_history("Du: " + user_input)
        response = self.generate_response(self.dialogue)
        self.append_to_chat_history("Chatbot: " + response)

    def generate_response(self, dialogue):
        # Konkateniere die vorherigen Dialogfragmente zu einem Gespräch
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chat_app = ChatApp()
    chat_app.show()
    sys.exit(app.exec_())
