import streamlit as st
import math

st.set_page_config(page_title="Sistem Operasi Franchise", layout="wide")

st.title("📦📈🔁 Sistem Operasi Franchise Kopi")
st.markdown("Gabungan Model: **Optimasi Produksi, Persediaan, dan Antrian**")

st.header("1️⃣ Optimasi Produksi")
st.markdown("*Hitung total profit berdasarkan jumlah minuman yang diproduksi*")

produk = ["Latte", "Cappuccino", "Matcha", "Hazelnut", "Red Velvet"]
profit_per_cup = [5000, 6000, 7000, 8000, 9000]
waktu_per_cup = [2, 3, 2, 4, 3]  # menit

produksi = []
total_waktu = 0
total_profit = 0

st.subheader("Input Jumlah Produksi Harian")
col1, col2, col3 = st.columns(3)
with col1:
    for i, p in enumerate(produk):
        jumlah = st.number_input(f"{p} (cup)", min_value=0, value=0, step=1, key=f"prod_{i}")
        produksi.append(jumlah)
        total_waktu += jumlah * waktu_per_cup[i]
        total_profit += jumlah * profit_per_cup[i]

kapasitas_waktu = 1200  # menit/hari
st.info(f"⏱️ Total waktu produksi: {total_waktu} menit dari maksimum {kapasitas_waktu} menit")
st.success(f"💰 Total estimasi profit: Rp{total_profit:,.0f}")

if total_waktu > kapasitas_waktu:
    st.warning("⚠️ Produksi melebihi kapasitas waktu harian!")

st.divider()
st.header("2️⃣ Model Persediaan (EOQ & ROP)")

st.markdown("*Hitung jumlah optimal pembelian bahan baku*")

bahan = ["Susu Cair", "Kopi Bubuk", "Bubuk Matcha", "Sirup Hazelnut", "Red Velvet"]
D = st.number_input("Permintaan tahunan (liter/unit)", value=21900)
S = st.number_input("Biaya pemesanan (Rp)", value=100000)
H = st.number_input("Biaya penyimpanan/tahun (Rp/unit)", value=500)
lead_time = st.number_input("Lead time (hari)", value=1)
kebutuhan_per_hari = st.number_input("Kebutuhan rata-rata per hari", value=60.0)
deviasi = st.number_input("Deviasi standar kebutuhan per hari", value=5.0)

st.subheader("📦 Hasil EOQ dan ROP")

eoq = math.sqrt((2 * D * S) / H)
rop = kebutuhan_per_hari * lead_time + 1.65 * deviasi

st.write(f"🔹 **EOQ (Jumlah optimal pemesanan)**: {eoq:.2f} unit")
st.write(f"🔹 **ROP (Titik pemesanan ulang)**: {rop:.2f} unit")

st.divider()
st.header("3️⃣ Model Antrian")

st.markdown("*Evaluasi antrian pelanggan di outlet atau antrian bahan baku di gudang*")

mode = st.selectbox("Jenis Antrian", ["Antrian Pelanggan Outlet", "Antrian Restok Bahan di Gudang"])

lambda_rate = st.number_input("Rata-rata kedatangan per jam (λ)", value=90 if mode == "Antrian Pelanggan Outlet" else 10.0)
mu_rate = st.number_input("Rata-rata pelayanan per jam per server (μ)", value=30.0 if mode == "Antrian Pelanggan Outlet" else 2.0)
c = st.number_input("Jumlah server/barista/petugas (c)", min_value=1, value=3 if mode == "Antrian Pelanggan Outlet" else 2)

rho = lambda_rate / (c * mu_rate)

st.subheader("📊 Hasil Evaluasi Antrian")
st.write(f"🔸 Utilisasi sistem (ρ): {rho:.2f}")

if rho >= 1:
    st.error("❌ Sistem tidak stabil! Tingkat kedatangan melebihi kapasitas pelayanan.")
else:
    st.success("✅ Sistem stabil")
    Lq = ((lambda_rate**2) / (mu_rate * (mu_rate - lambda_rate/c))) if c == 1 else None
    st.write("(Estimasi waktu tunggu dan panjang antrian lebih kompleks untuk c > 1, gunakan simulasi lanjut)")
