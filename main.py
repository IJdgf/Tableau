from tkinter import *
from tkinter import ttk, INSERT
from datetime import timedelta
# import re

# Colors: https://tcl.tk/man/tcl8.6/TkCmd/colors.htm

class MainWindow(Tk):
    def __init__(self):
        super().__init__()

        styl = ttk.Style()        
        styl.configure('my_mainframe.TFrame', background="black")                  
        styl.configure('TLabel', background="black",  foreground = 'white')
        styl.configure('tn1.TLabel', foreground = 'red')
        styl.configure('tn2.TLabel', foreground = 'blue')

        self.title("Tournament Tableu")
        self.geometry('1200x600')
        self.resizable(False, False)

        #Creating a mainfraime to place all widgets there. Add a style to configure the backgroundcolor
        self.mainframe = Mainframe(self, padding="12 12 12 12", style='my_mainframe.TFrame')
        self.mainframe.grid(column=0, row=0, sticky=(W, N, S, E)) #stick in all directions

        #Wenn the window size changed, mainfraim changes its size too:
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)


class Mainframe(ttk.Frame):
    def __init__(self, parent, padding=None, style=None):
        super().__init__(parent, padding=padding, style=style)
        self.parent = parent

        self.tournier_name = StringVar()
        self.tournier_name.set("Tournier")
        self.tn1_points = IntVar()
        self.tn2_points = IntVar()
        self.tn1_points.set(0)
        self.tn2_points.set(0)
        self.tn1_name = StringVar()
        self.tn2_name = StringVar()
        self.round_time = timedelta(minutes=0, seconds=30)
        self.minuten = int(self.round_time.total_seconds()/60)
        self.sekunden = int(self.round_time.total_seconds()%60)
        self.clock = StringVar()
        self.clock.set(value=f"{str(self.minuten).zfill(2)}:{str(self.sekunden).zfill(2)}")
        self.timer_on = False
        self.zaehler = True
        self.min_setter = StringVar(value="00")
        self.sec_setter = StringVar(value="30")
        self.fokus_disp = StringVar()
        # self.check_timer_entry_wrapper = (self.register(self.check_timer_entry), '%P')    #register the validation method in the Frame -> doesn't work

        self.create_widgets()
        self.bindings() #Commands from the Keyboard
        self.timer_go()

    def bindings(self):
        self.parent.bind('q', lambda event: self.score_plus(self.tn1_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind('a', lambda event: self.score_minus(self.tn1_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind('w', lambda event: self.score_plus(self.tn2_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind('s', lambda event: self.score_minus(self.tn2_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind("<space>", lambda event: self.time_on() if not isinstance(self.focus_get(), ttk.Entry) else None)
        not_name = str(self.tn1_entry.focus_get()) != ".!mainframe.!entry" and str(self.tn1_entry.focus_get()) != ".!mainframe.!entry2"
        self.parent.bind("<Return>", lambda event: self.set_timer() if not_name else None)
        self.bind('<Button-1>', lambda event: self.focus_set()) #Left mouse click to move the fokus away from widgets

    def create_widgets(self):
        btn_tournier = ttk.Button(self, text="Turnier/Stuffe", command=self.set_tournier_name)
        btn_tournier.grid(column=1, row=1, columnspan=2, sticky=W)


        tournier_name_label = ttk.Label(self, textvariable=self.tournier_name, font=('TkTextFont', 20, 'bold'))
        tournier_name_label.grid(column=5, row=1, columnspan=3)

        self.tn1_entry = ttk.Entry(self, width=15, textvariable=self.tn1_name, font=('TkTextFont', 20))
        self.tn1_entry.grid(column=1, row=3, columnspan=2, sticky=W)

        self.tn2_entry = ttk.Entry(self, width=15, textvariable=self.tn2_name, font=('TkTextFont', 20))
        self.tn2_entry.grid(column=10, row=3, columnspan=2, sticky=W)

        self.swap_btn = ttk.Button(self, text='\u2190 Umtauschen \u2192', command= self.name_swap)
        self.swap_btn.grid(column=5, row=3, columnspan=3)

        self.min_entry = ttk.Entry(self, textvariable=self.min_setter, width = 4, validate='key', font=('TkTextFont', 20)) #add validation parameters: type -> doesn't work
        # self.min_entry = ttk.Entry(self, textvariable=self.min_setter, width = 2, validate='key', font=('TkTextFont', 20)) #add validation parameters: type 
        # self.min_entry.configure(validatecommand=self.check_timer_entry_wrapper) #add validation method and delete the wrongsymbol
        # self.time_entry.configure(validatecommand=self.check_timer_entry_wrapper, invalidcommand=self.invalid_character) #add validation method and delete the wrongsymbol
        self.min_entry.grid(column=5, row=4, sticky=E)

        clock_spacer = ttk.Label(self, text=':', font=('TkTextFont', 16, 'bold'))
        clock_spacer.grid(column=6, row=4)

        set_timer = ttk.Button(self, text='Timer einstellen', command=self.set_timer)
        set_timer.grid(column=5, row=5, columnspan=3)

        self.sec_entry = ttk.Entry(self, textvariable=self.sec_setter, width = 4, validate='all', font=('TkTextFont', 20)) #add validation parameters: type -> doesn't work
        # self.sec_entry.configure(validatecommand=self.check_timer_entry_wrapper) #add validation method and delete the wrongsymbol
        # self.sec_entry.configure(validatecommand=self.check_timer_entry_wrapper, invalidcommand=self.invalid_character) #add validation method and delete the wrongsymbol
        self.sec_entry.grid(column=7, row=4, sticky=W)

        tn1_label = ttk.Label(self, textvariable=self.tn1_name, anchor='center', width=12, font=('TkTextFont', 40, 'bold'), style='tn1.TLabel')
        tn1_label.grid(column=1, row=5, columnspan=2)
        tn2_label = ttk.Label(self, textvariable=self.tn2_name, anchor='center', width=12, font=('TkTextFont', 40, 'bold'), style='tn2.TLabel')
        tn2_label.grid(column=10, row=5, columnspan=2)

        tn1_points_label = ttk.Label(self, textvariable=self.tn1_points, font=('TkTextFont', 80, 'bold'), style='tn1.TLabel')
        tn1_points_label.grid(column=1, row=6, columnspan=2)
        tn2_points_label = ttk.Label(self, textvariable=self.tn2_points, font=('TkTextFont', 80, 'bold'), style='tn2.TLabel')
        tn2_points_label.grid(column=10, row=6, columnspan=2)

        tn1_plus_btn = ttk.Button(self, text='+1', width=5, command=lambda: self.score_plus(self.tn1_points, 1))
        tn1_plus_btn.grid(column=1, row=7, sticky=E)
        tn1_plus2_btn = ttk.Button(self, text='+2', width=5, command=lambda: self.score_plus(self.tn1_points, 2))
        tn1_plus2_btn.grid(column=2, row=7, sticky=W)
        tn1_minus_btn = ttk.Button(self, text='-1', width=5, command=lambda: self.score_minus(self.tn1_points, 1))
        tn1_minus_btn.grid(column=1, row=8, sticky=E)
        tn1_minus2_btn = ttk.Button(self, text='-2', width=5, command=lambda: self.score_minus(self.tn1_points, 2))
        tn1_minus2_btn.grid(column=2, row=8, sticky=W)

        tn2_plus_btn = ttk.Button(self, text='+1', width=5, command=lambda: self.score_plus(self.tn2_points, 1))
        tn2_plus_btn.grid(column=10, row=7, sticky=E)
        tn2_plus2_btn = ttk.Button(self, text='+2', width=5, command=lambda: self.score_plus(self.tn2_points, 2))
        tn2_plus2_btn.grid(column=11, row=7, sticky=W)
        tn2_minus_btn = ttk.Button(self, text='-1', width=5, command=lambda: self.score_minus(self.tn2_points, 1))
        tn2_minus_btn.grid(column=10, row=8, sticky=E)
        tn2_minus2_btn = ttk.Button(self, text='-2', width=5, command=lambda: self.score_minus(self.tn2_points, 2))
        tn2_minus2_btn.grid(column=11, row=8, sticky=W)

        clock_label = ttk.Label(self, textvariable=self.clock, font=('TkTextFont', 80, 'bold'))
        clock_label.grid(column=5, row=5, rowspan=2, columnspan=3)

        clock_start_btn = ttk.Button(self, text="Zeit Start/Stop", command=self.time_on)
        clock_start_btn.grid(column=5, row=8, columnspan=3, sticky=(W, E))

        for child in self.winfo_children():        #padding for all the widgets
            child.grid_configure(padx=10, pady=10)

        for i in range(1, 10):
            self.columnconfigure(i, weight=1)
    
    def set_timer(self):
        minn = int(self.min_setter.get())
        secc = int(self.sec_setter.get())
        self.round_time = timedelta(minutes=minn, seconds=secc)
        self.minuten = int(self.round_time.total_seconds()/60)
        self.sekunden = int(self.round_time.total_seconds()%60)
        self.clock.set(value=f"{str(self.minuten).zfill(2)}:{str(self.sekunden).zfill(2)}")
        self.focus_set()  #move fokus to the mainframe (not any widget) to not use this button when spacebar was pressed

    # def check_timer_entry(self, newval):
    #     if not newval:
    #         return True
    #     if not re.match("^[0-9]*$", newval): # проверяем, что строка состоит только из цифр 
    #         return False
        
    # def invalid_character(self):
    #     value = self.sec_setter.get() #current entry value
    #     cursor_index = self.sec_entry.index(INSERT)  #Cursor position
    #     #delete the wrong symbol:
    #     self.sec_setter.set(value[:cursor_index-1] + value[cursor_index:])
    #     return False

    def name_swap(self):
        tempp = StringVar()
        tempp.set(self.tn1_name.get())
        self.tn1_name.set(self.tn2_name.get())
        self.tn2_name.set(tempp.get())
        self.focus_set()   #move fokus to the mainframe (not any widget) to not use this button when spacebar was pressed

    def set_tournier_name(self):
        self.focus_set()
        input_window = InputWindow(self, "Tournier, Gruppe")
        input_window.wait_window()

    def score_plus(self, score: IntVar, quant: int):
        # if str(self.tn1_entry.focus_get()) != ".!mainframe.!entry" and str(self.tn1_entry.focus_get()) != ".!mainframe.!entry2":
        i = score.get()
        i+= quant
        score.set(i)
        self.focus_set()  #move fokus to the mainframe (not any widget) to not use this button when spacebar was pressed
    
    def score_minus(self, score: IntVar, quant: int):
        i = score.get()
        i-= quant
        score.set(i)
        self.focus_set()  #move fokus to the mainframe (not any widget) to not use this button when spacebar was pressed

    def time_on(self):
        
        self.timer_on = not self.timer_on
        print(self.timer_on)
        if self.timer_on:
            self.zaehler = True
            self.timer_go()

    def timer_go(self):
        if (self.zaehler):
            self.round_time += timedelta(milliseconds=999)
            self.zaehler = not self.zaehler
        def time_minus():
            self.round_time -= timedelta(seconds=1)
        
        if self.round_time.total_seconds() > 1 and self.timer_on:
            time_minus()
            self.clock.set(value=f"{str(int(self.round_time.total_seconds()/60)).zfill(2)}:{str(int(self.round_time.total_seconds()%60)).zfill(2)}")
            print(self.round_time)
            print(self.clock.get())
            self.after(1000, self.timer_go)

class InputWindow(Toplevel):
    def __init__(self, parent, titel):
        super().__init__()
        self.parent = parent
        self.title(titel)
        self.geometry("500x150")
        self.input_line = StringVar()
        self.entered_line = ""

        entry_field = ttk.Entry(self, width= 50, textvariable=self.input_line)
        entry_field.grid(column=1, row=1, sticky=W)

        btn_ok = ttk.Button(self, text="Speichern", command=self.save_input)
        btn_ok.grid(column=2, row=1, sticky=E)

        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)
            
    def save_input(self):
        self.entered_line = self.input_line.get()
        self.parent.tournier_name.set(self.entered_line)
        self.destroy()

root = MainWindow()
root.mainloop()


