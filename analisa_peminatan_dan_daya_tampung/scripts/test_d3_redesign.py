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
df_d3 = pd.read_excel(excel_path, sheet_name='Diploma_3_Vokasi')

years = [2023, 2024, 2025, 2026]

# Aggregates for Panel A
macro_dt = [df_d3[f'Daya Tampung {y}'].sum() for y in years]
macro_du = [df_d3[f'Daftar Ulang {y}'].sum() for y in years]
macro_sisa = [dt - du for dt, du in zip(macro_dt, macro_du)]
macro_fr = [du / dt * 100.0 for dt, du in zip(macro_dt, macro_du)]

# Program studi data for Panel B
df_d3_clean = df_d3.copy()
df_d3_clean['Total_DT_4Y'] = sum(df_d3_clean[f'Daya Tampung {y}'] for y in years)
df_d3_clean['Total_DU_4Y'] = sum(df_d3_clean[f'Daftar Ulang {y}'] for y in years)
df_d3_clean['Total_Sisa_4Y'] = df_d3_clean['Total_DT_4Y'] - df_d3_clean['Total_DU_4Y']
df_d3_clean['Rata_FR_4Y'] = (df_d3_clean['Total_DU_4Y'] / df_d3_clean['Total_DT_4Y'] * 100.0).round(1)
df_d3_clean['FR_2026'] = (df_d3_clean['Daftar Ulang 2026'] / df_d3_clean['Daya Tampung 2026'] * 100.0).round(1)
df_d3_clean['Sisa_2026'] = df_d3_clean['Daya Tampung 2026'] - df_d3_clean['Daftar Ulang 2026']

def clean_d3_name(name):
    n = name.title().replace('D3 ', '').replace('D-Iii ', '')
    return f"D3 {n}"

df_d3_clean['Label_Prodi'] = df_d3_clean['Nama Program Studi'].apply(clean_d3_name)

# Sort by 4-year average fill rate
d3_sorted = df_d3_clean.sort_values('Rata_FR_4Y', ascending=True).reset_index(drop=True)

# Create Dual-Panel Figure
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(26, 10.5), dpi=300, gridspec_kw={'width_ratios': [1.0, 1.35]})

# -------------------------------------------------------------
# PANEL A: KINERJA MAKRO AGREGAT DIPLOMA 3 VOKASI (2023–2026)
# -------------------------------------------------------------
x_pos1 = np.arange(len(years))
w1 = 0.36

bars_dt = ax1.bar(x_pos1 - w1/2, macro_dt, width=w1, color='#F59E0B', edgecolor='#0F172A', linewidth=1.0, label='Target Daya Tampung D3', zorder=2)
bars_du = ax1.bar(x_pos1 + w1/2, macro_du, width=w1, color='#10B981', edgecolor='#0F172A', linewidth=1.0, label='Daftar Ulang Riil D3', zorder=2)

ax1.set_xticks(x_pos1)
ax1.set_xticklabels([f"Tahun {y}" for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_ylim(0, 850)
ax1.set_ylabel('Jumlah Mahasiswa / Kuota Kursi', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Kinerja Agregat & Defisit Kuota Tahunan D3 Vokasi (2023–2026)\nAkumulasi 4 Tahun: 1,320 Kursi Kosong (Keterisian Kumulatif Hanya 48.5%)', 
              fontsize=12.5, fontweight='bold', pad=12, color='#0F172A')
ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for idx, y in enumerate(years):
    dt_v = macro_dt[idx]
    du_v = macro_du[idx]
    sisa_v = macro_sisa[idx]
    fr_v = macro_fr[idx]
    
    # Text on Daya Tampung bar
    ax1.annotate(f"{dt_v} kursi", xy=(x_pos1[idx] - w1/2, dt_v), xytext=(0, 5), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#B45309')
    
    # Text on Daftar Ulang bar
    ax1.annotate(f"{du_v} mhs\n({fr_v:.1f}%)", xy=(x_pos1[idx] + w1/2, du_v), xytext=(0, 5), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#047857')
    
    # Deficit badge floating on top
    ax1.annotate(f"Defisit: {sisa_v} kursi", xy=(x_pos1[idx], max(dt_v, du_v)), xytext=(0, 32), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#991B1B',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.0),
                 arrowprops=dict(arrowstyle='->', color='#EF4444', lw=1.0, shrinkA=2, shrinkB=4))

# Callout banner at top of Panel A
tot_kuota = sum(macro_dt)
tot_mhs = sum(macro_du)
tot_defisit = sum(macro_sisa)
ax1.text(0.5, 0.04, f"TOTAL KUOTA 4 TAHUN: {tot_kuota} Kursi  |  TERISI: {tot_mhs} Mahasiswa  |  KOSONG: {tot_defisit} Kursi (51.5% Mubazir)",
         transform=ax1.transAxes, ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#991B1B',
         bbox=dict(boxstyle='square,pad=0.35', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.1))

ax1.legend(loc='upper left', frameon=True, fontsize=9.5, framealpha=0.95)

# -------------------------------------------------------------
# PANEL B: DIAGNOSTIK 11 PROGRAM STUDI D3 VOKASI
# -------------------------------------------------------------
y_pos2 = np.arange(len(d3_sorted))
colors_bars2 = ['#991B1B' if fr < 45.0 else '#D97706' if fr < 60.0 else '#059669' for fr in d3_sorted['Rata_FR_4Y']]

bars2 = ax2.barh(y_pos2, d3_sorted['Rata_FR_4Y'], color=colors_bars2, height=0.62, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

ax2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.6, label='Standar Keterisian Sehat (80%)', zorder=3)
ax2.axvline(50.0, color='#64748B', linestyle=':', linewidth=1.4, label='Batas Kritis Kelayakan (50%)', zorder=3)
ax2.axvspan(0, 50.0, color='#FEF2F2', alpha=0.4, zorder=0)

ax2.set_yticks(y_pos2)
ax2.set_yticklabels(d3_sorted['Label_Prodi'], fontsize=10.5, fontweight='bold', color='#1E293B')
ax2.set_xlim(0, 135)
ax2.set_ylim(-0.8, len(d3_sorted) - 0.2)
ax2.set_xlabel('Rata-rata Tingkat Keterisian Kuota 4 Tahun (2023–2026, %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Diagnostik 11 Program Studi D3 Vokasi (Kinerja Historis 2023–2026)\nMembedah Jurang Pemisah: Dari D3 Budidaya Peternakan (32.0%) hingga D3 Manajemen Informatika (68.8%)', 
              fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for i, r in d3_sorted.iterrows():
    fr4 = r['Rata_FR_4Y']
    du4 = int(r['Total_DU_4Y'])
    dt4 = int(r['Total_DT_4Y'])
    sisa4 = int(r['Total_Sisa_4Y'])
    fr26 = r['FR_2026']
    du26 = int(r['Daftar Ulang 2026'])
    dt26 = int(r['Daya Tampung 2026'])
    
    badge_txt = f"Rata 4Y: {fr4:.1f}% ({du4}/{dt4})  |  2026: {fr26:.1f}% ({du26}/{dt26})  |  Kosong: {sisa4} kursi"
    txt_c = '#991B1B' if fr4 < 45.0 else '#92400E' if fr4 < 60.0 else '#065F46'
    border_c = '#EF4444' if fr4 < 45.0 else '#F59E0B' if fr4 < 60.0 else '#10B981'
    bg_c = '#FEF2F2' if fr4 < 45.0 else '#FFFBEB' if fr4 < 60.0 else '#F0FDF4'
    
    ax2.annotate(badge_txt, xy=(fr4, i), xytext=(7, 0), textcoords='offset points',
                 va='center', ha='left', fontsize=8.4, fontweight='bold', color=txt_c,
                 bbox=dict(boxstyle='round,pad=0.20', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.92),
                 zorder=4)

legend_elements2 = [
    Patch(facecolor='#059669', edgecolor='#0F172A', label='Keterisian Moderat/Tinggi (≥60%)'),
    Patch(facecolor='#D97706', edgecolor='#0F172A', label='Keterisian Rentan (45%–59%)'),
    Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Keterisian Kritis (<45%) - Urgensi Penutupan/Konversi D4')
]
ax2.legend(handles=legend_elements2, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

plt.suptitle('EVALUASI MENYELURUH DAYA SERAP & KRISIS KUOTA 11 PROGRAM STUDI DIPLOMA 3 VOKASI USK (2023–2026)\nKombinasi Tren Makro Tahunan & Diagnostik Defisit per Program Studi Menuju Rasionalisasi Kuota 2027',
             fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
out_file = os.path.join(chart_dir, "08_evaluasi_multi_tahun_d3_vokasi.png")
plt.savefig(out_file, dpi=300)
plt.close()
print("Redesigned Chart 08 generated successfully at:", out_file)
