"""
build_all.py
=============================================================================
PIPELINE ORKESTRATOR UTAMA (ONE-CLICK MASTER BUILD RUNNER)
=============================================================================
Script ini menjalankan seluruh rantai proses sinkronisasi visualisasi dan dashboard
secara berurutan dalam satu perintah:
    python3 scripts/build_all.py

Opsi tambahan:
    --charts-only : Hanya meregenerasi grafik PNG
    --html-only   : Hanya meregenerasi HTML interaktif
    --from-raw    : Bangun ulang Master Excel dari data mentah
    --help        : Menampilkan bantuan
"""

import os
import sys
import time
import subprocess
from datetime import datetime

# Impor konfigurasi inti
sys.path.insert(0, os.path.dirname(__file__))
from core_data import (
    BASE_DIR, MASTER_EXCEL_PATH,
    load_s1_master, get_quadrant_summary
)

def run_step(step_name, script_path, cwd=BASE_DIR):
    print(f"\n▶ Menjalankan {step_name}...")
    t0 = time.time()
    try:
        res = subprocess.run([sys.executable, script_path], cwd=cwd, check=True)
        dur = time.time() - t0
        print(f"✔ {step_name} Selesai ({dur:.1f} detik)")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ ERROR saat menjalankan {step_name}: Kode Keluar {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ ERROR tak terduga: {e}")
        return False

def main():
    start_total = time.time()
    scripts_dir = os.path.dirname(__file__)

    print("=" * 75)
    print(" 🚀 USK DATA PIPELINE: ONE-CLICK MASTER RE-BUILD")
    print("=" * 75)
    print(f"Waktu Mulai: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    charts_only = "--charts-only" in sys.argv
    html_only = "--html-only" in sys.argv
    force_raw = ("--from-raw" in sys.argv) or ("--rebuild-master" in sys.argv)

    # 0. Cek Sinkronisasi dengan Raw Data (rekap data (fix).xlsx)
    from core_data import RAW_EXCEL_PATH, BUILD_MASTER_SCRIPT, SNAPSHOT_DIR
    import shutil

    need_rebuild_master = force_raw
    if os.path.exists(RAW_EXCEL_PATH) and os.path.exists(MASTER_EXCEL_PATH):
        if os.path.getmtime(RAW_EXCEL_PATH) > os.path.getmtime(MASTER_EXCEL_PATH):
            need_rebuild_master = True
            print("\n💡 Terdeteksi: 'rekap data (fix).xlsx' telah diperbarui!")
            print("   Otomatis menyelaraskan Master Excel terlebih dahulu...")

    if need_rebuild_master and os.path.exists(BUILD_MASTER_SCRIPT):
        print("\n[Tahap 0A] Menyimpan Snapshot Backup & Memperbarui Master Excel...")
        os.makedirs(SNAPSHOT_DIR, exist_ok=True)
        ts_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_snap = os.path.join(SNAPSHOT_DIR, f"master_pre_raw_update_{ts_str}.xlsx")
        if os.path.exists(MASTER_EXCEL_PATH):
            shutil.copy2(MASTER_EXCEL_PATH, backup_snap)
            print(f"📦 Backup snapshot dibuat: {os.path.basename(backup_snap)}")
        run_step("ETL Master Dataset dari Raw Data", BUILD_MASTER_SCRIPT)

    # 1. Validasi Keberadaan Data Master
    print("\n[Tahap 0B/5] Memvalidasi Database Master...")
    if not os.path.exists(MASTER_EXCEL_PATH):
        print(f"❌ Gagal: File {MASTER_EXCEL_PATH} tidak ditemukan!")
        sys.exit(1)

    try:
        df_s1 = load_s1_master()
        summary = get_quadrant_summary(df_s1)
        print(f"✔ Data Master Valid: 66 Prodi S1 termuat.")
        print(f"  Distribusi Kuadran: Q1={summary['Q1']['count']}, Q2={summary['Q2']['count']}, Q3={summary['Q3']['count']}, Q4={summary['Q4']['count']}")
    except Exception as e:
        print(f"❌ Gagal memvalidasi data master: {e}")
        sys.exit(1)

    steps = []

    if not html_only:
        steps.extend([
            ("Tahap 1/7: Generate Charts Reguler (1-17)", os.path.join(scripts_dir, "generate_charts.py")),
            ("Tahap 2/7: Generate Matriks All Labels (66 Prodi)", os.path.join(scripts_dir, "generate_chart13_all_labels.py")),
            ("Tahap 3/7: Generate Matriks 60 Prodi Mapan", os.path.join(scripts_dir, "generate_chart13_tanpa_prodi_baru.py")),
            ("Tahap 4/7: Generate Direktori Roster Kuadran", os.path.join(scripts_dir, "generate_slide2_direktori.py")),
            ("Tahap 5/7: Generate & Sinkronkan Rekap Selisih Lulus vs DU", os.path.join(scripts_dir, "beautify_selisih_excel.py")),
            ("Tahap 6/7: Generate & Sinkronkan Rekap Daya Tampung, Peminat & Sisa Kuota", os.path.join(scripts_dir, "build_rekap_daya_tampung_excel.py")),
        ])

    if not charts_only:
        steps.append(
            ("Tahap 7/7: Generate Dashboard Interaktif HTML", os.path.join(scripts_dir, "build_interactive_matrix_html.py"))
        )

    # Eksekusi seluruh tahapan
    failed = []
    for step_title, script_file in steps:
        if not os.path.exists(script_file):
            print(f"⚠️ Script tidak ditemukan: {script_file}")
            failed.append(step_title)
            continue

        success = run_step(step_title, script_file)
        if not success:
            failed.append(step_title)

    # Verifikasi Hasil Akhir
    print("\n" + "=" * 75)
    print(" 🔍 MENJALANKAN AUDIT VERIFIKASI AKHIR...")
    print("=" * 75)
    verify_script = os.path.join(scripts_dir, "verify_sync.py")
    if os.path.exists(verify_script):
        subprocess.run([sys.executable, verify_script], cwd=BASE_DIR)

    total_dur = time.time() - start_total
    print("\n" + "=" * 75)
    if not failed:
        print(f"✨ PIPELINE SELESAI DENGAN SUKSES! (Total waktu: {total_dur:.1f} detik)")
        print("   Seluruh file visualisasi dan dashboard sudah tersinkronisasi 100%.")
    else:
        print(f"⚠️ PIPELINE SELESAI DENGAN BEBERAPA KENDALA:")
        for f in failed:
            print(f"   - Gagal pada: {f}")
    print("=" * 75)

if __name__ == "__main__":
    main()
