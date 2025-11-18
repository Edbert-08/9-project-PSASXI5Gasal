import tkinter as tk 
from tkinter import ttk
from datetime import datetime

# ---------------- Fungsi Popup Toplevel ----------------
def popup(title, message, warna="#3498DB"):
    win = tk.Toplevel()
    win.title(title)
    win.geometry("300x150")
    win.config(bg=warna)
    win.resizable(False, False)

    tk.Label(win, text=title, font=("Arial Black", 16), bg=warna, fg="white").pack(pady=10)
    tk.Label(win, text=message, font=("Arial", 12), bg=warna, fg="white").pack()

    tk.Button(win, text="OK", bg="white", fg="black", font=("Arial", 12), command=win.destroy)\
        .pack(pady=15)

# ---------------- Data Parkir ----------------
data_parkir = []

# ---------------- Jendela Utama ----------------
root = tk.Tk()
root.title("Sistem Karcis Parkir")
root.geometry("700x500")
root.config(bg="#D6EAF8")

# ---------------- Frame ----------------
frame_login = tk.Frame(root, bg="#D6EAF8")
frame_menu = tk.Frame(root, bg="#E8DAEF")
frame_input = tk.Frame(root, bg="#FEF5E7")
frame_search = tk.Frame(root, bg="#E8F8F5")
frame_jumlah = tk.Frame(root, bg="#EBF5FB")

tree = None
label_total_karcis = None
label_total_uang = None

def show_frame(frame):
    frame.tkraise()
    if frame == frame_search:
        refresh_table()
    elif frame == frame_jumlah:
        refresh_jumlah()

def refresh_table(filter_plat="", filter_jenis="", filter_waktu=""):
    global tree
    if tree:
        for item in tree.get_children():
            tree.delete(item)

        for i, d in enumerate(data_parkir, start=1):
            if (filter_plat.lower() in d["plat"].lower() or not filter_plat) and \
               (filter_jenis.lower() in d["jenis"].lower() or not filter_jenis) and \
               (filter_waktu in d["waktu"] or not filter_waktu):

                tree.insert("", "end",
                    values=(i, d["plat"], d["jenis"], d["waktu"], d["biaya"]))

def refresh_jumlah():
    global label_total_karcis, label_total_uang
    total_karcis = len(data_parkir)
    total_uang = sum(d["biaya"] for d in data_parkir)

    label_total_karcis.config(text=f"Total Karcis: {total_karcis}")
    label_total_uang.config(text=f"Total Uang: Rp {total_uang:,}")

# ---------------- HALAMAN LOGIN ----------------
def halaman_login():
    tk.Label(frame_login, text="LOGIN KARCIS PARKIR", font=("Arial Black", 20),
             bg="#D6EAF8", fg="#154360").pack(pady=30)

    tk.Label(frame_login, text="Username:", bg="#D6EAF8", font=("Arial", 14)).pack()
    user = tk.Entry(frame_login, font=("Arial", 14))
    user.pack()

    tk.Label(frame_login, text="Password:", bg="#D6EAF8", font=("Arial", 14)).pack(pady=(10,0))
    pw = tk.Entry(frame_login, show="*", font=("Arial", 14))
    pw.pack()

    def login():
        if user.get() == "admin" and pw.get() == "1234":
            show_frame(frame_menu)
        else:
            popup("Gagal", "Username atau password salah!", "#E74C3C")

    tk.Button(frame_login, text="Login", bg="#3498DB", fg="white",
              font=("Arial", 14, "bold"), width=12, command=login).pack(pady=25)

# ---------------- HALAMAN MENU ----------------
def halaman_menu():
    tk.Label(frame_menu, text="MENU UTAMA", font=("Arial Black", 20),
             fg="#4A235A", bg="#E8DAEF").pack(pady=30)

    tk.Button(frame_menu, text="Input Data Parkir", width=25, bg="#BB8FCE", fg="white",
              font=("Arial", 14, "bold"), command=lambda: show_frame(frame_input)).pack(pady=10)

    tk.Button(frame_menu, text="Lihat Data Parkir", width=25, bg="#AF7AC5", fg="white",
              font=("Arial", 14


