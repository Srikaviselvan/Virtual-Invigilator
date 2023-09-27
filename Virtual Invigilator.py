import pygetwindow as gw
from tkinter import *
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
import cv2
import mediapipe as mp
import pyautogui
from time import sleep



def center_window(window):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the x and y coordinates to center the window
    x = (screen_width - window.winfo_reqwidth()) / 2
    y = (screen_height - window.winfo_reqheight()) / 2

    # Set the window's geometry to center it
    window.geometry("+%d+%d" % (x, y))


# Count number of browsers open
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


# Count chat applications open
def is_app_open(app_name):
    for window in gw.getAllTitles():
        if app_name.lower() in window.lower():
            return True
    return False

apps_to_check = ["Discord", "Instagram", "WhatsApp", "Telegram"]


# Display number of browsers
def display_browsers(loop = True, prompt = False):
    global browser_field
    if loop:
        while True:

            browsers = []

            for name in browser_names:
                browsers.append(count_browsers(name))
            
            string = ""

            for i in range(len(browsers)):
                if browsers[i] > 0:
                    string += f"{browser_names[i]} : {browsers[i]} browsers" + '\n'
            
            if browsers[0] > 1 or sum(browsers[1:]) > 0:
                string += "Close other browsers"
            
            browser_field.delete(1.0, END)
            browser_field.insert("insert", string)
    
    else:
        browsers = []

        for name in browser_names:
            browsers.append(count_browsers(name))
        
        string = ""

        for i in range(len(browsers)):
            if browsers[i] > 0:
                string += f"{browser_names[i]} : {browsers[i]} browsers" + '\n'
        
        if browsers[0] > 1 or sum(browsers[1:]) > 0:
            string += "Close other browsers\n"
        
        if not prompt:
            return string
        else:
            return sum(browsers)


# Display chat applications
def display_chat_apps(loop = True, prompt = False):
    global apps_to_check
    if loop:
        while True:
            string = ""
            for app_name in apps_to_check:
                if is_app_open(app_name):
                    string += app_name + " is opened\n"
            if len(string) > 0:
                string += "Close chat applications"
            chat_apps_field.delete(1.0, END)
            chat_apps_field.insert("insert", string)
    else:
        string = ""
        for app_name in apps_to_check:
            if is_app_open(app_name):
                string += app_name + " is opened\n"
        if len(string) > 0:
            string += "Close chat applications\n"
        
        if not prompt:
            return string
        else:
            return len(string)



# Close newly opened tabs in chrome
def close_new_tabs():
    global driver
    original_tab = driver.window_handles[0]
    for tab in driver.window_handles[1:]:
        driver.switch_to.window(tab)
        driver.close()


# Initialize chrome driver
def chrome_driver():
    try:
        global driver
        chrome_driver_path = r"C:\Users\srika\Downloads\chromedriver-win32\chromedriver-win32\chromedriver.exe"
        
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--disable-web-security')


        chrome_service = ChromeService(executable_path=chrome_driver_path)

        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        driver.get("https://www.youtube.com")
        driver.execute_script("window.open('');")

        driver.switch_to.window(driver.window_handles[0])


        while True:
            try:
                close_new_tabs()
            except:
                pass
    except:
        pass


def calibrate_eye_position():
    calibrate_window.destroy()
    global x_mid, y_mid
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()
    for _ in range(100):
        _, frame = cam.read()
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        frame_h, frame_w, _ = frame.shape
        if landmark_points:
            landmarks = landmark_points[0].landmark
            for id, landmark in enumerate(landmarks[474:478]):
                x = int(landmark.x * frame_w)
                y = int(landmark.y * frame_h)
                cv2.circle(frame, (x, y), 3, (0, 255, 0))
                if id == 1:
                    screen_x = screen_w * landmark.x
                    screen_y = screen_h * landmark.y
                    x_mid = screen_x
                    y_mid = screen_y
            cv2.imshow("LOOK AT YOUR SCREEN", frame)
        cv2.waitKey(1)
    cv2.destroyAllWindows()


# Display eye position
def display_eye_position():
    global calibrated, cam, screen_w, screen_h, face_mesh, eye_position_field
    pyautogui.FAILSAFE = False
    cam = cv2.VideoCapture(0)
    face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
    screen_w, screen_h = pyautogui.size()

    eye_position_field.delete(0, END)
    eye_position_field.insert(0, "Look at your screen")

    while True:
        try:
            _, frame = cam.read()
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                for id, landmark in enumerate(landmarks[474:478]):
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 0))
                    if id == 1:
                        screen_x = screen_w * landmark.x
                        screen_y = screen_h * landmark.y
                        if screen_x < x_mid - 75:
                            eye_position_field.delete(0, END)
                            eye_position_field.insert(0, "Looking left")
                        elif screen_x > x_mid + 75:
                            eye_position_field.delete(0, END)
                            eye_position_field.insert(0, "Looking right")
                        elif screen_y > y_mid + 45:
                            eye_position_field.delete(0, END)
                            eye_position_field.insert(0, "Looking down")
                        elif screen_y < y_mid - 45:
                            eye_position_field.delete(0, END)
                            eye_position_field.insert(0, "Looking up")
                        else:
                            eye_position_field.delete(0, END)
                            eye_position_field.insert(0, "Looking straight")
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
            cv2.waitKey(1)
        except Exception as e:
            pass


# Checks if Word is active and mouse is inside Chrome window
def is_word_active_and_mouse_inside():
    
    active_window = gw.getActiveWindow()

    if active_window is not None and "Chrome" in active_window.title:
        x, y = pyautogui.position()
        word_window = active_window

        if (word_window.left <= x <= word_window.left + word_window.width and
                word_window.top <= y <= word_window.top + word_window.height):
            return True
    return False


# Display mouse position
def display_mouse_position():
    while True:
        if is_word_active_and_mouse_inside():
            mouse_position_field.delete(0, END)
            mouse_position_field.insert(0, "Inside Chrome")
        else:
            mouse_position_field.delete(0, END)
            mouse_position_field.insert(0, "Outside Chrome")
        sleep(0.01)



# Start Exam Function
def start_exam():
    open = display_browsers(loop = False, prompt = True) + display_chat_apps(loop = False, prompt = True)
    if open == 0:
        button.destroy()
        win.destroy()
        Thread(target = chrome_driver).start()
        Thread(target = create_tkinter_window).start()


# Create tkinter window to display all information
def create_tkinter_window():
    global browser_field, chat_apps_field, eye_position_field, mouse_position_field, button
    window = Tk()
    window.configure(bg = 'blue')

    browser_label = Label(window, text = "Browsers open :", bg = 'black', fg = 'white').pack()
    browser_field = Text(window, width=40, height=10)
    browser_field.pack(padx = 5, pady = 5)

    chat_apps_label = Label(window, text = "Chat applications open :", bg = 'black', fg = 'white').pack()
    chat_apps_field = Text(window, width=40, height=10)
    chat_apps_field.pack(padx = 5, pady = 5)

    eye_position_label = Label(window, text = "Eye position :", bg = 'black', fg = 'white').pack()
    eye_position_field = Entry(window)
    eye_position_field.pack(padx = 5, pady = 5)

    mouse_position_label = Label(window, text = "Mouse position :", bg = 'black', fg = 'white').pack()
    mouse_position_field = Entry(window)
    mouse_position_field.pack(padx = 5, pady = 5)

    Thread(target = display_browsers).start()
    Thread(target = display_chat_apps).start()
    Thread(target = display_mouse_position).start()
    Thread(target = display_eye_position).start()

    window.focus_force()

    window.mainloop()


def prompt_user():
    global win, instructions_field, button
    win = Tk()
    win.geometry('500x200')
    win.configure(bg = 'blue')
    center_window(win)

    Label(win, bg = 'blue').pack(pady = 5)
    instructions_label = Label(win, text = "INSTRUCTIONS", bg = 'black', fg = 'white').pack(pady = 5, padx = 10)
    instructions_field = Text(win, width=70, height=2, bg = 'white', fg = 'black')
    instructions_field.pack(pady = 5, padx = 10)


    button = Button(win, text = "Start Exam", command = start_exam, bg = 'black', fg = 'white')
    button.pack(pady = 5, padx = 10)

    string = "Close all browsers and Click on 'Start Exam' to continue"

    instructions_field.insert('insert', string)

    win.focus_force()

    win.mainloop()


def login():
    global calibrate_window
    user_id = user_id_entry.get()
    password = password_entry.get()

    if user_id == '123' and password == '123':
        login_window.destroy()
        calibrate_window = Tk()
        calibrate_window.configure(bg = 'blue')
        calibrate_window.geometry('200x100')
        center_window(calibrate_window)
        Label(calibrate_window, bg = 'blue').pack(pady = 2)
        Label(calibrate_window, text = "Look at the screen", bg = 'white', fg = 'black').pack(padx = 10)
        Button(calibrate_window, text = "Calibrate eye position", command = calibrate_eye_position, bg = 'black', fg = 'white').pack(padx = 10, pady = 10)
        calibrate_window.mainloop()
        prompt_user()
        


def login_tkinter():
    global login_window, user_id_entry, password_entry
    login_window = Tk()
    center_window(login_window)
    login_window.geometry('300x200')
    login_window.configure(bg = 'blue')

    Label(bg = 'blue').pack(padx = 10)
    user_id_label = Label(login_window, text = "User ID :", bg = 'black', fg = 'white').pack()
    user_id_entry = Entry(login_window)
    user_id_entry.pack(padx = 10, pady = 10)

    password_label = Label(login_window, text = "Password :", bg = 'black', fg = 'white').pack()
    password_entry = Entry(login_window)
    password_entry.pack( padx = 10, pady = 10)

    login_button = Button(login_window, text = "Login", bg = 'black', fg = 'white', command = login)
    login_button.pack( padx = 10, pady = 10)

    login_window.mainloop()




# Main Function:
login_tkinter()
