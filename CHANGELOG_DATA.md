# 📜 Jurnal Log Perubahan Data & Repositori (CHANGELOG_DATA)
**Repositori Analisis Peminatan, Daya Tampung, dan Jalur Masuk USK (2022–2026)**

Dokumen ini mencatat setiap kronologi perubahan data master, penyesuaian angka historis, re-kalkulasi metrik strategis, serta pembaruan arsitektur repositori agar riwayat perubahan selalu transparan, dapat dilacak (*auditable*), dan mudah di-*rollback*.

---

## [2026-10-12 16:40] - Penyelarasan Penuh Rekap Selisih Lulus vs DU & Integrasi Pipeline Otomatis
- **Inisiator/Konteks:** Menyelaraskan seluruh 1.215 sel data pada `data/processed/rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx` dengan Database Master resmi (`Master_Semua_Prodi`) dan mengintegrasikannya ke dalam pipeline workflow otomatis (`scripts/build_all.py` dan `scripts/verify_sync.py`).
- **Tindakan & Penyesuaian Data:**
  1. **Audit & Penyelarasan 100% Identik:**
     - Menghilangkan seluruh 43 titik ketidaksesuaian (selisih) dari versi lama.
     - Perbaikan anomali nilai minus gugur pada prodi baru 2025, angka Teknik Lingkungan 2023 (0), angka Teknik Perminyakan 2025 (DT: 120, DU: 120), serta cadangan D3 & PSDKU 2026.
     - Formula gugur pada sheet `Rincian_Per_Prodi` distandardisasi menjadi `=MAX(0, Lulus - DU)`.
  2. **Dashboard Eksekutif Dinamis (Formula Live):**
     - Seluruh KPI Card di sheet `Ringkasan_Eksekutif` (Total Kelulusan, Total Registrasi & Yield Rate, Kursi Hangus, Potensi Kerugian UKT) kini menggunakan formula Excel dinamis yang terhubung langsung ke baris Grand Total sheet Rincian.
     - Tabel Tren Tahunan dan Tabel Distribusi Fakultas menggunakan formula `=SUMIF` dan `=COUNTIF` dinamis.
  3. **Integrasi ke Master Pipeline & Tooling:**
     - `scripts/core_data.py`: Ditambahkan path konstanta `REKAP_SELISIH_PATH` dan `BEAUTIFY_SELISIH_SCRIPT`.
     - `scripts/build_all.py`: Dimasukkan sebagai Tahap 5/6 sehingga otomatis di-generate dan diselaraskan setiap kali build berjalan.
     - `scripts/verify_sync.py`: Ditambahkan verifikasi timestamp file rekapitulasi selisih (Audit 1 detik: `✅ [SYNCED] 100%`).
- **Hasil Audit Verifikasi:** 81 Program Studi x 15 Kolom = 1.215 Sel diuji secara cell-by-cell. Total selisih: **0 (100% Sempurna & Identik)**.

---
- **Inisiator/Konteks:** Merapikan repositori yang sebelumnya memiliki direktori bertingkat berulang (`tugas-5/analisa_peminatan_dan_daya_tampung/`) dan file-file yang tersebar di root menjadi struktur modular standar industri kelas dunia.
- **Tindakan & Pengelompokan Berkas:**
  1. `data/`:
     - `raw/`: Seluruh data masukan mentah (`rekap data (fix).xlsx`, `DATA_KIP_*.xlsx`).
     - `master/`: Berkas tunggal Single Source of Truth (`master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`).
     - `processed/`: Dataset terdisagregasi per jalur dan rekap selisih kuota.
     - `snapshots/`: Salinan cadangan historis bertanggal.
     - `reference_sk/`: Surat Keputusan Rektor & dokumen legalitas PMB/UKT.
  2. `scripts/`: Seluruh script modul data science, pipeline runner, auditor diff, dan generator grafis.
  3. `docs/`: Seluruh 19 dokumen kajian akademik dan laporan eksekutif markdown.
  4. `output/`: Folder terpusat untuk seluruh artefak siap pakai (`grafik/`, `dashboard/`, `presentasi/`).
  5. `assets/`: Aset visual resmi USK (`logos/`).
  6. Root Directory: `README.md`, `PANDUAN_ARSITEKTUR_DAN_WORKFLOW.md`, `DATA_DICTIONARY.md`, `CHANGELOG_DATA.md`, dan `.gitignore`.
- **Hasil Pengujian Pipeline:**
  - `python3 scripts/verify_sync.py`: Status 100% SYNCED.
  - `python3 scripts/build_all.py`: Lolos seluruh tahap 1–5 tanpa kesalahan.
  - Seluruh script pelengkap (jalur masuk, KIP, D3 vokasi, slide generator) lolos uji eksekusi.

---

## [2026-10-12 11:20] - Pembentukan Arsitektur Sinkronisasi Terpusat & Audit Tooling
- **Inisiator/Konteks:** Standardisasi arsitektur repositori untuk mencegah kerja ganda (*DRY principle*) dan memastikan seluruh visualisasi tersinkronisasi 100%.
- **File Baru:**
  1. `scripts/core_data.py`: Modul parameter sentral (ambang batas 4.0x dan 80%, kamus singkatan nama).
  2. `scripts/build_all.py`: Pipeline runner *one-click* untuk meregenerasi seluruh grafik dan dashboard.
  3. `scripts/verify_sync.py`: Tool verifikasi status sinkronisasi repo dalam 1 detik.
  4. `scripts/audit_diff.py`: Tool pembanding perbedaan cell-by-cell file Excel master vs snapshot.
  5. `data/snapshots/`: Direktori penyimpanan snapshot bertanggal.
- **Hasil Audit Status:** Seluruh grafik PNG dan dashboard HTML terverifikasi tersinkronisasi penuh dengan Master Excel (`2026-10-12 11:21`).

---

## [2026-10-09 19:56] - Penyelarasan Kolom Kuadran Master & Koreksi Data Riwayat Resmi
- **File Terdampak:** `data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`
- **Sheet:** `S1_Kampus_Utama`, `Master_Semua_Prodi`
- **Rincian Perubahan:**
  1. **TEKNIK LINGKUNGAN:**
     - Data 2023 dinolkan (`Peminat: 0, DT: 0, DU: 0, Lulus: 0, Gugur: 0`).
     - *Alasan:* Sesuai data resmi universitas, mahasiswa baru Teknik Lingkungan baru aktif diterima pada tahun 2025 dan 2026.
     - *Dampak Metrik:* Rata-rata Keketatan aktif = 4,60x, Rata-rata Fill Rate aktif = 65,6%.
     - *Pergeseran Kuadran:* Berpindah dari **Kuadran I** ke **Kuadran III (Belum Optimal)**.
  2. **TEKNIK PERMINYAKAN:**
     - Data 2025 disesuaikan: Daya Tampung = 120 dan Daftar Ulang = 120 (dari sebelumnya DT: 80, DU: 48).
     - *Alasan:* Realisasi kuota mandiri dan penerimaan mahasiswa baru angkatan pertama berkapasitas penuh 120 kursi.
     - *Dampak Metrik:* Rata-rata Keketatan aktif = 4,47x, Rata-rata Fill Rate aktif = 71,6%.
     - *Status Kuadran:* Tetap di **Kuadran III (Belum Optimal)** dengan titik koordinat terbarui.
  3. **Penambahan Kolom Kuadran Resmi di Master:**
     - Menambahkan kolom `Kuadran 2026` dan `Kuadran 5-Tahun` secara terpisah di sheet master.
     - Mengakhiri ketidaksesuaian kolom lama dengan dashboard interaktif HTML.
- **Snapshot Terkait:** `data/snapshots/master_20261009_v2_revisi_perminyakan_lingkungan.xlsx`

---

## [2026-10-09 11:45] - Rekonsiliasi Daya Tampung 2026 Sesuai SK Rektor No. 121/UN11/KPT/2026
- **Sumber Data:** Dokumen resmi `data/reference_sk/121UN11KPT2026 SK Daya Tampung AWAL 2026-2027  tte KIRIM SNPMB PUSAT (1).pdf`
- **Temuan & Tindakan:**
  - Audit perbandingan antara file rekap awal vs SK Rektor menunjukkan bahwa kolom `Daya Tampung 2026` di file master telah 100% cocok dengan SK Rektor (total kuota S1 Kampus Utama = 7.395 kursi).
  - Penyesuaian angka kelulusan seleksi pada jalur mandiri agar konsisten dengan rumus `Lulus Seleksi = Daftar Ulang + Mundur/Gugur`.

---

## [Pedoman Standar untuk Perubahan Berikutnya]
Jika Anda atau asisten AI mengubah data master di masa depan:
1. Buat snapshot backup terlebih dahulu ke folder `data/snapshots/` dengan nama bertanggal (misal `master_YYYYMMDD_deskripsi.xlsx`).
2. Terapkan perubahan pada file master Excel.
3. Jalankan `python3 scripts/audit_diff.py` untuk memverifikasi cell yang berubah.
4. Jalankan `python3 scripts/build_all.py` untuk menyinkronkan seluruh output.
5. Tambahkan entri baru di bagian atas dokumen `CHANGELOG_DATA.md` ini.
