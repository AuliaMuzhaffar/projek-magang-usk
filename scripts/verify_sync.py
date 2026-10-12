"""
verify_sync.py
=============================================================================
AUDIT & VERIFIKASI KESEHATAN SINKRONISASI REPO (1 DETIK)
=============================================================================
Script ini memeriksa secara instan apakah file grafik (.png) dan dashboard (.html)
sudah mencerminkan data terbaru dari file Excel Master, atau masih tertinggal.
Jalankan kapan saja dengan:
    python3 scripts/verify_sync.py
"""

import os
import sys
import time
from datetime import datetime

# Impor konfigurasi inti
sys.path.insert(0, os.path.dirname(__file__))
from core_data import (
    MASTER_EXCEL_PATH, GRAFIK_DIR, INTERACTIVE_HTML_PATH, REKAP_SELISIH_PATH,
    load_s1_master, get_quadrant_summary, PRODI_BARU_LIST
)

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

def main():
    print("=" * 70)
    print(" 🔍 USK DATA REPO: AUDIT & HEALTH CHECK SINKRONISASI")
    print("=" * 70)

    # 1. Periksa Keberadaan File Master
    if not os.path.exists(MASTER_EXCEL_PATH):
        print(f"❌ ERROR: File master Excel tidak ditemukan:\n   {MASTER_EXCEL_PATH}")
        sys.exit(1)

    from core_data import RAW_EXCEL_PATH

    master_mtime = os.path.getmtime(MASTER_EXCEL_PATH)
    print(f"📁 Master Excel    : {os.path.basename(MASTER_EXCEL_PATH)}")
    print(f"   Terakhir Diubah : {format_timestamp(master_mtime)}")

    if os.path.exists(RAW_EXCEL_PATH):
        raw_mtime = os.path.getmtime(RAW_EXCEL_PATH)
        print(f"📄 Raw Data Excel  : {os.path.basename(RAW_EXCEL_PATH)}")
        print(f"   Terakhir Diubah : {format_timestamp(raw_mtime)}")
        if raw_mtime > master_mtime:
            print("   ⚠️  [STATUS] Raw Data telah diedit setelah Master dibuat! (Perlu sync master)")
        else:
            print("   ✅ [STATUS] Master Excel tersinkron dengan Raw Data.")
    print("-" * 70)

    # 2. Periksa Distribusi Data Master
    try:
        df_s1 = load_s1_master()
        summary_all = get_quadrant_summary(df_s1)
        df_60 = df_s1[~df_s1['Is_Prodi_Baru']]
        summary_60 = get_quadrant_summary(df_60)

        print(f"📊 Metrik Terkini Database Master:")
        print(f"   • Total S1 Kampus Utama : {len(df_s1)} Program Studi")
        print(f"   • Kuadran 66 Prodi      : Q1={summary_all['Q1']['count']} ({summary_all['Q1']['percent']:.1f}%), "
              f"Q2={summary_all['Q2']['count']} ({summary_all['Q2']['percent']:.1f}%), "
              f"Q3={summary_all['Q3']['count']} ({summary_all['Q3']['percent']:.1f}%), "
              f"Q4={summary_all['Q4']['count']} ({summary_all['Q4']['percent']:.1f}%)")
        print(f"   • Kuadran 60 Prodi Mapan: Q1={summary_60['Q1']['count']} ({summary_60['Q1']['percent']:.1f}%), "
              f"Q2={summary_60['Q2']['count']} ({summary_60['Q2']['percent']:.1f}%), "
              f"Q3={summary_60['Q3']['count']} ({summary_60['Q3']['percent']:.1f}%), "
              f"Q4={summary_60['Q4']['count']} ({summary_60['Q4']['percent']:.1f}%)")
    except Exception as e:
        print(f"❌ Gagal membaca atau memproses data master: {e}")
        sys.exit(1)

    print("-" * 70)
    print("🕒 Audit Status Timestamp Artefak Output:")

    artifacts = [
        ("Grafik Matriks All Labels", os.path.join(GRAFIK_DIR, "13_matriks_4_kuadran_5_tahun_2022_2026_all_labels.png")),
        ("Grafik Matriks 60 Prodi Mapan", os.path.join(GRAFIK_DIR, "13_matriks_4_kuadran_5_tahun_2022_2026_tanpa_prodi_baru.png")),
        ("Grafik Slide 2 Direktori Roster", os.path.join(GRAFIK_DIR, "13_companion_direktori_66_prodi_4_kuadran.png")),
        ("Grafik Matriks 5 Tahun Standar", os.path.join(GRAFIK_DIR, "13_matriks_4_kuadran_5_tahun_2022_2026.png")),
        ("Rekap Selisih Lulus vs DU (Excel)", REKAP_SELISIH_PATH),
        ("Dashboard HTML Interaktif", INTERACTIVE_HTML_PATH)
    ]

    all_synced = True
    for label, path in artifacts:
        if not os.path.exists(path):
            print(f"   ❌ [MISSING]      {label}")
            print(f"      File belum ada di: {path}")
            all_synced = False
            continue

        art_mtime = os.path.getmtime(path)
        time_diff = art_mtime - master_mtime

        # Jika artefak lebih tua dari master (dengan toleransi 1 detik)
        if time_diff < -1.0:
            print(f"   ⚠️  [OUT-OF-SYNC]  {label}")
            print(f"      Dibuat: {format_timestamp(art_mtime)} (Lebih tua dari Master Excel)")
            all_synced = False
        else:
            print(f"   ✅ [SYNCED]       {label}")
            print(f"      Dibuat: {format_timestamp(art_mtime)} (Tersinkron)")

    print("=" * 70)
    if all_synced:
        print("🎉 STATUS: SEMUA ARTEFAK TERSINKRONISASI 100% DENGAN MASTER DATA!")
        print("   Tidak ada pekerjaan ganda yang perlu dilakukan.")
    else:
        print("🚨 PERINGATAN: DITEMUKAN ARTEFAK YANG BELUM TERSINKRON!")
        print("   Silakan jalankan script pipeline berikut untuk memperbarui seluruh file:")
        print("   👉 python3 scripts/build_all.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
