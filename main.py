import time
from tkinter import *
from tkinter import ttk
from datetime import timedelta
from threading import Thread, Timer

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
        self.geometry('900x600')
        self.resizable(True, True)

        #Creating a mainfraime to place all widgets there. Add a style to configure the backgroundcolor
        self.mainframe = Mainframe(self, padding="3 3 12 12", style='my_mainframe.TFrame')
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
        self.round_time = timedelta(minutes=0, seconds=15)
        self.minuten = int(self.round_time.total_seconds()/60)
        self.sekunden = int(self.round_time.total_seconds()%60)
        self.clock = StringVar()
        self.clock.set(value=f"{str(self.minuten).zfill(2)}:{str(self.sekunden).zfill(2)}")
        self.timer_on = False
        self.zaehler = True
        self.time_setter = StringVar(value="01:30")
        self.fokus_disp = StringVar()
        # self.fokus_disp = StringVar(value=str(self.tn1_entry.focus_get()))

        self.create_widgets()
        self.bindings()
        self.timer_go()

    # def bindings(self):
    #     if str(self.tn1_entry.focus_get()) != ".!mainframe.!entry" and str(self.tn1_entry.focus_get()) != ".!mainframe.!entry2":
    #         self.parent.bind('q', lambda event: self.score_plus(self.tn1_points, 1))
    #         self.parent.bind('a', lambda event: self.score_minus(self.tn1_points, 1))
    #         self.parent.bind('w', lambda event: self.score_plus(self.tn2_points, 1))
    #         self.parent.bind('s', lambda event: self.score_minus(self.tn2_points, 1))
    #         self.parent.bind("<space>", lambda event: self.time_on())

    def bindings(self):
        self.parent.bind('q', lambda event: self.score_plus(self.tn1_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind('a', lambda event: self.score_minus(self.tn1_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind('w', lambda event: self.score_plus(self.tn2_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind('s', lambda event: self.score_minus(self.tn2_points, 1) if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.parent.bind("<space>", lambda event: self.time_on() if not isinstance(self.focus_get(), ttk.Entry) else None)
        self.bind('<Button-1>', lambda event: self.focus_set())

        # self.tn1_entry.bind('<KeyPress-q>', lambda event: self.score_plus(self.tn1_points, 1))
        # self.tn1_entry.bind('<KeyPress-a>', lambda event: self.score_minus(self.tn1_points, 1))
        # self.tn2_entry.bind('<KeyPress-w>', lambda event: self.score_plus(self.tn2_points, 1))
        # self.tn2_entry.bind('<KeyPress-s>', lambda event: self.score_minus(self.tn2_points, 1))
        # self.bind('<space>', lambda event: self.time_on())

    
    def create_widgets(self):
        btn_tournier = ttk.Button(self, text="Turnier/Stuffe", command=self.set_tournier_name)
        btn_tournier.grid(column=1, row=1, columnspan=2, sticky=W)


        tournier_name_label = ttk.Label(self, textvariable=self.tournier_name, font=('TkTextFont', 20, 'bold'))
        tournier_name_label.grid(column=5, row=1, columnspan=2)

        self.tn1_entry = ttk.Entry(self, width=30, textvariable=self.tn1_name)
        self.tn1_entry.grid(column=1, row=3, columnspan=2, sticky=W)

        # self.fokus_disp = StringVar(value=str(self.tn1_entry.focus_get()))
        # fokus_label = ttk.Label(self, textvariable=self.fokus_disp)
        # fokus_label.grid(column=7, row=1)
        # # self.fokus_disp = self.focus_get() --------------------------------------------

        self.tn2_entry = ttk.Entry(self, width=30, textvariable=self.tn2_name)
        self.tn2_entry.grid(column=7, row=3, columnspan=2, sticky=W)

        self.swap_btn = ttk.Button(self, text='\u2190 Umtauschen \u2192', command= self.name_swap)
        self.swap_btn.grid(column=5, row=3, columnspan=2)

        time_entry = ttk.Entry(self, textvariable=self.time_setter, width = 5)
        time_entry.grid(column=5, row=4, columnspan=2)

        tn1_label = ttk.Label(self, textvariable=self.tn1_name, font=('TkTextFont', 40, 'bold'), style='tn1.TLabel')
        tn1_label.grid(column=1, row=5, columnspan=2)
        tn2_label = ttk.Label(self, textvariable=self.tn2_name, font=('TkTextFont', 40, 'bold'), style='tn2.TLabel')
        tn2_label.grid(column=7, row=5, columnspan=2)

        tn1_points_label = ttk.Label(self, textvariable=self.tn1_points, font=('TkTextFont', 80, 'bold'), style='tn1.TLabel')
        tn1_points_label.grid(column=1, row=6, columnspan=2)
        tn2_points_label = ttk.Label(self, textvariable=self.tn2_points, font=('TkTextFont', 80, 'bold'), style='tn2.TLabel')
        tn2_points_label.grid(column=7, row=6, columnspan=2)

        tn1_plus_btn = ttk.Button(self, text='+1', width=5, command=lambda: self.score_plus(self.tn1_points, 1))
        tn1_plus_btn.grid(column=1, row=7, sticky=E)
        tn1_plus2_btn = ttk.Button(self, text='+2', width=5, command=lambda: self.score_plus(self.tn1_points, 2))
        tn1_plus2_btn.grid(column=2, row=7, sticky=W)
        tn1_minus_btn = ttk.Button(self, text='-1', width=5, command=lambda: self.score_minus(self.tn1_points, 1))
        tn1_minus_btn.grid(column=1, row=8, sticky=E)
        tn1_minus2_btn = ttk.Button(self, text='-2', width=5, command=lambda: self.score_minus(self.tn1_points, 2))
        tn1_minus2_btn.grid(column=2, row=8, sticky=W)

        tn2_plus_btn = ttk.Button(self, text='+1', width=5, command=lambda: self.score_plus(self.tn2_points, 1))
        tn2_plus_btn.grid(column=7, row=7, sticky=E)
        tn2_plus2_btn = ttk.Button(self, text='+2', width=5, command=lambda: self.score_plus(self.tn2_points, 2))
        tn2_plus2_btn.grid(column=8, row=7, sticky=W)
        tn2_minus_btn = ttk.Button(self, text='-1', width=5, command=lambda: self.score_minus(self.tn2_points, 1))
        tn2_minus_btn.grid(column=7, row=8, sticky=E)
        tn2_minus2_btn = ttk.Button(self, text='-2', width=5, command=lambda: self.score_minus(self.tn2_points, 2))
        tn2_minus2_btn.grid(column=8, row=8, sticky=W)

        clock_label = ttk.Label(self, textvariable=self.clock, font=('TkTextFont', 80, 'bold'))
        clock_label.grid(column=5, row=5, rowspan=2, columnspan=2)

        clock_start_btn = ttk.Button(self, text="Zeit Start/Stop", command=self.time_on)
        clock_start_btn.grid(column=5, row=8, columnspan=2, sticky=(W, E))

        # print(tournier_name_label['font'])
        for child in self.winfo_children():
            child.grid_configure(padx=10, pady=10)
    
    # def name_ok(self, inp: StringVar, outp: StringVar):
    #     outp.set(inp.get())

    def name_swap(self):
        tempp = StringVar()
        tempp.set(self.tn1_name.get())
        self.tn1_name.set(self.tn2_name.get())
        self.tn2_name.set(tempp.get())
        self.focus_set()
        # print(self.focus_get())


    def set_tournier_name(self):
        self.focus_set()
        input_window = InputWindow(self, "Tournier, Gruppe")
        input_window.wait_window()

    
    def score_plus(self, score: IntVar, quant: int):
        # if str(self.tn1_entry.focus_get()) != ".!mainframe.!entry" and str(self.tn1_entry.focus_get()) != ".!mainframe.!entry2":
        i = score.get()
        i+= quant
        score.set(i)
        self.focus_set()
    
    def score_minus(self, score: IntVar, quant: int):
        # if str(self.tn1_entry.focus_get()) != ".!mainframe.!entry" and str(self.tn1_entry.focus_get()) != ".!mainframe.!entry2":
        i = score.get()
        i-= quant
        score.set(i)
        self.focus_set()

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
        # i = 5
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
        # global entered_line
        self.entered_line = self.input_line.get()
        self.parent.tournier_name.set(self.entered_line)
        self.destroy()



root = MainWindow()
root.mainloop()


