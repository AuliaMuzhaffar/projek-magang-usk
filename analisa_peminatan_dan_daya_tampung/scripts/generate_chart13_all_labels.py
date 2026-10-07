"""
Script untuk meng-generate Chart 13 Versi Komparasi (Seluruh 66 Label Prodi):
13_matriks_4_kuadran_5_tahun_2022_2026_all_labels.png
Menerapkan Opsi 1: Ukuran titik seragam dan menghapus legenda kapasitas kuota (chartjunk removal)
untuk visualisasi eksekutif yang bersih dan fokus pada 2 sumbu strategis.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text

def main():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    excel_path = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "data", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    chart_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "grafik")
    os.makedirs(chart_dir, exist_ok=True)

    print("Loading data from Excel for all-labels comparison (Option 1)...")
    df_s1 = pd.read_excel(excel_path, sheet_name="S1_Kampus_Utama")
    rev_map = {
        'Nama Program Studi': 'Program_Studi',
        'Fakultas': 'Fakultas',
        'Rata Fill Rate 5-Thn (%)': 'Rata_FillRate_5Thn_Persen',
        'Rata Keketatan 5-Thn': 'Rata_Keketatan_5Thn',
        'Rata DT 5-Thn': 'Rata_DT_5Thn',
        'Rata DU 5-Thn': 'Rata_DU_5Thn',
        'Rata Peminat 5-Thn': 'Rata_Peminat_5Thn'
    }
    df_s1 = df_s1.rename(columns=rev_map)

    # 16:9 widescreen canvas, high resolution
    fig, ax = plt.subplots(figsize=(22, 12), dpi=300, facecolor='#FFFFFF')
    ax.set_facecolor('#FFFFFF')

    # x_max disesuaikan ke 52 agar Farmasi (44,06) memiliki ruang bernapas
    x_max = 52
    y_min, y_max = 24, 106

    # Piecewise transformation to widen dense lower range (Kuadran IV: 0 to 4.0)
    def forward(x):
        x = np.asarray(x, dtype=float)
        res = np.zeros_like(x)
        m1 = (x <= 4.0)
        res[m1] = x[m1] * (36.0 / 4.0)
        m2 = (x > 4.0) & (x <= 22.0)
        res[m2] = 36.0 + (x[m2] - 4.0) * (42.0 / 18.0)
        m3 = (x > 22.0)
        res[m3] = 78.0 + (x[m3] - 22.0) * (22.0 / (x_max - 22.0))
        return res

    def inverse(y):
        y = np.asarray(y, dtype=float)
        res = np.zeros_like(y)
        m1 = (y <= 36.0)
        res[m1] = y[m1] * (4.0 / 36.0)
        m2 = (y > 36.0) & (y <= 78.0)
        res[m2] = 4.0 + (y[m2] - 36.0) * (18.0 / 42.0)
        m3 = (y > 78.0)
        res[m3] = 22.0 + (y[m3] - 78.0) * ((x_max - 22.0) / 22.0)
        return res

    ax.set_xscale('function', functions=(forward, inverse))

    # Background Quadrants
    ax.axvspan(4.0, x_max, ymin=(80 - y_min)/(y_max - y_min), ymax=1.0, color='#F0FDF4', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=(80 - y_min)/(y_max - y_min), ymax=1.0, color='#F0F9FF', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=0.0, ymax=(80 - y_min)/(y_max - y_min), color='#FFF1F2', alpha=0.55, zorder=0)
    ax.axvspan(4.0, x_max, ymin=0.0, ymax=(80 - y_min)/(y_max - y_min), color='#FFFBEB', alpha=0.55, zorder=0)

    # Benchmark Lines & Badges (Varian 1: Cool Slate Grey - Netral, Lembut, Non-Hitam)
    line_slate = '#64748B'
    bg_slate = '#475569'
    border_slate = '#94A3B8'

    ax.axvline(x=4.0, color=line_slate, linestyle='--', linewidth=1.9, alpha=0.9, zorder=2)
    ax.axhline(y=80.0, color=line_slate, linestyle='--', linewidth=1.9, alpha=0.9, zorder=2)

    # Badge Horizontal 80% (Pill solid non-black, anchor kanan rapi)
    ax.text(49.5, 80.0, ' STANDAR KETERISIAN: 80% (TARGET SEHAT) ',
            ha='right', va='center', fontsize=9.0, color='#FFFFFF', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.35,rounding_size=0.5', facecolor=bg_slate, edgecolor=border_slate, linewidth=1.2, alpha=0.98),
            zorder=5)

    # Badge Vertikal 4.0 (Pill solid non-black, anchor sumbu X)
    ax.text(4.0, 25.5, ' ▲ AMBANG KEKETATAN: 4,0 : 1 ',
            ha='center', va='bottom', fontsize=9.0, color='#FFFFFF', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.35,rounding_size=0.5', facecolor=bg_slate, edgecolor=border_slate, linewidth=1.2, alpha=0.98),
            zorder=5)

    # Quadrant titles
    ax.text(x_max - 1.5, 104.0, 'KUADRAN I: UNGGULAN\n28 Program Studi (42,4%)',
            ha='right', va='top', fontsize=12, fontweight='bold', color='#047857', alpha=0.9, zorder=2, linespacing=1.2)
    ax.text(0.6, 104.0, 'KUADRAN II: STABIL\n4 Program Studi (6,1%)',
            ha='left', va='top', fontsize=12, fontweight='bold', color='#1D4ED8', alpha=0.9, zorder=2, linespacing=1.2)
    ax.text(x_max - 1.5, 26.5, 'KUADRAN III: BELUM OPTIMAL\n(Peminat Tinggi, Keterisian Belum Optimal)\n8 Program Studi (12,1%)',
            ha='right', va='bottom', fontsize=11, fontweight='bold', color='#B45309', alpha=0.9, zorder=2, linespacing=1.2)
    ax.text(0.6, 26.5, 'KUADRAN IV: PERLU REVITALISASI\n26 Program Studi (39,4%)',
            ha='left', va='bottom', fontsize=12, fontweight='bold', color='#B91C1C', alpha=0.9, zorder=2, linespacing=1.2)

    # Colors
    pt_cols_5y = []
    for _, r in df_s1.iterrows():
        x = r['Rata_Keketatan_5Thn']
        y = r['Rata_FillRate_5Thn_Persen']
        if x >= 4.0 and y >= 80.0:
            pt_cols_5y.append('#059669') # Emerald (Q1)
        elif x < 4.0 and y >= 80.0:
            pt_cols_5y.append('#2563EB') # Blue (Q2)
        elif x >= 4.0 and y < 80.0:
            pt_cols_5y.append('#D97706') # Amber (Q3: Belum Optimal)
        else:
            pt_cols_5y.append('#E11D48') # Rose Red (Q4: Perlu Revitalisasi)

    # OPSI 1: Ukuran titik seragam (90 pt), sangat bersih dan proporsional
    ax.scatter(df_s1['Rata_Keketatan_5Thn'], df_s1['Rata_FillRate_5Thn_Persen'],
               s=90, c=pt_cols_5y, edgecolors='#0F172A', linewidths=1.2, alpha=0.90, zorder=4)

    fak_abbr = {
        'Kedokteran': 'FK',
        'Kedokteran Gigi': 'FKG',
        'Kedokteran Hewan': 'FKH',
        'Keperawatan': 'FKep',
        'MIPA': 'FMIPA',
        'Teknik': 'FT',
        'Ekonomi dan Bisnis': 'FEB',
        'FISIP': 'FISIP',
        'FKIP': 'FKIP',
        'Hukum': 'FH',
        'Pertanian': 'FP',
        'Kelautan dan Perikanan': 'FPK'
    }

    prodi_short = {
        'PENDIDIKAN PANCASILA DAN KEWARGANEGARAAN': 'PPKn',
        'PENDIDIKAN KESEJAHTERAAN KELUARGA': 'PKK',
        'PENDIDIKAN SENI DRAMA TARI DAN MUSIK': 'Sendratasik',
        'PENDIDIKAN JASMANI KESEHATAN DAN REKREASI': 'Penjaskesrek',
        'PERENCANAAN WILAYAH DAN KOTA': 'PWK',
        'TEKNOLOGI INDUSTRI HASIL PERIKANAN': 'TIHP',
        'PEMANFAATAN SUMBERDAYA PERIKANAN': 'PSP',
        'PENDIDIKAN GURU SEKOLAH DASAR': 'PGSD',
        'PENDIDIKAN GURU PENDIDIKAN ANAK USIA DINI': 'PAUD',
        'PENDIDIKAN GURU PAUD': 'PAUD',
        'TEKNIK SUMBER DAYA AIR': 'TSDA',
        'TEKNOLOGI HASIL PERTANIAN': 'THP',
        'PENDIDIKAN DOKTER HEWAN': 'Dokter Hewan',
        'PENDIDIKAN BAHASA INGGRIS': 'Bhs Inggris',
        'PENDIDIKAN BAHASA INDONESIA': 'Bhs Indonesia',
        'PENDIDIKAN DOKTER GIGI': 'Dokter Gigi',
        'PENDIDIKAN DOKTER': 'Dokter',
        'BIMBINGAN KONSELING': 'Bimb. Konseling',
        'EKONOMI PEMBANGUNAN': 'Ek. Pembangunan',
        'PENDIDIKAN MATEMATIKA': 'Pend. Mat.',
        'PENDIDIKAN GEOGRAFI': 'Pend. Geografi',
        'PENDIDIKAN EKONOMI': 'Pend. Ekonomi',
        'PENDIDIKAN KIMIA': 'Pend. Kimia',
        'PENDIDIKAN FISIKA': 'Pend. Fisika',
        'PENDIDIKAN BIOLOGI': 'Pend. Biologi',
        'PENDIDIKAN SEJARAH': 'Pend. Sejarah'
    }

    texts = []
    pts_x = []
    pts_y = []

    for _, r in df_s1.iterrows():
        raw_p = r['Program_Studi']
        p_name = prodi_short.get(raw_p.strip(), raw_p.title())
        f_abbr = fak_abbr.get(r['Fakultas'], r['Fakultas'])
        lbl = f'{p_name} ({f_abbr})'
        px = float(r['Rata_Keketatan_5Thn'])
        py = float(r['Rata_FillRate_5Thn_Persen'])

        # Farmasi ditempatkan secara presisi tepat di samping titiknya
        if 'FARMASI' in raw_p.upper():
            ax.annotate(lbl,
                        xy=(px, py),
                        xytext=(-10, 0),
                        textcoords='offset points',
                        ha='right',
                        va='center',
                        fontsize=7.2,
                        fontweight='bold',
                        color='#1E293B',
                        bbox=dict(boxstyle='round,pad=0.18', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.6, alpha=0.95),
                        arrowprops=dict(arrowstyle='->', color='#64748B', lw=0.6, shrinkA=2, shrinkB=4),
                        zorder=7)
            continue

        pts_x.append(px)
        pts_y.append(py)

        # Smart initial directional dispersion
        if px < 4.0 and py < 80.0:  # Kuadran IV
            if py < 62.0:
                init_y = py - 4.2
                init_x = px - 0.25
            elif px < 2.2:
                init_y = py + 3.2
                init_x = px - 0.35
            else:
                init_y = py - 3.8
                init_x = px + 0.15
        elif px >= 4.0 and py >= 80.0:  # Kuadran I
            if py > 94.0:
                init_y = py + 3.2
                init_x = px
            elif px > 10.0:
                init_y = py + 1.8
                init_x = px + 1.0
            else:
                init_y = py + 2.5
                init_x = px + 0.5
        elif px < 4.0 and py >= 80.0:  # Kuadran II
            init_y = py + 2.2
            init_x = px - 0.5
        else:  # Kuadran III
            init_y = py - 2.8
            init_x = px + 1.0

        t = ax.text(init_x, init_y, lbl, fontsize=6.6, fontweight='bold', color='#1E293B',
                    bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.5, alpha=0.92),
                    zorder=6)
        texts.append(t)

    print(f"Mengoptimasi penempatan {len(texts)} label prodi dengan collision repulsion...")
    adjust_text(texts,
                target_x=pts_x,
                target_y=pts_y,
                arrowprops=dict(arrowstyle='->', color='#64748B', lw=0.55, shrinkA=1, shrinkB=2),
                expand=(1.4, 1.6),
                force_text=(0.8, 1.2),
                force_static=(0.6, 0.8),
                prevent_crossings=True,
                iter_lim=500)

    ax.set_xlim(0, x_max)
    ax.set_ylim(y_min, y_max)

    x_ticks = [0, 1, 2, 3, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50]
    ax.set_xticks(x_ticks)
    ax.tick_params(axis='x', labelsize=10.5, colors='#1E293B')
    ax.tick_params(axis='y', labelsize=10.5, colors='#1E293B')

    ax.set_xlabel('Rasio Keketatan Seleksi (Peminat per 1 Kursi Daya Tampung)', fontsize=12, fontweight='bold', color='#1E293B', labelpad=12)
    ax.set_ylabel('Persentase Keterisian Kuota / Fill Rate (%)', fontsize=12, fontweight='bold', color='#1E293B', labelpad=14)
    ax.set_title('Peta Portofolio 66 Program Studi S1 Kampus Utama USK - VERSI SELURUH 66 LABEL PRODI', fontsize=13.5, fontweight='bold', pad=14, color='#0F172A')

    ax.grid(True, linestyle=':', alpha=0.45, color='#94A3B8', zorder=0)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')

    # OPSI 1: Tidak ada legenda ukuran kuota (chartjunk dihapus!)
    plt.tight_layout()
    out_file = os.path.join(chart_dir, "13_matriks_4_kuadran_5_tahun_2022_2026_all_labels.png")
    plt.savefig(out_file, dpi=300)
    plt.close()
    print(f"Berhasil membuat chart perbandingan (Opsi 1) di: {out_file}")

if __name__ == "__main__":
    main()
