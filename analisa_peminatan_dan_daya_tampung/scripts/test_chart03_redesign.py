import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

excel_path = 'tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'
chart_dir = 'tugas-5/analisa_peminatan_dan_daya_tampung/grafik'

def normalize_cols(df):
    rev_map = {
        "Nama Program Studi": "Program_Studi",
        "Program Studi": "Program_Studi",
        "Fakultas": "Fakultas",
        "Jenjang": "Jenjang",
        "Slope DU (Orang/Thn)": "Slope_Tren_DU_Orang_Thn",
        "CAGR DU (%)": "CAGR_DU_Persen"
    }
    for yr in [2022, 2023, 2024, 2025, 2026]:
        rev_map[f"Peminat {yr}"] = f"Peminat_{yr}"
        rev_map[f"Daya Tampung {yr}"] = f"DT_{yr}"
        rev_map[f"Lulus Seleksi {yr}"] = f"LA_{yr}"
        rev_map[f"Daftar Ulang {yr}"] = f"DU_{yr}"
        rev_map[f"Kursi Kosong {yr}"] = f"Sisa_Kosong_{yr}"
    return df.rename(columns=rev_map)

df_s1 = normalize_cols(pd.read_excel(excel_path, sheet_name='S1_Kampus_Utama'))
years = [2022, 2023, 2024, 2025, 2026]

# Filter prodi with negative slope & CAGR
df_s1_decline = df_s1[(df_s1["DU_2022"] > 0) & (df_s1["CAGR_DU_Persen"] < 0)].copy()
df_s1_decline = df_s1_decline.sort_values(by="Slope_Tren_DU_Orang_Thn", ascending=True).head(6).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(16, 9.2), dpi=300)

colors = ["#DC2626", "#EA580C", "#7C3AED", "#BE185D", "#334155", "#0D9488"]
markers = ['o', 's', '^', 'D', 'v', 'P']

# Highly tailored offsets per prodi and year:
# 0: Manajemen: [266, 227, 206, 199, 199]
# 1: Ekonomi Islam: [165, 130, 130, 123, 122]
# 2: Ekonomi Pembangunan: [169, 141, 152, 145, 135]
# 3: Sosiologi: [108, 101, 102, 84, 92]
# 4: PSP Perikanan: [80, 83, 62, 71, 67]
# 5: Ilmu Kelautan: [119, 124, 104, 105, 113]
offsets_map = {
    0: [(0, 13), (0, 13), (0, 13), (0, 13), (0, 13)],       # Manajemen (always above)
    1: [(0, -15), (-14, -14), (0, -15), (0, 13), (0, 14)],   # Ekonomi Islam (below in 22-24, above in 25-26)
    2: [(0, 13), (14, 13), (0, 13), (0, 13), (0, 13)],       # Ekonomi Pembangunan (always above)
    3: [(0, -14), (0, -14), (0, -15), (0, -14), (0, -14)],   # Sosiologi (below)
    4: [(0, -14), (0, -14), (0, -15), (0, -14), (0, -14)],   # PSP Perikanan (below)
    5: [(0, 13), (0, -15), (0, 13), (0, -14), (0, -15)]      # Ilmu Kelautan (above 22, 24; below 23, 25, 26)
}

end_offsets = [
    (10, 0),    # Manajemen (199)
    (10, 7),    # Ekonomi Islam (122)
    (10, 0),    # Ekonomi Pembangunan (135)
    (10, 0),    # Sosiologi (92)
    (10, 0),    # PSP Perikanan (67)
    (10, -7)    # Ilmu Kelautan (113)
]

ax.set_xlim(2021.65, 2027.20)
ax.set_ylim(45, 290)
ax.grid(True, linestyle="--", alpha=0.45, color="#CBD5E1")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

fak_abbr = {
    'Ekonomi dan Bisnis': 'FEB',
    'Ilmu Sosial dan Ilmu Politik': 'FISIP',
    'Kelautan dan Perikanan': 'FPK',
    'ISIP': 'FISIP'
}

for idx, row in df_s1_decline.iterrows():
    y_series = [row[f"DU_{yr}"] for yr in years]
    c = colors[idx % len(colors)]
    m = markers[idx % len(markers)]
    f_txt = fak_abbr.get(str(row['Fakultas']).strip(), str(row['Fakultas']).strip())
    p_name = str(row['Program_Studi']).strip().title().replace('Psp', 'PSP')
    
    slope_val = row['Slope_Tren_DU_Orang_Thn']
    cagr_val = row['CAGR_DU_Persen']
    lbl = f"{p_name} ({f_txt})\nSlope: {slope_val:.1f} mhs/thn | CAGR: {cagr_val:.1f}%"
    
    ax.plot(years, y_series, marker=m, linewidth=3.0, markersize=8.5,
            color=c, markeredgecolor='white', markeredgewidth=2.0, alpha=0.95, label=lbl, zorder=3)
    
    # Pill data labels at every point
    offsets = offsets_map.get(idx, [(0, 12)] * 5)
    for yr, val, (ox, oy) in zip(years, y_series, offsets):
        ax.annotate(f"{int(val)}", xy=(yr, val), xytext=(ox, oy), textcoords='offset points',
                    ha='center', va='center', fontsize=9.2, fontweight='bold', color=c,
                    bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor=c, alpha=0.95, linewidth=1.0),
                    zorder=4)

    # End-of-line summary badge (contraction percentage)
    growth_pct = (y_series[-1] - y_series[0]) / y_series[0] * 100
    e_ox, e_oy = end_offsets[idx]
    ax.annotate(f"  {int(y_series[-1])} mhs ({growth_pct:.0f}%)", xy=(2026, y_series[-1]), xytext=(e_ox, e_oy),
                textcoords='offset points', va='center', ha='left', fontsize=9.8, fontweight='bold', color=c,
                zorder=4)

# Place Contextual Alert Box in the spacious upper right area (x=0.48 to 0.98, y=0.95)
ax.text(0.50, 0.94, 
        "TEMUAN STRATEGIS REKTORAT:\n"
        "• Episentrum Penurunan: 3 Prodi FEB (Manajemen, Ekonomi Islam, Ekonomi Pembangunan)\n"
        "  kehilangan 144 mahasiswa baru per angkatan dibanding 2022 (-24.0% kontraksi gabungan).\n"
        "• Manajemen & Ekonomi Islam tidak pernah rebound (0x naik dalam 4 tahun berturut-turut).\n"
        "• PSP Perikanan & Sosiologi konsisten mencatat tren penurunan di bawah 100 mahasiswa.",
        transform=ax.transAxes, ha='left', va='top', fontsize=9.0, fontweight='bold', color='#991B1B',
        bbox=dict(boxstyle='round,pad=0.45', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.1, alpha=0.96),
        zorder=2)

ax.set_xticks(years)
ax.set_xticklabels(['2022', '2023', '2024', '2025', '2026'], fontsize=11.5, fontweight='bold', color='#1E293B')
ax.tick_params(axis='y', labelsize=10.5, labelcolor='#1E293B')
ax.set_xlabel("Tahun Akademik Penerimaan", fontsize=12, fontweight='bold', labelpad=12, color='#0F172A')
ax.set_ylabel("Jumlah Mahasiswa Baru Daftar Ulang (Orang)", fontsize=12, fontweight='bold', labelpad=12, color='#0F172A')
ax.set_title("TREN PENURUNAN PROGRAM STUDI S1 DENGAN KONTRAKSI TERDALAM (2022–2026)\nEvaluasi Berdasarkan Slope Regresi Linier Negatif Terbesar & Laju Penurunan CAGR Majemuk", 
             fontsize=13.5, fontweight='bold', pad=22, color='#0F172A')

legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=True, 
                   fontsize=9.2, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.98, 
                   columnspacing=2.0, labelspacing=0.8, handlelength=2.5, handletextpad=0.8)
legend.get_frame().set_linewidth(1.2)

plt.tight_layout(rect=[0.02, 0.10, 0.98, 0.96])
out_file = os.path.join(chart_dir, "03_top_tren_penurunan_pendaftar_dan_peminat.png")
plt.savefig(out_file, dpi=300)
plt.close()
print("Refined Chart 03 saved successfully at:", out_file)
