import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Style configuration
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

script_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = os.path.abspath(os.path.join(script_dir, '..'))
data_dir = os.path.join(base_dir, '..')
chart_dir = os.path.join(base_dir, 'grafik')
os.makedirs(chart_dir, exist_ok=True)

file_kip_master = os.path.join(data_dir, 'DATA_KIP_2025-2026.xlsx')
file_kip_penerima = os.path.join(data_dir, 'PENERIMA_KIP_2025-2026.xlsx')

print("1. Loading Master and Pendaftar Datasets...")
df_kip25_master = pd.read_excel(file_kip_master, sheet_name='KIP 2025')
df_snbt25_pendaftar = pd.read_excel(file_kip_penerima, sheet_name='DAFTAR_KIP_SNBT_2025')

df_kip26_master = pd.read_excel(file_kip_master, sheet_name='KIP 2026')
df_snbt26_pendaftar = pd.read_excel(file_kip_penerima, sheet_name='DAFTAR_KIP_SNBT_2026')

# ---------------------------------------------------------
# Clean & Match 2025
# ---------------------------------------------------------
print("2. Processing & Cross-Checking Data KIP 2025...")
snbt_master_25 = df_kip25_master[df_kip25_master['Pola Seleksi'] == 'SNBT'].copy()
snbt_master_25.loc[:, 'no_ujian_str'] = snbt_master_25['No Ujian'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
snbt_codes_25 = set(snbt_master_25['no_ujian_str'])

df_snbt25_pendaftar = df_snbt25_pendaftar.copy()
df_snbt25_pendaftar.loc[:, 'kode_peserta_str'] = df_snbt25_pendaftar['KODE PESERTA'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
df_snbt25_pendaftar.loc[:, 'is_accepted'] = df_snbt25_pendaftar['kode_peserta_str'].isin(snbt_codes_25)
df_snbt25_pendaftar.loc[:, 'status_kip'] = df_snbt25_pendaftar['is_accepted'].apply(lambda x: 'DITERIMA' if x else 'DITOLAK')

# ---------------------------------------------------------
# Clean & Match 2026
# ---------------------------------------------------------
print("3. Processing & Cross-Checking Data KIP 2026...")
snbt_master_26 = df_kip26_master[df_kip26_master['Pola Seleksi'] == 'SNBT'].copy()
snbt_master_26.loc[:, 'no_ujian_str'] = snbt_master_26['No Ujian'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
snbt_codes_26 = set(snbt_master_26['no_ujian_str'])

df_snbt26_pendaftar = df_snbt26_pendaftar.copy()
df_snbt26_pendaftar.loc[:, 'kode_peserta_str'] = df_snbt26_pendaftar.iloc[:, 0].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
df_snbt26_pendaftar.loc[:, 'is_accepted'] = df_snbt26_pendaftar['kode_peserta_str'].isin(snbt_codes_26)
df_snbt26_pendaftar.loc[:, 'status_kip'] = df_snbt26_pendaftar['is_accepted'].apply(lambda x: 'DITERIMA' if x else 'DITOLAK')
df_snbt26_pendaftar.loc[:, 'prodi_nama'] = df_snbt26_pendaftar.iloc[:, 8].astype(str).str.strip().str.upper()

# Faculty Classifier function
def classify_faculty(prodi_str):
    p = str(prodi_str).upper()
    if 'GAYO LUES' in p or 'PDSKU' in p or 'PSDKU' in p:
        return 'PSDKU Gayo Lues'
    if any(k in p for k in ['PENDIDIKAN', 'PEND.', 'BIMBINGAN', 'PAUD', 'GURU', 'JASMANI', 'SENI DRAMA']):
        if 'DOKTER HEWAN' in p:
            return 'Kedokteran Hewan'
        return 'FKIP'
    if any(k in p for k in ['TEKNIK', 'PERENCANAAN WILAYAH', 'ARSITEKTUR', 'PERTAMBANGAN', 'GEOLOGI', 'GEOFISIKA']):
        return 'Teknik'
    if any(k in p for k in ['AGRIBISNIS', 'AGROTEKNOLOGI', 'PETERNAKAN', 'ILMU TANAH', 'PROTEKSI TANAMAN', 'TEKNOLOGI HASIL PERTANIAN', 'TEKNIK PERTANIAN', 'KEHUTANAN']):
        return 'Pertanian'
    if any(k in p for k in ['MANAJEMEN', 'AKUNTANSI', 'EKONOMI', 'KEUANGAN', 'PERBANKAN', 'BISNIS', 'SEKRETARI']):
        return 'Ekonomi & Bisnis'
    if any(k in p for k in ['FISIKA', 'KIMIA', 'BIOLOGI', 'MATEMATIKA', 'INFORMATIKA', 'STATISTIKA', 'FARMASI']):
        return 'FMIPA'
    if any(k in p for k in ['HUKUM']):
        return 'Hukum'
    if any(k in p for k in ['SOSIOLOGI', 'ILMU POLITIK', 'KOMUNIKASI', 'PEMERINTAHAN']):
        return 'FISIP'
    if any(k in p for k in ['ILMU KELAUTAN', 'BUDIDAYA PERAIRAN', 'PERIKANAN', 'PEMANFAATAN SUMBERDAYA']):
        return 'Kelautan & Perikanan'
    if any(k in p for k in ['KEPERAWATAN']):
        return 'Keperawatan'
    if any(k in p for k in ['DOKTER HEWAN', 'KEDOKTERAN HEWAN', 'KESEHATAN HEWAN']):
        return 'Kedokteran Hewan'
    if any(k in p for k in ['DOKTER GIGI', 'KEDOKTERAN GIGI']):
        return 'Kedokteran Gigi'
    if any(k in p for k in ['KEDOKTERAN', 'PENDIDIKAN DOKTER', 'PSIKOLOGI']):
        return 'Kedokteran'
    return 'Lainnya'

df_snbt25_pendaftar.loc[:, 'fakultas'] = df_snbt25_pendaftar['NAMA PRODI TERIMA'].apply(classify_faculty)
df_snbt26_pendaftar.loc[:, 'fakultas'] = df_snbt26_pendaftar['prodi_nama'].apply(classify_faculty)

# ---------------------------------------------------------
# Print Summary Metrics
# ---------------------------------------------------------
total_25_pendaftar = len(df_snbt25_pendaftar)
acc_25 = df_snbt25_pendaftar['is_accepted'].sum()
rej_25 = total_25_pendaftar - acc_25

total_26_pendaftar = len(df_snbt26_pendaftar)
acc_26 = df_snbt26_pendaftar['is_accepted'].sum()
rej_26 = total_26_pendaftar - acc_26

print(f"\n--- RINGKASAN VERIFIKASI ---")
print(f"2025 SNBT Pendaftar: {total_25_pendaftar} | Diterima: {acc_25} ({acc_25/total_25_pendaftar*100:.2f}%) | Ditolak: {rej_25} ({rej_25/total_25_pendaftar*100:.2f}%)")
print(f"2026 SNBT Pendaftar: {total_26_pendaftar} | Diterima: {acc_26} ({acc_26/total_26_pendaftar*100:.2f}%) | Ditolak: {rej_26} ({rej_26/total_26_pendaftar*100:.2f}%)")
print(f"Dinamika Penolakan: +{rej_26 - rej_25} mhs (+{(rej_26 - rej_25)/rej_25*100:.1f}%)")

# ==============================================================================
# CHART 24: KOMPARASI KUOTA, PENDAFTAR, DAN LONJAKAN PENOLAKAN (2025 VS 2026)
# ==============================================================================
print("\nGenerating 24_komparasi_kuota_pendaftar_dan_rejection_2025_2026.png...")
fig24, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=300)

# Subplot 1: Kuota Beasiswa & Pendaftar Lolos Seleksi
categories = ['Total Kuota KIP\n(Semua Jalur)', 'Kuota KIP\nJalur SNBP', 'Kuota KIP\nJalur SNBT', 'Pendaftar KIP\nLolos SNBT']
val_2025 = [1846, 941, 905, 1275]
val_2026 = [1639, 893, 746, 1361]
x = np.arange(len(categories))
width = 0.35

rects1 = ax1.bar(x - width/2, val_2025, width, label='Tahun 2025', color='#3B82F6', edgecolor='#1D4ED8', linewidth=1.2, zorder=3)
rects2 = ax1.bar(x + width/2, val_2026, width, label='Tahun 2026', color='#0EA5E9', edgecolor='#0284C7', linewidth=1.2, zorder=3)

ax1.set_title('Perbandingan Alokasi Kuota KIP & Pendaftar Lolos SNBT\nUniversitas Syiah Kuala (2025 vs 2026)', fontsize=13, fontweight='bold', pad=15, color='#0F172A')
ax1.set_ylabel('Jumlah Mahasiswa (Orang)', fontsize=11, fontweight='bold', color='#1E293B')
ax1.set_xticks(x)
ax1.set_xticklabels(categories, fontsize=10.5, fontweight='bold', color='#1E293B')
ax1.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax1.legend(frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10.5)

# Value labels and delta annotations on Subplot 1
for i in range(len(categories)):
    y1 = val_2025[i]
    y2 = val_2026[i]
    diff = y2 - y1
    pct = (diff / y1) * 100
    ax1.text(x[i] - width/2, y1 + 25, f"{y1:,}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1E293B')
    ax1.text(x[i] + width/2, y2 + 25, f"{y2:,}", ha='center', va='bottom', fontsize=10, fontweight='bold', color='#1E293B')
    
    # Delta Badge
    badge_color = '#DC2626' if diff < 0 else '#059669'
    delta_str = f"{diff:+d} ({pct:+.1f}%)"
    ax1.text(x[i], max(y1, y2) + 115, delta_str, ha='center', va='bottom', fontsize=9.5, fontweight='bold', 
             bbox=dict(boxstyle='round,pad=0.25', facecolor='#F8FAFC', edgecolor=badge_color, linewidth=1.2))

ax1.set_ylim(0, 2250)

# Subplot 2: Hasil Seleksi KIP SNBT (Diterima vs Ditolak)
years = ['SNBT 2025\n(Total: 1.275 mhs)', 'SNBT 2026\n(Total: 1.361 mhs)']
acc_vals = [905, 746]
rej_vals = [370, 615]
x2 = np.arange(len(years))
width2 = 0.45

p_acc = ax2.bar(x2, acc_vals, width2, label='Diterima KIP-Kuliah', color='#059669', edgecolor='#047857', linewidth=1.2, zorder=3)
p_rej = ax2.bar(x2, rej_vals, width2, bottom=acc_vals, label='Ditolak KIP-Kuliah', color='#DC2626', edgecolor='#B91C1C', linewidth=1.2, zorder=3)

ax2.set_title('Hasil Seleksi KIP-Kuliah Jalur SNBT\nLonjakan Penolakan Akibat Pemotongan Kuota & Kenaikan Pendaftar', fontsize=13, fontweight='bold', pad=15, color='#0F172A')
ax2.set_ylabel('Jumlah Pendaftar Lolos Akademik (Orang)', fontsize=11, fontweight='bold', color='#1E293B')
ax2.set_xticks(x2)
ax2.set_xticklabels(years, fontsize=11, fontweight='bold', color='#1E293B')
ax2.grid(axis='y', linestyle='--', alpha=0.5, zorder=0)
ax2.legend(frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10.5, loc='upper left')

# Annotations on Subplot 2
# 2025
ax2.text(0, acc_vals[0]/2, f"DITERIMA\n{acc_vals[0]} mhs\n(71,0%)", ha='center', va='center', fontsize=11, fontweight='bold', color='white')
ax2.text(0, acc_vals[0] + rej_vals[0]/2, f"DITOLAK\n{rej_vals[0]} mhs\n(29,0%)", ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# 2026
ax2.text(1, acc_vals[1]/2, f"DITERIMA\n{acc_vals[1]} mhs\n(54,8%)", ha='center', va='center', fontsize=11, fontweight='bold', color='white')
ax2.text(1, acc_vals[1] + rej_vals[1]/2, f"DITOLAK\n{rej_vals[1]} mhs\n(45,2%)", ha='center', va='center', fontsize=11, fontweight='bold', color='white')

# Highlight callout box
ax2.annotate('LONJAKAN PENOLAKAN:\n+245 Mahasiswa (+66,2%)\nTingkat Tolak Naik dari 29,0% ke 45,2%',
             xy=(1, acc_vals[1] + rej_vals[1]), xytext=(0.4, 1500),
             arrowprops=dict(facecolor='#DC2626', shrink=0.05, width=1.5, headwidth=7),
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF2F2', edgecolor='#DC2626', linewidth=1.5),
             fontsize=10.5, fontweight='bold', color='#991B1B')

ax2.set_ylim(0, 1650)

plt.tight_layout()
fig24_path = os.path.join(chart_dir, '24_komparasi_kuota_pendaftar_dan_rejection_2025_2026.png')
fig24.savefig(fig24_path, dpi=300)
plt.close(fig24)
print(f"Saved: {fig24_path}")

# ==============================================================================
# CHART 25: ANALISIS DEMOGRAFI & PENOLAKAN KIP SNBT 2025 (FAKULTAS, GENDER, JENJANG)
# ==============================================================================
print("\nGenerating 25_analisis_demografi_dan_penolakan_kip_2025.png...")
fig25, (ax_fak, ax_gen) = plt.subplots(1, 2, figsize=(18, 8.5), dpi=300)

# Fak stats 2025
fak_stat25 = df_snbt25_pendaftar.groupby('fakultas')['is_accepted'].agg(
    total='count',
    accepted='sum',
    rejected=lambda x: (x == False).sum()
).reset_index()
fak_stat25['reject_rate'] = fak_stat25['rejected'] / fak_stat25['total'] * 100
fak_stat25 = fak_stat25.sort_values(by='rejected', ascending=True)

y_pos = np.arange(len(fak_stat25))
bars_acc = ax_fak.barh(y_pos, fak_stat25['accepted'], color='#059669', edgecolor='#047857', label='Diterima KIP', height=0.6, zorder=3)
bars_rej = ax_fak.barh(y_pos, fak_stat25['rejected'], left=fak_stat25['accepted'], color='#DC2626', edgecolor='#B91C1C', label='Ditolak KIP', height=0.6, zorder=3)

ax_fak.set_yticks(y_pos)
ax_fak.set_yticklabels(fak_stat25['fakultas'], fontsize=10, fontweight='bold', color='#1E293B')
ax_fak.set_xlabel('Jumlah Pendaftar KIP Lolos Akademik SNBT 2025 (Orang)', fontsize=11, fontweight='bold', color='#1E293B')
ax_fak.set_title('Sebaran Hasil Seleksi KIP-Kuliah SNBT 2025 per Fakultas\n(Diurutkan dari Penolakan Tertinggi)', fontsize=12.5, fontweight='bold', pad=15, color='#0F172A')
ax_fak.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
ax_fak.legend(frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10, loc='lower right')

# Add annotations to faculty bars
for i, row in fak_stat25.reset_index().iterrows():
    tot = row['total']
    rej = row['rejected']
    acc = row['accepted']
    rate = row['reject_rate']
    label_text = f" {tot} (Tolak: {rej} | {rate:.1f}%)"
    ax_fak.text(tot + 3, i, label_text, va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

ax_fak.set_xlim(0, 520)

# Gender and Jenjang breakdown
gender_stat25 = df_snbt25_pendaftar.groupby('JENIS KEL')['is_accepted'].agg(
    total='count',
    accepted='sum',
    rejected=lambda x: (x == False).sum()
).reset_index()
gender_stat25['gender_label'] = gender_stat25['JENIS KEL'].map({'L': 'Laki-laki', 'P': 'Perempuan'})

jenjang_stat25 = df_snbt25_pendaftar.groupby('JENJANG PRODI TERIMA')['is_accepted'].agg(
    total='count',
    accepted='sum',
    rejected=lambda x: (x == False).sum()
).reset_index()

# Make Subplot 2 a two-panel comparison (Upper: Gender, Lower: Jenjang)
ax_gen.axis('off')
sub_gs = ax_gen.get_subplotspec().subgridspec(2, 1, hspace=0.35)
ax_gen_top = fig25.add_subplot(sub_gs[0])
ax_gen_bot = fig25.add_subplot(sub_gs[1])

# Gender Plot
y_g = np.arange(len(gender_stat25))
ax_gen_top.barh(y_g, gender_stat25['accepted'], color='#059669', edgecolor='#047857', height=0.5, label='Diterima', zorder=3)
ax_gen_top.barh(y_g, gender_stat25['rejected'], left=gender_stat25['accepted'], color='#DC2626', edgecolor='#B91C1C', height=0.5, label='Ditolak', zorder=3)
ax_gen_top.set_yticks(y_g)
ax_gen_top.set_yticklabels(gender_stat25['gender_label'], fontsize=10.5, fontweight='bold', color='#1E293B')
ax_gen_top.set_title('A. Proporsi Seleksi Berdasarkan Gender (SNBT 2025)', fontsize=11, fontweight='bold', pad=10, color='#0F172A')
ax_gen_top.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)

for i, r in gender_stat25.iterrows():
    tot = r['total']
    acc = r['accepted']
    rej = r['rejected']
    ax_gen_top.text(tot + 15, i, f"Total: {tot} (Diterima: {acc} | Tolak: {rej} - {rej/tot*100:.1f}%)", va='center', fontsize=9.5, fontweight='bold', color='#1E293B')
ax_gen_top.set_xlim(0, 1150)

# Jenjang Plot
jenjang_stat25 = jenjang_stat25.sort_values(by='total', ascending=True)
y_j = np.arange(len(jenjang_stat25))
ax_gen_bot.barh(y_j, jenjang_stat25['accepted'], color='#059669', edgecolor='#047857', height=0.5, label='Diterima', zorder=3)
ax_gen_bot.barh(y_j, jenjang_stat25['rejected'], left=jenjang_stat25['accepted'], color='#DC2626', edgecolor='#B91C1C', height=0.5, label='Ditolak', zorder=3)
ax_gen_bot.set_yticks(y_j)
ax_gen_bot.set_yticklabels(jenjang_stat25['JENJANG PRODI TERIMA'], fontsize=10.5, fontweight='bold', color='#1E293B')
ax_gen_bot.set_title('B. Proporsi Seleksi Berdasarkan Jenjang Studi (SNBT 2025)', fontsize=11, fontweight='bold', pad=10, color='#0F172A')
ax_gen_bot.set_xlabel('Jumlah Pendaftar (Orang)', fontsize=10.5, fontweight='bold', color='#1E293B')
ax_gen_bot.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)

for i, r in jenjang_stat25.reset_index().iterrows():
    tot = r['total']
    acc = r['accepted']
    rej = r['rejected']
    ax_gen_bot.text(tot + 15, i, f"Total: {tot} (Diterima: {acc} | Tolak: {rej} - {rej/tot*100:.1f}%)", va='center', fontsize=9.5, fontweight='bold', color='#1E293B')
ax_gen_bot.set_xlim(0, 1400)

plt.tight_layout()
fig25_path = os.path.join(chart_dir, '25_analisis_demografi_dan_penolakan_kip_2025.png')
fig25.savefig(fig25_path, dpi=300)
plt.close(fig25)
print(f"Saved: {fig25_path}")

# ==============================================================================
# CHART 26: TREN TOP 10 PRODI DENGAN PENOLAKAN KIP TERTINGGI (2025 VS 2026)
# ==============================================================================
print("\nGenerating 26_tren_prodi_penolakan_kip_2025_vs_2026.png...")
fig26, (ax_p25, ax_p26) = plt.subplots(1, 2, figsize=(19, 8.5), dpi=300)

# Top 10 Rejected Prodi 2025
p_stat25 = df_snbt25_pendaftar.groupby('NAMA PRODI TERIMA')['is_accepted'].agg(
    total='count',
    accepted='sum',
    rejected=lambda x: (x == False).sum()
).reset_index()
p_stat25['reject_rate'] = p_stat25['rejected'] / p_stat25['total'] * 100
top10_25 = p_stat25.sort_values(by=['rejected', 'total'], ascending=True).tail(10)

y_25 = np.arange(len(top10_25))
ax_p25.barh(y_25, top10_25['accepted'], color='#059669', edgecolor='#047857', height=0.6, label='Diterima KIP', zorder=3)
ax_p25.barh(y_25, top10_25['rejected'], left=top10_25['accepted'], color='#DC2626', edgecolor='#B91C1C', height=0.6, label='Ditolak KIP', zorder=3)
ax_p25.set_yticks(y_25)
ax_p25.set_yticklabels(top10_25['NAMA PRODI TERIMA'], fontsize=9.5, fontweight='bold', color='#1E293B')
ax_p25.set_xlabel('Jumlah Pendaftar Lolos SNBT (Orang)', fontsize=11, fontweight='bold', color='#1E293B')
ax_p25.set_title('Top 10 Program Studi Penolakan KIP Terbanyak - 2025\n(Kandidat Rentan Tidak Daftar Ulang)', fontsize=12, fontweight='bold', pad=15, color='#0F172A')
ax_p25.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
ax_p25.legend(frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10, loc='lower right')

for i, r in top10_25.reset_index().iterrows():
    tot = r['total']
    rej = r['rejected']
    pct = r['reject_rate']
    ax_p25.text(tot + 0.8, i, f" {rej} ditolak ({pct:.0f}%)", va='center', fontsize=9.5, fontweight='bold', color='#991B1B')
ax_p25.set_xlim(0, 55)

# Top 10 Rejected Prodi 2026
p_stat26 = df_snbt26_pendaftar.groupby('prodi_nama')['is_accepted'].agg(
    total='count',
    accepted='sum',
    rejected=lambda x: (x == False).sum()
).reset_index()
p_stat26['reject_rate'] = p_stat26['rejected'] / p_stat26['total'] * 100
top10_26 = p_stat26.sort_values(by=['rejected', 'total'], ascending=True).tail(10)

y_26 = np.arange(len(top10_26))
ax_p26.barh(y_26, top10_26['accepted'], color='#059669', edgecolor='#047857', height=0.6, label='Diterima KIP', zorder=3)
ax_p26.barh(y_26, top10_26['rejected'], left=top10_26['accepted'], color='#DC2626', edgecolor='#B91C1C', height=0.6, label='Ditolak KIP', zorder=3)
ax_p26.set_yticks(y_26)
ax_p26.set_yticklabels(top10_26['prodi_nama'], fontsize=9.5, fontweight='bold', color='#1E293B')
ax_p26.set_xlabel('Jumlah Pendaftar Lolos SNBT (Orang)', fontsize=11, fontweight='bold', color='#1E293B')
ax_p26.set_title('Top 10 Program Studi Penolakan KIP Terbanyak - 2026\n(Beban Penolakan Melonjak Drastis)', fontsize=12, fontweight='bold', pad=15, color='#0F172A')
ax_p26.grid(axis='x', linestyle='--', alpha=0.5, zorder=0)
ax_p26.legend(frameon=True, facecolor='white', edgecolor='#CBD5E1', fontsize=10, loc='lower right')

for i, r in top10_26.reset_index().iterrows():
    tot = r['total']
    rej = r['rejected']
    pct = r['reject_rate']
    ax_p26.text(tot + 0.8, i, f" {rej} ditolak ({pct:.0f}%)", va='center', fontsize=9.5, fontweight='bold', color='#991B1B')
ax_p26.set_xlim(0, 55)

plt.tight_layout()
fig26_path = os.path.join(chart_dir, '26_tren_prodi_penolakan_kip_2025_vs_2026.png')
fig26.savefig(fig26_path, dpi=300)
plt.close(fig26)
print(f"Saved: {fig26_path}")

print("\nAll 3 charts generated successfully!")
