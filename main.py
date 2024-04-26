from tkinter import *
from tkinter import ttk


class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        styl = ttk.Style()        
        styl.configure('my_mainframe.TFrame', background="red")

        self.title("Tournament Tableu")
        self.geometry('900x600')
        self.resizable(True, True)

        #Creating a mainfraime to place all widgets there. Add a style to configure the backgroundcolor
        self.mainframe = Mainframe(self, padding="3 3 12 12", style='my_mainframe.TFrame')
        self.mainframe.grid(column=0, row=0, sticky=(W, N, S, E)) #stick in all directions

        #Wenn the window size changed, mainfraim changes its size too:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # self.tournier_name_text = StringVar()
        # self.tournier_name_label_text = StringVar(value="")

        

        # def tournier_input_save(self, entered_text):
        #     self.tournier_name_text.set(entered_text)


class Mainframe(ttk.Frame):
    def __init__(self, parent, padding=None, style=None):
        super().__init__(parent, padding=padding, style=style)

        self.create_widgets()
        
    def create_widgets(self):

        btn_tournier = ttk.Button(self, text="Turnier/Stuffe", command=self.set_tournier_name)
        btn_tournier.grid(column=1, row=1, columnspan=3)

        tournier_name_label = ttk.Label(self, text="Test text!")
        tournier_name_label.grid(column=5, row=1, columnspan=2)
    
    def set_tournier_name(self):
            input_window = InputWindow(self.master, "Tournier, Gruppe")
            input_window.wait_window()
    

class InputWindow(Toplevel):
    # def __init__(self, titel, parent):
    def __init__(self, parent, titel):
        super().__init__(parent)
        # self.tournier
        # tournier = StringVar()
        # self.parent = parent
        self.title(titel)
        self.geometry("500x300")
        # self.input_line = StringVar()

        # entry_field = ttk.Entry(self, width= 50, textvariable=self.input_line)
        # entry_field.grid(column=1, row=1, sticky=W)

        # btn_ok = ttk.Button(self, text="Speichern", command=self.save_input)
        # btn_ok.grid(column=2, row=1, sticky=E)
            
    def save_input(self):
        # global entered_line
        entered_line = self.input_line.get()
        self.parent.tournier_input_save(entered_line)
        self.destroy()

    # def __str__(self) -> str:
    #     return tournier.get()








root = MainWindow()
root.mainloop()


