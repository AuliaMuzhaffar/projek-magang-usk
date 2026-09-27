import os
import pandas as pd

# Path ke file master
script_dir = os.path.dirname(os.path.abspath(__file__))
file_master = os.path.abspath(os.path.join(script_dir, '..', 'data', 'master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'))

print("=" * 75)
print("   BUKTI STATISTIK TINGKAT KETERISIAN KUOTA UNIVERSITAS SYIAH KUALA")
print("               (Sumber Data: 66 Prodi S1 Kampus Utama)")
print("=" * 75)

df = pd.read_excel(file_master, sheet_name='S1_Kampus_Utama')

# 1. Agregat Total Universitas per Tahun
print("\n[A] REKAPITULASI TOTAL UNIVERSITAS (TOTAL DAFTAR ULANG / TOTAL KUOTA)")
print("-" * 75)
print(f"{'Tahun':<10} | {'Total Kuota':<15} | {'Daftar Ulang':<15} | {'Keterisian USK (%)':<20}")
print("-" * 75)

total_kuota_5th = 0
total_du_5th = 0

for y in [2022, 2023, 2024, 2025, 2026]:
    dt = df[f'Daya Tampung {y}'].sum()
    du = df[f'Daftar Ulang {y}'].sum()
    rate = (du / dt) * 100
    total_kuota_5th += dt
    total_du_5th += du
    print(f"{y:<10} | {dt:>12,}    | {du:>12,}    | {rate:>15.2f}%")

print("-" * 75)
rate_5th = (total_du_5th / total_kuota_5th) * 100
print(f"{'5 TAHUN':<10} | {total_kuota_5th:>12,}    | {total_du_5th:>12,}    | {rate_5th:>15.2f}% (~80%)")
print("-" * 75)

# 2. Statistik Sebaran per Program Studi
print("\n[B] STATISTIK SEBARAN PER PROGRAM STUDI (MEAN & MEDIAN PRODI)")
print("-" * 75)
print(f"{'Tahun':<10} | {'Rata-rata (Mean)':<18} | {'Nilai Tengah (Median)':<22} | {'Prodi >= 80%':<15}")
print("-" * 75)

for y in [2022, 2023, 2024, 2025, 2026]:
    col = f'Fill Rate {y} (%)'
    mean_v = df[col].mean()
    med_v = df[col].median()
    above_80 = (df[col] >= 80).sum()
    print(f"{y:<10} | {mean_v:>14.2f}%   | {med_v:>18.2f}%   | {above_80}/66 ({above_80/66*100:.1f}%)")

print("-" * 75)
col_5th = 'Rata Fill Rate 5-Thn (%)'
mean_5th = df[col_5th].mean()
med_5th = df[col_5th].median()
above_80_5th = (df[col_5th] >= 80).sum()
print(f"{'5 TAHUN':<10} | {mean_5th:>14.2f}%   | {med_5th:>18.2f}%   | {above_80_5th}/66 ({above_80_5th/66*100:.1f}%)")
print("-" * 75)

print("\n[KESIMPULAN METODOLOGI]")
print(f"1. Total Agregat USK 5 Tahun berada di angka {rate_5th:.2f}% (Tepat dibulatkan 80%).")
print(f"2. Nilai Median 5 Tahun per Prodi adalah {med_5th:.2f}% (Membelah persis 50% prodi di atas vs 50% di bawah).")
print(f"3. Pada tahun 2026, rata-rata prodi mencapai {df['Fill Rate 2026 (%)'].mean():.2f}% dengan median {df['Fill Rate 2026 (%)'].median():.2f}%.")
print("=" * 75)
