import streamlit as st
import os
from supabase import create_client

# =========================
# PAGE
# =========================

st.set_page_config(page_title="WOW Hijab", layout="wide")

# =========================
# SUPABASE
# =========================

url = "https://iokwmnwttpuappilrucs.supabase.co"

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlva3dtbnd0dHB1YXBwaWxydWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwMjA3NTAsImV4cCI6MjA5NDU5Njc1MH0.PDvsxatgkSK0pl_6KG-b5mOLGG5M2je3JsLOv5yHp0Q"

supabase = create_client(url, key)

# =========================
# FOLDER GAMBAR
# =========================

if not os.path.exists("images"):
    os.makedirs("images")

# =========================
# LOGIN SESSION
# =========================

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

# =========================
# MENU
# =========================

menu = st.sidebar.selectbox(
    "Menu",
    ["Belanja", "Admin"]
)

# =========================
# BELANJA
# =========================

if menu == "Belanja":

    st.title("🧕 WOW Hijab")

    data = supabase.table("produk").select("*").execute().data

    if data:

        cols = st.columns(3)

        for i, d in enumerate(data):

            with cols[i % 3]:

                if d["gambar"]:
                    st.image(
                        d["gambar"],
                        use_container_width=True
                    )

                st.markdown(f"### {d['nama']}")
                st.write(f"💰 Rp{d['harga']}")
                st.write(f"📦 Stok: {d['stok']}")

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

            if user == "admin" and pw == "123":

                st.session_state.admin_login = True

                st.success("Login berhasil!")

                st.rerun()

            else:
                st.error("Username atau password salah")

    else:

        st.title("👩‍💼 Dashboard Admin")

        if st.button("Logout"):

            st.session_state.admin_login = False

            st.rerun()

        st.subheader("Tambah Produk")

        nama = st.text_input("Nama Produk")

        harga = st.number_input(
            "Harga",
            min_value=0
        )

        stok = st.number_input(
            "Stok",
            min_value=0
        )

        gambar = st.file_uploader(
            "Upload Gambar",
            type=["jpg", "png", "jpeg"]
        )

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

            st.success("Produk berhasil ditambahkan!")

        st.subheader("📦 Data Produk")

        data = supabase.table("produk").select("*").execute().data

        for d in data:

            if d["gambar"]:
                st.image(d["gambar"], width=150)

            st.write(
                f"{d['nama']} | Rp{d['harga']} | Stok: {d['stok']}"
            )
