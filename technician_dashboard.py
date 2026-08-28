from logging import root
import tkinter as tk
from tkinter import ttk

class TechnicianDashboard(tk.Frame):
    def __init__(self,main,techname):  #tk Frame acts as the parent class for AdminDashboard, inheritting it's functions!
        self.main = main
        self.techname = techname
        #use of self.main because main is or window dashboard

        self.main.title(f"Gridcare-Lite - Hello, Technician {self.techname}")
        self.main.geometry("800x600")
        self.main.configure(bg="#36c0ad") #configure for the background color
        self.main.resizable(False, False) #to avoid resizing the window's height and width


        #creating window widgets
        #self.title_label =ttk.Label(
        #    self.main,text = f"Welcome Admin {self.adminame}", font=('Helvetica', 16), background="#414e8f", foreground="white"
        #   )
        #self.title_label.pack(pady=20)
        #t.k uses bg and fg while ttk uses background and foreground

        self.sidebar_frame = tk.Frame(
            self.main, bg="#0d4b3f", width=200
            )
        self.sidebar_frame.pack(side="left", fill="y") # be at the left, fill the whole height of window
        #every method in this class has access to the side bar

        self.main_frame = tk.Frame(
            self.main, bg="#36c0ad"
            )
        self.main_frame.pack(side="right", fill="both", expand=True) #filling the rest of the window and expanding to fill the rest of the space

        self.heading = ttk.Label(
            self.main_frame, text=f"Welcome Admin {self.adminame}", font=('Helvetica', 16), background="#36c0ad", foreground="white")
        self.heading.pack()
'''
main = tk.Tk()
dashboard = TechnicianDashboard(main, "Eugenia") #ok, username has to be gotten from the login window but hard coded for now/

main.mainloop()
'''