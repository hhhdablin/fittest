import json
from tkinter import ttk
from tkinter import *
from datetime import datetime
from language import load_language, load_theme
from theme import apply_theme
from lang import settings_ru, settings_en

open_windows = {}

def update_all_windows(log_file, new_lang):
    global open_windows
    windows_to_update = open_windows.copy()
    open_windows.clear() 
    
    for window, recreate_func in windows_to_update.items():
        try:
            if window.winfo_exists():
                window.destroy()
            recreate_func()  
        except TclError:
            recreate_func()
            
def del_all_windows():
    global open_windows
    windows_to_del = open_windows.copy()
    open_windows.clear()
    for window, recreate_func in windows_to_del.items():
        try:
            if window.winfo_exists():
                window.destroy()
        except TclError:
            print("Error!")

def save(lan, theme, settings_window, log_file):
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            lang_data = json.load(f)
            new_lang = "ru" if lan.get() == "Русский" else "en"
            new_theme = "l" if (theme.get() in ("Светлая", "Light")) else "d"
            lang_data["language"] = new_lang
            lang_data["theme"] = new_theme
        
        
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(lang_data, f, ensure_ascii=False, indent=4)
        
        
        log_file.write(f"{datetime.now()}: Настройки сохранены (язык: {new_lang}, тема: {new_theme})\n")
        
        if settings_window in open_windows:
            del open_windows[settings_window]
        
        update_all_windows(log_file, new_lang)
        
        settings_window.destroy()
        
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Ошибка при сохранении настроек: {e}")

def show_settings(log_file):
    
    global open_windows
    
    current_language = load_language()  
    current_theme = load_theme()       
    
    lang = settings_ru if current_language == "ru" else settings_en
    
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Открыто окно 'Настройки'\n")

    settings_window = Toplevel()
    
    open_windows[settings_window] = lambda: show_settings(log_file)
        
    settings_window.title(lang[0])
    settings_window.geometry("500x400+500+300")
    
    Label(settings_window, text=lang[1], font=("Arial", 13)).place(x=10, y=10)
    Label(settings_window, text=lang[2], font=("Arial", 13)).place(x=10, y=40)
    
    language_values = ("Русский", "English")
    theme_values = (lang[3], lang[4]) 
    
    lan = ttk.Combobox(settings_window, values=language_values)
    theme = ttk.Combobox(settings_window, values=theme_values)
    
    lan.set("Русский" if current_language == "ru" else "English")
    theme.set(lang[3] if current_theme == "l" else lang[4]) 
    
    lan.place(x=150, y=10)
    theme.place(x=150, y=40)
    Button(settings_window, text=lang[5], command=lambda: save(lan, theme, settings_window, log_file), font=("Arial", 13)).place(x=10, y=70)
    
    apply_theme(settings_window, load_theme())