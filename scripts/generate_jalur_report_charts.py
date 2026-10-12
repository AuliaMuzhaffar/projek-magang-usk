import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

script_dir = os.path.dirname(os.path.abspath(__file__))
excel_path = os.path.abspath(os.path.join(script_dir, '..', 'data', 'analisa_jalur_masuk_dan_kebocoran_per_prodi_2022_2026.xlsx'))
chart_dir = os.path.abspath(os.path.join(script_dir, '..', 'grafik'))
os.makedirs(chart_dir, exist_ok=True)

df_pivot = pd.read_excel(excel_path, sheet_name='Pivot_5Thn_Per_Prodi', header=3)
df_detail = pd.read_excel(excel_path, sheet_name='Detail_5Thn_Prodi_Jalur', header=3)

def clean_label(p, f):
    fak_abbr = {
        'Ekonomi dan Bisnis': 'FEB',
        'Ilmu Sosial dan Ilmu Politik': 'FISIP',
        'Kelautan dan Perikanan': 'FPK',
        'Kedokteran': 'FK',
        'Kedokteran Gigi': 'FKG',
        'Kedokteran Hewan': 'FKH',
        'Keperawatan': 'FKEP',
        'Pertanian': 'FP',
        'Teknik': 'FT',
        'MIPA': 'FMIPA',
        'Hukum': 'FH',
        'FKIP': 'FKIP',
        'PSDKU Gayo Lues': 'PSDKU'
    }
    f_short = fak_abbr.get(str(f).strip(), str(f).strip())
    p_clean = str(p).strip().title().replace('Psdku', 'PSDKU').replace('Pdd', 'PDD').replace('Psp', 'PSP')
    if len(p_clean) > 26:
        p_clean = p_clean[:24] + '...'
    return f"{p_clean} ({f_short})"

# =============================================================
# CHART 18: KETERGANTUNGAN PINTU MASUK (MANDIRI VS NASIONAL)
# =============================================================
print("Generating 18_analisis_pintu_masuk_dan_ketergantungan_jalur_prodi.png...")
fig18, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 8.5), dpi=300)

df_s1 = df_pivot[df_pivot['Jenjang'] == 'S1'].copy()
df_s1['Pct_Mandiri'] = (df_s1['DU Mandiri'] / df_s1['Total DU (5-Thn)'].replace(0, 1) * 100).round(1)
df_s1['Pct_Nasional'] = ((df_s1['DU SNBP'] + df_s1['DU SNBT']) / df_s1['Total DU (5-Thn)'].replace(0, 1) * 100).round(1)

# Panel 1: Top 8 Bergantung Mandiri
top_mandiri = df_s1.sort_values(by='Pct_Mandiri', ascending=False).head(8).reset_index(drop=True)
y_pos1 = np.arange(len(top_mandiri))

bars1 = ax1.barh(y_pos1, top_mandiri['Pct_Mandiri'], color='#EA580C', alpha=0.9, height=0.6, edgecolor='#C2410C', linewidth=1.2, zorder=2)
ax1.set_yticks(y_pos1)
labels1 = [clean_label(r['Nama Program Studi'], r['Fakultas']) for _, r in top_mandiri.iterrows()]
ax1.set_yticklabels(labels1, fontsize=10.5, fontweight='bold', color='#1E293B')
ax1.invert_yaxis()
ax1.set_xlabel('Pangsa Mahasiswa Masuk Jalur Mandiri SMMPTN (%)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Top Program Studi S1 Paling Bergantung pada Jalur Mandiri (SMMPTN)\n(Basis Akumulasi Mahasiswa Masuk 2022–2026)', fontsize=12.5, fontweight='bold', pad=15, color='#C2410C')
ax1.set_xlim(0, 105)
ax1.grid(True, linestyle='--', alpha=0.45, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for i, r in top_mandiri.iterrows():
    val = r['Pct_Mandiri']
    du_m = int(r['DU Mandiri'])
    tot = int(r['Total DU (5-Thn)'])
    ax1.text(val + 1.5, i, f"{val:.1f}% ({du_m:,} dari {tot:,} mhs)", va='center', ha='left', fontsize=9.2, fontweight='bold', color='#9A3412', zorder=3)

# Panel 2: Top 8 Bergantung Nasional (SNBP+SNBT)
top_nasional = df_s1.sort_values(by='Pct_Nasional', ascending=False).head(8).reset_index(drop=True)
y_pos2 = np.arange(len(top_nasional))

bars2 = ax2.barh(y_pos2, top_nasional['Pct_Nasional'], color='#1D4ED8', alpha=0.9, height=0.6, edgecolor='#1E40AF', linewidth=1.2, zorder=2)
ax2.set_yticks(y_pos2)
labels2 = [clean_label(r['Nama Program Studi'], r['Fakultas']) for _, r in top_nasional.iterrows()]
ax2.set_yticklabels(labels2, fontsize=10.5, fontweight='bold', color='#1E293B')
ax2.invert_yaxis()
ax2.set_xlabel('Pangsa Mahasiswa Masuk Jalur Nasional SNBP + SNBT (%)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Top Program Studi S1 Paling Bergantung pada Jalur Nasional (SNBP+SNBT)\n(Basis Akumulasi Mahasiswa Masuk 2022–2026)', fontsize=12.5, fontweight='bold', pad=15, color='#1D4ED8')
ax2.set_xlim(0, 115)
ax2.grid(True, linestyle='--', alpha=0.45, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for i, r in top_nasional.iterrows():
    val = r['Pct_Nasional']
    du_n = int(r['DU SNBP'] + r['DU SNBT'])
    tot = int(r['Total DU (5-Thn)'])
    ax2.text(val + 1.5, i, f"{val:.1f}% ({du_n:,} dari {tot:,} mhs)", va='center', ha='left', fontsize=9.2, fontweight='bold', color='#1E3A8A', zorder=3)

fig18.suptitle("PROFIL KETERGANTUNGAN PINTU MASUK MAHASISWA BARU PER PROGRAM STUDI USK (2022–2026)\nKomparasi Program Studi Rintisan Mandiri vs Penopang Kuota Seleksi Nasional",
               fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)
fig18.tight_layout(rect=[0.01, 0.04, 0.99, 0.93])
fig18.savefig(os.path.join(chart_dir, "18_analisis_pintu_masuk_dan_ketergantungan_jalur_prodi.png"), dpi=300)
plt.close(fig18)

# =============================================================
# CHART 19: EPISENTRUM KEBOCORAN (TALENTA VS SMMPTN)
# =============================================================
print("Generating 19_episentrum_kebocoran_calon_mahasiswa_per_jalur.png...")
fig19, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 8.5), dpi=300)

# Top 8 Gugur TALENTA
talenta_data = df_detail[df_detail['Jalur Penerimaan'] == 'TALENTA'].copy()
top_talenta = talenta_data.sort_values(by='Calon Gugur (Mundur)', ascending=False).head(8).reset_index(drop=True)
y_pos1 = np.arange(len(top_talenta))

bars1 = ax1.barh(y_pos1, top_talenta['Calon Gugur (Mundur)'], color='#DC2626', alpha=0.9, height=0.6, edgecolor='#B91C1C', linewidth=1.2, zorder=2)
ax1.set_yticks(y_pos1)
labels1 = [clean_label(r['Nama Program Studi'], r['Fakultas']) for _, r in top_talenta.iterrows()]
ax1.set_yticklabels(labels1, fontsize=10.5, fontweight='bold', color='#1E293B')
ax1.invert_yaxis()
ax1.set_xlabel('Jumlah Calon Mahasiswa Lulus yang Mundur/Gugur (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax1.set_title('A. Top 8 Episentrum Kebocoran Terbesar di Jalur TALENTA (2022–2026)\n(Efek "Tiket Cadangan Gratis" Sebelum Pengumuman SNBT/Kedinasan)', fontsize=12.5, fontweight='bold', pad=15, color='#B91C1C')
ax1.set_xlim(0, 265)
ax1.grid(True, linestyle='--', alpha=0.45, color='#CBD5E1', zorder=0)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

for i, r in top_talenta.iterrows():
    gugur = int(r['Calon Gugur (Mundur)'])
    lulus = int(r['Calon Lulus Seleksi'])
    pct = r['Tingkat Kebocoran (%)'] * 100 if r['Tingkat Kebocoran (%)'] <= 1.0 else r['Tingkat Kebocoran (%)']
    ax1.text(gugur + 4, i, f"{gugur} orang ({pct:.1f}% kabur / {lulus} lulus)", va='center', ha='left', fontsize=9.2, fontweight='bold', color='#991B1B', zorder=3)

# Top 8 Gugur SMMPTN Mandiri
smmptn_data = df_detail[df_detail['Jalur Penerimaan'] == 'SMMPTN'].copy()
top_smmptn = smmptn_data.sort_values(by='Calon Gugur (Mundur)', ascending=False).head(8).reset_index(drop=True)
y_pos2 = np.arange(len(top_smmptn))

bars2 = ax2.barh(y_pos2, top_smmptn['Calon Gugur (Mundur)'], color='#7C3AED', alpha=0.9, height=0.6, edgecolor='#6D28D9', linewidth=1.2, zorder=2)
ax2.set_yticks(y_pos2)
labels2 = [clean_label(r['Nama Program Studi'], r['Fakultas']) for _, r in top_smmptn.iterrows()]
ax2.set_yticklabels(labels2, fontsize=10.5, fontweight='bold', color='#1E293B')
ax2.invert_yaxis()
ax2.set_xlabel('Jumlah Calon Mahasiswa Lulus yang Mundur/Gugur (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
ax2.set_title('B. Top 8 Episentrum Kebocoran Terbesar di Jalur Mandiri SMMPTN (2022–2026)\n(Efek Syok Finansial Uang Pangkal IPI & Pilihan Poltekkes/PTN Lain)', fontsize=12.5, fontweight='bold', pad=15, color='#6D28D9')
ax2.set_xlim(0, 265)
ax2.grid(True, linestyle='--', alpha=0.45, color='#CBD5E1', zorder=0)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

for i, r in top_smmptn.iterrows():
    gugur = int(r['Calon Gugur (Mundur)'])
    lulus = int(r['Calon Lulus Seleksi'])
    pct = r['Tingkat Kebocoran (%)'] * 100 if r['Tingkat Kebocoran (%)'] <= 1.0 else r['Tingkat Kebocoran (%)']
    ax2.text(gugur + 4, i, f"{gugur} orang ({pct:.1f}% kabur / {lulus} lulus)", va='center', ha='left', fontsize=9.2, fontweight='bold', color='#5B21B6', zorder=3)

fig19.suptitle("EPISENTRUM KEBOCORAN PENERIMAAN MAHASISWA BARU DI TINGKAT PROGRAM STUDI (2022–2026)\nPembedahan Kasus Calon Mahasiswa Lulus Seleksi yang Tidak Mendaftar Ulang",
               fontsize=14.5, fontweight='bold', color='#0F172A', y=0.98)
fig19.tight_layout(rect=[0.01, 0.04, 0.99, 0.93])
fig19.savefig(os.path.join(chart_dir, "19_episentrum_kebocoran_calon_mahasiswa_per_jalur.png"), dpi=300)
plt.close(fig19)

print("Charts 18 and 19 successfully generated!")
