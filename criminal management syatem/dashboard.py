from tkinter import *
from tkinter import ttk, messagebox
import database
import main
import time


class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1000x600")
        self.root.title("Dashboard")
        self.root.configure(bg="#0f172a")
        

        # ===== NAVBAR =====
        navbar = Frame(root, bg="#020617", height=60)
        navbar.pack(fill=X)

        Label(navbar, text="CRIMINAL MANAGEMENT SYSTEM",
              font=("Segoe UI", 16, "bold"),
              bg="#020617", fg="white").pack(side=LEFT, padx=15)

        self.clock_label = Label(navbar, font=("Segoe UI", 11),
                                 bg="#020617", fg="#facc15")
        self.clock_label.pack(side=RIGHT, padx=20)
        self.update_clock()

        # ===== SIDEBAR =====
        sidebar = Frame(root, bg="#111827", width=200)
        sidebar.pack(side=LEFT, fill=Y)

        def sidebar_btn(text, command=None):
            btn = Button(sidebar, text=text,
                         font=("Segoe UI", 11),
                         bg="#111827", fg="#e5e7eb",
                         activebackground="#1f2937",
                         activeforeground="white",
                         bd=0, anchor="w",
                         cursor="hand2",
                         command=command)
            btn.pack(fill=X, padx=10, pady=5)

            def on_enter(e): btn['bg'] = "#1f2937"
            def on_leave(e): btn['bg'] = "#111827"

            btn.bind("<Enter>", on_enter)
            btn.bind("<Leave>", on_leave)

        sidebar_btn("🏠 Dashboard")
        sidebar_btn("📋 Records", self.show_records)
        sidebar_btn("📊 Quick Stats", self.show_stats)
        sidebar_btn("➕ Add Criminal", self.open_main)
        sidebar_btn("🚪 Logout", self.logout)

        # ===== MAIN AREA =====
        main_frame = Frame(root, bg="#0f172a")
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=20)

        Label(main_frame, text="Dashboard",
              font=("Segoe UI", 20, "bold"),
              bg="#0f172a", fg="white").pack(anchor="w")

        # ===== CARDS =====
        card_frame = Frame(main_frame, bg="#0f172a")
        card_frame.pack(pady=20)

        self.total_label = self.create_card(card_frame, "Total Criminals", "#2563eb", 0)
        self.wanted_label = self.create_card(card_frame, "Most Wanted", "#ef4444", 1)

        # ===== BUTTONS =====
        btn_frame = Frame(main_frame, bg="#0f172a")
        btn_frame.pack(pady=10)

        Button(btn_frame, text="🔄 Refresh",
               command=self.load_data,
               bg="#3b82f6", fg="white",
               font=("Segoe UI", 10, "bold"),
               cursor="hand2").pack(side=LEFT, padx=5)

        Button(btn_frame, text="📂 Open Full System",
               command=self.open_main,
               bg="#22c55e", fg="white",
               font=("Segoe UI", 10, "bold"),
               cursor="hand2").pack(side=LEFT, padx=5)

        # ===== CONTENT AREA =====
        self.content_frame = Frame(main_frame, bg="#0f172a")
        self.content_frame.pack(fill=BOTH, expand=True)

        self.load_data()

    # ===== CLOCK =====
    def update_clock(self):
        self.clock_label.config(text=time.strftime("%H:%M:%S"))
        self.clock_label.after(1000, self.update_clock)

    # ===== CARD =====
    def create_card(self, parent, title, color, col):
        card = Frame(parent, bg=color, width=220, height=120)
        card.grid(row=0, column=col, padx=15)
        card.pack_propagate(False)

        Label(card, text=title,
              font=("Segoe UI", 12, "bold"),
              bg=color, fg="white").pack(pady=10)

        value = Label(card, text="0",
                      font=("Segoe UI", 20, "bold"),
                      bg=color, fg="white")
        value.pack()

        return value

    # ===== LOAD DATA =====
    def load_data(self):
        try:
            conn = database.get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM criminal")
            total = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM criminal WHERE wanted='yes'")
            wanted = cursor.fetchone()[0]

            conn.close()

            self.total_label.config(text=str(total))
            self.wanted_label.config(text=str(wanted))

        except Exception as e:
            print("DB Error:", e)

    # ===== CLEAR =====
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ===== RECORDS =====
    def show_records(self):
        self.clear_content()

        Label(self.content_frame, text="Criminal Records",
              font=("Segoe UI", 16, "bold"),
              bg="#0f172a", fg="white").pack(pady=10)

        search_frame = Frame(self.content_frame, bg="#0f172a")
        search_frame.pack()

        self.search_var = StringVar()

        Entry(search_frame, textvariable=self.search_var, width=25).pack(side=LEFT, padx=5)
        Button(search_frame, text="Search", command=self.search_data).pack(side=LEFT)

        self.table = ttk.Treeview(self.content_frame,
                                 columns=("name", "crime", "wanted"),
                                 show="headings")

        self.table.heading("name", text="Name")
        self.table.heading("crime", text="Crime")
        self.table.heading("wanted", text="Wanted")

        self.table.pack(fill=BOTH, expand=True)

        self.load_records()

    def load_records(self):
        for row in self.table.get_children():
            self.table.delete(row)

        conn = database.get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT Criminal_name, crimeType, wanted FROM criminal")
        rows = cursor.fetchall()

        for row in rows:
            if row[2] == "yes":
                self.table.insert("", END, values=row, tags=("wanted",))
            else:
                self.table.insert("", END, values=row)

        self.table.tag_configure("wanted", background="red")

        conn.close()

    def search_data(self):
        value = self.search_var.get()

        for row in self.table.get_children():
            self.table.delete(row)

        conn = database.get_connection()
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT Criminal_name, crimeType, wanted 
            FROM criminal 
            WHERE Criminal_name LIKE '%{value}%' OR crimeType LIKE '%{value}%'
        """)

        for row in cursor.fetchall():
            self.table.insert("", END, values=row)

        conn.close()

    # ===== STATS =====
    def show_stats(self):
        self.clear_content()

        Label(self.content_frame, text="Crime Statistics",
              font=("Segoe UI", 16, "bold"),
              bg="#0f172a", fg="white").pack(pady=10)

        conn = database.get_connection()
        cursor = conn.cursor()

        # DATE STATS
        Label(self.content_frame, text="By Date",
              font=("Segoe UI", 13, "bold"),
              bg="#0f172a", fg="#38bdf8").pack()

        cursor.execute("SELECT dateofcrime, COUNT(*) FROM criminal GROUP BY dateofcrime")

        for date, count in cursor.fetchall():
            row = Frame(self.content_frame, bg="#0f172a")
            row.pack(anchor="w", pady=3, padx=20)

            Label(row, text=str(date), width=15, anchor="w",
                  bg="#0f172a", fg="white").pack(side=LEFT)

            Frame(row, bg="#3b82f6", width=count*50, height=15).pack(side=LEFT, padx=5)

            Label(row, text=str(count), bg="#0f172a", fg="white").pack(side=LEFT)

        # CRIME TYPE STATS
        Label(self.content_frame, text="By Crime Type",
              font=("Segoe UI", 13, "bold"),
              bg="#0f172a", fg="#22c55e").pack(pady=10)

        cursor.execute("SELECT crimeType, COUNT(*) FROM criminal GROUP BY crimeType")

        for crime, count in cursor.fetchall():
            row = Frame(self.content_frame, bg="#0f172a")
            row.pack(anchor="w", pady=3, padx=20)

            Label(row, text=str(crime), width=15, anchor="w",
                  bg="#0f172a", fg="white").pack(side=LEFT)

            Frame(row, bg="#22c55e", width=count*50, height=15).pack(side=LEFT, padx=5)

            Label(row, text=str(count), bg="#0f172a", fg="white").pack(side=LEFT)

        conn.close()

    # ===== NAVIGATION =====
    def open_main(self):
        self.root.destroy()
        main.run_app()

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure?"):
            self.root.destroy()
            from tkinter import Tk
            import login
            root = Tk()
            login.Login(root)
            root.mainloop()