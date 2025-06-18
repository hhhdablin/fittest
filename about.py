from tkinter import messagebox
from tkinter import Toplevel, Label
from datetime import datetime
from theme import apply_theme
from language import load_language, load_theme
from lang import about_ru, about_en
from settings import open_windows

def show_about(log_file):
    global open_windows
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Открыто окно 'О программе'\n")
    
    lang = about_ru if load_language() == "ru" else about_en
    
    about_window = Toplevel()
    
    open_windows[about_window] = lambda: show_about(log_file)
    
    about_window.title(lang[0])
    about_window.geometry("400x150+500+300")
    
   
    Label(about_window, text=lang[1], font=("Arial", 16, "bold")).pack(pady=10)
    Label(about_window, text=lang[2], font=("Arial", 12)).pack()

    Label(about_window, text=lang[3], font=("Arial", 10)).pack(side="bottom", pady=10)
    
    apply_theme(about_window, load_theme())