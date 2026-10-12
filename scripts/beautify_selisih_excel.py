#!/usr/bin/env python3
"""
beautify_selisih_excel.py
=============================================================================
PEMBERSIH & PENATA TAMPILAN EXCEL REKAPITULASI SELISIH LULUS VS DAFTAR ULANG
=============================================================================
Skrip ini menata ulang file Excel:
data/processed/rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx

Menghasilkan format standar korporat / eksekutif:
1. Sheet 'Ringkasan_Eksekutif': Dashboard KPI cards, tren tahunan, ranking fakultas,
   serta Top 10 prodi paling bocor vs paling setia.
2. Sheet 'Rincian_Per_Prodi': Multi-tier header (Identitas, 2022, 2023, 2024, 2025, 2026,
   Total 5 Tahun), zebra striping, conditional highlighting, formula dinamis,
   baris Grand Total, dan freeze panes.
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_beautified_selisih_excel():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    file_path = os.path.join(repo_dir, "data", "processed", "rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx")
    
    if not os.path.exists(file_path):
        print(f"Error: File tidak ditemukan di {file_path}")
        return

    print("Membaca data sumber dari:", file_path)
    df_raw = pd.read_excel(file_path, sheet_name=0)

    # Inisialisasi Workbook baru
    wb = openpyxl.Workbook()
    wb.remove(wb.active) # Hapus sheet default

    # -------------------------------------------------------------------------
    # PALET WARNA & TIPOGRAFI STANDAR KORPORAT EKSEKUTIF
    # -------------------------------------------------------------------------
    FONT_FAMILY = "Segoe UI"
    
    # Warna Kategori & Header
    NAVY_MAIN      = "0D233A"  # Title Banner Navy Gelap
    SLATE_TITLE    = "1E293B"  # Subtitle Slate
    NAVY_2022      = "1E3A8A"  # Biru Tua 2022
    CYAN_2023      = "0369A1"  # Cyan Tua 2023
    GREEN_2024     = "15803D"  # Emerald 2024
    AMBER_2025     = "B45309"  # Amber 2025
    PURPLE_2026    = "6D28D9"  # Deep Purple 2026
    DARK_5THN      = "0F172A"  # Dark Slate Agregat 5 Tahun
    
    # Warna Sub-Header
    SUB_ID         = "334155"
    SUB_2022       = "2563EB"
    SUB_2023       = "0284C7"
    SUB_2024       = "16A34A"
    SUB_2025       = "D97706"
    SUB_2026       = "7C3AED"
    SUB_5THN       = "1E293B"

    # Warna Baris Data & Alert
    WHITE          = "FFFFFF"
    ICE_ROW        = "F8FAFC"  # Zebra Striping Lembut
    BORDER_LIGHT   = "E2E8F0"  # Garis Tabel Halus
    BORDER_DIVIDER = "94A3B8"  # Garis Vertikal Pemisah Antar-Tahun
    TOTAL_ROW_BG   = "0F172A"  # Grand Total Row
    
    # Alert Kebocoran
    ALERT_RED_BG   = "FEE2E2"  # Gugur >= 30%
    ALERT_RED_FG   = "991B1B"
    GOOD_GRN_BG    = "DCFCE7"  # Gugur <= 10%
    GOOD_GRN_FG    = "166534"
    CARD_BG_1      = "EFF6FF"  # Soft Blue Card
    CARD_BG_2      = "F0FDF4"  # Soft Green Card
    CARD_BG_3      = "FEF2F2"  # Soft Red Card
    CARD_BG_4      = "FFFBEB"  # Soft Amber Card

    # Gaya Border
    thin_light = Side(style='thin', color=BORDER_LIGHT)
    border_cell = Border(left=thin_light, right=thin_light, top=thin_light, bottom=thin_light)
    border_cell_divider = Border(left=thin_light, right=Side(style='medium', color=BORDER_DIVIDER), top=thin_light, bottom=thin_light)
    border_total = Border(
        left=thin_light, right=thin_light,
        top=Side(style='thin', color='FFFFFF'),
        bottom=Side(style='double', color='FFFFFF')
    )
    border_total_divider = Border(
        left=thin_light, right=Side(style='medium', color='FFFFFF'),
        top=Side(style='thin', color='FFFFFF'),
        bottom=Side(style='double', color='FFFFFF')
    )
    border_card = Border(
        left=Side(style='thin', color='CBD5E1'),
        right=Side(style='thin', color='CBD5E1'),
        top=Side(style='thin', color='CBD5E1'),
        bottom=Side(style='thin', color='CBD5E1')
    )

    # Gaya Font
    font_banner_title = Font(name=FONT_FAMILY, size=13, bold=True, color='FFFFFF')
    font_banner_sub   = Font(name=FONT_FAMILY, size=9.5, italic=True, color='E2E8F0')
    font_tier1        = Font(name=FONT_FAMILY, size=10, bold=True, color='FFFFFF')
    font_tier1_gold   = Font(name=FONT_FAMILY, size=10, bold=True, color='FDE68A')
    font_tier2        = Font(name=FONT_FAMILY, size=9, bold=True, color='FFFFFF')
    font_cell         = Font(name=FONT_FAMILY, size=9, color='0F172A')
    font_cell_bold    = Font(name=FONT_FAMILY, size=9, bold=True, color='0F172A')
    font_cell_alert   = Font(name=FONT_FAMILY, size=9, bold=True, color=ALERT_RED_FG)
    font_cell_good    = Font(name=FONT_FAMILY, size=9, bold=True, color=GOOD_GRN_FG)
    font_total        = Font(name=FONT_FAMILY, size=9.5, bold=True, color='FFFFFF')
    font_total_gold   = Font(name=FONT_FAMILY, size=9.5, bold=True, color='FDE68A')

    # Alignments
    al_center      = Alignment(horizontal='center', vertical='center')
    al_left        = Alignment(horizontal='left', vertical='center')
    al_right       = Alignment(horizontal='right', vertical='center')
    al_wrap_center = Alignment(horizontal='center', vertical='center', wrap_text=True)

    # Number Formats
    FMT_QTY = '#,##0;(#,##0);"-"'
    FMT_PCT = '0.0"%"'

    # =========================================================================
    # SHEET 1: RINGKASAN EKSEKUTIF (EXECUTIVE DASHBOARD)
    # =========================================================================
    print("Membangun Sheet 1: Ringkasan_Eksekutif...")
    ws1 = wb.create_sheet(title="Ringkasan_Eksekutif")
    ws1.views.sheetView[0].showGridLines = True

    # 1. Title Banner
    ws1.merge_cells("A1:K1")
    ws1.merge_cells("A2:K2")
    ws1.row_dimensions[1].height = 28
    ws1.row_dimensions[2].height = 20

    c1 = ws1["A1"]
    c1.value = "UNIVERSITAS SYIAH KUALA — DASHBOARD EKSEKUTIF KEBOCORAN KELULUSAN PMB (2022–2026)"
    c1.font = font_banner_title
    c1.fill = PatternFill(start_color=NAVY_MAIN, end_color=NAVY_MAIN, fill_type='solid')
    c1.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    c2 = ws1["A2"]
    c2.value = "Sintesis Longitudinal Disparitas Kelulusan Seleksi vs Registrasi Ulang Riil Mahasiswa Baru (Seluruh Jalur Masuk)"
    c2.font = font_banner_sub
    c2.fill = PatternFill(start_color=SLATE_TITLE, end_color=SLATE_TITLE, fill_type='solid')
    c2.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    ws1.row_dimensions[3].height = 10 # Spacer

    # Hitung Agregat untuk KPI Cards
    tot_lulus_5y = int(df_raw['Total_Lulus_5Thn'].sum())
    tot_du_5y    = int(df_raw['Total_DU_5Thn'].sum())
    tot_gugur_5y = int(df_raw['Total_Gugur_5Thn'].sum())
    pct_gugur_5y = (tot_gugur_5y / tot_lulus_5y * 100) if tot_lulus_5y > 0 else 0
    pct_yield_5y = (tot_du_5y / tot_lulus_5y * 100) if tot_lulus_5y > 0 else 0

    # 2. KPI Cards (Baris 4–6)
    cards = [
        ("A", "C", "TOTAL LULUS SELEKSI (5 TAHUN)", f"{tot_lulus_5y:,}", "Calon Mahasiswa Dinyatakan Lulus", CARD_BG_1, "1E3A8A"),
        ("D", "F", "TOTAL REGISTRASI ULANG (DU)", f"{tot_du_5y:,}", f"Tingkat Konversi (Yield Rate): {pct_yield_5y:.1f}%", CARD_BG_2, "166534"),
        ("G", "I", "TOTAL GUGUR / TIDAK REGISTRASI", f"{tot_gugur_5y:,}", "Kursi Ditinggalkan / Menolak Lolos", CARD_BG_3, "991B1B"),
        ("J", "K", "RATA-RATA % GUGUR USK", f"{pct_gugur_5y:.1f}%", "Defisit Konversi Calon Mahasiswa", CARD_BG_4, "B45309")
    ]

    ws1.row_dimensions[4].height = 18
    ws1.row_dimensions[5].height = 28
    ws1.row_dimensions[6].height = 18

    for c_start, c_end, title, val, sub, bg, fg in cards:
        ws1.merge_cells(f"{c_start}4:{c_end}4")
        ws1.merge_cells(f"{c_start}5:{c_end}5")
        ws1.merge_cells(f"{c_start}6:{c_end}6")
        
        # Title
        top = ws1[f"{c_start}4"]
        top.value = title
        top.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="64748B")
        top.alignment = al_center
        top.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')

        # Value
        mid = ws1[f"{c_start}5"]
        mid.value = val
        mid.font = Font(name=FONT_FAMILY, size=16, bold=True, color=fg)
        mid.alignment = al_center
        mid.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')

        # Subtitle
        bot = ws1[f"{c_start}6"]
        bot.value = sub
        bot.font = Font(name=FONT_FAMILY, size=8, italic=True, color="475569")
        bot.alignment = al_center
        bot.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')

        # Apply borders to card cells
        start_idx = openpyxl.utils.column_index_from_string(c_start)
        end_idx = openpyxl.utils.column_index_from_string(c_end)
        for r in range(4, 7):
            for c in range(start_idx, end_idx + 1):
                ws1.cell(r, c).border = border_card
                ws1.cell(r, c).fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')

    ws1.row_dimensions[7].height = 14 # Spacer

    # 3. TABEL 1: TREN TAHUNAN KEBOCORAN USK (Baris 8–15)
    ws1.merge_cells("A8:G8")
    t1_title = ws1["A8"]
    t1_title.value = "Tabel 1: Rekapitulasi Tahunan Dinamika Kelulusan vs Registrasi Ulang (2022–2026)"
    t1_title.font = Font(name=FONT_FAMILY, size=10.5, bold=True, color=NAVY_MAIN)
    ws1.row_dimensions[8].height = 22

    t1_headers = ["Tahun Akademik", "Total Lulus Seleksi", "Daftar Ulang (DU)", "Selisih Gugur", "% Gugur (Bocor)", "% Yield Rate", "Status Efisiensi"]
    ws1.row_dimensions[9].height = 22
    for i, h in enumerate(t1_headers, 1):
        cell = ws1.cell(9, i)
        cell.value = h
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=NAVY_MAIN, end_color=NAVY_MAIN, fill_type='solid')
        cell.alignment = al_center
        cell.border = border_cell

    years = [2022, 2023, 2024, 2025, 2026]
    for idx, yr in enumerate(years, 10):
        tot_l = int(df_raw[f'Lulus_{yr}'].sum())
        tot_d = int(df_raw[f'DU_{yr}'].sum())
        tot_g = int(df_raw[f'Selisih_Gugur_{yr}'].sum())
        pct_g = (tot_g / tot_l * 100) if tot_l > 0 else 0
        pct_y = (tot_d / tot_l * 100) if tot_l > 0 else 0
        status = "Optimal" if pct_g <= 16.5 else ("Moderat" if pct_g <= 18.0 else "Waspada")

        row_data = [yr, tot_l, tot_d, tot_g, pct_g, pct_y, status]
        ws1.row_dimensions[idx].height = 20
        bg_row = ICE_ROW if idx % 2 == 1 else WHITE
        
        for c_i, val in enumerate(row_data, 1):
            c_cell = ws1.cell(idx, c_i)
            c_cell.value = val
            c_cell.font = font_cell
            c_cell.fill = PatternFill(start_color=bg_row, end_color=bg_row, fill_type='solid')
            c_cell.border = border_cell
            
            if c_i == 1:
                c_cell.alignment = al_center
                c_cell.font = font_cell_bold
            elif c_i in [2, 3, 4]:
                c_cell.alignment = al_right
                c_cell.number_format = FMT_QTY
            elif c_i in [5, 6]:
                c_cell.alignment = al_right
                c_cell.number_format = FMT_PCT
                if c_i == 5 and val >= 18.0:
                    c_cell.font = font_cell_alert
                    c_cell.fill = PatternFill(start_color=ALERT_RED_BG, end_color=ALERT_RED_BG, fill_type='solid')
            elif c_i == 7:
                c_cell.alignment = al_center
                if status == "Optimal":
                    c_cell.font = font_cell_good
                elif status == "Waspada":
                    c_cell.font = font_cell_alert

    # Grand Total Baris Tabel 1 (Row 15)
    row_tot = 15
    ws1.row_dimensions[row_tot].height = 22
    t1_tot = ["TOTAL 5 TAHUN", tot_lulus_5y, tot_du_5y, tot_gugur_5y, pct_gugur_5y, pct_yield_5y, "17.2% Rata-rata"]
    for c_i, val in enumerate(t1_tot, 1):
        c_cell = ws1.cell(row_tot, c_i)
        c_cell.value = val
        c_cell.font = font_total if c_i != 5 else font_total_gold
        c_cell.fill = PatternFill(start_color=TOTAL_ROW_BG, end_color=TOTAL_ROW_BG, fill_type='solid')
        c_cell.border = border_total
        if c_i == 1:
            c_cell.alignment = al_center
        elif c_i in [2, 3, 4]:
            c_cell.alignment = al_right
            c_cell.number_format = FMT_QTY
        elif c_i in [5, 6]:
            c_cell.alignment = al_right
            c_cell.number_format = FMT_PCT
        else:
            c_cell.alignment = al_center

    ws1.row_dimensions[16].height = 14 # Spacer

    # 4. TABEL 2: PERINGKAT KEBOCORAN FAKULTAS (Baris 17–31)
    ws1.merge_cells("A17:G17")
    t2_title = ws1["A17"]
    t2_title.value = "Tabel 2: Peringkat Disparitas Kelulusan vs Registrasi Ulang per Fakultas (5 Tahun)"
    t2_title.font = Font(name=FONT_FAMILY, size=10.5, bold=True, color=NAVY_MAIN)
    ws1.row_dimensions[17].height = 22

    t2_headers = ["Peringkat", "Fakultas / Unit", "Jumlah Prodi", "Total Lulus", "Total DU", "Total Gugur", "% Gugur (Bocor)"]
    ws1.row_dimensions[18].height = 22
    for i, h in enumerate(t2_headers, 1):
        cell = ws1.cell(18, i)
        cell.value = h
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=SUB_ID, end_color=SUB_ID, fill_type='solid')
        cell.alignment = al_center
        cell.border = border_cell

    # Agregasi Fakultas
    fak_df = df_raw.groupby('Fakultas').agg(
        Jumlah_Prodi=('Nama Program Studi', 'count'),
        Total_Lulus=('Total_Lulus_5Thn', 'sum'),
        Total_DU=('Total_DU_5Thn', 'sum'),
        Total_Gugur=('Total_Gugur_5Thn', 'sum')
    ).reset_index()
    fak_df['Persen_Gugur'] = (fak_df['Total_Gugur'] / fak_df['Total_Lulus'] * 100).round(1)
    fak_df = fak_df.sort_values('Persen_Gugur', ascending=False).reset_index(drop=True)

    for rank, r_data in fak_df.iterrows():
        r_idx = 19 + rank
        ws1.row_dimensions[r_idx].height = 20
        bg_row = ICE_ROW if rank % 2 == 1 else WHITE

        ws1.cell(r_idx, 1, rank + 1).alignment = al_center
        ws1.cell(r_idx, 2, r_data['Fakultas']).alignment = al_left
        ws1.cell(r_idx, 3, r_data['Jumlah_Prodi']).alignment = al_center
        ws1.cell(r_idx, 4, r_data['Total_Lulus']).alignment = al_right
        ws1.cell(r_idx, 5, r_data['Total_DU']).alignment = al_right
        ws1.cell(r_idx, 6, r_data['Total_Gugur']).alignment = al_right
        
        pct_cell = ws1.cell(r_idx, 7, r_data['Persen_Gugur'])
        pct_cell.alignment = al_right
        pct_cell.number_format = FMT_PCT

        for c_i in range(1, 8):
            c_c = ws1.cell(r_idx, c_i)
            c_c.font = font_cell
            c_c.fill = PatternFill(start_color=bg_row, end_color=bg_row, fill_type='solid')
            c_c.border = border_cell
            if c_i in [4, 5, 6]:
                c_c.number_format = FMT_QTY

        if r_data['Persen_Gugur'] >= 22.0:
            pct_cell.font = font_cell_alert
            pct_cell.fill = PatternFill(start_color=ALERT_RED_BG, end_color=ALERT_RED_BG, fill_type='solid')
        elif r_data['Persen_Gugur'] <= 13.0:
            pct_cell.font = font_cell_good
            pct_cell.fill = PatternFill(start_color=GOOD_GRN_BG, end_color=GOOD_GRN_BG, fill_type='solid')

    ws1.row_dimensions[32].height = 14 # Spacer

    # 5. TABEL 3 & TABEL 4: TOP 10 PRODI PALING BOCOR VS PALING SETIA (Side-by-Side)
    # Filter prodi yang aktif (Total Lulus >= 50)
    valid_df = df_raw[df_raw['Total_Lulus_5Thn'] >= 50].copy()
    top_bocor = valid_df.sort_values('Rata_Persen_Gugur_5Thn', ascending=False).head(10).reset_index(drop=True)
    top_setia = valid_df.sort_values('Rata_Persen_Gugur_5Thn', ascending=True).head(10).reset_index(drop=True)

    ws1.merge_cells("A33:E33")
    t3_title = ws1["A33"]
    t3_title.value = "⚠️ Top 10 Program Studi Kebocoran Tertinggi (% Gugur)"
    t3_title.font = Font(name=FONT_FAMILY, size=10, bold=True, color=ALERT_RED_FG)

    ws1.merge_cells("G33:K33")
    t4_title = ws1["G33"]
    t4_title.value = "🏆 Top 10 Program Studi Paling Loyal / Setia (Terendah Gugur)"
    t4_title.font = Font(name=FONT_FAMILY, size=10, bold=True, color=GOOD_GRN_FG)
    ws1.row_dimensions[33].height = 22

    # Headers Top 10
    t34_h = ["No", "Program Studi", "Fakultas", "Total Gugur", "% Gugur"]
    ws1.row_dimensions[34].height = 20
    for i, h in enumerate(t34_h, 1):
        # Kiri (Bocor)
        c_kiri = ws1.cell(34, i)
        c_kiri.value = h
        c_kiri.font = font_tier2
        c_kiri.fill = PatternFill(start_color=ALERT_RED_FG, end_color=ALERT_RED_FG, fill_type='solid')
        c_kiri.alignment = al_center
        c_kiri.border = border_cell
        
        # Kanan (Setia)
        c_kanan = ws1.cell(34, i + 6)
        c_kanan.value = h
        c_kanan.font = font_tier2
        c_kanan.fill = PatternFill(start_color=GOOD_GRN_FG, end_color=GOOD_GRN_FG, fill_type='solid')
        c_kanan.alignment = al_center
        c_kanan.border = border_cell

    for k in range(10):
        r_k = 35 + k
        ws1.row_dimensions[r_k].height = 19
        bg_k = ICE_ROW if k % 2 == 1 else WHITE

        # Isi Kiri (Bocor)
        rb = top_bocor.iloc[k]
        ws1.cell(r_k, 1, k + 1).alignment = al_center
        ws1.cell(r_k, 2, rb['Nama Program Studi']).alignment = al_left
        ws1.cell(r_k, 3, rb['Fakultas']).alignment = al_left
        ws1.cell(r_k, 4, rb['Total_Gugur_5Thn']).alignment = al_right
        cb = ws1.cell(r_k, 5, rb['Rata_Persen_Gugur_5Thn'])
        cb.alignment = al_right
        cb.number_format = FMT_PCT
        cb.font = font_cell_alert
        cb.fill = PatternFill(start_color=ALERT_RED_BG, end_color=ALERT_RED_BG, fill_type='solid')

        for ci in range(1, 5):
            cc = ws1.cell(r_k, ci)
            cc.font = font_cell
            cc.fill = PatternFill(start_color=bg_k, end_color=bg_k, fill_type='solid')
            cc.border = border_cell
            if ci == 4:
                cc.number_format = FMT_QTY
        ws1.cell(r_k, 5).border = border_cell

        # Isi Kanan (Setia)
        rs = top_setia.iloc[k]
        ws1.cell(r_k, 7, k + 1).alignment = al_center
        ws1.cell(r_k, 8, rs['Nama Program Studi']).alignment = al_left
        ws1.cell(r_k, 9, rs['Fakultas']).alignment = al_left
        ws1.cell(r_k, 10, rs['Total_Gugur_5Thn']).alignment = al_right
        cs = ws1.cell(r_k, 11, rs['Rata_Persen_Gugur_5Thn'])
        cs.alignment = al_right
        cs.number_format = FMT_PCT
        cs.font = font_cell_good
        cs.fill = PatternFill(start_color=GOOD_GRN_BG, end_color=GOOD_GRN_BG, fill_type='solid')

        for ci in range(7, 11):
            cc = ws1.cell(r_k, ci)
            cc.font = font_cell
            cc.fill = PatternFill(start_color=bg_k, end_color=bg_k, fill_type='solid')
            cc.border = border_cell
            if ci == 10:
                cc.number_format = FMT_QTY
        ws1.cell(r_k, 11).border = border_cell

    # Column Widths Sheet 1
    ws1_widths = {
        'A': 6, 'B': 30, 'C': 16, 'D': 15, 'E': 14,
        'F': 14, 'G': 6, 'H': 30, 'I': 16, 'J': 15, 'K': 14
    }
    for col_letter, width in ws1_widths.items():
        ws1.column_dimensions[col_letter].width = width

    # =========================================================================
    # SHEET 2: RINCIAN PER PRODI (MULTI-TIER FULL MASTER TABLE)
    # =========================================================================
    print("Membangun Sheet 2: Rincian_Per_Prodi...")
    ws2 = wb.create_sheet(title="Rincian_Per_Prodi")
    ws2.views.sheetView[0].showGridLines = True

    # 1. Title Banner
    ws2.merge_cells("A1:AB1")
    ws2.merge_cells("A2:AB2")
    ws2.row_dimensions[1].height = 28
    ws2.row_dimensions[2].height = 20

    t2_c1 = ws2["A1"]
    t2_c1.value = "UNIVERSITAS SYIAH KUALA — REKAPITULASI LENGKAP SELISIH LULUS VS DAFTAR ULANG PER PROGRAM STUDI (2022–2026)"
    t2_c1.font = font_banner_title
    t2_c1.fill = PatternFill(start_color=NAVY_MAIN, end_color=NAVY_MAIN, fill_type='solid')
    t2_c1.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    t2_c2 = ws2["A2"]
    t2_c2.value = "Rincian Data Longitudinal 81 Program Studi Jenjang S1, D3, dan PSDKU Gayo Lues | Selisih Gugur = Lulus - DU"
    t2_c2.font = font_banner_sub
    t2_c2.fill = PatternFill(start_color=SLATE_TITLE, end_color=SLATE_TITLE, fill_type='solid')
    t2_c2.alignment = Alignment(horizontal='left', vertical='center', indent=1)

    ws2.row_dimensions[3].height = 8 # Spacer

    # 2. Multi-Tier Header (Baris 4 & 5)
    # Tier 1 (Kategori & Tahun)
    tier1_sections = [
        ("A", "D", "IDENTITAS PROGRAM STUDI", SUB_ID, False),
        ("E", "H", "TAHUN AKADEMIK 2022", NAVY_2022, False),
        ("I", "L", "TAHUN AKADEMIK 2023", CYAN_2023, False),
        ("M", "P", "TAHUN AKADEMIK 2024", GREEN_2024, False),
        ("Q", "T", "TAHUN AKADEMIK 2025", AMBER_2025, False),
        ("U", "X", "TAHUN AKADEMIK 2026", PURPLE_2026, False),
        ("Y", "AB", "TOTAL 5 TAHUN (2022–2026)", DARK_5THN, True),
    ]

    ws2.row_dimensions[4].height = 26
    ws2.row_dimensions[5].height = 26

    for c_start, c_end, label, bg, is_gold in tier1_sections:
        ws2.merge_cells(f"{c_start}4:{c_end}4")
        t_cell = ws2[f"{c_start}4"]
        t_cell.value = label
        t_cell.font = font_tier1_gold if is_gold else font_tier1
        t_cell.alignment = al_center
        
        s_idx = openpyxl.utils.column_index_from_string(c_start)
        e_idx = openpyxl.utils.column_index_from_string(c_end)
        for ci in range(s_idx, e_idx + 1):
            cell = ws2.cell(4, ci)
            cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')
            # Outer vertical divider border
            if ci == e_idx and ci != 28:
                cell.border = Border(left=thin_light, right=Side(style='medium', color=BORDER_DIVIDER), top=thin_light, bottom=thin_light)
            else:
                cell.border = border_cell

    # Tier 2 (Nama Kolom)
    tier2_cols = [
        # Identitas (1-4)
        ("No", SUB_ID), ("Fakultas", SUB_ID), ("Nama Program Studi", SUB_ID), ("Jenjang", SUB_ID),
        # 2022 (5-8)
        ("Lulus", SUB_2022), ("Daftar Ulang", SUB_2022), ("Gugur", SUB_2022), ("% Gugur", SUB_2022),
        # 2023 (9-12)
        ("Lulus", SUB_2023), ("Daftar Ulang", SUB_2023), ("Gugur", SUB_2023), ("% Gugur", SUB_2023),
        # 2024 (13-16)
        ("Lulus", SUB_2024), ("Daftar Ulang", SUB_2024), ("Gugur", SUB_2024), ("% Gugur", SUB_2024),
        # 2025 (17-20)
        ("Lulus", SUB_2025), ("Daftar Ulang", SUB_2025), ("Gugur", SUB_2025), ("% Gugur", SUB_2025),
        # 2026 (21-24)
        ("Lulus", SUB_2026), ("Daftar Ulang", SUB_2026), ("Gugur", SUB_2026), ("% Gugur", SUB_2026),
        # Total 5 Thn (25-28)
        ("Total Lulus", SUB_5THN), ("Total DU", SUB_5THN), ("Total Gugur", SUB_5THN), ("Rata % Gugur", SUB_5THN),
    ]

    divider_cols = [4, 8, 12, 16, 20, 24, 28]

    for ci, (col_name, col_bg) in enumerate(tier2_cols, 1):
        cell = ws2.cell(5, ci)
        cell.value = col_name
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=col_bg, end_color=col_bg, fill_type='solid')
        cell.alignment = al_center
        if ci in divider_cols and ci != 28:
            cell.border = Border(left=thin_light, right=Side(style='medium', color=BORDER_DIVIDER), top=thin_light, bottom=thin_light)
        else:
            cell.border = border_cell

    # 3. Data Rows dengan Rumus Excel Dinamis
    start_row = 6
    num_prodi = len(df_raw)

    for i, row in df_raw.iterrows():
        cur_row = start_row + i
        ws2.row_dimensions[cur_row].height = 20
        bg_row = ICE_ROW if i % 2 == 1 else WHITE

        # A: No
        ws2.cell(cur_row, 1, i + 1).alignment = al_center
        # B: Fakultas
        ws2.cell(cur_row, 2, str(row['Fakultas'])).alignment = al_left
        # C: Nama Program Studi
        ws2.cell(cur_row, 3, str(row['Nama Program Studi'])).alignment = al_left
        # D: Jenjang
        ws2.cell(cur_row, 4, str(row['Jenjang'])).alignment = al_center

        # Data Tahunan dengan Rumus
        # 2022: E, F, G, H
        ws2.cell(cur_row, 5, int(row['Lulus_2022']))
        ws2.cell(cur_row, 6, int(row['DU_2022']))
        ws2.cell(cur_row, 7, f"=E{cur_row}-F{cur_row}")
        ws2.cell(cur_row, 8, f"=IF(E{cur_row}>0, (G{cur_row}/E{cur_row})*100, 0)")

        # 2023: I, J, K, L
        ws2.cell(cur_row, 9, int(row['Lulus_2023']))
        ws2.cell(cur_row, 10, int(row['DU_2023']))
        ws2.cell(cur_row, 11, f"=I{cur_row}-J{cur_row}")
        ws2.cell(cur_row, 12, f"=IF(I{cur_row}>0, (K{cur_row}/I{cur_row})*100, 0)")

        # 2024: M, N, O, P
        ws2.cell(cur_row, 13, int(row['Lulus_2024']))
        ws2.cell(cur_row, 14, int(row['DU_2024']))
        ws2.cell(cur_row, 15, f"=M{cur_row}-N{cur_row}")
        ws2.cell(cur_row, 16, f"=IF(M{cur_row}>0, (O{cur_row}/M{cur_row})*100, 0)")

        # 2025: Q, R, S, T
        ws2.cell(cur_row, 17, int(row['Lulus_2025']))
        ws2.cell(cur_row, 18, int(row['DU_2025']))
        ws2.cell(cur_row, 19, f"=Q{cur_row}-R{cur_row}")
        ws2.cell(cur_row, 20, f"=IF(Q{cur_row}>0, (S{cur_row}/Q{cur_row})*100, 0)")

        # 2026: U, V, W, X
        ws2.cell(cur_row, 21, int(row['Lulus_2026']))
        ws2.cell(cur_row, 22, int(row['DU_2026']))
        ws2.cell(cur_row, 23, f"=U{cur_row}-V{cur_row}")
        ws2.cell(cur_row, 24, f"=IF(U{cur_row}>0, (W{cur_row}/U{cur_row})*100, 0)")

        # Total 5 Thn: Y, Z, AA, AB
        ws2.cell(cur_row, 25, f"=E{cur_row}+I{cur_row}+M{cur_row}+Q{cur_row}+U{cur_row}")
        ws2.cell(cur_row, 26, f"=F{cur_row}+J{cur_row}+N{cur_row}+R{cur_row}+V{cur_row}")
        ws2.cell(cur_row, 27, f"=G{cur_row}+K{cur_row}+O{cur_row}+S{cur_row}+W{cur_row}")
        ws2.cell(cur_row, 28, f"=IF(Y{cur_row}>0, (AA{cur_row}/Y{cur_row})*100, 0)")

        # Nilai acuan untuk visual alert (dari data mentah)
        pct_5y = float(row['Rata_Persen_Gugur_5Thn']) if pd.notnull(row['Rata_Persen_Gugur_5Thn']) else 0.0

        for ci in range(1, 29):
            cell = ws2.cell(cur_row, ci)
            cell.font = font_cell
            cell.fill = PatternFill(start_color=bg_row, end_color=bg_row, fill_type='solid')
            
            # Border
            if ci in divider_cols and ci != 28:
                cell.border = border_cell_divider
            else:
                cell.border = border_cell

            # Number Formatting & Alignment
            if ci in [5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26, 27]:
                cell.alignment = al_right
                cell.number_format = FMT_QTY
            elif ci in [8, 12, 16, 20, 24, 28]:
                cell.alignment = al_right
                cell.number_format = FMT_PCT

        # Conditional Highlight di Kolom 28 (Rata-rata 5 Tahun)
        cell_28 = ws2.cell(cur_row, 28)
        if pct_5y >= 30.0 and int(row['Total_Lulus_5Thn']) >= 50:
            cell_28.font = font_cell_alert
            cell_28.fill = PatternFill(start_color=ALERT_RED_BG, end_color=ALERT_RED_BG, fill_type='solid')
        elif pct_5y <= 10.0 and int(row['Total_Lulus_5Thn']) >= 50:
            cell_28.font = font_cell_good
            cell_28.fill = PatternFill(start_color=GOOD_GRN_BG, end_color=GOOD_GRN_BG, fill_type='solid')

    # 4. Baris Grand Total Universitas (Row 87)
    tot_row = start_row + num_prodi
    ws2.row_dimensions[tot_row].height = 24

    ws2.merge_cells(f"A{tot_row}:D{tot_row}")
    lbl_tot = ws2[f"A{tot_row}"]
    lbl_tot.value = "TOTAL UNIVERSITAS SYIAH KUALA"
    lbl_tot.font = font_total
    lbl_tot.alignment = Alignment(horizontal='center', vertical='center')

    # Rumus Total Tahunan
    qty_cols = [
        (5, 'E'), (6, 'F'), (7, 'G'),
        (9, 'I'), (10, 'J'), (11, 'K'),
        (13, 'M'), (14, 'N'), (15, 'O'),
        (17, 'Q'), (18, 'R'), (19, 'S'),
        (21, 'U'), (22, 'V'), (23, 'W'),
        (25, 'Y'), (26, 'Z'), (27, 'AA')
    ]
    for ci, letter in qty_cols:
        c = ws2.cell(tot_row, ci)
        c.value = f"=SUM({letter}6:{letter}{tot_row-1})"
        c.alignment = al_right
        c.number_format = FMT_QTY
        c.font = font_total

    # Rumus Persen Total
    pct_cols = [
        (8, 'G', 'E'),
        (12, 'K', 'I'),
        (16, 'O', 'M'),
        (20, 'S', 'Q'),
        (24, 'W', 'U'),
        (28, 'AA', 'Y')
    ]
    for ci, g_col, l_col in pct_cols:
        c = ws2.cell(tot_row, ci)
        c.value = f"=IF({l_col}{tot_row}>0, ({g_col}{tot_row}/{l_col}{tot_row})*100, 0)"
        c.alignment = al_right
        c.number_format = FMT_PCT
        c.font = font_total_gold if ci == 28 else font_total

    # Apply fills & borders to total row
    for ci in range(1, 29):
        c = ws2.cell(tot_row, ci)
        c.fill = PatternFill(start_color=TOTAL_ROW_BG, end_color=TOTAL_ROW_BG, fill_type='solid')
        if ci in divider_cols and ci != 28:
            c.border = border_total_divider
        else:
            c.border = border_total

    # 5. Freeze Panes & Lebar Kolom
    # Freeze row 5 and col A-D
    ws2.freeze_panes = "E6"

    # Lebar Kolom Optimal
    col_widths = {
        'A': 6,   # No
        'B': 24,  # Fakultas
        'C': 38,  # Nama Program Studi (long text bebas terpotong)
        'D': 10,  # Jenjang
    }
    # Kolom Angka (E s.d. AB)
    for ci in range(5, 29):
        letter = get_column_letter(ci)
        if ci in [8, 12, 16, 20, 24, 28]:
            col_widths[letter] = 12.5 # Persen
        else:
            col_widths[letter] = 12.0 # Qty

    for letter, w in col_widths.items():
        ws2.column_dimensions[letter].width = w

    # Simpan File Hasil Polishing
    print("Menyimpan file hasil perbaikan ke:", file_path)
    wb.save(file_path)
    print("✔ Berhasil! Tampilan Excel rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx telah diperbarui secara profesional.")

if __name__ == "__main__":
    build_beautified_selisih_excel()
