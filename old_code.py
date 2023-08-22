#!/usr/bin/python3
#ZAI is ZAI ARTIFICIAL INTELLIGENCE v0.2
#Diese Version stammt aus der Zeit vor der Vermarktung von OpenAI's GPT-3

########################################
############## IMPORTS #################
from gtts import gTTS
import wikipedia
import random
import os
import datetime
import wolframalpha
import speech_recognition
import pyttsx3


########################################
############## FUNCTIONS ###############

#Speech to text function:
def user_speech():
	recognizer = speech_recognition.Recognizer()
	with speech_recognition.Microphone() as mic:

		recognizer.adjust_for_ambient_noise(mic, duration=0.2)
		audio = recognizer.listen(mic)

		text = recognizer.recognize_google(audio)
		text_lower = text.lower()
	return text_lower

# SPEAK(); traduit le texte en son
def speak(text):
	sound = gTTS(text, lang='en')
	sound.save("voiceOfZAI.mp3")
	os.system("ffplay -autoexit -loglevel quiet voiceOfZAI.mp3")

def human():
	humanAnswer = "No, I am a set of pre-constructed mathematical and logical fuctions."
	speak(humanAnswer)
	print(humanAnswer)

def firstPresentation():
	iAm = "Nice to meet you, my name is ZAI. I am a programm made in 2021, I can perform tasks and researches for you."
	speak(iAm)
	print(iAm)

# PRESENTATION(); ZAI presents itself to the user
def presentation():
	presentation1 = "Hello, my name is ZAI"
	presentation2 = "I'm ZAI"
	presentation3 = "ZAI for you Sir"
	presentation4 = "Hello Master"
	allPresentations = [presentation1,presentation2,presentation3,presentation4]
	speak(random.choice(allPresentations))
	print(random.choice(allPresentations))

#ASK() Demande si je veux savoir quelquechose, renvoi l'entrée de l'utilisateur (texte)
def ask():
	basicQuestion = "What do you want to know?"
	speak(basicQuestion)
	theRequest = user_speech_v2()
	return theRequest

#SEARCHING() Recherche a travers Wikipedia et lis le sommaire
def searching(aRequest):
	speak("Searching on Wikipedia")
	try:
		results = wikipedia.summary(aRequest, sentences = 3)
		speak("According to Wikipedia ")
		speak(results)
		print(results)
	except wikipedia.exceptions.PageError:
		speak("There was an error in the research please try again")
		print("There was an error in the research please try again")
def tellsTheTime():
	strTime = datetime.datetime.now().strftime("%H:%M:%S")
	speak(f"the time is {strTime}")

def tellsTheDate():
	strDateDay = datetime.date.today().strftime("%d")
	strDateMonth = datetime.date.today().strftime("%m")
	print(strDateMonth)
	strDateYear = datetime.date.today().strftime("%Y")
	if strDateMonth == "01":
		strDateMonthName = "January"
	elif strDateMonth == "02":
		strDateMonthName = "February"
	elif strDateMonth == "03":
		strDateMonthName = "March"
	elif strDateMonth == "04":
		strDateMonthName = "April"
	elif strDateMonth == "05":
		strDateMonthName = "May"
	elif strDateMonth == "06":
		strDateMonthName = "June"
	elif strDateMonth == "07":
		strDateMonthName = "July"
	elif strDateMonth == "08":
		strDateMonthName = "August"
	elif strDateMonth == "09":
		strDateMonthName = "September"
	elif strDateMonth == "10":
		strDateMonthName = "October"
	elif strDateMonth == "11":
		strDateMonthName = "November"
	else:
		strDateMonthName = "December"
	speak(f'today is the {strDateDay} {strDateMonthName} {strDateYear}')

def wolfaramalphaAsk(aQuery):	
	#Client API
	client = wolframalpha.Client("AJ7HAR-LUPQ3RTQU8")
	#Ressources
	res = client.query(aQuery)
	#Results
	result1 = next(res.results).text
	return result1 #returns text

#INTERACTIONS(); la fonction en charge de détécter et selectionner la tache approprié
def interactions(selectInterations):
	if "wikipedia" in selectInterations or "Wikipedia" in selectInterations:
		searching(ask())
	elif "What time is it?" in selectInterations or "what time is it?" in selectInterations or "time?" in selectInterations:
		tellsTheTime()
	elif "are you human" in selectInterations:
		human()
	elif "Today" in selectInterations or "today" in selectInterations:
		tellsTheDate()
	elif "who are you" in selectInterations or "ZAI" in selectInterations:
		firstPresentation()
	elif "Hello" in selectInterations or "hello" in selectInterations:
		speak("Hello there")
	elif "exit" in selectInterations:
		quit()
	else:
		speak(wolfaramalphaAsk(selectInterations))
		print(wolfaramalphaAsk(selectInterations))
	#else:
	#	print("Sorry, I didn't understand could you please repeat?")


########################################
############## MAIN ####################

#THE BRAIN
def main():
	while(1):
		try:
			print(f"Your voice: {user_speech()}")
			interactions(user_speech())
		#interactions(input())
		except Exception as e:
			print(e)
			continue

if __name__ == '__main__':
	main()