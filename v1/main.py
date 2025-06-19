# === JARVIS APP VERSION 1: Basic GUI Layout ===
# GUI layout with camera placeholder (left), Jarvis face (top-right), and notepad output (bottom-right)

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import cv2
import threading

class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis v1")
        self.root.geometry("1000x600")
        self.root.configure(bg="black")

        self.setup_gui()
        self.cap = None  # Camera object placeholder

    def setup_gui(self):
        # === Split main window into 2 halves ===
        left_frame = tk.Frame(self.root, width=500, height=600, bg="black")
        left_frame.pack(side="left", fill="both")

        right_frame = tk.Frame(self.root, width=500, height=600, bg="gray20")
        right_frame.pack(side="right", fill="both")

        # === LEFT SIDE: Camera Feed ===
        self.camera_label = tk.Label(left_frame, bg="black")
        self.camera_label.pack(expand=True, fill="both")
        
        # === RIGHT SIDE ===
        # Top: Jarvis face (static image for now)
        self.jarvis_face_canvas = tk.Canvas(right_frame, height=300, bg="gray20", highlightthickness=0)
        self.jarvis_face_canvas.pack(fill="x")
        face_img = Image.open("assets/jarvis_face.jpg")
        face_img = face_img.resize((250, 250))
        self.face_img_tk = ImageTk.PhotoImage(face_img)
        self.jarvis_face_canvas.create_image(250, 150, image=self.face_img_tk)

        # Bottom: Notepad style output area
        self.output_area = ScrolledText(right_frame, height=15, bg="black", fg="lime", font=("Courier", 12))
        self.output_area.pack(fill="both", expand=True)
        self.output_area.insert(tk.END, "[Jarvis Initialized] Welcome to Version 1.\n")

    def run(self):
        self.root.mainloop()

# Entry point
if __name__ == "__main__":
    app_root = tk.Tk()
    app = JarvisApp(app_root)
    app.run()
