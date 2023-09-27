import pyautogui
import pygetwindow as gw
from tkinter import *
from threading import Thread
from time import sleep


def is_word_document_active_and_mouse_inside():
    
    active_window = gw.getActiveWindow()

    if active_window is not None and "Word" in active_window.title:
        x, y = pyautogui.position()
        word_window = active_window

        if (word_window.left <= x <= word_window.left + word_window.width and
                word_window.top <= y <= word_window.top + word_window.height):
            return True
    return False


def display():
    while True:
        if is_word_document_active_and_mouse_inside():
            mouse_field.delete(0, END)
            mouse_field.insert(0, "Inside")
        else:
            mouse_field.delete(0, END)
            mouse_field.insert(0, "Outside")
        sleep(0.01)


window = Tk()

mouse_field = Entry(window)
mouse_field.pack()

Thread(target = display).start()

window.mainloop()
