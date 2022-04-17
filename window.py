from Tkinter import *
#from gtts import gTTS
#import os
import pyttsx3
#import time
from time import strftime

class TextWindow:

	def __init__(self, master):
		self.root = master

		frame = Frame(master)
		frame.pack()
		master.title("E - Writer Output")


		self.label = Label(master, text="Connecting...", font=("Helvetica", 50))
		self.label.configure(wraplength=1000)
		#engine = pyttsx3.init()
		#engine.setProperty('rate', 100)
		#engine.setProperty('volume', 10)
		#engine.say("welcome to this E-Writer application. You can start writing whatever you want!!")
		#engine.runAndWait()
		self.label.pack()


		self.update_clock()
		#self.snd()




	def update_clock(self):
		#engine = pyttsx3.init()
		#engine.setProperty('rate', 100)
		#engine.setProperty('volume', 1)
		input_file = open("output.txt","rt")
		mytext=input_file.read()
		self.label.configure(text=mytext)
		#self.snd()

		#input_file1 = open("output.txt","rt")
		#t=input_file.tell()
		#engine.say(mytext[-1])
		#time.sleep(1)
		#while 1:
			#t1=input_file1.read(1)
			#if not t1: break
			#engine.say(t1)

		#l1=mytext.split(" ")
		#engine.say(l1[0])

		#l1.remove(l1[0])
		#for i in range(len(l1)):
			#engine.say(l1[i])

		#l1.pop(0)
		#engine.runAndWait()
		input_file.close()
		#input_file1.close()
		#language = 'en'
		#myobj = gTTS(text=mytext, lang=language, slow=False)
		#myobj.save("welcome.mp3")

		#os.system("start welcome.mp3")

		self.root.after(100, self.update_clock)




root = Tk()
def time():
		string = strftime('%H:%M:%S %p')
		lbl.config(text = string)
		lbl.after(1000, time)

lbl = Label(root, font = ('calibri', 40, 'bold'),foreground = 'black')
lbl.pack(anchor = 'se')
time()

w = Label(root, text='E - WRITER',font=("Times New Roman", 80),background = 'black',foreground = 'white')
w.pack()

canvas=Canvas(root)
canvas.pack()
canvas.config(width=1500,height=100)
line=canvas.create_line(15, 25, 1500, 25,fill='grey',width=5)

app = TextWindow(root)
root.mainloop()
root.destroy()
