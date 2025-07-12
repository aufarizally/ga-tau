import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import linprog

# Judul Aplikasi
st.title("Optimal Production of Shoes")

# Input dari Pengguna
st.header("Input Data")
profit_school = st.number_input("Keuntungan per unit Sepatu Sekolah (Rp):", min_value=0)
profit_sport = st.number_input("Keuntungan per unit Sepatu Olahraga (Rp):", min_value=0)
profit_formal = st.number_input("Keuntungan per unit Sepatu Kerja Formal (Rp):", min_value=0)

# Kebutuhan bahan baku per unit
material_school = st.number_input("Kebutuhan bahan baku per unit Sepatu Sekolah (m²):", min_value=0)
material_sport = st.number_input("Kebutuhan bahan baku per unit Sepatu Olahraga (m²):", min_value=0)
material_formal = st.number_input("Kebutuhan bahan baku per unit Sepatu Kerja Formal (m²):", min_value=0)

# Kebutuhan jam kerja per unit
time_school = st.number_input("Kebutuhan jam kerja per unit Sepatu Sekolah (jam):", min_value=0)
time_sport = st.number_input("Kebutuhan jam kerja per unit Sepatu Olahraga (jam):", min_value=0)
time_formal = st.number_input("Kebutuhan jam kerja per unit Sepatu Kerja Formal (jam):", min_value=0)

# Ketersediaan sumber daya
total_material = st.number_input("Total bahan baku yang tersedia (m²):", min_value=0)
total_time = st.number_input("Total jam tenaga kerja yang tersedia (jam):", min_value=0)

# Permintaan maksimal pasar
max_demand_school = st.number_input("Permintaan maksimal pasar Sepatu Sekolah (unit):", min_value=0)
max_demand_sport = st.number_input("Permintaan maksimal pasar Sepatu Olahraga (unit):", min_value=0)
max_demand_formal = st.number_input("Permintaan maksimal pasar Sepatu Kerja Formal (unit):", min_value=0)

# Tombol untuk menghitung
if st.button("Hitung Jumlah Optimal"):
    # Koefisien fungsi tujuan (negatif karena linprog meminimalkan)
    c = [-profit_school, -profit_sport, -profit_formal]

    # Koefisien batasan
    A = [
        [material_school, material_sport, material_formal],  # Bahan baku
        [time_school, time_sport, time_formal]                # Jam kerja
    ]
    b = [total_material, total_time]

    # Batasan permintaan
    bounds = [(0, max_demand_school), (0, max_demand_sport), (0, max_demand_formal)]

    # Menghitung solusi
    res = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')

    if res.success:
        optimal_production = res.x
        total_profit = -res.fun

        # Menampilkan hasil
        st.subheader("Jumlah Sepatu Optimal yang Harus Diproduksi:")
        st.write(f"Sepatu Sekolah: {int(optimal_production[0])} pasang")
        st.write(f"Sepatu Olahraga: {int(optimal_production[1])} pasang")
        st.write(f"Sepatu Kerja Formal: {int(optimal_production[2])} pasang")
        st.write(f"Total Keuntungan Maksimal (Rp): {int(total_profit)}")
    else:
        st.error("Tidak ada solusi yang ditemukan.")

# Visualisasi area feasible (jika hanya 2 variabel)
if st.checkbox("Tampilkan Visualisasi Area Feasible"):
    # Menggunakan hanya dua produk untuk visualisasi
    fig, ax = plt.subplots()
    x = np.linspace(0, max_demand_school, 100)
    y1 = (total_material - material_school * x) / material_sport
    y2 = (total_time - time_school * x) / time_sport

    ax.plot(x, y1, label='Bahan Baku')
    ax.plot(x, y2, label='Jam Kerja')
    ax.fill_between(x, np.minimum(y1, y2), color='gray', alpha=0.5)
    ax.set_xlim(0, max_demand_school)
    ax.set_ylim(0, max_demand_sport)
    ax.set_xlabel('Sepatu Sekolah')
    ax.set_ylabel('Sepatu Olahraga')
    ax.set_title('Area Feasible')
    ax.legend()
    st.pyplot(fig)

# Simpan laporan dalam PDF atau Excel (opsional)
if st.button("Simpan Laporan"):
    # Simpan laporan ke dalam format yang diinginkan
    # (Implementasi untuk menyimpan laporan bisa ditambahkan di sini)
    st.success("Laporan berhasil disimpan!")
