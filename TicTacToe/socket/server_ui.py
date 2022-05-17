import tkinter as tk
import socket
import threading


window = tk.Tk()
window.title("Le serveur Tic Tac Toe")
window.geometry("515x360+700+200")
window.iconbitmap("ressources/favicon.ico")

switch_off_IMG = tk.PhotoImage(file = "ressources/switch_off.png")
switch_on_IMG = tk.PhotoImage(file = "ressources/switch_on.png")

off_button = tk.Button(window,image=switch_off_IMG, height= 110, width=204, borderwidth = 0, command=lambda: off_on(off_button,on_button))

on_button = tk.Button(window,image=switch_on_IMG, height= 110, width=204, borderwidth = 0, command=lambda: on_off(on_button,off_button))
on_button.pack()


def on_off(widget_on,widget_off):
    widget_on.pack_forget()
    widget_off.pack()


def off_on(widget_off,widget_on):
    widget_off.pack_forget()
    widget_on.pack()


clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="Le serveur est").pack()

clientFrame.pack(side=tk.TOP, pady=(5, 10))






window.mainloop()
