from tensorflow.keras.models import load_model
from time import sleep
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.preprocessing import image
import cv2
import numpy as np
import os,random
import subprocess
import time
from tkinter import *
import pygame
from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
os.environ['TF_CPP_MIN_LOG_LEVEL'] = "2"

face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
classifier =load_model("Emotion_Detection.h5")

emotion_labels = ['Angry','Happy','Neutral', 'Sad', 'Surprise']

cap = cv2.VideoCapture(0)
now = time.time()
future = now + 10
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    key=cv2.waitKey(30) & 0xFF 
    if time.time() > future:##after 20second music will play
        
        cv2.destroyAllWindows()
        class MusicPlayer:

        # Defining Constructor
            def __init__(self,root):
                self.root = root
                    # Title of the window
                self.root.title("Music Player")
                # Window Geometry
                self.root.geometry("1800x900")
                self.root.configure(background = 'white')

                self.music=PhotoImage(file='icons/m5.png')
                self.play=PhotoImage(file='buttons/play1.png')
                self.pause=PhotoImage(file='buttons/pause2.png')
                self.rewind=PhotoImage(file='buttons/rewind1.png')
                self.stop=PhotoImage(file='buttons/stop1.png')
                self.next=PhotoImage(file='buttons/next.png')
                self.prev=PhotoImage(file='buttons/prev.png')
                # Initiating Pygame
                pygame.init()
                # Initiating Pygame Mixer
                pygame.mixer.init()
                # Declaring track Variable
                self.track = StringVar()
                # Declaring Status Variable
                self.status = StringVar()
                #Declaring mood
                self.mood = StringVar()
                #Declaring mood
                self.heading= StringVar()
                self.listofsongs=[]
                self.index = 0

                #heading frame
                headingframe = LabelFrame(self.root,font=("times new roman",24,"bold"),relief=GROOVE)
                headingframe.place(x=0,y=0,width=1700,height=100)

                
                #caption frame
                captionframe = LabelFrame(self.root,text="Your Mood",font=("times new roman",15,"bold"),fg="black",relief=GROOVE)
                captionframe.place(x=0,y=100,width=1000,height=70)

                # Creating Track Frame for Song label & status label
                trackframe = LabelFrame(self.root,text="Song Track",font=("times new roman",15,"bold"),fg="black",relief=GROOVE)
                trackframe.place(x=1000,y=100,width=600,height=640)
                # Inserting Song Track Label
                canvas=Label(trackframe,image=self.music,width=600, height=550).grid(row=0,column=0)
                songtrack = Label(trackframe,textvariable=self.track,width=65, height=2,font=("times new roman",12,"bold"),fg="black").grid(row=1,column=0)
                mood = Label(captionframe,textvariable=self.mood,width=50,height=1,font=("times new roman",20,"bold"),fg="black").grid(row=0,column=1)
                heading = Label(headingframe,textvariable=self.heading,width=70,height=2,font=("times new roman",30,"bold"),bg="black",fg="white").grid(row=0,column=0)

                # Inserting Status Label
                #trackstatus = Label(trackframe,textvariable=self.status,font=("times new roman",24,"bold"),bg="grey",fg="gold").grid(row=2,column=0,padx=10,pady=5)
                
                # Creating Button Frame
                buttonframe = LabelFrame(self.root,font=("times new roman",15,"bold"),bg="skyblue",fg="black",relief=GROOVE)
                buttonframe.place(x=0,y=740,width=1700,height=100)
                # Inserting Play Button
                prevbtn = Button(buttonframe,text="PREV",image=self.prev,width=50,height=50,command=self.prevsong,font=("times new roman",16,"bold"),bg="skyblue",fg="navyblue").grid(row=0,column=2,padx=20,pady=5)
                playbtn = Button(buttonframe,text="PLAY",image=self.play,width=50,height=50,command=self.playsong,font=("times new roman",16,"bold"),bg="skyblue",fg="navyblue").grid(row=0,column=3,padx=20,pady=5)
                nextbtn = Button(buttonframe,text="NEXT",image=self.next,width=50,height=50,command=self.nextsong,font=("times new roman",16,"bold"),bg="skyblue",fg="navyblue").grid(row=0,column=4,padx=20,pady=5)

                # Inserting Pause Button
                pausebtn = Button(buttonframe,text="PAUSE",image=self.pause,width=50,height=50,command= lambda:self.pausesong(paused),font=("times new roman",16,"bold"),bg="skyblue",fg="navyblue").grid(row=0,column=5,padx=20,pady=5)
                # Inserting Unpause Button
                rewindbtn = Button(buttonframe,text="Rewind",image=self.rewind,width=50,height=50,command=self.rewindsong,font=("times new roman",16,"bold"),bg="skyblue",fg="navyblue").grid(row=0,column=6,padx=20,pady=5)
                # Inserting Stop Button
                stopbtn = Button(buttonframe,text="STOP",image=self.stop,width=50,height=50,command=self.stopsong,font=("times new roman",16,"bold"),bg="skyblue",fg="navyblue").grid(row=0,column=7,padx=20,pady=5)

                # Creating Playlist Frame
                songsframe = LabelFrame(self.root,text="Song Playlist",font=("times new roman",15,"bold"),fg="black",relief=GROOVE)
                songsframe.place(x=0,y=170,width=1000,height=570)

                #btnframe = LabelFrame(self.root,font=("times new roman",15,"bold"),fg="white",relief=GROOVE)
                #btnframe.place(x=0,y=740,width=1000,height=100)
                addbtn = Button(buttonframe,text="Add songs",width=42,height=4,command=self.browse_file,font=("times new roman",16,"bold"),bg="deepskyblue",fg="black").grid(row=0,column=1,pady=1)
                delbtn = Button(buttonframe,text="Delete songs",width=42,height=4,command=self.del_song,font=("times new roman",16,"bold"),bg="deepskyblue",fg="black").grid(row=0,column=8,pady=1)


                # Inserting scrollbar
                scrol_y = Scrollbar(songsframe,orient=VERTICAL)
                # Inserting Playlist listbox
                self.playlist = Listbox(songsframe,width=700,height=400,yscrollcommand=scrol_y.set,selectbackground="pale violet red",selectmode=SINGLE,font=("times new roman",12,"bold"),bg="lightpink",fg="black",relief=GROOVE)
                # Applying Scrollbar to listbox
                scrol_y.pack(side=RIGHT,fill=Y)
                scrol_y.config(command=self.playlist.yview)
                self.playlist.pack(fill=BOTH)
                self.heading.set("Emotion Based Music Player")

                if label=='Neutral':

                    # Changing Directory for fetching Songs
                    os.chdir("playlist/Neutral")
                    self.mood.set("You are looking neutral, I am playing the song for You")

                    # Fetching Songs
                    songtracks = os.listdir()
                    # Inserting Songs into Playlist
                    for track in songtracks:
                        self.playlist.insert(END,track)
                if label=='Happy':

                    # Changing Directory for fetching Songs
                    os.chdir("playlist/Happy")
                    self.mood.set("You are looking happy, I am playing the song for You")

                    # Fetching Songs
                    songtracks = os.listdir()
                    # Inserting Songs into Playlist
                    for track in songtracks:
                        self.playlist.insert(END,track)
                if label=='Sad':

                    # Changing Directory for fetching Songs
                    os.chdir("playlist/Sad")
                    self.mood.set("You are looking sad, I am playing the song for You")

                    # Fetching Songs
                    songtracks = os.listdir()
                    # Inserting Songs into Playlist
                    for track in songtracks:
                        self.playlist.insert(END,track)                                                        
                if label=='Surprise':

                    # Changing Directory for fetching Songs
                    os.chdir("playlist/Surprise")
                    self.mood.set("You are looking surprise, I am playing the song for You")

                    # Fetching Songs
                    songtracks = os.listdir()
                    # Inserting Songs into Playlist
                    for track in songtracks:
                        self.playlist.insert(END,track)
                if label=='Angry':

                    # Changing Directory for fetching Songs
                    os.chdir("playlist/Angry")
                    self.mood.set("You are looking angry, I am playing the song for You")

                    # Fetching Songs
                    songtracks = os.listdir()
                    # Inserting Songs into Playlist
                    for track in songtracks:
                        self.playlist.insert(END,track)

                

            # Defining Play Song Function
            def playsong(self):
                # Displaying Selected Song title
                self.track.set(self.playlist.get(ACTIVE))
                # Displaying Status
            # self.status.set("-Playing")
                # Loading Selected Song
                pygame.mixer.music.load(self.playlist.get(ACTIVE))
                # Playing Selected Song
                pygame.mixer.music.play()
            def rewindsong(self):
                pygame.mixer.music.rewind()
            def stopsong(self):
                # Displaying Status
                #self.status.set("-Stopped")
                # Stopped Song
                pygame.mixer.music.stop()

            global paused
            paused = False
            def pausesong(self,is_paused):
                global paused
                paused=is_paused
                # Displaying Status
                #self.status.set("-Paused")
                # Paused Song
                if paused:
                    pygame.mixer.music.unpause()
                    paused= False
                else:  
                    pygame.mixer.music.pause()
                    paused= True

            def nextsong(self):
                next_song=self.playlist.curselection()
                next_song=next_song[0]+1
                song=self.playlist.get(next_song)
                self.track.set(self.playlist.get(next_song))
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.playlist.selection_clear(0,END)
                self.playlist.activate(next_song)
                self.playlist.selection_set(next_song,last=None)

            def prevsong(self):
                next_song=self.playlist.curselection()
                next_song=next_song[0]-1
                song=self.playlist.get(next_song)
                self.track.set(self.playlist.get(next_song))
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                self.playlist.selection_clear(0,END)
                self.playlist.activate(next_song)
                self.playlist.selection_set(next_song,last=None)

            def browse_file(self):
                global filename
                filename = filedialog.askopenfilename()
                f = os.path.basename(filename)
                index = 0
                self.playlist.insert(index, f)
                index += 1  
                add=tk.messagebox.showinfo("Success","Song add successfully.")    

            def del_song(self):
                selected_song = self.playlist.curselection()
                selected_song = int(selected_song[0])
                self.playlist.delete(selected_song)
                delete=tk.messagebox.showinfo("Success","Song Delete successfully.")
            
            

        # Creating TK Container
        root = Tk()
        # Passing Root to MusicPlayer Class
        application=MusicPlayer(root)
        # Root Window Looping
        root.mainloop()
            
        

    if key == 27:  # The Esc key
        break
      
cap.release()
cv2.destroyAllWindows()
