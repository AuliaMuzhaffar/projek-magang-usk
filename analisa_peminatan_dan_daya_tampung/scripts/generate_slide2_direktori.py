"""
Script untuk meng-generate Slide 2 (Companion Slide):
Direktori Lengkap 66 Program Studi S1 Kampus Utama USK Berdasarkan Matriks 4 Kuadran
Rata-rata Longitudinal 5 Tahun (2022–2026).
Didesain khusus untuk bahan pendukung Wakil Rektor & Direktur Akademik dalam rapat dekan.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    excel_path = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "data", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    chart_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "grafik")
    os.makedirs(chart_dir, exist_ok=True)

    print("Loading data from Excel...")
    df = pd.read_excel(excel_path, sheet_name="S1_Kampus_Utama")
    
    # Mapping nama kolom
    col_map = {
        'Nama Program Studi': 'Prodi',
        'Fakultas': 'Fakultas',
        'Rata Keketatan 5-Thn': 'Keketatan',
        'Rata Fill Rate 5-Thn (%)': 'FillRate',
        'Rata DT 5-Thn': 'DT',
        'Rata DU 5-Thn': 'DU'
    }
    df = df.rename(columns=col_map)

    # Singkatan Fakultas agar ringkas & elegan
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
    df['Fak_Abbr'] = df['Fakultas'].map(fak_abbr).fillna(df['Fakultas'])

    # Penyederhanaan nama prodi panjang agar pas di kartu tanpa overlap
    prodi_short = {
        'PENDIDIKAN PANCASILA DAN KEWARGANEGARAAN': 'PPKn',
        'PENDIDIKAN KESEJAHTERAAN KELUARGA': 'PKK',
        'PENDIDIKAN SENI DRAMA TARI DAN MUSIK': 'Sendratasik',
        'PENDIDIKAN JASMANI KESEHATAN DAN REKREASI': 'Penjaskesrek',
        'PERENCANAAN WILAYAH DAN KOTA': 'PWK',
        'TEKNOLOGI INDUSTRI HASIL PERIKANAN': 'TIHP Perikanan',
        'PEMANFAATAN SUMBERDAYA PERIKANAN': 'PSP Perikanan',
        'PENDIDIKAN GURU SEKOLAH DASAR': 'PGSD',
        'PENDIDIKAN GURU PENDIDIKAN ANAK USIA DINI': 'Pend. Guru PAUD',
        'PENDIDIKAN GURU PAUD': 'Pend. Guru PAUD',
        'TEKNIK SUMBER DAYA AIR': 'TSDA',
        'TEKNOLOGI HASIL PERTANIAN': 'THP',
        'PENDIDIKAN DOKTER HEWAN': 'Dokter Hewan',
        'PENDIDIKAN BAHASA INGGRIS': 'Pend. Bhs Inggris',
        'PENDIDIKAN BAHASA INDONESIA': 'Pend. Bhs Indonesia',
        'PENDIDIKAN DOKTER GIGI': 'Dokter Gigi',
        'PENDIDIKAN DOKTER': 'Pend. Dokter',
        'BIMBINGAN KONSELING': 'Bimb. Konseling',
        'EKONOMI PEMBANGUNAN': 'Ek. Pembangunan',
        'PENDIDIKAN MATEMATIKA': 'Pend. Matematika',
        'PENDIDIKAN GEOGRAFI': 'Pend. Geografi',
        'PENDIDIKAN EKONOMI': 'Pend. Ekonomi',
        'PENDIDIKAN KIMIA': 'Pend. Kimia',
        'PENDIDIKAN FISIKA': 'Pend. Fisika',
        'PENDIDIKAN BIOLOGI': 'Pend. Biologi',
        'PENDIDIKAN SEJARAH': 'Pend. Sejarah'
    }
    df['Prodi_Label'] = df['Prodi'].apply(lambda x: prodi_short.get(x.strip(), x.title()))

    # Klasifikasi Kuadran (Sesuai Konvensi Baru)
    # Q1: Kek >= 4.0 & FR >= 80% (Unggulan)
    # Q2: Kek < 4.0 & FR >= 80% (Stabil)
    # Q3: Kek >= 4.0 & FR < 80% (Belum Optimal)
    # Q4: Kek < 4.0 & FR < 80% (Perlu Revitalisasi)
    def assign_quadrant(r):
        k = r['Keketatan']
        f = r['FillRate']
        if k >= 4.0 and f >= 80.0:
            return 'Q1'
        elif k < 4.0 and f >= 80.0:
            return 'Q2'
        elif k >= 4.0 and f < 80.0:
            return 'Q3'
        else:
            return 'Q4'

    df['Kuadran'] = df.apply(assign_quadrant, axis=1)

    df_q1 = df[df['Kuadran'] == 'Q1'].sort_values(by='FillRate', ascending=False).reset_index(drop=True)
    df_q2 = df[df['Kuadran'] == 'Q2'].sort_values(by='FillRate', ascending=False).reset_index(drop=True)
    df_q3 = df[df['Kuadran'] == 'Q3'].sort_values(by='FillRate', ascending=False).reset_index(drop=True)
    df_q4 = df[df['Kuadran'] == 'Q4'].sort_values(by='FillRate', ascending=False).reset_index(drop=True)

    print(f"Data counts -> Q1: {len(df_q1)}, Q2: {len(df_q2)}, Q3: {len(df_q3)}, Q4: {len(df_q4)} (Total: {len(df)})")

    # Inisialisasi Canvas Widescreen 16:9 Ultra-HD
    fig, ax = plt.subplots(figsize=(18, 10.125), dpi=300, facecolor='#F8FAFC')
    ax.set_facecolor('#F8FAFC')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # =========================================================================
    # HEADER UTAMA SLIDE
    # =========================================================================
    ax.text(3.0, 97.2, "DIREKTORI PORTOFOLIO 66 PROGRAM STUDI S1 KAMPUS UTAMA USK",
            fontsize=15.5, fontweight='bold', color='#0F172A', va='center')
    ax.text(3.0, 94.6, "Rata-rata 5 Tahun (2022–2026) | Bahan Rapat Pimpinan: Wakil Rektor & Para Dekan Fakultas",
            fontsize=10.2, color='#475569', va='center')

    # Badge Pendamping Chart 13
    ax.text(97.0, 95.8, "SLIDE PENDAMPING (COMPANION ROSTER)\nUNTUK MATRIKS 4 KUADRAN",
            fontsize=8.5, fontweight='bold', color='#334155', ha='right', va='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=1.0))

    # Garis Pembatas Header
    ax.plot([3.0, 97.0], [93.2, 93.2], color='#E2E8F0', lw=1.2)

    # =========================================================================
    # FUNGSI HELPER: GAMBAR CARD CONTAINER
    # =========================================================================
    def draw_card(x0, y0, width, height, bg_col, border_col, header_col, title_text, count_text, policy_text, sublabel=None):
        # Background card
        rect = patches.FancyBboxPatch((x0, y0), width, height, boxstyle="round,pad=0.3,rounding_size=1.2",
                                      facecolor=bg_col, edgecolor=border_col, linewidth=1.4, zorder=1)
        ax.add_patch(rect)

        # Header banner bar
        header_height = 4.2
        header_rect = patches.FancyBboxPatch((x0, y0 + height - header_height), width, header_height,
                                            boxstyle="round,pad=0.1,rounding_size=0.8",
                                            facecolor=header_col, edgecolor='none', zorder=2)
        ax.add_patch(header_rect)

        # Title & Count in header
        ax.text(x0 + 1.2, y0 + height - 2.1, title_text, fontsize=11.5, fontweight='bold', color='#FFFFFF', va='center', zorder=3)
        ax.text(x0 + width - 1.2, y0 + height - 2.1, count_text, fontsize=10.0, fontweight='bold', color='#FFFFFF', ha='right', va='center', zorder=3)

        # Sub-header policy strip
        sub_y = y0 + height - header_height - 1.8
        sub_text = f"Kebijakan: {policy_text}"
        if sublabel:
            sub_text = f"{sublabel} | {sub_text}"
        ax.text(x0 + 1.2, sub_y, sub_text, fontsize=8.6, fontweight='bold', color=header_col, va='center', zorder=3)
        
        # Garis tipis pembatas sub-header
        ax.plot([x0 + 1.0, x0 + width - 1.0], [sub_y - 1.2, sub_y - 1.2], color=border_col, lw=0.9, zorder=2)
        return sub_y - 2.0

    # Layout Koordinat 4 Kartu (2x2)
    # Kolom Kiri: x = 3.0 s.d. 48.5 (lebar = 45.5)
    # Kolom Kanan: x = 51.5 s.d. 97.0 (lebar = 45.5)
    # Baris Atas: y = 50.5 s.d. 91.5 (tinggi = 41.0)
    # Baris Bawah: y = 3.5 s.d. 48.0 (tinggi = 44.5)

    # -------------------------------------------------------------------------
    # 1. TOP-LEFT: KUADRAN II - STABIL (4 Prodi | 6,1%)
    # -------------------------------------------------------------------------
    content_top_y2 = draw_card(
        x0=3.0, y0=50.5, width=45.5, height=41.0,
        bg_col='#F0F9FF', border_col='#BAE6FD', header_col='#1D4ED8',
        title_text="KUADRAN II: STABIL",
        count_text="4 Program Studi (6,1%)",
        policy_text="Lindungi & Pertahankan Kapasitas (Equilibrium)"
    )

    # Table Header Q2
    y_curr = content_top_y2 - 0.5
    ax.text(4.2, y_curr, "NO", fontsize=8.2, fontweight='bold', color='#475569')
    ax.text(6.8, y_curr, "PROGRAM STUDI (FAKULTAS)", fontsize=8.2, fontweight='bold', color='#475569')
    ax.text(32.5, y_curr, "KEKETATAN", fontsize=8.2, fontweight='bold', color='#475569', ha='right')
    ax.text(40.0, y_curr, "FILL RATE", fontsize=8.2, fontweight='bold', color='#475569', ha='right')
    ax.text(47.0, y_curr, "KUOTA", fontsize=8.2, fontweight='bold', color='#475569', ha='right')
    y_curr -= 1.4
    ax.plot([4.0, 47.5], [y_curr + 0.4, y_curr + 0.4], color='#CBD5E1', lw=0.7)

    # Render 4 Prodi Q2
    for idx, r in df_q2.iterrows():
        y_curr -= 2.3
        bg_row = '#E0F2FE' if idx % 2 == 0 else '#F0F9FF'
        ax.add_patch(patches.Rectangle((4.0, y_curr - 0.7), 43.5, 2.3, facecolor=bg_row, edgecolor='none', zorder=2))
        
        ax.text(4.5, y_curr + 0.4, f"{idx+1}", fontsize=8.6, fontweight='bold', color='#1E293B', zorder=3)
        ax.text(6.8, y_curr + 0.4, f"{r['Prodi_Label']} ({r['Fak_Abbr']})", fontsize=8.6, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(32.5, y_curr + 0.4, f"{r['Keketatan']:.2f}x", fontsize=8.5, color='#1E293B', ha='right', zorder=3)
        ax.text(40.0, y_curr + 0.4, f"{r['FillRate']:.1f}%", fontsize=8.6, fontweight='bold', color='#1D4ED8', ha='right', zorder=3)
        ax.text(47.0, y_curr + 0.4, f"{int(r['DT'])} kursi", fontsize=8.5, color='#475569', ha='right', zorder=3)

    # Box Insight Eksekutif Q2
    box_q2_y = 52.0
    ax.add_patch(patches.FancyBboxPatch((4.2, box_q2_y), 43.0, 15.2, boxstyle="round,pad=0.2,rounding_size=0.8",
                                        facecolor='#FFFFFF', edgecolor='#93C5FD', lw=1.0, zorder=2))
    ax.text(5.4, box_q2_y + 13.0, "RINGKASAN STRATEGIS KUADRAN II:", fontsize=9.0, fontweight='bold', color='#1E40AF', zorder=3)
    insight_q2_lines = [
        "• Karakteristik: Peminat moderat (< 4,0x), namun serapan daya tampung selalu penuh (>= 80%).",
        "• Total Kapasitas Kuota: 527 kursi | Mahasiswa Daftar Ulang: 460 orang (Serapan Rata-rata 87,4%).",
        "• Dominasi Fakultas: FKIP (2 prodi) dan FISIP (2 prodi) melayani ceruk peminat loyal (niche).",
        "• REKOMENDASI MENTOR UNTUK WR DI DEPAN DEKAN:",
        "  \"Jangan tergiur menaikkan kuota 4 prodi ini. Daya serap pasarnya berada di titik equilibrium.",
        "   Menaikkan kuota akan menyeret keketatan jatuh ke bawah 1,5x dan merusak status akreditasi.\""
    ]
    for i, line in enumerate(insight_q2_lines):
        col = '#1E3A8A' if 'REKOMENDASI' in line or 'Jangan' in line else '#334155'
        weight = 'bold' if 'REKOMENDASI' in line else 'normal'
        ax.text(5.4, box_q2_y + 10.8 - (i * 2.0), line, fontsize=7.8, color=col, fontweight=weight, zorder=3)

    # -------------------------------------------------------------------------
    # 2. TOP-RIGHT: KUADRAN I - UNGGULAN (28 Prodi | 42,4%)
    # -------------------------------------------------------------------------
    content_top_y1 = draw_card(
        x0=51.5, y0=50.5, width=45.5, height=41.0,
        bg_col='#F0FDF4', border_col='#A7F3D0', header_col='#047857',
        title_text="KUADRAN I: UNGGULAN",
        count_text="28 Program Studi (42,4%)",
        policy_text="Pertahankan Mutu & Buka Kelas Internasional"
    )

    # Q1 dibagi menjadi 2 Sub-kolom (masing-masing 14 prodi)
    subcol_w = 21.6
    subcol1_x = 52.4
    subcol2_x = 74.8

    # Header Sub-kolom 1
    ax.text(subcol1_x, content_top_y1 - 0.4, "# PRODI (FAK)", fontsize=7.6, fontweight='bold', color='#065F46')
    ax.text(subcol1_x + 16.3, content_top_y1 - 0.4, "KEK", fontsize=7.6, fontweight='bold', color='#065F46', ha='right')
    ax.text(subcol1_x + subcol_w - 0.3, content_top_y1 - 0.4, "FILL", fontsize=7.6, fontweight='bold', color='#065F46', ha='right')
    ax.plot([subcol1_x, subcol1_x + subcol_w], [content_top_y1 - 0.9, content_top_y1 - 0.9], color='#A7F3D0', lw=0.7)

    # Header Sub-kolom 2
    ax.text(subcol2_x, content_top_y1 - 0.4, "# PRODI (FAK)", fontsize=7.6, fontweight='bold', color='#065F46')
    ax.text(subcol2_x + 16.3, content_top_y1 - 0.4, "KEK", fontsize=7.6, fontweight='bold', color='#065F46', ha='right')
    ax.text(subcol2_x + subcol_w - 0.3, content_top_y1 - 0.4, "FILL", fontsize=7.6, fontweight='bold', color='#065F46', ha='right')
    ax.plot([subcol2_x, subcol2_x + subcol_w], [content_top_y1 - 0.9, content_top_y1 - 0.9], color='#A7F3D0', lw=0.7)

    row_h_q1 = 2.1
    # Render 14 prodi di Sub-kolom 1
    for i in range(14):
        r = df_q1.iloc[i]
        ry = content_top_y1 - 2.8 - (i * row_h_q1)
        bg = '#DCFCE7' if i % 2 == 0 else '#F0FDF4'
        ax.add_patch(patches.Rectangle((subcol1_x - 0.2, ry - 0.5), subcol_w + 0.4, row_h_q1, facecolor=bg, edgecolor='none', zorder=2))
        ax.text(subcol1_x, ry + 0.4, f"{i+1:02d}. {r['Prodi_Label']} ({r['Fak_Abbr']})", fontsize=7.6, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(subcol1_x + 16.3, ry + 0.4, f"{r['Keketatan']:.1f}x", fontsize=7.5, color='#334155', ha='right', zorder=3)
        ax.text(subcol1_x + subcol_w - 0.3, ry + 0.4, f"{r['FillRate']:.1f}%", fontsize=7.6, fontweight='bold', color='#047857', ha='right', zorder=3)

    # Render 14 prodi di Sub-kolom 2
    for i in range(14, 28):
        r = df_q1.iloc[i]
        idx_sub = i - 14
        ry = content_top_y1 - 2.8 - (idx_sub * row_h_q1)
        bg = '#DCFCE7' if idx_sub % 2 == 0 else '#F0FDF4'
        ax.add_patch(patches.Rectangle((subcol2_x - 0.2, ry - 0.5), subcol_w + 0.4, row_h_q1, facecolor=bg, edgecolor='none', zorder=2))
        ax.text(subcol2_x, ry + 0.4, f"{i+1:02d}. {r['Prodi_Label']} ({r['Fak_Abbr']})", fontsize=7.6, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(subcol2_x + 16.3, ry + 0.4, f"{r['Keketatan']:.1f}x", fontsize=7.5, color='#334155', ha='right', zorder=3)
        ax.text(subcol2_x + subcol_w - 0.3, ry + 0.4, f"{r['FillRate']:.1f}%", fontsize=7.6, fontweight='bold', color='#047857', ha='right', zorder=3)

    # Strip ringkasan bawah Q1
    ax.add_patch(patches.Rectangle((52.4, 51.2), 43.8, 1.8, facecolor='#ECFDF5', edgecolor='#A7F3D0', lw=0.8, zorder=2))
    ax.text(74.3, 52.1, "Total 28 Prodi • Rata-rata Keketatan: 10,8x • Keterisian: 90,5% • Kuota Terbuka: 4.542 kursi/thn",
            fontsize=7.8, fontweight='bold', color='#065F46', ha='center', va='center', zorder=3)

    # -------------------------------------------------------------------------
    # 3. BOTTOM-LEFT: KUADRAN IV - PERLU REVITALISASI (26 Prodi | 39,4%)
    # -------------------------------------------------------------------------
    content_top_y4 = draw_card(
        x0=3.0, y0=3.5, width=45.5, height=44.5,
        bg_col='#FFF1F2', border_col='#FECDD3', header_col='#B91C1C',
        title_text="KUADRAN IV: PERLU DITINGKATKAN",
        count_text="26 Program Studi (39,4%)",
        policy_text="WAJIB PANGKAS KUOTA (20%–40%) DI SPMB 2027"
    )

    # Q4 dibagi menjadi 2 Sub-kolom (masing-masing 13 prodi)
    subcol1_x4 = 3.9
    subcol2_x4 = 26.3

    # Header Sub-kolom 1
    ax.text(subcol1_x4, content_top_y4 - 0.4, "# PRODI (FAK)", fontsize=7.6, fontweight='bold', color='#991B1B')
    ax.text(subcol1_x4 + 16.3, content_top_y4 - 0.4, "KEK", fontsize=7.6, fontweight='bold', color='#991B1B', ha='right')
    ax.text(subcol1_x4 + subcol_w - 0.3, content_top_y4 - 0.4, "FILL", fontsize=7.6, fontweight='bold', color='#991B1B', ha='right')
    ax.plot([subcol1_x4, subcol1_x4 + subcol_w], [content_top_y4 - 0.9, content_top_y4 - 0.9], color='#FECDD3', lw=0.7)

    # Header Sub-kolom 2
    ax.text(subcol2_x4, content_top_y4 - 0.4, "# PRODI (FAK)", fontsize=7.6, fontweight='bold', color='#991B1B')
    ax.text(subcol2_x4 + 16.3, content_top_y4 - 0.4, "KEK", fontsize=7.6, fontweight='bold', color='#991B1B', ha='right')
    ax.text(subcol2_x4 + subcol_w - 0.3, content_top_y4 - 0.4, "FILL", fontsize=7.6, fontweight='bold', color='#991B1B', ha='right')
    ax.plot([subcol2_x4, subcol2_x4 + subcol_w], [content_top_y4 - 0.9, content_top_y4 - 0.9], color='#FECDD3', lw=0.7)

    row_h_q4 = 2.4
    # Render 13 prodi di Sub-kolom 1
    for i in range(13):
        r = df_q4.iloc[i]
        ry = content_top_y4 - 3.1 - (i * row_h_q4)
        bg = '#FFE4E6' if i % 2 == 0 else '#FFF1F2'
        ax.add_patch(patches.Rectangle((subcol1_x4 - 0.2, ry - 0.6), subcol_w + 0.4, row_h_q4, facecolor=bg, edgecolor='none', zorder=2))
        ax.text(subcol1_x4, ry + 0.4, f"{i+1:02d}. {r['Prodi_Label']} ({r['Fak_Abbr']})", fontsize=7.5, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(subcol1_x4 + 16.3, ry + 0.4, f"{r['Keketatan']:.1f}x", fontsize=7.4, color='#334155', ha='right', zorder=3)
        ax.text(subcol1_x4 + subcol_w - 0.3, ry + 0.4, f"{r['FillRate']:.1f}%", fontsize=7.5, fontweight='bold', color='#B91C1C', ha='right', zorder=3)

    # Render 13 prodi di Sub-kolom 2
    for i in range(13, 26):
        r = df_q4.iloc[i]
        idx_sub = i - 13
        ry = content_top_y4 - 3.1 - (idx_sub * row_h_q4)
        bg = '#FFE4E6' if idx_sub % 2 == 0 else '#FFF1F2'
        ax.add_patch(patches.Rectangle((subcol2_x4 - 0.2, ry - 0.6), subcol_w + 0.4, row_h_q4, facecolor=bg, edgecolor='none', zorder=2))
        ax.text(subcol2_x4, ry + 0.4, f"{i+1:02d}. {r['Prodi_Label']} ({r['Fak_Abbr']})", fontsize=7.5, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(subcol2_x4 + 16.3, ry + 0.4, f"{r['Keketatan']:.1f}x", fontsize=7.4, color='#334155', ha='right', zorder=3)
        ax.text(subcol2_x4 + subcol_w - 0.3, ry + 0.4, f"{r['FillRate']:.1f}%", fontsize=7.5, fontweight='bold', color='#B91C1C', ha='right', zorder=3)

    # Strip peringatan bawah Q4
    ax.add_patch(patches.Rectangle((3.8, 4.3), 44.0, 2.2, facecolor='#FEF2F2', edgecolor='#FCA5A5', lw=0.9, zorder=2))
    ax.text(25.8, 5.4, "Penyumbang 1.140 Bangku Kosong Semu • Arah Rektorat: Pangkas Kuota 20%–40% untuk Selamatkan Akreditasi",
            fontsize=7.8, fontweight='bold', color='#991B1B', ha='center', va='center', zorder=3)

    # -------------------------------------------------------------------------
    # 4. BOTTOM-RIGHT: KUADRAN III - BELUM OPTIMAL (8 Prodi | 12,1%)
    # -------------------------------------------------------------------------
    content_top_y3 = draw_card(
        x0=51.5, y0=3.5, width=45.5, height=44.5,
        bg_col='#FFFBEB', border_col='#FDE68A', header_col='#B45309',
        title_text="KUADRAN III: BELUM OPTIMAL",
        count_text="8 Program Studi (12,1%)",
        policy_text="Fasilitasi Cicilan IPI & Percepat Cadangan Mandiri",
        sublabel="(Peminat Tinggi, Keterisian Belum Optimal)"
    )

    # Table Header Q3
    y_curr3 = content_top_y3 - 0.4
    ax.text(52.7, y_curr3, "NO", fontsize=8.2, fontweight='bold', color='#78350F')
    ax.text(55.3, y_curr3, "PROGRAM STUDI (FAKULTAS)", fontsize=8.2, fontweight='bold', color='#78350F')
    ax.text(81.0, y_curr3, "KEKETATAN", fontsize=8.2, fontweight='bold', color='#78350F', ha='right')
    ax.text(88.5, y_curr3, "FILL RATE", fontsize=8.2, fontweight='bold', color='#78350F', ha='right')
    ax.text(95.5, y_curr3, "DEFISIT/THN", fontsize=8.2, fontweight='bold', color='#78350F', ha='right')
    y_curr3 -= 1.2
    ax.plot([52.5, 96.0], [y_curr3 + 0.4, y_curr3 + 0.4], color='#FDE68A', lw=0.7)

    # Render 8 Prodi Q3 dengan tinggi baris rapat agar tidak menabrak box diagnostik
    row_h_q3 = 1.95
    for idx, r in df_q3.iterrows():
        y_curr3 -= row_h_q3
        bg_row = '#FEF3C7' if idx % 2 == 0 else '#FFFBEB'
        ax.add_patch(patches.Rectangle((52.5, y_curr3 - 0.5), 43.5, row_h_q3, facecolor=bg_row, edgecolor='none', zorder=2))
        defisit_kursi = int(r['DT'] - r['DU'])
        ax.text(53.0, y_curr3 + 0.3, f"{idx+1}", fontsize=8.4, fontweight='bold', color='#1E293B', zorder=3)
        ax.text(55.3, y_curr3 + 0.3, f"{r['Prodi_Label']} ({r['Fak_Abbr']})", fontsize=8.4, fontweight='bold', color='#0F172A', zorder=3)
        ax.text(81.0, y_curr3 + 0.3, f"{r['Keketatan']:.2f}x", fontsize=8.4, color='#1E293B', ha='right', zorder=3)
        ax.text(88.5, y_curr3 + 0.3, f"{r['FillRate']:.1f}%", fontsize=8.4, fontweight='bold', color='#B45309', ha='right', zorder=3)
        ax.text(95.5, y_curr3 + 0.3, f"-{defisit_kursi} kursi", fontsize=8.4, fontweight='bold', color='#DC2626', ha='right', zorder=3)

    # Box Diagnostik Kunci Q3 (Ditempatkan di bagian bawah dengan ruang bebas di atasnya)
    box_q3_y = 4.3
    box_q3_h = 16.5
    ax.add_patch(patches.FancyBboxPatch((52.5, box_q3_y), 43.5, box_q3_h, boxstyle="round,pad=0.2,rounding_size=0.8",
                                        facecolor='#FFFFFF', edgecolor='#FCD34D', lw=1.0, zorder=2))
    ax.text(53.8, box_q3_y + 14.5, "DIAGNOSTIK AKAR MASALAH KUADRAN III (HILIR, BUKAN HULU):", fontsize=8.8, fontweight='bold', color='#B45309', zorder=3)
    insight_q3_lines = [
        "• Fenomena Unik: Peminat sangat tinggi (Akuntansi Perpajakan 14,2x, Teknik Perminyakan 6,7x).",
        "• Titik Kebocoran: Calon mahasiswa lulus seleksi namun TIDAK DAFTAR ULANG di jalur mandiri.",
        "• Penyebab Utama: Beban biaya IPI (Uang Pangkal) serta sistem pemanggilan cadangan terlambat.",
        "• PESAN STRATEGIS WR KEPADA DEKAN FT, FEB, FKIP, FP:",
        "  \"Fakultas TIDAK PERLU MEMANGKAS KUOTA prodi ini. Daya tarik prodi sangat kuat.",
        "   Solusi universitas: Buka fasilitas cicilan IPI dan percepat pemanggilan kuota cadangan!\""
    ]
    for i, line in enumerate(insight_q3_lines):
        col = '#92400E' if 'PESAN' in line or 'TIDAK PERLU' in line else '#334155'
        weight = 'bold' if 'PESAN' in line else 'normal'
        ax.text(53.8, box_q3_y + 12.2 - (i * 2.0), line, fontsize=7.8, color=col, fontweight=weight, zorder=3)

    # Simpan Gambar
    out_file = os.path.join(chart_dir, "13_companion_direktori_66_prodi_4_kuadran.png")
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, facecolor='#F8FAFC')
    plt.close()
    print(f"Successfully generated Slide 2 Companion chart at: {out_file}")

if __name__ == "__main__":
    main()
