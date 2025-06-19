# === JARVIS APP VERSION 2: Live Camera Feed ===
# Adds live webcam feed to the left side of the GUI using OpenCV and threading

import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import cv2
import threading

class JarvisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Jarvis v2")
        self.root.geometry("1000x600")
        self.root.configure(bg="black")

        self.setup_gui()
        self.cap = cv2.VideoCapture(0)  # Activate default webcam
        self.running = True
        self.update_camera()  # Start camera thread

    def setup_gui(self):
        # === Split main window into 2 halves ===
        left_frame = tk.Frame(self.root, width=500, height=600, bg="black")
        left_frame.pack(side="left", fill="both")

        right_frame = tk.Frame(self.root, width=500, height=600, bg="gray20")
        right_frame.pack(side="right", fill="both")

        # === LEFT SIDE: Live Camera Feed ===
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
        self.output_area.insert(tk.END, "[Jarvis Initialized] Live camera feed active.\n")

    def update_camera(self):
        def show_frame():
            if not self.running:
                return

            ret, frame = self.cap.read()
            if ret:
                frame = cv2.flip(frame, 1)  # Mirror the frame
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                self.camera_label.imgtk = imgtk
                self.camera_label.configure(image=imgtk)
            self.camera_label.after(10, show_frame)

        show_frame()

    def run(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.mainloop()

    def on_close(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

# Entry point
if __name__ == "__main__":
    app_root = tk.Tk()
    app = JarvisApp(app_root)
    app.run()