# Importing Required Modules & libraries
import os
from tkinter import *

import pygame
from PIL import ImageTk


# Defining MusicPlayer Class
class EmoMusicPlayer:

  # Defining Constructor
  def __init__(self,root):
    self.root = root
    # Title of the window
    self.root.title("Music Player")
    # Window Geometry
    self.root.geometry("1700x900")
    self.root.configure(background = '#66CD00')

    self.music=PhotoImage(file='icons/m3.png')
    
    # Initiating Pygame
    pygame.init()
    # Initiating Pygame Mixer
    pygame.mixer.init()
    
    self.heading= StringVar()
    self.caption=StringVar()
    #heading frame
    headingframe = LabelFrame(self.root,font=("times new roman",24,"bold"),relief=GROOVE)
    headingframe.place(x=0,y=0,width=1700,height=100)

    
    #caption frame
    captionframe = LabelFrame(self.root,font=("times new roman",15,"bold"),bg="skyblue",fg="dark blue",relief=GROOVE)
    captionframe.place(x=600,y=100,width=1000,height=600)

    trackframe = LabelFrame(self.root,font=("times new roman",15,"bold"),bg="#B22222",fg="dark blue",relief=GROOVE)
    trackframe.place(x=200,y=200,width=550,height=400)
    canvas=Label(captionframe,image=self.music,width=1000, height=600).grid(row=0,column=0)
    
    heading = Label(headingframe,textvariable=self.heading,width=70,height=2,font=("times new roman",30,"bold"),bg="black",fg="white").grid(row=0,column=0)
    caption = Label(trackframe,textvariable=self.caption,width=27,height=9,font=("times new roman",24,"bold"),bg="#B22222",fg="white").grid(row=0,column=0,padx=12,pady=1)

   
    buttonframe = LabelFrame(self.root,font=("times new roman",15,"bold"),bg="gold",fg="dark blue",relief=GROOVE)
    buttonframe.place(x=360,y=570,width=250,height=70)
    # Inserting Play Button

    playbtn = Button(buttonframe,text="Detect Your Emotion",command=self.fun,width=20,height=2,font=("times new roman",16,"bold"),fg="navyblue",bg="gold").grid(row=0,column=0)
    
    
    self.heading.set("Emotion Based Music Player")
    self.caption.set("Music brings us pleasure and releases\nour suffering.It can calm us down and\npụmp us up.It helps us manage pain,\n sleep better and be more productive.\n-Alex Doman")

  def fun(self):
    #import emoplayer

    os.system('python emplayer.py')

# Creating TK Container
root = Tk()
# Passing Root to MusicPlayer Class
application=EmoMusicPlayer(root)
# Root Window Looping
root.mainloop()
