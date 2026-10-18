import os
import sys
import json
import base64
import sys, os
libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "libs"))
if os.path.exists(libs_dir) and libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import pandas as pd
import numpy as np

# Impor konfigurasi sentral (Single Source of Truth)
sys.path.insert(0, os.path.dirname(__file__))
from core_data import (
    BASE_DIR, MASTER_EXCEL_PATH, RAW_EXCEL_PATH, DASHBOARD_DIR, INTERACTIVE_HTML_PATH,
    KEKETATAN_BENCHMARK, FILLRATE_BENCHMARK, FAKULTAS_ABBR, PRODI_HTML_SHORT_NAMES
)

def generate_interactive_html():
    repo_dir = BASE_DIR
    excel_path = MASTER_EXCEL_PATH
    raw_path = RAW_EXCEL_PATH
    html_output_dir = DASHBOARD_DIR
    os.makedirs(html_output_dir, exist_ok=True)
    html_output_path = INTERACTIVE_HTML_PATH

    if not os.path.exists(excel_path):
        print(f"File {excel_path} tidak ditemukan!")
        return

    print("Membaca data Excel Master_Semua_Prodi, S1 Kampus Utama, dan Diploma 3 Vokasi...")
    df_all = pd.read_excel(excel_path, sheet_name="Master_Semua_Prodi")
    df_s1 = pd.read_excel(excel_path, sheet_name="S1_Kampus_Utama")
    df_d3 = pd.read_excel(excel_path, sheet_name="Diploma_3_Vokasi")

    # Pemetaan Kode Prodi 7 Digit Resmi dari raw_path
    prodi_to_code = {}
    if os.path.exists(raw_path):
        try:
            df_raw = pd.read_excel(raw_path, sheet_name="Rekapitulasi Data", header=None)
            for _, rr in df_raw.iloc[4:].iterrows():
                kode_val = rr.iloc[1]
                nama_val = rr.iloc[2]
                if pd.notna(nama_val):
                    n_str = str(nama_val).strip().upper()
                    if pd.notna(kode_val):
                        try:
                            k_str = str(int(float(kode_val))).zfill(7)
                        except Exception:
                            k_str = str(kode_val).strip()
                        prodi_to_code[n_str] = k_str
        except Exception:
            pass
    prodi_to_code["TEKNIK PERMINYAKAN"] = "0411601"
    prodi_to_code["HUBUNGAN INTERNASIONAL"] = "0910101"

    def resolve_prodi_code(nama_str):
        n_up = nama_str.strip().upper()
        c = prodi_to_code.get(n_up)
        if not c:
            for k, v in prodi_to_code.items():
                if n_up in k or k in n_up:
                    c = v
                    break
        return c or "-"

    fak_abbr_map = FAKULTAS_ABBR

    # ----------------------------------------------------
    # 1. PROCESS S1 DATA (66 Program Studi)
    # ----------------------------------------------------
    s1_data = []
    for idx, r in df_s1.iterrows():
        p_name = str(r['Nama Program Studi']).strip()
        fak = str(r['Fakultas']).strip()
        fak_abbr = fak_abbr_map.get(fak, fak)
        kode_prodi = resolve_prodi_code(p_name)

        keketatan = round(float(r['Rata Keketatan 5-Thn']), 2)
        raw_fill_rate = round(float(r['Rata Fill Rate 5-Thn (%)']), 1)
        fill_rate = min(raw_fill_rate, 100.0) # Cap at 100.0%

        peminat_5thn = round(float(r['Rata Peminat 5-Thn']), 1)
        dt_5thn = round(float(r['Rata DT 5-Thn']), 1)
        du_5thn = round(float(r['Rata DU 5-Thn']), 1)
        sisa_kursi_5thn = max(0.0, round(dt_5thn - du_5thn, 1)) # No negative deficit
        tren_resmi = str(r.get('Klasifikasi Tren Resmi', 'Tren Stabil')).strip()
        klaster = str(r.get('Klaster Analisis', 'Reguler')).strip()

        # Klasifikasi Kuadran S1 (Ambang Standar dari core_data.py: 4.0x & 80%)
        if keketatan >= KEKETATAN_BENCHMARK and fill_rate >= FILLRATE_BENCHMARK:
            kuadran = "I"
            kuadran_title = "KUADRAN I: UNGGULAN"
            kuadran_desc = "Peminat Tinggi & Daya Serap Kuota Penuh (Prima)"
            color = "#059669" # Emerald Green
            rekomendasi = (
                "Pertahankan standar kualitas seleksi tinggi. Alokasi daya tampung dapat dinaikkan selektif "
                "(5–10%) jika kapasitas laboratorium dan rasio dosen mencukupi, mengingat animo pasar yang sangat kuat."
            )
        elif keketatan < KEKETATAN_BENCHMARK and fill_rate >= FILLRATE_BENCHMARK:
            kuadran = "II"
            kuadran_title = "KUADRAN II: STABIL"
            kuadran_desc = "Kompetisi Moderat, Namun Kuota Terserap Optimal"
            color = "#2563EB" # Royal Blue
            rekomendasi = (
                "Pertahankan kuota tetap stabil. Tingkatkan branding dan promosi ke sekolah mitra di luar Aceh "
                "untuk mendongkrak rasio keketatan seleksi menuju ambang kompetitif (>= 4,0 : 1)."
            )
        elif keketatan >= KEKETATAN_BENCHMARK and fill_rate < FILLRATE_BENCHMARK:
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
        tot_dt_5 = 0
        tot_lu_5 = 0
        tot_du_5 = 0
        for yr in [2022, 2023, 2024, 2025, 2026]:
            try:
                pem_y = int(r[f'Peminat {yr}']) if pd.notna(r.get(f'Peminat {yr}')) else 0
                dt_y = int(r[f'Daya Tampung {yr}']) if pd.notna(r.get(f'Daya Tampung {yr}')) else 0
                lu_y = int(r[f'Lulus Seleksi {yr}']) if pd.notna(r.get(f'Lulus Seleksi {yr}')) else 0
                du_y = int(r[f'Daftar Ulang {yr}']) if pd.notna(r.get(f'Daftar Ulang {yr}')) else 0
                raw_fr_y = round(float(r[f'Fill Rate {yr} (%)']), 1) if pd.notna(r.get(f'Fill Rate {yr} (%)')) else 0.0
                fr_y = min(raw_fr_y, 100.0) # Capped at 100%
                yr_y = round(float(r[f'Yield Rate {yr} (%)']), 1) if pd.notna(r.get(f'Yield Rate {yr} (%)')) else 0.0
                kek_y = round(float(r[f'Keketatan {yr}']), 2) if pd.notna(r.get(f'Keketatan {yr}')) else 0.0
                sisa_y = dt_y - du_y
                batal_y = lu_y - du_y
                tot_dt_5 += dt_y
                tot_lu_5 += lu_y
                tot_du_5 += du_y
                history.append({
                    "tahun": yr,
                    "peminat": pem_y,
                    "dt": dt_y,
                    "lulus": lu_y,
                    "du": du_y,
                    "sisa": sisa_y,
                    "batal": batal_y,
                    "fill_rate": fr_y,
                    "yield_rate": yr_y,
                    "keketatan": kek_y
                })
            except Exception:
                pass

        s1_data.append({
            "id": idx + 1,
            "kode": kode_prodi,
            "jenjang": "S1",
            "nama": p_name,
            "fakultas": fak,
            "fakultas_abbr": fak_abbr,
            "kuadran": kuadran,
            "kuadran_title": kuadran_title,
            "kuadran_desc": kuadran_desc,
            "color": color,
            "rekomendasi": rekomendasi,
            "keketatan": keketatan,
            "fill_rate": fill_rate,
            "peminat_5thn": peminat_5thn,
            "dt_5thn": dt_5thn,
            "du_5thn": du_5thn,
            "sisa_5thn": sisa_kursi_5thn,
            "tot_dt": tot_dt_5,
            "tot_lulus": tot_lu_5,
            "tot_du": tot_du_5,
            "tot_sisa": tot_dt_5 - tot_du_5,
            "tot_batal": tot_lu_5 - tot_du_5,
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
        kode_prodi = resolve_prodi_code(p_name)

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
        tot_dt_5 = 0
        tot_lu_5 = 0
        tot_du_5 = 0
        for yr in [2022, 2023, 2024, 2025, 2026]:
            try:
                pem_y = int(r[f'Peminat {yr}']) if pd.notna(r.get(f'Peminat {yr}')) else 0
                dt_y = int(r[f'Daya Tampung {yr}']) if pd.notna(r.get(f'Daya Tampung {yr}')) else 0
                lu_y = int(r[f'Lulus Seleksi {yr}']) if pd.notna(r.get(f'Lulus Seleksi {yr}')) else 0
                du_y = int(r[f'Daftar Ulang {yr}']) if pd.notna(r.get(f'Daftar Ulang {yr}')) else 0
                raw_fr_y = round(float(r[f'Fill Rate {yr} (%)']), 1) if pd.notna(r.get(f'Fill Rate {yr} (%)')) else 0.0
                fr_y = min(raw_fr_y, 100.0)
                yr_y = round(float(r[f'Yield Rate {yr} (%)']), 1) if pd.notna(r.get(f'Yield Rate {yr} (%)')) else 0.0
                kek_y = round(float(r[f'Keketatan {yr}']), 2) if pd.notna(r.get(f'Keketatan {yr}')) else 0.0
                sisa_y = dt_y - du_y
                batal_y = lu_y - du_y
                tot_dt_5 += dt_y
                tot_lu_5 += lu_y
                tot_du_5 += du_y
                history.append({
                    "tahun": yr,
                    "peminat": pem_y,
                    "dt": dt_y,
                    "lulus": lu_y,
                    "du": du_y,
                    "sisa": sisa_y,
                    "batal": batal_y,
                    "fill_rate": fr_y,
                    "yield_rate": yr_y,
                    "keketatan": kek_y
                })
            except Exception:
                pass

        d3_data.append({
            "id": 100 + idx + 1,
            "kode": kode_prodi,
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
            "rekomendasi": rekomendasi,
            "keketatan": keketatan,
            "fill_rate": fill_rate,
            "peminat_5thn": peminat_5thn,
            "dt_5thn": dt_5thn,
            "du_5thn": du_5thn,
            "sisa_5thn": sisa_kursi_5thn,
            "tot_dt": tot_dt_5,
            "tot_lulus": tot_lu_5,
            "tot_du": tot_du_5,
            "tot_sisa": tot_dt_5 - tot_du_5,
            "tot_batal": tot_lu_5 - tot_du_5,
            "tren_resmi": tren_resmi,
            "klaster": klaster,
            "history": history
        })

    # ----------------------------------------------------
    # 3. PROCESS ALL 81 PRODI FROM MASTER_SEMUA_PRODI
    # ----------------------------------------------------
    all_prodi_data = []
    for idx, r in df_all.iterrows():
        no_val = int(r['No']) if pd.notna(r.get('No')) else (idx + 1)
        p_name = str(r['Nama Program Studi']).strip()
        fak = str(r['Fakultas']).strip()
        fak_abbr = fak_abbr_map.get(fak, fak)
        jenjang = str(r.get('Jenjang', 'S1')).strip()
        klaster = str(r.get('Klaster Analisis', 'S1 Kampus Utama')).strip()
        kode_prodi = resolve_prodi_code(p_name)

        keketatan = round(float(r['Rata Keketatan 5-Thn']), 2)
        raw_fill_rate = round(float(r['Rata Fill Rate 5-Thn (%)']), 1)
        fill_rate = min(raw_fill_rate, 100.0)
        peminat_5thn = round(float(r['Rata Peminat 5-Thn']), 1)
        dt_5thn = round(float(r['Rata DT 5-Thn']), 1)
        du_5thn = round(float(r['Rata DU 5-Thn']), 1)
        sisa_kursi_5thn = max(0.0, round(dt_5thn - du_5thn, 1))
        tren_resmi = str(r.get('Klasifikasi Tren Resmi', 'Tren Stabil')).strip()
        is_prodi_baru = bool(tren_resmi == "Data Terbatas (Prodi Baru)" and klaster == "S1 Kampus Utama")

        if keketatan >= KEKETATAN_BENCHMARK and fill_rate >= FILLRATE_BENCHMARK:
            kuadran = "I"
            kuadran_title = "KUADRAN I: UNGGULAN"
            kuadran_desc = "Peminat Tinggi & Daya Serap Kuota Penuh (Prima)"
            color = "#059669"
            rekomendasi = (
                "Pertahankan standar kualitas seleksi tinggi. Alokasi daya tampung dapat dinaikkan selektif "
                "(5–10%) jika kapasitas laboratorium dan rasio dosen mencukupi."
            )
        elif keketatan < KEKETATAN_BENCHMARK and fill_rate >= FILLRATE_BENCHMARK:
            kuadran = "II"
            kuadran_title = "KUADRAN II: STABIL"
            kuadran_desc = "Kompetisi Moderat, Namun Kuota Terserap Optimal"
            color = "#2563EB"
            rekomendasi = (
                "Pertahankan kuota tetap stabil. Tingkatkan promosi untuk mendongkrak rasio keketatan seleksi "
                "menuju ambang kompetitif (>= 4,0 : 1)."
            )
        elif keketatan >= KEKETATAN_BENCHMARK and fill_rate < FILLRATE_BENCHMARK:
            kuadran = "III"
            kuadran_title = "KUADRAN III: BELUM OPTIMAL"
            kuadran_desc = "Peminat Sangat Tinggi, Namun Daftar Ulang Belum Optimal"
            color = "#D97706"
            rekomendasi = (
                "Investigasi mendalam penyebab tingginya calon mahasiswa lulus yang batal daftar ulang (yield loss). "
                "Tinjau tarif UKT/IPI dan optimalkan pemanggilan cadangan."
            )
        else:
            kuadran = "IV"
            kuadran_title = "KUADRAN IV: PERLU DITINGKATKAN"
            kuadran_desc = "Peminat Rendah & Kuota Kerap Tidak Terisi Penuh"
            color = "#E11D48"
            rekomendasi = (
                "Prioritas rasionalisasi daya tampung (downsizing kuota 15–30%) untuk menekan akumulasi kursi kosong, "
                "disertai penyegaran kurikulum berbasis kebutuhan pasar."
            )

        history = []
        tot_pem_5 = 0
        tot_dt_5 = 0
        tot_lu_5 = 0
        tot_du_5 = 0
        for yr in [2022, 2023, 2024, 2025, 2026]:
            pem_y = int(r[f'Peminat {yr}']) if pd.notna(r.get(f'Peminat {yr}')) else 0
            dt_y = int(r[f'Daya Tampung {yr}']) if pd.notna(r.get(f'Daya Tampung {yr}')) else 0
            lu_y = int(r[f'Lulus Seleksi {yr}']) if pd.notna(r.get(f'Lulus Seleksi {yr}')) else 0
            du_y = int(r[f'Daftar Ulang {yr}']) if pd.notna(r.get(f'Daftar Ulang {yr}')) else 0
            raw_fr_y = round(float(r[f'Fill Rate {yr} (%)']), 1) if pd.notna(r.get(f'Fill Rate {yr} (%)')) else 0.0
            fr_y = min(raw_fr_y, 100.0)
            yr_y = round(float(r[f'Yield Rate {yr} (%)']), 1) if pd.notna(r.get(f'Yield Rate {yr} (%)')) else 0.0
            kek_y = round(float(r[f'Keketatan {yr}']), 2) if pd.notna(r.get(f'Keketatan {yr}')) else 0.0
            sisa_y = dt_y - du_y
            batal_y = lu_y - du_y
            tot_pem_5 += pem_y
            tot_dt_5 += dt_y
            tot_lu_5 += lu_y
            tot_du_5 += du_y
            history.append({
                "tahun": yr,
                "peminat": pem_y,
                "dt": dt_y,
                "lulus": lu_y,
                "du": du_y,
                "sisa": sisa_y,
                "batal": batal_y,
                "fill_rate": fr_y,
                "yield_rate": yr_y,
                "keketatan": kek_y
            })

        tot_sisa_5 = tot_dt_5 - tot_du_5
        tot_batal_5 = tot_lu_5 - tot_du_5
        pct_sisa_5 = round((tot_sisa_5 / tot_dt_5 * 100.0), 1) if tot_dt_5 > 0 else 0.0
        pct_batal_5 = round((tot_batal_5 / tot_lu_5 * 100.0), 1) if tot_lu_5 > 0 else 0.0
        fill_5 = round((tot_du_5 / tot_dt_5 * 100.0), 1) if tot_dt_5 > 0 else 0.0
        yield_5 = round((tot_du_5 / tot_lu_5 * 100.0), 1) if tot_lu_5 > 0 else 0.0

        all_prodi_data.append({
            "id": 200 + no_val,
            "no": no_val,
            "kode": kode_prodi,
            "jenjang": jenjang,
            "klaster": klaster,
            "nama": p_name,
            "fakultas": fak,
            "fakultas_abbr": fak_abbr,
            "kuadran": kuadran,
            "kuadran_title": kuadran_title,
            "kuadran_desc": kuadran_desc,
            "color": color,
            "rekomendasi": rekomendasi,
            "keketatan": keketatan,
            "fill_rate": fill_rate,
            "peminat_5thn": peminat_5thn,
            "dt_5thn": dt_5thn,
            "du_5thn": du_5thn,
            "sisa_5thn": sisa_kursi_5thn,
            "tot_peminat": tot_pem_5,
            "tot_dt": tot_dt_5,
            "tot_lulus": tot_lu_5,
            "tot_du": tot_du_5,
            "tot_sisa": tot_sisa_5,
            "tot_batal": tot_batal_5,
            "pct_sisa": pct_sisa_5,
            "pct_batal": pct_batal_5,
            "fill_5thn": min(fill_5, 100.0),
            "yield_5thn": min(yield_5, 100.0),
            "tren_resmi": tren_resmi,
            "is_prodi_baru": is_prodi_baru,
            "history": history
        })

    # Read and encode USK logo
    logo_path = os.path.join(repo_dir, "assets", "logos", "usk-logo.png")
    usk_logo_b64 = ""
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            b64_str = base64.b64encode(f.read()).decode("utf-8")
            usk_logo_b64 = f"data:image/png;base64,{b64_str}"

    print(f"Total Semua Prodi: {len(all_prodi_data)} | S1: {len(s1_data)} | D3: {len(d3_data)}.")
    dataset_payload = {
        "s1": s1_data,
        "d3": d3_data,
        "all": all_prodi_data
    }
    json_data = json.dumps(dataset_payload, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Peta Portofolio Program Studi USK (2022–2026) — Dashboard Interaktif Eksekutif</title>
    <link rel="icon" type="image/png" id="usk-favicon" href="">
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

        /* View Switcher: Segmented Control (Apple / Tailwind style) */
        .view-mode-switcher {{
            display: inline-flex;
            align-items: center;
            background: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 28px;
            padding: 3.5px;
            gap: 4px;
            box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.04);
        }}
        .view-mode-btn {{
            background: transparent;
            color: #475569;
            border: 1px solid transparent;
            padding: 6px 14px;
            border-radius: 22px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            display: inline-flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }}
        .view-mode-btn:hover {{
            color: #0F172A;
            background: rgba(255, 255, 255, 0.7);
        }}
        .view-mode-btn.active {{
            background: #FFFFFF;
            color: #0F172A;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.12), 0 1px 2px rgba(15, 23, 42, 0.08);
            border: 1px solid rgba(203, 213, 225, 0.8);
        }}
        .view-mode-btn .vm-badge {{
            background: #E2E8F0;
            color: #475569;
            padding: 2px 7px;
            border-radius: 12px;
            font-size: 10.5px;
            font-weight: 800;
            transition: all 0.2s ease;
        }}
        .view-mode-btn.active .vm-badge {{
            background: #EFF6FF;
            color: #1D4ED8;
        }}
        .view-mode-btn:hover .vm-badge {{
            background: #CBD5E1;
            color: #0F172A;
        }}

        /* Trend Evaluation View Container */
        #trend-view-wrapper {{
            display: none;
            padding: 18px 28px 32px 28px;
            flex-direction: column;
            gap: 18px;
        }}
        .trend-macro-grid {{
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 14px;
        }}
        .trend-kpi-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 14px 16px;
            box-shadow: var(--shadow-sm);
            border-left: 4.5px solid #0F172A;
        }}
        .trend-kpi-card.tk-blue {{ border-left-color: #2563EB; }}
        .trend-kpi-card.tk-emerald {{ border-left-color: #059669; }}
        .trend-kpi-card.tk-rose {{ border-left-color: #E11D48; background: linear-gradient(180deg, #FFF1F2 0%, #FFFFFF 60%); }}
        .trend-kpi-card.tk-amber {{ border-left-color: #D97706; background: linear-gradient(180deg, #FFFBEB 0%, #FFFFFF 60%); }}
        .tk-title {{
            font-size: 11px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            color: var(--text-muted);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .tk-val {{
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            font-weight: 800;
            color: var(--text-main);
            margin-top: 4px;
            display: flex;
            align-items: baseline;
            gap: 8px;
        }}
        .tk-val span.tk-pct {{
            font-size: 13px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 6px;
        }}
        .tk-sub {{
            font-size: 11.5px;
            color: var(--text-muted);
            margin-top: 5px;
            line-height: 1.4;
        }}

        /* Macro Leaky Bucket Panel */
        .macro-leaky-panel {{
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            padding: 18px 20px;
            box-shadow: var(--shadow-sm);
            display: grid;
            grid-template-columns: 1.15fr 1fr;
            gap: 20px;
            align-items: center;
        }}
        .macro-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        .macro-table th {{
            background: #F1F5F9;
            color: #334155;
            font-weight: 700;
            padding: 8px 10px;
            text-align: right;
            border-bottom: 2px solid #CBD5E1;
        }}
        .macro-table th:first-child {{ text-align: left; }}
        .macro-table td {{
            padding: 7px 10px;
            text-align: right;
            border-bottom: 1px solid #E2E8F0;
            font-variant-numeric: tabular-nums;
        }}
        .macro-table td:first-child {{ text-align: left; font-weight: 700; }}
        .macro-table tr.total-row td {{
            background: #0F172A;
            color: #FFFFFF;
            font-weight: 800;
            border-bottom: none;
        }}

        /* Trend Controls & Presets Bar */
        .trend-controls-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            border-radius: 14px;
            padding: 14px 18px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .trend-toolbar-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            align-items: center;
            justify-content: space-between;
        }}
        .preset-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 7px;
            align-items: center;
        }}
        .preset-btn {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            color: #334155;
            padding: 6.5px 12px;
            border-radius: 8px;
            font-size: 11.5px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.15s ease;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }}
        .preset-btn:hover {{
            background: #F1F5F9;
            border-color: #94A3B8;
        }}
        .preset-btn.active {{
            background: #0F172A;
            color: #FFFFFF;
            border-color: #0F172A;
        }}
        .preset-btn.preset-rose.active {{
            background: #E11D48;
            border-color: #E11D48;
            color: #FFFFFF;
        }}
        .preset-btn.preset-amber.active {{
            background: #D97706;
            border-color: #D97706;
            color: #FFFFFF;
        }}
        .trend-select {{
            padding: 6.5px 11px;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            font-family: inherit;
            font-size: 12px;
            font-weight: 600;
            color: #1E293B;
            background: #F8FAFC;
            cursor: pointer;
        }}
        .trend-search-input {{
            padding: 7px 12px;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            font-family: inherit;
            font-size: 12px;
            width: 260px;
        }}

        /* 81 Prodi Sparkline Table */
        .trend-table-card {{
            background: #FFFFFF;
            border: 1px solid var(--border-subtle);
            border-radius: 16px;
            box-shadow: var(--shadow-sm);
            overflow: hidden;
        }}
        .trend-table-scroll {{
            overflow-x: auto;
            max-height: 760px;
            overflow-y: auto;
        }}
        table.prodi-trend-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            font-size: 12px;
        }}
        table.prodi-trend-table thead th {{
            position: sticky;
            top: 0;
            z-index: 10;
            background: #0F172A;
            color: #FFFFFF;
            font-weight: 700;
            padding: 10px 10px;
            text-align: center;
            border-bottom: 2px solid #334155;
            white-space: nowrap;
        }}
        table.prodi-trend-table thead tr.sub-hdr th {{
            top: 39px;
            background: #1E293B;
            color: #E2E8F0;
            font-size: 11px;
            padding: 6px 8px;
            border-bottom: 2px solid #475569;
        }}
        table.prodi-trend-table tbody tr {{
            cursor: pointer;
            transition: background 0.12s ease;
        }}
        table.prodi-trend-table tbody tr:nth-child(even) {{
            background: #F8FAFC;
        }}
        table.prodi-trend-table tbody tr:hover {{
            background: #EFF6FF !important;
        }}
        table.prodi-trend-table td {{
            padding: 9px 10px;
            border-bottom: 1px solid #E2E8F0;
            vertical-align: middle;
        }}
        .yr-vals-strip {{
            display: inline-grid;
            grid-template-columns: repeat(5, 36px);
            gap: 3px;
            font-variant-numeric: tabular-nums;
            font-size: 11px;
        }}
        .yr-pill {{
            text-align: center;
            padding: 2px 3px;
            border-radius: 4px;
            background: #F1F5F9;
            color: #334155;
            font-weight: 600;
        }}
        .yr-pill.hi-rose {{ background: #FFE4E6; color: #9F1239; font-weight: 700; }}
        .yr-pill.hi-amber {{ background: #FEF3C7; color: #92400E; font-weight: 700; }}
        .yr-pill.hi-ok {{ background: #DCFCE7; color: #166534; }}

        /* Drilldown Modal */
        .modal-backdrop {{
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.65);
            backdrop-filter: blur(4px);
            z-index: 999;
            display: none;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .modal-backdrop.open {{
            display: flex;
        }}
        .modal-dialog {{
            background: #FFFFFF;
            border-radius: 18px;
            width: 100%;
            max-width: 1080px;
            max-height: 92vh;
            overflow-y: auto;
            box-shadow: 0 24px 48px rgba(15, 23, 42, 0.35);
            border: 1px solid #CBD5E1;
            display: flex;
            flex-direction: column;
        }}
        .modal-header {{
            padding: 18px 24px;
            background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%);
            color: #FFFFFF;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-radius: 17px 17px 0 0;
        }}
        .modal-body {{
            padding: 20px 24px 24px 24px;
            display: flex;
            flex-direction: column;
            gap: 18px;
        }}
        .modal-charts-grid {{
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 16px;
        }}
        .modal-chart-box {{
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 14px 16px;
        }}
        .modal-chart-box h4 {{
            font-family: 'Outfit', sans-serif;
            font-size: 13.5px;
            font-weight: 700;
            color: #0F172A;
            margin-bottom: 4px;
        }}
        .modal-chart-box p {{
            font-size: 11.5px;
            color: #64748B;
            margin-bottom: 10px;
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
            .workspace, .macro-leaky-panel, .modal-charts-grid {{
                grid-template-columns: 1fr;
            }}
            .kpi-ribbon, .trend-macro-grid {{
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
            <img src="" data-usk-logo="1" alt="Logo Universitas Syiah Kuala" class="usk-header-logo" />
            <div class="brand-divider"></div>
            <div class="brand-titles">
                <h1 id="header-main-title">PETA KUADRAN 60 PROGRAM STUDI S1 KAMPUS UTAMA USK</h1>
                <p id="header-sub-title">Direktorat Pendidikan dan Administrasi Akademik • Universitas Syiah Kuala (2022–2026)</p>
            </div>
        </div>

        <!-- NAVIGATION & SUBSET SWITCHER GROUP -->
        <div class="nav-controls-group" style="display:flex; align-items:center; gap:10px; flex-wrap:wrap;">
            <!-- PRIMARY VIEW MODE SWITCHER -->
            <div class="view-mode-switcher" id="view-mode-switcher">
                <button class="view-mode-btn active" data-view="matrix" id="vm-btn-matrix" title="Tampilkan Peta Scatter 4 Kuadran">
                    📊 Peta Kuadran
                </button>
                <button class="view-mode-btn" data-view="trend" id="vm-btn-trend" title="Tampilkan Evaluasi Tren 81 Prodi: Kursi Kosong (DT-DU) & Batal Daftar Ulang (Lulus-DU)">
                    📉 Evaluasi Tren <span class="vm-badge">81 Prodi</span>
                </button>
            </div>

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

        <div class="header-actions" id="matrix-header-actions">
            <button class="btn btn-outline" id="btn-toggle-labels" title="Tampilkan atau sembunyikan semua label prodi di kanvas">
                🏷️ Toggle Semua Label
            </button>
            <button class="btn btn-outline" id="btn-reset-filters" title="Kembalikan semua filter ke kondisi awal">
                🔄 Reset Tampilan
            </button>
        </div>
    </header>

    <!-- ================================================================= -->
    <!-- VIEW 1: MATRIX SCATTER 4 KUADRAN                                  -->
    <!-- ================================================================= -->
    <div id="matrix-view-wrapper" style="display:flex; flex-direction:column; flex:1;">
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
                    <img src="" data-usk-logo="1" alt="Logo USK" class="ins-placeholder-logo" />
                    <h3>Pilih Program Studi</h3>
                    <p>Klik salah satu lingkaran titik pada kanvas atau gunakan kotak pencarian untuk melihat rincian evaluasi 5 tahun, profil kebocoran kuota, dan rekomendasi kebijakan prodi.</p>
                </div>
                <div id="ins-placeholder-d3" style="display:none; text-align:left;">
                    <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px; border-bottom:1px solid var(--border-subtle); padding-bottom:12px;">
                        <img src="" data-usk-logo="1" alt="Logo USK" style="width:38px; height:38px; object-fit:contain;" />
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
                            <th>Thn</th>
                            <th>Kuota</th>
                            <th>Lulus</th>
                            <th>DU</th>
                            <th title="Kursi Kosong (DT - DU)">Kosong</th>
                            <th title="Batal Daftar Ulang (Lulus - DU)">Batal</th>
                            <th>FR%</th>
                        </tr>
                    </thead>
                    <tbody id="ins-history-tbody">
                        <!-- Injected via JS -->
                    </tbody>
                </table>
                <button type="button" id="btn-open-modal-from-ins" style="width:100%; padding:10px 14px; border-radius:10px; border:1px solid #0F172A; background:#0F172A; color:#FFFFFF; font-family:inherit; font-size:12px; font-weight:700; cursor:pointer; display:flex; align-items:center; justify-content:center; gap:8px;">
                    📈 Bedah Grafik Tren Detail (Kursi Kosong &amp; Batal DU)
                </button>
            </div>
        </aside>
    </main>
    </div>

    <!-- ================================================================= -->
    <!-- VIEW 2: EVALUASI TREN 81 PRODI (KURSI KOSONG VS BATAL DAFTAR ULANG)-->
    <!-- ================================================================= -->
    <div id="trend-view-wrapper">
        <!-- BAGIAN 1: 4 KPI MAKRO (THE LEAKY BUCKET SUMMARY) -->
        <div class="trend-macro-grid">
            <div class="trend-kpi-card tk-blue">
                <div class="tk-title"><span>1. Akumulasi Daya Tampung &amp; Lulus (5-Thn)</span><span>🏛️</span></div>
                <div class="tk-val"><span id="tm-tot-dt">0</span> <span class="tk-pct" style="background:#EFF6FF; color:#1D4ED8;" id="tm-lulus-badge">Lulus: 0</span></div>
                <div class="tk-sub" id="tm-dt-sub">Total kapasitas kursi &amp; peserta lulus seleksi (2022–2026)</div>
            </div>
            <div class="trend-kpi-card tk-emerald">
                <div class="tk-title"><span>2. Realisasi Daftar Ulang (5-Thn)</span><span>✅</span></div>
                <div class="tk-val"><span id="tm-tot-du">0</span> <span class="tk-pct" style="background:#DCFCE7; color:#15803D;" id="tm-fr-badge">FR: 0%</span></div>
                <div class="tk-sub" id="tm-du-sub">Mahasiswa aktif terealisasi • Yield Rate kelulusan</div>
            </div>
            <div class="trend-kpi-card tk-rose">
                <div class="tk-title"><span>3. Tren Kuota Tidak Terisi (DT − DU)</span><span>🔴</span></div>
                <div class="tk-val" style="color:#BE123C;"><span id="tm-tot-sisa">0</span> <span class="tk-pct" style="background:#FFE4E6; color:#9F1239;" id="tm-sisa-pct">0% Kuota</span></div>
                <div class="tk-sub" id="tm-sisa-sub">Akumulasi bangku kosong tidak terisi selama 5 tahun</div>
            </div>
            <div class="trend-kpi-card tk-amber">
                <div class="tk-title"><span>4. Tren Batal Daftar Ulang (Lulus − DU)</span><span>🟠</span></div>
                <div class="tk-val" style="color:#B45309;"><span id="tm-tot-batal">0</span> <span class="tk-pct" style="background:#FEF3C7; color:#92400E;" id="tm-batal-pct">0% Lulus</span></div>
                <div class="tk-sub" id="tm-batal-sub">Calon mahasiswa sudah lulus seleksi namun gugur/mundur</div>
            </div>
        </div>

        <!-- BAGIAN 1B: VISUALISASI MAKRO "THE LEAKY BUCKET" (CHART + TABEL KRONOLOGIS 2022-2026) -->
        <div class="macro-leaky-panel">
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px; flex-wrap:wrap; gap:8px;">
                    <div>
                        <h3 style="font-family:'Outfit',sans-serif; font-size:15.5px; font-weight:800; color:#0F172A;">Grafik Makro "The Leaky Bucket": Daya Tampung vs Lulus vs Daftar Ulang (2022–2026)</h3>
                        <p style="font-size:11.5px; color:#64748B;">Membedakan kebocoran akibat kurang peminat (DT − Lulus) vs batal daftar ulang pasca kelulusan (Lulus − DU)</p>
                    </div>
                    <div style="display:flex; gap:10px; font-size:11px; font-weight:700;">
                        <span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; border-radius:2px; background:#3B82F6;"></span> Daya Tampung</span>
                        <span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; border-radius:2px; background:#6366F1;"></span> Lulus Seleksi</span>
                        <span style="display:inline-flex; align-items:center; gap:4px;"><span style="width:10px; height:10px; border-radius:2px; background:#10B981;"></span> Daftar Ulang</span>
                    </div>
                </div>
                <svg id="macro-leaky-svg" viewBox="0 0 620 235" style="width:100%; height:auto; background:#F8FAFC; border-radius:10px; border:1px solid #E2E8F0;"></svg>
            </div>
            <div>
                <h3 style="font-family:'Outfit',sans-serif; font-size:14.5px; font-weight:800; color:#0F172A; margin-bottom:4px;">Rekapitulasi Tren Tahunan Makro (2022 → 2026)</h3>
                <p style="font-size:11.5px; color:#64748B; margin-bottom:10px;">Menyesuaikan otomatis dengan filter klaster/fakultas yang dipilih di bawah</p>
                <table class="macro-table">
                    <thead>
                        <tr>
                            <th>Tahun</th>
                            <th>Daya Tampung</th>
                            <th>Lulus</th>
                            <th>Daftar Ulang</th>
                            <th style="color:#BE123C;">Kursi Kosong (DT−DU)</th>
                            <th style="color:#B45309;">Batal DU (Lulus−DU)</th>
                        </tr>
                    </thead>
                    <tbody id="macro-trend-tbody"></tbody>
                </table>
            </div>
        </div>

        <!-- BAGIAN 2: KONTROL FILTER & PRESET SORTIR 1-KLIK -->
        <div class="trend-controls-card">
            <div class="trend-toolbar-row">
                <div class="preset-group" id="trend-klaster-pills">
                    <button type="button" class="preset-btn active" data-klaster="ALL">🌐 Semua Prodi USK (81)</button>
                    <button type="button" class="preset-btn" data-klaster="S1_ALL">🎓 S1 Kampus Utama (66)</button>
                    <button type="button" class="preset-btn" data-klaster="S1_60">🏛️ 60 Prodi S1 Mapan</button>
                    <button type="button" class="preset-btn" data-klaster="D3">🛠️ D3 Vokasi (11)</button>
                    <button type="button" class="preset-btn" data-klaster="PSDKU">⛰️ PSDKU Gayo Lues (4)</button>
                </div>
                <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
                    <input type="text" id="trend-search-input" class="trend-search-input" placeholder="🔍 Cari prodi / kode / fakultas...">
                    <select id="trend-fak-select" class="trend-select">
                        <option value="ALL">Semua Fakultas (12)</option>
                    </select>
                    <select id="trend-quad-select" class="trend-select">
                        <option value="ALL">Semua Kuadran</option>
                        <option value="I">Kuadran I: Unggulan</option>
                        <option value="II">Kuadran II: Stabil</option>
                        <option value="III">Kuadran III: Belum Optimal</option>
                        <option value="IV">Kuadran IV: Perlu Ditingkatkan</option>
                    </select>
                </div>
            </div>
            <div class="trend-toolbar-row" style="border-top:1px solid #F1F5F9; padding-top:10px;">
                <div class="preset-group" id="trend-sort-presets">
                    <span style="font-size:11.5px; font-weight:800; color:#475569; margin-right:4px;">⚡ SORTIR EKSEKUTIF:</span>
                    <button type="button" class="preset-btn preset-rose active" data-sort="sisa_desc">🔴 Kursi Kosong Terbanyak (DT − DU)</button>
                    <button type="button" class="preset-btn preset-amber" data-sort="batal_desc">🟠 Batal Daftar Ulang Terbanyak (Lulus − DU)</button>
                    <button type="button" class="preset-btn preset-rose" data-sort="pct_sisa_desc">📉 % Kursi Kosong Tertinggi</button>
                    <button type="button" class="preset-btn preset-amber" data-sort="pct_batal_desc">⚠️ % Batal DU Tertinggi</button>
                    <button type="button" class="preset-btn" data-sort="no_asc">🔢 Urut No / Fakultas Resmi</button>
                </div>
                <div id="trend-count-label" style="font-size:12px; font-weight:700; color:#334155;">
                    Menampilkan: 81 Program Studi
                </div>
            </div>
        </div>

        <!-- BAGIAN 3: TABEL MATRIKS CERDAS SELURUH 81 PRODI DENGAN SPARKLINE -->
        <div class="trend-table-card">
            <div class="trend-table-scroll">
                <table class="prodi-trend-table">
                    <thead>
                        <tr>
                            <th rowspan="2" style="width:42px;">No</th>
                            <th rowspan="2" style="text-align:left; min-width:230px;">Program Studi &amp; Identitas</th>
                            <th rowspan="2" style="min-width:95px;">Kuadran</th>
                            <th colspan="3" style="background:#1E293B;">Akumulasi 5 Tahun (2022–2026)</th>
                            <th colspan="3" style="background:#881337;">🔴 TREN KUOTA TIDAK TERISI / KURSI KOSONG (DT − DU)</th>
                            <th colspan="3" style="background:#78350F;">🟠 TREN BATAL DAFTAR ULANG / MUNDUR (LULUS − DU)</th>
                            <th rowspan="2" style="width:90px;">Detail</th>
                        </tr>
                        <tr class="sub-hdr">
                            <th>Total DT</th>
                            <th>Total Lulus</th>
                            <th>Total DU</th>
                            <th style="background:#9F1239;">Tren 2022 → 2026</th>
                            <th style="background:#9F1239;">Sparkline</th>
                            <th style="background:#9F1239;">Total Kosong (%)</th>
                            <th style="background:#92400E;">Tren 2022 → 2026</th>
                            <th style="background:#92400E;">Sparkline</th>
                            <th style="background:#92400E;">Total Batal (%)</th>
                        </tr>
                    </thead>
                    <tbody id="prodi-trend-tbody">
                        <!-- Rendered dynamically via JS -->
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ================================================================= -->
    <!-- DRILL-DOWN MODAL: BEDAH GRAFIK TREN PRODI (2022–2026)              -->
    <!-- ================================================================= -->
    <div class="modal-backdrop" id="prodi-drilldown-modal">
        <div class="modal-dialog" onclick="event.stopPropagation()">
            <div class="modal-header">
                <div>
                    <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px; flex-wrap:wrap;">
                        <span id="md-kode" style="background:rgba(255,255,255,0.15); padding:2.5px 8px; border-radius:6px; font-size:11px; font-weight:700;">KODE</span>
                        <span id="md-fakultas" style="background:rgba(212,175,55,0.22); color:#FDE047; padding:2.5px 9px; border-radius:6px; font-size:11px; font-weight:700;">FAKULTAS</span>
                        <span id="md-kuadran" style="padding:2.5px 9px; border-radius:6px; font-size:11px; font-weight:800; background:#059669;">KUADRAN</span>
                        <span id="md-tren" style="background:rgba(255,255,255,0.12); padding:2.5px 9px; border-radius:6px; font-size:11px; font-weight:600;">TREN</span>
                    </div>
                    <h2 id="md-title" style="font-family:'Outfit',sans-serif; font-size:21px; font-weight:800; color:#FFFFFF; margin:0;">Nama Program Studi</h2>
                </div>
                <button type="button" onclick="closeProdiModal()" style="background:rgba(255,255,255,0.14); border:1px solid rgba(255,255,255,0.25); color:#FFFFFF; padding:7px 13px; border-radius:8px; font-weight:700; cursor:pointer; font-size:12.5px;">✕ Tutup</button>
            </div>
            <div class="modal-body">
                <!-- 4 KPI Prodi -->
                <div class="trend-macro-grid">
                    <div class="trend-kpi-card tk-blue">
                        <div class="tk-title"><span>Total Daya Tampung (5-Thn)</span><span>🏛️</span></div>
                        <div class="tk-val"><span id="md-tot-dt">0</span> <span class="tk-pct" style="background:#EFF6FF; color:#1D4ED8;" id="md-tot-lulus">Lulus: 0</span></div>
                        <div class="tk-sub" id="md-keketatan-sub">Rasio Keketatan 5-Thn: 0.0 : 1</div>
                    </div>
                    <div class="trend-kpi-card tk-emerald">
                        <div class="tk-title"><span>Realisasi Daftar Ulang (5-Thn)</span><span>✅</span></div>
                        <div class="tk-val"><span id="md-tot-du">0</span> <span class="tk-pct" style="background:#DCFCE7; color:#15803D;" id="md-fr-pct">FR: 0%</span></div>
                        <div class="tk-sub" id="md-yield-sub">Yield Rate (DU / Lulus): 0%</div>
                    </div>
                    <div class="trend-kpi-card tk-rose">
                        <div class="tk-title"><span>Akumulasi Kursi Kosong (DT − DU)</span><span>🔴</span></div>
                        <div class="tk-val" style="color:#BE123C;"><span id="md-tot-sisa">0</span> <span class="tk-pct" style="background:#FFE4E6; color:#9F1239;" id="md-sisa-pct">0%</span></div>
                        <div class="tk-sub">Kuota tidak terserap selama 2022–2026</div>
                    </div>
                    <div class="trend-kpi-card tk-amber">
                        <div class="tk-title"><span>Akumulasi Batal DU (Lulus − DU)</span><span>🟠</span></div>
                        <div class="tk-val" style="color:#B45309;"><span id="md-tot-batal">0</span> <span class="tk-pct" style="background:#FEF3C7; color:#92400E;" id="md-batal-pct">0%</span></div>
                        <div class="tk-sub">Calon mahasiswa lulus yang tidak daftar ulang</div>
                    </div>
                </div>

                <!-- 2 Grafik Interaktif Prodi -->
                <div class="modal-charts-grid">
                    <div class="modal-chart-box">
                        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:8px;">
                            <div>
                                <h4>1. Grafik Komparasi Kapasitas vs Lulus vs Daftar Ulang (2022–2026)</h4>
                                <p style="margin-bottom:6px;">Jurang antara garis menunjukkan Kursi Kosong (DT − DU) dan Batal Daftar Ulang (Lulus − DU)</p>
                            </div>
                        </div>
                        <!-- KETERANGAN WARNA & JENIS GARIS (LEGENDA) -->
                        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:10px; font-size:11px; font-weight:700;">
                            <span style="display:inline-flex; align-items:center; gap:5px; background:#EFF6FF; color:#1D4ED8; padding:3px 8px; border-radius:6px; border:1px solid #BFDBFE;">
                                <span style="width:12px; height:3.5px; background:#2563EB; border-radius:2px;"></span> 🔵 Garis Biru: <strong>Daya Tampung (DT)</strong>
                            </span>
                            <span style="display:inline-flex; align-items:center; gap:5px; background:#F3E8FF; color:#6B21A8; padding:3px 8px; border-radius:6px; border:1px solid #DDD6FE;">
                                <span style="width:14px; height:0px; border-top:2.5px dashed #7C3AED;"></span> 🟣 Garis Putus-putus: <strong>Lulus Seleksi</strong>
                            </span>
                            <span style="display:inline-flex; align-items:center; gap:5px; background:#DCFCE7; color:#15803D; padding:3px 8px; border-radius:6px; border:1px solid #86EFAC;">
                                <span style="width:12px; height:3.5px; background:#059669; border-radius:2px;"></span> 🟢 Garis Hijau: <strong>Daftar Ulang (DU)</strong>
                            </span>
                            <span style="display:inline-flex; align-items:center; gap:5px; background:#FFF1F2; color:#9F1239; padding:3px 8px; border-radius:6px; border:1px solid #FECDD3;">
                                <span style="width:10px; height:10px; background:#FECDD3; border-radius:2px;"></span> 🔴 Arsiran Merah: Sisa Kuota
                            </span>
                        </div>
                        <svg id="md-chart-lines" viewBox="0 0 540 230" style="width:100%; height:auto; background:#FFFFFF; border-radius:8px; border:1px solid #E2E8F0;"></svg>
                    </div>
                    <div class="modal-chart-box">
                        <h4>2. Tren Tahunan Kursi Kosong vs Batal Daftar Ulang (2022–2026)</h4>
                        <p style="margin-bottom:6px;">Perbandingan langsung jumlah kursi kosong (merah) dan mahasiswa mundur (oranye) tiap tahun</p>
                        <!-- KETERANGAN WARNA BATANG (LEGENDA) -->
                        <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:10px; font-size:11px; font-weight:700;">
                            <span style="display:inline-flex; align-items:center; gap:5px; background:#FFF1F2; color:#BE123C; padding:3px 8px; border-radius:6px; border:1px solid #FECDD3;">
                                <span style="width:10px; height:10px; background:#E11D48; border-radius:2px;"></span> 🔴 Batang Merah: <strong>Kursi Kosong (DT − DU)</strong>
                            </span>
                            <span style="display:inline-flex; align-items:center; gap:5px; background:#FFFBEB; color:#B45309; padding:3px 8px; border-radius:6px; border:1px solid #FDE68A;">
                                <span style="width:10px; height:10px; background:#D97706; border-radius:2px;"></span> 🟠 Batang Oranye: <strong>Batal Daftar Ulang (Lulus − DU)</strong>
                            </span>
                        </div>
                        <svg id="md-chart-bars" viewBox="0 0 420 230" style="width:100%; height:auto; background:#FFFFFF; border-radius:8px; border:1px solid #E2E8F0;"></svg>
                    </div>
                </div>

                <!-- Tabel Rincian Multi-Tahun (Descending 2026 -> 2022 sesuai GEMINI.md) -->
                <div>
                    <h4 style="font-family:'Outfit',sans-serif; font-size:14px; font-weight:800; color:#0F172A; margin-bottom:8px;">Tabel Rincian Tahunan Program Studi (Urutan Tahun Menurun: 2026 → 2022 &amp; Total 5 Tahun)</h4>
                    <table class="macro-table" style="border:1px solid #E2E8F0;">
                        <thead>
                            <tr>
                                <th>Tahun</th>
                                <th>Peminat</th>
                                <th>Daya Tampung (DT)</th>
                                <th>Lulus Seleksi</th>
                                <th>Daftar Ulang (DU)</th>
                                <th style="color:#BE123C;">Kursi Kosong (DT−DU)</th>
                                <th>Fill Rate (%)</th>
                                <th style="color:#B45309;">Batal DU (Lulus−DU)</th>
                                <th>% Batal DU</th>
                            </tr>
                        </thead>
                        <tbody id="md-history-tbody"></tbody>
                    </table>
                </div>

                <div class="rekomendasi-box">
                    <h4>💡 REKOMENDASI KEBIJAKAN PROGRAM STUDI</h4>
                    <p id="md-rekomendasi-text"></p>
                </div>
            </div>
        </div>
    </div>

    <!-- FOOTER -->
    <footer class="bottom-bar">
        <div>
            <strong>Universitas Syiah Kuala</strong> • Kampus Jantong Hate Rakyat Aceh • Akreditasi Unggul
        </div>
        <div id="footer-standards">
            Standar Evaluasi S1: <strong>Keketatan 4,0 : 1</strong> | <strong>Keterisian Ideal 80%</strong>
        </div>
    </footer>

    <!-- SCRIPT DATA & INTERACTION LOGIC -->
    <script>
        const USK_LOGO_B64 = "{usk_logo_b64}";
        if (USK_LOGO_B64) {{
            const favEl = document.getElementById('usk-favicon');
            if (favEl) favEl.href = USK_LOGO_B64;
            document.querySelectorAll('img[data-usk-logo]').forEach(img => {{
                img.src = USK_LOGO_B64;
            }});
        }}
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
        const PRODI_SHORT_NAMES = {json.dumps(PRODI_HTML_SHORT_NAMES, ensure_ascii=False)};

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
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 130, yThreshold80, 250, 22, '#475569', '#94A3B8', '#FFFFFF', 'STANDAR KETERISIAN: 80% (TARGET IDEAL)'));

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
                // Standar Keterisian Kuota Ideal 80% (Dashed slate)
                svg.appendChild(createLine(PLOT_X, yThreshold80, PLOT_X + PLOT_W, yThreshold80, '#64748B', 1.8, '5,4', 0.90));
                // Batas Kritis Kelayakan Operasional 50% (Prominent Red Dotted Line)
                svg.appendChild(createLine(PLOT_X, yThreshold50, PLOT_X + PLOT_W, yThreshold50, '#DC2626', 2.2, '3,4', 0.95));

                // Badges D3
                svg.appendChild(createPillBadge(xThreshold, PLOT_Y + PLOT_H - 18, 190, 22, '#475569', '#94A3B8', '#FFFFFF', '▲ AMBANG KEKETATAN: 4,0 : 1'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 130, yThreshold80, 240, 22, '#475569', '#94A3B8', '#FFFFFF', 'STANDAR IDEAL: 80% KETERISIAN'));
                svg.appendChild(createPillBadge(PLOT_X + PLOT_W - 145, yThreshold50, 270, 22, '#DC2626', '#F87171', '#FFFFFF', '⚠ BATAS KRITIS KELAYAKAN: 50%'));

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
                document.getElementById('ins-fillrate-status').textContent = frCapped >= 80.0 ? 'Keterisian Ideal (>= 80%)' : 'Under-Enrolled (< 80%)';
            }} else {{
                document.getElementById('ins-fillrate-status').textContent = frCapped >= 50.0 ? 'Di Atas Batas Kritis (>= 50%)' : 'Kritis Defisit (< 50%)';
            }}

            document.getElementById('ins-peminat').textContent = `${{Math.round(d.peminat_5thn).toLocaleString('id-ID')}} org/thn`;
            document.getElementById('ins-dt').textContent = `${{Math.round(d.dt_5thn)}} kursi/thn`;
            document.getElementById('ins-sisa-kursi').textContent = d.sisa_5thn > 0 ? `Bocor/Kosong: ${{d.sisa_5thn}} kursi` : 'Kuota Terserap Penuh (100%)';

            document.getElementById('ins-rekomendasi-text').textContent = d.rekomendasi;
            document.getElementById('ins-tren-tag').textContent = d.tren_resmi.toUpperCase();

            // Render table with 100% Capped Fill Rate + Kursi Kosong & Batal DU
            const tbody = document.getElementById('ins-history-tbody');
            tbody.innerHTML = '';
            d.history.forEach(h => {{
                const frHistory = clampFR(h.fill_rate);
                const tr = document.createElement('tr');
                const thresholdBenchmark = (currentLevel === 's1') ? 80.0 : 50.0;
                const sisaVal = (h.sisa !== undefined) ? h.sisa : (h.dt - h.du);
                const batalVal = (h.batal !== undefined) ? h.batal : ((h.lulus || h.dt) - h.du);
                tr.innerHTML = `
                    <td><strong>${{h.tahun}}</strong></td>
                    <td>${{h.dt}}</td>
                    <td>${{(h.lulus !== undefined ? h.lulus : '-')}}</td>
                    <td>${{h.du}}</td>
                    <td style="color:#BE123C; font-weight:700;">${{sisaVal}}</td>
                    <td style="color:#B45309; font-weight:700;">${{batalVal}}</td>
                    <td style="font-weight:700; color:${{frHistory >= thresholdBenchmark ? '#059669' : '#DC2626'}}">${{frHistory.toFixed(1)}}%</td>
                `;
                tbody.appendChild(tr);
            }});

            const btnModal = document.getElementById('btn-open-modal-from-ins');
            if (btnModal) {{
                btnModal.onclick = () => {{
                    const matchAll = (DATA_BY_LEVEL.all || []).find(x => x.nama.toUpperCase() === d.nama.toUpperCase() && x.jenjang === d.jenjang);
                    openProdiModal(matchAll || d);
                }};
            }}
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

        function updateD3TierControls() {{
            updateTierGuideCardStates();
            renderFacultyFilters();
        }}

        function toggleTierFilter(tierNum) {{
            currentD3Tier = (currentD3Tier === tierNum) ? 'ALL' : tierNum;
            updateD3TierControls();
            renderChart();
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
                    document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi S1: <strong>Keketatan 4,0 : 1</strong> | <strong>Keterisian Ideal 80%</strong>';
                }} else {{
                    document.getElementById('header-main-title').textContent = 'PETA KUADRAN 11 PROGRAM STUDI D3 VOKASI USK';
                    document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (11 Prodi D3 Vokasi)';
                    document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi D3: <strong>Keketatan 4,0 : 1</strong> | <strong>Standar Ideal 80%</strong> | <strong>Batas Kritis 50%</strong>';
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

        // =================================================================
        // VIEW 2 LOGIC: EVALUASI TREN 81 PRODI (KURSI KOSONG & BATAL DU)
        // =================================================================
        let currentViewMode = (window.location.hash.includes('tren')) ? 'trend' : 'matrix';
        let trendKlaster = 'ALL'; // ALL, S1_ALL, S1_60, D3, PSDKU
        let trendFak = 'ALL';
        let trendQuad = 'ALL';
        let trendSort = 'sisa_desc';
        let trendSearch = '';

        // Populate Fakultas Select in Trend View
        function initTrendFakOptions() {{
            const sel = document.getElementById('trend-fak-select');
            if (!sel) return;
            const faks = {{}};
            (DATA_BY_LEVEL.all || []).forEach(p => {{
                faks[p.fakultas] = (faks[p.fakultas] || 0) + 1;
            }});
            Object.keys(faks).sort((a, b) => faks[b] - faks[a]).forEach(f => {{
                const opt = document.createElement('option');
                opt.value = f;
                opt.textContent = `${{fak_abbr_map_client[f] || f}} — ${{f}} (${{faks[f]}})`;
                sel.appendChild(opt);
            }});
        }}

        function getFilteredTrendProdi() {{
            const list = DATA_BY_LEVEL.all || [];
            const filtered = list.filter(p => {{
                if (trendKlaster === 'S1_ALL' && p.klaster !== 'S1 Kampus Utama') return false;
                if (trendKlaster === 'S1_60' && (p.klaster !== 'S1 Kampus Utama' || p.is_prodi_baru)) return false;
                if (trendKlaster === 'D3' && p.klaster !== 'Diploma 3 Vokasi') return false;
                if (trendKlaster === 'PSDKU' && p.klaster !== 'PSDKU Gayo Lues') return false;
                if (trendFak !== 'ALL' && p.fakultas !== trendFak) return false;
                if (trendQuad !== 'ALL' && p.kuadran !== trendQuad) return false;
                if (trendSearch.trim() !== '') {{
                    const q = trendSearch.trim().toLowerCase();
                    const matchName = p.nama.toLowerCase().includes(q);
                    const matchCode = (p.kode || '').toLowerCase().includes(q);
                    const matchFak = p.fakultas.toLowerCase().includes(q) || p.fakultas_abbr.toLowerCase().includes(q);
                    if (!matchName && !matchCode && !matchFak) return false;
                }}
                return true;
            }});

            filtered.sort((a, b) => {{
                if (trendSort === 'sisa_desc') return (b.tot_sisa - a.tot_sisa) || (b.pct_sisa - a.pct_sisa);
                if (trendSort === 'batal_desc') return (b.tot_batal - a.tot_batal) || (b.pct_batal - a.pct_batal);
                if (trendSort === 'pct_sisa_desc') return (b.pct_sisa - a.pct_sisa) || (b.tot_sisa - a.tot_sisa);
                if (trendSort === 'pct_batal_desc') return (b.pct_batal - a.pct_batal) || (b.tot_batal - a.tot_batal);
                return a.no - b.no;
            }});
            return filtered;
        }}

        // Build Inline SVG Sparkline (5 points: 2022..2026)
        function buildSparklineSVG(vals, colorHex, fillHex) {{
            const w = 88, h = 28, padX = 6, padY = 5;
            const minV = Math.min(...vals, 0);
            const maxV = Math.max(...vals, 1);
            const range = Math.max(maxV - minV, 1);
            const pts = vals.map((v, i) => {{
                const x = padX + (i / 4) * (w - 2 * padX);
                const y = padY + (1 - (v - minV) / range) * (h - 2 * padY);
                return `${{x.toFixed(1)}},${{y.toFixed(1)}}`;
            }});
            const lastPt = pts[pts.length - 1].split(',');
            const firstPt = pts[0].split(',');
            const areaPts = `${{firstPt[0]}},${{h - 2}} ${{pts.join(' ')}} ${{lastPt[0]}},${{h - 2}}`;
            return `<svg width="${{w}}" height="${{h}}" viewBox="0 0 ${{w}} ${{h}}" style="overflow:visible; display:block; margin:0 auto;">
                <polygon points="${{areaPts}}" fill="${{fillHex}}" opacity="0.55"/>
                <polyline points="${{pts.join(' ')}}" fill="none" stroke="${{colorHex}}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="${{lastPt[0]}}" cy="${{lastPt[1]}}" r="2.8" fill="${{colorHex}}"/>
            </svg>`;
        }}

        function renderMacroLeakyBucket(filteredList) {{
            const yrStats = {{
                2022: {{ dt: 0, lu: 0, du: 0, sisa: 0, batal: 0 }},
                2023: {{ dt: 0, lu: 0, du: 0, sisa: 0, batal: 0 }},
                2024: {{ dt: 0, lu: 0, du: 0, sisa: 0, batal: 0 }},
                2025: {{ dt: 0, lu: 0, du: 0, sisa: 0, batal: 0 }},
                2026: {{ dt: 0, lu: 0, du: 0, sisa: 0, batal: 0 }}
            }};
            let sumDT = 0, sumLU = 0, sumDU = 0, sumSisa = 0, sumBatal = 0;

            filteredList.forEach(p => {{
                sumDT += p.tot_dt;
                sumLU += p.tot_lulus;
                sumDU += p.tot_du;
                sumSisa += p.tot_sisa;
                sumBatal += p.tot_batal;
                p.history.forEach(h => {{
                    if (yrStats[h.tahun]) {{
                        yrStats[h.tahun].dt += h.dt;
                        yrStats[h.tahun].lu += h.lulus;
                        yrStats[h.tahun].du += h.du;
                        yrStats[h.tahun].sisa += h.sisa;
                        yrStats[h.tahun].batal += h.batal;
                    }}
                }});
            }});

            const pctSisa = sumDT > 0 ? (sumSisa / sumDT * 100).toFixed(1) : '0.0';
            const pctBatal = sumLU > 0 ? (sumBatal / sumLU * 100).toFixed(1) : '0.0';
            const pctFR = sumDT > 0 ? (sumDU / sumDT * 100).toFixed(1) : '0.0';
            const pctYield = sumLU > 0 ? (sumDU / sumLU * 100).toFixed(1) : '0.0';

            document.getElementById('tm-tot-dt').textContent = sumDT.toLocaleString('id-ID') + ' Kursi';
            document.getElementById('tm-lulus-badge').textContent = 'Lulus: ' + sumLU.toLocaleString('id-ID');
            document.getElementById('tm-dt-sub').textContent = `Rata-rata ${{Math.round(sumDT / 5).toLocaleString('id-ID')}} kursi/thn (${{filteredList.length}} Prodi)`;

            document.getElementById('tm-tot-du').textContent = sumDU.toLocaleString('id-ID') + ' Mhs';
            document.getElementById('tm-fr-badge').textContent = `Fill Rate: ${{pctFR}}%`;
            document.getElementById('tm-du-sub').textContent = `Yield Rate Kelulusan: ${{pctYield}}% daftar ulang dari yang lulus`;

            document.getElementById('tm-tot-sisa').textContent = sumSisa.toLocaleString('id-ID') + ' Kursi';
            document.getElementById('tm-sisa-pct').textContent = `${{pctSisa}}% Kuota Kosong`;
            document.getElementById('tm-sisa-sub').textContent = `Rata-rata ${{Math.round(sumSisa / 5).toLocaleString('id-ID')}} kursi/thn tidak terisi`;

            document.getElementById('tm-tot-batal').textContent = sumBatal.toLocaleString('id-ID') + ' Org';
            document.getElementById('tm-batal-pct').textContent = `${{pctBatal}}% Batal DU`;
            const shareBatalOfSisa = sumSisa > 0 ? Math.min(100, Math.round(sumBatal / sumSisa * 100)) : 0;
            document.getElementById('tm-batal-sub').textContent = `Rata-rata ${{Math.round(sumBatal / 5).toLocaleString('id-ID')}} org/thn gugur pasca dinyatakan lulus (${{shareBatalOfSisa}}% beban kursi kosong)`;

            // Render Macro Table (Chronological 2022 -> 2026 + Total 5-Thn)
            const tbody = document.getElementById('macro-trend-tbody');
            tbody.innerHTML = '';
            [2022, 2023, 2024, 2025, 2026].forEach(yr => {{
                const st = yrStats[yr];
                const pSisa = st.dt > 0 ? (st.sisa / st.dt * 100).toFixed(1) : '0.0';
                const pBatal = st.lu > 0 ? (st.batal / st.lu * 100).toFixed(1) : '0.0';
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${{yr}}</td>
                    <td>${{st.dt.toLocaleString('id-ID')}}</td>
                    <td>${{st.lu.toLocaleString('id-ID')}}</td>
                    <td style="font-weight:700; color:#059669;">${{st.du.toLocaleString('id-ID')}}</td>
                    <td style="font-weight:700; color:#BE123C;">${{st.sisa.toLocaleString('id-ID')}} <span style="font-size:10.5px; color:#64748B;">(${{pSisa}}%)</span></td>
                    <td style="font-weight:700; color:#B45309;">${{st.batal.toLocaleString('id-ID')}} <span style="font-size:10.5px; color:#64748B;">(${{pBatal}}%)</span></td>
                `;
                tbody.appendChild(tr);
            }});
            const trTot = document.createElement('tr');
            trTot.className = 'total-row';
            trTot.innerHTML = `
                <td>TOTAL 5-THN</td>
                <td>${{sumDT.toLocaleString('id-ID')}}</td>
                <td>${{sumLU.toLocaleString('id-ID')}}</td>
                <td style="color:#6EE7B7;">${{sumDU.toLocaleString('id-ID')}}</td>
                <td style="color:#FDA4AF;">${{sumSisa.toLocaleString('id-ID')}} (${{pctSisa}}%)</td>
                <td style="color:#FDE047;">${{sumBatal.toLocaleString('id-ID')}} (${{pctBatal}}%)</td>
            `;
            tbody.appendChild(trTot);

            // Render Macro Leaky Bucket SVG Chart
            const svg = document.getElementById('macro-leaky-svg');
            if (!svg) return;
            const W = 620, H = 235, padL = 48, padR = 18, padT = 26, padB = 34;
            const plotW = W - padL - padR, plotH = H - padT - padB;
            const years = [2022, 2023, 2024, 2025, 2026];
            const maxVal = Math.max(...years.map(y => Math.max(yrStats[y].dt, yrStats[y].lu, yrStats[y].du)), 100) * 1.15;

            let svgHtml = '';
            // Grid lines
            for (let i = 0; i <= 4; i++) {{
                const v = Math.round((maxVal / 4) * i);
                const yPos = padT + plotH - (i / 4) * plotH;
                svgHtml += `<line x1="${{padL}}" y1="${{yPos}}" x2="${{W - padR}}" y2="${{yPos}}" stroke="#E2E8F0" stroke-dasharray="3,3"/>`;
                svgHtml += `<text x="${{padL - 6}}" y="${{yPos + 4}}" text-anchor="end" font-size="10" fill="#64748B" font-weight="600">${{v.toLocaleString('id-ID')}}</text>`;
            }}

            const groupW = plotW / 5;
            const barW = 20;
            years.forEach((yr, idx) => {{
                const st = yrStats[yr];
                const cx = padL + groupW * idx + groupW / 2;
                const hDT = (st.dt / maxVal) * plotH;
                const hLU = (st.lu / maxVal) * plotH;
                const hDU = (st.du / maxVal) * plotH;
                const yDT = padT + plotH - hDT;
                const yLU = padT + plotH - hLU;
                const yDU = padT + plotH - hDU;

                // Bars: DT, Lulus, DU
                svgHtml += `<rect x="${{cx - barW * 1.5 - 2}}" y="${{yDT}}" width="${{barW}}" height="${{hDT}}" rx="3" fill="#3B82F6"/>`;
                svgHtml += `<rect x="${{cx - barW * 0.5}}" y="${{yLU}}" width="${{barW}}" height="${{hLU}}" rx="3" fill="#6366F1"/>`;
                svgHtml += `<rect x="${{cx + barW * 0.5 + 2}}" y="${{yDU}}" width="${{barW}}" height="${{hDU}}" rx="3" fill="#10B981"/>`;

                // Year label
                svgHtml += `<text x="${{cx}}" y="${{H - 12}}" text-anchor="middle" font-size="11.5" font-weight="800" fill="#0F172A">${{yr}}</text>`;

                // Callout badge above bars: Kosong & Batal
                const topY = Math.min(yDT, yLU, yDU) - 7;
                svgHtml += `<text x="${{cx}}" y="${{topY}}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#BE123C">Kosong:${{st.sisa.toLocaleString('id-ID')}} | Batal:${{st.batal.toLocaleString('id-ID')}}</text>`;
            }});
            svg.innerHTML = svgHtml;
        }}

        function renderTrendTable() {{
            const filtered = getFilteredTrendProdi();
            renderMacroLeakyBucket(filtered);

            const countEl = document.getElementById('trend-count-label');
            if (countEl) countEl.textContent = `Menampilkan: ${{filtered.length}} dari ${{(DATA_BY_LEVEL.all || []).length}} Program Studi`;

            const tbody = document.getElementById('prodi-trend-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';

            filtered.forEach((p, idx) => {{
                const tr = document.createElement('tr');
                tr.title = `Klik untuk membuka grafik detail ${{p.nama}}`;
                tr.addEventListener('click', () => openProdiModal(p));

                const sisaArr = p.history.map(h => h.sisa);
                const batalArr = p.history.map(h => h.batal);

                const sisaPills = p.history.map(h => {{
                    const cls = h.sisa >= 30 ? 'hi-rose' : (h.sisa <= 5 ? 'hi-ok' : '');
                    return `<span class="yr-pill ${{cls}}" title="Kursi Kosong ${{h.tahun}}: ${{h.sisa}}">${{h.sisa}}</span>`;
                }}).join('');

                const batalPills = p.history.map(h => {{
                    const cls = h.batal >= 25 ? 'hi-amber' : (h.batal <= 5 ? 'hi-ok' : '');
                    return `<span class="yr-pill ${{cls}}" title="Batal DU ${{h.tahun}}: ${{h.batal}}">${{h.batal}}</span>`;
                }}).join('');

                const sparkSisa = buildSparklineSVG(sisaArr, '#E11D48', '#FECDD3');
                const sparkBatal = buildSparklineSVG(batalArr, '#D97706', '#FDE68A');

                const jenjangBadge = p.klaster === 'PSDKU Gayo Lues'
                    ? `<span style="background:#F3E8FF; color:#6B21A8; padding:1.5px 6px; border-radius:4px; font-size:10px; font-weight:700;">PSDKU</span>`
                    : `<span style="background:#F1F5F9; color:#334155; padding:1.5px 6px; border-radius:4px; font-size:10px; font-weight:700;">${{p.jenjang}}</span>`;

                const baruBadge = p.is_prodi_baru
                    ? `<span style="background:#DBEAFE; color:#1E40AF; padding:1.5px 5px; border-radius:4px; font-size:9.5px; font-weight:700; margin-left:4px;">BARU</span>`
                    : '';

                tr.innerHTML = `
                    <td style="text-align:center; font-weight:700; color:#64748B;">${{idx + 1}}</td>
                    <td>
                        <div style="font-weight:800; color:#0F172A; font-size:12.5px;">${{p.jenjang === 'D3' ? 'D3 ' : ''}}${{p.nama}}${{baruBadge}}</div>
                        <div style="display:flex; align-items:center; gap:6px; margin-top:3px; font-size:11px; color:#64748B;">
                            <span>Kode: <strong>${{p.kode}}</strong></span> • <span><strong>${{p.fakultas_abbr}}</strong> (${{p.fakultas}})</span> • ${{jenjangBadge}}
                        </div>
                    </td>
                    <td style="text-align:center;">
                        <span style="display:inline-block; padding:3px 8px; border-radius:6px; font-size:10.5px; font-weight:800; color:#FFFFFF; background:${{p.color}};">
                            Kuadran ${{p.kuadran}}
                        </span>
                        <div style="font-size:10px; color:#64748B; margin-top:2px;">FR: ${{p.fill_rate}}% • ${{p.keketatan}}x</div>
                    </td>
                    <td style="text-align:right; font-weight:600;">${{p.tot_dt.toLocaleString('id-ID')}}</td>
                    <td style="text-align:right; font-weight:600;">${{p.tot_lulus.toLocaleString('id-ID')}}</td>
                    <td style="text-align:right; font-weight:700; color:#059669;">${{p.tot_du.toLocaleString('id-ID')}}</td>
                    <td style="text-align:center; background:#FFFDFD;">
                        <div class="yr-vals-strip">${{sisaPills}}</div>
                    </td>
                    <td style="text-align:center; background:#FFFDFD;">${{sparkSisa}}</td>
                    <td style="text-align:right; background:#FFF1F2; font-weight:800; color:#BE123C;">
                        <div>${{p.tot_sisa.toLocaleString('id-ID')}} kursi</div>
                        <div style="font-size:10.5px; font-weight:700; color:#9F1239;">(${{p.pct_sisa}}% DT)</div>
                    </td>
                    <td style="text-align:center; background:#FFFDF9;">
                        <div class="yr-vals-strip">${{batalPills}}</div>
                    </td>
                    <td style="text-align:center; background:#FFFDF9;">${{sparkBatal}}</td>
                    <td style="text-align:right; background:#FFFBEB; font-weight:800; color:#B45309;">
                        <div>${{p.tot_batal.toLocaleString('id-ID')}} org</div>
                        <div style="font-size:10.5px; font-weight:700; color:#92400E;">(${{p.pct_batal}}% Lulus)</div>
                    </td>
                    <td style="text-align:center;">
                        <button type="button" style="padding:5px 9px; border-radius:6px; border:1px solid #CBD5E1; background:#FFFFFF; color:#0F172A; font-size:11px; font-weight:700; cursor:pointer;">🔍 Grafik</button>
                    </td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // Modal Drilldown Functions
        function openProdiModal(p) {{
            const modal = document.getElementById('prodi-drilldown-modal');
            if (!modal || !p) return;

            const totDT = p.tot_dt !== undefined ? p.tot_dt : p.history.reduce((s, h) => s + h.dt, 0);
            const totLU = p.tot_lulus !== undefined ? p.tot_lulus : p.history.reduce((s, h) => s + (h.lulus || 0), 0);
            const totDU = p.tot_du !== undefined ? p.tot_du : p.history.reduce((s, h) => s + h.du, 0);
            const totSisa = totDT - totDU;
            const totBatal = totLU - totDU;
            const pctSisa = totDT > 0 ? (totSisa / totDT * 100).toFixed(1) : '0.0';
            const pctBatal = totLU > 0 ? (totBatal / totLU * 100).toFixed(1) : '0.0';
            const pctFR = totDT > 0 ? (totDU / totDT * 100).toFixed(1) : '0.0';
            const pctYield = totLU > 0 ? (totDU / totLU * 100).toFixed(1) : '0.0';

            document.getElementById('md-kode').textContent = `Kode: ${{p.kode || '-'}}`;
            document.getElementById('md-fakultas').textContent = `${{p.fakultas_abbr}} • ${{p.fakultas}} (${{p.jenjang}})`;
            const qEl = document.getElementById('md-kuadran');
            qEl.textContent = p.kuadran_title;
            qEl.style.background = p.color;
            document.getElementById('md-tren').textContent = p.tren_resmi;
            document.getElementById('md-title').textContent = (p.jenjang === 'D3' ? 'D3 ' : '') + p.nama;

            document.getElementById('md-tot-dt').textContent = totDT.toLocaleString('id-ID') + ' Kursi';
            document.getElementById('md-tot-lulus').textContent = `Lulus: ${{totLU.toLocaleString('id-ID')}}`;
            document.getElementById('md-keketatan-sub').textContent = `Rasio Keketatan 5-Thn: ${{p.keketatan}} : 1`;

            document.getElementById('md-tot-du').textContent = totDU.toLocaleString('id-ID') + ' Mhs';
            document.getElementById('md-fr-pct').textContent = `Fill Rate: ${{pctFR}}%`;
            document.getElementById('md-yield-sub').textContent = `Yield Rate (DU / Lulus): ${{pctYield}}%`;

            document.getElementById('md-tot-sisa').textContent = totSisa.toLocaleString('id-ID') + ' Kursi';
            document.getElementById('md-sisa-pct').textContent = `${{pctSisa}}% DT`;

            document.getElementById('md-tot-batal').textContent = totBatal.toLocaleString('id-ID') + ' Org';
            document.getElementById('md-batal-pct').textContent = `${{pctBatal}}% Lulus`;
            document.getElementById('md-rekomendasi-text').textContent = p.rekomendasi || '';

            // 1. Render Modal Left Chart: 3 Lines (DT, Lulus, DU)
            const svgLines = document.getElementById('md-chart-lines');
            if (svgLines) {{
                const W = 540, H = 230, padL = 52, padR = 24, padT = 26, padB = 32;
                const plotW = W - padL - padR, plotH = H - padT - padB;
                const maxV = Math.max(...p.history.map(h => Math.max(h.dt, h.lulus || 0, h.du)), 10) * 1.18;

                let html = '';
                for (let i = 0; i <= 4; i++) {{
                    const v = Math.round((maxV / 4) * i);
                    const y = padT + plotH - (i / 4) * plotH;
                    html += `<line x1="${{padL}}" y1="${{y}}" x2="${{W - padR}}" y2="${{y}}" stroke="#E2E8F0" stroke-dasharray="3,3"/>`;
                    html += `<text x="${{padL - 7}}" y="${{y + 4}}" text-anchor="end" font-size="10" fill="#64748B">${{v}}</text>`;
                }}

                const getPt = (val, idx) => {{
                    const x = padL + (idx / 4) * plotW;
                    const y = padT + plotH - (val / maxV) * plotH;
                    return [x, y];
                }};

                const dtPts = p.history.map((h, i) => getPt(h.dt, i));
                const luPts = p.history.map((h, i) => getPt(h.lulus || 0, i));
                const duPts = p.history.map((h, i) => getPt(h.du, i));

                // Shaded gap area between DT and DU
                const polyDT_DU = [...dtPts.map(pt => pt.join(',')), ...duPts.slice().reverse().map(pt => pt.join(','))].join(' ');
                html += `<polygon points="${{polyDT_DU}}" fill="#FECDD3" opacity="0.35"/>`;

                const drawLine = (pts, color, dash='') => {{
                    const s = pts.map(pt => pt.join(',')).join(' ');
                    return `<polyline points="${{s}}" fill="none" stroke="${{color}}" stroke-width="2.6" ${{dash ? `stroke-dasharray="${{dash}}"` : ''}}/>`;
                }};
                html += drawLine(dtPts, '#2563EB');
                html += drawLine(luPts, '#7C3AED', '5,3');
                html += drawLine(duPts, '#059669');

                p.history.forEach((h, i) => {{
                    const [x, yDT] = dtPts[i];
                    const [_, yLU] = luPts[i];
                    const [__, yDU] = duPts[i];
                    const luVal = h.lulus || 0;

                    // Circles with native hover tooltip
                    html += `<circle cx="${{x}}" cy="${{yDT}}" r="4" fill="#2563EB"><title>${{h.tahun}}: Daya Tampung = ${{h.dt}} kursi</title></circle>`;
                    html += `<circle cx="${{x}}" cy="${{yLU}}" r="3.5" fill="#7C3AED"><title>${{h.tahun}}: Lulus Seleksi = ${{luVal}} orang</title></circle>`;
                    html += `<circle cx="${{x}}" cy="${{yDU}}" r="4" fill="#059669"><title>${{h.tahun}}: Daftar Ulang = ${{h.du}} mahasiswa</title></circle>`;

                    // 1. Data label Lulus (Ungu): di atas titik Lulus
                    html += `<text x="${{x}}" y="${{yLU - 7}}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#6B21A8">${{luVal}}</text>`;

                    // 2. Data label DT (Biru)
                    if (Math.abs(yDT - yLU) < 14) {{
                        if (Math.abs(yDU - yDT) > 22) {{
                            html += `<text x="${{x}}" y="${{yDT + 12}}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1D4ED8">${{h.dt}}</text>`;
                        }} else {{
                            html += `<text x="${{x - 14}}" y="${{yDT - 2}}" text-anchor="end" font-size="9.5" font-weight="700" fill="#1D4ED8">${{h.dt}}</text>`;
                        }}
                    }} else {{
                        html += `<text x="${{x}}" y="${{yDT - 7}}" text-anchor="middle" font-size="9.5" font-weight="700" fill="#1D4ED8">${{h.dt}}</text>`;
                    }}

                    // 3. Data label DU (Hijau): di bawah titik DU
                    if (Math.abs(yDU - yDT) < 14 && Math.abs(yDT - yLU) < 14) {{
                        html += `<text x="${{x + 14}}" y="${{yDU + 12}}" text-anchor="start" font-size="9.5" font-weight="800" fill="#047857">${{h.du}}</text>`;
                    }} else {{
                        html += `<text x="${{x}}" y="${{yDU + 13}}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#047857">${{h.du}}</text>`;
                    }}

                    // 4. Label Tahun X-axis
                    html += `<text x="${{x}}" y="${{H - 10}}" text-anchor="middle" font-size="11" font-weight="800" fill="#0F172A">${{h.tahun}}</text>`;
                }});
                svgLines.innerHTML = html;
            }}

            // 2. Render Modal Right Chart: Bars Kursi Kosong vs Batal DU
            const svgBars = document.getElementById('md-chart-bars');
            if (svgBars) {{
                const W = 420, H = 230, padL = 44, padR = 18, padT = 26, padB = 32;
                const plotW = W - padL - padR, plotH = H - padT - padB;
                const maxB = Math.max(...p.history.map(h => Math.max(h.sisa, h.batal, 0)), 10) * 1.22;

                let html = '';
                for (let i = 0; i <= 4; i++) {{
                    const v = Math.round((maxB / 4) * i);
                    const y = padT + plotH - (i / 4) * plotH;
                    html += `<line x1="${{padL}}" y1="${{y}}" x2="${{W - padR}}" y2="${{y}}" stroke="#E2E8F0" stroke-dasharray="3,3"/>`;
                    html += `<text x="${{padL - 6}}" y="${{y + 4}}" text-anchor="end" font-size="10" fill="#64748B">${{v}}</text>`;
                }}

                const gW = plotW / 5, bW = 16;
                p.history.forEach((h, i) => {{
                    const cx = padL + gW * i + gW / 2;
                    const sVal = Math.max(0, h.sisa);
                    const bVal = Math.max(0, h.batal);
                    const hS = (sVal / maxB) * plotH;
                    const hB = (bVal / maxB) * plotH;
                    const yS = padT + plotH - hS;
                    const yB = padT + plotH - hB;

                    html += `<rect x="${{cx - bW - 1}}" y="${{yS}}" width="${{bW}}" height="${{hS}}" rx="3" fill="#E11D48"><title>${{h.tahun}}: Kursi Kosong = ${{h.sisa}}</title></rect>`;
                    html += `<text x="${{cx - bW/2 - 1}}" y="${{yS - 4}}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#BE123C">${{h.sisa}}</text>`;

                    html += `<rect x="${{cx + 1}}" y="${{yB}}" width="${{bW}}" height="${{hB}}" rx="3" fill="#D97706"><title>${{h.tahun}}: Batal Daftar Ulang = ${{h.batal}}</title></rect>`;
                    html += `<text x="${{cx + bW/2 + 1}}" y="${{yB - 4}}" text-anchor="middle" font-size="9.5" font-weight="800" fill="#B45309">${{h.batal}}</text>`;

                    html += `<text x="${{cx}}" y="${{H - 10}}" text-anchor="middle" font-size="11" font-weight="800" fill="#0F172A">${{h.tahun}}</text>`;
                }});
                svgBars.innerHTML = html;
            }}

            // 3. Render Descending Multi-Year Table (2026 -> 2022 + Total 5 Tahun)
            const tbody = document.getElementById('md-history-tbody');
            tbody.innerHTML = '';
            p.history.slice().reverse().forEach(h => {{
                const pBatal = h.lulus > 0 ? (h.batal / h.lulus * 100).toFixed(1) : '0.0';
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${{h.tahun}}</td>
                    <td>${{h.peminat.toLocaleString('id-ID')}}</td>
                    <td>${{h.dt.toLocaleString('id-ID')}}</td>
                    <td>${{h.lulus.toLocaleString('id-ID')}}</td>
                    <td style="font-weight:700; color:#059669;">${{h.du.toLocaleString('id-ID')}}</td>
                    <td style="font-weight:800; color:#BE123C; background:#FFF1F2;">${{h.sisa.toLocaleString('id-ID')}}</td>
                    <td style="font-weight:700;">${{clampFR(h.fill_rate).toFixed(1)}}%</td>
                    <td style="font-weight:800; color:#B45309; background:#FFFBEB;">${{h.batal.toLocaleString('id-ID')}}</td>
                    <td style="font-weight:700;">${{pBatal}}%</td>
                `;
                tbody.appendChild(tr);
            }});
            const totPem = p.tot_peminat !== undefined ? p.tot_peminat : p.history.reduce((s, h) => s + h.peminat, 0);
            const trTot = document.createElement('tr');
            trTot.className = 'total-row';
            trTot.innerHTML = `
                <td>TOTAL 5 TAHUN</td>
                <td>${{totPem.toLocaleString('id-ID')}}</td>
                <td>${{totDT.toLocaleString('id-ID')}}</td>
                <td>${{totLU.toLocaleString('id-ID')}}</td>
                <td style="color:#6EE7B7;">${{totDU.toLocaleString('id-ID')}}</td>
                <td style="color:#FDA4AF;">${{totSisa.toLocaleString('id-ID')}}</td>
                <td>${{pctFR}}%</td>
                <td style="color:#FDE047;">${{totBatal.toLocaleString('id-ID')}}</td>
                <td>${{pctBatal}}%</td>
            `;
            tbody.appendChild(trTot);

            modal.classList.add('open');
        }}

        function closeProdiModal() {{
            const modal = document.getElementById('prodi-drilldown-modal');
            if (modal) modal.classList.remove('open');
        }}

        document.getElementById('prodi-drilldown-modal')?.addEventListener('click', () => closeProdiModal());
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') closeProdiModal();
        }});

        // View Mode Switching (Matrix vs Trend 81 Prodi)
        function setViewMode(mode) {{
            currentViewMode = mode;
            document.querySelectorAll('.view-mode-btn').forEach(b => {{
                b.classList.toggle('active', b.getAttribute('data-view') === mode);
            }});
            const matrixWrapper = document.getElementById('matrix-view-wrapper');
            const trendWrapper = document.getElementById('trend-view-wrapper');
            const lvlSwitcher = document.getElementById('level-switcher');
            const subSwitcher = document.getElementById('s1-subset-switcher');
            const hdrActions = document.getElementById('matrix-header-actions');

            if (mode === 'trend') {{
                matrixWrapper.style.display = 'none';
                trendWrapper.style.display = 'flex';
                if (lvlSwitcher) lvlSwitcher.style.display = 'none';
                if (subSwitcher) subSwitcher.style.display = 'none';
                if (hdrActions) hdrActions.style.display = 'none';
                document.getElementById('header-main-title').textContent = 'EVALUASI TREN 81 PRODI USK: KURSI KOSONG (DT−DU) & BATAL DAFTAR ULANG (LULUS−DU)';
                renderTrendTable();
            }} else {{
                matrixWrapper.style.display = 'flex';
                trendWrapper.style.display = 'none';
                if (lvlSwitcher) lvlSwitcher.style.display = 'inline-flex';
                if (subSwitcher) subSwitcher.style.display = (currentLevel === 's1') ? 'inline-flex' : 'none';
                if (hdrActions) hdrActions.style.display = 'flex';
                if (currentLevel === 'd3') {{
                    document.getElementById('header-main-title').textContent = 'PETA KUADRAN 11 PROGRAM STUDI D3 VOKASI USK';
                }} else {{
                    document.getElementById('header-main-title').textContent = (currentS1Subset === 'all')
                        ? 'PETA KUADRAN 66 PROGRAM STUDI S1 LENGKAP USK'
                        : 'PETA KUADRAN 60 PROGRAM STUDI S1 KAMPUS UTAMA USK';
                }}
                renderChart();
            }}
        }}

        document.querySelectorAll('.view-mode-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                setViewMode(btn.getAttribute('data-view'));
            }});
        }});

        // Event Listeners for Trend View Controls
        document.querySelectorAll('#trend-klaster-pills .preset-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                trendKlaster = btn.getAttribute('data-klaster');
                document.querySelectorAll('#trend-klaster-pills .preset-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderTrendTable();
            }});
        }});

        document.querySelectorAll('#trend-sort-presets .preset-btn').forEach(btn => {{
            btn.addEventListener('click', () => {{
                trendSort = btn.getAttribute('data-sort');
                document.querySelectorAll('#trend-sort-presets .preset-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                renderTrendTable();
            }});
        }});

        document.getElementById('trend-fak-select')?.addEventListener('change', (e) => {{
            trendFak = e.target.value;
            renderTrendTable();
        }});

        document.getElementById('trend-quad-select')?.addEventListener('change', (e) => {{
            trendQuad = e.target.value;
            renderTrendTable();
        }});

        document.getElementById('trend-search-input')?.addEventListener('input', (e) => {{
            trendSearch = e.target.value;
            renderTrendTable();
        }});

        // Initial Load
        initTrendFakOptions();
        const subsetSwitcher = document.getElementById('s1-subset-switcher');
        if (currentLevel === 'd3') {{
            document.querySelectorAll('.level-tab').forEach(t => {{
                t.classList.toggle('active', t.getAttribute('data-level') === 'd3');
            }});
            document.getElementById('header-main-title').textContent = 'PETA KUADRAN 11 PROGRAM STUDI D3 VOKASI USK';
            document.getElementById('chart-sub-heading').textContent = 'Matriks 4 Kuadran Interaktif (11 Prodi D3 Vokasi)';
            document.getElementById('footer-standards').innerHTML = 'Standar Evaluasi D3: <strong>Keketatan 4,0 : 1</strong> | <strong>Standar Ideal 80%</strong> | <strong>Batas Kritis 50%</strong>';
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

        if (currentViewMode === 'trend') {{
            setViewMode('trend');
        }}

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
            if (h.includes('tren')) {{
                setViewMode('trend');
                return;
            }}
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
