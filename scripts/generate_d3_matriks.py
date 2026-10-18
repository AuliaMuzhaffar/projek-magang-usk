import os
import numpy as np
import sys, os
libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "libs"))
if os.path.exists(libs_dir) and libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

def generate_d3_matriks_chart():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    excel_path = os.path.join(repo_dir, "data", "master", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    chart_dir = os.path.join(repo_dir, "output", "grafik")
    os.makedirs(chart_dir, exist_ok=True)

    print("Loading D3 data from Excel...")
    df_d3 = pd.read_excel(excel_path, sheet_name="Diploma_3_Vokasi")

    # Map column names cleanly
    rev_map = {
        "Nama Program Studi": "Program_Studi",
        "Rata Fill Rate 5-Thn (%)": "Rata_FillRate_5Thn_Persen",
        "Rata Keketatan 5-Thn": "Rata_Keketatan_5Thn",
        "Rata DT 5-Thn": "Rata_DT_5Thn",
        "Rata DU 5-Thn": "Rata_DU_5Thn",
        "Rata Peminat 5-Thn": "Rata_Peminat_5Thn",
        "Fakultas": "Fakultas"
    }
    df_d3 = df_d3.rename(columns=rev_map)

    print("Generating 13_matriks_4_kuadran_5_tahun_d3_2022_2026.png...")
    fig_d3 = plt.figure(figsize=(24, 12), dpi=300, facecolor='#F8FAFC')
    gs_d3 = gridspec.GridSpec(1, 2, width_ratios=[1.45, 1.0], wspace=0.12)

    ax_d3 = fig_d3.add_subplot(gs_d3[0])
    ax_d3_cards = fig_d3.add_subplot(gs_d3[1])
    ax_d3_cards.axis('off')

    ax_d3.set_facecolor('#FFFFFF')

    x_max_d3 = 21.0
    y_min_d3, y_max_d3 = 18.0, 105.0

    # 4 Quadrants background
    ax_d3.axvspan(4.0, x_max_d3, ymin=(80.0 - y_min_d3)/(y_max_d3 - y_min_d3), ymax=1.0, color='#F0FDF4', alpha=0.55, zorder=0)
    ax_d3.axvspan(0.0, 4.0, ymin=(80.0 - y_min_d3)/(y_max_d3 - y_min_d3), ymax=1.0, color='#F0F9FF', alpha=0.55, zorder=0)
    ax_d3.axvspan(0.0, 4.0, ymin=0.0, ymax=(80.0 - y_min_d3)/(y_max_d3 - y_min_d3), color='#FFF1F2', alpha=0.55, zorder=0)
    ax_d3.axvspan(4.0, x_max_d3, ymin=0.0, ymax=(80.0 - y_min_d3)/(y_max_d3 - y_min_d3), color='#FFFBEB', alpha=0.65, zorder=0)

    # Threshold lines (Hanya 2 garis benchmark resmi seperti S1)
    line_slate = '#64748B'
    ax_d3.axvline(x=4.0, color=line_slate, linestyle='--', linewidth=1.8, alpha=0.85, zorder=1)
    ax_d3.axhline(y=80.0, color=line_slate, linestyle='--', linewidth=1.8, alpha=0.85, zorder=1)

    # Badges on threshold lines
    ax_d3.text(4.2, 20.0, '▲ Ambang Keketatan: 4,0 : 1', fontsize=8.8, color='#475569', fontweight='bold', zorder=2)
    ax_d3.text(x_max_d3 - 0.4, 80.8, 'Batas Minimal Keterisian Ideal (80%)', ha='right', fontsize=8.8, color='#475569', fontweight='bold', zorder=2)

    # Quadrant Titles (100% Konsisten dengan S1)
    ax_d3.text(x_max_d3 - 0.8, 102.5, 'KUADRAN I: UNGGULAN\n0 Program Studi (0,0%)',
               ha='right', va='top', fontsize=11.0, fontweight='bold', color='#047857', alpha=0.75, zorder=2, linespacing=1.2)
    ax_d3.text(0.5, 102.5, 'KUADRAN II: STABIL\n0 Program Studi (0,0%)',
               ha='left', va='top', fontsize=11.0, fontweight='bold', color='#1D4ED8', alpha=0.75, zorder=2, linespacing=1.2)
    ax_d3.text(0.5, 20.5, 'KUADRAN IV: PERLU DITINGKATKAN\n0 Program Studi (0,0%)',
               ha='left', va='bottom', fontsize=11.0, fontweight='bold', color='#B91C1C', alpha=0.75, zorder=2, linespacing=1.2)
    ax_d3.text(x_max_d3 - 0.8, 20.5, 'KUADRAN III: BELUM OPTIMAL\n(Peminat Tinggi, Keterisian Belum Optimal)\n11 Program Studi (100,0% Seluruh Vokasi)',
               ha='right', va='bottom', fontsize=11.5, fontweight='bold', color='#B45309', alpha=0.95, zorder=2, linespacing=1.2)


    # Scatter points - Ukuran seragam s=100 (sama seperti S1), selaras warna Kuadran III (#D97706)
    ax_d3.scatter(df_d3['Rata_Keketatan_5Thn'], df_d3['Rata_FillRate_5Thn_Persen'],
                  s=100, c='#D97706', edgecolors='#0F172A', linewidths=1.2, alpha=0.92, zorder=4)

    annots_config_d3 = [
        ('D3 Teknik Listrik (FT)\n5,3x | 48,3% | DT: 38', 'TEKNIK LISTRIK', (-18, 20), 'right'),
        ('D3 Budidaya Peternakan (FP)\n5,7x | 30,6% | DT: 50', 'BUDIDAYA PETERNAKAN', (18, 16), 'left'),
        ('D3 Manajemen Agribisnis (FP)\n6,2x | 27,4% | DT: 95', 'MANAJEMEN AGRIBISNIS', (18, -18), 'left'),
        ('D3 Sekretari (FEB)\n7,3x | 46,0% | DT: 45', 'SEKRETARI', (-18, -20), 'right'),
        ('D3 Teknik Mesin (FT)\n7,5x | 50,6% | DT: 38', 'TEKNIK MESIN', (-18, 22), 'right'),
        ('D3 Teknik Sipil (FT)\n8,1x | 40,6% | DT: 70', 'TEKNIK SIPIL', (18, -18), 'left'),
        ('D3 Akuntansi (FEB)\n9,6x | 52,0% | DT: 72', 'AKUNTANSI', (16, 26), 'left'),
        ('D3 Keuangan & Perbankan (FEB)\n11,2x | 34,0% | DT: 69', 'KEUANGAN DAN PERBANKAN', (18, -16), 'left'),
        ('D3 Kesehatan Hewan (FKH)\n12,2x | 49,4% | DT: 42', 'KESEHATAN HEWAN', (18, 20), 'left'),
        ('D3 Manajemen Informatika (FMIPA)\n13,7x | 66,6% | DT: 80 ★ Keterisian Tertinggi', 'MANAJEMEN INFORMATIKA', (18, 16), 'left'),
        ('D3 Manajemen Perusahaan (FEB)\n17,7x | 42,6% | DT: 42', 'MANAJEMEN PERUSAHAAN', (-18, 18), 'right')
    ]

    for label, pat, (ox, oy), ha_align in annots_config_d3:
        m = df_d3[df_d3['Program_Studi'].str.contains(pat, regex=True, na=False)]
        if len(m) > 0:
            px = float(m.iloc[0]['Rata_Keketatan_5Thn'])
            py = float(m.iloc[0]['Rata_FillRate_5Thn_Persen'])
            ax_d3.annotate(label, xy=(px, py), xytext=(ox, oy), textcoords='offset points',
                           ha=ha_align, va='center', fontsize=8.3, fontweight='bold', color='#92400E',
                           bbox=dict(boxstyle='round,pad=0.30', facecolor='#FFFBEB', edgecolor='#F59E0B', linewidth=0.9, alpha=0.96),
                           arrowprops=dict(arrowstyle='->', color='#475569', lw=1.0, shrinkA=2, shrinkB=4),
                           zorder=5)

    ax_d3.set_xlim(0, x_max_d3)
    ax_d3.set_ylim(y_min_d3, y_max_d3)
    ax_d3.set_xlabel('Rasio Keketatan Seleksi (Peminat per 1 Kursi Daya Tampung)', fontsize=11, fontweight='bold', color='#1E293B', labelpad=10)
    ax_d3.set_ylabel('Persentase Keterisian Kuota / Fill Rate (%)', fontsize=11, fontweight='bold', color='#1E293B', labelpad=14)
    ax_d3.set_title('Peta Portofolio 11 Program Studi Diploma 3 Vokasi USK (Rata-rata Historis 2022–2026)', fontsize=12, fontweight='bold', pad=12, color='#0F172A')

    ax_d3.grid(True, linestyle=':', alpha=0.45, color='#94A3B8', zorder=0)
    for spine in ['top', 'right']:
        ax_d3.spines[spine].set_visible(False)
    ax_d3.spines['left'].set_color('#94A3B8')
    ax_d3.spines['bottom'].set_color('#94A3B8')

    # =========================================================================
    # RIGHT PANEL: DIREKTORI ROSTER KUADRAN III & KESIMPULAN STRATEGIS
    # =========================================================================
    rect_summary_d3 = FancyBboxPatch((0.02, 0.885), 0.96, 0.105, boxstyle='round,pad=0.02',
                                     facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2,
                                     transform=ax_d3_cards.transAxes, zorder=2)
    ax_d3_cards.add_patch(rect_summary_d3)
    ax_d3_cards.text(0.05, 0.962, 'RINGKASAN PORTOFOLIO DIPLOMA 3 VOKASI USK (HISTORIS)', fontsize=9.8, fontweight='bold', color='#0F172A', transform=ax_d3_cards.transAxes)

    kpi_items_d3 = [
        ('11 Prodi', '100% Kuadran III', 0.05),
        ('9,5 : 1', 'Rata-rata Keketatan', 0.38),
        ('44,4%', 'Rata-rata Keterisian', 0.70)
    ]
    for val, lbl, x_pos in kpi_items_d3:
        color_kpi = '#B45309' if '%' in val else '#1E40AF'
        ax_d3_cards.text(x_pos, 0.925, val, fontsize=12.5, fontweight='bold', color=color_kpi, transform=ax_d3_cards.transAxes)
        ax_d3_cards.text(x_pos, 0.898, lbl, fontsize=8.0, color='#64748B', transform=ax_d3_cards.transAxes)

    # 2. Tabel Roster Direktori Kuadran III
    rect_table_box = FancyBboxPatch((0.02, 0.285), 0.96, 0.585, boxstyle='round,pad=0.02',
                                    facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2,
                                    transform=ax_d3_cards.transAxes, zorder=2)
    ax_d3_cards.add_patch(rect_table_box)

    ax_d3_cards.text(0.05, 0.845, 'DIREKTORI ROSTER 11 PROGRAM STUDI (KUADRAN III)', fontsize=9.8, fontweight='bold', color='#B45309', transform=ax_d3_cards.transAxes)

    # Table Header
    y_th = 0.805
    ax_d3_cards.text(0.05, y_th, 'No', fontsize=8.0, fontweight='bold', color='#475569', transform=ax_d3_cards.transAxes)
    ax_d3_cards.text(0.10, y_th, 'Program Studi & Fakultas', fontsize=8.0, fontweight='bold', color='#475569', transform=ax_d3_cards.transAxes)
    ax_d3_cards.text(0.55, y_th, 'Keketatan', fontsize=8.0, fontweight='bold', color='#475569', transform=ax_d3_cards.transAxes, ha='center')
    ax_d3_cards.text(0.68, y_th, 'DT / DU', fontsize=8.0, fontweight='bold', color='#475569', transform=ax_d3_cards.transAxes, ha='center')
    ax_d3_cards.text(0.81, y_th, 'Fill Rate', fontsize=8.0, fontweight='bold', color='#475569', transform=ax_d3_cards.transAxes, ha='center')
    ax_d3_cards.text(0.93, y_th, 'Sisa', fontsize=8.0, fontweight='bold', color='#475569', transform=ax_d3_cards.transAxes, ha='center')

    # Line under header
    line_h = FancyBboxPatch((0.04, y_th - 0.012), 0.92, 0.003, boxstyle='square,pad=0',
                            facecolor='#E2E8F0', edgecolor='none', transform=ax_d3_cards.transAxes, zorder=3)
    ax_d3_cards.add_patch(line_h)

    # Sorted data
    fak_abbr_d3 = {'FMIPA': 'FMIPA', 'Ekonomi dan Bisnis': 'FEB', 'Teknik': 'FT', 'Pertanian': 'FP', 'Kedokteran Hewan': 'FKH'}
    d3_sorted = df_d3.sort_values('Rata_FillRate_5Thn_Persen', ascending=False).reset_index(drop=True)

    y_row = y_th - 0.045
    for idx, r in d3_sorted.iterrows():
        p_name = r['Program_Studi'].replace('DIPLOMA III ', '').replace('DIPLOMA 3 ', '').strip().title()
        f_abbr = fak_abbr_d3.get(r['Fakultas'], r['Fakultas'])
        full_name = f'{p_name} ({f_abbr})'
        kek_val = f"{r['Rata_Keketatan_5Thn']:.1f}x"
        dt_val = int(round(r['Rata_DT_5Thn']))
        du_val = int(round(r['Rata_DU_5Thn']))
        ratio_txt = f'{dt_val}/{du_val}'
        fr_val = f"{r['Rata_FillRate_5Thn_Persen']:.1f}%"
        sisa_val = int(round(r['Rata_DT_5Thn'] - r['Rata_DU_5Thn']))
        
        # Zebra striping
        if idx % 2 == 1:
            bg_row = FancyBboxPatch((0.04, y_row - 0.008), 0.92, 0.038, boxstyle='square,pad=0',
                                    facecolor='#F8FAFC', edgecolor='none', transform=ax_d3_cards.transAxes, zorder=2)
            ax_d3_cards.add_patch(bg_row)
            
        ax_d3_cards.text(0.05, y_row, f'{idx+1}.', fontsize=7.8, color='#64748B', transform=ax_d3_cards.transAxes)
        ax_d3_cards.text(0.10, y_row, full_name, fontsize=7.8, fontweight='bold', color='#1E293B', transform=ax_d3_cards.transAxes)
        ax_d3_cards.text(0.55, y_row, kek_val, fontsize=7.8, color='#0F172A', transform=ax_d3_cards.transAxes, ha='center')
        ax_d3_cards.text(0.68, y_row, ratio_txt, fontsize=7.8, color='#475569', transform=ax_d3_cards.transAxes, ha='center')
        
        # Color coding for FR
        fr_col = '#047857' if r['Rata_FillRate_5Thn_Persen'] >= 60.0 else '#B45309' if r['Rata_FillRate_5Thn_Persen'] >= 45.0 else '#DC2626'
        ax_d3_cards.text(0.81, y_row, fr_val, fontsize=7.8, fontweight='bold', color=fr_col, transform=ax_d3_cards.transAxes, ha='center')
        ax_d3_cards.text(0.93, y_row, f'{sisa_val}', fontsize=7.8, color='#DC2626' if sisa_val >= 25 else '#475569', transform=ax_d3_cards.transAxes, ha='center')
        
        y_row -= 0.040

    # 3. Strategic Action Plan Card for Leadership
    rect_action = FancyBboxPatch((0.02, 0.025), 0.96, 0.245, boxstyle='round,pad=0.02',
                                 facecolor='#FFFBEB', edgecolor='#F59E0B', linewidth=1.2,
                                 transform=ax_d3_cards.transAxes, zorder=2)
    ax_d3_cards.add_patch(rect_action)

    ax_d3_cards.text(0.05, 0.235, 'REKOMENDASI STRATEGIS KUADRAN III BAGI PIMPINAN:', fontsize=9.2, fontweight='bold', color='#92400E', transform=ax_d3_cards.transAxes)
    ax_d3_cards.text(0.05, 0.185, '• Diagnosis Masalah:\n  Animo peminat sangat tinggi (5,3x–17,7x), namun terjadi kebocoran masif saat pendaftaran\n  ulang (rata-rata keterisian hanya 44,4%) karena dijadikan prodi cadangan seleksi nasional.',
                     fontsize=7.8, color='#78350F', transform=ax_d3_cards.transAxes, linespacing=1.25)
    ax_d3_cards.text(0.05, 0.095, '• Langkah Kebijakan:\n  1. Upgrade ke D4: Konversi D3 Manajemen Informatika (FR 66,6%) & rumpun Teknik ke Sarjana Terapan.\n  2. Rasionalisasi Kuota: Pangkas kuota pada prodi defisit tinggi (Agribisnis, Perbankan, Peternakan).\n  3. Afirmasi Industri: Wajibkan kemitraan magang industri langsung untuk mengikat komitmen mahasiswa.',
                     fontsize=7.8, color='#78350F', fontweight='bold', transform=ax_d3_cards.transAxes, linespacing=1.25)

    fig_d3.suptitle('MATRIKS 4 KUADRAN: PORTOFOLIO 11 PROGRAM STUDI DIPLOMA 3 VOKASI USK', fontsize=15, fontweight='bold', y=0.980, color='#0F172A')
    fig_d3.subplots_adjust(left=0.075, right=0.985, top=0.915, bottom=0.075, wspace=0.12)

    out_file1 = os.path.join(chart_dir, "13_matriks_4_kuadran_5_tahun_d3_2022_2026.png")
    out_file2 = os.path.join(chart_dir, "13b_matriks_4_kuadran_d3_vokasi_2022_2026.png")
    plt.savefig(out_file1, dpi=300)
    plt.savefig(out_file2, dpi=300)
    plt.close(fig_d3)
    print(f"Successfully generated clean D3 chart at:\n- {out_file1}\n- {out_file2}")

if __name__ == "__main__":
    generate_d3_matriks_chart()
