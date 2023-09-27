import pygetwindow as gw
from tkinter import *
from threading import Thread

def is_app_open(app_name):
    for window in gw.getAllTitles():
        if app_name.lower() in window.lower():
            return True
    return False

apps_to_check = ["Discord", "Instagram", "WhatsApp", "Telegram"]

def display():
    global apps_to_check
    while True:
        string = ""
        for app_name in apps_to_check:
            if is_app_open(app_name):
                string += app_name + " is opened\n"
        chat_apps_field.delete(1.0, END)
        chat_apps_field.insert("insert", string)

window = Tk()

chat_apps_field = Text(window, width=40, height=10)
chat_apps_field.pack()

Thread(target = display).start()

window.mainloop()