"""
core_data.py
=============================================================================
MODUL SENTRAL KONFIGURASI & LOGIKA DATA (SINGLE SOURCE OF TRUTH)
=============================================================================
File ini adalah modul sentral untuk seluruh parameter, ambang batas kuadran,
pemetaan singkatan nama, serta pemuatan data master.
Seluruh script visualisasi, HTML, dan reporting mengimpor konstanta dan fungsi
dari modul ini agar semua file di repositori selalu konsisten secara otomatis.
"""

import os
import sys

# Ensure local dependencies in scripts/libs are accessible in sandbox
libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "libs"))
if os.path.exists(libs_dir) and libs_dir not in sys.path:
    sys.path.insert(0, libs_dir)

import warnings
import pandas as pd
import numpy as np

# Suppress pandas 3.0 Copy-on-Write FutureWarnings
warnings.filterwarnings('ignore', category=FutureWarning)

# ---------------------------------------------------------------------------
# 1. PATH DIREKTORI & FILE UTAMA (STRUKTUR MODULAR REPO)
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_MASTER_DIR = os.path.join(DATA_DIR, "master")
DATA_PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
SNAPSHOT_DIR = os.path.join(DATA_DIR, "snapshots")
REFERENCE_SK_DIR = os.path.join(DATA_DIR, "reference_sk")
DOCS_DIR = os.path.join(BASE_DIR, "docs")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
GRAFIK_DIR = os.path.join(OUTPUT_DIR, "grafik")
DASHBOARD_DIR = os.path.join(OUTPUT_DIR, "dashboard")
PRESENTASI_DIR = os.path.join(OUTPUT_DIR, "presentasi")

MASTER_EXCEL_PATH = os.path.join(DATA_MASTER_DIR, "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
RAW_EXCEL_PATH = os.path.join(DATA_RAW_DIR, "rekap data (fix).xlsx")
REKAP_SELISIH_PATH = os.path.join(DATA_PROCESSED_DIR, "rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx")
REKAP_DAYA_TAMPUNG_PATH = os.path.join(DATA_PROCESSED_DIR, "rekap_daya_tampung_peminat_dan_sisa_kuota_2022_2026.xlsx")
INTERACTIVE_HTML_PATH = os.path.join(DASHBOARD_DIR, "matriks_interaktif_kuadran_usk.html")
BUILD_MASTER_SCRIPT = os.path.join(os.path.dirname(__file__), "build_master_dataset.py")
BEAUTIFY_SELISIH_SCRIPT = os.path.join(os.path.dirname(__file__), "beautify_selisih_excel.py")
BUILD_REKAP_DT_SCRIPT = os.path.join(os.path.dirname(__file__), "build_rekap_daya_tampung_excel.py")

# ---------------------------------------------------------------------------
# 2. PARAMETER STANDAR & AMBANG BATAS KUADRAN (BENCHMARK)
# ---------------------------------------------------------------------------
KEKETATAN_BENCHMARK = 4.0      # Rasio Peminat per 1 Kursi Daya Tampung (>= 4.0 = Ketat)
FILLRATE_BENCHMARK = 80.0      # Persentase Keterisian Kuota (>= 80% = Ideal/Optimal)

# Daftar 6 Program Studi Baru (Data Terbatas < 5 Tahun Penuh)
PRODI_BARU_LIST = [
    "BISNIS DIGITAL",
    "HUBUNGAN INTERNASIONAL",
    "TEKNIK LINGKUNGAN",
    "TEKNIK PERMINYAKAN",
    "TEKNIK SUMBER DAYA AIR",
    "TEKNOLOGI INDUSTRI HASIL PERIKANAN"
]

# ---------------------------------------------------------------------------
# 3. SINGKATAN STANDAR FAKULTAS & NAMA PROGRAM STUDI
# ---------------------------------------------------------------------------
FAKULTAS_ABBR = {
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

PRODI_SHORT_NAMES = {
    'PENDIDIKAN PANCASILA DAN KEWARGANEGARAAN': 'PPKn',
    'PENDIDIKAN KESEJAHTERAAN KELUARGA': 'PKK',
    'PENDIDIKAN SENI DRAMA TARI DAN MUSIK': 'Sendratasik',
    'PENDIDIKAN JASMANI KESEHATAN DAN REKREASI': 'Penjaskesrek',
    'PERENCANAAN WILAYAH DAN KOTA': 'PWK',
    'TEKNOLOGI INDUSTRI HASIL PERIKANAN': 'TIHP',
    'PEMANFAATAN SUMBERDAYA PERIKANAN': 'PSP',
    'PENDIDIKAN GURU SEKOLAH DASAR': 'PGSD',
    'PENDIDIKAN GURU PENDIDIKAN ANAK USIA DINI': 'PAUD',
    'PENDIDIKAN GURU PAUD': 'PAUD',
    'TEKNIK SUMBER DAYA AIR': 'TSDA',
    'TEKNOLOGI HASIL PERTANIAN': 'THP',
    'PENDIDIKAN DOKTER HEWAN': 'Dokter Hewan',
    'PENDIDIKAN BAHASA INGGRIS': 'Bhs Inggris',
    'PENDIDIKAN BAHASA INDONESIA': 'Bhs Indonesia',
    'PENDIDIKAN DOKTER GIGI': 'Dokter Gigi',
    'PENDIDIKAN DOKTER': 'Dokter',
    'BIMBINGAN KONSELING': 'Bimb. Konseling',
    'EKONOMI PEMBANGUNAN': 'Ek. Pembangunan',
    'PENDIDIKAN MATEMATIKA': 'Pend. Mat.',
    'PENDIDIKAN GEOGRAFI': 'Pend. Geografi',
    'PENDIDIKAN EKONOMI': 'Pend. Ekonomi',
    'PENDIDIKAN KIMIA': 'Pend. Kimia',
    'PENDIDIKAN FISIKA': 'Pend. Fisika',
    'PENDIDIKAN BIOLOGI': 'Pend. Biologi',
    'PENDIDIKAN SEJARAH': 'Pend. Sejarah'
}

# Singkatan Nama Prodi Khusus Dashboard HTML Interaktif (Lebih Deskriptif untuk Layar)
PRODI_HTML_SHORT_NAMES = {
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
    # D3 Vokasi
    'KESEHATAN HEWAN': 'Kesehatan Hewan',
    'MANAJEMEN AGRIBISNIS': 'Manaj. Agribisnis',
    'TEKNIK LISTRIK': 'Tek. Listrik',
    'BUDIDAYA PETERNAKAN': 'Budidaya Peternakan',
    'MANAJEMEN PERUSAHAAN': 'Manaj. Perusahaan',
    'KEUANGAN DAN PERBANKAN': 'Keuangan & Perbankan',
    'MANAJEMEN INFORMATIKA': 'Manaj. Informatika',
    'SEKRETARI': 'Sekretari'
}

# ---------------------------------------------------------------------------
# 4. FUNGSI KLASIFIKASI KUADRAN
# ---------------------------------------------------------------------------
def classify_kuadran(keketatan: float, fill_rate: float):
    """
    Menentukan kuadran berdasarkan ambang batas resmi.
    Returns: (code, label, strategy_title, color_hex)
    """
    if keketatan >= KEKETATAN_BENCHMARK and fill_rate >= FILLRATE_BENCHMARK:
        return ("Q1", "Kuadran I (Unggulan)", "UNGGULAN: Pertahankan Mutu & Kuota", "#059669")
    elif keketatan < KEKETATAN_BENCHMARK and fill_rate >= FILLRATE_BENCHMARK:
        return ("Q2", "Kuadran II (Stabil)", "STABIL: Lindungi & Pertahankan Kapasitas", "#2563EB")
    elif keketatan >= KEKETATAN_BENCHMARK and fill_rate < FILLRATE_BENCHMARK:
        return ("Q3", "Kuadran III (Belum Optimal)", "BELUM OPTIMAL: Fasilitasi IPI & Percepat Cadangan", "#D97706")
    else:
        return ("Q4", "Kuadran IV (Perlu Ditingkatkan)", "PERLU DITINGKATKAN: Wajib Pangkas Kuota SPMB", "#E11D48")

# ---------------------------------------------------------------------------
# 5. FUNGSI LOADER SENTRAL DATA S1 KAMPUS UTAMA
# ---------------------------------------------------------------------------
def load_s1_master(excel_path=None):
    """
    Membaca sheet S1_Kampus_Utama dari master Excel, menstandarkan kolom,
    dan menghitung atribut turunan secara otomatis.
    """
    if excel_path is None:
        excel_path = MASTER_EXCEL_PATH

    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"File master data tidak ditemukan di: {excel_path}")

    df = pd.read_excel(excel_path, sheet_name="S1_Kampus_Utama").copy()

    # Standardisasi kolom
    rename_cols = {
        'Nama Program Studi': 'Prodi',
        'Fakultas': 'Fakultas',
        'Rata Keketatan 5-Thn': 'Keketatan',
        'Rata Fill Rate 5-Thn (%)': 'FillRate',
        'Rata DT 5-Thn': 'DT',
        'Rata DU 5-Thn': 'DU',
        'Rata Peminat 5-Thn': 'Peminat'
    }
    df = df.rename(columns=rename_cols).copy()

    # Singkatan Fakultas dan Label Prodi Pendek
    df['Fak_Abbr'] = df['Fakultas'].map(FAKULTAS_ABBR).fillna(df['Fakultas'])
    df['Prodi_Short'] = df['Prodi'].apply(lambda x: PRODI_SHORT_NAMES.get(str(x).strip(), str(x).title()))
    df['Label_Lengkap'] = df.apply(lambda r: f"{r['Prodi_Short']} ({r['Fak_Abbr']})", axis=1)

    # Identifikasi Prodi Baru
    df['Is_Prodi_Baru'] = df['Prodi'].str.strip().str.upper().isin([p.upper() for p in PRODI_BARU_LIST])

    # Hitung Kuadran Dinamis
    kuadran_results = df.apply(lambda r: classify_kuadran(r['Keketatan'], r['FillRate']), axis=1)
    df['Kuadran_Code'] = [k[0] for k in kuadran_results]
    df['Kuadran_Label'] = [k[1] for k in kuadran_results]
    df['Kuadran_Strategi'] = [k[2] for k in kuadran_results]
    df['Kuadran_Color'] = [k[3] for k in kuadran_results]

    return df

# ---------------------------------------------------------------------------
# 6. RINGKASAN STATISTIK DISTRIBUSI KUADRAN
# ---------------------------------------------------------------------------
def get_quadrant_summary(df):
    """
    Menghitung jumlah dan persentase program studi per kuadran.
    """
    n_total = len(df)
    summary = {}
    for code in ['Q1', 'Q2', 'Q3', 'Q4']:
        sub = df[df['Kuadran_Code'] == code]
        count = len(sub)
        pct = (count / n_total * 100.0) if n_total > 0 else 0.0
        summary[code] = {
            'count': count,
            'percent': pct,
            'prodi_list': sub['Prodi'].tolist()
        }
    return summary
