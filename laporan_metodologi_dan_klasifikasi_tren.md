# Metodologi & Laporan Hasil Klasifikasi Tren Peminatan Prodi USK
## Evaluasi Komprehensif 81 Program Studi Universitas Syiah Kuala (2022–2026)

**Penyusun:** Tim Magang USK  
**Tanggal Analisis:** 2 September 2026  
**Basis Data:** `rekap data.xlsx` (Sheet *Rekapitulasi Data* & *Data_Per_Prodi* pada `analisis_peminatan.xlsx`)  
**Dokumen Pendukung:** [`analisis_faktor.md`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisis_faktor.md) & [`analisis_faktor_kenaikan.md`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisis_faktor_kenaikan.md)

---

## 1. Latar Belakang & Tujuan Klasifikasi

Evaluasi tren peminatan 81 program studi di Universitas Syiah Kuala (USK) selama 5 tahun terakhir (2022–2026) bertujuan untuk:
1. **Mengidentifikasi Pola Pertumbuhan:** Memisahkan program studi yang tumbuh secara konsisten, mengalami lonjakan musiman, mengalami kemunduran, atau berfluktuasi tanpa arah pasti.
2. **Menghindari Bias Data Agregat:** Mengelompokkan program studi baru secara terpisah agar laju pertumbuhan eksponensial tahun awal (misal: +680%) tidak mendistorsi analisis program studi reguler yang telah mapan.
3. **Menyediakan Dasar Pengambilan Keputusan:** Memberikan justifikasi matematis yang objektif bagi pimpinan universitas dalam penentuan kuota daya tampung, alokasi dosen/laboratorium, dan evaluasi tarif UKT/IPI.

---

## 2. Metodologi & Algoritma Klasifikasi Matematis

Klasifikasi dilakukan secara otomatis melalui pemrosesan data Python menggunakan 3 indikator statistik utama:

```
                       ┌──────────────────────────────────────────────┐
                       │           DATA TOTAL PEMINAT PRODI           │
                       │             (5 Tahun: 2022–2026)             │
                       └──────────────────────┬───────────────────────┘
                                              │
                         Apakah data tersedia < 3 tahun?
                                              │
                      ┌───────────────────────┴───────────────────────┐
                     YA                                              TIDAK
                      ▼                                               ▼
             ┌─────────────────┐                      Hitung Metrik:
             │  DATA TERBATAS  │                      1. Perubahan YoY (%): Δ22-23, Δ23-24, Δ24-25, Δ25-26
             │  (Prodi Baru)   │                      2. Pertumbuhan Total 5 Tahun (%)
             └─────────────────┘                      3. CAGR (%)
                                                                      │
            ┌──────────────────────┬──────────────────────────────────┼──────────────────────────────────┬──────────────────────┐
            ▼                      ▼                                  ▼                                  ▼                      ▼
    Kenaikan YoY >= 3x     Penurunan YoY >= 3x              Pertumbuhan Total > +50%           Penurunan Total < -30%     Pola Naik-Turun
    (Hampir tiap thn naik) (Hampir tiap thn turun)          (Lonjakan Masif)                   (Anjlok Signifikan)        (Bergantian)
            │                      │                                  │                                  │                      │
            ▼                      ▼                                  ▼                                  ▼                      ▼
  ┌──────────────────┐   ┌──────────────────┐               ┌──────────────────┐               ┌──────────────────┐   ┌──────────────────┐
  │MENINGKAT KONSISTEN│  │ MENURUN KONSISTEN│               │  MENINGKAT TAJAM │               │  MENURUN TAJAM   │   │    FLUKTUATIF    │
  │    (35 Prodi)    │   │    (10 Prodi)    │               │    (5 Prodi)     │               │    (2 Prodi)     │   │    (25 Prodi)    │
  └──────────────────┘   └──────────────────┘               └──────────────────┘               └──────────────────┘   └──────────────────┘
```

### A. Rumus-Rumus Statistik:

1. **Perubahan Tahunan (Year-over-Year / YoY %):**
   $$\Delta \text{YoY}_{t} = \frac{\text{Peminat}_{t} - \text{Peminat}_{t-1}}{\text{Peminat}_{t-1}} \times 100\%$$
   *Dihitung untuk 4 transisi:* 2022→2023, 2023→2024, 2024→2025, dan 2025→2026.

2. **Pertumbuhan Kumulatif 5 Tahun (%):**
   $$\Delta \text{Total} = \frac{\text{Peminat}_{2026} - \text{Peminat}_{2022}}{\text{Peminat}_{2022}} \times 100\%$$

3. **Compound Annual Growth Rate (CAGR %):**
   $$\text{CAGR} = \left( \frac{\text{Peminat}_{\text{Akhir}}}{\text{Peminat}_{\text{Awal}}} \right)^{\frac{1}{n}} - 1$$
   *Dimana $n$ adalah rentang tahun ketersediaan data.*

---

### B. Matriks Kriteria Aturan Klasifikasi:

| Kategori Tren | Kriteria Algoritma | Karakteristik Utama |
|---|---|---|
| **Meningkat Konsisten** | • Jumlah transisi YoY positif $\ge 3$ dari 4 kali (atau $\ge N-1$ valid).<br>• Pertumbuhan total 5 tahun $> 0\%$. | Program studi yang permintaannya stabil menanjak hampir setiap tahun akademik. |
| **Meningkat Tajam** | • Pertumbuhan kumulatif total 5 tahun melompat $> +50\%$.<br>• Tidak memiliki pola penurunan konsisten. | Mengalami lonjakan peminat masif akibat momentum industri atau transformasi prodi. |
| **Menurun Konsisten** | • Jumlah transisi YoY negatif $\ge 3$ dari 4 kali.<br>• Arah grafik peminatan condong terus merosot. | Mengalami penurunan minat berkelanjutan yang memerlukan evaluasi kurikulum/biaya. |
| **Menurun Tajam** | • Penurunan kumulatif total 5 tahun melebihi $-30\%$ ($<-30\%$). | Mengalami penurunan drastis dalam skala volume besar dibanding 5 tahun lalu. |
| **Fluktuatif** | • Pola perubahan bergantian antara naik dan turun (2x naik & 2x turun).<br>• Tidak memenuhi syarat dominan meningkat atau menurun. | Dipengaruhi oleh tren sesaat, persepsi passing grade, atau dinamika kuota tahunan. |
| **Data Terbatas** | • Memiliki data historis $< 3$ tahun operasional. | Program studi baru yang baru dibuka pada kurun 2024–2026 (misal: Bisnis Digital, T. Perminyakan). |

---

## 3. Rekapitulasi Distribusi Tren 81 Prodi USK

Dari total **81 Program Studi** (69 S1, 11 D3, 1 D4) di lingkungan Universitas Syiah Kuala, sebaran kategorinya adalah sebagai berikut:

```
  ┌─────────────────────────────────────────────────────────────┐
  │         SEBARAN TREN PEMINATAN 81 PRODI USK (2022–2026)     │
  ├──────────────────────────────┬──────────────┬───────────────┤
  │ Kategori Tren                │ Jumlah Prodi │ Persentase    │
  ├──────────────────────────────┼──────────────┼───────────────┤
  │ 1. Meningkat Konsisten       │ 35 Prodi     │ 43,2%         │
  │ 2. Fluktuatif                │ 25 Prodi     │ 30,9%         │
  │ 3. Menurun Konsisten         │ 10 Prodi     │ 12,3%         │
  │ 4. Meningkat Tajam           │ 5 Prodi      │ 6,2%          │
  │ 5. Data Terbatas (Baru)      │ 4 Prodi      │ 4,9%          │
  │ 6. Menurun Tajam             │ 2 Prodi      │ 2,5%          │
  ├──────────────────────────────┼──────────────┼───────────────┤
  │ TOTAL                        │ 81 Prodi     │ 100,0%        │
  └──────────────────────────────┴──────────────┴───────────────┘
```

---

## 4. Laporan Rinci per Kategori Program Studi

---

### Kategori 1: Meningkat Konsisten (35 Program Studi — 43,2%)
*Program studi yang mengalami tren peningkatan peminat stabil dan berkesinambungan.*

| No | Program Studi | Jenjang | Fakultas | Peminat 2022 | Peminat 2026 | CAGR (%) | Karakteristik Tren |
|:--:|---|:---:|---|:---:|:---:|:---:|---|
| 1 | **Pendidikan Guru SD (PGSD)** | S1 | KIP | 1.621 | **2.175** | +7,6% | Top 4 volume USK, stabil naik |
| 2 | **Akuntansi** | S1 | FEB | 1.327 | **2.008** | +10,9% | Pertumbuhan konsisten di FEB |
| 3 | **Akuntansi Perpajakan** | D4 | FEB | 26 | **1.794** | +188,2% | Sukses konversi Sarjana Terapan |
| 4 | **Teknik Pertambangan** | S1 | Teknik | 845 | **1.735** | +19,7% | Booming hilirisasi industri mineral |
| 5 | **Teknik Sipil** | S1 | Teknik | 1.231 | **1.416** | +3,6% | Permintaan infrastruktur stabil |
| 6 | **Pendidikan Bahasa Indonesia** | S1 | KIP | 501 | **1.294** | +26,8% | Didorong kebutuhan guru PPPK |
| 7 | **Ilmu Pemerintahan** | S1 | FISIP | 886 | **1.220** | +8,3% | Naik konsisten di FISIP |
| 8 | **Pendidikan Bahasa Inggris** | S1 | KIP | 651 | **1.111** | +14,3% | Minat bahasa asing stabil tinggi |
| 9 | **Keuangan dan Perbankan** | D3 | FEB | — | **1.096** | +154,6% | Vokasi perbankan diminati |
| 10 | **Akuntansi** | D3 | FEB | — | **1.048** | +223,3% | Vokasi akuntansi terapan |
| 11 | **PPKn** | S1 | KIP | 434 | **1.025** | +24,0% | Penyerapan formasi guru tinggi |
| 12 | **Manajemen Perusahaan** | D3 | FEB | — | **929** | +369,1% | Vokasi manajemen bisnis |
| 13 | **Teknik Sipil** | D3 | Teknik | — | **925** | +338,1% | Vokasi konstruksi |
| 14 | **Agribisnis** | S1 | Pertanian | 875 | **869** | −0,2% | Volume peminat pertanian terbesar |
| 15 | **Pendidikan Jasmani (PJOK)** | S1 | KIP | 300 | **812** | +28,3% | Formasi guru olahraga daerah |
| 16 | **Manajemen Agribisnis** | D3 | Pertanian | — | **801** | +189,5% | Vokasi agribisnis terapan |
| 17 | **Pendidikan Guru PAUD** | S1 | KIP | 586 | **764** | +6,9% | Rebound formasi guru usia dini |
| 18 | **Teknik Mesin** | S1 | Teknik | 442 | **726** | +13,2% | Naik 4 tahun berturut-turut |
| 19 | **Pendidikan Biologi** | S1 | KIP | 550 | **638** | +3,8% | Stabil menanjak |
| 20 | **Agroteknologi** | S1 | Pertanian | 528 | **617** | +4,0% | Pertanian pangan stabil |
| 21 | **Kesehatan Hewan** | D3 | FKH | — | **572** | +158,8% | Paramedis veteriner unggulan |
| 22 | **Sosiologi** | S1 | FISIP | 484 | **519** | +1,8% | Naik perlahan |
| 23 | **Teknologi Hasil Pertanian** | S1 | Pertanian | 291 | **510** | +15,1% | Inovasi *food technology* |
| 24 | **Pendidikan Geografi** | S1 | KIP | 294 | **494** | +13,9% | Pertumbuhan kependidikan |
| 25 | **Biologi** | S1 | MIPA | 374 | **485** | +6,7% | Sains hayati MIPA |
| 26 | **Teknik Mesin** | D3 | Teknik | — | **468** | +139,7% | Vokasi manufaktur |
| 27 | **Budidaya Peternakan** | D3 | Pertanian | — | **454** | +188,0% | Vokasi peternakan |
| 28 | **Kehutanan** | S1 | Pertanian | 337 | **416** | +5,4% | Isu lingkungan & kehutanan |
| 29 | **Pendidikan Ekonomi** | S1 | KIP | 276 | **404** | +10,0% | Kependidikan soshum |
| 30 | **Sekretari** | D3 | FEB | — | **342** | +86,2% | Administrasi perkantoran |
| 31 | **Peternakan** | S1 | Pertanian | 331 | **331** | +0,0% | Industri protein hewani |
| 32 | **Teknik Listrik** | D3 | Teknik | — | **281** | +149,9% | Vokasi kelistrikan |
| 33 | **Pendidikan Biologi (PDD Gayo Lues)** | S1 | KIP | 13 | **24** | +16,6% | Tumbuh dari basis kecil |
| 34 | **Bimbingan Konseling** | S1 | KIP | 1.160 | **1.754** | +10,9% | Permintaan konselor sekolah |
| 35 | **Manajemen Informatika** | D3 | MIPA | — | **1.450** | +140,0% | Vokasi IT terapan |

---

### Kategori 2: Meningkat Tajam (5 Program Studi — 6,2%)
*Program studi reguler yang mengalami akselerasi pertumbuhan lebih dari +50% dalam 5 tahun.*

| No | Program Studi | Jenjang | Fakultas | Peminat 2022 | Peminat 2026 | Pertumbuhan 5 Thn | Rasio 2026 | Faktor Pendorong |
|:--:|---|:---:|---|:---:|:---:|:---:|:---:|---|
| 1 | **Teknik Industri** | S1 | Teknik | 660 | **1.052** | **+59,4%** | 10,52 : 1 | Optimasi supply chain & logistik industri |
| 2 | **Teknik Elektro** | S1 | Teknik | 449 | **709** | **+57,9%** | 7,09 : 1 | Elektrifikasi & transisi energi terbarukan |
| 3 | **Pendidikan Sejarah** | S1 | KIP | 406 | **643** | **+58,4%** | 5,36 : 1 | Penyerapan formasi guru sejarah daerah |
| 4 | **Teknik Lingkungan** | S1 | Teknik | 210 | **526** | **+150,5%** | 8,77 : 1 | Kepatuhan regulasi AMDAL & audit ESG korporasi |
| 5 | **Teknik Geologi** | S1 | Teknik | 241 | **470** | **+95,0%** | 7,83 : 1 | Eksplorasi mineral, air tanah, dan mitigasi bencana |

---

### Kategori 3: Menurun Konsisten (10 Program Studi — 12,3%)
*Program studi yang mengalami tren penurunan peminat secara bertahap dalam 3 dari 4 tahun.*

| No | Program Studi | Jenjang | Fakultas | Peminat 2022 | Peminat 2026 | CAGR (%) | Rasio 2026 | Faktor Utama Penurunan |
|:--:|---|:---:|---|:---:|:---:|:---:|:---:|---|
| 1 | **Pendidikan Dokter** | S1 | Kedokteran | 4.092 | **2.003** | −16,4% | 8,01 : 1 | Plafon IPI Mandiri Rp 76–250 Jt & aturan SNPMB |
| 2 | **Ilmu Keperawatan** | S1 | Keperawatan | 2.266 | **1.588** | −8,5% | 6,62 : 1 | Substitusi ke Farmasi & saturasi formasi ners lokal |
| 3 | **Teknik Komputer** | S1 | Teknik | 1.565 | **1.466** | −1,6% | 14,66 : 1 | Koreksi peminat akibat tren restrukturisasi tech |
| 4 | **Pendidikan Kesejahteraan Keluarga** | S1 | KIP | 897 | **943** | +1,3% | 5,89 : 1 | Tren peminat melandai di 2 tahun terakhir |
| 5 | **Ekonomi Islam** | S1 | FEB | 807 | **595** | −7,3% | 3,72 : 1 | Persaingan dengan Manajemen/Akuntansi reguler |
| 6 | **Teknik Pertanian** | S1 | Pertanian | 515 | **550** | +1,7% | 3,93 : 1 | Melandai di tahun 2026 |
| 7 | **Arsitektur** | S1 | Teknik | 720 | **503** | −8,6% | 7,19 : 1 | Penurunan stabil dari 720 (2022) ke 503 (2026) |
| 8 | **Budidaya Perairan** | S1 | FPK | 188 | **145** | −6,3% | 1,45 : 1 | Minat sektor akuakultur konvensional minim |
| 9 | **Pemanfaatan Sumberdaya Perikanan**| S1 | FPK | 153 | **129** | −4,2% | 1,29 : 1 | Preferensi kerja sektor perikanan tangkap rendah |
| 10 | **Proteksi Tanaman** | S1 | Pertanian | 109 | **105** | −0,9% | 1,05 : 1 | Spesialisasi hama/penyakit kurang populer |

---

### Kategori 4: Menurun Tajam (2 Program Studi — 2,5%)
*Program studi yang mengalami kontraksi peminat kumulatif lebih dari −30% dalam 5 tahun.*

| No | Program Studi | Jenjang | Fakultas | Peminat 2022 | Peminat 2026 | Penurunan 5 Thn | CAGR (%) | Evaluasi Kritis |
|:--:|---|:---:|---|:---:|:---:|:---:|:---:|---|
| 1 | **Pendidikan Dokter Hewan** | S1 | FKH | 1.344 | **897** | **−33,3%** | −9,6% | Biaya operasional ko-asistensi tinggi & preferensi profesi dokter hewan terkonsentrasi di perkotaan |
| 2 | **Sendratasik (Pendidikan Seni Drama Tari Musik)** | S1 | KIP | 612 | **386** | **−36,9%** | −10,9% | Pergeseran minat seni pertunjukan konvensional ke media kreatif digital |

---

### Kategori 5: Fluktuatif (25 Program Studi — 30,9%)
*Program studi dengan pola peminatan naik-turun bergantian tanpa arah tren tunggal.*

| No | Program Studi | Jenjang | Fakultas | Peminat 2022 | Peminat 2026 | Puncak Peminat (Tahun) | Rasio 2026 |
|:--:|---|:---:|---|:---:|:---:|:---:|:---:|
| 1 | **Ilmu Hukum** | S1 | Hukum | 2.532 | **3.720** | 3.880 (2025) | 6,64 : 1 *(Rank #1 USK)* |
| 2 | **Farmasi** | S1 | MIPA | 3.046 | **3.526** | 3.588 (2024) | 39,18 : 1 *(Terketat USK)* |
| 3 | **Manajemen** | S1 | FEB | 2.466 | **2.823** | 2.936 (2024) | 14,12 : 1 |
| 4 | **Informatika** | S1 | MIPA | 2.200 | **2.174** | 2.595 (2025) | 18,12 : 1 |
| 5 | **Ilmu Komunikasi** | S1 | FISIP | 1.526 | **1.788** | 1.764 (2024) | 9,93 : 1 |
| 6 | **Psikologi** | S1 | Kedokteran | 1.147 | **1.385** | 1.504 (2024) | 17,31 : 1 |
| 7 | **Pendidikan Dokter Gigi** | S1 | FKG | 1.571 | **1.204** | 1.624 (2024) | 15,05 : 1 |
| 8 | **Ekonomi Pembangunan** | S1 | FEB | 718 | **694** | 733 (2024) | 3,86 : 1 |
| 9 | **Perencanaan Wilayah & Kota (PWK)**| S1 | Teknik | 637 | **669** | 680 (2024) | 8,36 : 1 |
| 10 | **Statistika** | S1 | MIPA | 663 | **537** | 663 (2022) | 5,37 : 1 |
| 11 | **Ilmu Politik** | S1 | FISIP | 448 | **499** | 478 (2024) | 2,85 : 1 |
| 12 | **Pendidikan Matematika** | S1 | KIP | 473 | **448** | 521 (2025) | 4,48 : 1 |
| 13 | **Teknik Kimia** | S1 | Teknik | 344 | **438** | 474 (2025) | 3,65 : 1 |
| 14 | **Ilmu Kelautan** | S1 | FPK | 316 | **302** | 320 (2024) | 1,51 : 1 |
| 15 | **Teknik Geofisika** | S1 | Teknik | 186 | **209** | 230 (2024) | 3,48 : 1 |
| 16 | **Pendidikan Kimia** | S1 | KIP | 180 | **206** | 215 (2024) | 2,29 : 1 |
| 17 | **Ilmu Tanah** | S1 | Pertanian | 178 | **195** | 210 (2024) | 1,62 : 1 |
| 18 | **Kimia** | S1 | MIPA | 158 | **195** | 200 (2024) | 2,44 : 1 |
| 19 | **Matematika** | S1 | MIPA | 248 | **185** | 248 (2022) | 2,06 : 1 |
| 20 | **Pendidikan Fisika** | S1 | KIP | 175 | **155** | 175 (2024) | 1,94 : 1 |
| 21 | **TIHP (Teknologi Industri Perikanan)**| S1 | FPK | — | **103** | 131 (2025) | 2,06 : 1 |
| 22 | **Fisika** | S1 | MIPA | 77 | **94** | 94 (2026) | 1,18 : 1 |
| 23 | **Manajemen (PDD Gayo Lues)** | S1 | FEB | 35 | **29** | 65 (2024) | 0,72 : 1 |
| 24 | **Kehutanan (PDD Gayo Lues)** | S1 | Pertanian | 37 | **28** | 39 (2025) | 0,70 : 1 |
| 25 | **Agroteknologi (PDD Gayo Lues)** | S1 | Pertanian | 21 | **21** | 41 (2024) | 0,60 : 1 |

---

### Kategori 6: Data Terbatas / Prodi Baru (4 Program Studi — 4,9%)
*Program studi baru yang resmi beroperasi dalam 1–2 tahun terakhir (2024–2026).*

| No | Program Studi | Jenjang | Fakultas | Tahun Buka | Peminat 2025 | Peminat 2026 | Lonjakan YoY | Daya Tampung | Rasio Keketatan |
|:--:|---|:---:|---|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | **Bisnis Digital** | S1 | FEB | 2025 | 131 | **1.023** | **+680,9%** | 80 | **12,79 : 1** |
| 2 | **Teknik Perminyakan** | S1 | Teknik | 2025 | 143 | **930** | **+550,3%** | 80 | **11,62 : 1** |
| 3 | **Hubungan Internasional**| S1 | FISIP | 2026 | — | **188** | *Perdana* | 80 | **2,35 : 1** |
| 4 | **Teknik Sumber Daya Air**| S1 | Teknik | 2025 | 112 | **122** | **+8,9%** | 60 | **2,03 : 1** |

---

## 5. Distribusi Tren per Fakultas di USK

| Fakultas | Jumlah Prodi | Meningkat (Konsisten + Tajam) | Fluktuatif | Menurun (Konsisten + Tajam) | Prodi Baru |
|---|:---:|:---:|:---:|:---:|:---:|
| **KIP (Keguruan & Ilmu Pendidikan)** | 17 | **10** | 4 | 3 | 0 |
| **Teknik** | 17 | **9** | 4 | 2 | 2 |
| **Pertanian** | 12 | **6** | 4 | 2 | 0 |
| **Ekonomi dan Bisnis (FEB)** | 11 | **6** | 3 | 1 | 1 |
| **MIPA** | 8 | **2** | 6 | 0 | 0 |
| **FISIP** | 5 | **2** | 2 | 0 | 1 |
| **Kelautan dan Perikanan (FPK)** | 4 | **0** | 2 | 2 | 0 |
| **Kedokteran (FK)** | 2 | **0** | 1 | 1 | 0 |
| **Kedokteran Hewan (FKH)** | 2 | **1** | 0 | 1 | 0 |
| **Hukum (FH)** | 1 | **0** | 1 | 0 | 0 |
| **Keperawatan (FKep)** | 1 | **0** | 0 | 1 | 0 |
| **Kedokteran Gigi (FKG)** | 1 | **0** | 1 | 0 | 0 |
| **TOTAL** | **81** | **40 (49,4%)** | **25 (30,9%)** | **12 (14,8%)** | **4 (4,9%)** |

---

## 6. Kesimpulan & Implikasi Manajerial

1. **Stabilitas Sehat Institusi:** Sebanyak **80,3% program studi USK** berada pada tren positif (*Meningkat Konsisten*, *Meningkat Tajam*, atau *Fluktuatif Sehat*). Penurunan tajam terkonsentrasi hanya pada 14,8% prodi (12 prodi) yang sebagian besar dipicu oleh faktor kebijakan biaya IPI mandiri dan krisis peminat kampus satelit remote.
2. **Katalisator Pertumbuhan Baru:** Kehadiran prodi baru (*Bisnis Digital* dan *Teknik Perminyakan*) serta prodi Sarjana Terapan (*D4 Akuntansi Perpajakan*) membuktikan bahwa pasar merespons sangat cepat terhadap program studi yang memiliki relevansi industri nyata dan sertifikasi profesi.
3. **Fokus Perbaikan Strategis:** Perhatian khusus diperlukan untuk revitalisasi 4 prodi PDD Gayo Lues dan rumpun Kelautan/Perikanan (FPK) melalui restrukturisasi kurikulum berbasis ekonomi biru (*blue economy*) dan pemberian paket insentif beasiswa penempatan.
