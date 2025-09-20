import tkinter as tk
from tkinter import filedialog
import threading
import time
import random
import json
import os
from PIL import Image, ImageTk
from pynput import keyboard
from tkinter import ttk
import win32api
import win32con

settings_file = "settings.json"

left_cps = 0
clicking_left = False

def left_clicker():
    while True:
        if clicking_left:
            current_cps = max(1, random.uniform(left_cps - 3, left_cps + 3))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(1 / current_cps)
        else:
            time.sleep(0.01)

def on_key_press(key):
    global clicking_left
    try:
        if key.char == 'g':
            clicking_left = True
        elif key.char == 'h':
            clicking_left = False
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_key_press)
listener.start()

def save_settings(bg_path):
    with open(settings_file, 'w') as f:
        json.dump({"background": bg_path}, f)

def load_settings():
    if os.path.exists(settings_file):
        with open(settings_file, 'r') as f:
            data = json.load(f)
            return data.get("background", None)
    return None

def choose_background():
    path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if path:
        set_background(path)
        save_settings(path)

def set_background(path):
    try:
        img = Image.open(path)
        img = img.resize((800, 400), Image.LANCZOS)
        bg_image = ImageTk.PhotoImage(img)
        background_label.config(image=bg_image)
        background_label.image = bg_image
    except Exception as e:
        print(f"Background loading error: {e}")

def update_cps():
    global left_cps
    left_cps = left_slider.get()
    left_value.config(text=str(int(left_cps)))
    root.after(100, update_cps)

root = tk.Tk()
root.title("AutoClicker | By SwalyKHY")
root.geometry("500x150")
root.configure(bg="#1c1c1c")
root.resizable(False, False)

title = tk.Label(root, text="Click", font=("Segoe UI", 22, "bold"), fg="white", bg="#1c1c1c")
title.pack(pady=10)

frame = tk.Frame(root, bg="#2b2b2b")
frame.pack(pady=10, padx=20, fill="x")

style = ttk.Style()
style.theme_use("clam")
style.configure("TScale",
                background="#2b2b2b",
                troughcolor="#3c3c3c",
                sliderthickness=15,
                sliderlength=20,
                sliderrelief="flat",
                borderwidth=0)

left_label = tk.Label(frame, text="Left Click CPS", fg="#f5f5f5", bg="#2b2b2b", font=("Segoe UI", 11))
left_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

left_slider = ttk.Scale(frame, from_=0, to=25, orient="horizontal", length=150)
left_slider.set(10)
left_slider.grid(row=0, column=1, padx=5)

left_value = tk.Label(frame, text="10", fg="white", bg="#2b2b2b", font=("Segoe UI", 10))
left_value.grid(row=0, column=2, padx=5)

info_label = tk.Label(frame, text="G = Start | H = Stop", fg="#cccccc", bg="#2b2b2b", font=("Segoe UI", 10, "italic"))
info_label.grid(row=0, column=3, padx=10)

background_label = tk.Label(root, bg="#1c1c1c")
background_label.place(relx=0.5, rely=0.5, anchor="center")
background_label.lower()

bg_path = load_settings()
if bg_path:
    set_background(bg_path)

settings_button = tk.Button(root, text="⚙", font=("Arial", 12), command=choose_background, bg="black", fg="white", bd=0)
settings_button.place(x=370, y=10)

update_cps()

threading.Thread(target=left_clicker, daemon=True).start()

root.mainloop()
