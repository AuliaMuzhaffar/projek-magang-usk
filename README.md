# 🎓 Analisis Komprehensif Peminatan, Daya Tampung, dan Jalur Masuk Universitas Syiah Kuala (2022–2026)

[![Status](https://img.shields.io/badge/Status-Production%20Ready-success?style=flat-square)](#)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat-square&logo=python)](#)
[![Architecture](https://img.shields.io/badge/Architecture-Modular%20SSOT%20Pipeline-indigo?style=flat-square)](#)
[![Sync Health](https://img.shields.io/badge/Sync%20Check-100%25%20Verified-emerald?style=flat-square)](#)

Repositori ini menyajikan analisis longitudinal 5 tahun (Tahun Akademik 2022 s.d. 2026) mengenai tren peminatan pendaftar, kapasitas daya tampung, efisiensi keterisian (*fill rate*), tingkat konversi daftar ulang (*yield rate*), analisis kebocoran per jalur seleksi (SNBP, SNBT, Mandiri), disparitas bantuan KIP-Kuliah, serta pemodelan strategi portofolio Matriks 4 Kuadran bagi seluruh program studi di **Universitas Syiah Kuala (USK)**.

---

## 📂 Struktur Direktori Repositori (Standar Industri Modular)

Repositori ini telah direstrukturisasi secara modular dan terpadu untuk memastikan kerapian manajemen berkas, kemudahan pencarian, serta pemisahan yang tegas antara data mentah, modul data science, dokumentasi, dan artefak output:

```text
tugas-5/
├── assets/                          # Aset visual statis
│   └── logos/                       # Logo resmi USK (PNG, WebP)
│
├── data/                            # Manajemen data berjenjang (SSOT)
│   ├── raw/                         # Berkas Excel mentah sumber (rekap data fix, data KIP)
│   ├── master/                      # Single Source of Truth (master_analisa_*.xlsx)
│   ├── processed/                   # Dataset hasil olahan disagregasi per jalur masuk
│   ├── snapshots/                   # Salinan backup bertanggal untuk audit trail & rollback
│   └── reference_sk/                # Dokumen rujukan SK Rektor, Keputusan SNPMB & UKT
│
├── scripts/                         # Script eksekusi data science & visualisasi
│   ├── core_data.py                 # Modul sentral konfigurasi, benchmark kuadran & kamus data
│   ├── build_all.py                 # Master pipeline runner (One-Click Rebuild seluruh repo)
│   ├── verify_sync.py               # Pengecekan kesehatan sinkronisasi 1 detik
│   ├── audit_diff.py                # Pemeriksa perbedaan sel-demi-sel (Cell-by-Cell Diff)
│   ├── build_master_dataset.py      # ETL engine pembuat Master Excel dari Raw Data
│   ├── generate_charts.py           # Generator 17 visualisasi tren utama
│   ├── generate_chart13_*.py        # Generator Matriks 4 Kuadran (All Labels & Prodi Mapan)
│   ├── build_interactive_matrix_*.py# Generator dashboard analitik interaktif HTML
│   └── ...                          # Generator tematik (KIP, Jalur Masuk, Slide Roster)
│
├── docs/                            # 19 Laporan analitis mendalam & dokumen metodologi
│   ├── master_deck_presentasi_rkat.md
│   ├── laporan_analisa_peminatan_dan_daya_tampung.md
│   ├── laporan_analisis_jalur_masuk_dan_kebocoran.md
│   ├── laporan_analisis_kip_kuliah_dan_kebocoran_desil.md
│   ├── laporan_eksekutif_sintesis_tren_dan_portofolio_kuadran.md
│   └── ...
│
├── output/                          # Seluruh artefak publikasi siap pakai
│   ├── grafik/                      # 35+ visualisasi grafik resolusi tinggi (PNG)
│   ├── dashboard/                   # Dashboard interaktif web (matriks_interaktif_kuadran_usk.html)
│   └── presentasi/                  # Slide deck pimpinan (.pptx)
│
├── README.md                        # Panduan utama repositori
├── PANDUAN_ARSITEKTUR_DAN_WORKFLOW.md# Panduan teknis pipeline, deteksi perubahan & rollback
├── DATA_DICTIONARY.md               # Kamus data, definisi rumus, dan aturan prodi baru
├── CHANGELOG_DATA.md                # Jurnal kronologis perubahan angka historis
└── .gitignore                       # Filter berkas sistem, file besar & cache
```

---

## ⚡ Quickstart & Perintah Cepat

Repositori ini dilengkapi arsitektur **Zero-Redundancy Pipeline**. Anda tidak perlu lagi mengedit grafik atau HTML satu per satu secara manual:

| Kebutuhan Anda | Perintah Terminal | Waktu Eksekusi | Keterangan |
| :--- | :--- | :---: | :--- |
| **Cek Kesehatan Sinkronisasi** | `python3 scripts/verify_sync.py` | **~1 detik** | Memeriksa apakah output PNG/HTML tertinggal dari Master Excel. |
| **Bandingkan Selisih Angka** | `python3 scripts/audit_diff.py` | **~2 detik** | Menampilkan baris dan kolom yang berubah cell-by-cell. |
| **One-Click Rebuild All** | `python3 scripts/build_all.py` | **~17 detik** | Memperbarui seluruh grafik PNG, dashboard HTML & verifikasi. |
| **Paksa Rebuild dari Raw** | `python3 scripts/build_all.py --from-raw` | **~22 detik** | Mengolah ulang file raw menjadi master lalu memperbarui output. |
| **Uji Bukti Keterisian USK** | `python3 scripts/bukti_keterisian_usk.py` | **~1 detik** | Menampilkan rekap keterisian kuota USK per tahun & prodi. |

---

## 📊 Ringkasan Temuan Strategis & Metrik Kunci

### 1. Klasifikasi Portofolio Matriks 4 Kuadran (S1 Kampus Utama)
Berdasarkan ambang batas keketatan seleksi **4,0 : 1** (rasio peminat terhadap kapasitas) dan ambang batas efisiensi keterisian **80,0%** (*fill rate*):

| Kuadran | Status Portofolio | Versi 66 Prodi S1 | Versi 60 Prodi Mapan | Implikasi Strategis Pimpinan |
| :---: | :--- | :---: | :---: | :--- |
| **Kuadran I** | **Unggulan** (Ketat & Ideal) | **27 Prodi** (40,9%) | **26 Prodi** (43,3%) | Pertahankan akreditasi unggul/internasional, perluas kemitraan. |
| **Kuadran II** | **Stabil** (Niche Market Kuat) | **4 Prodi** (6,1%) | **3 Prodi** (5,0%) | **Kunci Kuota!** Jangan naikkan daya tampung agar equilibrium terjaga. |
| **Kuadran III**| **Belum Optimal** (Ketat, Bocor Hilir) | **9 Prodi** (13,6%) | **7 Prodi** (11,7%) | **Jangan pangkas kuota!** Sediakan cicilan UKT/IPI & sistem cadangan mandiri cepat. |
| **Kuadran IV** | **Perlu Revitalisasi** (Krisis Kronis) | **26 Prodi** (39,4%) | **24 Prodi** (40,0%) | **Wajib pangkas kuota 20%–40%** untuk menaikkan rasio keketatan dan akreditasi. |

> **Catatan 6 Program Studi Baru (< 5 Tahun Beroperasi):**  
> *Bisnis Digital, Hubungan Internasional, Teknik Lingkungan, Teknik Perminyakan, Teknik Sumber Daya Air,* dan *Teknologi Industri Hasil Perikanan* dihitung menggunakan **Fair Evaluation Rule** (rata-rata dihitung dari tahun aktif beroperasi, bukan dibagi 5 tahun) untuk mencegah penalti data kosong.

---

### 2. Episentrum Kebocoran Calon Mahasiswa (*Yield Loss*)
Dari analisis disagregasi jalur seleksi 2022–2026:
- **Jalur Seleksi Mandiri (SMMPTN & Mandiri Konsorsium)** merupakan titik kebocoran terbesar (tingkat gugur mencapai **30%–45%**), terutama akibat penumpukan pengumuman di akhir siklus penerimaan dan beban Uang Pangkal / IPI.
- **SNBT (UTBK Nasional)** memiliki *fill rate* tertinggi dan paling stabil, namun rentan mengalami penolakan registrasi pada calon mahasiswa penerima KIP-Kuliah di **Desil 5–6** yang tidak lolos verifikasi bantuan biaya hidup.

---

## 🎨 Artefak Utama Siap Akses

1. **Dashboard Interaktif Web:**  
   [matriks_interaktif_kuadran_usk.html](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/output/dashboard/matriks_interaktif_kuadran_usk.html)  
   *Dashboard analitik interaktif mandiri (standalone) dengan fitur filter fakultas, pencarian prodi real-time, toggle prodi baru, dan mode gelap/terang.*

2. **Visualisasi Grafik Eksekutif (35+ PNG):**  
   Tersedia di folder [output/grafik/](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/output/grafik/):
   - `13_matriks_4_kuadran_5_tahun_2022_2026_all_labels.png` (Matriks 66 Prodi lengkap)
   - `13_matriks_4_kuadran_5_tahun_2022_2026_tanpa_prodi_baru.png` (Matriks 60 Prodi mapan)
   - `13_companion_direktori_66_prodi_4_kuadran.png` (Roster direktori per kuadran)
   - `14_dual_panel_jalur_masuk_dan_kebocoran.png` (Analisis jalur masuk & yield)
   - `20_analisis_desil_dan_rejection_kip_snbt.png` (Efek jurang desil KIP)

3. **Presentasi Slide Deck (.pptx):**  
   Tersedia di folder [output/presentasi/](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/output/presentasi/) untuk bahan paparan Rektorat, Dekanat, dan RKAT.

4. **Dokumentasi Lengkap:**  
   - [PANDUAN_ARSITEKTUR_DAN_WORKFLOW.md](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/PANDUAN_ARSITEKTUR_DAN_WORKFLOW.md) : Panduan teknis alur kerja & rollback
   - [DATA_DICTIONARY.md](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/DATA_DICTIONARY.md) : Kamus data & definisi rumus
   - [CHANGELOG_DATA.md](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/CHANGELOG_DATA.md) : Jurnal audit perubahan angka historis
   - [docs/](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/docs/) : 19 laporan naratif kajian akademik komprehensif

---

## 🛡️ Jaminan Integritas & Keamanan Data

- **Git Versioning:** Seluruh file kode, dokumentasi, dan konfigurasi dilacak penuh dalam riwayat Git.
- **Snapshot Immutability:** Master Excel memiliki salinan waktu nyata bertanggal di `data/snapshots/`.
- **Reproducibility:** Seluruh visualisasi dan dashboard dapat dibangun kembali kapan saja dari nol (*fully reproducible*) dengan menjalankan `python3 scripts/build_all.py`.
