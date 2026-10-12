# 📊 Diagram Visual Alur Pipeline & Arsitektur Repositori
**Sistem Otomasi Data, Single Source of Truth (SSOT), dan One-Click Build USK**

Dokumen ini menyajikan representasi visual diagram alur kerja (*pipeline workflow*) dari hulu (data mentah) hingga hilir (grafik, dashboard, dan presentasi) agar mudah dilihat dan dipelajari melalui Markdown Preview.

---

## 1. Diagram Alur Utama (End-to-End Pipeline)

```mermaid
graph TD
    %% Styling & Warna Node
    classDef inputStyle fill:#EFF6FF,stroke:#3B82F6,stroke-width:2px,color:#1E3A8A;
    classDef etlStyle fill:#F5F3FF,stroke:#8B5CF6,stroke-width:2px,color:#4C1D95;
    classDef ssotStyle fill:#ECFDF5,stroke:#10B981,stroke-width:2.5px,color:#064E3B;
    classDef coreStyle fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#78350F;
    classDef buildStyle fill:#EEF2FF,stroke:#6366F1,stroke-width:2.5px,color:#312E81;
    classDef outStyle fill:#F0FDF4,stroke:#22C55E,stroke-width:2px,color:#14532D;
    classDef qcStyle fill:#FFF1F2,stroke:#F43F5E,stroke-width:2px,color:#881337;

    %% 1. Input Layer
    A["📥 1. INPUT (Bahan Mentah)<br><code>data/raw/rekap data (fix).xlsx</code><br><i>Data pendaftaran & kuota dari PMB</i>"]:::inputStyle

    %% 2. ETL Processing
    B["⚙️ 2. ETL ENGINE<br><code>scripts/build_master_dataset.py</code><br><i>Hitung regresi OLS, CAGR, kuadran</i>"]:::etlStyle

    %% 3. Master Dataset
    C["🏛️ 3. SINGLE SOURCE OF TRUTH (SSOT)<br><code>data/master/master_analisa_*.xlsx</code><br><i>Database resmi 66 prodi S1, D3 & PSDKU</i>"]:::ssotStyle

    %% 4. Shared Core Logic
    D["📖 4. BUKU RESEP UTAMA<br><code>scripts/core_data.py</code><br><i>Ambang Batas 4.0x & 80%, Kamus Prodi</i>"]:::coreStyle

    %% 5. Master Orchestrator
    E["🚀 5. ONE-CLICK ORCHESTRATOR<br><code>scripts/build_all.py</code><br><i>Menjalankan 5 tahap build serentak (~17s)</i>"]:::buildStyle

    %% 6. Output Layer
    F1["📊 6a. Visualisasi Grafik<br><code>output/grafik/</code><br><i>35+ Gambar PNG Resolusi Tinggi</i>"]:::outStyle
    F2["🌐 6b. Dashboard Interaktif<br><code>output/dashboard/</code><br><i>matriks_interaktif_kuadran_usk.html</i>"]:::outStyle
    F3["📑 6c. Slide Deck Eksekutif<br><code>output/presentasi/</code><br><i>Presentasi Rektorat & Dekan (.pptx)</i>"]:::outStyle

    %% 7. Quality Control
    G["🔍 7. QUALITY CONTROL (QC 1 DETIK)<br><code>scripts/verify_sync.py</code><br><i>Audit timestamp otomatis: SYNCED 100%</i>"]:::qcStyle

    %% Hubungan Alur Kerja
    A -->|"Dideteksi jika ada revisi"| B
    B -->|"Generate database terpadu"| C
    C -->|"Pemberian data bersih"| D
    D -->|"Parameter & data terpusat"| E
    
    E -->|"Render grafik PNG"| F1
    E -->|"Kompilasi web standalone"| F2
    E -->|"Update deck pimpinan"| F3
    
    E -->|"Verifikasi otomatis di akhir"| G
```

---

## 2. Penjelasan 7 Tahapan Alur Kerja

| No | Tahapan | Berkas Terkait | Fungsi & Tanggung Jawab |
| :---: | :--- | :--- | :--- |
| **1** | **Input Data Mentah** | [`data/raw/rekap data (fix).xlsx`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/data/raw/rekap%20data%20%28fix%29.xlsx) | File masukan mentah dari tim PMB atau rekan kerja yang memuat data kuota, pendaftar, dan kelulusan tahunan. |
| **2** | **ETL Engine** | [`scripts/build_master_dataset.py`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/scripts/build_master_dataset.py) | Mengolah data mentah menjadi data saintifik: menghitung slope tren (OLS), CAGR 5 tahun, persentase keterisian, dan klasifikasi kuadran. |
| **3** | **Single Source of Truth** | [`data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx) | **Satu-satunya sumber data sah**. Seluruh grafik dan dokumen mengacu ke file ini agar tidak ada angka yang berbeda di tempat lain. |
| **4** | **Buku Resep Utama** | [`scripts/core_data.py`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/scripts/core_data.py) | Modul Python yang menyimpan aturan bisnis (keketatan $\ge 4.0\text{x}$, keterisian $\ge 80\%$, daftar prodi baru, dan pemetaan nama prodi). |
| **5** | **One-Click Orchestrator** | [`scripts/build_all.py`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/scripts/build_all.py) | Perintah komando utama. Cukup jalankan satu baris ini, seluruh proses build berjalan otomatis secara berurutan. |
| **6** | **Output Siap Pakai** | `output/grafik/`, `output/dashboard/`, `output/presentasi/` | Hasil akhir visual yang siap dipresentasikan ke Rektor, Wakil Rektor, atau Dekanat dalam rapat pimpinan. |
| **7** | **Quality Control** | [`scripts/verify_sync.py`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/scripts/verify_sync.py) | Pemeriksaan instan (kurang dari 1 detik) untuk memastikan semua file output sudah memakai data master terbaru. |

---

## 3. Diagram Deteksi Otomatis & Pembuatan Snapshot Cadangan

Jika Anda atau rekan mengubah data di file mentah, berikut alur otomatisasi pengamanannya:

```mermaid
graph TD
    classDef alertStyle fill:#FEF2F2,stroke:#EF4444,stroke-width:2px,color:#991B1B;
    classDef safeStyle fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#064E3B;
    classDef procStyle fill:#EFF6FF,stroke:#3B82F6,stroke-width:2px,color:#1E3A8A;

    EDIT["Anda / Rekan mengedit:<br><code>data/raw/rekap data (fix).xlsx</code>"]:::alertStyle
    RUN["Jalankan di Terminal:<br><code>python3 scripts/build_all.py</code>"]:::procStyle
    
    CEK{"Apakah file mentah<br>lebih baru dari master?"}:::procStyle
    SNAP["💾 Otomatis Backup ke:<br><code>data/snapshots/master_YYYYMMDD_v*.xlsx</code>"]:::safeStyle
    ETL["⚙️ Bangun Ulang Master Dataset<br>(Hitung OLS, Keketatan, Kuadran)"]:::procStyle
    REGEN["🎨 Re-Render Seluruh Output<br>(Grafik PNG, HTML Dashboard, PPTX)"]:::procStyle
    SYNC["✅ Verifikasi Selesai: SYNCED 100%"]:::safeStyle

    EDIT --> RUN
    RUN --> CEK
    CEK -- Ya (Data Baru Terdeteksi) --> SNAP
    SNAP --> ETL
    ETL --> REGEN
    CEK -- Tidak (Hanya refresh visual) --> REGEN
    REGEN --> SYNC
```

---

## 4. Perintah Cepat untuk Keseharian

```bash
# 1. Cek apakah grafik Anda sudah tersinkron dengan database terbaru (1 detik)
python3 scripts/verify_sync.py

# 2. Cek baris atau sel Excel mana yang baru saja berubah (2 detik)
python3 scripts/audit_diff.py

# 3. Sinkronkan seluruh grafik PNG, dashboard HTML, dan PPT sekaligus (17 detik)
python3 scripts/build_all.py
```
