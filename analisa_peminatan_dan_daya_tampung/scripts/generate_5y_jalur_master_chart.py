import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'))
chart_dir = os.path.abspath(os.path.join(script_dir, '..', 'grafik'))
os.makedirs(chart_dir, exist_ok=True)
df_all = pd.read_excel(excel_path, sheet_name='Rincian_Jalur_Semua_Tahun')

years = [2022, 2023, 2024, 2025, 2026]
jalurs = ['SNBT', 'SNBP', 'SMMPTN', 'TALENTA', 'SMC', 'ADIK']
jalurs_yield = ['SNBT', 'SNBP', 'SMMPTN', 'TALENTA', 'SMC']

jalur_colors = {
    'SNBT': '#1D4ED8',      # Royal Blue
    'SNBP': '#059669',      # Emerald Green
    'SMMPTN': '#EA580C',    # Amber / Orange
    'TALENTA': '#7C3AED',   # Royal Purple
    'SMC': '#0D9488',       # Dark Teal
    'ADIK': '#64748B'       # Slate Gray
}
markers = {
    'SNBT': 's', 
    'SNBP': 'o', 
    'SMMPTN': '^', 
    'TALENTA': 'D', 
    'SMC': 'v'
}

# Aggregate data
data_du = {j: [] for j in jalurs}
tot_du_yr = []
data_gugur = {j: [] for j in jalurs}
tot_gugur_yr = []
data_yield = {j: [] for j in jalurs_yield}

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
        du = grp[j]['Mahasiswa Daftar Ulang'] if j in grp else 0
        lulus = grp[j]['Calon Lulus Seleksi'] if j in grp else 0
        gugur = grp[j]['Mundur / Gugur'] if j in grp else 0
        data_du[j].append(du)
        data_gugur[j].append(gugur)
        yr_du += du
        yr_gugur += gugur
    tot_du_yr.append(yr_du)
    tot_gugur_yr.append(yr_gugur)
    
    for j in jalurs_yield:
        if j in grp:
            du = grp[j]['Mahasiswa Daftar Ulang']
            lulus = grp[j]['Calon Lulus Seleksi']
            y_rate = (du / lulus * 100.0) if lulus > 0 else np.nan
        else:
            y_rate = np.nan
        data_yield[j].append(y_rate)

def annotate_stacked_bars(ax, data_dict, tot_list, is_intake=True):
    x = np.arange(len(years))
    w = 0.50
    bottoms = np.zeros(len(years))
    
    for j in jalurs:
        vals = np.array(data_dict[j])
        ax.bar(x, vals, bottom=bottoms, label=j, color=jalur_colors[j], width=w, edgecolor='#FFFFFF', linewidth=1.0, zorder=2)
        
        for idx, (v, b) in enumerate(zip(vals, bottoms)):
            if v == 0:
                continue
            tot = tot_list[idx]
            pct = v / tot * 100.0
            mid_y = b + v / 2.0
            
            if is_intake:
                # Panel A: Intake Mix (0 - 10,000)
                if v >= 500:
                    ax.text(idx, mid_y, f'{v:,}\n({pct:.0f}%)', ha='center', va='center',
                            fontsize=8.5, fontweight='bold', color='#FFFFFF', zorder=4)
                elif v >= 160:
                    ax.text(idx, mid_y, f'{v:,} ({pct:.0f}%)', ha='center', va='center',
                            fontsize=7.2, fontweight='bold', color='#FFFFFF', zorder=4)
                elif v >= 90:
                    # 2024 SMC = 104 (1%) callout
                    ax.annotate(f'{j}: {v:,} ({pct:.0f}%)',
                                xy=(idx - w/2, mid_y),
                                xytext=(idx - 0.32, mid_y + 80),
                                ha='right', va='center',
                                arrowprops=dict(arrowstyle='->', color=jalur_colors[j], lw=1.2),
                                fontsize=7.5, fontweight='bold', color=jalur_colors[j],
                                bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=jalur_colors[j], linewidth=1.0, alpha=0.96),
                                zorder=5)
            else:
                # Panel B/C: Gugur / Kebocoran (0 - 2,000)
                if v >= 200:
                    ax.text(idx, mid_y, f'{v:,}\n({pct:.0f}%)', ha='center', va='center',
                            fontsize=8.5, fontweight='bold', color='#FFFFFF', zorder=4)
                elif v >= 70:
                    if v >= 140:
                        ax.text(idx, mid_y, f'{v:,}\n({pct:.0f}%)', ha='center', va='center',
                                fontsize=8.0, fontweight='bold', color='#FFFFFF', zorder=4)
                    else:
                        ax.text(idx, mid_y, f'{v:,} ({pct:.0f}%)', ha='center', va='center',
                                fontsize=7.2, fontweight='bold', color='#FFFFFF', zorder=4)
                elif v >= 20: # 2024 TALENTA=23, SMC=32
                    if idx == 2 and j in ['TALENTA', 'SMC']:
                        y_callout = 1682 if j == 'SMC' else 1610
                        ax.annotate(f'{j}: {v} ({pct:.0f}%)',
                                    xy=(idx - w/2, mid_y),
                                    xytext=(idx - 0.35, y_callout),
                                    ha='right', va='center',
                                    arrowprops=dict(arrowstyle='->', color=jalur_colors[j], lw=1.2),
                                    fontsize=7.8, fontweight='bold', color=jalur_colors[j],
                                    bbox=dict(boxstyle='round,pad=0.22', facecolor='#FFFFFF', edgecolor=jalur_colors[j], linewidth=1.0, alpha=0.96),
                                    zorder=5)
                    else:
                        ax.text(idx, mid_y, f'{v} ({pct:.0f}%)', ha='center', va='center',
                                fontsize=6.8, fontweight='bold', color='#FFFFFF', zorder=4)
        bottoms += vals
        
    for idx, tot in enumerate(tot_list):
        lbl = 'Total:' if is_intake else 'Gugur:'
        bg_col = '#EFF6FF' if is_intake else '#FEF2F2'
        edge_col = '#3B82F6' if is_intake else '#EF4444'
        txt_col = '#0F172A' if is_intake else '#991B1B'
        
        ax.annotate(f'{lbl}\n{tot:,}', xy=(idx, tot), xytext=(0, 10), textcoords='offset points',
                    ha='center', va='bottom', fontsize=9.2, fontweight='bold', color=txt_col,
                    bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_col, edgecolor=edge_col, linewidth=0.9), zorder=4)
    
    ax.set_xticks(x)
    ax.set_xticklabels([str(y) for y in years], fontsize=10.5, fontweight='bold', color='#1E293B')
    ax.set_ylim(0, max(tot_list) * 1.25)
    ax.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(loc='upper left', frameon=True, fontsize=8.2, framealpha=0.92)

# =========================================================================
# 1. GENERATE DUAL PANEL CHART (Intake vs Kebocoran)
# =========================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 6.2), dpi=300)

annotate_stacked_bars(ax1, data_du, tot_du_yr, is_intake=True)
ax1.set_ylabel('Jumlah Mahasiswa Daftar Ulang (Orang)', fontsize=10.5, fontweight='bold', color='#0F172A', labelpad=8)
ax1.set_title('A. Dinamika Serapan Mahasiswa Baru per Jalur (2022–2026)\nIntake Tumbuh +34.9% (6,197 → 8,361 Mahasiswa)', 
              fontsize=11.5, fontweight='bold', pad=10, color='#1E40AF')

annotate_stacked_bars(ax2, data_gugur, tot_gugur_yr, is_intake=False)
ax2.set_ylabel('Jumlah Calon Mahasiswa Mengundurkan Diri (Orang)', fontsize=10.5, fontweight='bold', color='#0F172A', labelpad=8)
ax2.set_title('B. Dinamika Kebocoran Pendaftaran per Jalur (2022–2026)\nKebocoran Terkendali: 1,231 (2022) → 1,617 (2026)', 
              fontsize=11.5, fontweight='bold', pad=10, color='#991B1B')

plt.tight_layout()
out_dual = '14_dual_panel_jalur_masuk_dan_kebocoran.png'
plt.savefig(os.path.join(chart_dir, out_dual), dpi=300)
plt.close()
print(f"Generated {out_dual}")

# =========================================================================
# 2. GENERATE 3-PANEL EXECUTIVE MASTER DASHBOARD
# =========================================================================
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 8.5), dpi=300)

# Panel 1: Intake Mix
annotate_stacked_bars(ax1, data_du, tot_du_yr, is_intake=True)
ax1.set_ylabel('Jumlah Mahasiswa Baru Daftar Ulang (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Dinamika Serapan Mahasiswa Baru per Jalur (2022–2026)\nIntake Tumbuh +34.9% (6,197 → 8,361 Mahasiswa)', 
              fontsize=12, fontweight='bold', pad=12, color='#1E40AF')

# Panel 2: Redesigned Executive Yield Rate
ax2.axhspan(80, 102, facecolor='#F0FDF4', alpha=0.5, zorder=0)
ax2.axhspan(52, 80, facecolor='#FFFBEB', alpha=0.35, zorder=0)

ax2.axhline(80.0, color='#059669', linestyle='--', linewidth=1.5, alpha=0.85, zorder=2)
ax2.text(2022.05, 80.8, 'Target Registrasi Sehat (≥ 80.0%)', fontsize=9, fontweight='bold', color='#047857', zorder=3)

for j in jalurs_yield:
    y_vals = data_yield[j]
    valid_pts = [(years[i], y_vals[i]) for i in range(len(years)) if not np.isnan(y_vals[i])]
    if valid_pts:
        vx, vy = zip(*valid_pts)
        lw = 2.8 if j in ['SNBP', 'SNBT', 'TALENTA'] else 2.2
        ms = 7.5 if j in ['SNBP', 'SNBT', 'TALENTA'] else 6.5
        ax2.plot(vx, vy, label=f"{j}", color=jalur_colors[j], marker=markers[j],
                 linewidth=lw, markersize=ms, zorder=4)

# Smart Anti-Collision Labels
for i, yr in enumerate(years):
    yr_pts = []
    for j in jalurs_yield:
        val = data_yield[j][i]
        if not np.isnan(val):
            yr_pts.append((j, val))
    yr_pts.sort(key=lambda item: item[1], reverse=True)
    
    min_gap = 3.6
    placed_y = []
    for j, val in yr_pts:
        target_y = val
        if placed_y:
            prev_y = placed_y[-1]
            if prev_y - target_y < min_gap:
                target_y = prev_y - min_gap
        placed_y.append(target_y)
    
    for (j, actual_val), lab_y in zip(yr_pts, placed_y):
        ax2.annotate(f"{actual_val:.1f}%",
                     xy=(yr, actual_val),
                     xytext=(yr, lab_y + (1.0 if lab_y >= actual_val else -1.0)),
                     ha='center', va='center',
                     fontsize=8.3, fontweight='bold', color=jalur_colors[j],
                     bbox=dict(boxstyle='round,pad=0.18', facecolor='#FFFFFF', edgecolor=jalur_colors[j], linewidth=0.8, alpha=0.95),
                     zorder=6)

# Callout Card for TALENTA 2026
ax2.annotate('INSIGHT REALISASI TALENTA 2026:\n* 308 dari 461 Lulus Seleksi Daftar Ulang\n* Yield Rate: 66.8% (153 Mengundurkan Diri)\n* Butuh buffer kuota cadangan mitigasi',
             xy=(2026, 66.8), xytext=(2024.1, 55.5),
             arrowprops=dict(facecolor='#7C3AED', edgecolor='#7C3AED', shrink=0.08, width=1.5, headwidth=6),
             fontsize=8.2, fontweight='bold', color='#4C1D95',
             bbox=dict(boxstyle='round,pad=0.32', facecolor='#F5F3FF', edgecolor='#8B5CF6', linewidth=1.2, alpha=0.98),
             zorder=7)

ax2.set_xticks(years)
ax2.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_ylim(50, 102)
ax2.set_ylabel('Tingkat Konversi Registrasi (Yield Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Tren Efisiensi Konversi Pendaftaran (Yield Rate 2022–2026)\nStabilitas Jalur Nasional (≥84%) vs Variabilitas Jalur Mandiri & Talenta (66.8%)', 
              fontsize=12, fontweight='bold', pad=12, color='#065F46')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=1)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.legend(loc='lower left', frameon=True, fontsize=8.8, framealpha=0.95, edgecolor='#CBD5E1')

# Clean Footnote below axis
ax2.text(0.01, -0.09, '*Catatan: Jalur ADIK (<30 mhs/tahun, afirmasi 3T) tidak ditampilkan agar skala perbandingan institusional proporsional.',
         transform=ax2.transAxes, fontsize=7.6, fontstyle='italic', color='#64748B')

# Panel 3: Gugur
annotate_stacked_bars(ax3, data_gugur, tot_gugur_yr, is_intake=False)
ax3.set_ylabel('Jumlah Calon Mahasiswa Mengundurkan Diri (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax3.set_title('C. Dinamika Kebocoran Pendaftaran per Jalur (2022–2026)\nKebocoran Terkendali: 1,231 (2022) → 1,617 (2026)', 
              fontsize=12, fontweight='bold', pad=12, color='#991B1B')

plt.suptitle('PANORAMA DINAMIKA JALUR MASUK & ESKALASI KEBOCORAN PMB USK (2022–2026)\nAnalisis 5 Tahun: Pergeseran Kontribusi Intake Riil, Tren Yield Rate, dan Calon Mahasiswa yang Mundur',
             fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
out_5y = "14_tren_jalur_masuk_dan_kebocoran_5_tahun_2022_2026.png"
plt.savefig(os.path.join(chart_dir, out_5y), dpi=300)
plt.close()
print(f"Generated {out_5y}")
