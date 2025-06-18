import sqlite3
from tkinter import *
from tkinter import ttk
from data_users import *
from sort import setup_sorting
from settings import open_windows
from theme import apply_theme
from language import load_language, load_theme
from lang import admin_ru, admin_en
from datetime import datetime


def show_admin_panel(log_file, connection):
    global open_windows
    
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Открыто окно 'Администрирование'\n")
    
    lang = admin_ru if load_language() == "ru" else admin_en
    
    cursor = connection.cursor()
    admin_panel = Tk()
    
    open_windows[admin_panel] = lambda: show_admin_panel(log_file, connection)
    
    admin_panel.title(lang[0])
    admin_panel.geometry("900x400+300+100")
    
    NAME_Label = Label(admin_panel, text=lang[1], font=("Arial", 13))
    PASSWORD_Label = Label(admin_panel, text=lang[2], font=("Arial", 13))
    ACCESS_Label = Label(admin_panel, text=lang[3], font=("Arial", 13))
    NAME_Entry = Entry(admin_panel, font=("Arial", 13))
    PASSWORD_Entry = Entry(admin_panel, font=("Arial", 13))
    ACCESS_Combobox = ttk.Combobox(admin_panel, values=("a", "b", "c"))
    
    SAVE = Button(admin_panel, text=lang[4], command=lambda: save(table, NAME_Entry, PASSWORD_Entry, ACCESS_Combobox, log_file, connection, cursor), font=("Arial", 13))
    UPDATE = Button(admin_panel, text=lang[5], command=lambda: edit(table, NAME_Entry, PASSWORD_Entry, ACCESS_Combobox,SAVE, log_file, connection, cursor, UPDATE, DELETE), font=("Arial", 13))
    DELETE = Button(admin_panel, text=lang[6], command=lambda: delete(table, log_file, connection, cursor), font=("Arial", 13))
    # BLOCKED = Button(admin_panel,text=lang[7],command= lambda:  ())

    NAME_Label.place(x=10, y=30)
    PASSWORD_Label.place(x=10, y=70)
    ACCESS_Label.place(x=10, y=110)
    NAME_Entry.place(x=140, y=30)
    PASSWORD_Entry.place(x=140, y=70)
    ACCESS_Combobox.place(x=140, y=110)
    
    SAVE.place(x=10, y=150)
    UPDATE.place(x=110, y=150)
    DELETE.place(x=10, y=190)
    # BLOCKED.place(x=110,y=190)
    
    columns = ("ID", "NAME", "PASSWORD", "ACCESS")
    table = ttk.Treeview(admin_panel, columns=columns, show="headings")
    table.heading("ID", text="id", anchor="center")
    table.heading("NAME", text=lang[1], anchor="center")
    table.heading("PASSWORD", text=lang[2], anchor="center")
    table.heading("ACCESS", text=lang[3])
    
    table.column("ID", width=10, anchor="w")
    table.column("NAME", width=50, anchor="w")
    table.column("PASSWORD", width=75, anchor="w")
    table.column("ACCESS", width=100, anchor="w")

    table.place(x=380, y=33, width=500, height=350)

    cursor.execute("SELECT * FROM users;")

    pipls=cursor.fetchall()
    connection.commit()

    for data in pipls:
        table.insert("", END, values=data)

    setup_sorting(table)
    
    apply_theme(admin_panel, load_theme())

    admin_panel.mainloop()