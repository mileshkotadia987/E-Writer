import pyttsx3
import time
import datetime

def speak(audio):
	engine = pyttsx3.init()
	engine.setProperty('rate', 120)
	engine.setProperty('volume', 1)
	engine.say(audio)
	engine.runAndWait()

def wishMe():
	hour = int(datetime.datetime.now().hour)
	if hour>= 0 and hour<12:
		speak("Good Morning Sir !")

	elif hour>= 12 and hour<18:
		speak("Good Afternoon Sir !")

	else:
		speak("Good Evening Sir !")




def ex1(prev = ''):
	input_file = open("output.txt","rt")
	mytext = input_file.read()
	words = mytext.split(' ')
	char = mytext[-1]
	if prev == mytext:
		speak("")
	else:
		if char == " ":
			speak(words[-1])
		else:
			speak(char)
	# for i in words:
	# 	for j in i:
	# 		speak(j)
	# 	speak(i)
	input_file.close()
	prev = mytext
	ex1(prev)



wishMe()
speak("welcome to this E-Writer application.")
speak("I am your Assistant. You can start writing!!")
prev = ''
ex1(prev)
