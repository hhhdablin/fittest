import os
import sqlite3
from encoding import *

dirname=os.path.dirname(__file__)
os.chdir(dirname)

connection = sqlite3.connect("base.db")
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tab_1(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,  him_el1 TEXT, him_el2 TEXT, him_proc TEXT, price TEXT, date TEXT)")

zayavki = [
    ("Брылев Тимофей", "Магний", "Кальций", "Горение", 20000, "2025-06-20")
]
for z in zayavki:
    cursor.execute("INSERT INTO tab_1 (name, him_el1, him_el2, him_proc, price, date) VALUES (?, ?, ?, ?, ?, ?)", (cezar(z[0]), cezar(z[1]), cezar(z[2]), cezar(z[3]), cezar(z[4]), cezar(z[5])))

cursor.execute("CREATE TABLE IF NOT EXISTS users(ID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, access TEXT)")

users = (("admin", "admin", "a"), ("manager", "manager", "b"), ("user", "", "c"))

cursor.executemany("INSERT INTO users (name, password, access) VALUES (?, ?, ?)", users)

connection.commit()
connection.close()