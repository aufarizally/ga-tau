import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Fungsi perhitungan
def total_waktu_produksi(x, y):
    return 2 * x*2 + 3 * x * y + y*2

def turunan_parsial(x, y):
    dT_dx = 4 * x + 3 * y
    dT_dy = 3 * x + 2 * y
    return dT_dx, dT_dy

def waktu_baku(waktu_normal, toleransi):
    return waktu_normal * (1 + toleransi)

# Fungsi Simulasi variasi toleransi, pekerja, dan jam kerja
def simulasi_dinamis(waktu_normal):
    data = []
    for toleransi in range(0, 10):  # 0% sampai 9%
        for jumlah_pekerja in range(5, 11, 1):  # dari 5 ke 10 pekerja
            for jam_kerja in range(4, 13, 2):  # dari 4 sampai 12 jam
                wb = waktu_baku(waktu_normal, toleransi / 100)
                total_jam = jumlah_pekerja * jam_kerja
                unit = total_jam / wb if wb > 0 else 0
                data.append({
                    "Toleransi (%)": toleransi,
                    "Jumlah Pekerja": jumlah_pekerja,
                    "Jam Kerja per Hari": jam_kerja,
                    "Waktu Baku (jam)": round(wb, 2),
                    "Total Jam Kerja (jam)": total_jam,
                    "Unit Mobil": int(unit)
                })
    return pd.DataFrame(data)

# Antarmuka Streamlit
st.title("🚗 Aplikasi Analisis Waktu Baku Produksi Mobil")

# Input Pengguna
st.sidebar.header("📥 Input Aktivitas Produksi")
x = st.sidebar.number_input("Waktu Perakitan Mesin (x) [jam]", min_value=0.0, value=2.0, step=0.5)
y = st.sidebar.number_input("Waktu Pemasangan Bodi (y) [jam]", min_value=0.0, value=3.0, step=0.5)
toleransi_persen = st.sidebar.slider("Toleransi (%)", min_value=0, max_value=30, value=15)
jumlah_pekerja = st.sidebar.slider("Jumlah Pekerja", 1, 100, 10)
jam_kerja_per_hari = st.sidebar.slider("Jam Kerja per Hari", 4, 24, 8)

# Perhitungan Dasar
waktu_total = total_waktu_produksi(x, y)
dT_dx, dT_dy = turunan_parsial(x, y)
wb = waktu_baku(waktu_total, toleransi_persen / 100)

# Tampilkan Hasil
st.header("📊 Hasil Perhitungan Produksi")
st.write(f"*Total Waktu Produksi (T):* {waktu_total:.2f} jam")
st.write(f"*Turunan Parsial terhadap x (∂T/∂x):* {dT_dx:.2f}")
st.write(f"*Turunan Parsial terhadap y (∂T/∂y):* {dT_dy:.2f}")
st.write(f"*Toleransi:* {toleransi_persen}%")
st.write(f"*Waktu Baku (WB):* {wb:.2f} jam")

# Grafik Turunan Parsial
st.subheader("📈 Grafik Pengaruh Aktivitas terhadap Waktu Produksi")
fig, ax = plt.subplots()
aktivitas = ['Perakitan Mesin (x)', 'Pemasangan Bodi (y)']
pengaruh = [dT_dx, dT_dy]
warna = ['#FF6F61', '#6BAED6']
bars = ax.bar(aktivitas, pengaruh, color=warna)
ax.set_ylabel("Pengaruh terhadap Total Waktu (jam)")
ax.set_title("Turunan Parsial ∂T/∂x dan ∂T/∂y")
ax.grid(True, axis='y', linestyle='--', alpha=0.6)
for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'{yval:.1f}', ha='center', va='bottom', fontweight='bold')
st.pyplot(fig)

# Estimasi Produksi
total_jam_harian = jumlah_pekerja * jam_kerja_per_hari
unit_mobil_harian = total_jam_harian / wb if wb > 0 else 0
unit_mesin_harian = total_jam_harian / x if x > 0 else 0
st.subheader("🚀 Estimasi Produksi Harian")
st.write(f"*Jumlah Pekerja:* {jumlah_pekerja} orang")
st.write(f"*Jam Kerja per Hari:* {jam_kerja_per_hari} jam")
st.write(f"*Total Jam Kerja Harian:* {total_jam_harian} jam")
st.write(f"*Mobil yang Bisa Dirakit per Hari:* {unit_mobil_harian:.2f} unit")
st.write(f"*Unit Mesin yang Dirakit (x = {x} jam):* {unit_mesin_harian:.0f} unit per hari")

# Tabel Simulasi Dinamis
st.subheader("📋 Tabel Simulasi Variasi Input")
df_simulasi = simulasi_dinamis(waktu_total)
st.dataframe(df_simulasi)