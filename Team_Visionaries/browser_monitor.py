import psutil
import pygetwindow as gw
from tkinter import *
from threading import Thread


def count_browsers(window_title):
    try:
        window_names = gw.getAllTitles()
        window_names_2 = []

        for window_name in window_names:
            if window_title in window_name:
                window_names_2.append(window_name)

        return len(window_names_2)
    except:
        pass

browser_names = ['Chrome', 'Firefox', 'Edge', 'Brave', 'Opera']

def display():
    while True:

        browsers = []

        for name in browser_names:
            browsers.append(count_browsers(name))
        
        string = ""

        for i in range(len(browsers)):
            if browsers[i] > 0:
                string += f"{browser_names[i]} : {browsers[i]} browsers" + '\n'
        
        browser_field.delete(1.0, END)
        browser_field.insert("insert", string)

window = Tk()

browser_field = Text(window, width=40, height=10)
browser_field.pack()

Thread(target = display).start()

window.mainloop()
