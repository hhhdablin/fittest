import datetime
from tkinter import *
from encoding import *
from tkinter.ttk import Treeview

def save(table, FIO_Entry, HIM1_COmbobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor):

    name = FIO_Entry.get()
    him1 = HIM1_COmbobox.get()
    him2 = HIM2_Combobox.get()
    him = HIM_Combobox.get()
    price = PRICE_Entry.get()
    cursor.execute(
        'INSERT INTO tab_1(name, him_el1, him_el2, him_proc, price, date) VALUES (?, ?, ?, ?, ?, ?);', (cezar(name), cezar(him1), cezar(him2), cezar(him), cezar(price), cezar(datetime.date.today())))
    connection.commit()
    for item in table.get_children():
        table.delete(item)
    cursor.execute("SELECT * FROM tab_1;")
    zayavki = cursor.fetchall()
    connection.commit()
    for zayav in zayavki:
        new_zayav = []
        for i in zayav:
            new_zayav.append(rev_cezar(str(i)) if zayav.index(i) != 0 else str(i))
        table.insert("", END, values=new_zayav)

    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запись {table.get_children()[-1]} сохранена \n")
    FIO_Entry.delete(0, END)
    HIM1_COmbobox.delete(0, END)
    HIM2_Combobox.delete(0, END)
    HIM_Combobox.delete(0, END)
    PRICE_Entry.delete(0, END)


def edit(table, FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, SAVE, log_file, connection, cursor, UPDATE, DELETE, lang):
    id = table.selection()
    if not id:
        return


    FIO_Entry.insert(0, table.item(id)["values"][1])
    HIM1_Combobox.insert(0, table.item(id)["values"][2])
    HIM2_Combobox.insert(0, table.item(id)["values"][3])
    HIM_Combobox.insert(0, table.item(id)["values"][4])
    PRICE_Entry.insert(0, table.item(id)["values"][5])

    SAVE.config(text=lang[18], command=lambda: update(table, SAVE, id,
                                                           FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry,
                                                           log_file, connection, cursor, UPDATE, DELETE, lang))
    UPDATE.config(state=DISABLED)
    DELETE.config(state=DISABLED)

    

def update(table, SAVE, id,
           FIO_Entry, HIM1_Combobox, HIM2_Combobox, HIM_Combobox, PRICE_Entry, log_file, connection, cursor, UPDATE, DELETE, lang):
    name = FIO_Entry.get()
    him1 = HIM1_Combobox.get()
    him2 = HIM2_Combobox.get()
    him = HIM_Combobox.get()
    price = PRICE_Entry.get()

    cursor.execute("UPDATE tab_1 SET name = ?, him_el1 = ?, him_el2 = ?, him_proc = ?, price = ?, date = ? WHERE ID = ?;", (cezar(name), cezar(him1), cezar(him2), cezar(him), cezar(price), cezar(datetime.date.today()), table.item(id[0])['values'][0]))
    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запись {id[0]} изменена \n")
    connection.commit()
    for item in table.get_children():
        table.delete(item)
    cursor.execute("SELECT * FROM tab_1;")
    zayavki = cursor.fetchall()
    connection.commit()
    for zayav in zayavki:
        new_zayav = []
        for i in zayav:
            new_zayav.append(rev_cezar(str(i)) if zayav.index(i) != 0 else str(i))
        table.insert("", END, values=new_zayav)
    FIO_Entry.delete(0, END)
    HIM1_Combobox.delete(0, END)
    HIM2_Combobox.delete(0, END)
    HIM_Combobox.delete(0, END)
    PRICE_Entry.delete(0, END)
    SAVE.config(text=lang[10], command=lambda: save(table, FIO_Entry, HIM1_Combobox, HIM2_Combobox,
                                                       HIM_Combobox, PRICE_Entry, log_file, connection, cursor))
    UPDATE.config(state=NORMAL)
    DELETE.config(state=NORMAL)

def delete(table: Treeview, log_file, connection, cursor):

    id = table.selection()
    id_data = table.item(id)["values"][0]
    cursor.execute("DELETE FROM tab_1 WHERE ID = ?", (id_data,))
    connection.commit()
    for item in table.get_children():
        table.delete(item)

    cursor.execute("SELECT * FROM tab_1;")
    zayavki = cursor.fetchall()
    connection.commit()
    for zayav in zayavki:
        new_zayav = []
        for i in zayav:
            new_zayav.append(rev_cezar(str(i)) if zayav.index(i) != 0 else str(i))
        table.insert("", END, values=new_zayav)

    log_file.write(f"{datetime.datetime.now().strftime('%d.%m.%Y_%H.%M.%S')}: Запись {id[0]} удалена \n")
    
def setup_right_click_handler(table, cursor, connection, log_file, lang):
    
    def on_right_click(event):
        item = table.identify_row(event.y)
        if item:
            table.selection_set(item)
            show_context_menu(event)
    
    def show_context_menu(event):
        menu = Menu(table, tearoff=0)
        menu.add_command(
            label=lang,
            command=lambda: delete(table, log_file, connection, cursor)
        )
        menu.post(event.x_root, event.y_root)
    
    table.bind("<Button-3>", on_right_click)