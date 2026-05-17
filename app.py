import streamlit as st
from supabase import create_client

# =========================
# CONFIG
# =========================

st.set_page_config(
    page_title="WOW Hijab",
    layout="wide"
)

# =========================
# SUPABASE
# =========================

url = "https://iokwmnwttpuappilrucs.supabase.co"

key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imlva3dtbnd0dHB1YXBwaWxydWNzIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkwMjA3NTAsImV4cCI6MjA5NDU5Njc1MH0.PDvsxatgkSK0pl_6KG-b5mOLGG5M2je3JsLOv5yHp0Q"

supabase = create_client(url, key)

# =========================
# STYLE
# =========================

st.markdown("""
<style>

.main {
    background-color: #fffafc;
}

.card {
    border: 2px solid #ffd6e0;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    background-color: white;
}

.stButton>button {
    background-color: pink;
    color: white;
    border-radius: 10px;
    border: none;
}

</style>
""", unsafe_allow_html=True)

# =========================
# BANNER
# =========================

st.image(
    "banner.png",
    use_container_width=True
)

st.markdown(
    "<h1 style='text-align:center; color:pink;'>🧣 WOW Hijab</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Hijab Cantik, Lucu, dan Imut 🎀</p>",
    unsafe_allow_html=True
)

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

    st.header("Produk Kami")

    try:
        response = supabase.table("produk").select("*").execute()
        data = response.data

    except Exception as e:
        st.error(e)
        data = []

    if data:

        cols = st.columns(3)

        for i, d in enumerate(data):

            with cols[i % 3]:

                st.markdown(
                    '<div class="card">',
                    unsafe_allow_html=True
                )

                if d["gambar"]:
                    st.image(
                        d["gambar"],
                        use_container_width=True
                    )

                st.subheader(d["nama"])
                st.write(f"💰 Rp{d['harga']}")
                st.write(f"📦 Stok: {d['stok']}")

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

    else:
        st.warning("Belum ada produk")

    # =========================
    # FORM ORDER
    # =========================

    st.header("🛒 Form Order")

    with st.form("form_order"):

        nama = st.text_input("Nama")
        nohp = st.text_input("No HP")
        alamat = st.text_area("Alamat")
        pesanan = st.text_input("Pesanan")

        jumlah = st.number_input(
            "Jumlah",
            min_value=1,
            step=1
        )

        submit = st.form_submit_button(
            "Pesan Sekarang"
        )

        if submit:

            st.success("Pesanan berhasil dibuat 🎉")
        
# =========================
# ADMIN
# =========================

if menu == "Admin":

    st.header("🔐 Login Admin")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if user == "admin" and pw == "123":

        st.success("Login berhasil")

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

gambar = st.selectbox(
    "Pilih Gambar",
    [
        "Bergo Pet Tipis.jpg",
        "Ciput Bandana 2 Warna.jpg",
        "Ciput Bandana Rajut.jpg",
        "Hijab Renang.jpg",
        "Jilbab Anak.jpg",
        "Pashmina Cashmere.jpg",
        "Pashmina Shawl.jpg"
    ]
)

if st.button("Simpan Produk"):

    image_url = supabase.storage.from_("produk").get_public_url(gambar)

    supabase.table("produk").insert({
        "nama": nama,
        "harga": harga,
        "stok": stok,
        "gambar": image_url
    }).execute()

    st.success("Produk berhasil ditambahkan!")
