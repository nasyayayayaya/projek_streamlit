import streamlit as st
import os

from supabase import create_client

st.set_page_config(page_title="Toko Hijab", layout="wide")

# =========================
# SUPABASE
# =========================

url = "https://iokwmnwttpuappilrucs.supabase.co/rest/v1/"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlva3dtbnd0dHB1YXBwaWxydWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwMjA3NTAsImV4cCI6MjA5NDU5Njc1MH0.PDvsxatgkSK0pl_6KG-b5mOLGG5M2je3JsLOv5yHp0Q"

supabase = create_client(url, key)

# =========================
# SETUP
# =========================

from supabase import create_client
if not os.path.exists("images"):
    os.makedirs("images")

# =========================
# DATABASE
# =========================
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    harga INTEGER,
    stok INTEGER,
    gambar TEXT
)
''')

c.execute('''
CREATE TABLE IF NOT EXISTS transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    no_hp TEXT,
    alamat TEXT,
    produk TEXT,
    jumlah INTEGER,
    total INTEGER,
    bukti TEXT
)
''')

# akun admin default
c.execute("SELECT * FROM users WHERE username='admin'")
if not c.fetchone():
    c.execute("INSERT INTO users (username,password) VALUES ('admin','123')")
    conn.commit()

# =========================
# SESSION LOGIN ADMIN
# =========================
if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

menu = st.sidebar.selectbox("Menu", ["Belanja", "Admin"])

# =========================
# USER (TANPA LOGIN)
# =========================
if menu == "Belanja":
    st.title("WOW Hijab")

    data = supabase.table("produk").select("*").execute().data

    cols = st.columns(3)

    for i, d in enumerate(data):
        with cols[i % 3]:
            if d[4]:
                st.image(d[4], use_container_width=True)
            st.markdown(f"### {d['nama']}")
st.write(f"💰 Rp{d['harga']}")
st.write(f"📦 Stok: {d['stok']}")
st.image(d["gambar"], use_container_width=True)

st.divider()
st.subheader("🛍️ Form Pembelian")

nama = st.text_input("Nama")
no_hp = st.text_input("No HP")
alamat = st.text_area("Alamat")

c.execute("SELECT id, nama, harga, stok FROM produk")
produk = c.fetchall()

if produk:
        pilihan = st.selectbox("Pilih Produk", produk,
                               format_func=lambda x: f"{x[1]} (Stok: {x[3]})")

        jumlah = st.number_input("Jumlah", min_value=1)
        bukti = st.file_uploader("Upload Bukti Transfer", type=["jpg","png"])

        if pilihan:
            id_produk, nama_produk, harga, stok = pilihan
            total = harga * jumlah

            st.info(f"Total: Rp{total}")

            if st.button("Beli"):
                if jumlah > stok:
                    st.error("Stok tidak cukup!")
                else:
                    bukti_path = ""
                    if bukti:
                        bukti_path = f"images/{bukti.name}"
                        with open(bukti_path, "wb") as f:
                            f.write(bukti.getbuffer())

                    c.execute("""
                    INSERT INTO transaksi
                    (nama,no_hp,alamat,produk,jumlah,total,bukti)
                    VALUES (?,?,?,?,?,?,?)
                    """,(nama,no_hp,alamat,nama_produk,jumlah,total,bukti_path))

                    # update stok
                    c.execute("UPDATE produk SET stok = stok - ? WHERE id=?",
                              (jumlah,id_produk))

                    conn.commit()

                    st.success("Pembelian berhasil!")

                    # INVOICE
                    st.markdown("## 🧾 Invoice")
                    st.write(f"Nama: {nama}")
                    st.write(f"No HP: {no_hp}")
                    st.write(f"Produk: {nama_produk}")
                    st.write(f"Jumlah: {jumlah}")
                    st.write(f"Total: Rp{total}")
else:
    st.warning("Belum ada produk")

# =========================
# ADMIN
# =========================
if menu == "Admin":

    if not st.session_state.admin_login:
        st.title("🔐 Login Admin")

        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        if st.button("Login"):
            c.execute("SELECT * FROM users WHERE username=? AND password=?",(user,pw))
            if c.fetchone():
                st.session_state.admin_login = True
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Salah!")

    else:
        st.title("👩‍💼 Dashboard Admin")

        if st.button("Logout"):
            st.session_state.admin_login = False
            st.rerun()

        st.subheader("Tambah Produk")

        nama = st.text_input("Nama Produk")
        harga = st.number_input("Harga", min_value=0)
        stok = st.number_input("Stok", min_value=0)
        gambar = st.file_uploader("Upload Gambar", type=["jpg","png"])

        if st.button("Simpan Produk"):
            path = ""
            if gambar:
                path = f"images/{gambar.name}"
                with open(path, "wb") as f:
                    f.write(gambar.getbuffer())

            supabase.table("produk").insert({
    "nama": nama,
    "harga": harga,
    "stok": stok,
    "gambar": path
}).execute()
            st.success("Produk ditambahkan!")

        st.subheader("📦 Data Produk")

        c.execute("SELECT * FROM produk")
        data = c.fetchall()

        for d in data:
            st.write(f"{d[1]} | Rp{d[2]} | Stok: {d[3]}")

        st.subheader("🧾 Transaksi")

        c.execute("SELECT * FROM transaksi")
        trx = c.fetchall()

        for t in trx:
            st.write(f"{t[1]} beli {t[4]} ({t[5]}) - Rp{t[6]}")
            if t[7]:
                st.image(t[7], width=150)
