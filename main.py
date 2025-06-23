# === JARVIS APP VERSION 3: Facial Recognition and Primary User Setup ===
# Adds facial recognition using face_recognition library and user initialization

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import cv2
import face_recognition
import numpy as np
import os
import pickle

class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis v3")
        self.root.geometry("1000x600")
        self.root.configure(bg="black")

        self.known_encodings = []
        self.known_names = []
        self.load_users()

        self.setup_gui()
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.update_camera()

    def setup_gui(self):
        left_frame = tk.Frame(self.root, width=500, height=600, bg="black")
        left_frame.pack(side="left", fill="both")

        right_frame = tk.Frame(self.root, width=500, height=600, bg="gray20")
        right_frame.pack(side="right", fill="both")

        self.camera_label = tk.Label(left_frame, bg="black")
        self.camera_label.pack(expand=True, fill="both")

        self.jarvis_face_canvas = tk.Canvas(right_frame, height=300, bg="gray20", highlightthickness=0)
        self.jarvis_face_canvas.pack(fill="x")
        face_img = Image.open("assets/jarvis_face.jpg").resize((250, 250))
        self.face_img_tk = ImageTk.PhotoImage(face_img)
        self.jarvis_face_canvas.create_image(250, 150, image=self.face_img_tk)

        self.output_area = ScrolledText(right_frame, height=15, bg="black", fg="lime", font=("Courier", 12))
        self.output_area.pack(fill="both", expand=True)
        self.output_area.insert(tk.END, "[Jarvis Initialized] Face recognition system loading...\n")

    def update_camera(self):
        def show_frame():
            if not self.running:
                return

            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                for face_encoding, face_location in zip(face_encodings, face_locations):
                    matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = self.known_names[first_match_index]
                        self.log_output(f"Hello, {name}! Welcome back.")
                    elif not self.known_encodings:
                        self.register_primary_user(face_encoding)
                        name = "Primary User"

                    top, right, bottom, left = [v * 4 for v in face_location]
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)

            self.camera_label.after(100, show_frame)

        show_frame()

    def register_primary_user(self, encoding):
        os.makedirs("data", exist_ok=True)
        with open("data/encodings.pkl", "wb") as f:
            pickle.dump(([encoding], ["Primary User"]), f)
        self.known_encodings.append(encoding)
        self.known_names.append("Primary User")
        self.log_output("[Jarvis] Primary user registered.")

    def load_users(self):
        if os.path.exists("data/encodings.pkl"):
            with open("data/encodings.pkl", "rb") as f:
                self.known_encodings, self.known_names = pickle.load(f)

    def log_output(self, message):
        self.output_area.insert(tk.END, f"{message}\n")
        self.output_area.see(tk.END)

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    app_root = tk.Tk()
    app = JarvisApp(app_root)
    app.run()