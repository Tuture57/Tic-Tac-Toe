import tkinter
from tkinter import *
from tkinter import messagebox
import random as r

def button(master):
    leBouton = Button(master,bg="white",width=3,text="   ",font=('arial',60,'bold'),bd=1)
    return leBouton

def playerPlaying():
    global a
    if a == "X": a = "O"
    elif a == "O": a = "X"

def gameReset():
    for i in range(3):
        for j in range(3):
            grid[i][j]["text"] = ""
            grid[i][j]["state"] = NORMAL

def checkWin():
    global a
    for i in range(3):
        if grid[i][0]["text"] == grid[i][1]["text"] == grid[i][2]["text"] == a or grid[0][i]["text"] == grid[1][i]["text"] == grid[2][i]["text"] == a:
            messagebox.showinfo("Victoire",""+a+" a gagné !")
            gameReset()

        elif grid[0][0]["text"] == grid[1][1]["text"] == grid[2][2]["text"] == a or grid[0][2]["text"] == grid[1][1]["text"] == grid[2][0]["text"] == a:
            messagebox.showinfo("Victoire",""+a+" a gagné !")
            gameReset()

        elif grid[0][0]["state"] == grid[0][1]["state"] == grid[0][2]["state"] == grid[1][0]["state"] == grid[1][1]["state"] == grid[1][2]["state"] == grid[2][0]["state"] == grid[2][1]["state"] == grid[2][2]["state"] == DISABLED:
            messagebox.showinfo("Egalité","Le jeu se finit sur une égalité !")
            gameReset()

def buttonClick(row,col):
    global a
    grid[row][col].config(text=a, state=DISABLED, disabledforeground=color[a])
    checkWin()
    playerPlaying()
    label.config(text = "C'est au tour de " + a)

#Main variables

root = Tk()
root.title("TIIIIIIIIIIIIIIIC tac toe")
root.geometry("800x1200")
root.configure(bg="white")
a = r.choice(["O","X"])
color = {"O": "red", "X": "blue"}

#Grid def

grid = [[],[],[]]

for i in range(3):
    for j in range(3):
        grid[i].append(button(root))
        grid[i][j].config(command=lambda row=i,col=j:buttonClick(row,col))
        grid[i][j].grid(row=i, column=j)

#Label def

label = Label(text = "C'est au tour de " + a, font=("arial",20,"bold"))
label.grid(row=3, column=0, columnspan=3)
root.mainloop()
