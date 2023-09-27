import cv2
import mediapipe as mp
import pyautogui
from tkinter import *
from threading import Thread
from time import sleep

pyautogui.FAILSAFE = False
firstMove = True
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

calibrated = False

def display():
    global calibrated
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
                        if not calibrated:
                            x_mid = screen_x
                            y_mid = screen_y
                            calibrated = True
                            sleep(3)
                        else:
                            print(screen_x, screen_y)
                            if screen_x < x_mid - 75:
                                eye_field.delete(0, END)
                                eye_field.insert(0, "Looking left")
                            elif screen_x > x_mid + 75:
                                eye_field.delete(0, END)
                                eye_field.insert(0, "Looking right")
                            elif screen_y > y_mid + 45:
                                eye_field.delete(0, END)
                                eye_field.insert(0, "Looking down")
                            elif screen_y < y_mid - 45:
                                eye_field.delete(0, END)
                                eye_field.insert(0, "Looking up")
                            else:
                                eye_field.delete(0, END)
                                eye_field.insert(0, "Looking straight")
                left = [landmarks[145], landmarks[159]]
                for landmark in left:
                    x = int(landmark.x * frame_w)
                    y = int(landmark.y * frame_h)
                    cv2.circle(frame, (x, y), 3, (0, 255, 255))
            cv2.imshow('Eye Monitor', frame)
            cv2.waitKey(1)
        except Exception as e:
            print(e)

window = Tk()

eye_field = Entry(window)
eye_field.pack()

Thread(target = display).start()

window.mainloop()
