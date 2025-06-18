import os
import sqlite3
from datetime import datetime
from login import loging
from admin import show_admin_panel
from data import save, edit, delete, setup_right_click_handler
from about import show_about
from settings import show_settings, del_all_windows, open_windows
from sort import setup_sorting
from tkinter import *
from encoding import *
from tkinter import ttk
from lang import main_ru, main_en
from theme import apply_theme
from language import load_language, load_theme

dirname = os.path.dirname(__file__)
os.chdir(dirname)

if not os.path.exists("log"):
    os.mkdir("log")

now = datetime.now()
name = now.strftime("%d.%m.%Y_%H.%M.%S")

log_file = open(rf"log\log_{name}.txt", "w", encoding="utf-8")

connection = sqlite3.connect("base.db")
cursor = connection.cursor()


def on_closing(tk):
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Программа завершила работу")
    log_file.close()
    connection.close()
    tk.destroy()


def handle_enter(event, table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor):
    widget = event.widget
    if widget == FIO_Entry:
        HIM1_Combobox.focus_set()
    elif widget == HIM1_Combobox:
        HIM2_Combobox.focus_set()
    elif widget == HIM2_Combobox:
        HIM_Combobox.focus_set()
    elif widget == HIM_Combobox:
        PRICE_Entry.focus_set()
    elif widget == PRICE_Entry:
        save(table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor)


def main_window(access):
    
    user = "admin" if access == "a" else ("manager" if access == "b" else "user")
    
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Программа начала работу. Пользователь: {user}\n")
    
    global open_windows, tk
    lang = main_ru if load_language() == "ru" else main_en
    
    tk = Tk()
    
    open_windows[tk] = lambda: main_window(access)
        
    tk.title(lang[0])
    tk.geometry("1200x800+300+100")
    tk.protocol("WM_DELETE_WINDOW", lambda: on_closing(tk))
    
    
    spravka_menu = Menu(tearoff=0)
    if access == "a":
        spravka_menu.add_command(label=lang[1], command=lambda: show_admin_panel(log_file, connection))
    spravka_menu.add_command(label=lang[2], command=lambda:show_about(log_file))
    
    exit_menu = Menu(tearoff=0)
    exit_menu.add_command(label=lang[15], command=lambda: restart())
    exit_menu.add_command(label=lang[16], command=lambda: del_all_windows())
    
    main_menu = Menu()
    main_menu.add_command(label=lang[3],command=lambda:show_settings(log_file))
    main_menu.add_cascade(label=lang[4], menu=spravka_menu)
    main_menu.add_cascade(label=lang[14], menu=exit_menu)
 
    tk.config(menu=main_menu)

    him_el1 = ["Натрий", "Магний", "Алюминий", "Кремний", "Фосфор", "Сера", "Хлор", "Аргон", "Калий", "Кальций"]
    him_el2 = ["Скандий", "Титан", "Ванадий", "Хром", "Марганец", "Железо", "Кобальт", "Никель", "Медь", "Цинк"]
    him_proc = ["Горение", "Фотосинтез", "Электролиз", "Ферментация", "Нейтрализация", "Окисление металлов", "Каталитический крекинг", "Полимеризация", "Гидролиз", "Дистилляция"]

    new_work = LabelFrame(tk, text=lang[5], font=("Arial", 15))
    FIO_Label = Label(new_work, text=lang[6], font=("Arial", 13))
    FIO_Entry = Entry(new_work)
    HIM1_Label = Label(new_work, text=lang[7], font=("Arial", 13))
    HIM2_Label = Label(new_work, text=lang[8], font=("Arial", 13))
    HIM_PROC = Label(new_work, text=lang[17], font=("Arial", 13))
    HIM_Combobox = ttk.Combobox(new_work, values=him_proc)
    HIM1_Combobox = ttk.Combobox(new_work, values=him_el1)
    HIM2_Combobox = ttk.Combobox(new_work, values=him_el2)
    PRICE_Label = Label(new_work, text=lang[9], font=("Arial", 13))
    PRICE_Entry = Entry(new_work)
    SAVE = Button(new_work, text=lang[10], command=lambda: save(table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox,
                                                                PRICE_Entry, log_file, connection, cursor), font=("Arial", 13))
    UPDATE = Button(new_work, text=lang[11], command=lambda: edit(table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox,
                                                                    PRICE_Entry, SAVE, log_file, connection,
                                                                    cursor, UPDATE, DELETE, lang), font=("Arial", 13))
    DELETE = Button(new_work, text=lang[12], command=lambda: delete(table, log_file, connection, cursor), font=("Arial", 13))
    
    if access == "c":
        SAVE.config(state=DISABLED)
        UPDATE.config(state=DISABLED)
        DELETE.config(state=DISABLED)

    FIO_Label.place(x=10, y=10)
    HIM1_Label.place(x=10, y=50)
    HIM2_Label.place(x=10, y=90)
    HIM_PROC.place(x=10, y=130)
    PRICE_Label.place(x=10, y=170)

    FIO_Entry.place(x=120, y=10, width=200)
    HIM1_Combobox.place(x=180, y=50)
    HIM2_Combobox.place(x=180, y=90)
    HIM_Combobox.place(x=180, y=130)
    PRICE_Entry.place(x=180, y=175)

    SAVE.place(x=10, y=210)
    UPDATE.place(x=10, y=260)
    DELETE.place(x=120, y=260)
    new_work.place(x=20, y=20, width=370, height=350)

    if access in ("a", "b"):
        FIO_Entry.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor))
        HIM1_Combobox.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor))
        HIM2_Combobox.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor))
        HIM_Combobox.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor))
        PRICE_Entry.bind('<Return>', lambda e: handle_enter(e, table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor))


    columns = ("ID", "FIO", "him_1", "him_2", "him_proc", "price", "datePriem")
    table = ttk.Treeview(tk, columns=columns, show="headings")
    table.heading("ID", text="Id", anchor="center")
    table.heading("FIO", text=lang[6], anchor="center")
    table.heading("him_1", text=lang[7], anchor="center")
    table.heading("him_2", text=lang[8], anchor="center")
    table.heading("him_proc", text=lang[17], anchor="center")
    table.heading("price", text=lang[9], anchor="center")
    table.heading("datePriem", text=lang[13], anchor="center")
    table.column("ID", width=15, anchor="w")
    table.column("FIO", width=220, anchor="w")
    table.column("him_1", width=100, anchor="w")
    table.column("him_2", width=100, anchor="w")
    table.column("him_proc", width=100, anchor="w")
    table.column("price", width=75, anchor="w")
    table.column("datePriem", width=75, anchor="w")

    table.place(x=400, y=33, width=785, height=750)

    cursor.execute("SELECT * FROM tab_1;")

    pipls=cursor.fetchall()
    connection.commit()

    for data in pipls:
        new_zayav = []
        for i in data:
            new_zayav.append(rev_cezar(str(i)) if data.index(i) != 0 else str(i))

        table.insert("", END, values=new_zayav)


    setup_sorting(table)
    if access in ('a', 'b'):
        setup_right_click_handler(table, cursor, connection, log_file, lang[12
        ])

    apply_theme(tk, load_theme())
    
    tk.mainloop()


def start():
    a = loging(log_file)
    if a in ('a', 'b', 'c'):
        main_window(a)

def restart():
    del_all_windows()
    start()
    log_file.write(f"{datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Выполнен выход из аккаунта\n")
    
if __name__ == "__main__":
    start()