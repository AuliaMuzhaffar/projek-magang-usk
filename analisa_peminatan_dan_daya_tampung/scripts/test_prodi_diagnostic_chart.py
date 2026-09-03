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
df_s1 = pd.read_excel(excel_path, sheet_name='S1_Kampus_Utama')

df_s1['Sisa_2026'] = df_s1['Daya Tampung 2026'] - df_s1['Daftar Ulang 2026']
df_s1['FR_2026'] = (df_s1['Daftar Ulang 2026'] / df_s1['Daya Tampung 2026'] * 100.0).round(1)
df_s1['Rata_FR_5Thn'] = (df_s1['Rata DU 5-Thn'] / df_s1['Rata DT 5-Thn'] * 100.0).round(1)

def clean_prodi(row):
    p = row['Nama Program Studi']
    f = row['Fakultas']
    fak_abbr = {
        'Kedokteran Gigi': 'FKG', 'Kedokteran': 'FK', 'Hukum': 'FH',
        'Kedokteran Hewan': 'FKH', 'Ekonomi dan Bisnis': 'FEB', 'FISIP': 'FISIP',
        'Keperawatan': 'FKep', 'Teknik': 'FT', 'FKIP': 'FKIP', 'MIPA': 'FMIPA',
        'Pertanian': 'FP', 'Kelautan dan Perikanan': 'FPK'
    }
    short_f = fak_abbr.get(f, f)
    p_title = p.title()
    p_title = p_title.replace('Pgsd', 'PGSD').replace('Pendidikan', 'Pend.').replace('Teknologi', 'Teknol.')
    return f"{p_title} ({short_f})"

df_s1['Label_Prodi'] = df_s1.apply(clean_prodi, axis=1)

# Top 15 Kursi Kosong
top15_sisa = df_s1.sort_values('Sisa_2026', ascending=True).tail(15).reset_index(drop=True)

# 12 Terendah vs 12 Tertinggi
bottom12_fr = df_s1.sort_values('FR_2026', ascending=False).tail(12).reset_index(drop=True)
top12_fr = df_s1.sort_values('FR_2026', ascending=True).tail(12).reset_index(drop=True)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(27, 11.5), dpi=300, gridspec_kw={'width_ratios': [1.22, 1.18]})

# -------------------------------------------------------------
# Panel 1: Top 15 Kursi Kosong Terbanyak
# -------------------------------------------------------------
y_pos1 = np.arange(len(top15_sisa))
colors_sisa = ['#991B1B' if fr < 65.0 else '#D97706' if fr < 80.0 else '#2563EB' for fr in top15_sisa['FR_2026']]

bars1 = ax1.barh(y_pos1, top15_sisa['Sisa_2026'], color=colors_sisa, height=0.64, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

ax1.set_yticks(y_pos1)
ax1.set_yticklabels(top15_sisa['Label_Prodi'], fontsize=10.5, fontweight='bold', color='#1E293B')
max_s1 = top15_sisa['Sisa_2026'].max()
ax1.set_xlim(0, max_s1 * 1.65)
ax1.set_ylim(-0.8, len(top15_sisa) - 0.2)
ax1.set_xlabel('Jumlah Kursi Kosong Absolut (Bangku Tidak Terisi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Episentrum Kursi Kosong Terbesar per Program Studi (Tahun 2026)\n15 Prodi Ini Menyumbang 759 Kursi Kosong (48.4% dari Total Defisit 1,569 Kampus)', 
              fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for i, r in top15_sisa.iterrows():
    s_val = int(r['Sisa_2026'])
    du = int(r['Daftar Ulang 2026'])
    dt = int(r['Daya Tampung 2026'])
    fr = r['FR_2026']
    r5 = r['Rata_FR_5Thn']
    
    badge_txt = f"{s_val} kursi kosong  |  Terisi: {du}/{dt} ({fr:.1f}%)  |  Rata 5-Thn: {r5:.1f}%"
    txt_c = '#991B1B' if fr < 65.0 else '#92400E' if fr < 80.0 else '#1E40AF'
    border_c = '#EF4444' if fr < 65.0 else '#F59E0B' if fr < 80.0 else '#3B82F6'
    bg_c = '#FEF2F2' if fr < 65.0 else '#FFFBEB' if fr < 80.0 else '#EFF6FF'
    
    ax1.annotate(badge_txt, xy=(s_val, i), xytext=(7, 0), textcoords='offset points',
                 va='center', ha='left', fontsize=8.6, fontweight='bold', color=txt_c,
                 bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.92),
                 zorder=4)

legend_elements1 = [
    Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Keterisian Kritis (<65%) - Defisit Berat'),
    Patch(facecolor='#D97706', edgecolor='#0F172A', label='Keterisian Rentan (65%–79%) - Defisit Sedang'),
    Patch(facecolor='#2563EB', edgecolor='#0F172A', label='Keterisian Sehat (≥80%) tapi Kuota Terlampau Besar (Over-Ekspansi)')
]
ax1.legend(handles=legend_elements1, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

# -------------------------------------------------------------
# Panel 2: Polaritas Keterisian Kuota (12 Tertinggi vs 12 Terendah)
# -------------------------------------------------------------
combined_fr = pd.concat([bottom12_fr, top12_fr]).reset_index(drop=True)
y_pos2 = np.arange(len(combined_fr))

colors_fr2 = ['#DC2626' if i < 12 else '#059669' for i in range(len(combined_fr))]
bars2 = ax2.barh(y_pos2, combined_fr['FR_2026'], color=colors_fr2, height=0.64, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

ax2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Batas Keterisian Sehat (80%)', zorder=3)
ax2.axvspan(0, 80.0, color='#FEF2F2', alpha=0.35, zorder=0)

ax2.axhline(11.5, color='#475569', linestyle='-', linewidth=1.2, alpha=0.75, zorder=3)
ax2.annotate('JURANG POLARISASI PORTOFOLIO: Selisih Keterisian Ekstrem 30% s.d. 48%',
             xy=(2, 11.5), xytext=(4, 11.5), textcoords='data', va='center', ha='left',
             fontsize=8.5, fontweight='bold', color='#1E293B',
             bbox=dict(boxstyle='square,pad=0.25', facecolor='#F1F5F9', edgecolor='#64748B', linewidth=0.8),
             zorder=5)

ax2.set_yticks(y_pos2)
ax2.set_yticklabels(combined_fr['Label_Prodi'], fontsize=9.8, fontweight='bold', color='#1E293B')
ax2.set_xlim(0, 148)
ax2.set_ylim(-0.8, len(combined_fr) - 0.2)
ax2.set_xlabel('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Polaritas Ekstrem Keterisian Kuota: 12 Bintang Penuh vs 12 Krisis Akut (2026)\nMembedah Polarisasi Daya Tarik Nyata Program Studi di Pasar Pendidikan', 
              fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for i, r in combined_fr.iterrows():
    fr = r['FR_2026']
    r5 = r['Rata_FR_5Thn']
    du = int(r['Daftar Ulang 2026'])
    dt = int(r['Daya Tampung 2026'])
    
    badge_txt2 = f"{fr:.1f}% ({du}/{dt})  |  Rata 5-Thn: {r5:.1f}%"
    txt_c2 = '#991B1B' if fr < 80.0 else '#065F46'
    border_c2 = '#EF4444' if fr < 80.0 else '#10B981'
    bg_c2 = '#FEF2F2' if fr < 80.0 else '#F0FDF4'
    
    ax2.annotate(badge_txt2, xy=(fr, i), xytext=(7, 0), textcoords='offset points',
                 va='center', ha='left', fontsize=8.4, fontweight='bold', color=txt_c2,
                 bbox=dict(boxstyle='round,pad=0.20', facecolor=bg_c2, edgecolor=border_c2, linewidth=0.8, alpha=0.92),
                 zorder=4)

legend_elements2 = [
    Patch(facecolor='#059669', edgecolor='#0F172A', label='Top 12 Prodi Prima (Penuh 95% s.d. 100%)'),
    Patch(facecolor='#DC2626', edgecolor='#0F172A', label='Bottom 12 Prodi Krisis Akut (Keterisian 52% s.d. 67%)'),
]
ax2.legend(handles=legend_elements2, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

plt.suptitle('DIAGNOSTIK MENDALAM DAYA SERAP & DEFISIT KUOTA TINGKAT PROGRAM STUDI S1 USK (2026)\nMenyentuh Akar Masalah: 15 Prodi Episentrum Kursi Kosong & Jurang Pemisah Bintang vs Krisis Akut',
             fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

plt.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
out_file = os.path.join(chart_dir, "16_analisa_keterisian_dan_kursi_kosong_program_studi.png")
plt.savefig(out_file, dpi=300)
plt.close()
print("Perfect Chart 16 generated successfully at:", out_file)
