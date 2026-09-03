import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

excel_path = 'tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'
chart_dir = 'tugas-5/analisa_peminatan_dan_daya_tampung/grafik'
df_s1 = pd.read_excel(excel_path, sheet_name='S1_Kampus_Utama')

# Aggregate data
fak_grp = df_s1.groupby('Fakultas').agg({
    'Daya Tampung 2022': 'sum', 'Daftar Ulang 2022': 'sum',
    'Daya Tampung 2023': 'sum', 'Daftar Ulang 2023': 'sum',
    'Daya Tampung 2024': 'sum', 'Daftar Ulang 2024': 'sum',
    'Daya Tampung 2025': 'sum', 'Daftar Ulang 2025': 'sum',
    'Daya Tampung 2026': 'sum', 'Daftar Ulang 2026': 'sum',
    'Peminat 2026': 'sum',
    'Rata Peminat 5-Thn': 'sum', 'Rata DT 5-Thn': 'sum', 'Rata DU 5-Thn': 'sum'
}).reset_index()

for yr in [2022, 2023, 2024, 2025, 2026]:
    fak_grp[f'FR_{yr}'] = (fak_grp[f'Daftar Ulang {yr}'] / fak_grp[f'Daya Tampung {yr}'] * 100.0).round(1)

fak_grp['Rata_FR_5Thn'] = (fak_grp['Rata DU 5-Thn'] / fak_grp['Rata DT 5-Thn'] * 100.0).round(1)
fak_grp['Rata_Ket_5Thn'] = (fak_grp['Rata Peminat 5-Thn'] / fak_grp['Rata DT 5-Thn']).round(2)
fak_grp['Sisa_2026'] = fak_grp['Daya Tampung 2026'] - fak_grp['Daftar Ulang 2026']

# -------------------------------------------------------------
# 1. POLISHED CHART 07: EXECUTIVE DUAL PANEL
# -------------------------------------------------------------
fak_sorted = fak_grp.sort_values('FR_2026', ascending=True).reset_index(drop=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(23, 9.2), dpi=300, gridspec_kw={'width_ratios': [1.38, 1.0]})

y_pos = np.arange(len(fak_sorted))
h = 0.38

# Panel 1: Perbandingan Keterisian Kuota (2022 vs 2026) & Delta
bars22 = ax1.barh(y_pos - h/2.0, fak_sorted['FR_2022'], height=h, label='Tingkat Keterisian 2022 (%)', 
                  color='#94A3B8', alpha=0.85, edgecolor='#64748B', linewidth=1.0, zorder=2)

colors_26 = ['#DC2626' if fr < 80.0 else '#2563EB' for fr in fak_sorted['FR_2026']]
bars26 = ax1.barh(y_pos + h/2.0, fak_sorted['FR_2026'], height=h, label='Tingkat Keterisian 2026 (%)', 
                  color=colors_26, alpha=0.92, edgecolor='#1E3A8A', linewidth=1.1, zorder=2)

ax1.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Batas Minimal Keterisian Sehat (80%)', zorder=3)
ax1.axvspan(0, 80.0, color='#FEF2F2', alpha=0.35, zorder=0)

ax1.set_yticks(y_pos)
ax1.set_yticklabels(fak_sorted['Fakultas'], fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_xlim(0, 135)  # Extended limit to comfortably fit long pill badges
ax1.set_xlabel('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Perbandingan Keterisian Kuota per Fakultas (2022 vs 2026)\nEvaluasi Efisiensi Serapan Kuota Pasca Penetapan PTN-BH', 
              fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(loc='lower left', bbox_to_anchor=(0.02, 0.02), frameon=True, fontsize=9.5, framealpha=0.95)

# Annotate bars with a single, elegant unified pill badge
for i, r in fak_sorted.iterrows():
    f22 = r['FR_2022']
    f26 = r['FR_2026']
    delta = f26 - f22
    delta_str = f"+{delta:.1f}%" if delta > 0 else f"{delta:.1f}%"
    
    du26 = int(r['Daftar Ulang 2026'])
    dt26 = int(r['Daya Tampung 2026'])
    
    badge_txt = f"{f26:.1f}% ({du26:,}/{dt26:,})  |  Δ: {delta_str}"
    border_c = '#EF4444' if f26 < 80.0 else '#93C5FD'
    bg_c = '#FEF2F2' if f26 < 80.0 else '#FFFFFF'
    txt_c = '#991B1B' if f26 < 80.0 else '#0F172A'
    
    ax1.annotate(badge_txt, xy=(f26, i + h/2.0), xytext=(7, 0), textcoords='offset points',
                 va='center', ha='left', fontsize=8.8, fontweight='bold', color=txt_c,
                 bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.95),
                 zorder=4)

# Panel 2: Beban Kursi Kosong Absolut per Fakultas Tahun 2026
fak_sisa_sorted = fak_grp.sort_values('Sisa_2026', ascending=True).reset_index(drop=True)
y_pos2 = np.arange(len(fak_sisa_sorted))

sisa_cols = ['#991B1B' if s >= 200 else '#EA580C' if s >= 70 else '#059669' for s in fak_sisa_sorted['Sisa_2026']]
bars_sisa = ax2.barh(y_pos2, fak_sisa_sorted['Sisa_2026'], color=sisa_cols, height=0.62, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

ax2.set_yticks(y_pos2)
ax2.set_yticklabels(fak_sisa_sorted['Fakultas'], fontsize=11, fontweight='bold', color='#1E293B')
max_sisa = fak_sisa_sorted['Sisa_2026'].max()
ax2.set_xlim(0, max_sisa * 1.30)
ax2.set_xlabel('Jumlah Kursi Kosong Absolut (Bangku Tidak Terisi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Kontribusi Beban Kursi Kosong per Fakultas (Tahun 2026)\nTotal 1,569 Bangku Kosong di 12 Fakultas S1 Kampus Utama', 
              fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

tot_sisa = fak_sisa_sorted['Sisa_2026'].sum()
for i, r in fak_sisa_sorted.iterrows():
    s_val = int(r['Sisa_2026'])
    pct_share = (s_val / tot_sisa * 100.0) if tot_sisa > 0 else 0
    txt_col = '#991B1B' if s_val >= 200 else '#92400E' if s_val >= 70 else '#065F46'
    
    if s_val == 0:
        label_txt = "0 kursi (Penuh 100%)"
    else:
        label_txt = f"{s_val:,} kursi ({pct_share:.1f}% total defisit)"
        
    ax2.annotate(label_txt, xy=(s_val, i), xytext=(7, 0), textcoords='offset points',
                 va='center', ha='left', fontsize=9.0, fontweight='bold', color=txt_col,
                 bbox=dict(boxstyle='round,pad=0.22', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.7, alpha=0.92),
                 zorder=4)

plt.suptitle('EVALUASI KOMPREHENSIF DAYA SERAP & DEFISIT KUOTA 12 FAKULTAS S1 USK (2022–2026)\nKomparasi Efisiensi Keterisian Kuota vs Beban Riil Kursi Kosong yang Ditanggung Fakultas',
             fontsize=14, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
plt.savefig(os.path.join(chart_dir, "07_analisa_peminatan_dan_keterisian_fakultas.png"), dpi=300)
plt.close()
print("Clean Chart 07 generated.")


# -------------------------------------------------------------
# 2. POLISHED CHART 15: MASTER 5-YEAR LONGITUDINAL DASHBOARD
# -------------------------------------------------------------
fak_5y_sorted = fak_grp.sort_values('Rata_FR_5Thn', ascending=False).reset_index(drop=True)

fig, (ax_heat, ax_line) = plt.subplots(1, 2, figsize=(26, 9.5), dpi=300, gridspec_kw={'width_ratios': [1.12, 1.28]})

# Panel 1: Heatmap 12 Fakultas x 5 Tahun
matrix_data = fak_5y_sorted[['FR_2022', 'FR_2023', 'FR_2024', 'FR_2025', 'FR_2026', 'Rata_FR_5Thn']].values
col_labels = ['2022', '2023', '2024', '2025', '2026', 'Rata 5-Thn']
row_labels = fak_5y_sorted['Fakultas'].tolist()

cmap = plt.cm.RdYlGn
norm = mcolors.Normalize(vmin=55, vmax=102)

im = ax_heat.imshow(matrix_data, cmap=cmap, norm=norm, aspect='auto')

ax_heat.set_xticks(np.arange(len(col_labels)))
ax_heat.set_yticks(np.arange(len(row_labels)))
ax_heat.set_xticklabels(col_labels, fontsize=11, fontweight='bold', color='#1E293B')
ax_heat.set_yticklabels(row_labels, fontsize=11, fontweight='bold', color='#1E293B')
ax_heat.set_title('A. Heatmap Keterisian Kuota 12 Fakultas (2022–2026)\nIdentifikasi Zona Hijau (Prima), Kuning (Rentan), & Merah Kronis', 
                  fontsize=12.5, fontweight='bold', pad=14, color='#065F46')

for r in range(len(row_labels)):
    for c in range(len(col_labels)):
        val = matrix_data[r, c]
        tc = '#FFFFFF' if (val < 62 or val > 95) else '#0F172A'
        fw = 'bold' if c == 5 else 'normal'
        ax_heat.text(c, r, f"{val:.1f}%", ha='center', va='center', fontsize=9.5, fontweight=fw, color=tc)

cbar = fig.colorbar(im, ax=ax_heat, orientation='horizontal', pad=0.08, shrink=0.75)
cbar.set_label('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=10, fontweight='bold')

# Panel 2: Lintasan Tren 5 Tahun dengan Anti-Collision Label Spacing
years = [2022, 2023, 2024, 2025, 2026]
colors_faculty = {
    'Hukum': '#1E40AF', 'Kedokteran': '#047857', 'Kedokteran Gigi': '#0D9488',
    'Kedokteran Hewan': '#0284C7', 'Ekonomi dan Bisnis': '#4338CA', 'FISIP': '#6D28D9',
    'Keperawatan': '#B45309', 'Teknik': '#D97706', 'FKIP': '#EA580C', 'MIPA': '#E11D48',
    'Pertanian': '#C026D3', 'Kelautan dan Perikanan': '#DC2626'
}

raw_endpoints = []
for _, r in fak_5y_sorted.iterrows():
    fak_name = r['Fakultas']
    y_trajectory = [r[f'FR_{yr}'] for yr in years]
    is_bottom = fak_name in ['Pertanian', 'Kelautan dan Perikanan']
    is_giant = fak_name in ['FKIP', 'Teknik', 'MIPA']
    
    lw = 3.2 if is_bottom or is_giant else 1.8
    alpha_val = 0.95 if is_bottom or is_giant else 0.75
    col = colors_faculty.get(fak_name, '#475569')
    
    ax_line.plot(years, y_trajectory, marker='o', linewidth=lw, alpha=alpha_val, color=col, 
                 label=f"{fak_name} ({r['Rata_FR_5Thn']:.1f}%)", zorder=4)
    raw_endpoints.append({
        'fak': fak_name,
        'val': y_trajectory[-1],
        'col': col
    })

ax_line.axhline(80.0, color='#DC2626', linestyle='--', linewidth=2.0, alpha=0.85, label='Batas Keterisian Sehat (80%)', zorder=2)
ax_line.axvspan(2022, 2026, ymin=0, ymax=(80-50)/(107-50), color='#FEF2F2', alpha=0.45, zorder=0)

ax_line.set_xticks(years)
ax_line.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
ax_line.set_ylim(50, 107)
ax_line.set_xlim(2021.8, 2028.0)  # Generous room for clean callout tags
ax_line.set_ylabel('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax_line.set_title('B. Lintasan Historis Keterisian Kuota 12 Fakultas (2022–2026)\nMenyingkap Krisis 2023–2024 dan Pemulihan Rentan Menuju 2026', 
                  fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
ax_line.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax_line.spines['top'].set_visible(False)
ax_line.spines['right'].set_visible(False)

# ANTI-COLLISION LABEL SPREADER
raw_endpoints.sort(key=lambda x: x['val'])
min_dist = 2.4  # minimum vertical distance in percentage points
adjusted_y = [ep['val'] for ep in raw_endpoints]

for _ in range(15):  # relaxation iterations
    for i in range(1, len(adjusted_y)):
        if adjusted_y[i] - adjusted_y[i-1] < min_dist:
            overlap = min_dist - (adjusted_y[i] - adjusted_y[i-1])
            adjusted_y[i] += overlap / 2.0
            adjusted_y[i-1] -= overlap / 2.0

for ep, y_adj in zip(raw_endpoints, adjusted_y):
    # draw subtle connector line if adjusted
    if abs(y_adj - ep['val']) > 0.4:
        ax_line.plot([2026, 2026.25], [ep['val'], y_adj], color=ep['col'], linestyle=':', linewidth=0.9, alpha=0.8, zorder=4)
        x_text = 2026.3
    else:
        x_text = 2026.15
        
    ax_line.annotate(f"{ep['fak']}: {ep['val']:.1f}%", xy=(2026, ep['val']), xytext=(x_text, y_adj),
                     textcoords='data', va='center', ha='left', fontsize=8.4, fontweight='bold', color=ep['col'],
                     bbox=dict(boxstyle='round,pad=0.18', facecolor='#FFFFFF', edgecolor=ep['col'], linewidth=0.7, alpha=0.92),
                     zorder=5)

# Callout on Pertanian plunge
ax_line.annotate('Anjloknya Pertanian (63.6%):\nTitik krisis pendaftaran 2023-2024',
                 xy=(2024, 63.6), xytext=(2022.6, 53.5),
                 arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', shrink=0.08, width=1.5, headwidth=6),
                 fontsize=8.5, fontweight='bold', color='#991B1B',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=1.1),
                 zorder=6)

plt.suptitle('PANORAMA EVALUASI LONGITUDINAL 5 TAHUN DAYA SERAP KUOTA 12 FAKULTAS USK (2022–2026)\nMenghilangkan Bias Titik Tunggal: Memetakan Konsistensi Fakultas Prima vs Krisis Kapasitas Kronis',
             fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.02, 0.99, 0.93])
plt.savefig(os.path.join(chart_dir, "15_evaluasi_kinerja_fakultas_5_tahun_2022_2026.png"), dpi=300)
plt.close()
print("Polished Chart 15 generated successfully.")
