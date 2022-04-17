from tkinter import *  
from tkinter import ttk  
app=Tk()  
#App Title  
app.title("Python GUI Application ")  
#Lable  
name=ttk.Label(app, text="Draw basic line")  
name.pack()  
#Canvas  
canvas=Canvas(app)  
canvas.pack()  
canvas.config(width=480,height=360)  
#Canvas values  
line=canvas.create_line(60,160,280,90,fill='blue',width=5)  
#Calling Main()  
app.mainloop() 
