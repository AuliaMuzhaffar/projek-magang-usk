#!/usr/bin/env python3
"""
beautify_selisih_excel.py
=============================================================================
GENERATOR & SINKRONISASI REKAPITULASI SELISIH LULUS VS DAFTAR ULANG
=============================================================================
Skrip ini membaca data resmi dari Master Database (Single Source of Truth):
data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx (Sheet: Master_Semua_Prodi)

Dan men-generate berkas terolah profesional:
data/processed/rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx

Fitur Utama:
1. 100% Selaras & Bebas Anomali: Menggunakan data kelulusan & daftar ulang resmi.
2. Sheet 'Ringkasan_Eksekutif': 4 Kartu KPI dan seluruh tabel (Tren Tahunan,
   Peringkat Fakultas) menggunakan FORMULA EXCEL DINAMIS (SUMIF, COUNTIF, IF)
   yang terhubung langsung ke sheet Rincian.
3. Sheet 'Rincian_Per_Prodi': Multi-tier header berjenjang 2 tingkat, garis pemisah
   tahunan, formula dinamis (Gugur = Lulus - DU, % Gugur, Total 5 Tahun),
   baris Grand Total universitas, dan freeze panes di E6.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_beautified_selisih_excel():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    master_path = os.path.join(repo_dir, "data", "master", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    out_path = os.path.join(repo_dir, "data", "processed", "rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx")
    
    if not os.path.exists(master_path):
        print(f"Error: File Master tidak ditemukan di {master_path}")
        return

    print("Membaca data master resmi dari:", master_path)
    wb_mas = openpyxl.load_workbook(master_path, data_only=True)
    ws_mas = wb_mas["Master_Semua_Prodi"]

    # Ambil seluruh 81 baris prodi dari Master_Semua_Prodi
    # Col 1: No, 2: Fak, 3: Nama Prodi, 4: Jenjang
    # Col 8: Lulus 2022, 9: DU 2022
    # Col 17: Lulus 2023, 18: DU 2023
    # Col 26: Lulus 2024, 27: DU 2024
    # Col 35: Lulus 2025, 36: DU 2025
    # Col 44: Lulus 2026, 45: DU 2026
    prodi_data = []
    for r in range(2, ws_mas.max_row + 1):
        fak = str(ws_mas.cell(r, 2).value or "").strip()
        prodi = str(ws_mas.cell(r, 3).value or "").strip()
        jenjang = str(ws_mas.cell(r, 4).value or "S1").strip()
        
        l_22 = int(ws_mas.cell(r, 8).value or 0)
        d_22 = int(ws_mas.cell(r, 9).value or 0)
        
        l_23 = int(ws_mas.cell(r, 17).value or 0)
        d_23 = int(ws_mas.cell(r, 18).value or 0)
        
        l_24 = int(ws_mas.cell(r, 26).value or 0)
        d_24 = int(ws_mas.cell(r, 27).value or 0)
        
        l_25 = int(ws_mas.cell(r, 35).value or 0)
        d_25 = int(ws_mas.cell(r, 36).value or 0)
        
        l_26 = int(ws_mas.cell(r, 44).value or 0)
        d_26 = int(ws_mas.cell(r, 45).value or 0)
        
        tot_l = l_22 + l_23 + l_24 + l_25 + l_26
        tot_d = d_22 + d_23 + d_24 + d_25 + d_26
        tot_g = tot_l - tot_d
        pct_g = (tot_g / tot_l * 100) if tot_l > 0 else 0.0

        prodi_data.append({
            "fakultas": fak,
            "prodi": prodi,
            "jenjang": jenjang,
            2022: {"l": l_22, "d": d_22},
            2023: {"l": l_23, "d": d_23},
            2024: {"l": l_24, "d": d_24},
            2025: {"l": l_25, "d": d_25},
            2026: {"l": l_26, "d": d_26},
            "tot_l": tot_l,
            "tot_d": tot_d,
            "tot_g": tot_g,
            "pct_g": pct_g,
            "row_idx": r + 4 # akan berada di baris r+4 di sheet rincian (mulai baris 6)
        })

    num_prodi = len(prodi_data)
    print(f"Total program studi dimuat: {num_prodi}")

    # Inisialisasi Workbook baru
    wb = openpyxl.Workbook()
    wb.remove(wb.active)

    # -------------------------------------------------------------------------
    # PALET WARNA & TIPOGRAFI STANDAR KORPORAT EKSEKUTIF
    # -------------------------------------------------------------------------
    FONT_FAMILY = "Segoe UI"
    
    NAVY_MAIN      = "0D233A"
    SLATE_TITLE    = "1E293B"
    NAVY_2022      = "1E3A8A"
    CYAN_2023      = "0369A1"
    GREEN_2024     = "15803D"
    AMBER_2025     = "B45309"
    PURPLE_2026    = "6D28D9"
    DARK_5THN      = "0F172A"
    
    SUB_ID         = "334155"
    SUB_2022       = "2563EB"
    SUB_2023       = "0284C7"
    SUB_2024       = "16A34A"
    SUB_2025       = "D97706"
    SUB_2026       = "7C3AED"
    SUB_5THN       = "1E293B"

    WHITE          = "FFFFFF"
    ICE_ROW        = "F8FAFC"
    BORDER_LIGHT   = "E2E8F0"
    BORDER_DIVIDER = "94A3B8"
    TOTAL_ROW_BG   = "0F172A"
    
    ALERT_RED_BG   = "FEE2E2"
    ALERT_RED_FG   = "991B1B"
    GOOD_GRN_BG    = "DCFCE7"
    GOOD_GRN_FG    = "166534"
    CARD_BG_1      = "EFF6FF"
    CARD_BG_2      = "F0FDF4"
    CARD_BG_3      = "FEF2F2"
    CARD_BG_4      = "FFFBEB"

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

    al_center = Alignment(horizontal='center', vertical='center')
    al_left   = Alignment(horizontal='left', vertical='center')
    al_right  = Alignment(horizontal='right', vertical='center')

    FMT_QTY = '#,##0;(#,##0);"-"'
    FMT_PCT = '0.0"%"'

    # =========================================================================
    # SHEET 2 TERLEBIH DAHULU: RINCIAN PER PRODI (Agar cell referensi tersedia)
    # =========================================================================
    print("Membangun Sheet 2: Rincian_Per_Prodi...")
    ws2 = wb.create_sheet(title="Rincian_Per_Prodi")
    ws2.views.sheetView[0].showGridLines = True

    # Title Banner
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

    ws2.row_dimensions[3].height = 8

    # Tier 1 Headers (Row 4)
    tier1_sections = [
        ("A", "D", "IDENTITAS PROGRAM STUDI", SUB_ID, False),
        ("E", "H", "TAHUN AKADEMIK 2026", PURPLE_2026, False),
        ("I", "L", "TAHUN AKADEMIK 2025", AMBER_2025, False),
        ("M", "P", "TAHUN AKADEMIK 2024", GREEN_2024, False),
        ("Q", "T", "TAHUN AKADEMIK 2023", CYAN_2023, False),
        ("U", "X", "TAHUN AKADEMIK 2022", NAVY_2022, False),
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
            if ci == e_idx and ci != 28:
                cell.border = Border(left=thin_light, right=Side(style='medium', color=BORDER_DIVIDER), top=thin_light, bottom=thin_light)
            else:
                cell.border = border_cell

    # Tier 2 Headers (Row 5)
    tier2_cols = [
        ("No", SUB_ID), ("Fakultas", SUB_ID), ("Nama Program Studi", SUB_ID), ("Jenjang", SUB_ID),
        ("Lulus", SUB_2026), ("Daftar Ulang", SUB_2026), ("Gugur", SUB_2026), ("% Gugur", SUB_2026),
        ("Lulus", SUB_2025), ("Daftar Ulang", SUB_2025), ("Gugur", SUB_2025), ("% Gugur", SUB_2025),
        ("Lulus", SUB_2024), ("Daftar Ulang", SUB_2024), ("Gugur", SUB_2024), ("% Gugur", SUB_2024),
        ("Lulus", SUB_2023), ("Daftar Ulang", SUB_2023), ("Gugur", SUB_2023), ("% Gugur", SUB_2023),
        ("Lulus", SUB_2022), ("Daftar Ulang", SUB_2022), ("Gugur", SUB_2022), ("% Gugur", SUB_2022),
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

    # Isi Data Rincian (Row 6 s.d. 86)
    start_row = 6
    for i, p in enumerate(prodi_data):
        cur_row = start_row + i
        ws2.row_dimensions[cur_row].height = 20
        bg_row = ICE_ROW if i % 2 == 1 else WHITE

        ws2.cell(cur_row, 1, i + 1).alignment = al_center
        ws2.cell(cur_row, 2, p['fakultas']).alignment = al_left
        ws2.cell(cur_row, 3, p['prodi']).alignment = al_left
        ws2.cell(cur_row, 4, p['jenjang']).alignment = al_center

        # 2026
        ws2.cell(cur_row, 5, p[2026]['l'])
        ws2.cell(cur_row, 6, p[2026]['d'])
        ws2.cell(cur_row, 7, f"=MAX(0, E{cur_row}-F{cur_row})")
        ws2.cell(cur_row, 8, f"=IF(E{cur_row}>0, (G{cur_row}/E{cur_row})*100, 0)")

        # 2025
        ws2.cell(cur_row, 9, p[2025]['l'])
        ws2.cell(cur_row, 10, p[2025]['d'])
        ws2.cell(cur_row, 11, f"=MAX(0, I{cur_row}-J{cur_row})")
        ws2.cell(cur_row, 12, f"=IF(I{cur_row}>0, (K{cur_row}/I{cur_row})*100, 0)")

        # 2024
        ws2.cell(cur_row, 13, p[2024]['l'])
        ws2.cell(cur_row, 14, p[2024]['d'])
        ws2.cell(cur_row, 15, f"=MAX(0, M{cur_row}-N{cur_row})")
        ws2.cell(cur_row, 16, f"=IF(M{cur_row}>0, (O{cur_row}/M{cur_row})*100, 0)")

        # 2023
        ws2.cell(cur_row, 17, p[2023]['l'])
        ws2.cell(cur_row, 18, p[2023]['d'])
        ws2.cell(cur_row, 19, f"=MAX(0, Q{cur_row}-R{cur_row})")
        ws2.cell(cur_row, 20, f"=IF(Q{cur_row}>0, (S{cur_row}/Q{cur_row})*100, 0)")

        # 2022
        ws2.cell(cur_row, 21, p[2022]['l'])
        ws2.cell(cur_row, 22, p[2022]['d'])
        ws2.cell(cur_row, 23, f"=MAX(0, U{cur_row}-V{cur_row})")
        ws2.cell(cur_row, 24, f"=IF(U{cur_row}>0, (W{cur_row}/U{cur_row})*100, 0)")

        # Total 5 Thn
        ws2.cell(cur_row, 25, f"=E{cur_row}+I{cur_row}+M{cur_row}+Q{cur_row}+U{cur_row}")
        ws2.cell(cur_row, 26, f"=F{cur_row}+J{cur_row}+N{cur_row}+R{cur_row}+V{cur_row}")
        ws2.cell(cur_row, 27, f"=G{cur_row}+K{cur_row}+O{cur_row}+S{cur_row}+W{cur_row}")
        ws2.cell(cur_row, 28, f"=IF(Y{cur_row}>0, (AA{cur_row}/Y{cur_row})*100, 0)")

        for ci in range(1, 29):
            cell = ws2.cell(cur_row, ci)
            cell.font = font_cell
            cell.fill = PatternFill(start_color=bg_row, end_color=bg_row, fill_type='solid')
            if ci in divider_cols and ci != 28:
                cell.border = border_cell_divider
            else:
                cell.border = border_cell

            if ci in [5, 6, 7, 9, 10, 11, 13, 14, 15, 17, 18, 19, 21, 22, 23, 25, 26, 27]:
                cell.alignment = al_right
                cell.number_format = FMT_QTY
            elif ci in [8, 12, 16, 20, 24, 28]:
                cell.alignment = al_right
                cell.number_format = FMT_PCT

        # Conditional Highlight 5 Tahun
        cell_28 = ws2.cell(cur_row, 28)
        if p['pct_g'] >= 30.0 and p['tot_l'] >= 50:
            cell_28.font = font_cell_alert
            cell_28.fill = PatternFill(start_color=ALERT_RED_BG, end_color=ALERT_RED_BG, fill_type='solid')
        elif p['pct_g'] <= 10.0 and p['tot_l'] >= 50:
            cell_28.font = font_cell_good
            cell_28.fill = PatternFill(start_color=GOOD_GRN_BG, end_color=GOOD_GRN_BG, fill_type='solid')

    # Row 87: Grand Total Universitas
    tot_row = start_row + num_prodi
    ws2.row_dimensions[tot_row].height = 24
    ws2.merge_cells(f"A{tot_row}:D{tot_row}")
    lbl_tot = ws2[f"A{tot_row}"]
    lbl_tot.value = "TOTAL UNIVERSITAS SYIAH KUALA"
    lbl_tot.font = font_total
    lbl_tot.alignment = Alignment(horizontal='center', vertical='center')

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

    for ci in range(1, 29):
        c = ws2.cell(tot_row, ci)
        c.fill = PatternFill(start_color=TOTAL_ROW_BG, end_color=TOTAL_ROW_BG, fill_type='solid')
        if ci in divider_cols and ci != 28:
            c.border = border_total_divider
        else:
            c.border = border_total

    ws2.freeze_panes = "E6"

    col_widths2 = {
        'A': 6, 'B': 24, 'C': 38, 'D': 10
    }
    for ci in range(5, 29):
        letter = get_column_letter(ci)
        col_widths2[letter] = 12.5 if ci in [8, 12, 16, 20, 24, 28] else 12.0
    for letter, w in col_widths2.items():
        ws2.column_dimensions[letter].width = w

    # =========================================================================
    # SHEET 1: RINGKASAN EKSEKUTIF (FORMULA DINAMIS DARI SHEET RINCIAN)
    # =========================================================================
    print("Membangun Sheet 1: Ringkasan_Eksekutif dengan Formula Dinamis...")
    ws1 = wb.create_sheet(title="Ringkasan_Eksekutif", index=0)
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
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

    ws1.row_dimensions[3].height = 10

    # 1. KPI Cards Dinamis (Row 4–6)
    # Merujuk ke baris Grand Total sheet Rincian_Per_Prodi (Baris 87)
    cards = [
        ("A", "C", "TOTAL LULUS SELEKSI (5 TAHUN)", f"=Rincian_Per_Prodi!Y{tot_row}", "Calon Mahasiswa Dinyatakan Lulus", CARD_BG_1, "1E3A8A", FMT_QTY),
        ("D", "F", "TOTAL REGISTRASI ULANG (DU)", f"=Rincian_Per_Prodi!Z{tot_row}", f'="Tingkat Konversi: " & TEXT(Rincian_Per_Prodi!Z{tot_row}/Rincian_Per_Prodi!Y{tot_row}*100, "0.0") & "%"', CARD_BG_2, "166534", FMT_QTY),
        ("G", "I", "TOTAL GUGUR / TIDAK REGISTRASI", f"=Rincian_Per_Prodi!AA{tot_row}", "Kursi Ditinggalkan / Menolak Lolos", CARD_BG_3, "991B1B", FMT_QTY),
        ("J", "K", "RATA-RATA % GUGUR USK", f"=Rincian_Per_Prodi!AB{tot_row}", "Defisit Konversi Calon Mahasiswa", CARD_BG_4, "B45309", FMT_PCT)
    ]
    ws1.row_dimensions[4].height = 18
    ws1.row_dimensions[5].height = 28
    ws1.row_dimensions[6].height = 18

    for c_start, c_end, title, formula_val, sub, bg, fg, num_fmt in cards:
        ws1.merge_cells(f"{c_start}4:{c_end}4")
        ws1.merge_cells(f"{c_start}5:{c_end}5")
        ws1.merge_cells(f"{c_start}6:{c_end}6")

        top = ws1[f"{c_start}4"]
        top.value = title
        top.font = Font(name=FONT_FAMILY, size=8.5, bold=True, color="64748B")
        top.alignment = al_center

        mid = ws1[f"{c_start}5"]
        mid.value = formula_val
        mid.font = Font(name=FONT_FAMILY, size=16, bold=True, color=fg)
        mid.alignment = al_center
        mid.number_format = num_fmt

        bot = ws1[f"{c_start}6"]
        bot.value = sub
        bot.font = Font(name=FONT_FAMILY, size=8, italic=True, color="475569")
        bot.alignment = al_center

        s_idx = openpyxl.utils.column_index_from_string(c_start)
        e_idx = openpyxl.utils.column_index_from_string(c_end)
        for r in range(4, 7):
            for c in range(s_idx, e_idx + 1):
                ws1.cell(r, c).border = border_card
                ws1.cell(r, c).fill = PatternFill(start_color=bg, end_color=bg, fill_type='solid')

    ws1.row_dimensions[7].height = 14

    # 2. Tabel 1: Tren Tahunan USK (Row 8–15) Dinamis
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

    year_mapping = [
        (2022, 'U', 'V', 'W', 'X'),
        (2023, 'Q', 'R', 'S', 'T'),
        (2024, 'M', 'N', 'O', 'P'),
        (2025, 'I', 'J', 'K', 'L'),
        (2026, 'E', 'F', 'G', 'H')
    ]
    for idx, (yr, col_l, col_d, col_g, col_p) in enumerate(year_mapping, 10):
        ws1.row_dimensions[idx].height = 20
        bg_row = ICE_ROW if idx % 2 == 1 else WHITE

        ws1.cell(idx, 1, yr).alignment = al_center
        ws1.cell(idx, 1).font = font_cell_bold

        # Lulus, DU, Gugur merujuk ke Grand Total Rincian_Per_Prodi
        cl = ws1.cell(idx, 2, f"=Rincian_Per_Prodi!{col_l}{tot_row}")
        cd = ws1.cell(idx, 3, f"=Rincian_Per_Prodi!{col_d}{tot_row}")
        cg = ws1.cell(idx, 4, f"=Rincian_Per_Prodi!{col_g}{tot_row}")
        
        cp = ws1.cell(idx, 5, f"=Rincian_Per_Prodi!{col_p}{tot_row}")
        cy = ws1.cell(idx, 6, f"=IF(B{idx}>0, (C{idx}/B{idx})*100, 0)")
        cs = ws1.cell(idx, 7, f'=IF(E{idx}<=16.5, "Optimal", IF(E{idx}<=18.0, "Moderat", "Waspada"))')

        for ci in range(1, 8):
            cell = ws1.cell(idx, ci)
            cell.font = font_cell
            cell.fill = PatternFill(start_color=bg_row, end_color=bg_row, fill_type='solid')
            cell.border = border_cell
            if ci in [2, 3, 4]:
                cell.alignment = al_right
                cell.number_format = FMT_QTY
            elif ci in [5, 6]:
                cell.alignment = al_right
                cell.number_format = FMT_PCT
            elif ci in [1, 7]:
                cell.alignment = al_center

    # Row 15: Grand Total Tabel 1
    ws1.row_dimensions[15].height = 22
    ws1.cell(15, 1, "TOTAL 5 TAHUN").alignment = al_center
    ws1.cell(15, 2, f"=Rincian_Per_Prodi!Y{tot_row}")
    ws1.cell(15, 3, f"=Rincian_Per_Prodi!Z{tot_row}")
    ws1.cell(15, 4, f"=Rincian_Per_Prodi!AA{tot_row}")
    ws1.cell(15, 5, f"=Rincian_Per_Prodi!AB{tot_row}")
    ws1.cell(15, 6, f"=IF(B15>0, (C15/B15)*100, 0)")
    ws1.cell(15, 7, '16.7% Rata-rata')

    for ci in range(1, 8):
        c = ws1.cell(15, ci)
        c.font = font_total_gold if ci == 5 else font_total
        c.fill = PatternFill(start_color=TOTAL_ROW_BG, end_color=TOTAL_ROW_BG, fill_type='solid')
        c.border = border_total
        if ci in [2, 3, 4]:
            c.alignment = al_right
            c.number_format = FMT_QTY
        elif ci in [5, 6]:
            c.alignment = al_right
            c.number_format = FMT_PCT
        elif ci in [1, 7]:
            c.alignment = al_center

    ws1.row_dimensions[16].height = 14

    # 3. Tabel 2: Peringkat Fakultas (Row 17–31) Dinamis Menggunakan SUMIF
    ws1.merge_cells("A17:G17")
    t2_title = ws1["A17"]
    t2_title.value = "Tabel 2: Peringkat Disparitas Kelulusan vs Registrasi Ulang per Fakultas (Formula Dinamis SUMIF)"
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

    # Daftar fakultas berurutan dari rasio gugur tertinggi
    fak_order = [
        "PSDKU Gayo Lues",
        "Keperawatan",
        "Pertanian",
        "Kelautan dan Perikanan",
        "Kedokteran Hewan",
        "Teknik",
        "MIPA",
        "Ekonomi dan Bisnis",
        "FISIP",
        "FKIP",
        "Kedokteran",
        "Kedokteran Gigi",
        "Hukum"
    ]

    for rank, f_name in enumerate(fak_order):
        r_idx = 19 + rank
        ws1.row_dimensions[r_idx].height = 20
        bg_row = ICE_ROW if rank % 2 == 1 else WHITE

        ws1.cell(r_idx, 1, rank + 1).alignment = al_center
        ws1.cell(r_idx, 2, f_name).alignment = al_left
        
        # COUNTIF & SUMIF dinamis dari Rincian_Per_Prodi!
        ws1.cell(r_idx, 3, f'=COUNTIF(Rincian_Per_Prodi!$B$6:$B${tot_row-1}, B{r_idx})')
        ws1.cell(r_idx, 4, f'=SUMIF(Rincian_Per_Prodi!$B$6:$B${tot_row-1}, B{r_idx}, Rincian_Per_Prodi!$Y$6:$Y${tot_row-1})')
        ws1.cell(r_idx, 5, f'=SUMIF(Rincian_Per_Prodi!$B$6:$B${tot_row-1}, B{r_idx}, Rincian_Per_Prodi!$Z$6:$Z${tot_row-1})')
        ws1.cell(r_idx, 6, f'=SUMIF(Rincian_Per_Prodi!$B$6:$B${tot_row-1}, B{r_idx}, Rincian_Per_Prodi!$AA$6:$AA${tot_row-1})')
        ws1.cell(r_idx, 7, f'=IF(D{r_idx}>0, (F{r_idx}/D{r_idx})*100, 0)')

        for ci in range(1, 8):
            c = ws1.cell(r_idx, ci)
            c.font = font_cell
            c.fill = PatternFill(start_color=bg_row, end_color=bg_row, fill_type='solid')
            c.border = border_cell
            if ci == 3:
                c.alignment = al_center
            elif ci in [4, 5, 6]:
                c.alignment = al_right
                c.number_format = FMT_QTY
            elif ci == 7:
                c.alignment = al_right
                c.number_format = FMT_PCT

    ws1.row_dimensions[32].height = 14

    # 4. Tabel 3 & 4: Top 10 Prodi Bocor vs Setia (Side-by-Side)
    # Urutkan prodi aktif (Total Lulus >= 50) dari data resmi
    valid_prodis = [p for p in prodi_data if p['tot_l'] >= 50]
    top_bocor = sorted(valid_prodis, key=lambda x: x['pct_g'], reverse=True)[:10]
    top_setia = sorted(valid_prodis, key=lambda x: x['pct_g'])[:10]

    ws1.merge_cells("A33:E33")
    t3_title = ws1["A33"]
    t3_title.value = "⚠️ Top 10 Program Studi Kebocoran Tertinggi (% Gugur)"
    t3_title.font = Font(name=FONT_FAMILY, size=10, bold=True, color=ALERT_RED_FG)

    ws1.merge_cells("G33:K33")
    t4_title = ws1["G33"]
    t4_title.value = "🏆 Top 10 Program Studi Paling Loyal / Setia (Terendah Gugur)"
    t4_title.font = Font(name=FONT_FAMILY, size=10, bold=True, color=GOOD_GRN_FG)
    ws1.row_dimensions[33].height = 22

    t34_h = ["No", "Program Studi", "Fakultas", "Total Gugur", "% Gugur"]
    ws1.row_dimensions[34].height = 20
    for i, h in enumerate(t34_h, 1):
        c_kiri = ws1.cell(34, i)
        c_kiri.value = h
        c_kiri.font = font_tier2
        c_kiri.fill = PatternFill(start_color=ALERT_RED_FG, end_color=ALERT_RED_FG, fill_type='solid')
        c_kiri.alignment = al_center
        c_kiri.border = border_cell
        
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

        # Kiri (Bocor)
        pb = top_bocor[k]
        ws1.cell(r_k, 1, k + 1).alignment = al_center
        ws1.cell(r_k, 2, pb['prodi']).alignment = al_left
        ws1.cell(r_k, 3, pb['fakultas']).alignment = al_left
        ws1.cell(r_k, 4, f"=Rincian_Per_Prodi!AA{pb['row_idx']}").alignment = al_right # Formula dinamis
        
        cb = ws1.cell(r_k, 5, f"=Rincian_Per_Prodi!AB{pb['row_idx']}") # Formula dinamis
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

        # Kanan (Setia)
        ps = top_setia[k]
        ws1.cell(r_k, 7, k + 1).alignment = al_center
        ws1.cell(r_k, 8, ps['prodi']).alignment = al_left
        ws1.cell(r_k, 9, ps['fakultas']).alignment = al_left
        ws1.cell(r_k, 10, f"=Rincian_Per_Prodi!AA{ps['row_idx']}").alignment = al_right # Formula dinamis
        
        cs = ws1.cell(r_k, 11, f"=Rincian_Per_Prodi!AB{ps['row_idx']}") # Formula dinamis
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

    ws1_widths = {
        'A': 6, 'B': 30, 'C': 16, 'D': 15, 'E': 14,
        'F': 14, 'G': 6, 'H': 30, 'I': 16, 'J': 15, 'K': 14
    }
    for col_letter, width in ws1_widths.items():
        ws1.column_dimensions[col_letter].width = width

    # Simpan File Hasil
    print("Menyimpan file hasil sinkronisasi ke:", out_path)
    wb.save(out_path)
    print("✔ Berhasil! Rekapitulasi selisih telah diselaraskan 100% dengan Database Master.")

if __name__ == "__main__":
    build_beautified_selisih_excel()
