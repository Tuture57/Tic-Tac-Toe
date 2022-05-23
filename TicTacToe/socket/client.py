from tkinter import *
from tkinter import messagebox
import random as r
import socket
import threading

######################################
HOST_ADDR = "127.0.0.1"
HOST_PORT = 8432

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST_ADDR, HOST_PORT))

######################################

def button(master):
    leBouton = Button(master,bg="white",width=3,text="   ",font=('arial',60,'bold'),bd=1)
    return leBouton

def gameReset():
    global temp, boutonmask, a, advteam, tours
    tours = 0
    temp = []
    boutonmask = []
    if a == "X":
        a = "O"
        advteam = "X"
    elif a == "O":
        a = "X"
        advteam = "O"
    for i in range(3):
        for j in range(3):
            grid[i][j]["text"] = ""
            grid[i][j]["state"] = NORMAL
    if a == "X":
        label.config(text = "C'est a ton tour "+ a)
        click_enable()
    elif a =="O":
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
        if len(boutonmask)!=0:
            row = i[0]
            col = i[1]
            grid[row][col]["state"] = DISABLED


def checkWin():
    global a, advteam, tours
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
    click_disable()
    label.config(text = "C'est au tour de l'adversaire "+ advteam)
    checkWin()


def buttonClick2(row,col):
    global a, advteam, boutonmask, temp, tours
    tours = tours + 1
    grid[row][col].config(text=advteam, state=DISABLED, disabledforeground=color[advteam])
    temp = [row,col]
    boutonmask.append(temp)
    click_enable()
    label.config(text = "C'est a ton tour "+ a)
    checkWin2()


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
root.title("client")
root.geometry("460x530")
root.resizable(height=False, width=False)
root.configure(bg="white")
msg=client.recv(4096)
a = msg.decode()
print(a)
if a == "O":
    advteam = "X"
elif a == 'X':
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