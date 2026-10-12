# 📜 Jurnal Log Perubahan Data (CHANGELOG_DATA)
**Repositori Analisis Peminatan, Daya Tampung, dan Jalur Masuk USK (2022–2026)**

Dokumen ini mencatat setiap kronologi perubahan data master, penyesuaian angka historis, dan re-kalkulasi metrik strategis agar riwayat perubahan selalu transparan, dapat dilacak (*auditable*), dan mudah di-*rollback*.

---

## [2026-10-12] - Pembentukan Arsitektur Sinkronisasi Terpusat & Audit Tooling
- **Inisiator/Konteks:** Standardisasi arsitektur repositori untuk mencegah kerja ganda (*DRY principle*) dan memastikan seluruh visualisasi tersinkronisasi 100%.
- **File Baru:**
  1. `analisa_peminatan_dan_daya_tampung/scripts/core_data.py`: Modul parameter sentral (ambang batas 4.0x dan 80%, kamus singkatan nama).
  2. `analisa_peminatan_dan_daya_tampung/scripts/build_all.py`: Pipeline runner *one-click* untuk meregenerasi seluruh grafik dan dashboard.
  3. `analisa_peminatan_dan_daya_tampung/scripts/verify_sync.py`: Tool verifikasi status sinkronisasi repo dalam 1 detik.
  4. `analisa_peminatan_dan_daya_tampung/scripts/audit_diff.py`: Tool pembanding perbedaan cell-by-cell file Excel master vs snapshot.
  5. `analisa_peminatan_dan_daya_tampung/data/snapshots/`: Direktori penyimpanan snapshot bertanggal.
- **Hasil Audit Status:** Seluruh grafik PNG dan dashboard HTML terverifikasi tersinkronisasi penuh dengan Master Excel (`2026-10-12 11:21`).

---

## [2026-10-09 19:56] - Penyelarasan Kolom Kuadran Master & Koreksi Data Riwayat Resmi
- **File Terdampak:** `analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`
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
- **Snapshot Terkait:** `analisa_peminatan_dan_daya_tampung/data/snapshots/master_20261009_v2_revisi_perminyakan_lingkungan.xlsx`

---

## [2026-10-09 11:45] - Rekonsiliasi Daya Tampung 2026 Sesuai SK Rektor No. 121/UN11/KPT/2026
- **Sumber Data:** Dokumen resmi `121UN11KPT2026 SK Daya Tampung AWAL 2026-2027 tte KIRIM SNPMB PUSAT (1).pdf`
- **Temuan & Tindakan:**
  - Audit perbandingan antara file rekap awal vs SK Rektor menunjukkan bahwa kolom `Daya Tampung 2026` di file master telah 100% cocok dengan SK Rektor (total kuota S1 Kampus Utama = 7.395 kursi).
  - Penyesuaian angka kelulusan seleksi pada jalur mandiri agar konsisten dengan rumus `Lulus Seleksi = Daftar Ulang + Mundur/Gugur`.

---

## [Pedoman Standar untuk Perubahan Berikutnya]
Jika Anda atau asisten AI mengubah data master di masa depan:
1. Buat snapshot backup terlebih dahulu ke folder `analisa_peminatan_dan_daya_tampung/data/snapshots/` dengan nama bertanggal (misal `master_YYYYMMDD_deskripsi.xlsx`).
2. Terapkan perubahan pada file master Excel.
3. Jalankan `python3 analisa_peminatan_dan_daya_tampung/scripts/audit_diff.py` untuk memverifikasi cell yang berubah.
4. Jalankan `python3 analisa_peminatan_dan_daya_tampung/scripts/build_all.py` untuk menyinkronkan seluruh output.
5. Tambahkan entri baru di bagian atas dokumen `CHANGELOG_DATA.md` ini.
