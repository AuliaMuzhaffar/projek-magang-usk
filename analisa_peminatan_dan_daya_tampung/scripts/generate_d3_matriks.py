import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D

def generate_d3_matriks_chart():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    excel_path = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "data", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    chart_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "grafik")
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

    fig = plt.figure(figsize=(24, 12), dpi=300, facecolor='#F8FAFC')
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.68, 1.0], wspace=0.14)

    ax = fig.add_subplot(gs[0])
    ax_cards = fig.add_subplot(gs[1])
    ax_cards.axis('off')

    ax.set_facecolor('#FFFFFF')

    x_max = 21.0
    y_min, y_max = 18.0, 105.0

    # Gentle Pastel Quadrant Backgrounds
    ax.axvspan(4.0, x_max, ymin=(80.0 - y_min)/(y_max - y_min), ymax=1.0, color='#F0FDF4', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=(80.0 - y_min)/(y_max - y_min), ymax=1.0, color='#F0F9FF', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=0.0, ymax=(80.0 - y_min)/(y_max - y_min), color='#FFF1F2', alpha=0.55, zorder=0)
    ax.axvspan(4.0, x_max, ymin=0.0, ymax=(80.0 - y_min)/(y_max - y_min), color='#FFFBEB', alpha=0.65, zorder=0)

    # Subtle Threshold lines
    ax.axvline(x=4.0, color='#64748B', linestyle='--', linewidth=1.6, alpha=0.85, zorder=1)
    ax.axhline(y=80.0, color='#64748B', linestyle='--', linewidth=1.6, alpha=0.85, zorder=1)
    # Secondary reference line for critical viability
    ax.axhline(y=50.0, color='#DC2626', linestyle=':', linewidth=1.3, alpha=0.70, zorder=1)

    # Badges on threshold lines
    ax.text(4.2, 19.5, 'Ambang Keketatan (4,0 : 1)', fontsize=8.5, color='#475569', fontweight='bold', zorder=2)
    ax.text(x_max - 0.4, 80.8, 'Standar Keterisian Kuota Sehat (80%)', ha='right', fontsize=8.5, color='#475569', fontweight='bold', zorder=2)
    ax.text(x_max - 0.4, 50.8, 'Batas Kritis Kelayakan Operasional (50%)', ha='right', fontsize=8.2, color='#DC2626', fontweight='bold', zorder=2)

    # Subtle Quadrant Titles inside plot
    ax.text(x_max - 0.8, 102.5, 'KUADRAN I: UNGGULAN\n0 Program Studi (0,0%)',
            ha='right', va='top', fontsize=10.5, fontweight='bold', color='#047857', alpha=0.75, zorder=2, linespacing=1.2)
    ax.text(0.5, 102.5, 'KUADRAN II: STABIL \n0 Program Studi (0,0%)',
            ha='left', va='top', fontsize=10.5, fontweight='bold', color='#1D4ED8', alpha=0.75, zorder=2, linespacing=1.2)
    ax.text(0.5, 20.5, 'KUADRAN III: KURANG DIMINATI\n0 Program Studi (0,0%)',
            ha='left', va='bottom', fontsize=10.5, fontweight='bold', color='#B91C1C', alpha=0.75, zorder=2, linespacing=1.2)
    ax.text(x_max - 0.8, 20.5, 'KUADRAN IV: SELEKTIF TAPI BOCOR \n11 Program Studi (100,0% Seluruh Vokasi Terjebak di Sini)',
            ha='right', va='bottom', fontsize=11.0, fontweight='bold', color='#B45309', alpha=0.95, zorder=2, linespacing=1.2)

    # Callout banner for Kuadran IV anomaly in upper area
    ax.text(12.5, 93.5, 'TEMUAN ANOMALI STRUKTURAL VOKASI USK:\n100% (11 Program Studi D3) Terkonsentrasi di Kuadran IV\nPeminat Membludak (Keketatan 5,3x–17,7x), Namun Keterisian Anjlok (<80%)',
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#92400E',
            bbox=dict(boxstyle='round,pad=0.55', facecolor='#FFFBEB', edgecolor='#F59E0B', linewidth=1.2, alpha=0.96),
            zorder=3)

    # Scatter points - all in Kuadran IV (Color-coded by viability tier)
    pt_cols = []
    for _, r in df_d3.iterrows():
        y = r['Rata_FillRate_5Thn_Persen']
        if y >= 60.0:
            pt_cols.append('#059669') # Emerald for standout (Manajemen Informatika)
        elif y >= 45.0:
            pt_cols.append('#D97706') # Amber for Moderate / Vulnerable
        else:
            pt_cols.append('#DC2626') # Crimson for Acute Deficit (<45%)

    sizes_d3 = 90 + (df_d3['Rata_DT_5Thn'] / 100.0) * 320
    scatter = ax.scatter(df_d3['Rata_Keketatan_5Thn'], df_d3['Rata_FillRate_5Thn_Persen'],
                         s=sizes_d3, c=pt_cols, edgecolors='#0F172A', linewidths=1.2, alpha=0.92, zorder=4)

    # Clean, non-overlapping annotations for all 11 D3 programs
    annots_config_d3 = [
        ('D3 Teknik Listrik (FT)\n5,3x | 48,3% | DT: 38', 'TEKNIK LISTRIK', (-18, 20), 'right'),
        ('D3 Budidaya Peternakan (FP)\n5,6x | 30,6% | DT: 50', 'BUDIDAYA PETERNAKAN', (18, 16), 'left'),
        ('D3 Manajemen Agribisnis (FP)\n6,2x | 27,4% | DT: 95', 'MANAJEMEN AGRIBISNIS', (18, -18), 'left'),
        ('D3 Sekretari (FEB)\n7,3x | 46,0% | DT: 45', 'SEKRETARI', (-18, -20), 'right'),
        ('D3 Teknik Mesin (FT)\n7,5x | 50,6% | DT: 38', 'TEKNIK MESIN', (-18, 22), 'right'),
        ('D3 Teknik Sipil (FT)\n8,1x | 40,6% | DT: 70', 'TEKNIK SIPIL', (18, -18), 'left'),
        ('D3 Akuntansi (FEB)\n9,6x | 52,0% | DT: 73', 'AKUNTANSI', (16, 26), 'left'),
        ('D3 Keuangan & Perbankan (FEB)\n11,2x | 34,0% | DT: 69', 'KEUANGAN DAN PERBANKAN', (18, -16), 'left'),
        ('D3 Kesehatan Hewan (FKH)\n12,2x | 49,4% | DT: 43', 'KESEHATAN HEWAN', (18, 20), 'left'),
        ('D3 Manajemen Informatika (FMIPA)\n13,7x | 66,6% | DT: 80 ★ Bintang Vokasi', 'MANAJEMEN INFORMATIKA', (18, 16), 'left'),
        ('D3 Manajemen Perusahaan (FEB)\n17,7x | 42,6% | DT: 43', 'MANAJEMEN PERUSAHAAN', (-18, 18), 'right')
    ]

    for label, pat, (ox, oy), ha_align in annots_config_d3:
        m = df_d3[df_d3['Program_Studi'].str.contains(pat, regex=True, na=False)]
        if len(m) > 0:
            px = float(m.iloc[0]['Rata_Keketatan_5Thn'])
            py = float(m.iloc[0]['Rata_FillRate_5Thn_Persen'])
            badge_bg = '#F0FDF4' if py >= 60.0 else '#FEF2F2' if py < 45.0 else '#FFFBEB'
            badge_edge = '#10B981' if py >= 60.0 else '#EF4444' if py < 45.0 else '#F59E0B'
            badge_txt_c = '#065F46' if py >= 60.0 else '#991B1B' if py < 45.0 else '#92400E'

            ax.annotate(label, xy=(px, py), xytext=(ox, oy), textcoords='offset points',
                        ha=ha_align, va='center', fontsize=8.3, fontweight='bold', color=badge_txt_c,
                        bbox=dict(boxstyle='round,pad=0.30', facecolor=badge_bg, edgecolor=badge_edge, linewidth=0.9, alpha=0.96),
                        arrowprops=dict(arrowstyle='->', color='#475569', lw=1.0, shrinkA=2, shrinkB=4),
                        zorder=5)

    ax.set_xlim(0, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Rasio Keketatan Seleksi (Peminat per 1 Kursi Daya Tampung)', fontsize=11, fontweight='bold', color='#1E293B', labelpad=10)
    ax.set_ylabel('Persentase Keterisian Kuota / Fill Rate (%)', fontsize=11, fontweight='bold', color='#1E293B', labelpad=14)
    ax.set_title('Peta Portofolio 11 Program Studi Diploma 3 Vokasi USK (Rata-rata Historis 2022–2026)', fontsize=12, fontweight='bold', pad=12, color='#0F172A')

    ax.grid(True, linestyle=':', alpha=0.45, color='#94A3B8', zorder=0)
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')

    # Size legend inside Kuadran II (which has plenty of room)
    leg_dt = [40, 70, 100]
    leg_sizes = [90 + (dt / 100.0) * 320 for dt in leg_dt]
    leg_handles = [Line2D([0], [0], marker='o', color='w', label=f'{dt} kursi',
                          markerfacecolor='#94A3B8', markersize=np.sqrt(s), markeredgecolor='#0F172A')
                   for dt, s in zip(leg_dt, leg_sizes)]
    leg = ax.legend(handles=leg_handles, loc='upper left', bbox_to_anchor=(0.02, 0.90),
                    title='Kapasitas Kuota (Daya Tampung)', frameon=True, fontsize=8.5, title_fontsize=9.0)
    leg.get_frame().set_facecolor('#FFFFFF')
    leg.get_frame().set_edgecolor('#CBD5E1')
    leg.get_frame().set_alpha(0.95)

    # -----------------
    # RIGHT PANEL: EXECUTIVE CARDS
    # -----------------
    rect_summary = FancyBboxPatch((0.02, 0.875), 0.96, 0.115, boxstyle='round,pad=0.02',
                                  facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=1.2,
                                  transform=ax_cards.transAxes, zorder=2)
    ax_cards.add_patch(rect_summary)

    ax_cards.text(0.06, 0.965, 'RINGKASAN PORTOFOLIO DIPLOMA 3 VOKASI USK (HISTORIS)', fontsize=10, fontweight='bold', color='#0F172A', transform=ax_cards.transAxes)

    kpi_items = [
        ('11 Prodi', '100% Kuadran IV', 0.06),
        ('9,5 : 1', 'Rata-rata Keketatan', 0.40),
        ('44,4%', 'Rata-rata Keterisian', 0.72)
    ]
    for val, lbl, x_pos in kpi_items:
        color_kpi = '#B45309' if '%' in val else '#1E40AF'
        ax_cards.text(x_pos, 0.925, val, fontsize=13, fontweight='bold', color=color_kpi, transform=ax_cards.transAxes)
        ax_cards.text(x_pos, 0.895, lbl, fontsize=8.0, color='#64748B', transform=ax_cards.transAxes)

    cards_d3 = [
        {
            'title': 'ANOMALI: 100% PRODI TERJEBAK DI KUADRAN IV',
            'badge': '11 Prodi (100%)',
            'badge_c': '#B45309', 'bg': '#FFFBEB', 'border': '#F59E0B', 'title_c': '#92400E',
            'kondisi': 'Peminat tinggi (≥ 4,0x) tapi keterisian selalu rontok (< 80%).',
            'contoh': 'Keketatan 5,3x s.d. 17,7x namun rata-rata keterisian hanya 44,4%.',
            'rekomendasi': 'Ilusi Keketatan Semu: Dijadikan pilihan cadangan lalu gugur massal.'
        },
        {
            'title': 'TIER 1: SATU-SATUNYA BINTANG VOKASI (FR ≥ 60%)',
            'badge': '1 Prodi (9,1%)',
            'badge_c': '#047857', 'bg': '#F0FDF4', 'border': '#10B981', 'title_c': '#065F46',
            'kondisi': 'D3 Manajemen Informatika (FMIPA): FR 66,6% (2026: 72,5%, 2025: 82,5%).',
            'contoh': 'Peminat tertinggi vokasi (1.100 mhs/thn) dengan keketatan 13,7 : 1.',
            'rekomendasi': 'Prioritas #1 konversi menjadi Sarjana Terapan (D4 Rekayasa TI).'
        },
        {
            'title': 'TIER 2: RENTAN KONVERSI (FR 45%–55%)',
            'badge': '5 Prodi (45,5%)',
            'badge_c': '#D97706', 'bg': '#FEF3C7', 'border': '#F59E0B', 'title_c': '#78350F',
            'kondisi': 'Akuntansi (52%), Mesin (51%), Keswan (49%), Listrik (48%), Sekretari (46%).',
            'contoh': 'Peminat besar (200–760 orang) namun konversi daftar ulang macet.',
            'rekomendasi': 'Konversi prodi teknik/akuntansi ke D4; perkuat jalur magang industri.'
        },
        {
            'title': 'TIER 3: KRISIS DEFISIT AKUT (FR < 45%)',
            'badge': '5 Prodi (45,5%)',
            'badge_c': '#B91C1C', 'bg': '#FFF1F2', 'border': '#F43F5E', 'title_c': '#991B1B',
            'kondisi': 'Manajemen Perush (43%), Sipil (41%), Perbankan (34%), Peternakan (31%), Agribisnis (27%).',
            'contoh': 'Episentrum bangku kosong: D3 Agribisnis & Perbankan rugi >150 kursi.',
            'rekomendasi': 'Rasionalisasi kuota drastis (pangkas 40%–50%) atau moratorium.'
        }
    ]

    y_starts = [0.655, 0.440, 0.225, 0.010]
    box_h = 0.200

    for idx, c in enumerate(cards_d3):
        y = y_starts[idx]
        rect = FancyBboxPatch((0.02, y), 0.96, box_h, boxstyle='round,pad=0.02',
                              facecolor=c['bg'], edgecolor=c['border'], linewidth=1.2,
                              transform=ax_cards.transAxes, zorder=2)
        ax_cards.add_patch(rect)

        ax_cards.text(0.06, y + box_h - 0.038, c['title'], fontsize=10, fontweight='bold', color=c['title_c'], transform=ax_cards.transAxes)
        ax_cards.text(0.94, y + box_h - 0.038, c['badge'], fontsize=9, fontweight='bold', color=c['badge_c'], ha='right', transform=ax_cards.transAxes)
        ax_cards.text(0.06, y + box_h - 0.078, f"Karakter: {c['kondisi']}", fontsize=8.3, color='#334155', transform=ax_cards.transAxes)
        ax_cards.text(0.06, y + box_h - 0.120, f"Detail: {c['contoh']}", fontsize=8.0, fontstyle='italic', color='#64748B', transform=ax_cards.transAxes)
        ax_cards.text(0.06, y + 0.025, f"Rekomendasi: {c['rekomendasi']}", fontsize=8.4, fontweight='bold', color=c['title_c'], transform=ax_cards.transAxes)

    # Main Title at Top
    fig.suptitle('MATRIKS 4 KUADRAN: PORTOFOLIO 11 PROGRAM STUDI DIPLOMA 3 VOKASI USK', fontsize=15, fontweight='bold', y=0.980, color='#0F172A')

    fig.subplots_adjust(left=0.075, right=0.985, top=0.915, bottom=0.075, wspace=0.14)

    # Save to both standard names
    out_file1 = os.path.join(chart_dir, "13_matriks_4_kuadran_5_tahun_d3_2022_2026.png")
    out_file2 = os.path.join(chart_dir, "13b_matriks_4_kuadran_d3_vokasi_2022_2026.png")
    plt.savefig(out_file1, dpi=300)
    plt.savefig(out_file2, dpi=300)
    plt.close()
    print(f"Successfully generated:\n- {out_file1}\n- {out_file2}")

if __name__ == "__main__":
    generate_d3_matriks_chart()
