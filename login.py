import os

import sqlite3
import datetime
from tkinter import *
from encoding import *
from tkinter import ttk
from tkinter import messagebox
from language import load_language, load_theme
from lang import login_ru, login_en
from theme import apply_theme

access = ""
lang = []

users = {}

def check(name, password, login):
    global access
    if name.get() in list(users):
        if users[name.get()][0] == password.get():
            access = users[name.get()][1]
            login.destroy()
        else:
            messagebox.showerror(lang[5], lang[6])
    else:
        messagebox.showerror(lang[5], lang[7])
            

def loging(log_file):
    global users, lang

    lang = login_ru if load_language() == "ru" else login_en
    
    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запущено окно авторизации\n")
    
    dirname=os.path.dirname(__file__)
    os.chdir(dirname)

    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()
    
    for i in cursor.execute("SELECT * FROM users").fetchall():
        users[i[1]] = (i[2], i[3])

    login = Tk()

    login.geometry("400x300+500+300")
    login.resizable(False, False)
    login.title(lang[0])

    label = Label(login, text=lang[1], font=("Arial", 18))
    name_ladel = Label(login, text=lang[2], font=("Arial", 14))
    password_ladel = Label(login, text=lang[3], font=("Arial", 14))

    name = ttk.Combobox(login, values=list(users), font=("Arial", 14))
    password = Entry(login, font=("Arial", 14), show="*")
    
    name.bind("<Return>", lambda event: password.focus())
    password.bind("<Return>", lambda event: check(name, password, login))

    go = Button(login, font=("Arial", 14), command=lambda: check(name, password, login), text=lang[4])

    label.place(x=10, y=10)
    name_ladel.place(x=10, y=60)
    password_ladel.place(x=10, y=110)
    name.place(x=150, y=60)
    password.place(x=150, y=110)
    go.place(x=150, y=160)
    
    apply_theme(login, load_theme())

    login.mainloop()
    
    return access
