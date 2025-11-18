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
              font=("Arial", 14, "bold"), command=lambda: show_frame(frame_search)).pack(pady=10)

    tk.Button(frame_menu, text="Jumlah Karcis", width=25, bg="#884EA0", fg="white",
              font=("Arial", 14, "bold"), command=lambda: show_frame(frame_jumlah)).pack(pady=10)

# ---------------- HALAMAN INPUT DATA ----------------
def halaman_input():
    tk.Label(frame_input, text="INPUT DATA PARKIR", font=("Arial Black", 20),
             fg="#935116", bg="#FEF5E7").pack(pady=20)

    tk.Label(frame_input, text="Nomor Plat:", bg="#FEF5E7", font=("Arial", 14)).pack()
    plat = tk.Entry(frame_input, font=("Arial", 14))
    plat.pack()

    tk.Label(frame_input, text="Jenis Kendaraan:", bg="#FEF5E7", font=("Arial", 14)).pack(pady=(10,0))

    pilihan = tk.StringVar(value="Mobil")
    jenis = ttk.OptionMenu(frame_input, pilihan, "Mobil", "Mobil", "Motor")
    jenis.pack()

    tk.Label(frame_input, text="Waktu Masuk (Otomatis)", bg="#FEF5E7",
             font=("Arial", 14)).pack(pady=(10,0))

    def simpan_data():
        if not plat.get():
            popup("Peringatan", "Nomor Plat harus diisi!", "#F1C40F")
            return

        waktu_masuk = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        biaya = 10000 if pilihan.get() == "Mobil" else 5000

        data_parkir.append({
            "plat": plat.get(),
            "jenis": pilihan.get(),
            "waktu": waktu_masuk,
            "biaya": biaya
        })

        popup("Sukses", "Data parkir berhasil disimpan!", "#27AE60")

        plat.delete(0, tk.END)
        pilihan.set("Mobil")
        show_frame(frame_menu)

    tk.Button(frame_input, text="Simpan", bg="#D35400", fg="white",
              font=("Arial", 14, "bold"), command=simpan_data).pack(pady=20)

    tk.Button(frame_input, text="Kembali", bg="#BFC9CA",
              font=("Arial", 12, "bold"), command=lambda: show_frame(frame_menu)).pack()

# ---------------- HALAMAN SEARCH ----------------
def halaman_search():
    global tree
    tk.Label(frame_search, text="DATA KARCIS PARKIR", font=("Arial Black", 20),
             fg="#0E6251", bg="#E8F8F5").pack(pady=20)

    frame_search_controls = tk.Frame(frame_search, bg="#E8F8F5")
    frame_search_controls.pack(pady=10)

    tk.Label(frame_search_controls, text="Cari Plat:", bg="#E8F8F5").grid(row=0, column=0)
    entry_plat = tk.Entry(frame_search_controls)
    entry_plat.grid(row=0, column=1)

    tk.Label(frame_search_controls, text="Jenis:", bg="#E8F8F5").grid(row=0, column=2)
    combo_jenis = ttk.Combobox(frame_search_controls, values=["", "Mobil", "Motor"], state="readonly")
    combo_jenis.grid(row=0, column=3)

    tk.Label(frame_search_controls, text="Waktu:", bg="#E8F8F5").grid(row=0, column=4)
    entry_waktu = tk.Entry(frame_search_controls)
    entry_waktu.grid(row=0, column=5)

    def search():
        refresh_table(entry_plat.get(), combo_jenis.get(), entry_waktu.get())

    tk.Button(frame_search_controls, text="Cari", bg="#28B463",
              fg="white", command=search).grid(row=0, column=6, padx=10)

    frame_table = tk.Frame(frame_search)
    frame_table.pack(pady=10)

    tree = ttk.Treeview(frame_table,
                        columns=("No", "Plat", "Jenis", "Waktu", "Biaya"),
                        show="headings", height=10)

    for col in ("No","Plat","Jenis","Waktu","Biaya"):
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor="center")

    tree.pack()

    tk.Button(frame_search, text="Kembali", bg="#BFC9CA",
              font=("Arial", 12, "bold"), command=lambda: show_frame(frame_menu)).pack(pady=15)

# ---------------- HALAMAN JUMLAH ----------------
def halaman_jumlah():
    global label_total_karcis, label_total_uang
    tk.Label(frame_jumlah, text="JUMLAH KARCIS", font=("Arial Black", 20),
             fg="#1B4F72", bg="#EBF5FB").pack(pady=25)

    label_total_karcis = tk.Label(frame_jumlah, text="", font=("Arial", 16), bg="#EBF5FB")
    label_total_karcis.pack()

    label_total_uang = tk.Label(frame_jumlah, text="", font=("Arial", 16),
                                bg="#EBF5FB", fg="#145A32")
    label_total_uang.pack()

    tk.Button(frame_jumlah, text="Kembali", bg="#BFC9CA",
              font=("Arial", 12, "bold"), command=lambda: show_frame(frame_menu)).pack(pady=20)

# ---------------- Init Frame ----------------
halaman_login()
halaman_menu()
halaman_input()
halaman_search()
halaman_jumlah()

for frame in (frame_login, frame_menu, frame_input, frame_search, frame_jumlah):
    frame.place(relwidth=1, relheight=1)

show_frame(frame_login)
root.mainloop()



