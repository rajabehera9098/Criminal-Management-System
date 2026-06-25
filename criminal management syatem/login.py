from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import main

# 🔥 Rounded rectangle function
def round_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # ===== Background Image =====
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, "images", "police5.jpeg")

        bg_img = Image.open(img_path)
        bg_img = bg_img.resize((800, 500))
        self.bg = ImageTk.PhotoImage(bg_img)

        Label(self.root, image=self.bg).place(x=0, y=0, width=800, height=500)

        # ===== Title =====
        #Label(self.root,
              #text="CRIMINAL MANAGEMENT SYSTEM",
              #font=("Arial", 18, "bold"),
              #bg="#000000", fg="#facc15").place(relx=0.5, y=20, anchor="center")

        # ===== ROUNDED LOGIN CARD =====
        canvas = Canvas(self.root, width=330, height=402,
                        bg="#111111", highlightthickness=0)
        canvas.place(relx=0.23, rely=0.49, anchor=CENTER)

        round_rect(canvas, 3, 4, 322, 400,
                   radius=25,
                   fill="#111827",
                   outline="#1e293b",
                   width=2)

        frame = Frame(canvas, bg="#111827")
        frame.place(x=10, y=10, width=300, height=390)
        # ===== TOP HEADER (LOGO + TEXT) =====
        top_frame = Frame(frame, bg="#0f172a")
        top_frame.pack(fill=X, pady=(10, 5))

        # LOGO
        logo_path = os.path.join(base_path, "images", "logo2.jpeg")
        logo_img = Image.open(logo_path)
        logo_img = logo_img.resize((45, 45))

        self.logo_img = ImageTk.PhotoImage(logo_img)

        Label(top_frame, image=self.logo_img, bg="#0f172a").pack(side=LEFT, padx=10)

        # TEXT SIDE
        text_frame = Frame(top_frame, bg="#0f172a")
        text_frame.pack(side=LEFT)

        Label(text_frame, text="CRIMINAL",
            font=("Arial", 13, "bold"),
            bg="#0f172a", fg="#facc15").pack(anchor="w")

        Label(text_frame, text="MANAGEMENT SYSTEM",
            font=("Arial", 10),
            bg="#0f172a", fg="white").pack(anchor="w")

        # ===== CONTENT =====
        Label(frame, text="LOGIN",
              font=("Arial", 18, "bold"),
              bg="#111827", fg="white").pack(pady=(15, 5))

        Label(frame, text="Welcome Back",
              font=("Arial", 10),
              bg="#111827", fg="#facc15").pack(pady=(0, 10))

        # USERNAME
        Label(frame, text="Username🧑‍💻",
              bg="#111827", fg="white").pack(anchor="w", padx=20)

        self.username = Entry(frame,
                              bg="#1e293b", fg="white",
                              insertbackground="white",
                              relief=FLAT)
        self.username.pack(padx=20, pady=5, ipady=6, fill=X)
        self.username.focus()

        # PASSWORD
        Label(frame, text="Password🔐",
              bg="#111827", fg="white").pack(anchor="w", padx=20, pady=(10, 0))

        self.password = Entry(frame,
                              show="*",
                              bg="#1e293b", fg="white",
                              insertbackground="white",
                              relief=FLAT)
        self.password.pack(padx=20, pady=5, ipady=6, fill=X)

        # SHOW / HIDE PASSWORD
        self.show_pass = False

        def toggle_password():
            if self.show_pass:
                self.password.config(show="*")
                self.show_pass = False
                toggle_btn.config(text="👁 Show")
            else:
                self.password.config(show="")
                self.show_pass = True
                toggle_btn.config(text="🙈 Hide")

        toggle_btn = Button(frame, text="👁 Show",
                            command=toggle_password,
                            bg="#1e293b", fg="white",
                            bd=0, cursor="hand2")
        toggle_btn.pack(pady=5)

        # BUTTON HOVER
        def on_enter(e):
            login_btn['bg'] = "#1d4ed8"

        def on_leave(e):
            login_btn['bg'] = "#2563eb"

        # LOGIN BUTTON
        login_btn = Button(frame, text="LOGIN",
                           command=self.login,
                           font=("Arial", 12, "bold"),
                           bg="#008000", fg="white",
                           relief=FLAT,
                           cursor="hand2")
        login_btn.pack(pady=4, ipadx=10, ipady=5)

        login_btn.bind("<Enter>", on_enter)
        login_btn.bind("<Leave>", on_leave)

        # ENTER KEY
        self.root.bind("<Return>", lambda event: self.login())

        # FOOTER
        #Label(self.root, text="Criminal Management System",
              #font=("Arial", 10),
              #bg="black", fg="white").place(x=10, y=470)

    def login(self):
        if self.username.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All fields are required")
            return

        if self.username.get() == "a" and self.password.get() == "1":
            messagebox.showinfo("Success", "Login Successful")
            self.root.destroy()

            from tkinter import Tk
            import dashboard

            root = Tk()
            dashboard.Dashboard(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


if __name__ == "__main__":
    root = Tk()
    app = Login(root)
    root.mainloop()