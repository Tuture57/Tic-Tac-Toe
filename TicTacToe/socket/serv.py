from tkinter import *
from tkinter import messagebox
import random as r
import socket
import threading

######################################
host, port = ('127.0.0.1', 8432)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind((host, port))
socket.listen(5)
print("le serveur est démaré")
client, adress = socket.accept()
print("Le client d'ip", adress,"s'est connecté")

######################################

def button(master):
    leBouton = Button(master,bg="white",width=3,text="   ",font=('arial',60,'bold'),bd=1)
    return leBouton

def playerPlaying():
    global a
    if a == "X":
        a = "O"
    elif a == "O":
        a = "X"

def gameReset():
    global temp, boutonmask, a, advteam
    temp = []
    boutonmask = []
    for i in range(3):
        for j in range(3):
            grid[i][j]["text"] = ""
            grid[i][j]["state"] = NORMAL
    if a == "X":
        label.config(text = "C'est a ton tour "+ a)
        click_enable()
    elif advteam == "X":
        label.config(text = "C'est au tour de l'adversaire "+ advteam)
        click_disable()


def click_disable():
    for i in range(3):
        for j in range(3):
            grid[i][j]["state"] = DISABLED

def click_enable():
    global boutonmask
    for i in range(3):
        for j in range(3):
            grid[i][j]["state"] = NORMAL
    for i in boutonmask:
        row = i[0]
        col = i[1]
        grid[row][col]["state"] = DISABLED

def checkWin():
    global a, tours
    for i in range(3):
        if grid[i][0]["text"] == grid[i][1]["text"] == grid[i][2]["text"] == a or grid[0][i]["text"] == grid[1][i]["text"] == grid[2][i]["text"] == a:
            messagebox.showinfo("Victoire", "tu as gagné")
            gameReset()

        elif grid[0][0]["text"] == grid[1][1]["text"] == grid[2][2]["text"] == a or grid[0][2]["text"] == grid[1][1]["text"] == grid[2][0]["text"] == a:
            messagebox.showinfo("Victoire", "tu as gagné")
            gameReset()

        elif tours == 9 and grid[0][0]["text"] != "" and grid[0][1]["text"] != "" and grid[0][2]["text"] != "" and grid[1][0]["text"] != "" and grid[1][1]["text"] != "" and grid[1][2]["text"] != "" and grid[2][0]["text"] != "" and grid[2][1]["text"] != "" and grid[2][2]["text"] != "":
            messagebox.showinfo("Egalité", "vous avez fait une egalité")
            gameReset()

def checkWin2():
    global a, advteam, tours
    for i in range(3):
        if grid[i][0]["text"] == grid[i][1]["text"] == grid[i][2]["text"] == advteam or grid[0][i]["text"] == grid[1][i]["text"] == grid[2][i]["text"] == advteam:
            messagebox.showinfo("Perdu", "tu as perdu")
            gameReset()

        elif grid[0][0]["text"] == grid[1][1]["text"] == grid[2][2]["text"] == advteam or grid[0][2]["text"] == grid[1][1]["text"] == grid[2][0]["text"] == advteam:
            messagebox.showinfo("Perdu", "tu as perdu")
            gameReset()

        elif tours == 9 and grid[0][0]["text"] != "" and grid[0][1]["text"] != "" and grid[0][2]["text"] != "" and grid[1][0]["text"] != "" and grid[1][1]["text"] != "" and grid[1][2]["text"] != "" and grid[2][0]["text"] != "" and grid[2][1]["text"] != "" and grid[2][2]["text"] != "":
            messagebox.showinfo("Egalité", "vous avez fait une egalité")
            gameReset()

def buttonClick(row,col):
    global a, boutonmask, temp, tours
    tours = tours + 1
    grid[row][col].config(text=a, state=DISABLED, disabledforeground=color[a])
    data = f"{row}{col}"
    client.send(data.encode())
    temp = [row,col]
    boutonmask.append(temp)
    print(boutonmask)
    click_disable()
    checkWin()
    label.config(text = "C'est au tour de l'adversaire "+ advteam)

def buttonClick2(row,col):
    global a, advteam, boutonmask, temp, tours
    tours = tours + 1
    grid[row][col].config(text=advteam, state=DISABLED, disabledforeground=color[advteam])
    temp = [row,col]
    boutonmask.append(temp)
    print(boutonmask)
    click_enable()
    checkWin2()
    label.config(text = "C'est a ton tour "+ a)

def message_receive():
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

label = Label(text = "C'est a ton tour", font=("arial",20,"bold"))
label.grid(row=3, column=0, columnspan=3)

threading._start_new_thread(message_receive, ())

gameReset()
root.mainloop()