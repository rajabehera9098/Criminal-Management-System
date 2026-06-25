from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import main

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Slight window transparency
        self.root.attributes("-alpha", 0.97)

        # ===== Background Image =====
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path,"images","police5.jpeg")

        bg_img = Image.open(img_path)
        bg_img = bg_img.resize((800, 500))

        self.bg = ImageTk.PhotoImage(bg_img)

        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, width=800, height=500)

        # ===== Title =====
        Label(self.root,
              text="CRIMINAL MANAGEMENT SYSTEM",
              font=("Arial", 18, "bold"),
              bg="#000000", fg="#e84118").place(relx=0.5, y=20, anchor="center")

        # ===== Glass Style Login Card =====

        # Border glow
        #border = Frame(self.root, bg="#e84118")
        #border.place(relx=0.2, rely=0.5, anchor=CENTER, width=310, height=330)

        # Main transparent-style card
        frame = Frame(self.root, bg="#111111")
        frame.place(relx=0.3, rely=0.5, anchor=CENTER, width=320, height=320)

        Label(frame, text="LOGIN",
              font=("Arial", 18, "bold"),
              bg="#000000", fg="white").pack(pady=10)

        Label(frame, text="Welcome Back!",
              font=("Arial", 10),
              bg="#000000", fg="#e84118").pack()

        # Username
        Label(frame, text="Username",
              font=("Arial", 11),
              bg="#000000", fg="white").pack(pady=5)

        self.username = Entry(frame, font=("Arial", 12),
                              bg="#111111", fg="white",
                              insertbackground="white", bd=0)
        self.username.pack(pady=5, ipady=6)
        self.username.focus()

        Frame(frame, bg="#e84118", height=1, width=200).pack()

        # Password
        Label(frame, text="Password",
              font=("Arial", 11),
              bg="#000000", fg="white").pack(pady=5)

        self.password = Entry(frame, font=("Arial", 12),
                              show="*",
                              bg="#111111", fg="white",
                              insertbackground="white", bd=0)
        self.password.pack(pady=5, ipady=6)

        Frame(frame, bg="#e84118", height=1, width=200).pack()

        # Show/Hide Password
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
                            bg="#333333", fg="white",
                            bd=0, cursor="hand2")
        toggle_btn.pack(pady=5)

        # Hover Effect
        def on_enter(e):
            e.widget['bg'] = "#c23616"

        def on_leave(e):
            e.widget['bg'] = "#e84118"

        # Login Button
        btn = Button(frame, text="Login",
                     command=self.login,
                     font=("Arial", 12, "bold"),
                     bg="#e84118", fg="white",
                     activebackground="#c23616",
                     cursor="hand2",
                     bd=0)

        btn.pack(pady=15, ipadx=20, ipady=5)
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

        # Enter key login
        self.root.bind("<Return>", lambda event: self.login())

        # Footer
        Label(self.root, text="Criminal Management System",
              font=("Arial", 10),
              bg="black", fg="white").place(x=10, y=470)


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