#!/usr/bin/env python3
"""
5 Visualisasi Tambahan (Executive Gap Analysis) — Analisis Peminatan & Daya Tampung USK (2022–2026)
Standar: Widescreen 16:9, Tipografi Tajam, Bebas Tumpang Tindih, Siap Dipresentasikan ke Rektorat/Dekan.
"""

import os
from collections import Counter
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import FancyBboxPatch, Patch
from matplotlib.lines import Line2D

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

def main():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    excel1 = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "data",
                          "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    excel2 = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "data",
                          "analisa_jalur_masuk_dan_kebocoran_per_prodi_2022_2026.xlsx")
    chart_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "grafik")
    os.makedirs(chart_dir, exist_ok=True)

    print("Memuat data Excel...")
    df_s1 = pd.read_excel(excel1, sheet_name="S1_Kampus_Utama")

    # Pivot 5-Thn Kebocoran
    df_pivot_raw = pd.read_excel(excel2, sheet_name='Pivot_5Thn_Per_Prodi', header=2)
    df_pivot_raw.columns = df_pivot_raw.iloc[0]
    df_kebocoran = df_pivot_raw.iloc[1:].reset_index(drop=True)
    df_kebocoran = df_kebocoran[~df_kebocoran['Nama Program Studi'].astype(str).str.contains('PDD|GAYO', case=False)].copy()

    years = [2022, 2023, 2024, 2025, 2026]

    # =========================================================================
    # CHART 1: FUNNEL PIPELINE (Corong Seleksi Calon Mahasiswa)
    # =========================================================================
    print("[1/5] Menghasilkan A1_funnel_perjalanan_calon_mahasiswa.png...")

    funnel_data = []
    for y in years:
        funnel_data.append({
            'Tahun': y,
            'Peminat': df_s1[f'Peminat {y}'].sum(),
            'Daya_Tampung': df_s1[f'Daya Tampung {y}'].sum(),
            'Lulus_Seleksi': df_s1[f'Lulus Seleksi {y}'].sum(),
            'Daftar_Ulang': df_s1[f'Daftar Ulang {y}'].sum(),
            'Gugur': df_s1[f'Mundur/Gugur {y}'].sum()
        })
    df_funnel = pd.DataFrame(funnel_data)

    tot_pem = df_funnel['Peminat'].sum()
    tot_dt = df_funnel['Daya_Tampung'].sum()
    tot_ls = df_funnel['Lulus_Seleksi'].sum()
    tot_du = df_funnel['Daftar_Ulang'].sum()
    tot_gg = df_funnel['Gugur'].sum()

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(22, 11), dpi=300, facecolor='#F8FAFC',
                                     gridspec_kw={'width_ratios': [1.25, 1.0], 'wspace': 0.14})

    # --- LEFT PANEL: CORONG PIPELINE ---
    ax_l.set_facecolor('#FFFFFF')
    ax_l.set_xlim(-0.1, 1.1)
    ax_l.set_ylim(-0.02, 1.05)
    ax_l.axis('off')

    stages = [
        ('Peminat Terdaftar', tot_pem, '100% dari total pendaftar akun seleksi USK', '#1D4ED8', '#EFF6FF', 0.81, 0.92),
        ('Kapasitas Kuota (Daya Tampung)', tot_dt, f'{tot_dt/tot_pem*100:.1f}% rasio daya serap kuota kampus', '#4F46E5', '#EEF2FF', 0.56, 0.74),
        ('Lulus Seleksi', tot_ls, f'{tot_ls/tot_dt*100:.1f}% kuota terisi oleh kelulusan panitia', '#D97706', '#FFFBEB', 0.31, 0.60),
        ('Registrasi / Daftar Ulang', tot_du, f'{tot_du/tot_ls*100:.1f}% yield rate peserta lulus seleksi', '#059669', '#ECFDF5', 0.06, 0.50)
    ]

    for name, val, sub, border_col, bg_col, yp, w in stages:
        x_left = (1.0 - w) / 2.0
        rect = FancyBboxPatch((x_left, yp), w, 0.13, boxstyle='round,pad=0.015',
                              facecolor=bg_col, edgecolor=border_col, linewidth=2.0, zorder=3)
        ax_l.add_patch(rect)

        # Stage Number
        ax_l.text(0.5, yp + 0.088, f"{val:,.0f}", ha='center', va='center',
                  fontsize=21, fontweight='bold', color=border_col, zorder=5)
        # Stage Title & Subtitle
        ax_l.text(0.5, yp + 0.050, name.upper(), ha='center', va='center',
                  fontsize=10.5, fontweight='bold', color='#0F172A', zorder=5)
        ax_l.text(0.5, yp + 0.020, sub, ha='center', va='center',
                  fontsize=9.0, color='#475569', zorder=5)

    # Drop-off badges in the gaps
    dropoffs = [
        (0.750, f"Tersaring Seleksi: -{tot_pem - tot_dt:,.0f} ({ (tot_pem-tot_dt)/tot_pem*100:.1f}% Pelamar Tidak Lolos)", '#DC2626', '#FEF2F2'),
        (0.500, f"Kuota Tidak Terpenuhi di Kelulusan: -{tot_dt - tot_ls:,.0f} ({ (tot_dt-tot_ls)/tot_dt*100:.1f}% Kuota Belum Terisi)", '#B45309', '#FFFBEB'),
        (0.250, f"KEBOCORAN BESAR (Mundur): -{tot_ls - tot_du:,.0f} ({ (tot_ls-tot_du)/tot_ls*100:.1f}% Lulus tapi Tidak Masuk)", '#B91C1C', '#FEE2E2')
    ]

    for yp_drop, text_drop, text_col, bg_drop in dropoffs:
        ax_l.annotate('', xy=(0.5, yp_drop - 0.032), xytext=(0.5, yp_drop + 0.032),
                     arrowprops=dict(arrowstyle='->', color='#94A3B8', lw=2.0, mutation_scale=14), zorder=2)
        ax_l.text(0.5, yp_drop, text_drop, ha='center', va='center', fontsize=9.0, fontweight='bold',
                  color=text_col, bbox=dict(boxstyle='round,pad=0.35', facecolor=bg_drop, edgecolor=text_col, alpha=0.98, lw=1.2), zorder=6)

    # Title of Left Panel (well above first card)
    ax_l.text(0.5, 0.985, 'PIPELINE SELEKSI: DARI PEMINAT HINGGA MAHASISWA MASUK',
              ha='center', va='bottom', fontsize=13, fontweight='bold', color='#0F172A')

    # --- RIGHT PANEL: TABLE & STRATEGIC TAKEAWAYS ---
    ax_r.set_facecolor('#FFFFFF')
    ax_r.axis('off')

    ax_r.text(0.5, 0.99, 'TREN SELEKSI TAHUNAN & ANATOMI KEBOCORAN',
              ha='center', va='top', fontsize=13, fontweight='bold', color='#0F172A', transform=ax_r.transAxes)

    # Annual Table Header
    headers = ['Tahun', 'Peminat', 'Kuota', 'Lulus', 'Daftar', 'Mundur', 'Yield']
    cols_x = [0.03, 0.16, 0.31, 0.46, 0.60, 0.74, 0.88]

    ax_r.add_patch(FancyBboxPatch((0.01, 0.89), 0.98, 0.048, boxstyle='round,pad=0.01',
                                  facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=1.0, transform=ax_r.transAxes))
    for h, cx in zip(headers, cols_x):
        ax_r.text(cx, 0.914, h, ha='left', va='center', fontsize=10, fontweight='bold', color='#334155', transform=ax_r.transAxes)

    curr_y = 0.835
    for _, r in df_funnel.iterrows():
        y_int = int(r['Tahun'])
        yr = r['Daftar_Ulang'] / r['Lulus_Seleksi'] * 100
        yr_col = '#059669' if yr >= 83 else '#D97706' if yr >= 80 else '#DC2626'

        if y_int % 2 == 1:
            ax_r.add_patch(FancyBboxPatch((0.01, curr_y - 0.022), 0.98, 0.048, boxstyle='square,pad=0.0',
                                          facecolor='#F8FAFC', edgecolor='none', transform=ax_r.transAxes))

        row_vals = [
            str(y_int),
            f"{r['Peminat']:,.0f}",
            f"{r['Daya_Tampung']:,.0f}",
            f"{r['Lulus_Seleksi']:,.0f}",
            f"{r['Daftar_Ulang']:,.0f}",
            f"{r['Gugur']:,.0f}",
            f"{yr:.1f}%"
        ]
        for j, (v, cx) in enumerate(zip(row_vals, cols_x)):
            fc = yr_col if j == 6 else '#0F172A'
            fw = 'bold' if j in [0, 6] else 'normal'
            ax_r.text(cx, curr_y, v, ha='left', va='center', fontsize=9.5, fontweight=fw, color=fc, transform=ax_r.transAxes)
        curr_y -= 0.058

    # Total Row Box
    ax_r.add_patch(FancyBboxPatch((0.01, curr_y - 0.022), 0.98, 0.052, boxstyle='round,pad=0.01',
                                  facecolor='#E2E8F0', edgecolor='#94A3B8', lw=1.2, transform=ax_r.transAxes))
    tot_yr = tot_du / tot_ls * 100
    totals_val = ['TOTAL', f"{tot_pem:,.0f}", f"{tot_dt:,.0f}", f"{tot_ls:,.0f}", f"{tot_du:,.0f}", f"{tot_gg:,.0f}", f"{tot_yr:.1f}%"]
    for j, (v, cx) in enumerate(zip(totals_val, cols_x)):
        ax_r.text(cx, curr_y + 0.002, v, ha='left', va='center', fontsize=10, fontweight='bold', color='#0F172A', transform=ax_r.transAxes)

    # Executive Insight Box
    insight_box = FancyBboxPatch((0.01, 0.03), 0.98, 0.46, boxstyle='round,pad=0.02',
                                 facecolor='#FFF7ED', edgecolor='#FDBA74', linewidth=1.5, transform=ax_r.transAxes)
    ax_r.add_patch(insight_box)

    ax_r.text(0.05, 0.45, 'TEMUAN STRATEGIS & ANATOMI MASALAH:', ha='left', va='center',
              fontsize=11.5, fontweight='bold', color='#9A3412', transform=ax_r.transAxes)

    points = [
        ("Filter Seleksi Sangat Ketat:", f" Dari {tot_pem:,.0f} pelamar, hanya {tot_ls:,.0f} yang dinyatakan lulus ({tot_ls/tot_pem*100:.1f}%). Minat pelamar USK sangat tinggi."),
        ("Titik Kebocoran Nyata:", f" Sebanyak {tot_gg:,.0f} calon mahasiswa lulus BATAL mendaftar ulang ({tot_gg/tot_ls*100:.1f}%). Setara dengan potensi 133 kelas."),
        ("Stabilitas Konversi 2026:", " Registrasi 2026 mencatat 7.976 daftar ulang (Yield 85,4%), membuktikan retensi lulusan terjaga kuat di atas batas 80%."),
        ("Rekomendasi Kebijakan:", " Terapkan sistem 'Cadangan Aktif' (Over-booking dinamis) dan percepat penetapan UKT untuk memitigasi 1.368 kursi gugur.")
    ]

    p_y = 0.37
    for title, desc in points:
        ax_r.text(0.05, p_y, f"\u25b6 {title}", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#C2410C', transform=ax_r.transAxes)
        ax_r.text(0.05, p_y - 0.042, desc, ha='left', va='center', fontsize=9, color='#334155', transform=ax_r.transAxes)
        p_y -= 0.090

    fig.suptitle('CORONG SELEKSI MAHASISWA BARU: DARI PEMINAT HINGGA DAFTAR ULANG (2022–2026)\n'
                 'Evaluasi Efisiensi Penjaringan & Titik Kebocoran Peserta Lulus Seleksi S1 Kampus Utama USK',
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.98)

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.93])
    plt.savefig(os.path.join(chart_dir, "A1_funnel_perjalanan_calon_mahasiswa.png"), dpi=300)
    plt.close()
    print("  Done A1_funnel")

    # =========================================================================
    # CHART 2: HEATMAP 66 PRODI (2-KOLOM 16:9 PRESENTATION-GRADE)
    # =========================================================================
    print("[2/5] Menghasilkan A2_heatmap_fill_rate_prodi_tahun.png...")

    prodi_stats = []
    for _, r in df_s1.iterrows():
        p_name = r['Nama Program Studi']
        fak = r['Fakultas']

        # Hanya hitung tahun di mana daya tampung > 0 (menghindari mendivisi dengan tahun belum buka)
        fills = []
        valid_fills = []
        for y in years:
            dt_y = r[f'Daya Tampung {y}']
            fr_y = r[f'Fill Rate {y} (%)']
            if pd.isna(dt_y) or dt_y == 0:
                fills.append(np.nan)
            else:
                fills.append(fr_y if pd.notna(fr_y) else 0.0)
                valid_fills.append(fr_y if pd.notna(fr_y) else 0.0)

        avg_fr = np.mean(valid_fills) if len(valid_fills) > 0 else 0.0
        fr_26 = fills[4] if pd.notna(fills[4]) else 0.0

        prodi_stats.append({
            'Prodi': p_name,
            'Fakultas': fak,
            'Fills': fills,
            'Avg': avg_fr,
            'FR_2026': fr_26
        })

    # Sort by Avg Fill Rate ascending
    df_hm = pd.DataFrame(prodi_stats).sort_values('Avg', ascending=True).reset_index(drop=True)

    # 33 prodi terendah di kiri, 33 prodi tertinggi di kanan
    df_hm_left = df_hm.iloc[:33].reset_index(drop=True)
    df_hm_right = df_hm.iloc[33:].reset_index(drop=True)

    fig, (ax_hl, ax_hr) = plt.subplots(1, 2, figsize=(24, 12), dpi=300, facecolor='#F8FAFC',
                                       gridspec_kw={'wspace': 0.10})

    def render_heatmap_panel(ax, sub_df, title, is_left_panel=True):
        ax.set_facecolor('#FFFFFF')
        ax.axis('off')

        banner_bg = '#FEF2F2' if is_left_panel else '#F0FDF4'
        banner_border = '#EF4444' if is_left_panel else '#10B981'
        banner_text_col = '#991B1B' if is_left_panel else '#065F46'
        ax.add_patch(FancyBboxPatch((0.01, 0.94), 0.98, 0.05, boxstyle='round,pad=0.01',
                                   facecolor=banner_bg, edgecolor=banner_border, lw=1.5, transform=ax.transAxes))
        ax.text(0.5, 0.965, title, ha='center', va='center', fontsize=11.5, fontweight='bold',
                color=banner_text_col, transform=ax.transAxes)

        col_x = [0.02, 0.45, 0.54, 0.63, 0.72, 0.81, 0.90]
        col_names = ['PROGRAM STUDI', '2022', '2023', '2024', '2025', '2026', 'RATA']

        ax.add_patch(FancyBboxPatch((0.01, 0.895), 0.98, 0.038, boxstyle='square,pad=0.0',
                                   facecolor='#F1F5F9', edgecolor='#CBD5E1', lw=0.8, transform=ax.transAxes))
        for cn, cx in zip(col_names, col_x):
            align = 'left' if cn == 'PROGRAM STUDI' else 'center'
            ax.text(cx if align == 'left' else cx + 0.035, 0.914, cn, ha=align, va='center',
                    fontsize=8.5, fontweight='bold', color='#334155', transform=ax.transAxes)

        row_h = 0.0255
        start_y = 0.872

        def get_fr_color(val):
            if pd.isna(val) or val is None:
                return '#F1F5F9', '#94A3B8'  # Abu-abu (Belum buka)
            elif val < 60:
                return '#F87171', '#7F1D1D'  # Merah pekat
            elif val < 70:
                return '#FCA5A5', '#991B1B'  # Merah muda
            elif val < 80:
                return '#FDE68A', '#78350F'  # Kuning / Jingga
            elif val < 90:
                return '#A7F3D0', '#064E3B'  # Hijau muda
            else:
                return '#34D399', '#064E3B'  # Hijau segar

        for idx, r in sub_df.iterrows():
            y_curr = start_y - (idx * row_h)

            short_p = r['Prodi'][:24] + '..' if len(r['Prodi']) > 24 else r['Prodi']
            ax.text(0.02, y_curr, short_p, ha='left', va='center', fontsize=8, color='#0F172A', transform=ax.transAxes)

            for y_i, val in enumerate(r['Fills']):
                cx = col_x[1 + y_i]
                bg_col, txt_col = get_fr_color(val)
                is_alert = pd.notna(val) and val < 68 and val > 0

                cell_rect = FancyBboxPatch((cx, y_curr - 0.011), 0.075, 0.022, boxstyle='round,pad=0.002',
                                           facecolor=bg_col, edgecolor='#DC2626' if is_alert else 'none',
                                           lw=1.2 if is_alert else 0.0, transform=ax.transAxes)
                ax.add_patch(cell_rect)

                cell_txt = f"{val:.0f}" if pd.notna(val) else "–"
                ax.text(cx + 0.0375, y_curr, cell_txt, ha='center', va='center', fontsize=8,
                        fontweight='bold' if (is_alert or (pd.notna(val) and val >= 95)) else 'normal',
                        color=txt_col, transform=ax.transAxes)

            avg_bg, avg_txt = get_fr_color(r['Avg'])
            avg_rect = FancyBboxPatch((col_x[6], y_curr - 0.011), 0.08, 0.022, boxstyle='round,pad=0.002',
                                      facecolor=avg_bg, edgecolor='#475569', lw=0.6, transform=ax.transAxes)
            ax.add_patch(avg_rect)
            ax.text(col_x[6] + 0.04, y_curr, f"{r['Avg']:.1f}%", ha='center', va='center',
                    fontsize=8, fontweight='bold', color=avg_txt, transform=ax.transAxes)

    render_heatmap_panel(ax_hl, df_hm_left, '33 PRODI PRIORITAS EVALUASI (Fill Rate Rata-rata 45% – 78%)', is_left_panel=True)
    render_heatmap_panel(ax_hr, df_hm_right, '33 PRODI KINERJA STABIL & UNGGULAN (Fill Rate Rata-rata 79% – 100%)', is_left_panel=False)

    fig.suptitle('PETA PANAS KETERISIAN KUOTA (FILL RATE) 66 PROGRAM STUDI S1 USK (2022–2026)\n'
                 'Tinjauan Menyeluruh Daya Serap Kuota Per Tahun \u00b7 Border Merah = Alarm Kritis (< 68%) \u00b7 Sel Abu-abu = Belum Dibuka',
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.98)

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.94])
    plt.savefig(os.path.join(chart_dir, "A2_heatmap_fill_rate_prodi_tahun.png"), dpi=300)
    plt.close()
    print("  Done A2_heatmap")

    # =========================================================================
    # CHART 3: ANALISIS PARETO KURSI KOSONG (TOP 30 PRODI DEFISIT)
    # =========================================================================
    print("[3/5] Menghasilkan A3_pareto_kursi_kosong.png...")

    prodi_kosong = []
    for _, r in df_s1.iterrows():
        total_k = sum(r[f'Kursi Kosong {y}'] for y in years if pd.notna(r[f'Kursi Kosong {y}']))
        prodi_kosong.append({
            'Prodi': r['Nama Program Studi'],
            'Fakultas': r['Fakultas'],
            'Total_Kosong': total_k
        })

    df_pk = pd.DataFrame(prodi_kosong).sort_values('Total_Kosong', ascending=False).reset_index(drop=True)
    total_semua_kosong = df_pk['Total_Kosong'].sum()

    # Tampilkan Top 30 prodi agar visual lereng Pareto sangat alami dan proporsional
    top_n = 30
    df_top = df_pk.iloc[:top_n].copy()
    df_top.loc[:, 'Kumulatif'] = df_top['Total_Kosong'].cumsum()
    df_top.loc[:, 'Kumulatif_Pct'] = df_top['Kumulatif'] / total_semua_kosong * 100

    fig, (ax_p, ax_box) = plt.subplots(1, 2, figsize=(22, 10.5), dpi=300, facecolor='#F8FAFC',
                                       gridspec_kw={'width_ratios': [1.5, 0.8], 'wspace': 0.12})

    ax_p.set_facecolor('#FFFFFF')
    n_display = len(df_top)
    x_pos = np.arange(n_display)

    colors_pareto = []
    for _, r in df_top.iterrows():
        if r['Kumulatif_Pct'] <= 50:
            colors_pareto.append('#DC2626')  # Merah (Kritis 50% loss)
        elif r['Kumulatif_Pct'] <= 80:
            colors_pareto.append('#F59E0B')  # Jingga (Prioritas intervensi)
        else:
            colors_pareto.append('#3B82F6')  # Biru

    bars = ax_p.bar(x_pos, df_top['Total_Kosong'], color=colors_pareto, edgecolor='#1E293B',
                    linewidth=0.7, alpha=0.9, zorder=3)

    for i in range(min(15, n_display)):
        ax_p.text(i, df_top.iloc[i]['Total_Kosong'] + 6, f"{df_top.iloc[i]['Total_Kosong']:.0f}",
                  ha='center', va='bottom', fontsize=8, fontweight='bold', color='#0F172A')

    short_labels = [p[:20] + '..' if len(p) > 20 else p for p in df_top['Prodi']]
    ax_p.set_xticks(x_pos)
    ax_p.set_xticklabels(short_labels, rotation=50, ha='right', fontsize=8.5, color='#1E293B')
    ax_p.set_ylabel('Total Kursi Kosong (Kumulatif 5 Tahun)', fontsize=11, fontweight='bold', color='#1E293B')
    ax_p.set_ylim(0, max(df_top['Total_Kosong']) * 1.18)

    ax_p2 = ax_p.twinx()
    ax_p2.plot(x_pos, df_top['Kumulatif_Pct'], color='#1D4ED8', linewidth=2.5, marker='o',
               markersize=4.5, zorder=5)
    ax_p2.set_ylabel('Persentase Kumulatif dari Total Defisit Kampus (%)', fontsize=11, fontweight='bold', color='#1D4ED8')
    ax_p2.set_ylim(0, 105)

    # 80% Cutoff Line
    ax_p2.axhline(y=80, color='#DC2626', linestyle='--', linewidth=1.5, alpha=0.8, zorder=2)
    ax_p.grid(axis='y', linestyle=':', alpha=0.4, color='#94A3B8', zorder=0)

    # Clean Inset Note on Pareto Plot
    ax_p.text(0.50, 0.88, 'AMBANG 80% DEFISIT TOTAL\nDidominasi oleh 35 Prodi S1 teratas (53% dari total 66 prodi)',
              ha='center', va='center', fontsize=9.5, fontweight='bold', color='#991B1B',
              transform=ax_p.transAxes,
              bbox=dict(boxstyle='round,pad=0.5', facecolor='#FEF2F2', edgecolor='#FCA5A5', alpha=0.95))

    legend_p = [
        Patch(facecolor='#DC2626', edgecolor='#1E293B', label='Penyumbang 0–50% Defisit (Zona Kritis)'),
        Patch(facecolor='#F59E0B', edgecolor='#1E293B', label='Penyumbang 50–80% Defisit (Zona Prioritas)'),
        Patch(facecolor='#3B82F6', edgecolor='#1E293B', label='Penyumbang Defisit Lanjutan (>80%)'),
        Line2D([0], [0], color='#1D4ED8', linewidth=2.5, marker='o', markersize=5, label='Kurva Kumulatif Defisit (%)')
    ]
    ax_p.legend(handles=legend_p, loc='upper left', fontsize=9, frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    # Right Panel: Faculty Summary & Actionable Recs
    ax_box.set_facecolor('#FFFFFF')
    ax_box.axis('off')

    ax_box.text(0.5, 0.99, 'KONSENTRASI DEFISIT PER FAKULTAS', ha='center', va='top',
                fontsize=12.5, fontweight='bold', color='#0F172A', transform=ax_box.transAxes)

    fak_dict = {}
    for _, r in df_s1.iterrows():
        f = r['Fakultas']
        tk = sum(r[f'Kursi Kosong {y}'] for y in years if pd.notna(r[f'Kursi Kosong {y}']))
        fak_dict[f] = fak_dict.get(f, 0) + tk
    df_fak = pd.DataFrame(list(fak_dict.items()), columns=['Fakultas', 'Kosong']).sort_values('Kosong', ascending=False)

    top_faks = df_fak.head(5)
    f_y = 0.91
    for _, rf in top_faks.iterrows():
        pct_f = rf['Kosong'] / total_semua_kosong * 100
        ax_box.add_patch(FancyBboxPatch((0.02, f_y - 0.05), 0.96, 0.055, boxstyle='round,pad=0.01',
                                        facecolor='#F8FAFC', edgecolor='#CBD5E1', lw=1.0, transform=ax_box.transAxes))
        ax_box.text(0.06, f_y - 0.022, rf['Fakultas'], ha='left', va='center', fontsize=10, fontweight='bold', color='#1E293B', transform=ax_box.transAxes)
        ax_box.text(0.92, f_y - 0.022, f"{rf['Kosong']:,} ({pct_f:.1f}%)", ha='right', va='center', fontsize=9.5, fontweight='bold', color='#B91C1C', transform=ax_box.transAxes)
        f_y -= 0.075

    # Strategic Action Box
    action_box = FancyBboxPatch((0.02, 0.03), 0.96, 0.46, boxstyle='round,pad=0.02',
                                facecolor='#EFF6FF', edgecolor='#93C5FD', lw=1.5, transform=ax_box.transAxes)
    ax_box.add_patch(action_box)

    ax_box.text(0.06, 0.45, 'IMPLIKASI ALOKASI KUOTA (RKAT):', ha='left', va='center',
                fontsize=11.5, fontweight='bold', color='#1E40AF', transform=ax_box.transAxes)

    recs = [
        ("Total Kehilangan Kuota:", f" Sebanyak {total_semua_kosong:,} kursi hangus selama 5 tahun. Menimbulkan pemborosan alokasi dosen dan ruang kelas."),
        ("Konsentrasi 4 Fakultas Utama:", " FKIP, Teknik, Pertanian, dan FPK menyumbang 74,5% dari seluruh kursi kosong di USK."),
        ("Top 5 Prodi Defisit Kronis:", " Budidaya Perairan (384), Teknik Kimia (283), Keperawatan (278), Ilmu Kelautan (275), dan Pend. Fisika (267)."),
        ("Rasionalisasi Kuota:", " Kurangi kuota 15–25% pada 10 prodi defisit kronis, lalu alihkan kursi ke prodi berdaya saing tinggi (Informatika, Kedokteran, Manajemen).")
    ]

    r_y = 0.37
    for h_rec, desc_rec in recs:
        ax_box.text(0.06, r_y, f"\u25cf {h_rec}", ha='left', va='center', fontsize=9.5, fontweight='bold', color='#1D4ED8', transform=ax_box.transAxes)
        ax_box.text(0.06, r_y - 0.042, desc_rec, ha='left', va='center', fontsize=9, color='#334155', transform=ax_box.transAxes)
        r_y -= 0.090

    fig.suptitle('ANALISIS PARETO: KONSENTRASI PEMBOROSAN KURSI KOSONG S1 USK (2022–2026)\n'
                 'Prinsip 80/20: Mayoritas Kursi Kosong Terpusat pada Segelintir Program Studi dan Fakultas',
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.98)

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.93])
    plt.savefig(os.path.join(chart_dir, "A3_pareto_kursi_kosong.png"), dpi=300)
    plt.close()
    print("  Done A3_pareto")

    # =========================================================================
    # CHART 4: DINAMIKA MIGRASI KUADRAN 2022 -> 2026 (SLOPE / SANKEY STYLE)
    # =========================================================================
    print("[4/5] Menghasilkan A4_slope_migrasi_kuadran_2022_2026.png...")

    def get_quadrant_id(keketatan, fill_rate):
        if keketatan >= 4.0 and fill_rate >= 80.0:
            return 1  # Unggulan
        elif keketatan < 4.0 and fill_rate >= 80.0:
            return 2  # Stabil
        elif keketatan < 4.0 and fill_rate < 80.0:
            return 3  # Kurang Diminati
        else:
            return 4  # Selektif tapi Bocor

    quad_labels = {
        1: 'KUADRAN I\nUNGGULAN',
        2: 'KUADRAN II\nSTABIL',
        3: 'KUADRAN III\nKURANG DIMINATI',
        4: 'KUADRAN IV\nSELEKTIF BOCOR'
    }
    quad_theme = {
        1: ('#059669', '#ECFDF5', '#A7F3D0'),
        2: ('#2563EB', '#EFF6FF', '#BFDBFE'),
        3: ('#DC2626', '#FEF2F2', '#FECACA'),
        4: ('#D97706', '#FFFBEB', '#FDE68A')
    }

    prodi_migs = []
    for _, r in df_s1.iterrows():
        p = r['Nama Program Studi']
        k22 = r['Keketatan 2022'] if pd.notna(r['Keketatan 2022']) else 0
        f22 = r['Fill Rate 2022 (%)'] if pd.notna(r['Fill Rate 2022 (%)']) else 0
        k26 = r['Keketatan 2026'] if pd.notna(r['Keketatan 2026']) else 0
        f26 = r['Fill Rate 2026 (%)'] if pd.notna(r['Fill Rate 2026 (%)']) else 0

        q22 = get_quadrant_id(k22, f22)
        q26 = get_quadrant_id(k26, f26)

        direction = 'tetap' if q22 == q26 else ('naik' if q26 < q22 else 'turun')
        prodi_migs.append({
            'Prodi': p,
            'Fakultas': r['Fakultas'],
            'Q22': q22,
            'Q26': q26,
            'Dir': direction
        })

    df_mig = pd.DataFrame(prodi_migs)
    trans_counts = Counter((r['Q22'], r['Q26']) for _, r in df_mig.iterrows())

    fig, (ax_s, ax_c) = plt.subplots(1, 2, figsize=(22, 10.5), dpi=300, facecolor='#F8FAFC',
                                     gridspec_kw={'width_ratios': [1.35, 1.0], 'wspace': 0.10})

    ax_s.set_facecolor('#FFFFFF')
    ax_s.set_xlim(-0.2, 3.2)
    ax_s.set_ylim(-0.4, 4.6)
    ax_s.axis('off')

    y_coords = {1: 3.6, 2: 2.5, 3: 1.4, 4: 0.3}

    # Pillars
    for q in [1, 2, 3, 4]:
        yp = y_coords[q]
        border_c, bg_c, _ = quad_theme[q]

        # 2022 Pillar
        c22 = sum(1 for _, r in df_mig.iterrows() if r['Q22'] == q)
        ax_s.add_patch(FancyBboxPatch((0.0, yp - 0.38), 0.75, 0.76, boxstyle='round,pad=0.03',
                                     facecolor=bg_c, edgecolor=border_c, lw=2.0, zorder=3))
        ax_s.text(0.375, yp + 0.12, quad_labels[q], ha='center', va='center',
                  fontsize=9.5, fontweight='bold', color=border_c, zorder=5)
        ax_s.text(0.375, yp - 0.18, f"{c22} Prodi", ha='center', va='center',
                  fontsize=12, fontweight='bold', color='#0F172A', zorder=5)

        # 2026 Pillar
        c26 = sum(1 for _, r in df_mig.iterrows() if r['Q26'] == q)
        ax_s.add_patch(FancyBboxPatch((2.25, yp - 0.38), 0.75, 0.76, boxstyle='round,pad=0.03',
                                     facecolor=bg_c, edgecolor=border_c, lw=2.0, zorder=3))
        ax_s.text(2.625, yp + 0.12, quad_labels[q], ha='center', va='center',
                  fontsize=9.5, fontweight='bold', color=border_c, zorder=5)
        ax_s.text(2.625, yp - 0.18, f"{c26} Prodi", ha='center', va='center',
                  fontsize=12, fontweight='bold', color='#0F172A', zorder=5)

    ax_s.text(0.375, 4.35, 'TAHUN 2022', ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')
    ax_s.text(2.625, 4.35, 'TAHUN 2026', ha='center', va='center', fontsize=14, fontweight='bold', color='#0F172A')

    # Staggered Badge Positions to prevent collision
    # Each transition key has (t_ratio, y_shift)
    stagger_map = {
        (1, 1): (0.50, 0.0), (2, 2): (0.50, 0.0), (3, 3): (0.50, 0.0), (4, 4): (0.50, 0.0),
        (3, 1): (0.35, 0.08), (4, 1): (0.42, -0.06), (3, 2): (0.68, -0.05),
        (1, 2): (0.28, 0.05), (1, 4): (0.75, -0.05), (3, 4): (0.65, 0.06), (4, 3): (0.30, 0.05)
    }

    for (q_from, q_to), count in trans_counts.items():
        if count == 0:
            continue
        y1, y2 = y_coords[q_from], y_coords[q_to]
        lw = max(1.2, min(count * 0.75, 9.0))
        alpha = max(0.4, min(count / 25.0, 0.85))

        if q_from == q_to:
            line_col = '#94A3B8'
            ax_s.annotate('', xy=(2.25, y2), xytext=(0.75, y1),
                         arrowprops=dict(arrowstyle='->', color=line_col, lw=lw, alpha=alpha, mutation_scale=12))
            ax_s.text(1.5, y1, f"{count}", ha='center', va='center', fontsize=9, fontweight='bold',
                      color='#334155', bbox=dict(boxstyle='circle,pad=0.25', facecolor='#FFFFFF', edgecolor='#CBD5E1', lw=1.0), zorder=6)
        else:
            is_upgrade = q_to < q_from
            line_col = '#059669' if is_upgrade else '#DC2626'
            rad = 0.10 if is_upgrade else -0.10
            ax_s.annotate('', xy=(2.25, y2), xytext=(0.75, y1),
                         arrowprops=dict(arrowstyle='->', color=line_col, lw=lw, alpha=alpha,
                                         connectionstyle=f'arc3,rad={rad}', mutation_scale=12))

            t_rat, y_off = stagger_map.get((q_from, q_to), (0.50, 0.0))
            bx = 0.75 + t_rat * (2.25 - 0.75)
            by = y1 + t_rat * (y2 - y1) + y_off
            ax_s.text(bx, by, f"{count}", ha='center', va='center', fontsize=8.5, fontweight='bold',
                      color=line_col, bbox=dict(boxstyle='circle,pad=0.25', facecolor='#FFFFFF', edgecolor=line_col, lw=1.2), zorder=6)

    # Right: Migration Summary Cards
    ax_c.set_facecolor('#FFFFFF')
    ax_c.axis('off')

    tetap_n = sum(1 for _, r in df_mig.iterrows() if r['Dir'] == 'tetap')
    naik_n = sum(1 for _, r in df_mig.iterrows() if r['Dir'] == 'naik')
    turun_n = sum(1 for _, r in df_mig.iterrows() if r['Dir'] == 'turun')

    ax_c.text(0.5, 0.99, 'REKAPITULASI MIGRASI PORTOFOLIO PRODI', ha='center', va='top',
              fontsize=12.5, fontweight='bold', color='#0F172A', transform=ax_c.transAxes)

    stats_y = 0.89
    stat_items = [
        (0.02, 0.30, 'TETAP POSISI', f"{tetap_n} Prodi ({tetap_n/66*100:.0f}%)", '#64748B', '#F1F5F9', '#CBD5E1'),
        (0.35, 0.30, 'NAIK KELAS \u2191', f"{naik_n} Prodi ({naik_n/66*100:.0f}%)", '#059669', '#ECFDF5', '#A7F3D0'),
        (0.68, 0.30, 'TERDEGRADASI \u2193', f"{turun_n} Prodi ({turun_n/66*100:.0f}%)", '#DC2626', '#FEF2F2', '#FECACA')
    ]
    for x_b, w_b, title_b, val_b, c_b, bg_b, bd_b in stat_items:
        ax_c.add_patch(FancyBboxPatch((x_b, stats_y), w_b, 0.075, boxstyle='round,pad=0.01',
                                      facecolor=bg_b, edgecolor=bd_b, lw=1.2, transform=ax_c.transAxes))
        ax_c.text(x_b + w_b/2, stats_y + 0.048, title_b, ha='center', va='center', fontsize=8.5, fontweight='bold', color=c_b, transform=ax_c.transAxes)
        ax_c.text(x_b + w_b/2, stats_y + 0.020, val_b, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#0F172A', transform=ax_c.transAxes)

    # Card 1: Naik Kelas
    ax_c.add_patch(FancyBboxPatch((0.02, 0.47), 0.96, 0.39, boxstyle='round,pad=0.02',
                                  facecolor='#F0FDF4', edgecolor='#86EFAC', lw=1.5, transform=ax_c.transAxes))
    ax_c.text(0.06, 0.83, '\u25b2 PERUBAHAN POSITIF (PRODI NAIK KELAS / UPGRADE):', ha='left', va='center',
              fontsize=10.5, fontweight='bold', color='#166534', transform=ax_c.transAxes)

    naik_list = [
        ("Bisnis Digital", "Kuadran III \u2192 I (Unggulan): Peminatan meledak, kuota terisi 98%"),
        ("Teknik Lingkungan", "Kuadran III \u2192 I (Unggulan): Rebound signifikan dari 69% ke 83%"),
        ("Ilmu Keperawatan", "Kuadran III \u2192 I (Unggulan): Keketatan naik tajam, penyerapan stabil"),
        ("Tek. Sumber Daya Air", "Kuadran III \u2192 II (Stabil): Fill rate naik dari 64% ke 87%"),
        ("Pendidikan Seni Drama", "Kuadran III \u2192 II (Stabil): Fill rate naik dari 75% ke 92%")
    ]
    u_y = 0.77
    for p_name, p_desc in naik_list:
        ax_c.text(0.06, u_y, f"\u2714 {p_name}:", ha='left', va='center', fontsize=9, fontweight='bold', color='#15803D', transform=ax_c.transAxes)
        ax_c.text(0.06, u_y - 0.03, p_desc, ha='left', va='center', fontsize=8.5, color='#334155', transform=ax_c.transAxes)
        u_y -= 0.062

    # Card 2: Terdegradasi
    ax_c.add_patch(FancyBboxPatch((0.02, 0.03), 0.96, 0.40, boxstyle='round,pad=0.02',
                                  facecolor='#FEF2F2', edgecolor='#FCA5A5', lw=1.5, transform=ax_c.transAxes))
    ax_c.text(0.06, 0.395, '\u25bc PERINGATAN STRATEGIS (PRODI TERDEGRADASI / DOWNGRADE):', ha='left', va='center',
              fontsize=10.5, fontweight='bold', color='#991B1B', transform=ax_c.transAxes)

    turun_list = [
        ("Pend. Dokter Hewan", "Kuadran I \u2192 II (Stabil): Rasio peminatan melandai, turun dari kuadran bintang"),
        ("Arsitektur", "Kuadran I \u2192 II (Stabil): Peminat turun, persaingan mengendur"),
        ("Pend. Guru PAUD", "Kuadran I \u2192 IV (Bocor): Peminat banyak tapi yang daftar ulang anjlok ke 74%"),
        ("Perenc. Wilayah Kota", "Kuadran I \u2192 IV (Bocor): Masalah drop-out tinggi di tahap daftar ulang (75%)"),
        ("Teknik Elektro", "Kuadran III \u2192 IV (Bocor): Terjebak masalah ganda peminat rendah & mundur")
    ]
    d_y = 0.335
    for p_name, p_desc in turun_list:
        ax_c.text(0.06, d_y, f"\u2718 {p_name}:", ha='left', va='center', fontsize=9, fontweight='bold', color='#B91C1C', transform=ax_c.transAxes)
        ax_c.text(0.06, d_y - 0.03, p_desc, ha='left', va='center', fontsize=8.5, color='#334155', transform=ax_c.transAxes)
        d_y -= 0.062

    fig.suptitle('MIGRASI KUADRAN PROGRAM STUDI S1 UNIVERSITAS SYIAH KUALA (2022 \u2192 2026)\n'
                 'Evolusi Posisi Strategis 66 Prodi: 44 Bertahan, 14 Menguat (Naik Kelas), 8 Melemah (Perlu Intervensi)',
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.98)

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.93])
    plt.savefig(os.path.join(chart_dir, "A4_slope_migrasi_kuadran_2022_2026.png"), dpi=300)
    plt.close()
    print("  Done A4_slope")

    # =========================================================================
    # CHART 5: SCATTER KORELASI KEBOCORAN vs FILL RATE (16:9 DENGAN 4 KUADRAN)
    # =========================================================================
    print("[5/5] Menghasilkan A5_scatter_kebocoran_vs_fill_rate.png...")

    scatter_rows = []
    for _, rs1 in df_s1.iterrows():
        p_name = rs1['Nama Program Studi'].strip()
        fak = rs1['Fakultas']

        match_k = df_kebocoran[df_kebocoran['Nama Program Studi'].astype(str).str.strip().str.upper() == p_name.upper()]
        if len(match_k) > 0:
            row_k = match_k.iloc[0]
            keb_rate = float(row_k['Tingkat Kebocoran']) * 100 if pd.notna(row_k['Tingkat Kebocoran']) else 0.0
            gugur_tot = float(row_k['Total Gugur (5-Thn)']) if pd.notna(row_k['Total Gugur (5-Thn)']) else 0.0
        else:
            gugur_tot = sum(rs1[f'Mundur/Gugur {y}'] for y in years if pd.notna(rs1[f'Mundur/Gugur {y}']))
            lulus_tot = sum(rs1[f'Lulus Seleksi {y}'] for y in years if pd.notna(rs1[f'Lulus Seleksi {y}']))
            keb_rate = (gugur_tot / lulus_tot * 100) if lulus_tot > 0 else 0.0

        # Hanya rata-ratakan tahun di mana DT > 0
        valid_fr = []
        valid_dt = []
        for y in years:
            dty = rs1[f'Daya Tampung {y}']
            fry = rs1[f'Fill Rate {y} (%)']
            if pd.notna(dty) and dty > 0 and pd.notna(fry):
                valid_fr.append(fry)
                valid_dt.append(dty)

        avg_fr = np.mean(valid_fr) if len(valid_fr) > 0 else 0.0
        avg_dt = np.mean(valid_dt) if len(valid_dt) > 0 else 50.0

        scatter_rows.append({
            'Prodi': p_name,
            'Fakultas': fak,
            'Kebocoran': keb_rate,
            'Fill_Rate': avg_fr,
            'DT': avg_dt,
            'Gugur': gugur_tot
        })

    df_sc = pd.DataFrame(scatter_rows)

    fig, ax = plt.subplots(figsize=(20, 10.5), dpi=300, facecolor='#F8FAFC')
    ax.set_facecolor('#FFFFFF')

    # Shaded Quadrant Backgrounds
    ax.axvspan(0, 15.0, ymin=(80 - 25)/(105 - 25), ymax=1.0, color='#F0FDF4', alpha=0.5, zorder=0)
    ax.axvspan(15.0, 50.0, ymin=(80 - 25)/(105 - 25), ymax=1.0, color='#FFFBEB', alpha=0.5, zorder=0)
    ax.axvspan(0, 15.0, ymin=0.0, ymax=(80 - 25)/(105 - 25), color='#EFF6FF', alpha=0.5, zorder=0)
    ax.axvspan(15.0, 50.0, ymin=0.0, ymax=(80 - 25)/(105 - 25), color='#FEF2F2', alpha=0.5, zorder=0)

    # Threshold Lines
    ax.axhline(y=80, color='#64748B', linestyle='--', linewidth=1.5, alpha=0.8, zorder=1)
    ax.axvline(x=15, color='#64748B', linestyle='--', linewidth=1.5, alpha=0.8, zorder=1)

    # Threshold Labels
    ax.text(1.0, 80.8, 'Standar Keterisian Kuota (80%)', fontsize=9, fontweight='bold', color='#475569', zorder=3)
    ax.text(15.2, 28.0, 'Ambang Batas Kebocoran Wajar (15%)', fontsize=9, fontweight='bold', color='#475569', zorder=3)

    # Quadrant Title Labels (Placed safely away from edges and legend)
    ax.text(1.5, 103, 'KUADRAN A: IDEAL & PRIMA\nKebocoran Rendah (<15%) \u00b7 Kuota Terisi Penuh (>80%)',
            ha='left', va='top', fontsize=10, fontweight='bold', color='#047857', zorder=2)
    ax.text(32.0, 103, 'KUADRAN B: PHANTOM DEMAND / BUFFER KUAT\nKebocoran Tinggi (>15%) \u00b7 Kuota Tetap Penuh (>80%)',
            ha='left', va='top', fontsize=10, fontweight='bold', color='#B45309', zorder=2)
    ax.text(1.5, 32, 'KUADRAN C: DEFISIT PEMINAT MURNI\nKebocoran Rendah (<15%) \u00b7 Kuota Kosong (<80%)',
            ha='left', va='bottom', fontsize=10, fontweight='bold', color='#1D4ED8', zorder=2)
    ax.text(48.5, 32, 'KUADRAN D: ZONA KRITIS / DOUBLE JEOPARDY\nKebocoran Tinggi (>15%) \u00b7 Kuota Sangat Kosong (<80%)',
            ha='right', va='bottom', fontsize=10, fontweight='bold', color='#B91C1C', zorder=2)

    # Scatter points
    colors_sc = []
    for _, r in df_sc.iterrows():
        if r['Kebocoran'] <= 15.0 and r['Fill_Rate'] >= 80.0:
            colors_sc.append('#10B981')  # Emerald
        elif r['Kebocoran'] > 15.0 and r['Fill_Rate'] >= 80.0:
            colors_sc.append('#F59E0B')  # Amber
        elif r['Kebocoran'] <= 15.0 and r['Fill_Rate'] < 80.0:
            colors_sc.append('#3B82F6')  # Blue
        else:
            colors_sc.append('#EF4444')  # Red

    sizes = 60 + (df_sc['DT'] / df_sc['DT'].max()) * 260
    scatter = ax.scatter(df_sc['Kebocoran'], df_sc['Fill_Rate'], s=sizes, c=colors_sc,
                         edgecolors='#1E293B', linewidth=1.2, alpha=0.88, zorder=4)

    # Outlier Labels (Carefully positioned offsets)
    outliers_callouts = [
        ('PENDIDIKAN DOKTER', (-15, 14)),
        ('ILMU HUKUM', (12, 10)),
        ('INFORMATIKA', (-15, -18)),
        ('PSIKOLOGI', (15, 10)),
        ('FARMASI', (15, -12)),
        ('FISIKA', (15, -10)),
        ('BUDIDAYA PERAIRAN', (15, -12)),
        ('TEKNIK KIMIA', (-25, -15)),
        ('TEKNOLOGI INDUSTRI HASIL', (15, 10)),
        ('TEKNIK PERMINYAKAN', (15, -10))
    ]

    for p_out, (ox, oy) in outliers_callouts:
        m_row = df_sc[df_sc['Prodi'].str.contains(p_out, case=False, na=False)]
        if len(m_row) > 0:
            rx = m_row.iloc[0]
            short_lbl = rx['Prodi'][:20]
            ax.annotate(short_lbl,
                        xy=(rx['Kebocoran'], rx['Fill_Rate']),
                        xytext=(ox, oy), textcoords='offset points',
                        fontsize=8, fontweight='bold', color='#0F172A',
                        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor='#64748B', alpha=0.92, lw=0.8),
                        arrowprops=dict(arrowstyle='->', color='#64748B', lw=1.0),
                        zorder=6)

    # Regression Trendline
    valid_sc = df_sc.dropna(subset=['Kebocoran', 'Fill_Rate'])
    if len(valid_sc) > 1:
        z = np.polyfit(valid_sc['Kebocoran'], valid_sc['Fill_Rate'], 1)
        p_fit = np.poly1d(z)
        x_trend = np.linspace(5, 38, 100)
        ax.plot(x_trend, p_fit(x_trend), '--', color='#6366F1', linewidth=2.0, alpha=0.7, zorder=3)
        corr_r = valid_sc['Kebocoran'].corr(valid_sc['Fill_Rate'])

        ax.text(0.98, 0.05, f'Korelasi Pearson (r): {corr_r:.3f}\n(Korelasi Lemah: Kursi kosong tidak semata karena mahasiswa mundur)',
                ha='right', va='bottom', fontsize=9.5, fontweight='bold', color='#4338CA',
                transform=ax.transAxes,
                bbox=dict(boxstyle='round,pad=0.5', facecolor='#EEF2FF', edgecolor='#A5B4FC', alpha=0.95))

    ax.set_xlim(0, 50)
    ax.set_ylim(25, 106)
    ax.set_xlabel('Tingkat Kebocoran / Drop-out Rate (%) [Peserta Mundur / Lulus Seleksi]', fontsize=11, fontweight='bold', color='#1E293B', labelpad=8)
    ax.set_ylabel('Rata-rata Keterisian Kuota (Fill Rate 5 Tahun) (%)', fontsize=11, fontweight='bold', color='#1E293B', labelpad=8)

    ax.grid(True, linestyle=':', alpha=0.4, color='#94A3B8', zorder=0)
    for sp in ['top', 'right']:
        ax.spines[sp].set_visible(False)

    # Legend for bubble sizes (placed top-right with no overlap)
    for dt_sample, lbl in [(50, '50 kursi'), (150, '150 kursi'), (250, '250 kursi')]:
        s_sz = 60 + (dt_sample / df_sc['DT'].max()) * 260
        ax.scatter([], [], s=s_sz, c='#94A3B8', edgecolors='#0F172A', label=lbl)
    ax.legend(loc='upper right', bbox_to_anchor=(0.99, 0.97), title='Daya Tampung Rata-rata',
              frameon=True, fontsize=8.5, title_fontsize=9, facecolor='#FFFFFF', edgecolor='#CBD5E1')

    fig.suptitle('MATRIKS KORELASI: TINGKAT KEBOCORAN vs KETERISIAN KUOTA PRODI S1 USK (2022–2026)\n'
                 'Memisahkan Masalah Drop-out Peserta Lulus dari Masalah Minimnya Minat Pelamar di Awal',
                 fontsize=14, fontweight='bold', color='#0F172A', y=0.98)

    plt.tight_layout(rect=[0.02, 0.02, 0.98, 0.93])
    plt.savefig(os.path.join(chart_dir, "A5_scatter_kebocoran_vs_fill_rate.png"), dpi=300)
    plt.close()
    print("  Done A5_scatter")

    print("\n[SUKSES] Seluruh 5 Visualisasi Tambahan Selesai Dibuat!")

if __name__ == '__main__':
    main()
