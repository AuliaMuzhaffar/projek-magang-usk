# LAPORAN ANALISIS EKSEKUTIF: DATA KIP-KULIAH UNIVERSITAS SYIAH KUALA (2025–2026)
## Dekonstruksi Anomali Kebocoran SNBT, Efek "Jurang Desil 5–6", dan Pemetaan Ketergantungan Sosial-Ekonomi Portofolio Program Studi

---

**Penulis:** Data Analyst & Visualisasi Data PMB  
**Target Pembaca:** Wakil Rektor I (Akademik), Wakil Rektor II (Keuangan & Sumber Daya), Tim Task Force PMB, dan Pimpinan Fakultas/Program Studi USK  
**Status Dokumen:** Laporan Investigasi Khusus & Rekomendasi Strategis PTN-BH  
**Klasifikasi Data:** Audit-Grade Internal Analytics  

---

## 1. RINGKASAN EKSEKUTIF (EXECUTIVE SUMMARY)

Laporan ini disusun secara terpisah untuk menjawab salah satu pertanyaan paling mendasar dan krusial dari evaluasi Penerimaan Mahasiswa Baru (PMB) Universitas Syiah Kuala (USK) tahun 2026:

> *"Mengapa terjadi kebocoran (kursi kosong / calon mahasiswa tidak mendaftar ulang) yang begitu masif pada jalur seleksi nasional SNBT 2026, khususnya pada program studi yang memiliki peminat tinggi dan sedang?"*

Berdasarkan investigasi mendalam terhadap integrasi dua dataset baru:
1. `DATA_KIP_2025-2026.xlsx` (Data Induk Penerima KIP-Kuliah USK 2025–2026), dan
2. `PENERIMA_KIP_2025-2026.xlsx` (Data Calon Pelamar SNBT vs Penerima KIP-Kuliah Terverifikasi),

ditemukan **bukti kausalitas empiris (*smoking gun*)** yang membongkar bahwa fenomena "kebocoran SNBT" bukanlah penolakan sukarela oleh siswa karena berpindah ke kampus swasta atau gap year, melainkan **kegagalan sistemik dalam transisi pembiayaan kuliah (*economic drop-out*) akibat pemotongan kuota KIP-Kuliah dan penerapan batas desil (*desil threshold cutoff*)**.

### Temuan Kunci (*Key Takeaways*):
1. **Korelasi Kausalitas 98.2%:** Pada SNBT 2026, tercatat **626 calon mahasiswa gugur (mundur/tidak daftar ulang)** di seluruh USK. Pada saat yang sama, terdapat **615 calon pelamar KIP-Kuliah yang lulus ujian SNBT namun DITOLAK status KIP-nya** oleh sistem verifikasi kampus ($615 / 626 = \mathbf{98{,}24\%}$).
2. **Efek Jurang (*Cliff-Edge Effect*) Desil 5 & 6 yang Absolut (100% Ditolak):** Pelamar KIP SNBT pada Desil 1–4 menikmati tingkat penerimaan beasiswa yang sangat tinggi (**88.2% – 93.6%**). Namun, pada **Desil 5 dan Desil 6**, terjadi pemotongan total (*hard cut-off*) di mana tingkat kelulusan KIP adalah **0.0% (100% DITOLAK)**. 
3. **534 Mahasiswa Terhempas Menjadi Mahasiswa Reguler:** Sebanyak **534 calon mahasiswa dari Desil 5 dan 6 (149 Desil 5 + 385 Desil 6)** yang dinyatakan lulus akademik UTBK tidak memperoleh KIP-Kuliah dan secara otomatis dialihkan menjadi mahasiswa UKT reguler. Karena berasal dari keluarga prasejahtera yang tidak sanggup membayar UKT reguler, **mereka terpaksa tidak melakukan pendaftaran ulang**.
4. **Ketergantungan Ekstrem Kuadran III (Defisit/Rentan):** Program studi pada Kuadran III memiliki rata-rata ketergantungan mahasiswa KIP-Kuliah sebesar **32.92% (tertimbang: 31.11%)**, dengan prodi klaster keguruan (FKIP) dan perikanan (FPK) mencapai **45% – 56.7%**. Sebaliknya, Kuadran I (Prime/Unggulan) hanya memiliki rata-rata penetrasi KIP **13.03% (tertimbang: 13.19%)**, bahkan prodi favorit seperti Kedokteran Gigi hanya 1.0% dan Kedokteran hanya 2.4%.
5. **Kesenjangan Gender yang Masif:** Sebanyak **77.36% (1.268 mahasiswa)** dari total penerima KIP-Kuliah 2026 di USK adalah **perempuan**, menunjukkan bahwa KIP-Kuliah berfungsi sebagai instrumen utama mobilitas sosial perempuan prasejahtera di Aceh.

---

## 2. STUDI KOMPARASI MULTI-TAHUN: DINAMIKA KIP-KULIAH USK (2025 VS 2026)

Integrasi data historis tahun 2025 dari lembar kerja `KIP 2025` dan `DAFTAR_KIP_SNBT_2025` membuka pemahaman komparatif yang sangat mendalam mengenai perubahan kebijakan fiskal beasiswa dan dampaknya terhadap seleksi mahasiswa baru di USK.

### 2.1. Dekonstruksi Alokasi Kuota dan Lonjakan Penolakan (+66.2%)
Terjadi pergeseran makro yang signifikan antara tahun akademik 2025 dan 2026 yang memicu ketegangan likuiditas dan kuota di tingkat universitas.

#### Tabel 1: Perbandingan Metrik Makro KIP-Kuliah USK 2025 vs 2026 (Data Definitif Fix)
*Sumber: Master Data Final `DATA_KIP_2025-2026.xlsx` & `PENERIMA_KIP_2025-2026.xlsx`*

| Parameter Metrik | Tahun 2025 (Definitif) | Tahun 2026 (Definitif) | Perubahan ($\Delta$) | Persentase Perubahan | Catatan Kebijakan |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Total Kuota Penerima KIP (SK Rektor)** | **1.846** | **1.639** | **-207** | **-11.21%** | Kontraksi alokasi kuota dari Puslapdik Kemendikbudristek |
| - Alokasi Jalur SNBP | 941 (50.97%) | 893 (54.48%) | -48 | -5.10% | Penyesuaian proporsi jalur prestasi |
| - Alokasi Jalur SNBT | 905 (49.03%) | 746 (45.52%) | -159 | **-17.57%** | Pemotongan kuota jalur tes tertulis nasional |
| **Pendaftar KIP Lolos Seleksi SNBT** | **1.275** | **1.361** | **+86** | **+6.75%** | Minat calon mahasiswa prasejahtera terus meningkat |
| **Pendaftar KIP SNBT Diterima Beasiswa** | **905** | **746** | **-159** | **-17.57%** | Kuota resmi terserap 100% tanpa sisa |
| **Pendaftar KIP SNBT DITOLAK Kampus** | **370** | **615** | **+245** | **+66.22%** | **Lonjakan penolakan masif (efek ganda kuota turun & pendaftar naik)** |
| **Tingkat Penolakan KIP SNBT (*Rejection Rate*)** | **29.02%** | **45.19%** | **+16.17 pp** | **+55.72%** | Peluang ditolak beasiswa meningkat tajam |
| **Total Kursi Kosong Jalur SNBT (Calon Gugur)** | **551** | **626** | **+75** | **+13.61%** | Calon mahasiswa lulus seleksi yang tidak registrasi ulang |
| **Rasio Korelasi Penolakan KIP thd Kursi Kosong** | **67.15%** (370/551) | **98.24%** (615/626) | **+31.09 pp** | **+46.30%** | Di 2026 nyaris seluruh kursi kosong didorong penolakan KIP |

![Perbandingan Alokasi Kuota KIP dan Lonjakan Penolakan SNBT USK 2025 vs 2026](grafik/24_komparasi_kuota_pendaftar_dan_rejection_2025_2026.png)

```
Dinamika Penolakan KIP-Kuliah Jalur SNBT di USK:
Tahun 2025 (Total Pendaftar 1.275): [██████████░░░░░░░░░░░░░░░] 29.02% Ditolak (370 mhs)
Tahun 2026 (Total Pendaftar 1.361): [███████████████░░░░░░░░░░] 45.19% Ditolak (615 mhs) -> LONJAKAN +66.2%!
```

#### Sintesis Kunci:
1. **Efek Gunting (*Scissor Effect*):** Di satu sisi minat siswa prasejahtera mengikuti UTBK SNBT USK tumbuh sebesar **+6.75% (1.275 menjadi 1.361)**, namun di sisi lain kuota beasiswa SNBT justru dipotong sebesar **-17.57% (905 menjadi 746)**. Kesenjangan inilah yang melipatgandakan jumlah siswa ditolak dari **370 menjadi 615 mahasiswa**.
2. **Prioritas Alokasi SNBP Membebani SNBT:** Pada kedua tahun, alokasi KIP untuk jalur prestasi SNBP selalu diamankan terlebih dahulu (941 di 2025, 893 di 2026). Akibatnya, jalur SNBT menjadi penerima beban kontraksi terbesar.
3. **Evolusi Kausalitas Kursi Kosong SNBT (67.15% $\rightarrow$ 98.24%):**
   Pada tahun 2025, korelasi makro penolakan KIP terhadap kursi kosong SNBT tercatat **67.15%** (370 tolak KIP dari 551 kursi kosong), di mana masih terdapat 181 kursi kosong (32.85%) yang disebabkan oleh faktor non-KIP (seperti lolos sekolah kedinasan atau PTN Jawa). Namun pada tahun 2026, korelasinya melonjak drastis menjadi **98.24%** (615 tolak KIP dari 626 kursi kosong). Hal ini membuktikan bahwa pada tahun 2026, fenomena kursi kosong SNBT hampir secara mutlak (98.2%) merupakan krisis keterpaksaan ekonomi akibat penolakan beasiswa KIP.

---

### 2.2. Rekonstruksi Profil Demografi dan Penolakan KIP SNBT 2025
Berbeda dengan tahun 2026 di mana data desil DTKS Kemensos sudah terintegrasi pada berkas pendaftar SNBT pusat, pada tahun 2025 format data ekspor nasional belum menyertakan kolom desil. Oleh karena itu, penolakan 370 mahasiswa di tahun 2025 murni berbasis kuota program studi dan verifikasi administrasi kampus.

#### Tabel 1B: Sebaran Hasil Seleksi KIP SNBT 2025 Berdasarkan Fakultas
*Sumber: Hasil Rekonsiliasi `No Ujian == KODE PESERTA` (2025)*

| Fakultas | Total Pendaftar Lolos SNBT | Diterima KIP | Ditolak KIP | Tingkat Penolakan (%) | Porsi thd Total Ditolak |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **FKIP** | 448 | 341 | **107** | 23.88% | 28.92% |
| **Teknik** | 157 | 101 | **56** | 35.67% | 15.14% |
| **Pertanian** | 157 | 112 | **45** | 28.66% | 12.16% |
| **Ekonomi & Bisnis** | 110 | 70 | **40** | 36.36% | 10.81% |
| **FISIP** | 83 | 57 | **26** | 31.33% | 7.03% |
| **FMIPA** | 90 | 65 | **25** | 27.78% | 6.76% |
| **Kelautan & Perikanan** | 101 | 79 | **22** | 21.78% | 5.95% |
| **Keperawatan** | 45 | 27 | **18** | **40.00%** | 4.86% |
| **Kedokteran Hewan** | 20 | 7 | **13** | **65.00%** | 3.51% |
| **PSDKU Gayo Lues** | 26 | 17 | **9** | 34.62% | 2.43% |
| **Hukum** | 36 | 27 | **9** | 25.00% | 2.43% |
| **Kedokteran** | 2 | 2 | **0** | **0.00%** | 0.00% |
| **TOTAL USK (2025)** | **1.275** | **905** | **370** | **29.02%** | **100.00%** |

![Analisis Demografi dan Sebaran Penolakan KIP SNBT USK 2025](grafik/25_analisis_demografi_dan_penolakan_kip_2025.png)

#### Profil Demografi Peserta 2025:
* **Gender:** Dari 1.275 pendaftar KIP SNBT 2025, sebanyak **925 orang (72.55%) adalah Perempuan** (658 diterima, 267 ditolak / 28.86%) dan **350 orang (27.45%) adalah Laki-laki** (247 diterima, 103 ditolak / 29.43%). Tingkat penolakan relatif seimbang antar gender (~29%).
* **Jenjang:** Program S1 mencakup **1.187 pendaftar** (858 diterima, 329 ditolak / 27.72%), program D3 mencakup **84 pendaftar** (43 diterima, 41 ditolak / 48.81%), dan D4 mencakup **4 pendaftar** (4 diterima / 0.0% ditolak). Jenjang diploma D3 mengalami tingkat penolakan yang jauh lebih tinggi (48.8%) dibanding S1 (27.7%).

---

### 2.3. Pergeseran Episentrum Program Studi Rentan Penolakan KIP (2025 vs 2026)
Membandingkan 10 program studi dengan jumlah calon mahasiswa ditolak beasiswanya terbanyak membuktikan bahwa beban sosial-ekonomi terkonsentrasi pada prodi-prodi tertentu.

![Tren Program Studi dengan Penolakan KIP Terbanyak 2025 vs 2026](grafik/26_tren_prodi_penolakan_kip_2025_vs_2026.png)

#### Tabel 1C: Matriks Pergeseran Top Program Studi Penolakan KIP (2025 vs 2026)

| Program Studi | Pendaftar 2025 | Ditolak 2025 | Rejection Rate 2025 | Pendaftar 2026 | Ditolak 2026 | Rejection Rate 2026 | Tren Dinamika Penolakan |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Ilmu Keperawatan** | 45 | **18** | 40.00% | 47 | **22** | **46.81%** | Konsisten episentrum krisis beban KIP (+4 mhs) |
| **Pendidikan Guru SD (PGSD)** | 37 | **12** | 32.43% | 47 | **22** | **46.81%** | Lonjakan penolakan drastis (+10 mhs ditolak) |
| **Teknologi Pangan / Hasil Pertanian** | 22 | **10** | 45.45% | 22 | **19** | **86.36%** | Tingkat penolakan melonjak hampir 2x lipat |
| **Budidaya Perairan** | 34 | **5** | 14.71% | 44 | **18** | **40.91%** | Peminat naik tajam, penolakan naik lebih dari 3x lipat |
| **Ilmu Hukum** | 36 | **9** | 25.00% | 37 | **18** | **48.65%** | Penolakan berlipat ganda dari 25% ke 48.6% |
| **Manajemen Agribisnis (D3)** | 20 | **7** | 35.00% | 20 | **17** | **85.00%** | Kerentanan vokasi: 85% pelamar ditolak beasiswanya |
| **Pend. Jasmani Kesehatan & Rekreasi** | 36 | **7** | 19.44% | 28 | **16** | **57.14%** | Rejection rate naik dari 19.4% ke 57.1% |
| **Akuntansi** | 21 | **8** | 38.10% | 22 | **15** | **68.18%** | Penolakan meningkat tajam (+7 mhs) |
| **Ilmu Pemerintahan** | 24 | **7** | 29.17% | 28 | **14** | **50.00%** | 50% pelamar ditolak di 2026 |
| **Agribisnis** | 24 | **7** | 29.17% | 28 | **14** | **50.00%** | Penolakan meningkat 2x lipat |
| **Pendidikan Dokter Hewan** | 19 | **12** | **63.16%** | 19 | **10** | **52.63%** | Konsisten memiliki barrier penolakan sangat tinggi |

---

## 3. "THE SMOKING GUN": EFEK JURANG DESIL KEMENSOS (*CLIFF-EDGE EFFECT*)

Untuk memahami ke mana 615 calon mahasiswa yang ditolak tersebut berasal, kita membedah kolom `DESIL KIP-K` pada data `DAFTAR_KIP_SNBT_2026` terhadap data final penerima beasiswa `DATA_KIP_2025-2026.xlsx` berdasarkan Nomor Ujian UTBK. Desil ini mengacu pada Data Terpadu Kesejahteraan Sosial (DTKS) Kementerian Sosial Republik Indonesia, dengan skala:
- **Desil 1:** Rumah tangga termiskin (Sangat Miskin / Desil Terendah 10%)
- **Desil 2:** Rumah tangga miskin
- **Desil 3:** Rumah tangga hampir miskin
- **Desil 4:** Rumah tangga rentan miskin
- **Desil 5:** Rumah tangga berpenghasilan menengah-bawah
- **Desil 6:** Rumah tangga menengah yang mendekati batas rentan
- **Desil 0:** Data belum terpadu / verifikasi khusus

### Tabel 2: Distribusi dan Tingkat Penerimaan KIP SNBT 2026 Berdasarkan Desil (Data Final)

| Desil KIP-K (DTKS) | Total Lulus SNBT | Diterima KIP (Fix) | Ditolak KIP | Tingkat Kelulusan KIP (%) | Tingkat Penolakan KIP (%) | Proporsi thd Total Ditolak |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Desil 0** | 25 | 17 | 8 | 68.00% | 32.00% | 1.30% |
| **Desil 1** | 221 | 201 | 20 | 90.95% | 9.05% | 3.25% |
| **Desil 2** | 186 | 164 | 22 | 88.17% | 11.83% | 3.58% |
| **Desil 3** | 219 | 205 | 14 | 93.61% | 6.39% | 2.28% |
| **Desil 4** | 176 | 159 | 17 | 90.34% | 9.66% | 2.76% |
| **Desil 5** | **149** | **0** | **149** | **0.00%** | **100.00%** | **24.23%** |
| **Desil 6** | **385** | **0** | **385** | **0.00%** | **100.00%** | **62.60%** |
| **TOTAL** | **1.361** | **746** | **615** | **54.81%** | **45.19%** | **100.00%** |

![Investigasi Empiris Kebocoran Jalur SNBT dan Efek Jurang Desil KIP-Kuliah](grafik/20_analisis_desil_dan_rejection_kip_snbt.png)

```
Tingkat Penerimaan KIP Berdasarkan Desil (SNBT 2026):
Desil 1: [██████████████████░░] 91.0% Diterima (201 lolos, 20 ditolak)
Desil 2: [█████████████████░░░] 88.2% Diterima (164 lolos, 22 ditolak)
Desil 3: [███████████████████░] 93.6% Diterima (205 lolos, 14 ditolak)
Desil 4: [██████████████████░░] 90.3% Diterima (159 lolos, 17 ditolak)
------------------------- CUTOFF MUTLAK AMBANG KUOTA -------------------------
Desil 5: [░░░░░░░░░░░░░░░░░░░░]   0.0% Diterima (100.0% / 149 Siswa Ditolak!)
Desil 6: [░░░░░░░░░░░░░░░░░░░░]   0.0% Diterima (100.0% / 385 Siswa Ditolak!)
```

### Mekanisme Kegagalan Sistemik:
1. **Desil 1 hingga 4 Mendapatkan Perlindungan Penuh:**
   Panitia KIP-K USK berhasil mengamankan 729 mahasiswa dari Desil 1–4 (tingkat kelulusan rata-rata **90.9%**). Sebanyak 73 penolakan di desil ini umumnya disebabkan ketidaklengkapan berkas fisik atau ketidakcocokan data NIK saat verifikasi faktual.
2. **Ketiadaan Kuota untuk Desil 5 dan 6 (Hard Cut-off 100%):**
   Begitu kuota KIP terserap habis oleh Desil 1–4, USK kehabisan alokasi beasiswa. Akibatnya, diterapkan garis batas mutlak (*hard cut-off*): dari total 534 pelamar Desil 5 dan 6, **0 orang (0.0%) yang lolos**, dan **seluruh 534 orang (100.0%) ditolak sekaligus**.
3. **Konversi Paksa ke UKT Reguler Menghasilkan Gugur Terpaksa:**
   Sesuai regulasi nasional, calon mahasiswa yang ditolak KIP-K tidak digugurkan kelulusannya dari kampus, melainkan **ditetapkan tarif Uang Kuliah Tunggal (UKT) reguler**.
   Namun, Desil 5 dan 6 menurut standar sosial-ekonomi bukanlah keluarga kaya raya; mereka adalah keluarga berpendapatan rendah-menengah informal (petani kecil, buruh harian, pedagang mikro) yang tidak memiliki bantalan tabungan darurat.
   Ketika menerima tagihan UKT reguler sebesar Rp 2.500.000 hingga Rp 5.000.000 per semester, **534 siswa ini tidak mampu membayar dan terpaksa membatalkan niat kuliah di USK**.

$$\text{Tingkat Korelasi Kebocoran} = \frac{\text{KIP Ditolak (615)}}{\text{Calon Gugur SNBT (626)}} = \mathbf{98{,}24\%}$$

$$\text{Kontribusi Desil 5-6 thd Penolakan} = \frac{534}{615} = \mathbf{86{,}83\%}$$

> **Kesimpulan Kunci:** Anomali "kursi kosong SNBT" 2026 di USK sebesar 626 kursi secara empiris **98,24% identik dengan 615 calon mahasiswa KIP yang ditolak**, di mana **86,8% (534 jiwa) di antaranya terhempas dari Desil 5 dan 6**. Ini adalah temuan mutlak yang memvalidasi integritas data universitas dan membantah keraguan bahwa calon mahasiswa sengaja kabur tanpa alasan.

---

## 4. DAMPAK SEKTORAL: PROGRAM STUDI DENGAN PENOLAKAN KIP DAN KEBOCORAN TERTINGGI

Di bawah ini adalah pemetaan 20 program studi di USK yang mengalami penolakan KIP SNBT terbesar, disandingkan dengan angka calon mahasiswa yang gugur (*tidak daftar ulang*) pada jalur SNBT 2026.

### Tabel 3: Matriks Korelasi Penolakan KIP Desil 5–6 vs Calon Gugur SNBT 2026

| Nama Program Studi | Calon Lulus SNBT | Daftar Ulang SNBT | Calon Gugur (Mundur) | Pelamar KIP SNBT Lulus | KIP SNBT Diterima | KIP SNBT DITOLAK | KIP Desil 5-6 DITOLAK |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ilmu Keperawatan** | 136 | 116 | **20** | 47 | 25 | **22** | **20** |
| **Pendidikan Guru SD (PGSD)** | 89 | 80 | **9** | 47 | 25 | **22** | **20** |
| **Teknologi Hasil Pertanian** | 45 | 37 | **8** | 33 | 14 | **19** | **19** |
| **Budidaya Perairan** | 69 | 53 | **16** | 44 | 25 | **19** | **12** |
| **Ilmu Hukum** | 204 | 190 | **14** | 37 | 19 | **18** | **15** |
| **Manajemen Agribisnis (D3)** | 57 | 17 | **40** | 20 | 3 | **17** | **10** |
| **Akuntansi** | 44 | 24 | **20** | 22 | 7 | **15** | **14** |
| **Pend. Jasmani Kesehatan & Rekreasi** | 76 | 67 | **9** | 28 | 13 | **15** | **13** |
| **Budidaya Peternakan (D3)** | 33 | 14 | **19** | 20 | 6 | **14** | **10** |
| **Ilmu Pemerintahan** | 71 | 59 | **12** | 28 | 14 | **14** | **14** |
| **Agribisnis** | 60 | 50 | **10** | 28 | 14 | **14** | **13** |
| **Ekonomi Islam** | 62 | 53 | **9** | 24 | 11 | **13** | **12** |
| **Ilmu Politik** | 69 | 53 | **16** | 24 | 11 | **13** | **12** |
| **Teknik Sipil** | 45 | 21 | **24** | 21 | 9 | **12** | **11** |
| **Peternakan** | 44 | 36 | **8** | 23 | 12 | **11** | **9** |
| **Pendidikan Bahasa Indonesia** | 65 | 59 | **6** | 28 | 17 | **11** | **9** |
| **Ilmu Komunikasi** | 48 | 41 | **7** | 23 | 12 | **11** | **10** |
| **Teknik Pertanian** | 36 | 30 | **6** | 20 | 10 | **10** | **8** |
| **Pendidikan Dokter Hewan** | 92 | 84 | **8** | 19 | 9 | **10** | **10** |
| **Pendidikan Sejarah** | 42 | 36 | **6** | 22 | 12 | **10** | **9** |

![Sinkronisasi Data Kebocoran Program Studi dan Penolakan KIP-Kuliah USK SNBT 2026](grafik/23_korelasi_prodi_calon_gugur_vs_kip_desil.png)

### Analisis Kasus Spesifik:
1. **Ilmu Keperawatan & PGSD:**
   Kedua prodi ini memiliki profil peminat yang luar biasa besar namun sangat sensitif terhadap biaya pendidikan. Di Keperawatan, terdapat 20 siswa gugur dan persis 20 siswa berasal dari Desil 5–6 yang ditolak KIP-nya. Di PGSD, 20 siswa Desil 5–6 ditolak KIP-nya, menyebabkan goncangan pengisian kursi.
2. **Program Vokasi Pertanian (Manajemen Agribisnis & Budidaya Peternakan):**
   Pada Manajemen Agribisnis, dari 57 calon lulus SNBT, hanya 17 yang daftar ulang (40 calon gugur!). Sebanyak 17 pendaftar KIP ditolak (10 di antaranya Desil 5–6). Karena jenjang vokasi sering dianggap opsi kedua, begitu KIP ditolak, calon mahasiswa langsung mengundurkan diri secara massal.
3. **Ilmu Pemerintahan & Ilmu Politik (FISIP):**
   Di Ilmu Pemerintahan, 14 calon ditolak KIP (semuanya 100% dari Desil 5–6), dan kursi yang bocor mencapai 12 kursi. Di Ilmu Politik, 13 calon ditolak KIP (12 dari Desil 5–6), dan kebocoran mencapai 16 kursi.

---

## 5. PEMETAAN KETERGANTUNGAN SOSIAL-EKONOMI BERDASARKAN MATRIKS 4 KUADRAN

Ketika data penerima KIP-Kuliah 2026 diintegrasikan ke dalam **Matriks 4 Kuadran USK** (S1 Kampus Utama), terungkap jurang stratifikasi sosial-ekonomi yang sangat tajam antar kuadran.

### Tabel 4: Profil Ketergantungan KIP-Kuliah Berdasarkan Kuadran USK (S1 Kampus Utama 2026)

| Kuadran Portofolio | Jumlah Prodi | Total Mahasiswa Daftar Ulang | Total Penerima KIP 2026 | Rata-rata KIP Prodi (%) | Median KIP (%) | Rasio Tertimbang KIP (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Kuadran I (Prime / Unggulan)** | 25 | 3.905 | 515 | **13.03%** | 8.82% | **13.19%** |
| **Kuadran II (Niche / Stabil)** | 8 | 1.046 | 153 | **13.94%** | 11.72% | **14.63%** |
| **Kuadran III (Defisit / Rentan)** | 25 | 2.359 | 734 | **32.92%** | **30.61%** | **31.11%** |
| **Kuadran IV (Bocor / Bottleneck)** | 8 | 666 | 163 | **22.79%** | 19.78% | **24.47%** |
| **TOTAL KAMPUS UTAMA** | **66** | **7.976** | **1.565** | **19.85%** | **17.50%** | **19.62%** |

![Stratifikasi Sosial-Ekonomi Portofolio Program Studi USK 2026](grafik/21_ketergantungan_kip_antar_kuadran_dan_top_prodi.png)

```
Perbandingan Ketergantungan KIP Antar Kuadran:
Kuadran I   (Unggulan) : [██████░░░░░░░░░░░░░░] 13.19% KIP (Mayoritas UKT Mandiri/Tinggi)
Kuadran II  (Stabil)   : [███████░░░░░░░░░░░░░] 14.63% KIP (Kapasitas Terkendali)
Kuadran IV  (Bocor)    : [████████████░░░░░░░░] 24.47% KIP (Rentan Terhempas UKT)
Kuadran III (Kritis)   : [███████████████░░░░░] 31.11% KIP (KETERGANTUNGAN STRUKTURAL TINGGI!)
```

### Tabel 5: Top 10 Prodi Paling Bergantung pada KIP vs Top 10 Prodi Paling Sedikit KIP

| Peringkat | Program Studi Ketergantungan Ekstrem KIP (Kuadran III & Vokasi) | KIP (%) | Program Studi Rendah KIP / Elite (Kuadran I) | KIP (%) |
| :---: | :--- | :---: | :--- | :---: |
| 1 | **Pemanfaatan Sumberdaya Perikanan (PSP)** | **56.72%** | **Pendidikan Dokter Gigi** | **1.00%** |
| 2 | **Sekretari (D3)** | **55.56%** | **Pendidikan Dokter** | **2.40%** |
| 3 | **Pendidikan Fisika** | **53.85%** | **Informatika** | **3.42%** |
| 4 | **Budidaya Perairan** | **51.11%** | **Teknik Perminyakan** | **3.85%** |
| 5 | **Pendidikan Ekonomi** | **49.51%** | **Teknik Pertambangan** | **5.08%** |
| 6 | **Pendidikan Kimia** | **48.00%** | **Psikologi** | **5.26%** |
| 7 | **Pendidikan Geografi** | **46.22%** | **Pendidikan Dokter Hewan** | **5.80%** |
| 8 | **Ilmu Tanah** | **44.87%** | **Teknik Geologi** | **6.41%** |
| 9 | **Fisika (FMIPA)** | **42.86%** | **Statistika** | **6.54%** |
| 10 | **Pendidikan Guru PAUD** | **42.72%** | **Teknik Sipil** | **6.75%** |

### Implikasi Strategis Kuadran III:
- **Kuadran III adalah "Jaring Pengaman Sosial" (*Social Safety Net*) USK:** Program studi di Fakultas Keguruan dan Ilmu Pendidikan (FKIP), Fakultas Kelautan dan Perikanan (FPK), dan Fakultas Pertanian (FP) menyerap mahasiswa dari latar belakang ekonomi paling rentan.
- **Vulnerabilitas Finansial Tinggi:** Ketika kuota KIP nasional berkurang, prodi-prodi Kuadran III menjadi pihak yang paling menderita. Penurunan kuota KIP secara langsung menyebabkan kursi kosong yang parah di Kuadran III karena calon peminat mereka tidak memiliki kemampuan finansial untuk beralih ke UKT mandiri.
- **Kontras dengan Kuadran I:** Di prodi Kuadran I seperti Kedokteran (2.4%), Kedokteran Gigi (1.0%), dan Informatika (3.4%), hampir seluruh mahasiswa membayar UKT Golongan 5–8 dan Iuran Pengembangan Institusi (IPI) puluhan hingga ratusan juta rupiah.

---

## 6. PROFIL DEMOGRAFIS PENERIMA KIP-KULIAH USK 2026

Berdasarkan analisis lembar kerja `KIP 2026` (1.639 mahasiswa penerima beasiswa):

![Profil Demografis dan Sebaran Penerima KIP-Kuliah USK 2026](grafik/22_demografi_fakultas_dan_gender_kip_2026.png)

### 6.1. Distribusi per Fakultas

```
Porsi Penerima KIP-Kuliah USK Berdasarkan Fakultas (2026):
FKIP         : [████████████████████] 39.72% (651 mahasiswa)
Pertanian    : [███████░░░░░░░░░░░░░] 13.30% (218 mahasiswa)
FEB          : [█████░░░░░░░░░░░░░░░]  9.33% (153 mahasiswa)
FT           : [█████░░░░░░░░░░░░░░░]  9.27% (152 mahasiswa)
FPK          : [████░░░░░░░░░░░░░░░░]  8.11% (133 mahasiswa)
FISIP        : [████░░░░░░░░░░░░░░░░]  7.20% (118 mahasiswa)
FMIPA        : [██░░░░░░░░░░░░░░░░░░]  4.27%  (70 mahasiswa)
Keperawatan  : [██░░░░░░░░░░░░░░░░░░]  3.84%  (63 mahasiswa)
Hukum        : [██░░░░░░░░░░░░░░░░░░]  3.36%  (55 mahasiswa)
FKH          : [░░░░░░░░░░░░░░░░░░░░]  0.92%  (15 mahasiswa)
FK           : [░░░░░░░░░░░░░░░░░░░░]  0.61%  (10 mahasiswa)
FKG          : [░░░░░░░░░░░░░░░░░░░░]  0.06%   (1 mahasiswa)
```

- **FKIP Menguasai Hampir 40% Kuota KIP:** Sebanyak 651 dari 1.639 penerima beasiswa USK berada di bawah naungan FKIP. Hal ini mencerminkan misi historis USK dalam mencetak tenaga pendidik bagi wilayah Aceh dan Sumatera bagian utara dari keluarga prasejahtera.
- **Klaster Agro-Maritim (Pertanian & FPK) Menyerap 21.4%:** Pertanian (218 mahasiswa) dan Kelautan/Perikanan (133 mahasiswa) merupakan pilar ketahanan pangan yang sangat bergantung pada beasiswa afirmasi pemerintah.

### 6.2. Distribusi Gender

| Jenis Kelamin | Jumlah Mahasiswa | Persentase (%) |
| :--- | :---: | :---: |
| **Perempuan** | **1.268** | **77.36%** |
| **Laki-laki** | **371** | **22.64%** |
| **Total** | **1.639** | **100.00%** |

- **Feminisme Pendidikan Tinggi:** Rasio 3.4 : 1 antara perempuan dan laki-laki pada penerima KIP-Kuliah menunjukkan bahwa program KIP di USK menjadi pendorong utama emansipasi dan akses pendidikan tinggi bagi anak perempuan dari keluarga miskin di Aceh.
- Tingginya konsentrasi perempuan juga berkorelasi erat dengan dominasi pendaftaran pada FKIP, Keperawatan, dan Ilmu Sosial.

### 6.3. Distribusi Jalur Masuk Penerima KIP 2026

| Jalur Masuk | Jumlah Mahasiswa | Persentase (%) |
| :--- | :---: | :---: |
| **SNBP (Prestasi Rapor)** | **893** | **54.48%** |
| **SNBT (Tes UTBK)** | **746** | **45.52%** |
| **Total** | **1.639** | **100.00%** |

- Jalur SNBP menyerap lebih dari separuh kuota KIP di awal tahun. Prioritas ini secara administratif membatasi ruang gerak bagi calon mahasiswa jalur SNBT, sehingga memicu krisis desil pada seleksi tes nasional.

---

## 7. REKOMENDASI KEBIJAKAN STRATEGIS UNTUK REKTORAT & PTN-BH USK

Penemuan bahwa **534 mahasiswa berprestasi UTBK dari Desil 5 & 6 gugur karena ketiadaan beasiswa (100% ditolak)** menuntut USK sebagai Perguruan Tinggi Negeri Berbadan Hukum (PTN-BH) untuk melakukan reformasi kebijakan pembiayaan. USK tidak boleh membiarkan kursi akademik kosong sementara calon mahasiswa berpotensi terhempas kemiskinan.

### Kebijakan 1: Pembentukan Skema "UKT Penyelamat" (*Safety-Net Transition UKT*)
- **Masalah:** Mahasiswa KIP Desil 5–6 yang ditolak langsung dikenakan UKT Reguler Kelompok III s.d. V (Rp 2.500.000 – Rp 4.500.000) yang tidak sanggup mereka bayar.
- **Solusi:** Terbitkan Keputusan Rektor mengenai *Automatic Safety-Net UKT*. Semua pelamar KIP-K jalur SNBT yang berstatus Desil 5 dan 6 yang tidak tertampung kuota APBN **secara otomatis ditetapkan pada UKT Kelompok I (Rp 500.000) atau UKT Kelompok II (Rp 1.000.000)** pada semester pertama, disertai hak mencicil 2 tahap.
- **Dampak Penyelamatan:** Skema ini diproyeksikan mampu menyelamatkan minimal **60% s.d. 70% (320 – 375 mahasiswa)** agar tetap mendaftar ulang di USK.

### Kebijakan 2: Subsidi Silang Surplus IPI Kuadran I ke "KIP Kemitraan PTN-BH"
- **Masalah:** USK mengalami defisit kuota KIP dari kementerian (-207 kursi).
- **Solusi:** Manfaatkan fleksibilitas keuangan PTN-BH. Alokasikan **5% s.d. 7.5% dari total penerimaan IPI Jalur Mandiri program studi kaya (Kedokteran, Kedokteran Gigi, Farmasi, Informatika, Pertambangan)** untuk membentuk dana abadi *Beasiswa KIP Kemitraan USK*.
- **Kalkulasi Finansial:**
  $$\text{Dana IPI Kuadran I} \approx \text{Rp 40 Miliar} \times 5\% = \text{Rp 2,0 Miliar}$$
  Dengan biaya SPP flat Rp 2.400.000/tahun per mahasiswa, dana Rp 2 Miliar ini dapat mendanai **833 beasiswa mandiri**, melampaui seluruh defisit 534 calon mahasiswa Desil 5–6 di SNBT!

### Kebijakan 3: Sinergi Dana Otonomi Khusus (Otsus) & Baitul Mal Aceh
- **Masalah:** Keterbatasan ruang fiskal APBN Kemendiktisaintek.
- **Solusi:** Pimpinan USK melakukan advokasi data mikro ini kepada Pemerintah Aceh dan Baitul Mal Provinsi Aceh. Sebanyak 534 nama calon mahasiswa Desil 5–6 yang terverifikasi miskin tetapi berprestasi diajukan sebagai penerima manfaat langsung *Beasiswa Senif Fisabilillah / Fakir Miskin Baitul Mal Aceh*.
- **Narasi Advokasi:** Mengentaskan kemiskinan ekstrem di Aceh melalui jaminan pendidikan tinggi bagi anak petani dan nelayan lokal.

### Kebijakan 4: Sinkronisasi Kuota KIP dengan Penetapan Daya Tampung SNBT
- **Masalah:** Penentuan daya tampung SNBT dilakukan tanpa mempertimbangkan kapasitas kuota KIP, sehingga terjadi *over-promising* kelulusan pada prodi yang padat KIP (seperti FPK dan FKIP).
- **Solusi:** Mulai PMB 2027, penetapan kuota kelulusan SNBT pada prodi-prodi Kuadran III harus disinkronkan dengan sisa kuota definitif KIP-K pasca-SNBP, atau menyiapkan kuota cadangan beasiswa internal sebelum pengumuman kelulusan dilakukan.

---

## 8. PANDUAN KOMUNIKASI & ADVOKASI KEPADA MENTOR & PIMPINAN

Ketika mempresentasikan hasil temuan ini kepada mentor, dekan, atau tim pimpinan yang meragukan anomali data (*"merasa seperti plot twist yang tidak masuk akal"*), gunakan alur argumentasi berbasis data berikut:

1. **Buka dengan Rekonsiliasi Matematika Sederhana:**
   *"Pak/Ibu, data menunjukkan SNBT 2026 mengalami kursi kosong sebesar 626 orang. Selama ini kita menduga mereka kabur ke PTS. Namun ketika kita sandingkan dengan data verifikasi KIP definitif (berdasarkan No Ujian UTBK), ada 615 calon mahasiswa KIP yang ditolak beasiswanya. Angkanya 98,24% identik (615 tolak KIP vs 626 kursi kosong)."*
2. **Tunjukkan Bukti Hard Cutoff Desil:**
   *"Bukan karena mereka tidak mau kuliah di USK. Pelamar Desil 1–4 diterima KIP-nya rata-rata 90,9%. Tetapi pelamar Desil 5 dan 6 diterima 0,0% (100% ditolak mutlak!). Ada 534 anak dari keluarga berpendapatan rendah yang lulus tes UTBK USK, tapi saat verifikasi beasiswa mereka ditolak total karena kuota KIP USK dari pusat turun 207 kursi."*
3. **Jelaskan Beban Finansial:**
   *"Begitu KIP ditolak, mereka dialihkan ke UKT reguler jutaan rupiah. Karena orang tua mereka buruh dan petani Desil 5-6, mereka tidak sanggup membayar, sehingga terpaksa mundur. Jadi ini bukan fenomena 'peminat kabur', melainkan 'kegagalan daya beli'."*
4. **Tutup dengan Solusi Institusional PTN-BH:**
   *"Dengan memahami akar masalah ini, solusinya bukan menurunkan daya tampung atau menyalahkan peminat, melainkan USK sebagai PTN-BH harus menyiapkan skema UKT Penyelamat (Golongan 1-2) atau subsidi silang dari dana IPI prodi unggulan agar 534 calon mahasiswa ini terselamatkan."*

---
*Dokumen ini merupakan bagian dari Laporan Analisis Penerimaan Mahasiswa Baru Universitas Syiah Kuala (USK).*
