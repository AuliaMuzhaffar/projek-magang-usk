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
df_master = pd.read_excel(excel_path, sheet_name='Master_Semua_Prodi')

years = [2022, 2023, 2024, 2025, 2026]
tot_pm = [df_master[f'Peminat {yr}'].sum() for yr in years]
tot_dt = [df_master[f'Daya Tampung {yr}'].sum() for yr in years]
tot_du = [df_master[f'Daftar Ulang {yr}'].sum() for yr in years]
fill_rates = [tot_du[i] / tot_dt[i] * 100.0 for i in range(5)]
gaps = [tot_dt[i] - tot_du[i] for i in range(5)]

# Create Dual-Panel Figure with optimal aspect ratio
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(21, 9.2), dpi=300, gridspec_kw={'width_ratios': [1.0, 1.25]})

# -------------------------------------------------------------
# PANEL A: SISI PERMINTAAN PASAR (DEMAND SIDE) - TREN PEMINAT
# -------------------------------------------------------------
x_pos1 = np.arange(len(years))
bars_pm = ax1.bar(x_pos1, [p / 1000.0 for p in tot_pm], width=0.48, color='#0284C7', edgecolor='#0F172A', linewidth=1.1, zorder=2, alpha=0.92)

# Line overlay with markers
ax1.plot(x_pos1, [p / 1000.0 for p in tot_pm], color='#0369A1', marker='o', linewidth=3.0, markersize=8.5, 
         markerfacecolor='#FFFFFF', markeredgecolor='#0369A1', markeredgewidth=2.2, zorder=3)

ax1.set_xticks(x_pos1)
ax1.set_xticklabels([f"Tahun {y}" for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_ylim(0, 95)
ax1.set_ylabel('Jumlah Peminat Pendaftar (Ribu Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Dinamika Pasar: Ledakan Minat Calon Mahasiswa Baru (2022–2026)\nAkumulasi 5 Tahun: 297,872 Peminat (+39.5% Pertumbuhan, Rebound Kuat Pasca PTN-BH)', 
              fontsize=12.2, fontweight='bold', pad=14, color='#0F172A')
ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Annotations on Panel A bars
for idx, (p, y) in enumerate(zip(tot_pm, years)):
    p_k = p / 1000.0
    if idx == 0:
        yoy_txt = "Basis Awal"
    else:
        prev_p = tot_pm[idx - 1]
        yoy_val = (p - prev_p) / prev_p * 100.0
        yoy_txt = f"+{yoy_val:.1f}% YoY" if yoy_val > 0 else f"{yoy_val:.1f}% YoY"
    
    badge_label = f"{p:,} orang\n({yoy_txt})"
    y_offset = 14 if idx == 2 else 8
    ax1.annotate(badge_label, xy=(x_pos1[idx], p_k), xytext=(0, y_offset), textcoords='offset points',
                 ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#0369A1',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#F0F9FF', edgecolor='#0284C7', linewidth=0.9, alpha=0.95),
                 zorder=4)

# Momentum callouts in Panel A
ax1.annotate('Integrasi D3 Vokasi\nke SNPMB Nasional', xy=(x_pos1[1], tot_pm[1]/1000.0), xytext=(x_pos1[1] - 0.25, 26),
             fontsize=8.5, fontweight='bold', color='#475569',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#F8FAFC', edgecolor='#94A3B8', linewidth=0.8),
             arrowprops=dict(arrowstyle='->', color='#64748B', lw=1.1, shrinkA=2, shrinkB=4))

ax1.annotate('Transformasi PTN-BH:\nLonjakan Peminat (+46.7%)', xy=(x_pos1[2], 75), xytext=(x_pos1[2] - 0.35, 84),
             fontsize=8.5, fontweight='bold', color='#0369A1',
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=0.9),
             arrowprops=dict(arrowstyle='->', color='#0284C7', lw=1.1, shrinkA=2, shrinkB=2))

# Bottom banner Panel A
tot_peminat_5thn = sum(tot_pm)
growth_overall = (tot_pm[-1] - tot_pm[0]) / tot_pm[0] * 100.0
ax1.text(0.5, 0.04, f"TOTAL PEMINAT 5 TAHUN: {tot_peminat_5thn:,} Orang  |  PERTUMBUHAN: +{growth_overall:.1f}%  |  CAGR: +8.7%/Tahun",
         transform=ax1.transAxes, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#0369A1',
         bbox=dict(boxstyle='square,pad=0.35', facecolor='#E0F2FE', edgecolor='#0284C7', linewidth=1.1))

# -------------------------------------------------------------
# PANEL B: SISI KAPASITAS & SERAPAN (SUPPLY & CONVERSION SIDE)
# -------------------------------------------------------------
x_pos2 = np.arange(len(years))
w2 = 0.35

bars_dt = ax2.bar(x_pos2 - w2/2, tot_dt, width=w2, color='#F59E0B', edgecolor='#0F172A', linewidth=1.0, label='Target Daya Tampung Kuota', zorder=2)
bars_du = ax2.bar(x_pos2 + w2/2, tot_du, width=w2, color='#10B981', edgecolor='#0F172A', linewidth=1.0, label='Daftar Ulang Riil Mahasiswa', zorder=2)

ax2.set_xticks(x_pos2)
ax2.set_xticklabels([f"Tahun {y}" for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_ylim(0, 14200)
ax2.set_ylabel('Jumlah Kuota Kursi & Mahasiswa (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Realitas Kapasitas: Over-Ekspansi Kuota vs Defisit Bangku Kosong (2022–2026)\nAkumulasi 5 Tahun: 10,984 Bangku Kosong (23.0% dari 47,738 Kuota Berakhir Terbuang)', 
              fontsize=12.2, fontweight='bold', pad=14, color='#B45309')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for idx, y in enumerate(years):
    dt_v = tot_dt[idx]
    du_v = tot_du[idx]
    gap_v = gaps[idx]
    fr_v = fill_rates[idx]
    
    # Text on Daya Tampung bar
    ax2.annotate(f"{dt_v:,}\nkuota", xy=(x_pos2[idx] - w2/2, dt_v), xytext=(0, 4), textcoords='offset points',
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#B45309')
    
    # Text on Daftar Ulang bar
    ax2.annotate(f"{du_v:,}\nmasuk", xy=(x_pos2[idx] + w2/2, du_v), xytext=(0, 4), textcoords='offset points',
                 ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#047857')
    
    # Deficit callout floating on top
    badge_c = '#FEF2F2' if fr_v < 80.0 else '#ECFDF5'
    border_c = '#EF4444' if fr_v < 80.0 else '#10B981'
    txt_c = '#991B1B' if fr_v < 80.0 else '#065F46'
    
    ax2.annotate(f"Defisit: {gap_v:,} kursi\nKeterisian: {fr_v:.1f}%", xy=(x_pos2[idx], dt_v), xytext=(0, 28), textcoords='offset points',
                 ha='center', va='bottom', fontsize=8.6, fontweight='bold', color=txt_c,
                 bbox=dict(boxstyle='round,pad=0.22', facecolor=badge_c, edgecolor=border_c, linewidth=1.0),
                 arrowprops=dict(arrowstyle='->', color=border_c, lw=1.0, shrinkA=2, shrinkB=4))

# Bottom banner Panel B
tot_dt_5thn = sum(tot_dt)
tot_du_5thn = sum(tot_du)
tot_gap_5thn = sum(gaps)
rata_fr_5thn = tot_du_5thn / tot_dt_5thn * 100.0

ax2.text(0.5, 0.04, f"TOTAL KUOTA 5 TAHUN: {tot_dt_5thn:,} Kursi  |  TERISI: {tot_du_5thn:,} Mahasiswa  |  KOSONG: {tot_gap_5thn:,} Kursi ({100-rata_fr_5thn:.1f}% Mubazir)",
         transform=ax2.transAxes, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#991B1B',
         bbox=dict(boxstyle='square,pad=0.35', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.1))

ax2.legend(loc='upper left', frameon=True, fontsize=9.5, framealpha=0.95)

plt.suptitle('PANORAMA EVALUASI TREN MAKRO UNIVERSITAS SYIAH KUALA (2022–2026)\nDekonstruksi Paradoks PMB: Minat Melimpah Ruah (+39.5%), Namun Defisit Kuota Kronis (10,984 Kursi Terbuang)',
             fontsize=14.0, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
out_file = os.path.join(chart_dir, "01_tren_makro_peminat_dt_du_usk.png")
plt.savefig(out_file, dpi=300)
plt.close()
print("Refined Chart 01 saved at:", out_file)
