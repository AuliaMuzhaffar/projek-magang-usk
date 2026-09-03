import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

excel_path = 'tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'
chart_dir = 'tugas-5/analisa_peminatan_dan_daya_tampung/grafik'
df_all = pd.read_excel(excel_path, sheet_name='Rincian_Jalur_Semua_Tahun')

years = [2022, 2023, 2024, 2025, 2026]
jalurs = ['SNBT', 'SNBP', 'SMMPTN', 'TALENTA', 'SMC', 'ADIK']

jalur_colors = {
    'SNBT': '#1D4ED8',      # Royal Blue
    'SNBP': '#059669',      # Emerald Green
    'SMMPTN': '#EA580C',    # Amber / Orange
    'TALENTA': '#7C3AED',   # Royal Purple
    'SMC': '#0D9488',       # Dark Teal
    'ADIK': '#64748B'       # Slate Gray
}

# Aggregate data
data_du = {j: [] for j in jalurs}
data_gugur = {j: [] for j in jalurs}
data_yield = {j: [] for j in jalurs}
tot_du_yr = []
tot_gugur_yr = []

for yr in years:
    df_yr = df_all[df_all['Tahun Akademik'] == yr]
    grp = df_yr.groupby('Jalur Penerimaan').agg({
        'Mahasiswa Daftar Ulang': 'sum',
        'Calon Lulus Seleksi': 'sum',
        'Mundur / Gugur': 'sum'
    }).to_dict(orient='index')
    
    yr_du = 0
    yr_gugur = 0
    for j in jalurs:
        if j in grp:
            du = grp[j]['Mahasiswa Daftar Ulang']
            lulus = grp[j]['Calon Lulus Seleksi']
            gugur = grp[j]['Mundur / Gugur']
            y_rate = (du / lulus * 100.0) if lulus > 0 else np.nan
        else:
            du = 0
            gugur = 0
            y_rate = np.nan
        data_du[j].append(du)
        data_gugur[j].append(gugur)
        data_yield[j].append(y_rate)
        yr_du += du
        yr_gugur += gugur
    tot_du_yr.append(yr_du)
    tot_gugur_yr.append(yr_gugur)

# Build 3-Panel Executive Master Dashboard
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 8.5), dpi=300)

x = np.arange(len(years))
w = 0.52

# -------------------------------------------------------------
# PANEL 1: EVOLUSI KOMPOSISI MAHASISWA DAFTAR ULANG (INTAKE MIX)
# -------------------------------------------------------------
bottoms = np.zeros(len(years))
for j in jalurs:
    vals = np.array(data_du[j])
    ax1.bar(x, vals, bottom=bottoms, label=j, color=jalur_colors[j], width=w, edgecolor='#FFFFFF', linewidth=1.0, zorder=2)
    
    # Annotate significant segments
    for idx, (v, b) in enumerate(zip(vals, bottoms)):
        if v >= 600:
            pct = v / tot_du_yr[idx] * 100.0
            ax1.text(idx, b + v/2.0, f"{v:,}\n({pct:.0f}%)", ha='center', va='center',
                     fontsize=8.8, fontweight='bold', color='#FFFFFF', zorder=3)
        elif v >= 150:
            ax1.text(idx, b + v/2.0, f"{v:,}", ha='center', va='center',
                     fontsize=8.0, fontweight='bold', color='#FFFFFF', zorder=3)
    bottoms += vals

for idx, tot in enumerate(tot_du_yr):
    ax1.annotate(f"Total:\n{tot:,}", xy=(idx, tot), xytext=(0, 7), textcoords='offset points',
                 ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#0F172A',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.0),
                 zorder=4)

ax1.set_xticks(x)
ax1.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_ylim(0, max(tot_du_yr) * 1.25)
ax1.set_ylabel('Jumlah Mahasiswa Baru Daftar Ulang (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Dinamika Serapan Mahasiswa Baru per Jalur (2022–2026)\nIntake Tumbuh +34.9% (6,197 → 8,361 Mahasiswa)', 
              fontsize=12, fontweight='bold', pad=12, color='#1E40AF')
ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(loc='lower left', bbox_to_anchor=(0.02, 0.65), frameon=True, fontsize=9, framealpha=0.92)

# -------------------------------------------------------------
# PANEL 2: TREN YIELD RATE (%) PER JALUR 5 TAHUN
# -------------------------------------------------------------
markers = {'SNBT': 's', 'SNBP': 'o', 'SMMPTN': '^', 'TALENTA': 'D', 'SMC': 'v', 'ADIK': 'p'}
for j in jalurs:
    y_vals = data_yield[j]
    # Filter non-nan for line plotting
    valid_pts = [(years[i], y_vals[i]) for i in range(len(years)) if not np.isnan(y_vals[i])]
    if valid_pts:
        vx, vy = zip(*valid_pts)
        lw = 3.0 if j in ['SNBP', 'SNBT', 'TALENTA', 'SMMPTN'] else 2.0
        ms = 8 if j in ['SNBP', 'SNBT', 'TALENTA', 'SMMPTN'] else 6
        ax2.plot(vx, vy, label=f"{j}", color=jalur_colors[j], marker=markers[j],
                 linewidth=lw, markersize=ms, zorder=4)
        for px, py in valid_pts:
            offset_y = 10 if j in ['SNBP', 'SNBT'] else -15 if j == 'TALENTA' and px == 2026 else 8
            ax2.annotate(f"{py:.1f}%", xy=(px, py), xytext=(0, offset_y), textcoords='offset points',
                         ha='center', va='center', fontsize=8.5, fontweight='bold', color=jalur_colors[j],
                         bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor=jalur_colors[j], linewidth=0.7, alpha=0.9),
                         zorder=5)

ax2.axhline(80.0, color='#64748B', linestyle='--', linewidth=1.5, alpha=0.85, label='Batas Standar Sehat (80%)', zorder=2)
ax2.set_xticks(years)
ax2.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_ylim(15, 105)
ax2.set_ylabel('Tingkat Konversi Registrasi (Yield Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Tren Efisiensi Konversi Pendaftaran (Yield Rate 2022–2026)\nSorotan: Anjloknya Jalur TALENTA 2026 ke Titik Kritis 24.9%', 
              fontsize=12, fontweight='bold', pad=12, color='#065F46')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(loc='lower left', frameon=True, fontsize=8.8, framealpha=0.92)

# Callout for TALENTA collapse
ax2.annotate('CRASH KONVERSI TALENTA:\n935 dari 1,238 Calon Mhs\nMengundurkan Diri (75.1% Bocor)',
             xy=(2026, 24.9), xytext=(2024.5, 34.0),
             arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
             fontsize=8.5, fontweight='bold', color='#991B1B',
             bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=1.2),
             zorder=6)

# -------------------------------------------------------------
# PANEL 3: ESKALASI KEBOCORAN (GUGUR) PER JALUR 5 TAHUN
# -------------------------------------------------------------
bottoms_g = np.zeros(len(years))
for j in jalurs:
    vals_g = np.array(data_gugur[j])
    ax3.bar(x, vals_g, bottom=bottoms_g, label=j, color=jalur_colors[j], width=w, edgecolor='#FFFFFF', linewidth=1.0, zorder=2)
    
    for idx, (v, b) in enumerate(zip(vals_g, bottoms_g)):
        if v >= 350:
            ax3.text(idx, b + v/2.0, f"{v:,}", ha='center', va='center',
                     fontsize=8.8, fontweight='bold', color='#FFFFFF', zorder=3)
        elif v >= 100:
            ax3.text(idx, b + v/2.0, f"{v:,}", ha='center', va='center',
                     fontsize=8.0, fontweight='bold', color='#FFFFFF', zorder=3)
    bottoms_g += vals_g

for idx, tot in enumerate(tot_gugur_yr):
    ax3.annotate(f"Gugur:\n{tot:,}", xy=(idx, tot), xytext=(0, 7), textcoords='offset points',
                 ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#991B1B',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.0),
                 zorder=4)

ax3.set_xticks(x)
ax3.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax3.set_ylim(0, max(tot_gugur_yr) * 1.25)
ax3.set_ylabel('Jumlah Calon Mahasiswa Mengundurkan Diri (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax3.set_title('C. Eskalasi Kebocoran Pendaftaran per Jalur (2022–2026)\nKebocoran Membengkak +94.9% (1,231 → 2,399 Calon Mhs)', 
              fontsize=12, fontweight='bold', pad=12, color='#991B1B')
ax3.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.legend(loc='upper left', frameon=True, fontsize=9, framealpha=0.92)

plt.suptitle('PANORAMA DINAMIKA JALUR MASUK & ESKALASI KEBOCORAN PMB USK (2022–2026)\nAnalisis 5 Tahun: Pergeseran Kontribusi Intake Riil, Tren Yield Rate, dan Ledakan Calon Mahasiswa yang Mundur',
             fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
out_5y = "14_tren_jalur_masuk_dan_kebocoran_5_tahun_2022_2026.png"
plt.savefig(os.path.join(chart_dir, out_5y), dpi=300)
plt.close()
print(f"Generated {out_5y}")
