from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Tournament Tableu")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(W, N, S, E))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


