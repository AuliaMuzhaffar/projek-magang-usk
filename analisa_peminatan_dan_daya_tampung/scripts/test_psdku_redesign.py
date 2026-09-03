import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

excel_path = 'tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'
chart_dir = 'tugas-5/analisa_peminatan_dan_daya_tampung/grafik'
df_psdku = pd.read_excel(excel_path, sheet_name='PSDKU_Gayo_Lues')

years = [2022, 2023, 2024, 2025, 2026]

# Panel A: Annual Aggregates
macro_dt = [df_psdku[f'Daya Tampung {y}'].sum() for y in years]
macro_du = [df_psdku[f'Daftar Ulang {y}'].sum() for y in years]
macro_sisa = [dt - du for dt, du in zip(macro_dt, macro_du)]
macro_fr = [du / dt * 100.0 for dt, du in zip(macro_dt, macro_du)]

# Panel B: 4 Program Studi Diagnostics
df_clean = df_psdku.copy()
df_clean['Total_DT_5Y'] = sum(df_clean[f'Daya Tampung {y}'] for y in years)
df_clean['Total_DU_5Y'] = sum(df_clean[f'Daftar Ulang {y}'] for y in years)
df_clean['Total_Sisa_5Y'] = df_clean['Total_DT_5Y'] - df_clean['Total_DU_5Y']
df_clean['Rata_FR_5Y'] = (df_clean['Total_DU_5Y'] / df_clean['Total_DT_5Y'] * 100.0).round(1)
df_clean['FR_2026'] = (df_clean['Daftar Ulang 2026'] / df_clean['Daya Tampung 2026'] * 100.0).round(1)
df_clean['Sisa_2026'] = df_clean['Daya Tampung 2026'] - df_clean['Daftar Ulang 2026']

def clean_psdku_name(name):
    n = name.replace('(PDD GAYO LUES)', '').replace('(Gayo Lues)', '').strip().title()
    return f"{n} (Gayo Lues)"

df_clean['Label_Prodi'] = df_clean['Nama Program Studi'].apply(clean_psdku_name)
psdku_sorted = df_clean.sort_values('Rata_FR_5Y', ascending=True).reset_index(drop=True)

# Create Dual-Panel Figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(25, 10), dpi=300, gridspec_kw={'width_ratios': [1.05, 1.25]})

# -------------------------------------------------------------
# PANEL A: TREN JURANG KUOTA VS REALISASI PSDKU (2022–2026)
# -------------------------------------------------------------
x_pos1 = np.arange(len(years))
w1 = 0.35

bars_dt = ax1.bar(x_pos1 - w1/2, macro_dt, width=w1, color='#F59E0B', edgecolor='#0F172A', linewidth=1.0, label='Target Daya Tampung Kuota', zorder=2)
bars_du = ax1.bar(x_pos1 + w1/2, macro_du, width=w1, color='#0284C7', edgecolor='#0F172A', linewidth=1.0, label='Daftar Ulang Riil Mahasiswa', zorder=2)

ax1.set_xticks(x_pos1)
ax1.set_xticklabels([f"Tahun {y}" for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_ylim(0, 275)
ax1.set_ylabel('Jumlah Mahasiswa / Kuota Kursi', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Jurang Daya Tampung vs Mahasiswa Masuk Riil PSDKU Gayo Lues (2022–2026)\nAkumulasi 5 Tahun: 783 Kursi Kosong (Keterisian Kumulatif Hanya 25.4% / 74.6% Mubazir)', 
              fontsize=12.2, fontweight='bold', pad=12, color='#0F172A')
ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for idx, y in enumerate(years):
    dt_v = macro_dt[idx]
    du_v = macro_du[idx]
    sisa_v = macro_sisa[idx]
    fr_v = macro_fr[idx]
    
    # Text on Daya Tampung bar
    ax1.annotate(f"{dt_v} kursi", xy=(x_pos1[idx] - w1/2, dt_v), xytext=(0, 4), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#B45309')
    
    # Text on Daftar Ulang bar
    ax1.annotate(f"{du_v} mhs\n({fr_v:.1f}%)", xy=(x_pos1[idx] + w1/2, du_v), xytext=(0, 4), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#0369A1')
    
    # Deficit badge floating on top
    ax1.annotate(f"Defisit: {sisa_v} kursi\n({100-fr_v:.1f}% Kosong)", xy=(x_pos1[idx], dt_v), xytext=(0, 24), textcoords='offset points',
                 ha='center', va='bottom', fontsize=8.6, fontweight='bold', color='#991B1B',
                 bbox=dict(boxstyle='round,pad=0.22', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.0),
                 arrowprops=dict(arrowstyle='->', color='#EF4444', lw=1.0, shrinkA=2, shrinkB=4))

# Callout banner at top of Panel A
tot_kuota = sum(macro_dt)
tot_mhs = sum(macro_du)
tot_defisit = sum(macro_sisa)
ax1.text(0.5, 0.04, f"TOTAL KUOTA 5 TAHUN: {tot_kuota} Kursi  |  TERISI: {tot_mhs} Mahasiswa  |  KOSONG: {tot_defisit} Kursi (74.6% Mubazir)",
         transform=ax1.transAxes, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#991B1B',
         bbox=dict(boxstyle='square,pad=0.35', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.1))

ax1.legend(loc='upper left', frameon=True, fontsize=9.5, framealpha=0.95)

# -------------------------------------------------------------
# PANEL B: DIAGNOSTIK 4 PROGRAM STUDI PSDKU GAYO LUES
# -------------------------------------------------------------
y_pos2 = np.arange(len(psdku_sorted))
colors_bars2 = ['#991B1B' for _ in range(len(psdku_sorted))]

bars2 = ax2.barh(y_pos2, psdku_sorted['Rata_FR_5Y'], color=colors_bars2, height=0.55, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

ax2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.6, label='Standar Keterisian Sehat (80%)', zorder=3)
ax2.axvline(50.0, color='#EA580C', linestyle=':', linewidth=1.4, label='Batas Kritis Kelayakan Kelas Mandiri (50%)', zorder=3)
ax2.axvspan(0, 50.0, color='#FEF2F2', alpha=0.45, zorder=0)

ax2.set_yticks(y_pos2)
ax2.set_yticklabels(psdku_sorted['Label_Prodi'], fontsize=11.0, fontweight='bold', color='#1E293B')
ax2.set_xlim(0, 115)
ax2.set_ylim(-0.8, len(psdku_sorted) - 0.2)
ax2.set_xlabel('Rata-rata Tingkat Keterisian Kuota 5 Tahun (2022–2026, %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Diagnostik 4 Program Studi PSDKU Gayo Lues (Kinerja Historis 5 Tahun)\nSeluruh Program Studi Berada di Bawah 30% Keterisian (Zona Krisis Akut Permanen)', 
              fontsize=12.2, fontweight='bold', pad=12, color='#991B1B')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for i, r in psdku_sorted.iterrows():
    fr5 = r['Rata_FR_5Y']
    du5 = int(r['Total_DU_5Y'])
    dt5 = int(r['Total_DT_5Y'])
    sisa5 = int(r['Total_Sisa_5Y'])
    fr26 = r['FR_2026']
    du26 = int(r['Daftar Ulang 2026'])
    dt26 = int(r['Daya Tampung 2026'])
    
    badge_txt = f"Rata 5-Thn: {fr5:.1f}% ({du5}/{dt5})  |  2026: {fr26:.1f}% ({du26}/{dt26})  |  Defisit 5-Thn: {sisa5} kursi"
    txt_c = '#991B1B'
    border_c = '#EF4444'
    bg_c = '#FEF2F2'
    
    ax2.annotate(badge_txt, xy=(fr5, i), xytext=(7, 0), textcoords='offset points',
                 va='center', ha='left', fontsize=8.6, fontweight='bold', color=txt_c,
                 bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.95),
                 zorder=4)

legend_elements2 = [
    Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Krisis Akut Ekstrem (<30%) — Seluruh Prodi PSDKU Terperangkap di Zona Ini')
]
ax2.legend(handles=legend_elements2, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=1, frameon=True, fontsize=9.0, framealpha=0.95)

plt.suptitle('EVALUASI MENYELURUH DAYA SERAP & INEFISIENSI OPERASIONAL PSDKU GAYO LUES (2022–2026)\nAnomali Geografis & Isolasi Demografis: Pembuktian Ilmiah Krisis Kuota Kampus Cabang Terpencil',
             fontsize=14.0, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
out_file = os.path.join(chart_dir, "09_subanalisis_psdku_gayo_lues.png")
plt.savefig(out_file, dpi=300)
plt.close()
print("Redesigned Chart 09 generated successfully at:", out_file)
