# PANDUAN KERJA & ATURAN PROYEK (USK PMB ANALYSIS)
# =============================================================================
# File: GEMINI.md
# Deskripsi: Panduan aturan, konvensi data, dan standar workflow otomatis untuk AI
# Lokasi: Root Repositori tugas-5
# =============================================================================

Dokumen ini berisi aturan wajib, konvensi data, dan prosedur operasi standar (SOP) yang harus dipatuhi oleh AI saat beroperasi di dalam repositori ini.

---

## 1. Single Source of Truth (Database Master)
- **Sumber Data Mutlak:** Seluruh analisis angka, visualisasi chart, dan rekapitulasi data **wajib** merujuk pada file master resmi:
  `data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx` (Sheet: `Master_Semua_Prodi`).
- **Kode Program Studi Resmi:** Seluruh 81 prodi menggunakan kode resmi 7 digit (misal `0115001` Manajemen Gayo Lues, `1110201` Budidaya Perairan, `0411601` Teknik Perminyakan) yang bersumber dari `data/raw/rekap data (fix).xlsx`.
- **Integritas Data:** Dilarang meng-hardcode angka atau membuat asumsi metrik tanpa verifikasi langsung dari database master.

---

## 2. Standar Penyusunan Berkas Excel (Data Processed)
Seluruh file Excel terolah di dalam `data/processed/` harus mengikuti standar berikut:
1. **Urutan Kolom Multi-Tahun:**
   Urutan kolom tahun dari kiri ke kanan **wajib menurun (descending)**:
   `[Identitas Prodi]` → **2026** → **2025** → **2024** → **2023** → **2022** → `[TOTAL 5 TAHUN (2022–2026)]`.
2. **Formula Dinamis Sisa Kuota:**
   Kolom Sisa Kuota harus menggunakan formula dinamis: `=Total Daya Tampung - Total Daftar Ulang` (misal `=E6-G6`).
3. **Sheet Ringkasan Eksekutif:**
   - 4 KPI Card teratas wajib mengambil angka dinamis via formula live ke sheet rincian (bukan angka mati).
   - Tabel Kinerja Fakultas wajib menggunakan formula dinamis Excel (`=COUNTIF` dan `=SUMIF`).
   - Baris Tabel Tren Tahunan dipertahankan kronologis (**2022 naik ke 2026**) agar tren pertumbuhan historis mudah dibaca.
4. **Penamaan Tab Sheet Tahunan:**
   Seragamkan penamaan tab sheet tahunan menjadi:
   `Tahun_2026`, `Tahun_2025`, `Tahun_2024`, `Tahun_2023`, `Tahun_2022`.
5. **Estetika & Format:**
   Tampilkan gridlines (`showGridLines = True`), font korporat (Segoe UI/Calibri), perataan teks rapi (angka rata kanan, kode/jenjang rata tengah), serta format angka `#,#0` dan persentase `0.0%`.

---

## 3. Pipeline Workflow & Otomasi Hilir (Zero Double Work)
Untuk memastikan pengguna **tidak perlu kerja 2 kali**, AI wajib mematuhi aturan efek domino otomatis (*automatic cascade*) berikut:
1. **Modul Sentral Konfigurasi (core_data.py):**
   Selalu rujuk dan gunakan modul `scripts/core_data.py` untuk konstanta path, ambang batas benchmark (Keketatan `4.0x`, Fill Rate `80.0%`), dan fungsi pemuatan data S1. Jangan pernah menduplikasi konstanta di skrip lain.
2. **Efek Domino Otomatis (Automatic Cascade Trigger):**
   Setiap kali ada pembaruan pada data hulu (`data/raw/` atau `data/master/`) atau perubahan konfigurasi di `scripts/`:
   - AI **wajib langsung menjalankan orkestrator tunggal**:
     ```bash
     python3 scripts/build_all.py
     ```
   - Skrip ini akan otomatis mendeteksi perubahan, membuat backup snapshot, memperbarui master dataset, dan meregenerasi seluruh artefak hilir:
     - 17 Grafik Reguler + Matriks 4 Kuadran (All Labels & 60 Prodi Mapan).
     - Berkas Excel `rekap_selisih_lulus_vs_daftar_ulang_2022_2026.xlsx`.
     - Berkas Excel `rekap_daya_tampung_peminat_dan_sisa_kuota_2022_2026.xlsx`.
     - Dashboard Interaktif HTML `matriks_interaktif_kuadran_usk.html`.
3. **Audit Verifikasi Cepat Wajib (1 Detik):**
   Sebelum menyatakan pekerjaan selesai kepada pengguna, AI **wajib mengeksekusi**:
   ```bash
   python3 scripts/verify_sync.py
   ```
   Pastikan seluruh artefak berstatus `[SYNCED]` 100%. Jika ada artefak yang berstatus `[OUT-OF-SYNC]` atau `[MISSING]`, AI wajib memperbaikinya segera.
4. **Sinkronisasi Narasi Laporan (docs/):**
   Jika angka agregat di master berubah, AI wajib memperbarui tabel metrik dan angka narasi di dalam laporan eksekutif di folder `docs/` agar tidak terjadi perbedaan antara laporan teks dan database master.

---

## 4. Kebijakan Keamanan & Git (Version Control)
- **Izin Commit/Push:** Dilarang melakukan `git commit` atau `git push` ke GitHub tanpa instruksi/izin eksplisit dari pengguna.
- **Integritas Dokumen:** Seluruh diagram arsitektur, catatan data dictionary, dan panduan workflow harus selalu konsisten dengan implementasi kode terbaru.
