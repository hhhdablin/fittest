import os
import sqlite3
import hashlib

def coding_password(password):
    return str(hashlib.sha256(password.encode("utf-8")).digest())

def check_password(name, entry_password):
    dirname=os.path.dirname(__file__)
    os.chdir(dirname)
    connection = sqlite3.connect("base.db")
    cursor = connection.cursor()
    if coding_password(entry_password) == cursor.execute("SELECT password FROM users WHERE name = ?", (name, )).fetchall()[0][0]:
        return True
    return False

def cezar(s):
    text = ''
    for i in str(s):
        text += chr(ord(i) + 25)
    return text

def rev_cezar(str):
    text = ''
    for i in str:
        text += chr(ord(i) - 25)
    return text
