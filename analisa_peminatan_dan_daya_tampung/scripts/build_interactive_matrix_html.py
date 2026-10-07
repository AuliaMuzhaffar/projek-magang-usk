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
            kuadran_desc = "Peminat Sangat Tinggi, Namun Terjadi Kebocoran Daftar Ulang"
            color = "#D97706" # Amber
            rekomendasi = (
                "Investigasi mendalam penyebab kebocoran registrasi ulang (yield loss). Evaluasi penyesuaian "
                "kelompok UKT, tinjau waktu pengumuman, dan perketat komitmen calon mahasiswa pada jalur mandiri/SNBT."
            )
        else:
            kuadran = "IV"
            kuadran_title = "KUADRAN IV: PERLU REVITALISASI"
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

        # Seluruh 11 D3 berada di Kuadran IV secara formal (<80% & >=4.0x)
        # Pengelompokan Berdasarkan 3 Tier Kelayakan Vokasi:
        if fill_rate >= 60.0:
            tier = 1
            tier_title = "TIER 1: STANDOUT VOKASI"
            tier_desc = "Bintang Vokasi: Fill Rate Tinggi (≥ 60%) & Peminat Membludak"
            color = "#059669" # Emerald Green
            kuadran_title = "KUADRAN IV (TIER 1: STANDOUT VOKASI)"
            kuadran_desc = "Peminat Tertinggi Vokasi & Keterisian Kuota Stabil (≥ 60%)"
            rekomendasi = (
                "Prioritas #1 untuk segera dikonversi dan dinaikkan statusnya menjadi Sarjana Terapan "
                "(D4 Rekayasa Perangkat Lunak / TI). Animo pasar sangat tinggi (1.100 mhs/thn) dengan daya serap terbaik di vokasi USK (66,6%)."
            )
        elif fill_rate >= 45.0:
            tier = 2
            tier_title = "TIER 2: RENTAN KONVERSI"
            tier_desc = "Keterisian Moderat (45%–55%), Di Bawah Standar Sehat 80%"
            color = "#D97706" # Amber
            kuadran_title = "KUADRAN IV (TIER 2: RENTAN KONVERSI)"
            kuadran_desc = "Peminat Cukup Tinggi (200–760 org), Namun Daftar Ulang Macet"
            rekomendasi = (
                "Kandidat konversi ke Sarjana Terapan (D4) dengan restrukturisasi kurikulum berbasis kemitraan industri "
                "(teaching factory). Perkuat skema ikatan kerja agar pendaftar tidak gugur massal saat tahap daftar ulang."
            )
        else:
            tier = 3
            tier_title = "TIER 3: DEFISIT AKUT"
            tier_desc = "Di Bawah Batas Kritis Kelayakan Operasional (< 50%)"
            color = "#DC2626" # Crimson Red
            kuadran_title = "KUADRAN IV (TIER 3: DEFISIT AKUT)"
            kuadran_desc = "Kritis: Tingkat Keterisian Jebol (< 45%) & Bangku Kosong Masif"
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
            "kuadran": "IV",
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
            padding: 14px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 50;
            box-shadow: var(--shadow-sm);
            flex-wrap: wrap;
            gap: 16px;
        }}

        .brand-area {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .usk-header-logo {{
            height: 48px;
            width: auto;
            max-width: 140px;
            object-fit: contain;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.05));
        }}

        .brand-divider {{
            width: 1px;
            height: 38px;
            background: var(--border-subtle);
        }}

        .brand-titles h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: var(--text-main);
            line-height: 1.25;
            letter-spacing: -0.3px;
        }}

        .brand-titles p {{
            font-size: 12px;
            color: var(--text-muted);
            margin-top: 2px;
            font-weight: 500;
        }}

        /* LEVEL SWITCHER (Segmented Control Tabs) */
        .level-switcher {{
            display: inline-flex;
            align-items: center;
            background: #F1F5F9;
            padding: 4px;
            border-radius: 28px;
            border: 1px solid var(--border-subtle);
            gap: 4px;
        }}

        .level-tab {{
            border: none;
            background: transparent;
            padding: 8px 18px;
            border-radius: 22px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 13px;
            font-weight: 700;
            color: #475569;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
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

        .header-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 8px 14px;
            font-size: 12.5px;
            font-weight: 600;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            text-decoration: none;
            border: 1px solid transparent;
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
            padding: 9px 14px 9px 38px;
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

        .dot-label {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 9.5px;
            font-weight: 700;
            pointer-events: none;
            transition: opacity 0.2s ease;
        }}

        /* Floating Tooltip */
        #interactive-tooltip {{
            position: absolute;
            display: none;
            pointer-events: none;
            z-index: 100;
            background: rgba(15, 23, 42, 0.94);
            backdrop-filter: blur(8px);
            color: #FFFFFF;
            padding: 12px 16px;
            border-radius: 12px;
            box-shadow: var(--shadow-lg);
            width: 260px;
            transform: translate(-50%, -100%);
            margin-top: -12px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }}

        #interactive-tooltip::after {{
            content: '';
            position: absolute;
            bottom: -6px;
            left: 50%;
            transform: translateX(-50%);
            border-width: 6px 6px 0;
            border-style: solid;
            border-color: rgba(15, 23, 42, 0.94) transparent;
            display: block;
            width: 0;
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

        .ins-tag-row {{
            display: flex;
            gap: 8px;
            align-items: center;
            margin-bottom: 8px;
            flex-wrap: wrap;
        }}

        .ins-fakultas-tag {{
            font-size: 11px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 6px;
            background: #F1F5F9;
            color: #334155;
        }}

        .ins-kuadran-tag {{
            font-size: 11px;
            font-weight: 700;
            padding: 3px 10px;
            border-radius: 20px;
            color: #FFFFFF;
        }}

        .ins-title {{
            font-family: 'Outfit', sans-serif;
            font-size: 20px;
            font-weight: 800;
            line-height: 1.25;
            color: var(--text-main);
            margin-bottom: 4px;
        }}

        .ins-sub {{
            font-size: 12px;
            color: var(--text-muted);
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
                <h1 id="header-main-title">PETA PORTOFOLIO STRATEGIS 66 PROGRAM STUDI S1</h1>
                <p id="header-sub-title">Direktorat Akademik & Perencanaan • Universitas Syiah Kuala (2022–2026)</p>
            </div>
        </div>

        <!-- LEVEL SWITCHER SEGMENTED TABS -->
        <div class="level-switcher" id="level-switcher">
            <button class="level-tab active" data-level="s1" id="tab-s1">
                🎓 S1 Sarjana <span class="tab-badge">66 Prodi</span>
            </button>
            <button class="level-tab" data-level="d3" id="tab-d3">
                🛠️ D3 Vokasi <span class="tab-badge">11 Prodi</span>
            </button>
        </div>

        <div class="header-actions">
            <button class="btn btn-outline" id="btn-toggle-labels" title="Tampilkan atau sembunyikan semua label prodi di kanvas">
                🏷️ Toggle Semua Label
            </button>
            <button class="btn btn-outline" id="btn-reset-filters" title="Kembalikan semua filter ke kondisi awal">
                🔄 Reset Tampilan
            </button>
            <button class="btn btn-primary" onclick="window.print()" title="Cetak laporan / simpan PDF">
                🖨️ Cetak / PDF
            </button>
        </div>
    </header>

    <!-- KPI SUMMARY CARDS (Clickable Filters) -->
    <section class="kpi-ribbon" id="kpi-ribbon-container">
        <!-- Rendered dynamically via JavaScript -->
    </section>

    <!-- SEARCH & FACULTY FILTERS -->
    <section class="controls-strip">
        <div class="search-box">
            <span class="search-icon">🔍</span>
            <input type="text" id="prodi-search" placeholder="Cari nama prodi atau fakultas (cth: Farmasi, FT, Informatika)...">
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
                    <h2 id="chart-sub-heading">Matriks 4 Kuadran Interaktif (Keketatan Seleksi vs Tingkat Keterisian Kuota)</h2>
                    <p id="chart-sub-guide">Arahkan kursor ke titik prodi untuk ringkasan instan • Klik titik untuk membuka analisis detail</p>
                </div>
                <div class="canvas-toolbar">
                    <span id="match-counter" style="font-size:12px; font-weight:600; color:var(--text-muted); margin-right:8px;">Menampilkan: 66/66 Prodi</span>
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
        </div>

        <!-- RIGHT: EXECUTIVE INSPECTOR DRAWER -->
        <aside class="inspector-panel" id="inspector-panel">
            <div class="inspector-placeholder" id="ins-placeholder">
                <img src="{usk_logo_b64}" alt="Logo USK" class="ins-placeholder-logo" />
                <h3>Pilih Program Studi</h3>
                <p>Klik salah satu lingkaran titik pada kanvas atau gunakan kotak pencarian untuk melihat rincian evaluasi 5 tahun, profil kebocoran kuota, dan rekomendasi kebijakan prodi.</p>
            </div>

            <div class="inspector-content" id="ins-content">
                <div class="ins-header">
                    <div class="ins-tag-row">
                        <span class="ins-fakultas-tag" id="ins-fak">FAKULTAS</span>
                        <span class="ins-kuadran-tag" id="ins-quad-tag">KUADRAN I</span>
                    </div>
                    <div class="ins-title" id="ins-name">Nama Program Studi</div>
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
        let currentLevel = "s1"; // "s1" or "d3"
        let currentFaculty = "ALL";
        let currentFilterCard = "ALL"; // Quadrant in S1 or Tier in D3
        let searchQuery = "";
        let showAllLabels = false;
        let selectedProdiId = null;

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
                const cardsConfig = [
                    {{
                        id: 'I',
                        label: 'Kuadran I: Unggulan',
                        icon: '🏆',
                        val: '28',
                        sub: 'Prodi (42,4%)',
                        note: 'Peminat Tinggi & Kuota Terpenuhi',
                        class: 'c-emerald'
                    }},
                    {{
                        id: 'II',
                        label: 'Kuadran II: Stabil',
                        icon: '⚖️',
                        val: '4',
                        sub: 'Prodi (6,1%)',
                        note: 'Seleksi Moderat, Daya Serap Aman',
                        class: 'c-blue'
                    }},
                    {{
                        id: 'III',
                        label: 'Kuadran III: Belum Optimal',
                        icon: '⚠️',
                        val: '8',
                        sub: 'Prodi (12,1%)',
                        note: 'Peminat Tinggi tapi Bocor Daftar Ulang',
                        class: 'c-amber'
                    }},
                    {{
                        id: 'IV',
                        label: 'Kuadran IV: Revitalisasi',
                        icon: '🚨',
                        val: '26',
                        sub: 'Prodi (39,4%)',
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
                // D3 Cards (Anomali + 3 Tier Kelayakan)
                const cardsConfig = [
                    {{
                        id: 'ALL_D3',
                        label: 'Anomali Vokasi (100%)',
                        icon: '🚨',
                        val: '11',
                        sub: 'Prodi Kuadran IV',
                        note: 'Rata Keketatan 9,5x | Fill Rate 44,4%',
                        class: 'c-amber'
                    }},
                    {{
                        id: 'TIER_1',
                        label: 'Tier 1: Standout Vokasi',
                        icon: '⭐',
                        val: '1',
                        sub: 'Prodi (9,1%)',
                        note: 'FR ≥ 60% • D3 Manajemen Informatika',
                        class: 'c-emerald'
                    }},
                    {{
                        id: 'TIER_2',
                        label: 'Tier 2: Rentan Konversi',
                        icon: '🔄',
                        val: '5',
                        sub: 'Prodi (45,5%)',
                        note: 'FR 45%–55% • Konversi Selektif D4',
                        class: 'c-amber'
                    }},
                    {{
                        id: 'TIER_3',
                        label: 'Tier 3: Krisis Defisit Akut',
                        icon: '📉',
                        val: '5',
                        sub: 'Prodi (45,5%)',
                        note: 'FR < 45% • Rasionalisasi Kuota 40-50%',
                        class: 'c-crimson'
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

            const currentList = DATA_BY_LEVEL[currentLevel];
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
        }}

        const fak_abbr_map_client = {json.dumps(fak_abbr_map)};

        // Filter Evaluation
        function isProdiVisible(d) {{
            // Faculty filter
            if (currentFaculty !== "ALL" && d.fakultas !== currentFaculty) return false;

            // Card Filter
            if (currentLevel === 's1') {{
                if (currentFilterCard !== "ALL" && d.kuadran !== currentFilterCard) return false;
            }} else {{
                if (currentFilterCard === 'TIER_1' && d.tier !== 1) return false;
                if (currentFilterCard === 'TIER_2' && d.tier !== 2) return false;
                if (currentFilterCard === 'TIER_3' && d.tier !== 3) return false;
            }}

            // Search query
            if (searchQuery.trim() !== "") {{
                const q = searchQuery.toLowerCase();
                const matchName = d.nama.toLowerCase().includes(q);
                const matchFak = d.fakultas.toLowerCase().includes(q) || (d.fakultas_abbr && d.fakultas_abbr.toLowerCase().includes(q));
                if (!matchName && !matchFak) return false;
            }}
            return true;
        }}

        // Render Canvas
        function renderChart() {{
            const svg = document.getElementById('matrix-svg');
            svg.innerHTML = '';

            const currentList = DATA_BY_LEVEL[currentLevel];
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

                // Watermark Quadrant Titles
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + 22, 'end', '13', '800', '#059669', 0.85, 'KUADRAN I: UNGGULAN (28 Prodi)'));
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + 22, 'start', '13', '800', '#2563EB', 0.85, 'KUADRAN II: STABIL (4 Prodi)'));
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + PLOT_H - 14, 'end', '12.5', '800', '#D97706', 0.85, 'KUADRAN III: BELUM OPTIMAL (8 Prodi)'));
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + PLOT_H - 14, 'start', '13', '800', '#E11D48', 0.85, 'KUADRAN IV: REVITALISASI (26 Prodi)'));

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
                svg.appendChild(createPillBadge(xThreshold, PLOT_Y + PLOT_H - 16, 190, 22, '#475569', '#94A3B8', '#FFFFFF', '▲ AMBANG KEKETATAN: 4,0 : 1'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 130, yThreshold80, 240, 22, '#475569', '#94A3B8', '#FFFFFF', 'STANDAR SEHAT: 80% KETERISIAN'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 145, yThreshold50, 270, 22, '#DC2626', '#F87171', '#FFFFFF', '⚠ BATAS KRITIS KELAYAKAN: 50%'));

                // Callout Banner: Anomali Struktural Vokasi USK
                const bannerGroup = createSVGElement('g', {{ transform: `translate(${{PLOT_X + PLOT_W / 2 + 50}}, ${{PLOT_Y + 45}})` }});
                const bannerRect = createSVGElement('rect', {{
                    x: -240, y: -26, width: 480, height: 52, rx: 10,
                    fill: '#FFFBEB', stroke: '#F59E0B', 'stroke-width': 1.4, opacity: 0.96
                }});
                const bannerT1 = createText(0, -6, 'middle', '11.5', '800', '#92400E', 1, 'TEMUAN ANOMALI STRUKTURAL VOKASI USK:');
                const bannerT2 = createText(0, 12, 'middle', '11', '700', '#B45309', 1, '100% (11 Prodi D3) Terkonsentrasi di Kuadran IV (Keketatan 5,3x–17,7x, FR < 80%)');
                bannerGroup.appendChild(bannerRect);
                bannerGroup.appendChild(bannerT1);
                bannerGroup.appendChild(bannerT2);
                svg.appendChild(bannerGroup);

                // Watermark Quadrant Titles D3
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + 18, 'end', '11.5', '700', '#94A3B8', 0.70, 'KUADRAN I: UNGGULAN (0 Prodi / 0%)'));
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + 18, 'start', '11.5', '700', '#94A3B8', 0.70, 'KUADRAN II: STABIL (0 Prodi / 0%)'));
                svg.appendChild(createText(PLOT_X + 14, PLOT_Y + PLOT_H - 14, 'start', '11.5', '700', '#94A3B8', 0.70, 'KUADRAN III: KURANG DIMINATI (0 Prodi / 0%)'));
                svg.appendChild(createText(PLOT_X + PLOT_W - 14, PLOT_Y + PLOT_H - 14, 'end', '12', '800', '#B45309', 0.95, 'KUADRAN IV: SELEKTIF TAPI BOCOR (11 Prodi / 100% Vokasi)'));
            }}

            // Axis Titles
            svg.appendChild(createText(PLOT_X + PLOT_W / 2, PLOT_Y + PLOT_H + 42, 'middle', '12.5', '700', '#0F172A', 1, 'Rasio Keketatan Seleksi (Peminat per 1 Kursi Daya Tampung)'));
            const yTitle = createText(-(PLOT_Y + PLOT_H / 2), 18, 'middle', '12.5', '700', '#0F172A', 1, 'Persentase Keterisian Kuota / Fill Rate (%)');
            yTitle.setAttribute('transform', 'rotate(-90)');
            svg.appendChild(yTitle);

            // Render Dots & Labels
            const dotsGroup = createSVGElement('g', {{ id: 'dots-group' }});
            const labelsGroup = createSVGElement('g', {{ id: 'labels-group' }});

            let matchCount = 0;

            currentList.forEach(d => {{
                const visible = isProdiVisible(d);
                if (visible) matchCount++;

                const cx = mapX(d.keketatan);
                const cy = mapY(clampFR(d.fill_rate));

                // Uniform Circle Radius (7.5px) for all data points
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
                circle.addEventListener('mouseleave', onDotLeave);
                circle.addEventListener('click', () => onDotClick(d));

                dotsGroup.appendChild(circle);

                // Labels: HANYA tampil jika tombol Toggle Semua Label aktif ATAU titik tersebut sedang diklik
                const showThisLabel = showAllLabels || (selectedProdiId === d.id);

                if (showThisLabel && visible) {{
                    const labelText = createSVGElement('text', {{
                        x: cx + rRadius + 4,
                        y: cy + 3,
                        class: 'dot-label',
                        fill: '#1E293B'
                    }});
                    // Clean shortened label
                    let shortName = d.nama.replace('PENDIDIKAN ', 'PEND. ').replace('KESEHATAN ', 'KES. ');
                    if (currentLevel === 'd3') {{
                        shortName = 'D3 ' + shortName;
                    }}
                    labelText.textContent = shortName;
                    labelsGroup.appendChild(labelText);
                }}
            }});

            svg.appendChild(dotsGroup);
            svg.appendChild(labelsGroup);

            // Update match counter
            document.getElementById('match-counter').textContent = `Menampilkan: ${{matchCount}}/${{currentList.length}} Prodi`;
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

        // Tooltip interaction
        const tooltip = document.getElementById('interactive-tooltip');
        const svgContainer = document.getElementById('svg-container');

        function onDotHover(e, d) {{
            const circle = e.target;
            circle.setAttribute('r', '11.5');

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

            tooltip.style.display = 'block';

            const rect = svgContainer.getBoundingClientRect();
            const mouseX = e.clientX - rect.left;
            const mouseY = e.clientY - rect.top;

            tooltip.style.left = `${{mouseX}}px`;
            tooltip.style.top = `${{mouseY - 14}}px`;
        }}

        function onDotLeave(e) {{
            const circle = e.target;
            const dId = parseInt(circle.getAttribute('data-id'));
            circle.setAttribute('r', selectedProdiId === dId ? '10.5' : '7.5');
            tooltip.style.display = 'none';
        }}

        function onDotClick(d) {{
            selectedProdiId = d.id;
            renderChart();
            showInspector(d);
        }}

        function showInspector(d) {{
            document.getElementById('ins-placeholder').style.display = 'none';
            const content = document.getElementById('ins-content');
            content.style.display = 'block';

            document.getElementById('ins-fak').textContent = `${{d.fakultas_abbr}} • ${{d.fakultas}} (${{d.jenjang}})`;
            const qTag = document.getElementById('ins-quad-tag');
            qTag.textContent = d.kuadran_title;
            qTag.style.backgroundColor = d.color;

            document.getElementById('ins-name').textContent = (d.jenjang === 'D3' ? 'D3 ' : '') + d.nama;
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
                searchQuery = "";
                document.getElementById('prodi-search').value = "";
                selectedProdiId = null;

                // Update Header and Subtitles
                if (currentLevel === 's1') {{
                    document.getElementById('header-main-title').textContent = 'PETA PORTOFOLIO STRATEGIS 66 PROGRAM STUDI S1';
                    document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (Keketatan Seleksi vs Keterisian Kuota S1)';
                    document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi S1: <strong>Keketatan 4,0 : 1</strong> | <strong>Keterisian Sehat 80%</strong>';
                }} else {{
                    document.getElementById('header-main-title').textContent = 'PETA PORTOFOLIO STRATEGIS 11 PROGRAM STUDI DIPLOMA 3 VOKASI';
                    document.getElementById('chart-sub-heading').textContent = 'Matriks Anomali Vokasi USK (Keketatan Seleksi vs Keterisian Kuota D3)';
                    document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi D3: <strong>Keketatan 4,0 : 1</strong> | <strong>Standar Sehat 80%</strong> | <strong>Batas Kritis 50%</strong>';
                }}

                renderKPIRibbon();
                renderFacultyFilters();
                renderChart();

                // Pastikan panel inspector dan titik kembali bersih saat ganti level
                selectedProdiId = null;
                document.getElementById('ins-content').style.display = 'none';
                document.getElementById('ins-placeholder').style.display = 'block';
            }});
        }});

        // Search Input
        document.getElementById('prodi-search').addEventListener('input', (e) => {{
            searchQuery = e.target.value;
            renderChart();
        }});

        // Toggle Labels
        document.getElementById('btn-toggle-labels').addEventListener('click', (e) => {{
            showAllLabels = !showAllLabels;
            e.target.classList.toggle('active', showAllLabels);
            renderChart();
        }});

        // Reset Filters Button
        document.getElementById('btn-reset-filters').addEventListener('click', () => {{
            currentFaculty = "ALL";
            currentFilterCard = "ALL";
            searchQuery = "";
            showAllLabels = false;
            selectedProdiId = null;

            document.getElementById('prodi-search').value = "";
            document.getElementById('btn-toggle-labels').classList.remove('active');

            document.getElementById('ins-content').style.display = 'none';
            document.getElementById('ins-placeholder').style.display = 'block';

            renderKPIRibbon();
            renderFacultyFilters();
            renderChart();
        }});

        // Initial Load
        renderKPIRibbon();
        renderFacultyFilters();
        renderChart();

        // Initial Load bersih (tanpa auto-select, kanvas bebas dari label mengambang)
        selectedProdiId = null;
        document.getElementById('ins-content').style.display = 'none';
        document.getElementById('ins-placeholder').style.display = 'block';
    </script>
</body>
</html>
"""

    with open(html_output_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Berhasil menghasilkan dashboard interaktif multi-jenjang di: {html_output_path}")

if __name__ == "__main__":
    generate_interactive_html()
