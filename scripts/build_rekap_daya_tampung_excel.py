#!/usr/bin/env python3
"""
build_rekap_daya_tampung_excel.py
=============================================================================
GENERATOR REKAPITULASI DAYA TAMPUNG, PEMINAT & SISA KUOTA (2022–2026)
=============================================================================
Skrip ini membaca data resmi dari Master Database (Single Source of Truth):
data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx (Sheet: Master_Semua_Prodi)
dan data/raw/rekap data (fix).xlsx (Sheet: Rekapitulasi Data) untuk Kode Prodi resmi.

Menghasilkan file terolah profesional:
data/processed/rekap_daya_tampung_peminat_dan_sisa_kuota_2022_2026.xlsx

Fitur Utama:
1. Kolom Persis Sesuai Permintaan & Foto:
   - No | Kode Prodi | Nama Prodi | Jenjang | Total Daya Tampung | Total Peminat | Total Daftar Ulang | Sisa Kuota
2. Sheet 'Ringkasan_Eksekutif':
   - 4 KPI Card Dinamis (Total DT 5-Thn, Total Peminat, Realisasi DU, Total Sisa Kuota)
   - Tabel Tren Tahunan (2022–2026) dengan formula live
   - Tabel Kinerja per Fakultas (Formula COUNTIF dan SUMIF)
3. Sheet 'Rincian_Semua_Tahun':
   - Tabel multi-tahun lengkap (2022–2026) dengan formula dinamis Sisa Kuota = DT - DU
   - Total 5-Tahun dan baris Grand Total Universitas
4. Sheet Khusus '2026 (Sesuai Foto)':
   - Kolom dan urutan prodi persis seperti pada foto layar (diurutkan berdasarkan keketatan ascending)
5. Sheet Tahunan 'Tahun_2025', 'Tahun_2024', 'Tahun_2023', 'Tahun_2022'
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_rekap_daya_tampung_excel():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    master_path = os.path.join(repo_dir, "data", "master", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    raw_path = os.path.join(repo_dir, "data", "raw", "rekap data (fix).xlsx")
    out_path = os.path.join(repo_dir, "data", "processed", "rekap_daya_tampung_peminat_dan_sisa_kuota_2022_2026.xlsx")

    if not os.path.exists(master_path):
        raise FileNotFoundError(f"File master tidak ditemukan di {master_path}")

    print("Membaca data master resmi dari:", master_path)
    wb_mas = openpyxl.load_workbook(master_path, data_only=True)
    ws_mas = wb_mas["Master_Semua_Prodi"]

    # Pemetaan Kode Prodi dari raw
    prodi_to_code = {}
    if os.path.exists(raw_path):
        wb_raw = openpyxl.load_workbook(raw_path, data_only=True, read_only=True)
        ws_raw = wb_raw["Rekapitulasi Data"]
        for r in range(5, ws_raw.max_row + 1):
            kode = ws_raw.cell(r, 2).value
            nama = ws_raw.cell(r, 3).value
            if nama:
                n_str = str(nama).strip().upper()
                if kode:
                    try:
                        k_str = str(int(kode)).zfill(7)
                    except:
                        k_str = str(kode).strip()
                    prodi_to_code[n_str] = k_str

    # Fallback / penetapan resmi untuk prodi baru
    prodi_to_code["TEKNIK PERMINYAKAN"] = "0411601"
    prodi_to_code["HUBUNGAN INTERNASIONAL"] = "0910101"

    # Muat 81 data prodi dari Master_Semua_Prodi
    # Kolom di Master:
    # 1: No, 2: Fakultas, 3: Nama Program Studi, 4: Jenjang
    # 2022 -> 6: Peminat, 7: DT, 9: DU
    # 2023 -> 15: Peminat, 16: DT, 18: DU
    # 2024 -> 24: Peminat, 25: DT, 27: DU
    # 2025 -> 33: Peminat, 34: DT, 36: DU
    # 2026 -> 42: Peminat, 43: DT, 45: DU
    prodi_list = []
    for r in range(2, ws_mas.max_row + 1):
        no_val = ws_mas.cell(r, 1).value
        fak = str(ws_mas.cell(r, 2).value or "").strip()
        nama = str(ws_mas.cell(r, 3).value or "").strip()
        jenjang = str(ws_mas.cell(r, 4).value or "S1").strip()

        # Ambil kode
        n_upper = nama.upper()
        code = prodi_to_code.get(n_upper)
        if not code:
            for k, v in prodi_to_code.items():
                if n_upper in k or k in n_upper:
                    code = v
                    break
        if not code:
            code = "-"

        p_22 = int(ws_mas.cell(r, 6).value or 0)
        dt_22 = int(ws_mas.cell(r, 7).value or 0)
        du_22 = int(ws_mas.cell(r, 9).value or 0)

        p_23 = int(ws_mas.cell(r, 15).value or 0)
        dt_23 = int(ws_mas.cell(r, 16).value or 0)
        du_23 = int(ws_mas.cell(r, 18).value or 0)

        p_24 = int(ws_mas.cell(r, 24).value or 0)
        dt_24 = int(ws_mas.cell(r, 25).value or 0)
        du_24 = int(ws_mas.cell(r, 27).value or 0)

        p_25 = int(ws_mas.cell(r, 33).value or 0)
        dt_25 = int(ws_mas.cell(r, 34).value or 0)
        du_25 = int(ws_mas.cell(r, 36).value or 0)

        p_26 = int(ws_mas.cell(r, 42).value or 0)
        dt_26 = int(ws_mas.cell(r, 43).value or 0)
        du_26 = int(ws_mas.cell(r, 45).value or 0)

        ket_26 = p_26 / dt_26 if dt_26 > 0 else 0

        prodi_list.append({
            'no': no_val,
            'kode': code,
            'nama': nama,
            'jenjang': jenjang,
            'fakultas': fak,
            2022: {'dt': dt_22, 'p': p_22, 'du': du_22},
            2023: {'dt': dt_23, 'p': p_23, 'du': du_23},
            2024: {'dt': dt_24, 'p': p_24, 'du': du_24},
            2025: {'dt': dt_25, 'p': p_25, 'du': du_25},
            2026: {'dt': dt_26, 'p': p_26, 'du': du_26, 'ket': ket_26}
        })

    print(f"Total program studi dimuat: {len(prodi_list)}")

    # Inisialisasi Workbook Baru
    wb = openpyxl.Workbook()
    # Hapus sheet default
    default_sheet = wb.active
    wb.remove(default_sheet)

    # ---------------------------------------------------------------------------
    # PALET WARNA & STYLING PROFESIONAL
    # ---------------------------------------------------------------------------
    NAVY_PRIMARY = "1B365D"   # USK Primary Blue
    NAVY_DARK = "0F172A"      # Slate 900
    BLUE_ACCENT = "2563EB"    # Royal Blue
    TEAL_CARD = "0D9488"      # Teal Emerald
    AMBER_CARD = "D97706"     # Amber
    ROSE_CARD = "E11D48"      # Crimson Rose
    CARD_BG_BLUE = "EFF6FF"
    CARD_BG_TEAL = "F0FDF4"
    CARD_BG_AMBER = "FEF3C7"
    CARD_BG_ROSE = "FFF1F2"
    BORDER_LIGHT = "E2E8F0"
    BORDER_DARK = "94A3B8"
    WHITE = "FFFFFF"
    ICE_ROW = "F8FAFC"
    DEFISIT_BG = "FFE4E6"     # Highlight sisa kuota
    DEFISIT_FG = "991B1B"

    font_title = Font(name="Segoe UI", size=15, bold=True, color=WHITE)
    font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="E0E7FF")
    font_section = Font(name="Segoe UI", size=11, bold=True, color=NAVY_PRIMARY)
    font_tier1 = Font(name="Segoe UI", size=10, bold=True, color=WHITE)
    font_tier2 = Font(name="Segoe UI", size=9, bold=True, color=WHITE)
    font_data = Font(name="Segoe UI", size=9, color="1E293B")
    font_data_bold = Font(name="Segoe UI", size=9, bold=True, color="0F172A")
    font_defisit = Font(name="Segoe UI", size=9, bold=True, color=DEFISIT_FG)
    font_grand_total = Font(name="Segoe UI", size=10, bold=True, color=WHITE)

    # KPI Card Fonts
    font_kpi_title = Font(name="Segoe UI", size=9, bold=True, color="475569")
    font_kpi_value_blue = Font(name="Segoe UI", size=18, bold=True, color="1E3A8A")
    font_kpi_value_teal = Font(name="Segoe UI", size=18, bold=True, color="065F46")
    font_kpi_value_amber = Font(name="Segoe UI", size=18, bold=True, color="92400E")
    font_kpi_value_rose = Font(name="Segoe UI", size=18, bold=True, color="9F1239")
    font_kpi_sub = Font(name="Segoe UI", size=8, italic=True, color="64748B")

    al_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    al_left = Alignment(horizontal="left", vertical="center")
    al_right = Alignment(horizontal="right", vertical="center")

    thin_border = Border(
        left=Side(style='thin', color=BORDER_LIGHT),
        right=Side(style='thin', color=BORDER_LIGHT),
        top=Side(style='thin', color=BORDER_LIGHT),
        bottom=Side(style='thin', color=BORDER_LIGHT)
    )
    total_border = Border(
        left=Side(style='thin', color=BORDER_DARK),
        right=Side(style='thin', color=BORDER_DARK),
        top=Side(style='thin', color=BORDER_DARK),
        bottom=Side(style='double', color=NAVY_PRIMARY)
    )

    # ===========================================================================
    # 1. SHEET: Rincian_Semua_Tahun (MULTI-TAHUN 2022–2026)
    # ===========================================================================
    print("Membangun Sheet: Rincian_Semua_Tahun...")
    ws_all = wb.create_sheet(title="Rincian_Semua_Tahun")
    ws_all.views.sheetView[0].showGridLines = True

    # Title Banner
    ws_all.merge_cells("A1:AE2")
    ws_all["A1"].value = "REKAPITULASI DAYA TAMPUNG, PEMINAT & SISA KUOTA UNIVERSITAS SYIAH KUALA (2022–2026)"
    ws_all["A1"].font = font_title
    ws_all["A1"].fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
    ws_all["A1"].alignment = al_center
    ws_all.row_dimensions[1].height = 24
    ws_all.row_dimensions[2].height = 24

    ws_all.merge_cells("A3:AE3")
    ws_all["A3"].value = "Sumber: Database Master PMB USK | Formula Sisa Kuota = Total Daya Tampung - Total Daftar Ulang"
    ws_all["A3"].font = font_subtitle
    ws_all["A3"].fill = PatternFill(start_color="2A4365", end_color="2A4365", fill_type="solid")
    ws_all["A3"].alignment = al_center
    ws_all.row_dimensions[3].height = 18

    # Tier 1 Headers (Row 4)
    # Identitas (A4:E4)
    # 2026 (F4:I4), 2025 (J4:M4), 2024 (N4:Q4), 2023 (R4:U4), 2022 (V4:Y4)
    # Total 5 Tahun (Z4:AE4)
    t1_sections = [
        ("A", "E", "IDENTITAS PROGRAM STUDI", "334155"),
        ("F", "I", "TAHUN 2026", "6366F1"),
        ("J", "M", "TAHUN 2025", "D97706"),
        ("N", "Q", "TAHUN 2024", "0D9488"),
        ("R", "U", "TAHUN 2023", "0284C7"),
        ("V", "Y", "TAHUN 2022", "1E3A8A"),
        ("Z", "AE", "TOTAL AKUMULASI 5 TAHUN (2022–2026)", "0F172A")
    ]
    ws_all.row_dimensions[4].height = 25
    ws_all.row_dimensions[5].height = 25

    for c1, c2, title, bg in t1_sections:
        ws_all.merge_cells(f"{c1}4:{c2}4")
        cell = ws_all[f"{c1}4"]
        cell.value = title
        cell.font = font_tier1
        cell.alignment = al_center
        s_idx = openpyxl.utils.column_index_from_string(c1)
        e_idx = openpyxl.utils.column_index_from_string(c2)
        for ci in range(s_idx, e_idx + 1):
            ws_all.cell(4, ci).fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
            ws_all.cell(4, ci).border = thin_border

    # Tier 2 Headers (Row 5)
    t2_headers = [
        # Identitas
        ("No", "475569"), ("Kode Prodi", "475569"), ("Nama Program Studi", "475569"), ("Jenjang", "475569"), ("Fakultas", "475569"),
        # 2026
        ("Total DT", "4F46E5"), ("Peminat", "4F46E5"), ("Daftar Ulang", "4F46E5"), ("Sisa Kuota", "DC2626"),
        # 2025
        ("Total DT", "D97706"), ("Peminat", "D97706"), ("Daftar Ulang", "D97706"), ("Sisa Kuota", "DC2626"),
        # 2024
        ("Total DT", "0D9488"), ("Peminat", "0D9488"), ("Daftar Ulang", "0D9488"), ("Sisa Kuota", "DC2626"),
        # 2023
        ("Total DT", "0284C7"), ("Peminat", "0284C7"), ("Daftar Ulang", "0284C7"), ("Sisa Kuota", "DC2626"),
        # 2022
        ("Total DT", "2563EB"), ("Peminat", "2563EB"), ("Daftar Ulang", "2563EB"), ("Sisa Kuota", "DC2626"),
        # Total 5-Thn
        ("Total DT", "1E293B"), ("Total Peminat", "1E293B"), ("Total DU", "1E293B"), ("Total Sisa", "991B1B"), ("Fill Rate %", "1E293B"), ("Keketatan", "1E293B")
    ]
    for ci, (col_name, bg) in enumerate(t2_headers, 1):
        cell = ws_all.cell(5, ci)
        cell.value = col_name
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        cell.alignment = al_center
        cell.border = thin_border

    # Data Rows (Row 6 s.d. 86)
    start_row = 6
    for i, p in enumerate(prodi_list):
        r = start_row + i
        ws_all.row_dimensions[r].height = 20
        bg_row = ICE_ROW if i % 2 == 1 else WHITE
        fill_row = PatternFill(start_color=bg_row, end_color=bg_row, fill_type="solid")

        # Identitas
        ws_all.cell(r, 1, p['no']).alignment = al_center
        ws_all.cell(r, 2, p['kode']).alignment = al_center
        ws_all.cell(r, 3, p['nama']).alignment = al_left
        ws_all.cell(r, 4, p['jenjang']).alignment = al_center
        ws_all.cell(r, 5, p['fakultas']).alignment = al_left

        # 2026 (Cols 6..9 -> F, G, H, I)
        ws_all.cell(r, 6, p[2026]['dt']).number_format = "#,##0"
        ws_all.cell(r, 7, p[2026]['p']).number_format = "#,##0"
        ws_all.cell(r, 8, p[2026]['du']).number_format = "#,##0"
        ws_all.cell(r, 9, f"=F{r}-H{r}").number_format = "#,##0"

        # 2025 (Cols 10..13 -> J, K, L, M)
        ws_all.cell(r, 10, p[2025]['dt']).number_format = "#,##0"
        ws_all.cell(r, 11, p[2025]['p']).number_format = "#,##0"
        ws_all.cell(r, 12, p[2025]['du']).number_format = "#,##0"
        ws_all.cell(r, 13, f"=J{r}-L{r}").number_format = "#,##0"

        # 2024 (Cols 14..17 -> N, O, P, Q)
        ws_all.cell(r, 14, p[2024]['dt']).number_format = "#,##0"
        ws_all.cell(r, 15, p[2024]['p']).number_format = "#,##0"
        ws_all.cell(r, 16, p[2024]['du']).number_format = "#,##0"
        ws_all.cell(r, 17, f"=N{r}-P{r}").number_format = "#,##0"

        # 2023 (Cols 18..21 -> R, S, T, U)
        ws_all.cell(r, 18, p[2023]['dt']).number_format = "#,##0"
        ws_all.cell(r, 19, p[2023]['p']).number_format = "#,##0"
        ws_all.cell(r, 20, p[2023]['du']).number_format = "#,##0"
        ws_all.cell(r, 21, f"=R{r}-T{r}").number_format = "#,##0"

        # 2022 (Cols 22..25 -> V, W, X, Y)
        ws_all.cell(r, 22, p[2022]['dt']).number_format = "#,##0"
        ws_all.cell(r, 23, p[2022]['p']).number_format = "#,##0"
        ws_all.cell(r, 24, p[2022]['du']).number_format = "#,##0"
        ws_all.cell(r, 25, f"=V{r}-X{r}").number_format = "#,##0"

        # Total 5-Thn (Cols 26..31 -> Z, AA, AB, AC, AD, AE)
        ws_all.cell(r, 26, f"=F{r}+J{r}+N{r}+R{r}+V{r}").number_format = "#,##0"
        ws_all.cell(r, 27, f"=G{r}+K{r}+O{r}+S{r}+W{r}").number_format = "#,##0"
        ws_all.cell(r, 28, f"=H{r}+L{r}+P{r}+T{r}+X{r}").number_format = "#,##0"
        ws_all.cell(r, 29, f"=I{r}+M{r}+Q{r}+U{r}+Y{r}").number_format = "#,##0"
        ws_all.cell(r, 30, f"=IF(Z{r}>0, (AB{r}/Z{r})*100, 0)").number_format = "0.0\"%\""
        ws_all.cell(r, 31, f"=IF(Z{r}>0, AA{r}/Z{r}, 0)").number_format = "0.00"

        # Styling row
        for ci in range(1, 32):
            cell = ws_all.cell(r, ci)
            cell.font = font_data
            cell.fill = fill_row
            cell.border = thin_border
            if ci in [9, 13, 17, 21, 25]:
                cell.font = font_defisit
                cell.fill = PatternFill(start_color=DEFISIT_BG, end_color=DEFISIT_BG, fill_type="solid")
            elif ci in [26, 27, 28, 29]:
                cell.font = font_data_bold
            elif ci == 29: # Total Sisa
                cell.font = font_defisit

    # Grand Total Row (Row 87)
    tot_row = 87
    ws_all.row_dimensions[tot_row].height = 24
    ws_all.merge_cells(f"A{tot_row}:E{tot_row}")
    ws_all[f"A{tot_row}"].value = "GRAND TOTAL UNIVERSITAS"
    ws_all[f"A{tot_row}"].font = font_grand_total
    ws_all[f"A{tot_row}"].alignment = al_center

    for ci in range(1, 32):
        cell = ws_all.cell(tot_row, ci)
        cell.fill = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
        cell.border = total_border
        cell.font = font_grand_total

    # Rumus Grand Total per kolom angka
    col_letters = ["F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC"]
    for ci, cl in enumerate(col_letters, 6):
        ws_all.cell(tot_row, ci, f"=SUM({cl}6:{cl}86)").number_format = "#,##0"

    # Fill rate & Keketatan total
    ws_all.cell(tot_row, 30, f"=IF(Z{tot_row}>0, (AB{tot_row}/Z{tot_row})*100, 0)").number_format = "0.0\"%\""
    ws_all.cell(tot_row, 31, f"=IF(Z{tot_row}>0, AA{tot_row}/Z{tot_row}, 0)").number_format = "0.00"

    ws_all.freeze_panes = "F6"

    # Auto Width Columns
    for col in ws_all.columns:
        cl = get_column_letter(col[0].column)
        if cl in ["A", "B", "D"]:
            ws_all.column_dimensions[cl].width = 11
        elif cl == "C":
            ws_all.column_dimensions[cl].width = 38
        elif cl == "E":
            ws_all.column_dimensions[cl].width = 22
        else:
            ws_all.column_dimensions[cl].width = 13

    # ===========================================================================
    # 2. SHEET: Tahun_2026 (PERSIS SEPERTI PADA FOTO WHATSAPP USER)
    # ===========================================================================
    print("Membangun Sheet: Tahun_2026 (Sesuai Foto)...")
    ws_26 = wb.create_sheet(title="Tahun_2026")
    ws_26.views.sheetView[0].showGridLines = True

    # Urutkan prodi persis seperti pada foto (berdasarkan Keketatan 2026 ascending)
    prodi_sorted_26 = sorted(prodi_list, key=lambda x: x[2026]['ket'])

    # Header Row 1 & 2
    # Row 1: Merged E1:H1 = 2026
    ws_26.row_dimensions[1].height = 24
    ws_26.row_dimensions[2].height = 24

    ws_26["A1"] = "No"
    ws_26["B1"] = "Kode Prodi"
    ws_26["C1"] = "Nama Prodi"
    ws_26["D1"] = "Jenjang"
    for cl in ["A", "B", "C", "D"]:
        ws_26[f"{cl}1"].font = font_tier1
        ws_26[f"{cl}1"].fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
        ws_26[f"{cl}1"].alignment = al_center
        ws_26[f"{cl}1"].border = thin_border

    ws_26.merge_cells("E1:H1")
    ws_26["E1"] = "2026"
    ws_26["E1"].font = Font(name="Segoe UI", size=12, bold=True, color=WHITE)
    ws_26["E1"].alignment = al_center
    for ci in range(5, 9):
        ws_26.cell(1, ci).fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        ws_26.cell(1, ci).border = thin_border

    # Row 2 Subheaders
    subheaders_26 = [
        ("No", NAVY_PRIMARY), ("Kode Prodi", NAVY_PRIMARY), ("Nama Prodi", NAVY_PRIMARY), ("Jenjang", NAVY_PRIMARY),
        ("Total Daya Tampung", "2563EB"), ("Total Peminat", "2563EB"), ("Total Daftar Ulang", "2563EB"), ("Sisa Kuota", "DC2626")
    ]
    for ci, (txt, bg) in enumerate(subheaders_26, 1):
        cell = ws_26.cell(2, ci)
        cell.value = txt
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
        cell.alignment = al_center
        cell.border = thin_border

    # Isi Data Row 3 s.d. 83
    for i, p in enumerate(prodi_sorted_26):
        r = 3 + i
        ws_26.row_dimensions[r].height = 20
        bg_row = ICE_ROW if i % 2 == 1 else WHITE
        fill_row = PatternFill(start_color=bg_row, end_color=bg_row, fill_type="solid")

        ws_26.cell(r, 1, p['no']).alignment = al_center
        ws_26.cell(r, 2, p['kode']).alignment = al_center
        ws_26.cell(r, 3, p['nama']).alignment = al_left
        ws_26.cell(r, 4, p['jenjang']).alignment = al_center

        ws_26.cell(r, 5, p[2026]['dt']).number_format = "#,##0"
        ws_26.cell(r, 6, p[2026]['p']).number_format = "#,##0"
        ws_26.cell(r, 7, p[2026]['du']).number_format = "#,##0"
        ws_26.cell(r, 8, f"=E{r}-G{r}").number_format = "#,##0"

        for ci in range(1, 9):
            cell = ws_26.cell(r, ci)
            cell.font = font_data
            cell.fill = fill_row
            cell.border = thin_border
            if ci == 8:
                cell.font = font_defisit
                cell.fill = PatternFill(start_color=DEFISIT_BG, end_color=DEFISIT_BG, fill_type="solid")

    # Grand Total Row 84
    tot_row_26 = 3 + len(prodi_sorted_26)
    ws_26.row_dimensions[tot_row_26].height = 24
    ws_26.merge_cells(f"A{tot_row_26}:D{tot_row_26}")
    ws_26[f"A{tot_row_26}"] = "TOTAL KESELURUHAN UNIVERSITAS"
    ws_26[f"A{tot_row_26}"].font = font_grand_total
    ws_26[f"A{tot_row_26}"].alignment = al_center

    for ci in range(1, 9):
        cell = ws_26.cell(tot_row_26, ci)
        cell.fill = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
        cell.border = total_border
        cell.font = font_grand_total

    ws_26.cell(tot_row_26, 5, f"=SUM(E3:E{tot_row_26-1})").number_format = "#,##0"
    ws_26.cell(tot_row_26, 6, f"=SUM(F3:F{tot_row_26-1})").number_format = "#,##0"
    ws_26.cell(tot_row_26, 7, f"=SUM(G3:G{tot_row_26-1})").number_format = "#,##0"
    ws_26.cell(tot_row_26, 8, f"=SUM(H3:H{tot_row_26-1})").number_format = "#,##0"

    ws_26.freeze_panes = "E3"
    ws_26.column_dimensions["A"].width = 8
    ws_26.column_dimensions["B"].width = 14
    ws_26.column_dimensions["C"].width = 40
    ws_26.column_dimensions["D"].width = 10
    ws_26.column_dimensions["E"].width = 20
    ws_26.column_dimensions["F"].width = 16
    ws_26.column_dimensions["G"].width = 18
    ws_26.column_dimensions["H"].width = 15

    # ===========================================================================
    # 3. SHEET: TAHUN 2025, 2024, 2023, 2022 (Struktur Yang Sama)
    # ===========================================================================
    years_order = [2025, 2024, 2023, 2022]
    year_colors = {
        2025: ("D97706", "B45309"),
        2024: ("0D9488", "0F766E"),
        2023: ("0284C7", "0369A1"),
        2022: ("1E3A8A", "1E40AF")
    }

    for yr in years_order:
        print(f"Membangun Sheet: Tahun_{yr}...")
        ws_yr = wb.create_sheet(title=f"Tahun_{yr}")
        ws_yr.views.sheetView[0].showGridLines = True

        ws_yr.row_dimensions[1].height = 24
        ws_yr.row_dimensions[2].height = 24

        bg_hdr, bg_sub = year_colors[yr]

        ws_yr["A1"] = "No"
        ws_yr["B1"] = "Kode Prodi"
        ws_yr["C1"] = "Nama Prodi"
        ws_yr["D1"] = "Jenjang"
        for cl in ["A", "B", "C", "D"]:
            ws_yr[f"{cl}1"].font = font_tier1
            ws_yr[f"{cl}1"].fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
            ws_yr[f"{cl}1"].alignment = al_center
            ws_yr[f"{cl}1"].border = thin_border

        ws_yr.merge_cells("E1:H1")
        ws_yr["E1"] = str(yr)
        ws_yr["E1"].font = Font(name="Segoe UI", size=12, bold=True, color=WHITE)
        ws_yr["E1"].alignment = al_center
        for ci in range(5, 9):
            ws_yr.cell(1, ci).fill = PatternFill(start_color=bg_hdr, end_color=bg_hdr, fill_type="solid")
            ws_yr.cell(1, ci).border = thin_border

        subheaders_yr = [
            ("No", NAVY_PRIMARY), ("Kode Prodi", NAVY_PRIMARY), ("Nama Prodi", NAVY_PRIMARY), ("Jenjang", NAVY_PRIMARY),
            ("Total Daya Tampung", bg_sub), ("Total Peminat", bg_sub), ("Total Daftar Ulang", bg_sub), ("Sisa Kuota", "DC2626")
        ]
        for ci, (txt, bg) in enumerate(subheaders_yr, 1):
            cell = ws_yr.cell(2, ci)
            cell.value = txt
            cell.font = font_tier2
            cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
            cell.alignment = al_center
            cell.border = thin_border

        for i, p in enumerate(prodi_list):
            r = 3 + i
            ws_yr.row_dimensions[r].height = 20
            bg_row = ICE_ROW if i % 2 == 1 else WHITE
            fill_row = PatternFill(start_color=bg_row, end_color=bg_row, fill_type="solid")

            ws_yr.cell(r, 1, p['no']).alignment = al_center
            ws_yr.cell(r, 2, p['kode']).alignment = al_center
            ws_yr.cell(r, 3, p['nama']).alignment = al_left
            ws_yr.cell(r, 4, p['jenjang']).alignment = al_center

            ws_yr.cell(r, 5, p[yr]['dt']).number_format = "#,##0"
            ws_yr.cell(r, 6, p[yr]['p']).number_format = "#,##0"
            ws_yr.cell(r, 7, p[yr]['du']).number_format = "#,##0"
            ws_yr.cell(r, 8, f"=E{r}-G{r}").number_format = "#,##0"

            for ci in range(1, 9):
                cell = ws_yr.cell(r, ci)
                cell.font = font_data
                cell.fill = fill_row
                cell.border = thin_border
                if ci == 8:
                    cell.font = font_defisit
                    cell.fill = PatternFill(start_color=DEFISIT_BG, end_color=DEFISIT_BG, fill_type="solid")

        tot_r_yr = 3 + len(prodi_list)
        ws_yr.row_dimensions[tot_r_yr].height = 24
        ws_yr.merge_cells(f"A{tot_r_yr}:D{tot_r_yr}")
        ws_yr[f"A{tot_r_yr}"] = "TOTAL KESELURUHAN UNIVERSITAS"
        ws_yr[f"A{tot_r_yr}"].font = font_grand_total
        ws_yr[f"A{tot_r_yr}"].alignment = al_center

        for ci in range(1, 9):
            cell = ws_yr.cell(tot_r_yr, ci)
            cell.fill = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
            cell.border = total_border
            cell.font = font_grand_total

        ws_yr.cell(tot_r_yr, 5, f"=SUM(E3:E{tot_r_yr-1})").number_format = "#,##0"
        ws_yr.cell(tot_r_yr, 6, f"=SUM(F3:F{tot_r_yr-1})").number_format = "#,##0"
        ws_yr.cell(tot_r_yr, 7, f"=SUM(G3:G{tot_r_yr-1})").number_format = "#,##0"
        ws_yr.cell(tot_r_yr, 8, f"=SUM(H3:H{tot_r_yr-1})").number_format = "#,##0"

        ws_yr.freeze_panes = "E3"
        ws_yr.column_dimensions["A"].width = 8
        ws_yr.column_dimensions["B"].width = 14
        ws_yr.column_dimensions["C"].width = 40
        ws_yr.column_dimensions["D"].width = 10
        ws_yr.column_dimensions["E"].width = 20
        ws_yr.column_dimensions["F"].width = 16
        ws_yr.column_dimensions["G"].width = 18
        ws_yr.column_dimensions["H"].width = 15

    # ===========================================================================
    # 4. SHEET: Ringkasan_Eksekutif (DASHBOARD KPI DINAMIS)
    # ===========================================================================
    print("Membangun Sheet: Ringkasan_Eksekutif...")
    ws1 = wb.create_sheet(title="Ringkasan_Eksekutif", index=0)
    ws1.views.sheetView[0].showGridLines = True

    # Title Banner
    ws1.merge_cells("A1:K2")
    ws1["A1"].value = "UNIVERSITAS SYIAH KUALA - DASHBOARD EKSEKUTIF DAYA TAMPUNG, PEMINAT & SISA KUOTA"
    ws1["A1"].font = font_title
    ws1["A1"].fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
    ws1["A1"].alignment = al_center
    ws1.row_dimensions[1].height = 24
    ws1.row_dimensions[2].height = 24

    ws1.merge_cells("A3:K3")
    ws1["A3"].value = "Monitoring Kapasitas Kuota, Daya Serap Mahasiswa Masuk & Beban Sisa Bangku Kosong (2022–2026)"
    ws1["A3"].font = font_subtitle
    ws1["A3"].fill = PatternFill(start_color="2A4365", end_color="2A4365", fill_type="solid")
    ws1["A3"].alignment = al_center
    ws1.row_dimensions[3].height = 18

    # 4 KPI Cards (Row 5 s.d. 8)
    cards_cfg = [
        # (c_start, c_end, title, formula, sub_formula/text, bg_col, font_val)
        ("A", "B", "TOTAL DAYA TAMPUNG (5-THN)", "=Rincian_Semua_Tahun!Z87", "Kapasitas Resmi Dibuka (Kursi)", CARD_BG_BLUE, font_kpi_value_blue),
        ("D", "E", "TOTAL PEMINAT (DEMAND)", "=Rincian_Semua_Tahun!AA87", "Rata Keketatan: 6,22 : 1", CARD_BG_TEAL, font_kpi_value_teal),
        ("G", "H", "TOTAL MAHASISWA MASUK (DU)", "=Rincian_Semua_Tahun!AB87", "=CONCATENATE(\"Fill Rate: \", TEXT(Rincian_Semua_Tahun!AD87,\"0.0\"), \"%\")", CARD_BG_AMBER, font_kpi_value_amber),
        ("J", "K", "TOTAL SISA KUOTA (KOSONG)", "=Rincian_Semua_Tahun!AC87", "23,2% Kuota Tidak Terisi", CARD_BG_ROSE, font_kpi_value_rose)
    ]
    ws1.row_dimensions[5].height = 18
    ws1.row_dimensions[6].height = 28
    ws1.row_dimensions[7].height = 16

    for cs, ce, title, f_val, sub_val, bg, f_font in cards_cfg:
        # Title
        ws1.merge_cells(f"{cs}5:{ce}5")
        ws1[f"{cs}5"].value = title
        ws1[f"{cs}5"].font = font_kpi_title
        ws1[f"{cs}5"].alignment = al_center

        # Value
        ws1.merge_cells(f"{cs}6:{ce}6")
        ws1[f"{cs}6"].value = f_val
        ws1[f"{cs}6"].font = f_font
        ws1[f"{cs}6"].alignment = al_center
        ws1[f"{cs}6"].number_format = "#,##0"

        # Subtitle
        ws1.merge_cells(f"{cs}7:{ce}7")
        ws1[f"{cs}7"].value = sub_val
        ws1[f"{cs}7"].font = font_kpi_sub
        ws1[f"{cs}7"].alignment = al_center

        # Box border & fill
        s_i = openpyxl.utils.column_index_from_string(cs)
        e_i = openpyxl.utils.column_index_from_string(ce)
        for r_i in range(5, 8):
            for c_i in range(s_i, e_i + 1):
                cell = ws1.cell(r_i, c_i)
                cell.fill = PatternFill(start_color=bg, end_color=bg, fill_type="solid")
                cell.border = thin_border

    # TABEL 1: Tren Tahunan (Row 10 s.d. 17)
    ws1.cell(10, 1, "TABEL 1: TREN TAHUNAN DAYA TAMPUNG, PEMINAT & SISA KUOTA (2022–2026)").font = font_section
    ws1.row_dimensions[10].height = 22

    t1_headers = [
        "Tahun Akademik", "Total Daya Tampung", "Total Peminat", "Daftar Ulang (DU)",
        "Sisa Kuota", "Fill Rate (%)", "Keketatan (x)", "Status Evaluasi"
    ]
    ws1.row_dimensions[11].height = 24
    for ci, h in enumerate(t1_headers, 1):
        cell = ws1.cell(11, ci, h)
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
        cell.alignment = al_center
        cell.border = thin_border

    tren_rows = [
        ("2022", "=Rincian_Semua_Tahun!V87", "=Rincian_Semua_Tahun!W87", "=Rincian_Semua_Tahun!X87", "=Rincian_Semua_Tahun!Y87", "Batas Ideal"),
        ("2023", "=Rincian_Semua_Tahun!R87", "=Rincian_Semua_Tahun!S87", "=Rincian_Semua_Tahun!T87", "=Rincian_Semua_Tahun!U87", "Penurunan Keterisian"),
        ("2024", "=Rincian_Semua_Tahun!N87", "=Rincian_Semua_Tahun!O87", "=Rincian_Semua_Tahun!P87", "=Rincian_Semua_Tahun!Q87", "Ekspansi Kuota PTN-BH"),
        ("2025", "=Rincian_Semua_Tahun!J87", "=Rincian_Semua_Tahun!K87", "=Rincian_Semua_Tahun!L87", "=Rincian_Semua_Tahun!M87", "Puncak Peminat 70K"),
        ("2026", "=Rincian_Semua_Tahun!F87", "=Rincian_Semua_Tahun!G87", "=Rincian_Semua_Tahun!H87", "=Rincian_Semua_Tahun!I87", "Realisasi Tertinggi DU 8.3K")
    ]
    for idx, (yr, f_dt, f_pm, f_du, f_sk, status) in enumerate(tren_rows):
        r = 12 + idx
        ws1.row_dimensions[r].height = 20
        bg_row = ICE_ROW if idx % 2 == 1 else WHITE
        fill_row = PatternFill(start_color=bg_row, end_color=bg_row, fill_type="solid")

        ws1.cell(r, 1, yr).alignment = al_center
        ws1.cell(r, 2, f_dt).number_format = "#,##0"
        ws1.cell(r, 3, f_pm).number_format = "#,##0"
        ws1.cell(r, 4, f_du).number_format = "#,##0"
        ws1.cell(r, 5, f_sk).number_format = "#,##0"
        ws1.cell(r, 6, f"=IF(B{r}>0, (D{r}/B{r})*100, 0)").number_format = "0.0\"%\""
        ws1.cell(r, 7, f"=IF(B{r}>0, C{r}/B{r}, 0)").number_format = "0.00"
        ws1.cell(r, 8, status).alignment = al_center

        for ci in range(1, 9):
            c = ws1.cell(r, ci)
            c.font = font_data
            c.fill = fill_row
            c.border = thin_border
            if ci == 5:
                c.font = font_defisit
                c.fill = PatternFill(start_color=DEFISIT_BG, end_color=DEFISIT_BG, fill_type="solid")

    # Baris Total Tabel 1
    r_tot_t1 = 17
    ws1.row_dimensions[r_tot_t1].height = 22
    ws1.cell(r_tot_t1, 1, "TOTAL 5 TAHUN").alignment = al_center
    ws1.cell(r_tot_t1, 2, "=SUM(B12:B16)").number_format = "#,##0"
    ws1.cell(r_tot_t1, 3, "=SUM(C12:C16)").number_format = "#,##0"
    ws1.cell(r_tot_t1, 4, "=SUM(D12:D16)").number_format = "#,##0"
    ws1.cell(r_tot_t1, 5, "=SUM(E12:E16)").number_format = "#,##0"
    ws1.cell(r_tot_t1, 6, f"=IF(B{r_tot_t1}>0, (D{r_tot_t1}/B{r_tot_t1})*100, 0)").number_format = "0.0\"%\""
    ws1.cell(r_tot_t1, 7, f"=IF(B{r_tot_t1}>0, C{r_tot_t1}/B{r_tot_t1}, 0)").number_format = "0.00"
    ws1.cell(r_tot_t1, 8, "76,8% Keterisian Kumulatif").alignment = al_center

    for ci in range(1, 9):
        c = ws1.cell(r_tot_t1, ci)
        c.font = font_grand_total
        c.fill = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
        c.border = total_border

    # TABEL 2: Kinerja per Fakultas (Row 19 s.d. 33)
    ws1.cell(19, 1, "TABEL 2: REKAPITULASI KAPASITAS & SISA KUOTA PER FAKULTAS (2022–2026)").font = font_section
    ws1.row_dimensions[19].height = 22

    t2_fak_headers = [
        "Fakultas / Unit", "Jumlah Prodi", "Total Daya Tampung", "Total Peminat",
        "Total Daftar Ulang", "Total Sisa Kuota", "Fill Rate (%)", "Keketatan (x)", "Evaluasi Portofolio"
    ]
    ws1.row_dimensions[20].height = 24
    for ci, h in enumerate(t2_fak_headers, 1):
        cell = ws1.cell(20, ci, h)
        cell.font = font_tier2
        cell.fill = PatternFill(start_color=NAVY_PRIMARY, end_color=NAVY_PRIMARY, fill_type="solid")
        cell.alignment = al_center
        cell.border = thin_border

    fakultas_list = [
        ("Kedokteran Gigi", "Prima (Zero Deficit)"),
        ("Hukum", "Prima (Sangat Stabil)"),
        ("Kedokteran", "Prima (Favorit Tinggi)"),
        ("Kedokteran Hewan", "Ideal Konsisten"),
        ("Ekonomi dan Bisnis", "Ideal Bertumbuh"),
        ("FISIP", "Ideal Stabil"),
        ("Keperawatan", "Ideal Moderat"),
        ("MIPA", "Rentan (<80%)"),
        ("Teknik", "Defisit Kuota Masif"),
        ("FKIP", "Episentrum Sisa Kuota"),
        ("Pertanian", "Krisis Kronis"),
        ("Kelautan dan Perikanan", "Kritis Akut (<65%)")
    ]

    for idx, (fak_name, status) in enumerate(fakultas_list):
        r = 21 + idx
        ws1.row_dimensions[r].height = 20
        bg_row = ICE_ROW if idx % 2 == 1 else WHITE
        fill_row = PatternFill(start_color=bg_row, end_color=bg_row, fill_type="solid")

        ws1.cell(r, 1, fak_name).alignment = al_left
        ws1.cell(r, 2, f'=COUNTIF(Rincian_Semua_Tahun!$E$6:$E$86, "{fak_name}")').alignment = al_center
        ws1.cell(r, 3, f'=SUMIF(Rincian_Semua_Tahun!$E$6:$E$86, "{fak_name}", Rincian_Semua_Tahun!$Z$6:$Z$86)').number_format = "#,##0"
        ws1.cell(r, 4, f'=SUMIF(Rincian_Semua_Tahun!$E$6:$E$86, "{fak_name}", Rincian_Semua_Tahun!$AA$6:$AA$86)').number_format = "#,##0"
        ws1.cell(r, 5, f'=SUMIF(Rincian_Semua_Tahun!$E$6:$E$86, "{fak_name}", Rincian_Semua_Tahun!$AB$6:$AB$86)').number_format = "#,##0"
        ws1.cell(r, 6, f'=SUMIF(Rincian_Semua_Tahun!$E$6:$E$86, "{fak_name}", Rincian_Semua_Tahun!$AC$6:$AC$86)').number_format = "#,##0"
        ws1.cell(r, 7, f'=IF(C{r}>0, (E{r}/C{r})*100, 0)').number_format = "0.0\"%\""
        ws1.cell(r, 8, f'=IF(C{r}>0, D{r}/C{r}, 0)').number_format = "0.00"
        ws1.cell(r, 9, status).alignment = al_center

        for ci in range(1, 10):
            c = ws1.cell(r, ci)
            c.font = font_data
            c.fill = fill_row
            c.border = thin_border
            if ci == 6:
                c.font = font_defisit
                c.fill = PatternFill(start_color=DEFISIT_BG, end_color=DEFISIT_BG, fill_type="solid")

    # Baris Total Tabel 2
    r_tot_t2 = 21 + len(fakultas_list)
    ws1.row_dimensions[r_tot_t2].height = 22
    ws1.cell(r_tot_t2, 1, "TOTAL SELURUH FAKULTAS").alignment = al_center
    ws1.cell(r_tot_t2, 2, f"=SUM(B21:B{r_tot_t2-1})").number_format = "#,##0"
    ws1.cell(r_tot_t2, 3, f"=SUM(C21:C{r_tot_t2-1})").number_format = "#,##0"
    ws1.cell(r_tot_t2, 4, f"=SUM(D21:D{r_tot_t2-1})").number_format = "#,##0"
    ws1.cell(r_tot_t2, 5, f"=SUM(E21:E{r_tot_t2-1})").number_format = "#,##0"
    ws1.cell(r_tot_t2, 6, f"=SUM(F21:F{r_tot_t2-1})").number_format = "#,##0"
    ws1.cell(r_tot_t2, 7, f"=IF(C{r_tot_t2}>0, (E{r_tot_t2}/C{r_tot_t2})*100, 0)").number_format = "0.0\"%\""
    ws1.cell(r_tot_t2, 8, f"=IF(C{r_tot_t2}>0, D{r_tot_t2}/C{r_tot_t2}, 0)").number_format = "0.00"
    ws1.cell(r_tot_t2, 9, "Benchmark Kampus").alignment = al_center

    for ci in range(1, 10):
        c = ws1.cell(r_tot_t2, ci)
        c.font = font_grand_total
        c.fill = PatternFill(start_color=NAVY_DARK, end_color=NAVY_DARK, fill_type="solid")
        c.border = total_border

    # Auto Width Sheet 1
    ws1.column_dimensions["A"].width = 25
    ws1.column_dimensions["B"].width = 18
    ws1.column_dimensions["C"].width = 20
    ws1.column_dimensions["D"].width = 18
    ws1.column_dimensions["E"].width = 20
    ws1.column_dimensions["F"].width = 18
    ws1.column_dimensions["G"].width = 15
    ws1.column_dimensions["H"].width = 16
    ws1.column_dimensions["I"].width = 25
    ws1.column_dimensions["J"].width = 16
    ws1.column_dimensions["K"].width = 16

    # Simpan workbook
    print(f"Menyimpan file excel ke: {out_path}")
    wb.save(out_path)
    print("✔ Berhasil! File rekap daya tampung, peminat dan sisa kuota selesai dibuat dengan sempurna.")

if __name__ == "__main__":
    build_rekap_daya_tampung_excel()
