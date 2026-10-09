import os
import json
import base64
import pandas as pd
import numpy as np

def generate_interactive_html():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    project_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung")
    excel_path = os.path.join(project_dir, "data", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    html_output_path = os.path.join(project_dir, "matriks_interaktif_kuadran_usk.html")

    if not os.path.exists(excel_path):
        print(f"File {excel_path} tidak ditemukan!")
        return

    print("Membaca data Excel S1 Kampus Utama dan Diploma 3 Vokasi...")
    df_s1 = pd.read_excel(excel_path, sheet_name="S1_Kampus_Utama")
    df_d3 = pd.read_excel(excel_path, sheet_name="Diploma_3_Vokasi")

    fak_abbr_map = {
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

    # ----------------------------------------------------
    # 1. PROCESS S1 DATA (66 Program Studi)
    # ----------------------------------------------------
    s1_data = []
    for idx, r in df_s1.iterrows():
        p_name = str(r['Nama Program Studi']).strip()
        fak = str(r['Fakultas']).strip()
        fak_abbr = fak_abbr_map.get(fak, fak)

        keketatan = round(float(r['Rata Keketatan 5-Thn']), 2)
        raw_fill_rate = round(float(r['Rata Fill Rate 5-Thn (%)']), 1)
        fill_rate = min(raw_fill_rate, 100.0) # Cap at 100.0%

        peminat_5thn = round(float(r['Rata Peminat 5-Thn']), 1)
        dt_5thn = round(float(r['Rata DT 5-Thn']), 1)
        du_5thn = round(float(r['Rata DU 5-Thn']), 1)
        sisa_kursi_5thn = max(0.0, round(dt_5thn - du_5thn, 1)) # No negative deficit
        tren_resmi = str(r.get('Klasifikasi Tren Resmi', 'Tren Stabil')).strip()
        klaster = str(r.get('Klaster Analisis', 'Reguler')).strip()

        # Klasifikasi Kuadran S1 (Ambang Standar: 4.0x & 80%)
        if keketatan >= 4.0 and fill_rate >= 80.0:
            kuadran = "I"
            kuadran_title = "KUADRAN I: UNGGULAN"
            kuadran_desc = "Peminat Tinggi & Daya Serap Kuota Penuh (Prima)"
            color = "#059669" # Emerald Green
            rekomendasi = (
                "Pertahankan standar kualitas seleksi tinggi. Alokasi daya tampung dapat dinaikkan selektif "
                "(5–10%) jika kapasitas laboratorium dan rasio dosen mencukupi, mengingat animo pasar yang sangat kuat."
            )
        elif keketatan < 4.0 and fill_rate >= 80.0:
            kuadran = "II"
            kuadran_title = "KUADRAN II: STABIL"
            kuadran_desc = "Kompetisi Moderat, Namun Kuota Terserap Optimal"
            color = "#2563EB" # Royal Blue
            rekomendasi = (
                "Pertahankan kuota tetap stabil. Tingkatkan branding dan promosi ke sekolah mitra di luar Aceh "
                "untuk mendongkrak rasio keketatan seleksi menuju ambang kompetitif (>= 4,0 : 1)."
            )
        elif keketatan >= 4.0 and fill_rate < 80.0:
            kuadran = "III"
            kuadran_title = "KUADRAN III: BELUM OPTIMAL"
            kuadran_desc = "Peminat Sangat Tinggi, Namun Daftar Ulang Belum Optimal"
            color = "#D97706" # Amber
            rekomendasi = (
                "Investigasi mendalam penyebab kebocoran registrasi ulang (yield loss). Evaluasi penyesuaian "
                "kelompok UKT, tinjau waktu pengumuman, dan perketat komitmen calon mahasiswa pada jalur mandiri/SNBT."
            )
        else:
            kuadran = "IV"
            kuadran_title = "KUADRAN IV: PERLU DITINGKATKAN"
            kuadran_desc = "Peminat Rendah & Kuota Kerap Tidak Terisi Penuh"
            color = "#E11D48" # Rose Red
            rekomendasi = (
                "Prioritas restrukturisasi kurikulum dan modernisasi profil lulusan agar relevan dengan kebutuhan industri. "
                "Pertimbangkan rasionalisasi daya tampung (downsizing kuota 15–25%) guna menyehatkan fill rate dan efisiensi operasional."
            )

        # Riwayat Tahunan 2022-2026 dengan Capping 100%
        history = []
        for yr in [2022, 2023, 2024, 2025, 2026]:
            try:
                pem_y = int(r[f'Peminat {yr}']) if pd.notna(r.get(f'Peminat {yr}')) else 0
                dt_y = int(r[f'Daya Tampung {yr}']) if pd.notna(r.get(f'Daya Tampung {yr}')) else 0
                du_y = int(r[f'Daftar Ulang {yr}']) if pd.notna(r.get(f'Daftar Ulang {yr}')) else 0
                raw_fr_y = round(float(r[f'Fill Rate {yr} (%)']), 1) if pd.notna(r.get(f'Fill Rate {yr} (%)')) else 0.0
                fr_y = min(raw_fr_y, 100.0) # Capped at 100%
                kek_y = round(float(r[f'Keketatan {yr}']), 2) if pd.notna(r.get(f'Keketatan {yr}')) else 0.0
                history.append({
                    "tahun": yr,
                    "peminat": pem_y,
                    "dt": dt_y,
                    "du": du_y,
                    "fill_rate": fr_y,
                    "keketatan": kek_y
                })
            except Exception:
                pass

        s1_data.append({
            "id": idx + 1,
            "jenjang": "S1",
            "nama": p_name,
            "fakultas": fak,
            "fakultas_abbr": fak_abbr,
            "kuadran": kuadran,
            "kuadran_title": kuadran_title,
            "kuadran_desc": kuadran_desc,
            "color": color,
            "keketatan": keketatan,
            "fill_rate": fill_rate,
            "peminat_5thn": peminat_5thn,
            "dt_5thn": dt_5thn,
            "du_5thn": du_5thn,
            "sisa_5thn": sisa_kursi_5thn,
            "tren_resmi": tren_resmi,
            "klaster": klaster,
            "is_prodi_baru": bool(tren_resmi == "Data Terbatas (Prodi Baru)"),
            "history": history
        })

    # ----------------------------------------------------
    # 2. PROCESS D3 DATA (11 Program Studi Vokasi)
    # ----------------------------------------------------
    d3_data = []
    for idx, r in df_d3.iterrows():
        p_name = str(r['Nama Program Studi']).strip()
        fak = str(r['Fakultas']).strip()
        fak_abbr = fak_abbr_map.get(fak, fak)

        keketatan = round(float(r['Rata Keketatan 5-Thn']), 2)
        raw_fill_rate = round(float(r['Rata Fill Rate 5-Thn (%)']), 1)
        fill_rate = min(raw_fill_rate, 100.0)

        peminat_5thn = round(float(r['Rata Peminat 5-Thn']), 1)
        dt_5thn = round(float(r['Rata DT 5-Thn']), 1)
        du_5thn = round(float(r['Rata DU 5-Thn']), 1)
        sisa_kursi_5thn = max(0.0, round(dt_5thn - du_5thn, 1))
        tren_resmi = str(r.get('Klasifikasi Tren Resmi', 'Tren Stabil')).strip()
        klaster = str(r.get('Klaster Analisis', 'Vokasi')).strip()

        # Seluruh 11 D3 berada di Kuadran III secara formal (Keketatan >= 4.0x & Fill Rate < 80%)
        # Diselaraskan 100% dengan standar S1: KUADRAN III: BELUM OPTIMAL
        kuadran = "III"
        kuadran_title = "KUADRAN III: BELUM OPTIMAL"
        kuadran_desc = "Peminat Sangat Tinggi, Namun Daftar Ulang Belum Optimal"

        # Sub-klasifikasi berdasarkan 3 Klaster Evaluasi Vokasi:
        if fill_rate >= 60.0:
            tier = 1
            tier_title = "KLASTER 1: KOMPETITIF"
            tier_desc = "Daya Saing Tinggi: Fill Rate Prima (≥ 60%) & Peminat Membludak"
            color = "#059669" # Emerald Green
            rekomendasi = (
                "Prioritas #1 untuk segera dikonversi dan dinaikkan statusnya menjadi Sarjana Terapan "
                "(D4 Rekayasa Perangkat Lunak / TI). Animo pasar sangat tinggi (1.100 mhs/thn) dengan daya serap terbaik di vokasi USK (66,6%)."
            )
        elif fill_rate >= 45.0:
            tier = 2
            tier_title = "KLASTER 2: PERLU PENDAMPINGAN"
            tier_desc = "Keterisian Moderat (45%–55%), Memerlukan Pendampingan Strategis"
            color = "#D97706" # Amber
            rekomendasi = (
                "Kandidat konversi ke Sarjana Terapan (D4) dengan restrukturisasi kurikulum berbasis kemitraan industri "
                "(teaching factory). Perkuat skema ikatan kerja agar pendaftar tidak gugur massal saat tahap daftar ulang."
            )
        else:
            tier = 3
            tier_title = "KLASTER 3: EVALUASI KHUSUS"
            tier_desc = "Keterisian Kritis (< 45%), Memerlukan Evaluasi Restrukturisasi"
            color = "#DC2626" # Crimson Red
            rekomendasi = (
                "Evaluasi kelayakan operasional mendesak. Lakukan rasionalisasi daya tampung drastis (pangkas kuota 40%–50%) "
                "untuk menghentikan akumulasi bangku kosong (>150 kursi/thn), atau pertimbangkan moratorium/merger prodi jika defisit terus berlanjut."
            )

        # Riwayat Tahunan D3 2022-2026
        history = []
        for yr in [2022, 2023, 2024, 2025, 2026]:
            try:
                pem_y = int(r[f'Peminat {yr}']) if pd.notna(r.get(f'Peminat {yr}')) else 0
                dt_y = int(r[f'Daya Tampung {yr}']) if pd.notna(r.get(f'Daya Tampung {yr}')) else 0
                du_y = int(r[f'Daftar Ulang {yr}']) if pd.notna(r.get(f'Daftar Ulang {yr}')) else 0
                raw_fr_y = round(float(r[f'Fill Rate {yr} (%)']), 1) if pd.notna(r.get(f'Fill Rate {yr} (%)')) else 0.0
                fr_y = min(raw_fr_y, 100.0)
                kek_y = round(float(r[f'Keketatan {yr}']), 2) if pd.notna(r.get(f'Keketatan {yr}')) else 0.0
                history.append({
                    "tahun": yr,
                    "peminat": pem_y,
                    "dt": dt_y,
                    "du": du_y,
                    "fill_rate": fr_y,
                    "keketatan": kek_y
                })
            except Exception:
                pass

        d3_data.append({
            "id": 100 + idx + 1,
            "jenjang": "D3",
            "nama": p_name,
            "fakultas": fak,
            "fakultas_abbr": fak_abbr,
            "kuadran": kuadran,
            "tier": tier,
            "tier_title": tier_title,
            "tier_desc": tier_desc,
            "kuadran_title": kuadran_title,
            "kuadran_desc": kuadran_desc,
            "color": color,
            "keketatan": keketatan,
            "fill_rate": fill_rate,
            "peminat_5thn": peminat_5thn,
            "dt_5thn": dt_5thn,
            "du_5thn": du_5thn,
            "sisa_5thn": sisa_kursi_5thn,
            "tren_resmi": tren_resmi,
            "klaster": klaster,
            "history": history
        })

    # Read and encode USK logo
    logo_path = os.path.join(project_dir, "image", "usk-logo.png")
    usk_logo_b64 = "image/usk-logo.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            b64_str = base64.b64encode(f.read()).decode("utf-8")
            usk_logo_b64 = f"data:image/png;base64,{b64_str}"

    print(f"Total S1: {len(s1_data)} prodi, Total D3: {len(d3_data)} prodi.")
    dataset_payload = {
        "s1": s1_data,
        "d3": d3_data
    }
    json_data = json.dumps(dataset_payload, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Peta Portofolio Program Studi USK (2022–2026) — Dashboard Interaktif Eksekutif</title>
    <link rel="icon" type="image/png" href="{usk_logo_b64}">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-page: #F8FAFC;
            --bg-surface: #FFFFFF;
            --bg-card: #FFFFFF;
            --border-subtle: #E2E8F0;
            --border-strong: #CBD5E1;
            --text-main: #0F172A;
            --text-muted: #64748B;
            --text-subtle: #94A3B8;

            --q1-color: #059669;
            --q1-bg: #F0FDF4;
            --q1-border: #BBF7D0;

            --q2-color: #2563EB;
            --q2-bg: #EFF6FF;
            --q2-border: #BFDBFE;

            --q3-color: #D97706;
            --q3-bg: #FFFBEB;
            --q3-border: #FDE68A;

            --q4-color: #E11D48;
            --q4-bg: #FFF1F2;
            --q4-border: #FECDD3;

            --shadow-sm: 0 1px 3px rgba(15, 23, 42, 0.05);
            --shadow-md: 0 4px 12px -2px rgba(15, 23, 42, 0.08), 0 2px 6px -1px rgba(15, 23, 42, 0.04);
            --shadow-lg: 0 12px 28px -4px rgba(15, 23, 42, 0.12), 0 4px 12px -2px rgba(15, 23, 42, 0.06);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-page);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            overflow-x: hidden;
        }}

        /* Header Bar */
        header.top-header {{
            background: #FFFFFF;
            border-bottom: 1px solid var(--border-subtle);
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 50;
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
            gap: 10px;
        }}

        .brand-area {{
            display: flex;
            align-items: center;
            gap: 14px;
        }}

        .usk-header-logo {{
            height: 44px;
            width: auto;
            max-width: 130px;
            object-fit: contain;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }}

        .brand-divider {{
            width: 1px;
            height: 36px;
            background: var(--border-subtle);
        }}

        .brand-titles h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 15.5px;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.25;
            letter-spacing: -0.25px;
            white-space: nowrap;
        }}

        .brand-titles p {{
            font-size: 10.8px;
            letter-spacing: -0.15px;
            color: var(--text-muted);
            margin-top: 2px;
            font-weight: 500;
            white-space: nowrap;
        }}

        /* LEVEL SWITCHER (Segmented Control Tabs) */
        .level-switcher {{
            display: inline-flex;
            align-items: center;
            background: #F1F5F9;
            padding: 3px;
            border-radius: 28px;
            border: 1px solid var(--border-subtle);
            gap: 3px;
        }}

        .level-tab {{
            border: none;
            background: transparent;
            padding: 6px 14px;
            border-radius: 22px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12.5px;
            font-weight: 700;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .level-tab:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.6);
        }}

        .level-tab.active {{
            background: #1E3A8A;
            color: #FFFFFF;
            box-shadow: 0 4px 12px rgba(30, 58, 138, 0.25);
        }}

        .tab-badge {{
            font-size: 11px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 12px;
            background: rgba(0, 0, 0, 0.08);
            color: inherit;
        }}

        .level-tab.active .tab-badge {{
            background: rgba(255, 255, 255, 0.22);
            color: #FFFFFF;
        }}

        /* S1 SUBSET SWITCHER */
        .s1-subset-switcher {{
            display: inline-flex;
            align-items: center;
            background: #F8FAFC;
            padding: 3px;
            border-radius: 24px;
            border: 1px solid #CBD5E1;
            gap: 4px;
            transition: all 0.25s ease;
        }}

        .subset-tab {{
            border: none;
            background: transparent;
            padding: 5px 12px;
            border-radius: 18px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 11.5px;
            font-weight: 700;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 5px;
            white-space: nowrap;
        }}

        .subset-tab:hover {{
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.85);
        }}

        .subset-tab.active {{
            background: #0284C7;
            color: #FFFFFF;
            box-shadow: 0 2px 8px rgba(2, 132, 199, 0.32);
        }}

        .canvas-footnote {{
            padding: 10px 16px;
            font-size: 11.5px;
            font-style: italic;
            color: #475569;
            background: #F8FAFC;
            border-top: 1px dashed #CBD5E1;
            border-radius: 0 0 12px 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 6px 12px;
            font-size: 12px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            border: 1px solid transparent;
            white-space: nowrap;
        }}

        .btn-outline {{
            background: #FFFFFF;
            border-color: var(--border-strong);
            color: var(--text-main);
        }}

        .btn-outline:hover {{
            background: #F1F5F9;
            border-color: #94A3B8;
        }}

        .btn-outline.active {{
            background: #1E3A8A;
            border-color: #1E3A8A;
            color: #FFFFFF;
        }}

        .btn-primary {{
            background: #2563EB;
            color: #FFFFFF;
        }}

        .btn-primary:hover {{
            background: #1D4ED8;
        }}

        /* KPI Quick Stat Ribbon */
        .kpi-ribbon {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
            padding: 16px 28px 0 28px;
        }}

        .kpi-card {{
            background: var(--bg-surface);
            border-radius: 12px;
            padding: 14px 18px;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-sm);
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }}

        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}

        .kpi-card.active {{
            outline: 2px solid;
            box-shadow: var(--shadow-md);
        }}

        .kpi-card.c-emerald {{ border-left: 4px solid #059669; }}
        .kpi-card.c-emerald.active {{ outline-color: #059669; }}

        .kpi-card.c-blue {{ border-left: 4px solid #2563EB; }}
        .kpi-card.c-blue.active {{ outline-color: #2563EB; }}

        .kpi-card.c-amber {{ border-left: 4px solid #D97706; }}
        .kpi-card.c-amber.active {{ outline-color: #D97706; }}

        .kpi-card.c-rose {{ border-left: 4px solid #E11D48; }}
        .kpi-card.c-rose.active {{ outline-color: #E11D48; }}

        .kpi-card.c-crimson {{ border-left: 4px solid #DC2626; }}
        .kpi-card.c-crimson.active {{ outline-color: #DC2626; }}

        .kpi-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}

        .kpi-label {{
            font-size: 11.5px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .kpi-val-row {{
            display: flex;
            align-items: baseline;
            gap: 8px;
        }}

        .kpi-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 26px;
            font-weight: 800;
            line-height: 1.1;
        }}

        .kpi-sub {{
            font-size: 12px;
            font-weight: 600;
            color: var(--text-muted);
        }}

        .kpi-note {{
            font-size: 11px;
            color: var(--text-muted);
            margin-top: 4px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        /* Search & Filter Bar */
        .controls-strip {{
            padding: 14px 28px;
            display: flex;
            gap: 16px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .search-box {{
            flex: 1;
            min-width: 280px;
            max-width: 440px;
            position: relative;
        }}

        .search-box input {{
            width: 100%;
            padding: 9px 38px 9px 38px;
            border-radius: 10px;
            border: 1px solid var(--border-strong);
            background: #FFFFFF;
            font-size: 13px;
            font-family: inherit;
            color: var(--text-main);
            transition: all 0.2s ease;
        }}

        .search-box input:focus {{
            outline: none;
            border-color: #2563EB;
            box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
        }}

        .search-icon {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 14px;
            color: var(--text-subtle);
            pointer-events: none;
        }}

        .search-clear-btn {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #E2E8F0;
            color: #64748B;
            border: none;
            cursor: pointer;
            display: none;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 700;
            line-height: 1;
            transition: all 0.15s ease;
            z-index: 2;
        }}

        .search-clear-btn:hover {{
            background: #CBD5E1;
            color: #0F172A;
            transform: translateY(-50%) scale(1.08);
        }}

        /* Search Dropdown Popover */
        .search-dropdown {{
            position: absolute;
            top: calc(100% + 6px);
            left: 0;
            right: 0;
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 12px;
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.14), 0 4px 10px rgba(15, 23, 42, 0.05);
            max-height: 320px;
            overflow-y: auto;
            z-index: 1000;
            display: none;
            padding: 6px;
        }}

        .search-dropdown::-webkit-scrollbar {{
            width: 6px;
        }}
        .search-dropdown::-webkit-scrollbar-track {{
            background: #F8FAFC;
            border-radius: 6px;
        }}
        .search-dropdown::-webkit-scrollbar-thumb {{
            background: #CBD5E1;
            border-radius: 6px;
        }}
        .search-dropdown::-webkit-scrollbar-thumb:hover {{
            background: #94A3B8;
        }}

        .search-dropdown-item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 10px;
            padding: 8px 12px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.15s ease;
            user-select: none;
        }}

        .search-dropdown-item:hover,
        .search-dropdown-item.active-item {{
            background: #F1F5F9;
        }}

        .search-item-left {{
            display: flex;
            align-items: center;
            gap: 8px;
            min-width: 0;
            flex: 1;
        }}

        .search-item-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            flex-shrink: 0;
        }}

        .search-item-name {{
            font-size: 12.5px;
            font-weight: 700;
            color: #0F172A;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .search-item-badges {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-shrink: 0;
        }}

        .search-badge-fak {{
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            background: #F1F5F9;
            color: #475569;
            border: 1px solid #E2E8F0;
        }}

        .search-badge-quad {{
            font-size: 10px;
            font-weight: 800;
            padding: 2px 7px;
            border-radius: 6px;
            white-space: nowrap;
        }}

        .search-dropdown-empty {{
            padding: 16px 12px;
            text-align: center;
            font-size: 12px;
            color: #94A3B8;
            font-weight: 500;
        }}

        .filter-pills-row {{
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
            align-items: center;
        }}

        .filter-pill {{
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 11.5px;
            font-weight: 600;
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.15s ease;
            user-select: none;
        }}

        .filter-pill:hover {{
            background: #F1F5F9;
            color: var(--text-main);
        }}

        .filter-pill.active {{
            background: #0F172A;
            color: #FFFFFF;
            border-color: #0F172A;
            box-shadow: var(--shadow-sm);
        }}

        /* Workspace Grid */
        .workspace {{
            flex: 1;
            padding: 0 28px 24px 28px;
            display: grid;
            grid-template-columns: 1fr 390px;
            gap: 20px;
            align-items: start;
        }}

        .chart-container {{
            background: var(--bg-surface);
            border-radius: 16px;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-sm);
            padding: 20px;
            position: relative;
            display: flex;
            flex-direction: column;
        }}

        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .chart-title-group h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 17px;
            font-weight: 700;
            color: var(--text-main);
        }}

        .chart-title-group p {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 3px;
        }}

        /* D3 Sub-Tier Classification Legend Strip */
        .d3-tier-legend-strip {{
            display: none;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 12px;
            background: #F8FAFC;
            padding: 10px 12px;
            border-radius: 12px;
            border: 1px solid #E2E8F0;
        }}

        .tier-guide-card {{
            background: #FFFFFF;
            border-radius: 10px;
            padding: 12px 14px;
            border: 1px solid #E2E8F0;
            border-left-width: 4.5px;
            cursor: pointer;
            transition: all 0.22s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            flex-direction: column;
            gap: 6px;
            user-select: none;
        }}

        .tier-guide-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 14px rgba(0,0,0,0.08);
            border-color: #CBD5E1;
        }}

        .tier-guide-card.active {{
            box-shadow: 0 0 0 2px var(--brand-navy), 0 6px 14px rgba(15,23,42,0.12);
        }}

        .tier-guide-card.tg-tier-1 {{
            border-left-color: #059669;
        }}
        .tier-guide-card.tg-tier-1.active {{
            background: #F0FDF4;
            border-color: #86EFAC;
            border-left-color: #059669;
        }}

        .tier-guide-card.tg-tier-2 {{
            border-left-color: #D97706;
        }}
        .tier-guide-card.tg-tier-2.active {{
            background: #FFFBEB;
            border-color: #FDE68A;
            border-left-color: #D97706;
        }}

        .tier-guide-card.tg-tier-3 {{
            border-left-color: #DC2626;
        }}
        .tier-guide-card.tg-tier-3.active {{
            background: #FFF1F2;
            border-color: #FECDD3;
            border-left-color: #DC2626;
        }}

        .tgc-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .tgc-title-group {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12.5px;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
        }}

        .tg-tier-1 .tgc-title-group {{ color: #065F46; }}
        .tg-tier-2 .tgc-title-group {{ color: #92400E; }}
        .tg-tier-3 .tgc-title-group {{ color: #991B1B; }}

        .tgc-badge {{
            font-size: 10px;
            font-weight: 700;
            padding: 2.5px 7px;
            border-radius: 6px;
            background: #F1F5F9;
            color: #475569;
        }}

        .tgc-rule {{
            font-size: 11px;
            font-weight: 700;
            color: #1E293B;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .tgc-rule span.kriteria-tag {{
            font-size: 9px;
            font-weight: 800;
            text-transform: uppercase;
            padding: 2px 5px;
            border-radius: 4px;
            letter-spacing: 0.3px;
        }}
        .tg-tier-1 .tgc-rule span.kriteria-tag {{ background: #DCFCE7; color: #166534; }}
        .tg-tier-2 .tgc-rule span.kriteria-tag {{ background: #FEF3C7; color: #92400E; }}
        .tg-tier-3 .tgc-rule span.kriteria-tag {{ background: #FFE4E6; color: #9F1239; }}

        .tgc-prodi {{
            font-size: 11px;
            font-weight: 500;
            color: #334155;
            line-height: 1.45;
            margin-top: 2px;
        }}

        /* D3 Sub-Tier Executive Sidebar Card Styles */
        .d3-sidebar-card {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}

        .d3-sidebar-tier-block {{
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 11px 13px;
            transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            cursor: pointer;
        }}

        .d3-sidebar-tier-block:hover {{
            transform: translateY(-1.5px);
            box-shadow: 0 5px 12px rgba(0,0,0,0.07);
        }}

        .d3-stb-tier-1 {{
            border-left: 4.5px solid #059669;
            background: linear-gradient(180deg, #F0FDF4 0%, #FFFFFF 100%);
        }}

        .d3-stb-tier-2 {{
            border-left: 4.5px solid #D97706;
            background: linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 100%);
        }}

        .d3-stb-tier-3 {{
            border-left: 4.5px solid #DC2626;
            background: linear-gradient(180deg, #FFF1F2 0%, #FFFFFF 100%);
        }}

        .d3-stb-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 7px;
        }}

        .d3-stb-title {{
            font-size: 12px;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .d3-stb-tier-1 .d3-stb-title {{ color: #065F46; }}
        .d3-stb-tier-2 .d3-stb-title {{ color: #92400E; }}
        .d3-stb-tier-3 .d3-stb-title {{ color: #991B1B; }}

        .d3-stb-badges {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}

        .d3-stb-badge-fr {{
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 5px;
        }}

        .d3-stb-tier-1 .d3-stb-badge-fr {{ background: #DCFCE7; color: #166534; }}
        .d3-stb-tier-2 .d3-stb-badge-fr {{ background: #FEF3C7; color: #92400E; }}
        .d3-stb-tier-3 .d3-stb-badge-fr {{ background: #FFE4E6; color: #9F1239; }}

        .d3-stb-badge-count {{
            font-size: 10px;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 5px;
            background: #F1F5F9;
            color: #475569;
        }}

        .d3-prodi-chips {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}

        .d3-prodi-chip {{
            display: inline-flex;
            align-items: center;
            font-size: 10.5px;
            font-weight: 600;
            padding: 3.5px 8.5px;
            border-radius: 6px;
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            color: #334155;
            transition: all 0.15s ease;
            cursor: pointer;
        }}

        .d3-prodi-chip:hover {{
            transform: translateY(-1px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
        }}

        .d3-stb-tier-1 .d3-prodi-chip {{
            background: #F0FDF4;
            border-color: #A7F3D0;
            color: #065F46;
        }}
        .d3-stb-tier-1 .d3-prodi-chip:hover {{
            background: #DCFCE7;
            border-color: #34D399;
        }}

        .d3-stb-tier-2 .d3-prodi-chip {{
            background: #FFFDF5;
            border-color: #FDE68A;
            color: #78350F;
        }}
        .d3-stb-tier-2 .d3-prodi-chip:hover {{
            background: #FEF3C7;
            border-color: #FBBF24;
        }}

        .d3-stb-tier-3 .d3-prodi-chip {{
            background: #FFF5F5;
            border-color: #FECDD3;
            color: #881337;
        }}
        .d3-stb-tier-3 .d3-prodi-chip:hover {{
            background: #FFE4E6;
            border-color: #FB7185;
        }}

        .svg-wrapper {{
            position: relative;
            width: 100%;
            height: 590px;
            background: #FFFFFF;
            border-radius: 10px;
            overflow: visible;
        }}

        svg.main-svg {{
            width: 100%;
            height: 100%;
            overflow: visible;
        }}

        /* Dot styling & interactions */
        .dot {{
            cursor: pointer;
            transition: r 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), opacity 0.2s ease, stroke-width 0.2s ease;
        }}

        .dot:hover {{
            stroke-width: 3.5px !important;
            stroke: #0F172A !important;
        }}

        .dot.dimmed {{
            opacity: 0.12 !important;
            pointer-events: none;
        }}

        .dot.selected {{
            stroke: #0F172A !important;
            stroke-width: 4px !important;
        }}

        /* Anti-Collision Interactive Badges & Leader Lines */
        .leader-line {{
            pointer-events: none;
            transition: stroke 0.15s ease, stroke-width 0.15s ease, opacity 0.15s ease;
        }}

        .label-badge {{
            cursor: pointer;
            transition: transform 0.12s ease;
        }}

        .label-badge .badge-rect {{
            transition: stroke 0.15s ease, stroke-width 0.15s ease, filter 0.15s ease;
            filter: drop-shadow(0 1px 2px rgba(15, 23, 42, 0.08));
        }}

        .label-badge:hover .badge-rect,
        .label-badge.highlighted .badge-rect {{
            stroke-width: 1.8px !important;
            filter: drop-shadow(0 2px 6px rgba(15, 23, 42, 0.22));
        }}

        .label-badge.selected .badge-rect {{
            stroke-width: 2.0px !important;
            filter: drop-shadow(0 2px 8px rgba(15, 23, 42, 0.28));
        }}

        .label-badge .badge-text {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 8.5px;
            font-weight: 700;
            user-select: none;
            pointer-events: none;
        }}

        /* Floating Tooltip */
        #interactive-tooltip {{
            position: absolute;
            display: none;
            pointer-events: none;
            z-index: 100;
            background: rgba(15, 23, 42, 0.95);
            backdrop-filter: blur(10px);
            color: #FFFFFF;
            padding: 12px 16px;
            border-radius: 12px;
            box-shadow: var(--shadow-lg), 0 8px 24px rgba(15, 23, 42, 0.35);
            width: 260px;
            transform: translate(-50%, -100%);
            margin-top: -12px;
            border: 1px solid rgba(255, 255, 255, 0.18);
            transition: opacity 0.12s ease;
        }}

        #interactive-tooltip::after {{
            content: '';
            position: absolute;
            bottom: -6px;
            left: var(--arrow-left, 50%);
            transform: translateX(-50%);
            border-width: 6px 6px 0;
            border-style: solid;
            border-color: rgba(15, 23, 42, 0.95) transparent;
            display: block;
            width: 0;
        }}

        /* Smart Vertical Flipped Down Tooltip */
        #interactive-tooltip.flipped-down {{
            transform: translate(-50%, 0);
            margin-top: 14px;
        }}

        #interactive-tooltip.flipped-down::after {{
            bottom: auto;
            top: -6px;
            border-width: 0 6px 6px;
            border-color: transparent transparent rgba(15, 23, 42, 0.95);
        }}

        .tt-badge-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
        }}

        .tt-faculty {{
            font-size: 10.5px;
            font-weight: 800;
            text-transform: uppercase;
            color: #94A3B8;
        }}

        .tt-quadrant {{
            font-size: 10.5px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.15);
        }}

        .tt-prodi-name {{
            font-family: 'Outfit', sans-serif;
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.3;
        }}

        .tt-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px 12px;
            font-size: 11.5px;
            border-top: 1px solid rgba(255, 255, 255, 0.12);
            padding-top: 8px;
            margin-top: 4px;
        }}

        .tt-metric-label {{
            color: #94A3B8;
        }}

        .tt-metric-value {{
            font-weight: 700;
            color: #F8FAFC;
        }}

        .tt-hint {{
            font-size: 10px;
            color: #38BDF8;
            margin-top: 8px;
            text-align: center;
            font-weight: 500;
        }}

        /* Right Inspector Panel */
        .inspector-panel {{
            background: var(--bg-surface);
            border-radius: 16px;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-sm);
            padding: 22px;
            position: sticky;
            top: 92px;
        }}

        .inspector-placeholder {{
            text-align: center;
            padding: 46px 20px;
            color: var(--text-muted);
        }}

        .ins-placeholder-logo {{
            width: 72px;
            height: auto;
            margin-bottom: 16px;
            opacity: 0.9;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.06));
            transition: transform 0.3s ease;
        }}

        .inspector-placeholder:hover .ins-placeholder-logo {{
            transform: scale(1.05);
        }}

        .inspector-placeholder h3 {{
            font-family: 'Outfit', sans-serif;
            font-size: 16px;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 6px;
        }}

        .inspector-placeholder p {{
            font-size: 12px;
            line-height: 1.5;
            color: var(--text-muted);
        }}

        /* Inspector Content */
        .inspector-content {{
            display: none;
        }}

        .ins-header {{
            margin-bottom: 16px;
            padding-bottom: 14px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .ins-top-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }}

        .ins-fakultas-tag {{
            font-size: 11px;
            font-weight: 700;
            padding: 3px 9px;
            border-radius: 6px;
            background: #F1F5F9;
            color: #334155;
            border: 1px solid #E2E8F0;
        }}

        .ins-close-btn {{
            background: #F1F5F9;
            border: 1px solid #CBD5E1;
            color: #475569;
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.15s ease;
        }}
        .ins-close-btn:hover {{
            background: #E2E8F0;
            color: #0F172A;
            border-color: #94A3B8;
        }}

        .ins-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 19px;
            font-weight: 800;
            line-height: 1.25;
            color: var(--text-main);
            margin-bottom: 8px;
            letter-spacing: -0.2px;
        }}

        .ins-badges-row {{
            display: flex;
            align-items: center;
            gap: 6px;
            flex-wrap: wrap;
            margin-bottom: 8px;
        }}

        .ins-kuadran-tag {{
            font-size: 11px;
            font-weight: 700;
            padding: 3.5px 10px;
            border-radius: 20px;
            color: #FFFFFF;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
        }}

        .ins-tier-tag {{
            font-size: 11px;
            font-weight: 700;
            padding: 3.5px 9px;
            border-radius: 20px;
            white-space: nowrap;
            display: inline-flex;
            align-items: center;
            border: 1px solid transparent;
        }}

        .ins-sub {{
            font-size: 12px;
            color: #64748B;
            line-height: 1.5;
            font-weight: 500;
        }}

        .ins-kpi-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 18px;
        }}

        .ins-kpi-card {{
            background: #F8FAFC;
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            padding: 10px 12px;
        }}

        .ins-kpi-title {{
            font-size: 10.5px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .ins-kpi-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 2px;
        }}

        .ins-kpi-sub {{
            font-size: 10.5px;
            color: var(--text-subtle);
            margin-top: 2px;
        }}

        /* Annual Table */
        .ins-section-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-main);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .history-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 11.5px;
            margin-bottom: 18px;
        }}

        .history-table th {{
            background: #F1F5F9;
            color: #475569;
            font-weight: 700;
            text-align: left;
            padding: 7px 8px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .history-table td {{
            padding: 7px 8px;
            border-bottom: 1px solid var(--border-subtle);
            color: var(--text-main);
        }}

        .history-table tr:hover td {{
            background: #F8FAFC;
        }}

        /* Executive Recommendation Box */
        .rekomendasi-box {{
            background: #F0FDF4;
            border: 1px solid #BBF7D0;
            border-radius: 10px;
            padding: 14px;
            position: relative;
        }}

        .rekomendasi-box h4 {{
            font-family: 'Outfit', sans-serif;
            font-size: 12.5px;
            font-weight: 700;
            color: #065F46;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .rekomendasi-box p {{
            font-size: 12px;
            line-height: 1.5;
            color: #047857;
        }}

        /* Footer */
        footer.bottom-bar {{
            background: #FFFFFF;
            border-top: 1px solid var(--border-subtle);
            padding: 12px 28px;
            font-size: 11.5px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: auto;
        }}

        @media (max-width: 1100px) {{
            .workspace {{
                grid-template-columns: 1fr;
            }}
            .kpi-ribbon {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}

        @media print {{
            .controls-strip, header.top-header, footer.bottom-bar {{
                display: none;
            }}
            .workspace {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>

    <!-- TOP HEADER -->
    <header class="top-header">
        <div class="brand-area">
            <img src="{usk_logo_b64}" alt="Logo Universitas Syiah Kuala" class="usk-header-logo" />
            <div class="brand-divider"></div>
            <div class="brand-titles">
                <h1 id="header-main-title">PETA KUADRAN 60 PROGRAM STUDI S1 KAMPUS UTAMA USK</h1>
                <p id="header-sub-title">Direktorat Pendidikan dan Administrasi Akademik • Universitas Syiah Kuala (2022–2026)</p>
            </div>
        </div>

        <!-- NAVIGATION & SUBSET SWITCHER GROUP -->
        <div class="nav-controls-group" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <div class="level-switcher" id="level-switcher">
                <button class="level-tab active" data-level="s1" id="tab-s1">
                    🎓 S1 Sarjana <span class="tab-badge" id="tab-s1-badge">60 Prodi</span>
                </button>
                <button class="level-tab" data-level="d3" id="tab-d3">
                    🛠️ D3 Vokasi <span class="tab-badge">11 Prodi</span>
                </button>
            </div>

            <!-- S1 SUBSET SWITCHER (Hanya tampil saat Level S1 aktif) -->
            <div class="s1-subset-switcher" id="s1-subset-switcher">
                <button class="subset-tab" data-subset="all" id="subset-all" title="Tampilkan seluruh 66 program studi S1 termasuk prodi baru">
                    🌐 Semua Prodi S1 (66)
                </button>
                <button class="subset-tab active" data-subset="established" id="subset-established" title="Tampilkan 60 program studi S1 tanpa 6 prodi baru (data lengkap 5 tahun)">
                    🏛️ 60 Prodi S1 (Tanpa Prodi Baru)
                </button>
            </div>
        </div>

        <div class="header-actions">
            <button class="btn btn-outline" id="btn-toggle-labels" title="Tampilkan atau sembunyikan semua label prodi di kanvas">
                🏷️ Toggle Semua Label
            </button>
            <button class="btn btn-outline" id="btn-reset-filters" title="Kembalikan semua filter ke kondisi awal">
                🔄 Reset Tampilan
            </button>
        </div>
    </header>

    <!-- KPI SUMMARY CARDS (Clickable Filters) -->
    <section class="kpi-ribbon" id="kpi-ribbon-container">
        <!-- Rendered dynamically via JavaScript -->
    </section>

    <!-- SEARCH & FACULTY FILTERS -->
    <section class="controls-strip">
        <div class="search-box" id="search-box-wrapper">
            <span class="search-icon">🔍</span>
            <input type="text" id="prodi-search" placeholder="Cari nama prodi, fakultas, akronim (cth: Farmasi, FT, TI, PWK)..." autocomplete="off">
            <button id="search-clear-btn" class="search-clear-btn" title="Bersihkan pencarian" type="button">✕</button>
            <div id="search-dropdown" class="search-dropdown"></div>
        </div>

        <div class="filter-pills-row" id="faculty-filters">
            <!-- Rendered dynamically via JavaScript -->
        </div>
    </section>

    <!-- MAIN WORKSPACE -->
    <main class="workspace">
        <!-- LEFT: SVG MATRIX CANVAS -->
        <div class="chart-container">
            <div class="chart-header">
                <div class="chart-title-group">
                    <h2 id="chart-sub-heading">Matriks 4 Kuadran Interaktif (60 Prodi S1 Kampus Utama)</h2>
                    <p id="chart-sub-guide">Arahkan kursor ke titik prodi untuk ringkasan instan • Klik titik untuk membuka analisis detail</p>
                </div>
                <div class="canvas-toolbar">
                    <span id="match-counter" style="font-size:12px; font-weight:600; color:var(--text-muted); margin-right:8px;">Menampilkan: 66/66 Prodi</span>
                </div>
            </div>

            <!-- D3 KLASTER EVALUASI CLASSIFICATION GUIDE STRIP (Visible only when currentLevel === 'd3') -->
            <div id="d3-tier-legend-strip" class="d3-tier-legend-strip">
                <div class="tier-guide-card tg-tier-1" data-tier="1" id="card-tier-1" title="Klik untuk memfilter Klaster 1">
                    <div class="tgc-header">
                        <div class="tgc-title-group">
                            <span>⭐</span>
                            <span>Klaster 1: Kompetitif</span>
                        </div>
                        <span class="tgc-badge">1 Prodi (9,1%)</span>
                    </div>
                    <div class="tgc-rule"><span class="kriteria-tag">Kriteria</span> Fill Rate (FR) ≥ 60%</div>
                    <div class="tgc-prodi"><strong>D3 Manajemen Informatika</strong></div>
                </div>

                <div class="tier-guide-card tg-tier-2" data-tier="2" id="card-tier-2" title="Klik untuk memfilter Klaster 2">
                    <div class="tgc-header">
                        <div class="tgc-title-group">
                            <span>🔄</span>
                            <span>Klaster 2: Perlu Pendampingan</span>
                        </div>
                        <span class="tgc-badge">5 Prodi (45,5%)</span>
                    </div>
                    <div class="tgc-rule"><span class="kriteria-tag">Kriteria</span> Fill Rate (FR) 45% – 55%</div>
                    <div class="tgc-prodi"><strong>5 Prodi:</strong> Akuntansi, Tek. Mesin, Keswan, Tek. Listrik, Sekretari</div>
                </div>

                <div class="tier-guide-card tg-tier-3" data-tier="3" id="card-tier-3" title="Klik untuk memfilter Klaster 3">
                    <div class="tgc-header">
                        <div class="tgc-title-group">
                            <span>📉</span>
                            <span>Klaster 3: Evaluasi Khusus</span>
                        </div>
                        <span class="tgc-badge">5 Prodi (45,5%)</span>
                    </div>
                    <div class="tgc-rule"><span class="kriteria-tag">Kriteria</span> Fill Rate (FR) &lt; 45% (Batas Kritis &lt; 50%)</div>
                    <div class="tgc-prodi"><strong>5 Prodi:</strong> Manaj. Perusahaan, Tek. Sipil, Keu. Perbankan, Peternakan, Agribisnis</div>
                </div>
            </div>

            <div class="svg-wrapper" id="svg-container">
                <!-- SVG injected dynamically -->
                <svg id="matrix-svg" class="main-svg" viewBox="0 0 1000 580" preserveAspectRatio="xMidYMid meet"></svg>

                <!-- TOOLTIP CARD -->
                <div id="interactive-tooltip">
                    <div class="tt-badge-row">
                        <span class="tt-faculty" id="tt-fakultas">FT</span>
                        <span class="tt-quadrant" id="tt-kuadran">Unggulan</span>
                    </div>
                    <div class="tt-prodi-name" id="tt-name">Nama Program Studi</div>
                    <div class="tt-grid">
                        <div>
                            <div class="tt-metric-label">Rasio Keketatan:</div>
                            <div class="tt-metric-value" id="tt-keketatan">5.3 : 1</div>
                        </div>
                        <div>
                            <div class="tt-metric-label">Fill Rate Kuota:</div>
                            <div class="tt-metric-value" id="tt-fillrate">95.4%</div>
                        </div>
                        <div>
                            <div class="tt-metric-label">Peminat Rata-rata:</div>
                            <div class="tt-metric-value" id="tt-peminat">850 org</div>
                        </div>
                        <div>
                            <div class="tt-metric-label">Daya Tampung:</div>
                            <div class="tt-metric-value" id="tt-dt">120 kursi</div>
                        </div>
                    </div>
                    <div class="tt-hint">👆 Klik titik untuk membedah data lengkap 5 tahun</div>
                </div>
            </div>
            <!-- CANVAS FOOTNOTE METODOLOGI (Muncul hanya saat mode 60 prodi aktif) -->
            <div id="canvas-footnote-note" class="canvas-footnote" style="display:none;">
                <span>📌</span>
                <span><strong>Catatan Metodologi:</strong> Mengecualikan 6 Program Studi Baru dengan data terbatas &lt; 5 tahun (Bisnis Digital, Hubungan Internasional, Teknik Lingkungan, Teknik Perminyakan, TSDA, TIHP).</span>
            </div>
        </div>

        <!-- RIGHT: EXECUTIVE INSPECTOR DRAWER -->
        <aside class="inspector-panel" id="inspector-panel">
            <div class="inspector-placeholder" id="ins-placeholder">
                <div id="ins-placeholder-s1">
                    <img src="{usk_logo_b64}" alt="Logo USK" class="ins-placeholder-logo" />
                    <h3>Pilih Program Studi</h3>
                    <p>Klik salah satu lingkaran titik pada kanvas atau gunakan kotak pencarian untuk melihat rincian evaluasi 5 tahun, profil kebocoran kuota, dan rekomendasi kebijakan prodi.</p>
                </div>
                <div id="ins-placeholder-d3" style="display:none; text-align:left;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; border-bottom:1px solid var(--border-subtle); padding-bottom:12px;">
                        <img src="{usk_logo_b64}" alt="Logo USK" style="width:38px; height:38px; object-fit:contain;" />
                        <div>
                            <h4 style="font-size:13.5px; font-weight:800; color:var(--text-main); margin:0; letter-spacing:-0.2px;">STANDAR KLASTER VOKASI USK</h4>
                            <span style="font-size:11px; font-weight:600; color:var(--text-muted);">11 Program Studi D3 • Evaluasi Komparatif 2022–2026</span>
                        </div>
                    </div>
                    <p style="font-size:12px; color:var(--text-muted); line-height:1.55; margin-bottom:14px;">
                        Seluruh 11 Program Studi D3 USK berada pada <strong>Kuadran III</strong> (Peminat Membludak, Keterisian &lt; 80%). Untuk analisis terarah, prodi diklasifikasikan ke dalam <strong>3 Klaster Evaluasi Keterisian Kuota (Fill Rate)</strong>:
                    </p>
                    <div class="d3-sidebar-card">
                        <!-- KLASTER 1 -->
                        <div class="d3-sidebar-tier-block d3-stb-tier-1" onclick="toggleTierFilter(1)" title="Klik untuk memfilter Klaster 1">
                            <div class="d3-stb-header">
                                <div class="d3-stb-title">⭐ Klaster 1: Kompetitif</div>
                                <div class="d3-stb-badges">
                                    <span class="d3-stb-badge-fr">FR ≥ 60%</span>
                                    <span class="d3-stb-badge-count">1 Prodi (9,1%)</span>
                                </div>
                            </div>
                            <div class="d3-prodi-chips">
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('MANAJEMEN INFORMATIKA')" title="Klik untuk membedah data prodi">D3 Manajemen Informatika</span>
                            </div>
                        </div>

                        <!-- KLASTER 2 -->
                        <div class="d3-sidebar-tier-block d3-stb-tier-2" onclick="toggleTierFilter(2)" title="Klik untuk memfilter Klaster 2">
                            <div class="d3-stb-header">
                                <div class="d3-stb-title">🔄 Klaster 2: Perlu Pendampingan</div>
                                <div class="d3-stb-badges">
                                    <span class="d3-stb-badge-fr">FR 45%–55%</span>
                                    <span class="d3-stb-badge-count">5 Prodi (45,5%)</span>
                                </div>
                            </div>
                            <div class="d3-prodi-chips">
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('AKUNTANSI')" title="Klik untuk membedah data prodi">D3 Akuntansi</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('TEKNIK MESIN')" title="Klik untuk membedah data prodi">D3 Teknik Mesin</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('KESEHATAN HEWAN')" title="Klik untuk membedah data prodi">D3 Kesehatan Hewan</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('TEKNIK LISTRIK')" title="Klik untuk membedah data prodi">D3 Teknik Listrik</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('SEKRETARI')" title="Klik untuk membedah data prodi">D3 Sekretari</span>
                            </div>
                        </div>

                        <!-- KLASTER 3 -->
                        <div class="d3-sidebar-tier-block d3-stb-tier-3" onclick="toggleTierFilter(3)" title="Klik untuk memfilter Klaster 3">
                            <div class="d3-stb-header">
                                <div class="d3-stb-title">📉 Klaster 3: Evaluasi Khusus</div>
                                <div class="d3-stb-badges">
                                    <span class="d3-stb-badge-fr">FR &lt; 45%</span>
                                    <span class="d3-stb-badge-count">5 Prodi (45,5%)</span>
                                </div>
                            </div>
                            <div class="d3-prodi-chips">
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('MANAJEMEN PERUSAHAAN')" title="Klik untuk membedah data prodi">D3 Manajemen Perusahaan</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('TEKNIK SIPIL')" title="Klik untuk membedah data prodi">D3 Teknik Sipil</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('KEUANGAN')" title="Klik untuk membedah data prodi">D3 Keuangan &amp; Perbankan</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('PETERNAKAN')" title="Klik untuk membedah data prodi">D3 Budidaya Peternakan</span>
                                <span class="d3-prodi-chip" onclick="event.stopPropagation(); selectD3ProdiByName('AGRIBISNIS')" title="Klik untuk membedah data prodi">D3 Manajemen Agribisnis</span>
                            </div>
                        </div>
                    </div>
                    <div style="margin-top:14px; font-size:11.5px; color:#475569; text-align:center; background:#F8FAFC; padding:10px 12px; border-radius:8px; border:1px dashed #CBD5E1; line-height:1.45;">
                        💡 Klik salah satu kartu klaster di atas atau titik prodi pada kanvas untuk memfilter dan membedah detail evaluasi prodi.
                    </div>
                </div>
            </div>

            <div class="inspector-content" id="ins-content">
                <div class="ins-header">
                    <!-- Baris 1: Fakultas & Tombol Tutup -->
                    <div class="ins-top-bar">
                        <span class="ins-fakultas-tag" id="ins-fak">FAKULTAS</span>
                        <button class="ins-close-btn" onclick="closeInspector()" title="Tutup detail dan kembali">✕ Tutup</button>
                    </div>

                    <!-- Baris 2: Nama Program Studi -->
                    <div class="ins-title" id="ins-name">Nama Program Studi</div>

                    <!-- Baris 3: Badges Status (Kuadran & Tier Vokasi) -->
                    <div class="ins-badges-row">
                        <span class="ins-kuadran-tag" id="ins-quad-tag">KUADRAN I</span>
                        <span class="ins-tier-tag" id="ins-tier-tag" style="display:none;">TIER 1</span>
                    </div>

                    <!-- Baris 4: Deskripsi Ringkas 1 Kalimat -->
                    <div class="ins-sub" id="ins-quad-desc">Deskripsi status kuadran strategis</div>
                </div>

                <!-- 4 KPI Metrics -->
                <div class="ins-kpi-grid">
                    <div class="ins-kpi-card">
                        <div class="ins-kpi-title">Rasio Keketatan (5-Thn)</div>
                        <div class="ins-kpi-val" id="ins-keketatan">0.0 : 1</div>
                        <div class="ins-kpi-sub" id="ins-keketatan-status">Kompetitif</div>
                    </div>
                    <div class="ins-kpi-card">
                        <div class="ins-kpi-title">Rata Fill Rate (5-Thn)</div>
                        <div class="ins-kpi-val" id="ins-fillrate">0.0%</div>
                        <div class="ins-kpi-sub" id="ins-fillrate-status">Kuota Terserap</div>
                    </div>
                    <div class="ins-kpi-card">
                        <div class="ins-kpi-title">Peminat Tahunan</div>
                        <div class="ins-kpi-val" id="ins-peminat">0</div>
                        <div class="ins-kpi-sub">Rata-rata 5 tahun</div>
                    </div>
                    <div class="ins-kpi-card">
                        <div class="ins-kpi-title">Daya Tampung (DT)</div>
                        <div class="ins-kpi-val" id="ins-dt">0</div>
                        <div class="ins-kpi-sub" id="ins-sisa-kursi">Sisa Kuota Kosong</div>
                    </div>
                </div>

                <!-- Executive Recommendation (Prominent Top Position) -->
                <div class="rekomendasi-box" id="ins-rekomendasi-box" style="margin-bottom: 18px;">
                    <h4>💡 REKOMENDASI KEBIJAKAN EKSEKUTIF</h4>
                    <p id="ins-rekomendasi-text">Rekomendasi alokasi kuota...</p>
                </div>

                <!-- 5-Year History Table -->
                <div class="ins-section-title">
                    <span>Evaluasi Historis 5 Tahun (2022–2026)</span>
                    <span id="ins-tren-tag" style="font-size:11px; padding:2px 8px; border-radius:12px; background:#F1F5F9; color:#475569;">TREN RESMI</span>
                </div>
                <table class="history-table">
                    <thead>
                        <tr>
                            <th>Tahun</th>
                            <th>Peminat</th>
                            <th>Kuota</th>
                            <th>Registrasi</th>
                            <th>Fill Rate</th>
                        </tr>
                    </thead>
                    <tbody id="ins-history-tbody">
                        <!-- Injected via JS -->
                    </tbody>
                </table>
            </div>
        </aside>
    </main>

    <!-- FOOTER -->
    <footer class="bottom-bar">
        <div>
            <strong>Universitas Syiah Kuala</strong> • Kampus Jantong Hate Rakyat Aceh • Akreditasi Unggul
        </div>
        <div id="footer-standards">
            Standar Evaluasi S1: <strong>Keketatan 4,0 : 1</strong> | <strong>Keterisian Sehat 80%</strong>
        </div>
    </footer>

    <!-- SCRIPT DATA & INTERACTION LOGIC -->
    <script>
        const DATA_BY_LEVEL = {json_data};

        // State Management
        let currentLevel = (window.location.hash.includes('d3') || window.location.search.includes('d3')) ? "d3" : "s1";
        let currentS1Subset = (window.location.hash.includes('60') || window.location.hash.includes('tanpa') || window.location.hash.includes('established') || window.location.search.includes('60')) ? "established" : "all";
        let currentFaculty = "ALL";
        let currentFilterCard = "ALL"; // Quadrant in S1 & D3 (I, II, III, IV)
        let currentD3Tier = "ALL"; // Sub-tier filter for D3 (1, 2, 3)
        let searchQuery = "";
        let showAllLabels = false;
        let selectedProdiId = null;

        // Sinkronisasi Dinamis URL Hash
        function syncUrlHash() {{
            let hash = currentLevel;
            if (currentLevel === 's1') {{
                hash = (currentS1Subset === 'established') ? 's1-60' : 's1';
            }}
            if (window.history && window.history.replaceState) {{
                window.history.replaceState(null, null, '#' + hash);
            }} else {{
                window.location.hash = hash;
            }}
        }}

        // Helper Dataset List Dinamis
        function getActiveList() {{
            if (currentLevel === 'd3') return DATA_BY_LEVEL.d3;
            if (currentS1Subset === 'established') {{
                return DATA_BY_LEVEL.s1.filter(p => !p.is_prodi_baru);
            }}
            return DATA_BY_LEVEL.s1;
        }}

        // Coordinate Transformation Settings
        const SVG_W = 1000;
        const SVG_H = 580;
        const PLOT_X = 65;
        const PLOT_Y = 35;
        const PLOT_W = SVG_W - PLOT_X - 35; // 900
        const PLOT_H = SVG_H - PLOT_Y - 55; // 490

        // Helper Capping Fill Rate
        function clampFR(val) {{
            const num = parseFloat(val);
            if (isNaN(num)) return 0.0;
            return Math.min(Math.max(num, 0.0), 100.0);
        }}

        // Scale functions
        function mapX(x) {{
            if (currentLevel === 's1') {{
                // Piecewise X scale for S1 (0 - 52)
                let normX = 0;
                if (x <= 4.0) {{
                    normX = (x / 4.0) * 0.36;
                }} else if (x <= 22.0) {{
                    normX = 0.36 + ((x - 4.0) / 18.0) * 0.42;
                }} else {{
                    normX = 0.78 + ((x - 22.0) / (52.0 - 22.0)) * 0.22;
                }}
                return PLOT_X + normX * PLOT_W;
            }} else {{
                // Linear X scale for D3 (0 - 21)
                const clampedX = Math.min(Math.max(x, 0.0), 21.0);
                const normX = clampedX / 21.0;
                return PLOT_X + normX * PLOT_W;
            }}
        }}

        function mapY(y) {{
            if (currentLevel === 's1') {{
                const yMin = 24.0;
                const yMax = 106.0;
                const normY = (y - yMin) / (yMax - yMin);
                return PLOT_Y + (1.0 - normY) * PLOT_H;
            }} else {{
                // Linear Y scale for D3 (18 - 105)
                const yMin = 18.0;
                const yMax = 105.0;
                const normY = (y - yMin) / (yMax - yMin);
                return PLOT_Y + (1.0 - normY) * PLOT_H;
            }}
        }}

        function createSVGElement(tag, attrs) {{
            const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
            for (let k in attrs) {{
                el.setAttribute(k, attrs[k]);
            }}
            return el;
        }}

        // Render KPI Ribbon dynamically
        function renderKPIRibbon() {{
            const container = document.getElementById('kpi-ribbon-container');
            container.innerHTML = '';

            if (currentLevel === 's1') {{
                const activeList = getActiveList();
                const totalCount = activeList.length;
                const qCounts = {{ 'I': 0, 'II': 0, 'III': 0, 'IV': 0 }};
                activeList.forEach(p => {{
                    if (qCounts[p.kuadran] !== undefined) qCounts[p.kuadran]++;
                }});

                const cardsConfig = [
                    {{
                        id: 'I',
                        label: 'Kuadran I: Unggulan',
                        icon: '🏆',
                        val: qCounts['I'].toString(),
                        sub: `Prodi (${{((qCounts['I'] / totalCount) * 100).toFixed(1).replace('.', ',')}}%)`,
                        note: 'Peminat Tinggi & Kuota Terpenuhi',
                        class: 'c-emerald'
                    }},
                    {{
                        id: 'II',
                        label: 'Kuadran II: Stabil',
                        icon: '⚖️',
                        val: qCounts['II'].toString(),
                        sub: `Prodi (${{((qCounts['II'] / totalCount) * 100).toFixed(1).replace('.', ',')}}%)`,
                        note: 'Seleksi Moderat, Daya Serap Aman',
                        class: 'c-blue'
                    }},
                    {{
                        id: 'III',
                        label: 'Kuadran III: Belum Optimal',
                        icon: '⚠️',
                        val: qCounts['III'].toString(),
                        sub: `Prodi (${{((qCounts['III'] / totalCount) * 100).toFixed(1).replace('.', ',')}}%)`,
                        note: 'Peminat Tinggi tapi Daftar Ulang Belum Optimal',
                        class: 'c-amber'
                    }},
                    {{
                        id: 'IV',
                        label: 'Kuadran IV: Perlu Ditingkatkan',
                        icon: '🚨',
                        val: qCounts['IV'].toString(),
                        sub: `Prodi (${{((qCounts['IV'] / totalCount) * 100).toFixed(1).replace('.', ',')}}%)`,
                        note: 'Peminat Sepi & Kuota Kerap Kosong',
                        class: 'c-rose'
                    }}
                ];

                cardsConfig.forEach(cfg => {{
                    const card = document.createElement('div');
                    card.className = `kpi-card ${{cfg.class}} ${{currentFilterCard === cfg.id ? 'active' : ''}}`;
                    card.setAttribute('data-filter', cfg.id);
                    card.title = `Klik untuk memfilter ${{cfg.label}}`;
                    card.innerHTML = `
                        <div class="kpi-header">
                            <span class="kpi-label">${{cfg.label}}</span>
                            <span style="font-size:14px;">${{cfg.icon}}</span>
                        </div>
                        <div class="kpi-val-row">
                            <span class="kpi-val">${{cfg.val}}</span>
                            <span class="kpi-sub">${{cfg.sub}}</span>
                        </div>
                        <div class="kpi-note">${{cfg.note}}</div>
                    `;
                    card.addEventListener('click', () => {{
                        if (currentFilterCard === cfg.id) {{
                            currentFilterCard = "ALL";
                        }} else {{
                            currentFilterCard = cfg.id;
                        }}
                        renderKPIRibbon();
                        renderChart();
                    }});
                    container.appendChild(card);
                }});
            }} else {{
                // D3 Cards: Format, Desain, dan Nama Kuadran 100% Identik dengan S1
                const cardsConfig = [
                    {{
                        id: 'I',
                        label: 'Kuadran I: Unggulan',
                        icon: '🏆',
                        val: '0',
                        sub: 'Prodi (0%)',
                        note: 'Peminat Tinggi & Kuota Terpenuhi',
                        class: 'c-emerald'
                    }},
                    {{
                        id: 'II',
                        label: 'Kuadran II: Stabil',
                        icon: '⚖️',
                        val: '0',
                        sub: 'Prodi (0%)',
                        note: 'Seleksi Moderat, Daya Serap Aman',
                        class: 'c-blue'
                    }},
                    {{
                        id: 'III',
                        label: 'Kuadran III: Belum Optimal',
                        icon: '⚠️',
                        val: '11',
                        sub: 'Prodi (100% Vokasi)',
                        note: 'Peminat Tinggi tapi Daftar Ulang Belum Optimal',
                        class: 'c-amber'
                    }},
                    {{
                        id: 'IV',
                        label: 'Kuadran IV: Perlu Ditingkatkan',
                        icon: '🚨',
                        val: '0',
                        sub: 'Prodi (0%)',
                        note: 'Peminat Sepi & Kuota Kerap Kosong',
                        class: 'c-rose'
                    }}
                ];

                cardsConfig.forEach(cfg => {{
                    const card = document.createElement('div');
                    card.className = `kpi-card ${{cfg.class}} ${{currentFilterCard === cfg.id ? 'active' : ''}}`;
                    card.setAttribute('data-filter', cfg.id);
                    card.title = `Klik untuk memfilter ${{cfg.label}}`;
                    card.innerHTML = `
                        <div class="kpi-header">
                            <span class="kpi-label">${{cfg.label}}</span>
                            <span style="font-size:14px;">${{cfg.icon}}</span>
                        </div>
                        <div class="kpi-val-row">
                            <span class="kpi-val">${{cfg.val}}</span>
                            <span class="kpi-sub">${{cfg.sub}}</span>
                        </div>
                        <div class="kpi-note">${{cfg.note}}</div>
                    `;
                    card.addEventListener('click', () => {{
                        if (currentFilterCard === cfg.id) {{
                            currentFilterCard = "ALL";
                        }} else {{
                            currentFilterCard = cfg.id;
                        }}
                        renderKPIRibbon();
                        renderChart();
                    }});
                    container.appendChild(card);
                }});
            }}
        }}

        // Render Faculty Filters dynamically
        function renderFacultyFilters() {{
            const container = document.getElementById('faculty-filters');
            container.innerHTML = '';

            const currentList = getActiveList();
            const fakCounts = {{}};
            currentList.forEach(p => {{
                fakCounts[p.fakultas] = (fakCounts[p.fakultas] || 0) + 1;
            }});

            // All Pill
            const allPill = document.createElement('span');
            allPill.className = `filter-pill ${{currentFaculty === 'ALL' ? 'active' : ''}}`;
            allPill.textContent = `Semua Fakultas (${{currentList.length}})`;
            allPill.setAttribute('data-fak', 'ALL');
            allPill.addEventListener('click', () => {{
                currentFaculty = 'ALL';
                renderFacultyFilters();
                renderChart();
            }});
            container.appendChild(allPill);

            // Per Faculty Pills sorted by count descending
            Object.keys(fakCounts).sort((a,b) => fakCounts[b] - fakCounts[a]).forEach(fak => {{
                const abbr = fak_abbr_map_client[fak] || fak;
                const pill = document.createElement('span');
                pill.className = `filter-pill ${{currentFaculty === fak ? 'active' : ''}}`;
                pill.textContent = `${{abbr}} (${{fakCounts[fak]}})`;
                pill.setAttribute('data-fak', fak);
                pill.addEventListener('click', () => {{
                    currentFaculty = fak;
                    renderFacultyFilters();
                    renderChart();
                }});
                container.appendChild(pill);
            }});

            // If D3, append sub-tier filter pills
            if (currentLevel === 'd3') {{
                const sep = document.createElement('span');
                sep.style.cssText = 'color:#94A3B8; font-weight:700; margin:0 6px; display:inline-flex; align-items:center; user-select:none;';
                sep.textContent = '│';
                container.appendChild(sep);

                const tierConfigs = [
                    {{ id: 'ALL', label: 'Semua Klaster (11)' }},
                    {{ id: 1, label: '⭐ Klaster 1: Kompetitif (FR ≥ 60% • 1)' }},
                    {{ id: 2, label: '🔄 Klaster 2: Pendampingan (FR 45%–55% • 5)' }},
                    {{ id: 3, label: '📉 Klaster 3: Evaluasi Khusus (FR < 45% • 5)' }}
                ];
                tierConfigs.forEach(t => {{
                    const pill = document.createElement('span');
                    pill.className = `filter-pill ${{currentD3Tier === t.id ? 'active' : ''}}`;
                    pill.textContent = t.label;
                    pill.title = `Filter ${{t.label}}`;
                    pill.addEventListener('click', () => {{
                        currentD3Tier = (currentD3Tier === t.id && t.id !== 'ALL') ? 'ALL' : t.id;
                        updateTierGuideCardStates();
                        renderFacultyFilters();
                        renderChart();
                    }});
                    container.appendChild(pill);
                }});
            }}
        }}

        const fak_abbr_map_client = {json.dumps(fak_abbr_map)};

        // Kamus Akronim & Singkatan Program Studi Populer USK
        const ACRONYM_MAP = {{
            'ti': ['informatika', 'teknologi informasi'],
            'it': ['informatika', 'teknologi informasi'],
            'pwk': ['perencanaan wilayah'],
            'paud': ['pendidikan anak usia dini', 'paud'],
            'pgsd': ['pendidikan guru sekolah dasar'],
            'hi': ['hubungan internasional'],
            'ilkom': ['ilmu komunikasi'],
            'mi': ['manajemen informatika'],
            'pko': ['kepelatihan olahraga'],
            'pjkr': ['jasmani, kesehatan'],
            'penjas': ['jasmani, kesehatan'],
            'fk': ['pendidikan dokter'],
            'fkg': ['dokter gigi'],
            'fkh': ['kedokteran hewan']
        }};

        // Pencarian Cerdas Multi-Kategori (Nama, Akronim, Fakultas, Kuadran, Tier)
        function matchSearchQuery(d, query) {{
            if (!query || query.trim() === '') return true;
            const q = query.trim().toLowerCase();

            // 1. Pencarian nama prodi (parsial & lengkap)
            const prodiName = (d.jenjang === 'D3' ? ('d3 ' + d.nama) : d.nama).toLowerCase();
            if (prodiName.includes(q)) return true;

            // 2. Pencarian nama fakultas atau singkatan resmi
            if (d.fakultas && d.fakultas.toLowerCase().includes(q)) return true;
            if (d.fakultas_abbr && d.fakultas_abbr.toLowerCase().includes(q)) return true;

            // 3. Pencarian berbasis akronim populer
            if (ACRONYM_MAP[q]) {{
                const targetKeywords = ACRONYM_MAP[q];
                for (let i = 0; i < targetKeywords.length; i++) {{
                    if (prodiName.includes(targetKeywords[i])) return true;
                }}
            }}

            // 4. Pencarian berbasis Kuadran
            if (q === 'q1' || q === 'kuadran 1' || q === 'kuadran i' || q === 'unggulan') {{
                if (d.kuadran === 'I') return true;
            }}
            if (q === 'q2' || q === 'kuadran 2' || q === 'kuadran ii' || q === 'stabil') {{
                if (d.kuadran === 'II') return true;
            }}
            if (q === 'q3' || q === 'kuadran 3' || q === 'kuadran iii' || q === 'belum optimal' || q === 'optimal') {{
                if (d.kuadran === 'III') return true;
            }}
            if (q === 'q4' || q === 'kuadran 4' || q === 'kuadran iv' || q === 'perlu ditingkatkan' || q === 'ditingkatkan') {{
                if (d.kuadran === 'IV') return true;
            }}

            // 5. Pencarian berbasis Klaster Vokasi (Khusus D3)
            if (currentLevel === 'd3') {{
                if ((q === 'tier 1' || q === 'klaster 1' || q === 'kompetitif') && d.tier === 1) return true;
                if ((q === 'tier 2' || q === 'klaster 2' || q === 'pendampingan' || q === 'perlu pendampingan') && d.tier === 2) return true;
                if ((q === 'tier 3' || q === 'klaster 3' || q === 'evaluasi' || q === 'evaluasi khusus') && d.tier === 3) return true;
            }}

            return false;
        }}

        // Filter Evaluation
        function isProdiVisible(d) {{
            // S1 Subset Filter (Eksklusi penuh 6 prodi baru bila mode 'established')
            if (currentLevel === 's1' && currentS1Subset === 'established' && d.is_prodi_baru) return false;

            // Faculty filter
            if (currentFaculty !== "ALL" && d.fakultas !== currentFaculty) return false;

            // Card Filter (Kuadran I, II, III, IV) - 100% seragam S1 & D3!
            if (currentFilterCard !== "ALL" && d.kuadran !== currentFilterCard) return false;

            // D3 Tier Filter
            if (currentLevel === 'd3' && currentD3Tier !== 'ALL' && d.tier !== currentD3Tier) return false;

            // Smart Search query
            if (searchQuery.trim() !== "") {{
                if (!matchSearchQuery(d, searchQuery)) return false;
            }}
            return true;
        }}

        // ====================================================
        // PRODI SHORT NAME DICTIONARY & TITLE CASE FORMATTING
        // ====================================================
        const PRODI_SHORT_NAMES = {{
            'PENDIDIKAN PANCASILA DAN KEWARGANEGARAAN': 'PPKn',
            'PENDIDIKAN KESEJAHTERAAN KELUARGA': 'PKK',
            'PENDIDIKAN SENI DRAMA TARI DAN MUSIK': 'Sendratasik',
            'PENDIDIKAN JASMANI KESEHATAN DAN REKREASI': 'Penjaskesrek',
            'PERENCANAAN WILAYAH DAN KOTA': 'PWK',
            'TEKNOLOGI INDUSTRI HASIL PERIKANAN': 'Tek. Ind. Perikanan',
            'PEMANFAATAN SUMBERDAYA PERIKANAN': 'Pemanfaatan Perikanan',
            'PENDIDIKAN GURU SEKOLAH DASAR': 'PGSD',
            'PENDIDIKAN GURU PAUD': 'PG PAUD',
            'PENDIDIKAN GURU PENDIDIKAN ANAK USIA DINI': 'PG PAUD',
            'TEKNIK SUMBER DAYA AIR': 'Tek. SDA',
            'TEKNOLOGI HASIL PERTANIAN': 'Tek. Hasil Pertanian',
            'PENDIDIKAN DOKTER HEWAN': 'Dokter Hewan',
            'PENDIDIKAN BAHASA INGGRIS': 'Pend. B. Inggris',
            'PENDIDIKAN BAHASA INDONESIA': 'Pend. B. Indonesia',
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
            'PENDIDIKAN SEJARAH': 'Pend. Sejarah',
            'ILMU ADMINISTRASI PUBLIK': 'Adm. Publik',
            'ILMU ADMINISTRASI NEGARA': 'Adm. Negara',
            'ILMU KOMUNIKASI': 'Ilmu Komunikasi',
            'ILMU PEMERINTAHAN': 'Ilmu Pemerintahan',
            'HUBUNGAN INTERNASIONAL': 'Hub. Internasional',
            'ILMU POLITIK': 'Ilmu Politik',
            'SOSIOLOGI': 'Sosiologi',
            'ILMU HUKUM': 'Ilmu Hukum',
            'TEKNIK INFORMATIKA': 'Informatika',
            'INFORMATIKA': 'Informatika',
            'SISTEM INFORMASI': 'Sistem Informasi',
            'TEKNIK KOMPUTER': 'Tek. Komputer',
            'TEKNIK SIPIL': 'Tek. Sipil',
            'TEKNIK MESIN': 'Tek. Mesin',
            'TEKNIK ELEKTRO': 'Tek. Elektro',
            'TEKNIK KIMIA': 'Tek. Kimia',
            'TEKNIK ARSITEKTUR': 'Arsitektur',
            'ARSITEKTUR': 'Arsitektur',
            'TEKNIK GEOFISIKA': 'Tek. Geofisika',
            'TEKNIK GEOLOGI': 'Tek. Geologi',
            'TEKNIK PERTAMBANGAN': 'Tek. Pertambangan',
            'TEKNIK INDUSTRI': 'Tek. Industri',
            'TEKNIK LINGKUNGAN': 'Tek. Lingkungan',
            'TEKNIK PERTANIAN': 'Tek. Pertanian',
            'AGRIBISNIS': 'Agribisnis',
            'AGROTEKNOLOGI': 'Agroteknologi',
            'PETERNAKAN': 'Peternakan',
            'ILMU TANAH': 'Ilmu Tanah',
            'PROTEKSI TANAMAN': 'Proteksi Tanaman',
            'BUDIDAYA PERAIRAN': 'Budidaya Perairan',
            'ILMU KELAUTAN': 'Ilmu Kelautan',
            'KEDOKTERAN HEWAN': 'Dokter Hewan',
            'FARMASI': 'Farmasi',
            'KEPERAWATAN': 'Keperawatan',
            'ILMU KEPERAWATAN': 'Keperawatan',
            'KEDOKTERAN': 'Kedokteran',
            'KEDOKTERAN GIGI': 'Kedokteran Gigi',
            'STATISTIKA': 'Statistika',
            'MATEMATIKA': 'Matematika',
            'FISIKA': 'Fisika',
            'KIMIA': 'Kimia',
            'BIOLOGI': 'Biologi',
            'MANAJEMEN': 'Manajemen',
            'AKUNTANSI': 'Akuntansi',
            'EKONOMI ISLAM': 'Ekonomi Islam',
            'BISNIS DIGITAL': 'Bisnis Digital',
            'AKUNTANSI PERPAJAKAN': 'Akun. Perpajakan',
            'TEKNIK PERMINYAKAN': 'Tek. Perminyakan',
            'PSIKOLOGI': 'Psikologi',
            'KEHUTANAN': 'Kehutanan',
            // D3 Vokasi
            'KESEHATAN HEWAN': 'Kesehatan Hewan',
            'MANAJEMEN AGRIBISNIS': 'Manaj. Agribisnis',
            'TEKNIK LISTRIK': 'Tek. Listrik',
            'BUDIDAYA PETERNAKAN': 'Budidaya Peternakan',
            'MANAJEMEN PERUSAHAAN': 'Manaj. Perusahaan',
            'KEUANGAN DAN PERBANKAN': 'Keuangan & Perbankan',
            'MANAJEMEN INFORMATIKA': 'Manaj. Informatika',
            'SEKRETARI': 'Sekretari'
        }};

        function formatShortProdiLabel(d) {{
            const rawName = (d.nama || '').trim().toUpperCase();
            let baseName = PRODI_SHORT_NAMES[rawName];
            if (!baseName) {{
                baseName = rawName
                    .replace('PENDIDIKAN GURU ', 'PG ')
                    .replace('PENDIDIKAN ', 'Pend. ')
                    .replace('TEKNOLOGI ', 'Tek. ')
                    .replace('TEKNIK ', 'Tek. ')
                    .replace('ADMINISTRASI ', 'Adm. ')
                    .toLowerCase()
                    .split(' ')
                    .map(w => w.charAt(0).toUpperCase() + w.slice(1))
                    .join(' ');
            }}
            const prefix = d.jenjang === 'D3' ? 'D3 ' : '';
            const fAbbr = d.fakultas_abbr ? ` (${{d.fakultas_abbr}})` : '';
            return `${{prefix}}${{baseName}}${{fAbbr}}`;
        }}

        // ====================================================
        // ANTI-COLLISION REPULSION LAYOUT ENGINE
        // ====================================================
        function solveLabelLayout(items, bounds) {{
            if (!items || items.length === 0) return [];
            if (items.length === 1) {{
                const it = items[0];
                it.lx = it.x0 + it.w / 2 + 8;
                it.ly = it.y0;
                it.needsLeaderLine = false;
                it.edgeX = it.lx;
                it.edgeY = it.ly;
                return items;
            }}

            // Urutkan item berdasarkan koordinat vertikal (cy) lalu horizontal (cx)
            items.sort((a, b) => (a.y0 !== b.y0 ? a.y0 - b.y0 : a.x0 - b.x0));

            // Inisialisasi posisi awal cerdas dengan Alternating Multi-Directional Staggering
            items.forEach((it, idx) => {{
                const d = it.d;
                const side = (idx % 2 === 0) ? 1 : -1;
                const nameUpper = d.nama.toUpperCase();

                if (nameUpper.includes('FARMASI')) {{
                    it.lx = it.x0 - it.w / 2 - 10;
                    it.ly = it.y0;
                }} else if (d.keketatan >= 4.0 && d.fill_rate >= 80.0) {{
                    // Kuadran I (Unggulan)
                    if (d.keketatan > 7.0) {{
                        it.lx = it.x0 + it.w / 2 + 8;
                        it.ly = it.y0 + (side * 6);
                    }} else if (d.fill_rate > 92.0) {{
                        it.lx = it.x0 + (side * 28);
                        it.ly = it.y0 - 16 - ((idx % 3) * 6);
                    }} else {{
                        it.lx = it.x0 + (side * (it.w / 2 + 10));
                        it.ly = it.y0 - 8 + (side * 6);
                    }}
                }} else if (d.keketatan < 4.0 && d.fill_rate >= 80.0) {{
                    // Kuadran II (Stabil)
                    it.lx = it.x0 - it.w / 2 - 8;
                    it.ly = it.y0 + (side * 6);
                }} else if (d.keketatan >= 4.0 && d.fill_rate < 80.0) {{
                    // Kuadran III (Belum Optimal)
                    it.lx = it.x0 + it.w / 2 + 8;
                    it.ly = it.y0 + (side * 6);
                }} else {{
                    // Kuadran IV (Perlu Ditingkatkan)
                    if (d.fill_rate < 58.0) {{
                        // Sebar ke bawah dan horizontal (area bawah lapang)
                        it.lx = it.x0 + ((idx % 5) - 2) * 22;
                        it.ly = it.y0 + 18 + ((idx % 3) * 8);
                    }} else if (d.keketatan < 1.4) {{
                        // Hanya titik di tepi kiri ekstrim yang ke kiri
                        it.lx = it.x0 - it.w / 2 - 8;
                        it.ly = it.y0 + (side * 8);
                    }} else {{
                        // Manfaatkan area lapang di kanan titik (menuju garis ambang 4.0)
                        it.lx = (side === 1) ? (it.x0 + it.w / 2 + 10) : (it.x0 - it.w / 2 - 8);
                        it.ly = it.y0 + 8 + (side * 6);
                    }}
                }}
            }});

            const N = items.length;
            const iterations = 150;

            for (let step = 0; step < iterations; step++) {{
                // 1. Box overlap repulsion (AABB)
                for (let i = 0; i < N; i++) {{
                    for (let j = i + 1; j < N; j++) {{
                        const a = items[i];
                        const b = items[j];
                        const dx = b.lx - a.lx;
                        const dy = b.ly - a.ly;
                        const minDistX = (a.w + b.w) / 2 + 4.0;
                        const minDistY = (a.h + b.h) / 2 + 2.5;
                        const overlapX = minDistX - Math.abs(dx);
                        const overlapY = minDistY - Math.abs(dy);

                        if (overlapX > 0 && overlapY > 0) {{
                            const sY = dy >= 0 ? 1 : -1;
                            const sX = dx >= 0 ? 1 : -1;
                            if (overlapY < 14.0 || (overlapY / minDistY) <= (overlapX / minDistX)) {{
                                const shiftY = (overlapY / 2.0) + 0.6;
                                a.ly -= sY * shiftY;
                                b.ly += sY * shiftY;
                            }} else {{
                                const shiftX = (overlapX / 2.0) + 0.6;
                                a.lx -= sX * shiftX;
                                b.lx += sX * shiftX;
                            }}
                        }}
                    }}
                }}

                // 2. Dots Repulsion (mencegah label menutupi titik data prodi)
                for (let i = 0; i < N; i++) {{
                    const a = items[i];
                    for (let j = 0; j < N; j++) {{
                        const pt = items[j];
                        const nearX = Math.max(a.lx - a.w / 2, Math.min(a.lx + a.w / 2, pt.x0));
                        const nearY = Math.max(a.ly - a.h / 2, Math.min(a.ly + a.h / 2, pt.y0));
                        const dPoint = Math.hypot(nearX - pt.x0, nearY - pt.y0);
                        if (dPoint < 8.5) {{
                            const push = (8.5 - dPoint) * 0.5;
                            let ang = Math.atan2(a.ly - pt.y0, a.lx - pt.x0);
                            if (Math.abs(dPoint) < 0.001) {{
                                ang = (a.id % 2 === 0) ? -Math.PI / 2 : Math.PI / 2;
                            }}
                            a.lx += Math.cos(ang) * push;
                            a.ly += Math.sin(ang) * push;
                        }}
                    }}
                }}

                // 3. Batas kanvas (Clamping)
                for (let i = 0; i < N; i++) {{
                    const a = items[i];
                    const hw = a.w / 2;
                    const hh = a.h / 2;
                    a.lx = Math.max(bounds.minX + hw, Math.min(bounds.maxX - hw, a.lx));
                    a.ly = Math.max(bounds.minY + hh, Math.min(bounds.maxY - hh, a.ly));
                }}
            }}

            // Helper minBound
            function minBound(vMax, val) {{
                return Math.min(vMax, val);
            }}

            // Tentukan leader line flag dan titik potong tepi box
            items.forEach(it => {{
                const dist = Math.hypot(it.lx - it.x0, it.ly - it.y0);
                if (dist > 14.0) {{
                    it.needsLeaderLine = true;
                    it.edgeX = Math.max(it.lx - it.w / 2, Math.min(it.lx + it.w / 2, it.x0));
                    it.edgeY = Math.max(it.ly - it.h / 2, Math.min(it.ly + it.h / 2, it.y0));
                }} else {{
                    it.needsLeaderLine = false;
                    it.edgeX = it.lx;
                    it.edgeY = it.ly;
                }}
            }});

            return items;
        }}

        // ====================================================
        // TOOLTIP & MUTUAL HIGHLIGHTING MANAGER
        // ====================================================
        const TooltipManager = {{
            get tooltip() {{ return document.getElementById('interactive-tooltip'); }},
            get svgContainer() {{ return document.getElementById('svg-container'); }},
            activeProdiId: null,

            show(e, d) {{
                this.activeProdiId = d.id;
                const tt = this.tooltip;
                if (!tt) return;

                document.getElementById('tt-fakultas').textContent = `${{d.fakultas_abbr}} • ${{d.fakultas}}`;
                document.getElementById('tt-name').textContent = (d.jenjang === 'D3' ? 'D3 ' : '') + d.nama;

                const qBadge = document.getElementById('tt-kuadran');
                qBadge.textContent = d.kuadran_title;
                qBadge.style.backgroundColor = d.color;
                qBadge.style.color = '#FFFFFF';

                document.getElementById('tt-keketatan').textContent = `${{d.keketatan}} : 1`;
                document.getElementById('tt-fillrate').textContent = `${{clampFR(d.fill_rate).toFixed(1)}}%`;
                document.getElementById('tt-peminat').textContent = `${{d.peminat_5thn.toLocaleString('id-ID')}} org`;
                document.getElementById('tt-dt').textContent = `${{d.dt_5thn}} kursi`;

                tt.style.display = 'block';
                this.updatePosition(e.clientX, e.clientY);
            }},

            updatePosition(clientX, clientY) {{
                const tt = this.tooltip;
                const container = this.svgContainer;
                if (!tt || tt.style.display === 'none' || !container) return;

                const rect = container.getBoundingClientRect();
                const mouseX = clientX - rect.left;
                const mouseY = clientY - rect.top;

                // Smart Vertical Flip: Jika kursor berada di dekat batas atas (< 185px dari tepi atas canvas), flip ke bawah kursor
                const flipDown = (mouseY < 185);
                tt.classList.toggle('flipped-down', flipDown);

                const targetTop = mouseY;

                // Horizontal Clamping agar tooltip tidak terpotong di tepi kiri/kanan SVG
                const ttHalfWidth = 135;
                let targetLeft = mouseX;
                if (targetLeft < ttHalfWidth + 12) {{
                    targetLeft = ttHalfWidth + 12;
                }} else if (targetLeft > rect.width - ttHalfWidth - 12) {{
                    targetLeft = rect.width - ttHalfWidth - 12;
                }}

                // Geser panah penunjuk (arrow) agar tetap menunjuk tepat ke titik kursor
                const arrowOffset = Math.max(16, Math.min(260 - 16, 130 + (mouseX - targetLeft)));
                tt.style.setProperty('--arrow-left', `${{arrowOffset}}px`);

                tt.style.left = `${{targetLeft}}px`;
                tt.style.top = `${{targetTop}}px`;
            }},

            hide() {{
                if (this.activeProdiId !== null) {{
                    this.clearHighlight(this.activeProdiId);
                    this.activeProdiId = null;
                }}
                const tt = this.tooltip;
                if (tt) {{
                    tt.style.display = 'none';
                    tt.classList.remove('flipped-down');
                }}
            }},

            highlight(d) {{
                const circle = document.querySelector(`.dot[data-id="${{d.id}}"]`);
                if (circle) {{
                    circle.setAttribute('r', '11.5');
                }}

                const lLine = document.querySelector(`.leader-line[data-id="${{d.id}}"]`);
                if (lLine) {{
                    lLine.setAttribute('stroke', d.color);
                    lLine.setAttribute('stroke-width', '1.6');
                    lLine.setAttribute('opacity', '1');
                }}

                const bBadge = document.querySelector(`.label-badge[data-id="${{d.id}}"]`);
                if (bBadge) {{
                    bBadge.classList.add('highlighted');
                    const bRect = bBadge.querySelector('.badge-rect');
                    if (bRect) {{
                        bRect.setAttribute('stroke', d.color);
                        bRect.setAttribute('stroke-width', '1.8');
                    }}
                }}
            }},

            clearHighlight(prodiId) {{
                const circle = document.querySelector(`.dot[data-id="${{prodiId}}"]`);
                if (circle) {{
                    circle.setAttribute('r', selectedProdiId === prodiId ? '10.5' : '7.5');
                }}

                const lLine = document.querySelector(`.leader-line[data-id="${{prodiId}}"]`);
                if (lLine) {{
                    lLine.setAttribute('stroke', '#94A3B8');
                    lLine.setAttribute('stroke-width', '0.85');
                    lLine.setAttribute('opacity', '0.85');
                }}

                const bBadge = document.querySelector(`.label-badge[data-id="${{prodiId}}"]`);
                if (bBadge) {{
                    bBadge.classList.remove('highlighted');
                    const bRect = bBadge.querySelector('.badge-rect');
                    if (bRect) {{
                        const isSel = (selectedProdiId === prodiId);
                        const currentList = getActiveList();
                        const p = currentList.find(x => x.id === prodiId);
                        const c = (isSel && p) ? p.color : '#CBD5E1';
                        bRect.setAttribute('stroke', c);
                        bRect.setAttribute('stroke-width', isSel ? '1.8' : '0.85');
                    }}
                }}
            }}
        }};

        function onDotHover(e, d) {{
            if (TooltipManager.activeProdiId && TooltipManager.activeProdiId !== d.id) {{
                TooltipManager.clearHighlight(TooltipManager.activeProdiId);
            }}
            TooltipManager.highlight(d);
            TooltipManager.show(e, d);
        }}

        function onDotLeave(d) {{
            TooltipManager.hide();
        }}

        function onBadgeHover(e, d) {{
            if (TooltipManager.activeProdiId && TooltipManager.activeProdiId !== d.id) {{
                TooltipManager.clearHighlight(TooltipManager.activeProdiId);
            }}
            TooltipManager.highlight(d);
            TooltipManager.show(e, d);
        }}

        function onBadgeLeave(d) {{
            TooltipManager.hide();
        }}

        // Render Canvas
        function renderChart() {{
            TooltipManager.hide();
            const svg = document.getElementById('matrix-svg');
            svg.innerHTML = '';

            const currentList = getActiveList();
            const xThreshold = mapX(4.0);
            const yThreshold80 = mapY(80.0);

            if (currentLevel === 's1') {{
                // 1. S1 Quadrant Shading
                // Q1: Top Right (x >= 4.0, y >= 80.0)
                svg.appendChild(createSVGElement('rect', {{
                    x: xThreshold, y: PLOT_Y,
                    width: (PLOT_X + PLOT_W) - xThreshold, height: yThreshold80 - PLOT_Y,
                    fill: '#F0FDF4', opacity: 0.65
                }}));
                // Q2: Top Left (x < 4.0, y >= 80.0)
                svg.appendChild(createSVGElement('rect', {{
                    x: PLOT_X, y: PLOT_Y,
                    width: xThreshold - PLOT_X, height: yThreshold80 - PLOT_Y,
                    fill: '#F0F9FF', opacity: 0.65
                }}));
                // Q4: Bottom Left (x < 4.0, y < 80.0)
                svg.appendChild(createSVGElement('rect', {{
                    x: PLOT_X, y: yThreshold80,
                    width: xThreshold - PLOT_X, height: (PLOT_Y + PLOT_H) - yThreshold80,
                    fill: '#FFF1F2', opacity: 0.65
                }}));
                // Q3: Bottom Right (x >= 4.0, y < 80.0)
                svg.appendChild(createSVGElement('rect', {{
                    x: xThreshold, y: yThreshold80,
                    width: (PLOT_X + PLOT_W) - xThreshold, height: (PLOT_Y + PLOT_H) - yThreshold80,
                    fill: '#FFFBEB', opacity: 0.65
                }}));

                // Hitung kuadran dinamis untuk Watermark S1
                const qCounts = {{ 'I': 0, 'II': 0, 'III': 0, 'IV': 0 }};
                currentList.forEach(p => {{
                    if (qCounts[p.kuadran] !== undefined) qCounts[p.kuadran]++;
                }});

                // Watermark Quadrant Titles S1 (2 Baris Rapi, Bebas Tabrakan dengan Ambang Batas)
                // Q1 (Top-Right)
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + 18, 'end', '12', '800', '#059669', 0.85, 'KUADRAN I: UNGGULAN'));
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + 32, 'end', '10.5', '700', '#059669', 0.85, `(${{qCounts['I']}} Prodi)`));

                // Q2 (Top-Left)
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + 18, 'start', '12', '800', '#2563EB', 0.85, 'KUADRAN II: STABIL'));
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + 32, 'start', '10.5', '700', '#2563EB', 0.85, `(${{qCounts['II']}} Prodi)`));

                // Q3 (Bottom-Right)
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + PLOT_H - 26, 'end', '12', '800', '#D97706', 0.85, 'KUADRAN III: BELUM OPTIMAL'));
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + PLOT_H - 12, 'end', '10.5', '700', '#D97706', 0.85, `(${{qCounts['III']}} Prodi)`));

                // Q4 (Bottom-Left: Bebas Tabrakan dengan Badge Ambang Tengah)
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + PLOT_H - 26, 'start', '12', '800', '#E11D48', 0.85, 'KUADRAN IV: PERLU DITINGKATKAN'));
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + PLOT_H - 12, 'start', '10.5', '700', '#E11D48', 0.85, `(${{qCounts['IV']}} Prodi)`));

                // Gridlines S1
                const yTicks = [30, 40, 50, 60, 70, 80, 90, 100];
                yTicks.forEach(yt => {{
                    const yPos = mapY(yt);
                    svg.appendChild(createLine(PLOT_X, yPos, PLOT_X + PLOT_W, yPos, '#E2E8F0', 1, '2,3'));
                    svg.appendChild(createText(PLOT_X - 10, yPos + 4, 'end', '11', '600', '#64748B', 1, yt + '%'));
                }});

                const xTicks = [0, 1, 2, 3, 4, 6, 8, 10, 15, 20, 25, 30, 40, 50];
                xTicks.forEach(xt => {{
                    const xPos = mapX(xt);
                    svg.appendChild(createLine(xPos, PLOT_Y, xPos, PLOT_Y + PLOT_H, '#E2E8F0', 1, '2,3'));
                    svg.appendChild(createText(xPos, PLOT_Y + PLOT_H + 18, 'middle', '11', '600', '#64748B', 1, xt));
                }});

                // Benchmark Lines S1
                svg.appendChild(createLine(xThreshold, PLOT_Y, xThreshold, PLOT_Y + PLOT_H, '#64748B', 2.0, '5,4', 0.95));
                svg.appendChild(createLine(PLOT_X, yThreshold80, PLOT_X + PLOT_W, yThreshold80, '#64748B', 2.0, '5,4', 0.95));

                // Badges S1
                svg.appendChild(createPillBadge(xThreshold, PLOT_Y + PLOT_H - 16, 190, 22, '#475569', '#94A3B8', '#FFFFFF', '▲ AMBANG KEKETATAN: 4,0 : 1'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 130, yThreshold80, 250, 22, '#475569', '#94A3B8', '#FFFFFF', 'STANDAR KETERISIAN: 80% (TARGET SEHAT)'));

            }} else {{
                // 2. D3 Canvas Rendering (Linear X 0-21, Critical Red Line 50%, Anomaly Banner)
                const yThreshold50 = mapY(50.0);

                // D3 Background Shading
                // Upper right (x >= 4.0, y >= 80)
                svg.appendChild(createSVGElement('rect', {{
                    x: xThreshold, y: PLOT_Y,
                    width: (PLOT_X + PLOT_W) - xThreshold, height: yThreshold80 - PLOT_Y,
                    fill: '#F0FDF4', opacity: 0.50
                }}));
                // Upper left (x < 4.0, y >= 80)
                svg.appendChild(createSVGElement('rect', {{
                    x: PLOT_X, y: PLOT_Y,
                    width: xThreshold - PLOT_X, height: yThreshold80 - PLOT_Y,
                    fill: '#F0F9FF', opacity: 0.50
                }}));
                // Lower left (x < 4.0, y < 80)
                svg.appendChild(createSVGElement('rect', {{
                    x: PLOT_X, y: yThreshold80,
                    width: xThreshold - PLOT_X, height: (PLOT_Y + PLOT_H) - yThreshold80,
                    fill: '#FFF1F2', opacity: 0.50
                }}));
                // Lower right (x >= 4.0, 50 <= y < 80) - Amber Zone
                svg.appendChild(createSVGElement('rect', {{
                    x: xThreshold, y: yThreshold80,
                    width: (PLOT_X + PLOT_W) - xThreshold, height: yThreshold50 - yThreshold80,
                    fill: '#FFFBEB', opacity: 0.65
                }}));
                // Lower right below 50% (x >= 4.0, y < 50) - Rose Critical Zone
                svg.appendChild(createSVGElement('rect', {{
                    x: xThreshold, y: yThreshold50,
                    width: (PLOT_X + PLOT_W) - xThreshold, height: (PLOT_Y + PLOT_H) - yThreshold50,
                    fill: '#FFF1F2', opacity: 0.75
                }}));

                // D3 Gridlines (Linear X: 0 to 20)
                const yTicks = [20, 30, 40, 50, 60, 70, 80, 90, 100];
                yTicks.forEach(yt => {{
                    const yPos = mapY(yt);
                    svg.appendChild(createLine(PLOT_X, yPos, PLOT_X + PLOT_W, yPos, '#E2E8F0', 1, '2,3'));
                    svg.appendChild(createText(PLOT_X - 10, yPos + 4, 'end', '11', '600', '#64748B', 1, yt + '%'));
                }});

                const xTicks = [0, 2.5, 5.0, 7.5, 10.0, 12.5, 15.0, 17.5, 20.0];
                xTicks.forEach(xt => {{
                    const xPos = mapX(xt);
                    svg.appendChild(createLine(xPos, PLOT_Y, xPos, PLOT_Y + PLOT_H, '#E2E8F0', 1, '2,3'));
                    svg.appendChild(createText(xPos, PLOT_Y + PLOT_H + 18, 'middle', '11', '600', '#64748B', 1, xt.toFixed(1)));
                }});

                // Benchmark Lines D3
                // Ambang Keketatan 4,0:1
                svg.appendChild(createLine(xThreshold, PLOT_Y, xThreshold, PLOT_Y + PLOT_H, '#64748B', 2.0, '5,4', 0.95));
                // Standar Keterisian Kuota Sehat 80% (Dashed slate)
                svg.appendChild(createLine(PLOT_X, yThreshold80, PLOT_X + PLOT_W, yThreshold80, '#64748B', 1.8, '5,4', 0.90));
                // Batas Kritis Kelayakan Operasional 50% (Prominent Red Dotted Line)
                svg.appendChild(createLine(PLOT_X, yThreshold50, PLOT_X + PLOT_W, yThreshold50, '#DC2626', 2.2, '3,4', 0.95));

                // Badges D3
                svg.appendChild(createPillBadge(xThreshold, PLOT_Y + PLOT_H - 18, 190, 22, '#475569', '#94A3B8', '#FFFFFF', '▲ AMBANG KEKETATAN: 4,0 : 1'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 130, yThreshold80, 240, 22, '#475569', '#94A3B8', '#FFFFFF', 'STANDAR SEHAT: 80% KETERISIAN'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 145, yThreshold50, 270, 22, '#DC2626', '#F87171', '#FFFFFF', '⚠ BATAS KRITIS KELAYAKAN: 50%'));

                // Callout Banner: Anomali Struktural Vokasi USK
                const bannerGroup = createSVGElement('g', {{ transform: `translate(${{PLOT_X + PLOT_W / 2}}, ${{PLOT_Y + 49}})` }});
                const bannerRect = createSVGElement('rect', {{
                    x: -290, y: -26, width: 580, height: 52, rx: 12,
                    fill: '#FFFBEB', stroke: '#F59E0B', 'stroke-width': 1.5, opacity: 0.97
                }});
                const bannerT1 = createText(0, -7, 'middle', '11.5', '800', '#92400E', 1, 'TEMUAN ANOMALI STRUKTURAL VOKASI USK:');
                const bannerT2 = createText(0, 11, 'middle', '10', '700', '#B45309', 1, '100% (11 Prodi D3) Terkonsentrasi di Kuadran III: Belum Optimal (Keketatan 5,3×–17,7×, FR < 80%)');
                bannerGroup.appendChild(bannerRect);
                bannerGroup.appendChild(bannerT1);
                bannerGroup.appendChild(bannerT2);
                svg.appendChild(bannerGroup);

                // Watermark Quadrant Titles D3 (Format & Desain Seragam 100% dengan S1)
                // Q1 (Top-Right)
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + 18, 'end', '12', '800', '#059669', 0.85, 'KUADRAN I: UNGGULAN'));
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + 32, 'end', '10', '600', '#64748B', 0.85, '(0 Prodi / 0%)'));

                // Q2 (Top-Left)
                svg.appendChild(createText(PLOT_X + 8, PLOT_Y + 18, 'start', '11', '800', '#2563EB', 0.85, 'KUADRAN II: STABIL'));
                svg.appendChild(createText(PLOT_X + 8, PLOT_Y + 32, 'start', '9.5', '600', '#64748B', 0.85, '(0 Prodi / 0%)'));

                // Q3 (Bottom-Right)
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + PLOT_H - 24, 'end', '12.5', '800', '#D97706', 0.95, 'KUADRAN III: BELUM OPTIMAL'));
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + PLOT_H - 10, 'end', '10.5', '700', '#B45309', 0.90, '(11 Prodi / 100% Vokasi)'));

                // Q4 (Bottom-Left)
                svg.appendChild(createText(PLOT_X + 8, yThreshold80 + 20, 'start', '10.5', '800', '#E11D48', 0.85, 'KUADRAN IV: PERLU DITINGKATKAN'));
                svg.appendChild(createText(PLOT_X + 8, yThreshold80 + 34, 'start', '9.5', '600', '#64748B', 0.85, '(0 Prodi / 0%)'));
            }}

            // Axis Titles
            svg.appendChild(createText(PLOT_X + PLOT_W / 2, PLOT_Y + PLOT_H + 42, 'middle', '12.5', '700', '#0F172A', 1, 'Rasio Keketatan Seleksi (Peminat per 1 Kursi Daya Tampung)'));
            const yTitle = createText(-(PLOT_Y + PLOT_H / 2), 18, 'middle', '12.5', '700', '#0F172A', 1, 'Persentase Keterisian Kuota / Fill Rate (%)');
            yTitle.setAttribute('transform', 'rotate(-90)');
            svg.appendChild(yTitle);

            // Render Dots, Leader Lines & Interactive Badges
            const dotsGroup = createSVGElement('g', {{ id: 'dots-group' }});
            const leaderLinesGroup = createSVGElement('g', {{ id: 'leader-lines-group' }});
            const labelsGroup = createSVGElement('g', {{ id: 'labels-group' }});

            let matchCount = 0;
            const itemsToLabel = [];

            currentList.forEach(d => {{
                const visible = isProdiVisible(d);
                if (visible) matchCount++;

                const cx = mapX(d.keketatan);
                const cy = mapY(clampFR(d.fill_rate));
                const rRadius = 7.5;

                const circle = createSVGElement('circle', {{
                    cx: cx,
                    cy: cy,
                    r: selectedProdiId === d.id ? 10.5 : rRadius,
                    fill: d.color,
                    stroke: selectedProdiId === d.id ? '#0F172A' : '#FFFFFF',
                    'stroke-width': selectedProdiId === d.id ? 3.5 : 2.0,
                    opacity: visible ? 0.92 : 0.12,
                    class: `dot ${{visible ? '' : 'dimmed'}} ${{selectedProdiId === d.id ? 'selected' : ''}}`,
                    'data-id': d.id
                }});

                circle.addEventListener('mouseenter', (e) => onDotHover(e, d));
                circle.addEventListener('mousemove', (e) => TooltipManager.updatePosition(e.clientX, e.clientY));
                circle.addEventListener('mouseleave', () => onDotLeave(d));
                circle.addEventListener('click', () => onDotClick(d));

                dotsGroup.appendChild(circle);

                // Labels: Tampil jika tombol Toggle Semua Label aktif ATAU titik sedang diklik ATAU cocok dengan pencarian
                const isSearchHit = (searchQuery.trim() !== "" && matchSearchQuery(d, searchQuery));
                const showThisLabel = showAllLabels || (selectedProdiId === d.id) || (isSearchHit && visible);

                if (showThisLabel && visible) {{
                    const shortText = formatShortProdiLabel(d);
                    const estW = Math.max(38, Math.round(shortText.length * 5.2 + 10));
                    itemsToLabel.push({{
                        id: d.id,
                        d: d,
                        x0: cx,
                        y0: cy,
                        text: shortText,
                        w: estW,
                        h: 15.0,
                        lx: cx,
                        ly: cy
                    }});
                }}
            }});

            // Jalankan Anti-Collision Solver
            const plotBounds = {{
                minX: PLOT_X + 6,
                maxX: PLOT_X + PLOT_W - 6,
                minY: PLOT_Y + 6,
                maxY: PLOT_Y + PLOT_H - 6
            }};
            const solvedLabels = solveLabelLayout(itemsToLabel, plotBounds);

            // 1. Gambar Leader Lines (di bawah badges)
            solvedLabels.forEach(it => {{
                if (it.needsLeaderLine) {{
                    const line = createSVGElement('line', {{
                        x1: it.x0,
                        y1: it.y0,
                        x2: it.edgeX,
                        y2: it.edgeY,
                        stroke: '#94A3B8',
                        'stroke-width': 0.85,
                        'stroke-linecap': 'round',
                        opacity: 0.85,
                        class: 'leader-line',
                        'data-id': it.id
                    }});
                    leaderLinesGroup.appendChild(line);
                }}
            }});

            // 2. Gambar Badge Labels Interaktif
            solvedLabels.forEach(it => {{
                const isSelected = (selectedProdiId === it.d.id);
                const badgeG = createSVGElement('g', {{
                    class: `label-badge ${{isSelected ? 'selected' : ''}}`,
                    'data-id': it.id,
                    transform: `translate(${{it.lx}}, ${{it.ly}})`
                }});

                const rect = createSVGElement('rect', {{
                    x: -it.w / 2,
                    y: -it.h / 2,
                    width: it.w,
                    height: it.h,
                    rx: 3.5,
                    fill: '#FFFFFF',
                    'fill-opacity': 0.95,
                    stroke: isSelected ? it.d.color : '#CBD5E1',
                    'stroke-width': isSelected ? 1.8 : 0.85,
                    class: 'badge-rect'
                }});

                const txt = createSVGElement('text', {{
                    x: 0,
                    y: 0,
                    'dominant-baseline': 'central',
                    'text-anchor': 'middle',
                    fill: '#1E293B',
                    class: 'badge-text'
                }});
                txt.textContent = it.text;

                badgeG.appendChild(rect);
                badgeG.appendChild(txt);

                // Event listener badge
                badgeG.addEventListener('mouseenter', (e) => onBadgeHover(e, it.d));
                badgeG.addEventListener('mousemove', (e) => TooltipManager.updatePosition(e.clientX, e.clientY));
                badgeG.addEventListener('mouseleave', () => onBadgeLeave(it.d));
                badgeG.addEventListener('click', () => onDotClick(it.d));

                labelsGroup.appendChild(badgeG);
            }});

            // Urutan render SVG:
            // Background & Grid -> Leader Lines -> Dots -> Label Badges
            svg.appendChild(leaderLinesGroup);
            svg.appendChild(dotsGroup);
            svg.appendChild(labelsGroup);

            // Update match counter
            document.getElementById('match-counter').textContent = `Menampilkan: ${{matchCount}}/${{currentList.length}} Prodi`;

            // Canvas Footnote Visibility (Hanya muncul saat mode 60 prodi aktif)
            const fnEl = document.getElementById('canvas-footnote-note');
            if (fnEl) {{
                fnEl.style.display = (currentLevel === 's1' && currentS1Subset === 'established') ? 'flex' : 'none';
            }}
        }}

        function createLine(x1, y1, x2, y2, stroke, width, dash = '', opacity = 1) {{
            const attrs = {{
                x1: x1, y1: y1, x2: x2, y2: y2,
                stroke: stroke, 'stroke-width': width, opacity: opacity
            }};
            if (dash) attrs['stroke-dasharray'] = dash;
            return createSVGElement('line', attrs);
        }}

        function createText(x, y, anchor, size, weight, fill, opacity, content) {{
            const t = createSVGElement('text', {{
                x: x, y: y, 'text-anchor': anchor,
                'font-size': size, 'font-weight': weight, fill: fill, opacity: opacity
            }});
            t.textContent = content;
            return t;
        }}

        function createPillBadge(x, y, w, h, bg, border, textColor, textContent) {{
            const g = createSVGElement('g', {{ transform: `translate(${{x}}, ${{y}})` }});
            const rect = createSVGElement('rect', {{
                x: -w/2, y: -h/2, width: w, height: h, rx: h/2,
                fill: bg, stroke: border, 'stroke-width': 1.2
            }});
            const t = createSVGElement('text', {{
                x: 0, y: 4, 'text-anchor': 'middle',
                'font-size': '10', 'font-weight': '700', fill: textColor
            }});
            t.textContent = textContent;
            g.appendChild(rect);
            g.appendChild(t);
            return g;
        }}

        // Boundary Safeguard: Sembunyikan tooltip saat kursor keluar canvas atau di ruang kosong
        const svgContainerEl = document.getElementById('svg-container');
        if (svgContainerEl) {{
            svgContainerEl.addEventListener('mouseleave', () => {{
                TooltipManager.hide();
            }});
            svgContainerEl.addEventListener('mousemove', (e) => {{
                if (!e.target.closest('.dot, .label-badge') && TooltipManager.activeProdiId !== null) {{
                    TooltipManager.hide();
                }}
            }});
        }}

        window.addEventListener('scroll', () => {{
            TooltipManager.hide();
        }}, {{ passive: true }});
        window.addEventListener('resize', () => {{
            TooltipManager.hide();
        }});
        window.addEventListener('beforeprint', () => {{
            TooltipManager.hide();
        }});





        function onDotClick(d) {{
            TooltipManager.hide();
            if (selectedProdiId === d.id) {{
                selectedProdiId = null;
                document.getElementById('ins-content').style.display = 'none';
                document.getElementById('ins-placeholder').style.display = 'block';
                updatePlaceholderView();
                renderChart();
            }} else {{
                selectedProdiId = d.id;
                renderChart();
                showInspector(d);
            }}
        }}

        function selectD3ProdiByName(keyword) {{
            const list = DATA_BY_LEVEL.d3;
            const p = list.find(item => item.nama.toUpperCase().includes(keyword.toUpperCase()));
            if (p) {{
                if (currentD3Tier !== 'ALL' && p.tier !== currentD3Tier) {{
                    currentD3Tier = 'ALL';
                    updateD3TierControls();
                }}
                selectedProdiId = p.id;
                renderChart();
                showInspector(p);
            }}
        }}

        function closeInspector() {{
            TooltipManager.hide();
            selectedProdiId = null;
            document.getElementById('ins-content').style.display = 'none';
            document.getElementById('ins-placeholder').style.display = 'block';
            updatePlaceholderView();
            renderChart();
        }}

        function showInspector(d) {{
            document.getElementById('ins-placeholder').style.display = 'none';
            const content = document.getElementById('ins-content');
            content.style.display = 'block';

            document.getElementById('ins-fak').textContent = `${{d.fakultas_abbr}} • ${{d.fakultas}} (${{d.jenjang}})`;
            
            // Kuadran Tag (Tetap utuh satu baris tanpa wrap)
            const qTag = document.getElementById('ins-quad-tag');
            qTag.textContent = d.kuadran_title;
            qTag.style.backgroundColor = d.color;

            // Tier Tag (Khusus D3, tampil sebagai badge mandiri yang proporsional)
            const tierTag = document.getElementById('ins-tier-tag');
            if (currentLevel === 'd3') {{
                tierTag.style.display = 'inline-flex';
                if (d.tier === 1) {{
                    tierTag.textContent = '⭐ Klaster 1: Kompetitif';
                    tierTag.style.background = '#DCFCE7';
                    tierTag.style.color = '#166534';
                    tierTag.style.borderColor = '#86EFAC';
                }} else if (d.tier === 2) {{
                    tierTag.textContent = '🔄 Klaster 2: Perlu Pendampingan';
                    tierTag.style.background = '#FEF3C7';
                    tierTag.style.color = '#92400E';
                    tierTag.style.borderColor = '#FDE68A';
                }} else {{
                    tierTag.textContent = '📉 Klaster 3: Evaluasi Khusus';
                    tierTag.style.background = '#FFE4E6';
                    tierTag.style.color = '#9F1239';
                    tierTag.style.borderColor = '#FECDD3';
                }}
            }} else {{
                tierTag.style.display = 'none';
            }}

            document.getElementById('ins-name').textContent = (d.jenjang === 'D3' ? 'D3 ' : '') + d.nama;
            
            // Subtitle deskripsi status kuadran ringkas 1 kalimat (Bersih & tidak ramai)
            document.getElementById('ins-quad-desc').textContent = d.kuadran_desc;

            document.getElementById('ins-keketatan').textContent = `${{d.keketatan}} : 1`;
            document.getElementById('ins-keketatan-status').textContent = d.keketatan >= 4.0 ? 'Keketatan Selektif (>= 4x)' : 'Keketatan Rendah (< 4x)';

            const frCapped = clampFR(d.fill_rate);
            document.getElementById('ins-fillrate').textContent = `${{frCapped.toFixed(1)}}%`;
            if (currentLevel === 's1') {{
                document.getElementById('ins-fillrate-status').textContent = frCapped >= 80.0 ? 'Kuota Sehat (>= 80%)' : 'Under-Enrolled (< 80%)';
            }} else {{
                document.getElementById('ins-fillrate-status').textContent = frCapped >= 50.0 ? 'Di Atas Batas Kritis (>= 50%)' : 'Kritis Defisit (< 50%)';
            }}

            document.getElementById('ins-peminat').textContent = `${{Math.round(d.peminat_5thn).toLocaleString('id-ID')}} org/thn`;
            document.getElementById('ins-dt').textContent = `${{Math.round(d.dt_5thn)}} kursi/thn`;
            document.getElementById('ins-sisa-kursi').textContent = d.sisa_5thn > 0 ? `Bocor/Kosong: ${{d.sisa_5thn}} kursi` : 'Kuota Terserap Penuh (100%)';

            document.getElementById('ins-rekomendasi-text').textContent = d.rekomendasi;
            document.getElementById('ins-tren-tag').textContent = d.tren_resmi.toUpperCase();

            // Render table with 100% Capped Fill Rate
            const tbody = document.getElementById('ins-history-tbody');
            tbody.innerHTML = '';
            d.history.forEach(h => {{
                const frHistory = clampFR(h.fill_rate);
                const tr = document.createElement('tr');
                const thresholdBenchmark = (currentLevel === 's1') ? 80.0 : 50.0;
                tr.innerHTML = `
                    <td>${{h.tahun}}</td>
                    <td>${{h.peminat.toLocaleString('id-ID')}}</td>
                    <td>${{h.dt}}</td>
                    <td>${{h.du}}</td>
                    <td style="font-weight:700; color:${{frHistory >= thresholdBenchmark ? '#059669' : '#DC2626'}}">${{frHistory.toFixed(1)}}%</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Sub-Tier Guide Card State & Visibility Handlers
        function updateTierGuideCardStates() {{
            [1, 2, 3].forEach(tierNum => {{
                const card = document.getElementById(`card-tier-${{tierNum}}`);
                if (card) {{
                    card.classList.toggle('active', currentD3Tier === tierNum);
                }}
            }});
        }}

        function updateD3TierStripVisibility() {{
            const strip = document.getElementById('d3-tier-legend-strip');
            if (strip) {{
                strip.style.display = (currentLevel === 'd3') ? 'grid' : 'none';
            }}
        }}

        function updatePlaceholderView() {{
            const phS1 = document.getElementById('ins-placeholder-s1');
            const phD3 = document.getElementById('ins-placeholder-d3');
            if (phS1 && phD3) {{
                if (currentLevel === 'd3') {{
                    phS1.style.display = 'none';
                    phD3.style.display = 'block';
                }} else {{
                    phS1.style.display = 'block';
                    phD3.style.display = 'none';
                }}
            }}
        }}

        // Click Event Handlers on Tier Guide Cards
        [1, 2, 3].forEach(tierNum => {{
            const card = document.getElementById(`card-tier-${{tierNum}}`);
            if (card) {{
                card.addEventListener('click', () => {{
                    currentD3Tier = (currentD3Tier === tierNum) ? 'ALL' : tierNum;
                    updateTierGuideCardStates();
                    renderFacultyFilters();
                    renderChart();
                }});
            }}
        }});

        // S1 Subset Switcher Event Handlers
        document.querySelectorAll('.subset-tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                const targetSubset = tab.getAttribute('data-subset');
                if (currentS1Subset === targetSubset) return;

                currentS1Subset = targetSubset;
                document.querySelectorAll('.subset-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Reset filter & seleksi
                currentFaculty = "ALL";
                currentFilterCard = "ALL";
                searchQuery = "";
                document.getElementById('prodi-search').value = "";
                selectedProdiId = null;

                // Update Header Titles & Badge
                if (currentS1Subset === 'all') {{
                    document.getElementById('header-main-title').textContent = 'PETA KUADRAN 66 PROGRAM STUDI S1 LENGKAP USK';
                    document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (66 Prodi S1 Lengkap)';
                    document.getElementById('tab-s1-badge').textContent = '66 Prodi';
                }} else {{
                    document.getElementById('header-main-title').textContent = 'PETA KUADRAN 60 PROGRAM STUDI S1 KAMPUS UTAMA USK';
                    document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (60 Prodi S1 Kampus Utama)';
                    document.getElementById('tab-s1-badge').textContent = '60 Prodi';
                }}

                document.getElementById('ins-content').style.display = 'none';
                document.getElementById('ins-placeholder').style.display = 'block';
                updatePlaceholderView();

                renderKPIRibbon();
                renderFacultyFilters();
                renderChart();

                // Sinkronisasi URL Hash
                syncUrlHash();
            }});
        }});

        // Level Switcher Event Handlers
        document.querySelectorAll('.level-tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                const targetLevel = tab.getAttribute('data-level');
                if (currentLevel === targetLevel) return;

                currentLevel = targetLevel;
                document.querySelectorAll('.level-tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');

                // Reset filters on level switch
                currentFaculty = "ALL";
                currentFilterCard = "ALL";
                currentD3Tier = "ALL";
                searchQuery = "";
                document.getElementById('prodi-search').value = "";
                document.getElementById('search-clear-btn').style.display = 'none';
                document.getElementById('search-dropdown').style.display = 'none';
                selectedProdiId = null;

                // Toggle S1 Subset Switcher visibility
                const subsetSwitcher = document.getElementById('s1-subset-switcher');
                if (subsetSwitcher) {{
                    subsetSwitcher.style.display = (currentLevel === 's1') ? 'inline-flex' : 'none';
                }}

                // Update Header and Subtitles
                if (currentLevel === 's1') {{
                    if (currentS1Subset === 'all') {{
                        document.getElementById('header-main-title').textContent = 'PETA KUADRAN 66 PROGRAM STUDI S1 LENGKAP USK';
                        document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (66 Prodi S1 Lengkap)';
                        document.getElementById('tab-s1-badge').textContent = '66 Prodi';
                    }} else {{
                        document.getElementById('header-main-title').textContent = 'PETA KUADRAN 60 PROGRAM STUDI S1 KAMPUS UTAMA USK';
                        document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (60 Prodi S1 Kampus Utama)';
                        document.getElementById('tab-s1-badge').textContent = '60 Prodi';
                    }}
                    document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi S1: <strong>Keketatan 4,0 : 1</strong> | <strong>Keterisian Sehat 80%</strong>';
                }} else {{
                    document.getElementById('header-main-title').textContent = 'PETA KUADRAN 11 PROGRAM STUDI D3 VOKASI USK';
                    document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (11 Prodi D3 Vokasi)';
                    document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi D3: <strong>Keketatan 4,0 : 1</strong> | <strong>Standar Sehat 80%</strong> | <strong>Batas Kritis 50%</strong>';
                }}

                updateD3TierStripVisibility();
                updateTierGuideCardStates();

                renderKPIRibbon();
                renderFacultyFilters();
                renderChart();

                // Pastikan panel inspector dan placeholder kembali bersih sesuai level
                selectedProdiId = null;
                document.getElementById('ins-content').style.display = 'none';
                document.getElementById('ins-placeholder').style.display = 'block';
                updatePlaceholderView();

                // Sinkronisasi URL Hash
                syncUrlHash();
            }});
        }});

        // Smart Search Dropdown & Keyboard Navigation
        let activeDropdownIndex = -1;

        function updateSearchDropdown() {{
            const dropdown = document.getElementById('search-dropdown');
            const clearBtn = document.getElementById('search-clear-btn');
            const q = searchQuery.trim();

            if (!q) {{
                dropdown.style.display = 'none';
                clearBtn.style.display = 'none';
                activeDropdownIndex = -1;
                return;
            }}

            clearBtn.style.display = 'flex';

            // Filter active list by smart search
            const activeList = getActiveList().filter(d => {{
                if (currentLevel === 's1' && currentS1Subset === 'established' && d.is_prodi_baru) return false;
                return matchSearchQuery(d, q);
            }});

            dropdown.innerHTML = '';
            activeDropdownIndex = -1;

            if (activeList.length === 0) {{
                dropdown.innerHTML = '<div class="search-dropdown-empty">🔍 Tidak ada program studi yang cocok</div>';
                dropdown.style.display = 'block';
                return;
            }}

            const maxResults = activeList.slice(0, 15);
            maxResults.forEach((d, idx) => {{
                const item = document.createElement('div');
                item.className = 'search-dropdown-item';
                item.setAttribute('data-id', d.id);
                item.setAttribute('data-idx', idx);

                const prodiDisplay = (d.jenjang === 'D3' ? 'D3 ' : '') + d.nama;
                const fakBadge = d.fakultas_abbr || d.fakultas;

                let quadBadgeHtml = '';
                if (currentLevel === 'd3') {{
                    const tierColors = {{
                        1: {{ bg: '#ECFDF5', text: '#059669', border: '#A7F3D0', label: '⭐ Klaster 1' }},
                        2: {{ bg: '#EFF6FF', text: '#2563EB', border: '#BFDBFE', label: '🔄 Klaster 2' }},
                        3: {{ bg: '#FEF2F2', text: '#DC2626', border: '#FECACA', label: '📉 Klaster 3' }}
                    }};
                    const tc = tierColors[d.tier] || tierColors[2];
                    quadBadgeHtml = `<span class="search-badge-quad" style="background:${{tc.bg}}; color:${{tc.text}}; border:1px solid ${{tc.border}};">${{tc.label}}</span>`;
                }} else {{
                    const quadColors = {{
                        'I': {{ bg: '#ECFDF5', text: '#059669', border: '#A7F3D0', label: 'Kuadran I' }},
                        'II': {{ bg: '#EFF6FF', text: '#2563EB', border: '#BFDBFE', label: 'Kuadran II' }},
                        'III': {{ bg: '#FFFBEB', text: '#D97706', border: '#FDE68A', label: 'Kuadran III' }},
                        'IV': {{ bg: '#FEF2F2', text: '#E11D48', border: '#FECDD3', label: 'Kuadran IV' }}
                    }};
                    const qc = quadColors[d.kuadran] || quadColors['I'];
                    quadBadgeHtml = `<span class="search-badge-quad" style="background:${{qc.bg}}; color:${{qc.text}}; border:1px solid ${{qc.border}};">${{qc.label}}</span>`;
                }}

                item.innerHTML = `
                    <div class="search-item-left">
                        <span class="search-item-dot" style="background: ${{d.color}};"></span>
                        <span class="search-item-name" title="${{prodiDisplay}}">${{prodiDisplay}}</span>
                    </div>
                    <div class="search-item-badges">
                        <span class="search-badge-fak">${{fakBadge}}</span>
                        ${{quadBadgeHtml}}
                    </div>
                `;

                item.addEventListener('click', () => {{
                    selectSearchResult(d);
                }});

                dropdown.appendChild(item);
            }});

            dropdown.style.display = 'block';
        }}

        function selectSearchResult(d) {{
            TooltipManager.hide();
            const input = document.getElementById('prodi-search');
            input.value = (d.jenjang === 'D3' ? 'D3 ' : '') + d.nama;
            searchQuery = input.value;

            document.getElementById('search-dropdown').style.display = 'none';
            document.getElementById('search-clear-btn').style.display = 'flex';

            // Reset conflicting filters if needed
            if (currentLevel === 'd3' && currentD3Tier !== 'ALL' && d.tier !== currentD3Tier) {{
                currentD3Tier = 'ALL';
                updateD3TierControls();
            }}
            if (currentFilterCard !== 'ALL' && d.kuadran !== currentFilterCard) {{
                currentFilterCard = 'ALL';
                renderKPIRibbon();
            }}
            if (currentFaculty !== 'ALL' && d.fakultas !== currentFaculty) {{
                currentFaculty = 'ALL';
                renderFacultyFilters();
            }}

            selectedProdiId = d.id;
            renderChart();
            showInspector(d);
        }}

        // Search Input Handlers
        const searchInput = document.getElementById('prodi-search');
        searchInput.addEventListener('input', (e) => {{
            TooltipManager.hide();
            searchQuery = e.target.value;
            renderChart();
            updateSearchDropdown();
        }});

        searchInput.addEventListener('focus', () => {{
            if (searchQuery.trim()) {{
                updateSearchDropdown();
            }}
        }});

        searchInput.addEventListener('keydown', (e) => {{
            const dropdown = document.getElementById('search-dropdown');
            if (dropdown.style.display === 'none') return;

            const items = dropdown.querySelectorAll('.search-dropdown-item');
            if (items.length === 0) return;

            if (e.key === 'ArrowDown') {{
                e.preventDefault();
                activeDropdownIndex = (activeDropdownIndex + 1) % items.length;
                items.forEach((it, i) => it.classList.toggle('active-item', i === activeDropdownIndex));
                items[activeDropdownIndex]?.scrollIntoView({{ block: 'nearest' }});
            }} else if (e.key === 'ArrowUp') {{
                e.preventDefault();
                activeDropdownIndex = (activeDropdownIndex - 1 + items.length) % items.length;
                items.forEach((it, i) => it.classList.toggle('active-item', i === activeDropdownIndex));
                items[activeDropdownIndex]?.scrollIntoView({{ block: 'nearest' }});
            }} else if (e.key === 'Enter') {{
                e.preventDefault();
                if (activeDropdownIndex >= 0 && items[activeDropdownIndex]) {{
                    items[activeDropdownIndex].click();
                }} else if (items.length > 0) {{
                    items[0].click();
                }}
            }} else if (e.key === 'Escape') {{
                dropdown.style.display = 'none';
            }}
        }});

        // Clear Search Button
        document.getElementById('search-clear-btn').addEventListener('click', () => {{
            TooltipManager.hide();
            const input = document.getElementById('prodi-search');
            input.value = '';
            searchQuery = '';
            document.getElementById('search-clear-btn').style.display = 'none';
            document.getElementById('search-dropdown').style.display = 'none';
            renderChart();
            input.focus();
        }});

        // Dismiss dropdown on outside click
        document.addEventListener('click', (e) => {{
            const wrapper = document.getElementById('search-box-wrapper');
            if (wrapper && !wrapper.contains(e.target)) {{
                document.getElementById('search-dropdown').style.display = 'none';
            }}
        }});

        // Toggle Labels
        document.getElementById('btn-toggle-labels').addEventListener('click', (e) => {{
            TooltipManager.hide();
            showAllLabels = !showAllLabels;
            e.target.classList.toggle('active', showAllLabels);
            renderChart();
        }});

        // Reset Filters Button
        document.getElementById('btn-reset-filters').addEventListener('click', () => {{
            TooltipManager.hide();
            currentFaculty = "ALL";
            currentFilterCard = "ALL";
            currentD3Tier = "ALL";
            searchQuery = "";
            showAllLabels = false;
            selectedProdiId = null;

            document.getElementById('prodi-search').value = "";
            document.getElementById('search-clear-btn').style.display = 'none';
            document.getElementById('search-dropdown').style.display = 'none';
            document.getElementById('btn-toggle-labels').classList.remove('active');

            updateTierGuideCardStates();

            document.getElementById('ins-content').style.display = 'none';
            document.getElementById('ins-placeholder').style.display = 'block';
            updatePlaceholderView();

            renderKPIRibbon();
            renderFacultyFilters();
            renderChart();
        }});

        // Initial Load
        const subsetSwitcher = document.getElementById('s1-subset-switcher');
        if (currentLevel === 'd3') {{
            document.querySelectorAll('.level-tab').forEach(t => {{
                t.classList.toggle('active', t.getAttribute('data-level') === 'd3');
            }});
            document.getElementById('header-main-title').textContent = 'PETA KUADRAN 11 PROGRAM STUDI D3 VOKASI USK';
            document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (11 Prodi D3 Vokasi)';
            document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi D3: <strong>Keketatan 4,0 : 1</strong> | <strong>Standar Sehat 80%</strong> | <strong>Batas Kritis 50%</strong>';
            if (subsetSwitcher) subsetSwitcher.style.display = 'none';
        }} else {{
            if (subsetSwitcher) subsetSwitcher.style.display = 'inline-flex';
            if (currentS1Subset === 'established') {{
                document.querySelectorAll('.subset-tab').forEach(t => {{
                    t.classList.toggle('active', t.getAttribute('data-subset') === 'established');
                }});
                document.getElementById('header-main-title').textContent = 'PETA KUADRAN 60 PROGRAM STUDI S1 KAMPUS UTAMA USK';
                document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (60 Prodi S1 Kampus Utama)';
                document.getElementById('tab-s1-badge').textContent = '60 Prodi';
            }} else {{
                document.querySelectorAll('.subset-tab').forEach(t => {{
                    t.classList.toggle('active', t.getAttribute('data-subset') === 'all');
                }});
                document.getElementById('header-main-title').textContent = 'PETA KUADRAN 66 PROGRAM STUDI S1 LENGKAP USK';
                document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (66 Prodi S1 Lengkap)';
                document.getElementById('tab-s1-badge').textContent = '66 Prodi';
            }}
        }}

        updateD3TierStripVisibility();
        updateTierGuideCardStates();

        renderKPIRibbon();
        renderFacultyFilters();
        renderChart();

        // Initial Load bersih (tanpa auto-select, kanvas bebas dari label mengambang)
        selectedProdiId = null;
        document.getElementById('ins-content').style.display = 'none';
        document.getElementById('ins-placeholder').style.display = 'block';
        updatePlaceholderView();

        // Sinkronkan URL Hash pada pemuatan awal
        syncUrlHash();

        // Dengarkan navigasi browser back/forward melalui hashchange
        window.addEventListener('hashchange', () => {{
            const h = (window.location.hash || '').toLowerCase();
            const newLevel = h.includes('d3') ? 'd3' : 's1';
            const newSubset = (h.includes('60') || h.includes('tanpa') || h.includes('established')) ? 'established' : 'all';

            if (newLevel !== currentLevel) {{
                const targetTab = document.querySelector(`.level-tab[data-level="${{newLevel}}"]`);
                if (targetTab) targetTab.click();
            }} else if (newLevel === 's1' && newSubset !== currentS1Subset) {{
                const targetSub = document.querySelector(`.subset-tab[data-subset="${{newSubset}}"]`);
                if (targetSub) targetSub.click();
            }}
        }});
    </script>
</body>
</html>
"""

    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Berhasil menghasilkan dashboard interaktif multi-jenjang di: {html_output_path}")

if __name__ == "__main__":
    generate_interactive_html()
