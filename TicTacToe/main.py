import tkinter
from tkinter import *
from tkinter import messagebox
import random as r
import sys
import os


clef = 97


fenetre = Tk()
fenetre.config(bg = "#87CEEB") #Couleur fond d'écran
fenetre.geometry("640x480")
fenetre.resizable(height=False, width=False)
label = Label(fenetre, text="Bienvenue sur le jeu",padx=100, pady=50)
label.pack()

def play():
    os.system('py ./game.py')

def server():
    os.system('py ./serv.py')

def client():
    os.system('py ./client.py')



play = Button(fenetre, text="Play", command = play)
play.pack()
server = Button(fenetre, text="Serveur", command = server)
server.pack()
client = Button(fenetre, text="Client", command = client)
client.pack()


fenetre.mainloop()


