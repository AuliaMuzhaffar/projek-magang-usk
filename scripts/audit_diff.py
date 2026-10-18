"""
audit_diff.py
=============================================================================
INSPEKTUR PERBEDAAN CELL-BY-CELL EXCEL MASTER
=============================================================================
Script ini membandingkan file master Excel dengan file versi lama (snapshot/backup)
untuk mendeteksi sel mana saja yang diubah, apa nilai lamanya, apa nilai barunya,
dan prodi mana saja yang kuadrannya bergeser.

Penggunaan:
    # Bandingkan master aktif dengan snapshot terbaru di data/snapshots/
    python3 scripts/audit_diff.py

    # Bandingkan dua file spesifik:
    python3 scripts/audit_diff.py file_lama.xlsx file_baru.xlsx
"""

import os
import sys
import glob
import sys, os
libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "libs"))
if os.path.exists(libs_dir) and libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import pandas as pd
import numpy as np

# Impor konfigurasi inti
sys.path.insert(0, os.path.dirname(__file__))
from core_data import MASTER_EXCEL_PATH, SNAPSHOT_DIR

def compare_sheets(df_old, df_new, sheet_name, key_col="Nama Program Studi"):
    diffs = []
    
    if key_col not in df_old.columns or key_col not in df_new.columns:
        print(f"⚠️ Kolom kunci '{key_col}' tidak ditemukan di sheet {sheet_name}.")
        return diffs

    # Filter prodi yang ada di kedua sheet
    prodis = set(df_old[key_col].dropna().unique()).union(set(df_new[key_col].dropna().unique()))
    
    common_cols = [c for c in df_old.columns if c in df_new.columns and c != key_col]

    for p in sorted(prodis):
        row_old = df_old[df_old[key_col] == p]
        row_new = df_new[df_new[key_col] == p]

        if row_old.empty:
            diffs.append({'Prodi': p, 'Kolom': '[STATUS]', 'Nilai_Lama': 'TIDAK ADA', 'Nilai_Baru': 'BARU DITAMBAHKAN'})
            continue
        if row_new.empty:
            diffs.append({'Prodi': p, 'Kolom': '[STATUS]', 'Nilai_Lama': 'ADA', 'Nilai_Baru': 'DIHAPUS'})
            continue

        for col in common_cols:
            v_old = row_old[col].values[0]
            v_new = row_new[col].values[0]

            # Normalisasi NaN / None
            if pd.isna(v_old) and pd.isna(v_new):
                continue
            
            # Bandingkan jika berbeda
            if v_old != v_new:
                # Toleransi floating point kecil
                try:
                    if abs(float(v_old) - float(v_new)) < 1e-4:
                        continue
                except (ValueError, TypeError):
                    pass

                diffs.append({
                    'Prodi': p,
                    'Kolom': col,
                    'Nilai_Lama': v_old,
                    'Nilai_Baru': v_new
                })

    return diffs

def main():
    print("=" * 75)
    print(" 🔎 AUDIT PERUBAHAN DATA: CELL-BY-CELL COMPARATOR")
    print("=" * 75)

    if len(sys.argv) >= 3:
        file_old = sys.argv[1]
        file_new = sys.argv[2]
    else:
        # Default: bandingkan file master aktif dengan snapshot di data/snapshots/
        snapshots = sorted(glob.glob(os.path.join(SNAPSHOT_DIR, "*.xlsx")))
        if not snapshots:
            print(f"⚠️ Belum ada file snapshot di {SNAPSHOT_DIR}.")
            print(f"   Silakan tentukan file yang ingin dibandingkan:")
            print(f"   python3 audit_diff.py <file_lama.xlsx> <file_baru.xlsx>")
            sys.exit(1)
        
        file_old = snapshots[-1] # Snapshot terbaru
        file_new = MASTER_EXCEL_PATH

    print(f"File 1 (Lama/Baseline): {os.path.basename(file_old)}")
    print(f"File 2 (Baru/Terkini) : {os.path.basename(file_new)}")
    print("-" * 75)

    xl_old = pd.ExcelFile(file_old)
    xl_new = pd.ExcelFile(file_new)

    target_sheet = "S1_Kampus_Utama"
    if target_sheet not in xl_old.sheet_names or target_sheet not in xl_new.sheet_names:
        target_sheet = xl_old.sheet_names[0]

    df_old = xl_old.parse(target_sheet)
    df_new = xl_new.parse(target_sheet)

    diffs = compare_sheets(df_old, df_new, target_sheet)

    if not diffs:
        print(f"✔ Tidak ada perbedaan nilai sel antara kedua file pada sheet '{target_sheet}'.")
        print("=" * 75)
        return

    print(f"🚨 Ditemukan {len(diffs)} sel dengan perbedaan nilai pada sheet '{target_sheet}':\n")
    print(f"{'PROGRAM STUDI':<35} | {'KOLOM':<25} | {'NILAI LAMA':<15} -> {'NILAI BARU'}")
    print("-" * 105)
    for d in diffs:
        v_old_str = f"{d['Nilai_Lama']:.2f}" if isinstance(d['Nilai_Lama'], (int, float)) else str(d['Nilai_Lama'])
        v_new_str = f"{d['Nilai_Baru']:.2f}" if isinstance(d['Nilai_Baru'], (int, float)) else str(d['Nilai_Baru'])
        print(f"{d['Prodi'][:35]:<35} | {d['Kolom'][:25]:<25} | {v_old_str:<15} -> {v_new_str}")

    print("=" * 105)

if __name__ == "__main__":
    main()
