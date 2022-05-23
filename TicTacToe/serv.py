#Les imports de librairies
from tkinter import *
from tkinter import messagebox
import random as r
import socket
import threading

#La config des données du serveur
host, port = ('127.0.0.1', 8432)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#met le serv en marche
socket.bind((host, port))
socket.listen(5)
print("le serveur est démarré")
#attend la connexion du client
client, adress = socket.accept()
print("Le client d'ip", adress,"s'est connecté")

#création du modele bouton
def button(master):
    leBouton = Button(master,bg="white",width=3,text="   ",font=('arial',60,'bold'),bd=1)
    return leBouton

#fonction pour réinitialiser le plateau de jeu
def gameReset():
    global temp, boutonmask, a, advteam, tours
    #réinitialise des variables temporaires
    tours = 0
    temp = []
    boutonmask = []
    #échange les croix et les ronds avec l'adversaire
    if a == "X":
        a = "O"
        advteam = "X"
    elif a == "O":
        a = "X"
        advteam = "O"
    #réinitialise le plateau de jeu
    for i in range(3):
        for j in range(3):
            grid[i][j]["text"] = ""
            grid[i][j]["state"] = NORMAL
    #Permet a celui qui a les croix de commencer et bloque celui qui a les ronds de commencer
    if a == "X":
        label.config(text = "C'est a ton tour "+ a)
        click_enable()
    elif a == "O":
        label.config(text = "C'est au tour de l'adversaire "+ advteam)
        click_disable()

#Fonction pour désactiver la cliquabilité du plateau de jeu
def click_disable():
    for i in range(3):
        for j in range(3):
            grid[i][j]["state"] = DISABLED

#Fonction pour réactiver la cliquabilité du plateau de jeu
def click_enable():
    global boutonmask
    for i in range(3):
        for j in range(3):
            grid[i][j]["state"] = NORMAL
    #redésactive les cases déjà utilisées 
    for i in boutonmask:
        if len(boutonmask)!=0:
            row = i[0]
            col = i[1]
            grid[row][col]["state"] = DISABLED

#Fonction pour vérifier la victoire de soi-meme
def checkWin():
    global a, tours, advteam
    for i in range(3):
        #vérifie pour la meme ligne ou colonne
        if grid[i][0]["text"] == grid[i][1]["text"] == grid[i][2]["text"] == a or grid[0][i]["text"] == grid[1][i]["text"] == grid[2][i]["text"] == a:
            messagebox.showinfo("Victoire", "tu as gagné")
            gameReset()
        #Vérifie pour les diagonales 
        elif grid[0][0]["text"] == grid[1][1]["text"] == grid[2][2]["text"] == a or grid[0][2]["text"] == grid[1][1]["text"] == grid[2][0]["text"] == a:
            messagebox.showinfo("Victoire", "tu as gagné")
            gameReset()
        #Vérifie s'il y a une egalité
        elif tours == 9 and grid[0][0]["text"] != "" and grid[0][1]["text"] != "" and grid[0][2]["text"] != "" and grid[1][0]["text"] != "" and grid[1][1]["text"] != "" and grid[1][2]["text"] != "" and grid[2][0]["text"] != "" and grid[2][1]["text"] != "" and grid[2][2]["text"] != "":
            messagebox.showinfo("Egalité", "vous avez fait une egalité")
            gameReset()

def checkWin2():
    global a, advteam, tours
    for i in range(3):
        #vérifie pour la meme ligne ou colonne
        if grid[i][0]["text"] == grid[i][1]["text"] == grid[i][2]["text"] == advteam or grid[0][i]["text"] == grid[1][i]["text"] == grid[2][i]["text"] == advteam:
            messagebox.showinfo("Perdu", "tu as perdu")
            gameReset()
        #Vérifie pour les diagonales 
        elif grid[0][0]["text"] == grid[1][1]["text"] == grid[2][2]["text"] == advteam or grid[0][2]["text"] == grid[1][1]["text"] == grid[2][0]["text"] == advteam:
            messagebox.showinfo("Perdu", "tu as perdu")
            gameReset()
        #Vérifie s'il y a une egalité
        elif tours == 9 and grid[0][0]["text"] != "" and grid[0][1]["text"] != "" and grid[0][2]["text"] != "" and grid[1][0]["text"] != "" and grid[1][1]["text"] != "" and grid[1][2]["text"] != "" and grid[2][0]["text"] != "" and grid[2][1]["text"] != "" and grid[2][2]["text"] != "":
            messagebox.showinfo("Egalité", "vous avez fait une egalité")
            gameReset()
            
#Fonction qui sync ses coups
def buttonClick(row,col):
    global a, boutonmask, temp, tours
    #compte les tours pour vérifier l'egalite
    tours = tours + 1
    #desactive le bouton cliqué pour ne pas le reutiliser
    grid[row][col].config(text=a, state=DISABLED, disabledforeground=color[a])
    #envoie les données a l'ordi de l'adversaire
    data = f"{row}{col}"
    client.send(data.encode())
    #ajoute la la liste des cases remplies pour ne pas les reutiliser
    temp = [row,col]
    boutonmask.append(temp)
    click_disable()
    label.config(text = "C'est au tour de l'adversaire "+ advteam)
    checkWin()

#Fonction qui sync les coups de l'adversaire
def buttonClick2(row,col):
    global a, advteam, boutonmask, temp, tours
    #compte les tours pour vérifier l'egalite
    tours = tours + 1
    #desactive le bouton cliqué pour ne pas le reutiliser
    grid[row][col].config(text=advteam, state=DISABLED, disabledforeground=color[advteam])
    #ajoute la la liste des cases remplies pour ne pas les reutiliser
    temp = [row,col]
    boutonmask.append(temp)
    #Réactive le clic car ca repasse a son tour
    click_enable()
    label.config(text = "C'est a ton tour "+ a)
    checkWin2()

#Fonction qui permet de recevoir les données de l'adversaire et de les traiter
def message_receive():
    #boucle infinie pour ne pas arreter la reception
    while True:
        msg=client.recv(4096)
        msg=msg.decode()
        if msg:
            msg = list(msg)
            buttonClick2(int(msg[0]), int(msg[1]))
            print(msg)

        msg = None

#Main variables

root = Tk()
root.title("server")
root.geometry("460x530")
root.resizable(height=False, width=False)
root.configure(bg="white")
a = r.choice(["O","X"])
if a == "O":
    client.send("X".encode())
    advteam = "X"
elif a == 'X':
    client.send("O".encode())
    advteam = "O"
color = {"O": "red", "X": "blue"}
boutonmask = []
temp = []
tours = 0


#Grid def

grid = [[],[],[]]

for i in range(3):
    for j in range(3):
        grid[i].append(button(root))
        grid[i][j].config(command=lambda row=i,col=j:buttonClick(row,col))
        grid[i][j].grid(row=i, column=j)

#Label def

label = Label(text = "", font=("arial",20,"bold"))
label.grid(row=3, column=0, columnspan=3)

threading._start_new_thread(message_receive, ())
gameReset()
root.mainloop()