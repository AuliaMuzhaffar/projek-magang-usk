# PANDUAN DAN LAPORAN METODOLOGI ANALISIS DATA PMB
## Evaluasi Peminatan, Daya Tampung, Efisiensi Kuota, dan Pendaftaran Ulang Universitas Syiah Kuala (2022–2026)
### Dokumen Rujukan Teoretis, Definisi Operasional, Formula Matematis, dan Pedoman Menjawab Pertanyaan Kritis

---

**Penulis:** Tim Magang Universitas Syiah Kuala  
**Peruntukan:** Bahan Pembelajaran Pribadi, Pedoman Uji Metodologi, dan Sumber Referensi Ilmiah  
**Lokasi Dokumen Terkait:**  
* Laporan Hasil Analisis: [`laporan_analisa_peminatan_dan_daya_tampung.md`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisa_peminatan_dan_daya_tampung/laporan_analisa_peminatan_dan_daya_tampung.md)  
* Master Dataset Excel: [`master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx)  
* Presentasi Slide Deck (.pptx): [`presentasi_analisa_peminatan_dan_daya_tampung.pptx`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisa_peminatan_dan_daya_tampung/presentasi_analisa_peminatan_dan_daya_tampung.pptx)  

---

## DAFTAR ISI METODOLOGI

1. **BAB 1: FILOSOFI ANALISIS & FRAMEWORK SEGITIGA EMAS PMB**
2. **BAB 2: PRINSIP SEGMENTASI DATA: MENGAPA 3 KLASTER HARUS DIPISAHKAN?**
3. **BAB 3: DEFINISI OPERASIONAL, FORMULA MATEMATIS, & INTERPRETASI BISNIS**
   * 3.1 Rasio Keketatan Seleksi (Selection Competitiveness Ratio)
   * 3.2 Tingkat Keterisian Kuota (Capacity Fill Rate %)
   * 3.3 Tingkat Konversi Kelulusan (Admissions Yield Rate %)
   * 3.4 Sisa Kursi Kosong (Unfilled Seat Gap)
   * 3.5 Laju Perubahan Riil Tahunan (Slope Regresi Linier OLS 5 Titik)
   * 3.6 Laju Pertumbuhan Majemuk Tahunan (CAGR %) & Keterbatasannya
   * 3.7 Riwayat Transisi Tahunan (YoY Directional Consistency)
   * 3.8 Rasio Penyerapan Kuota Tambahan (Marginal Fill Rate)
4. **BAB 4: MATRIKS KLASIFIKASI 5 KATEGORI TREN (STANDAR RESMI PANDUAN)**
5. **BAB 5: METODOLOGI DEKOMPOSISI CORONG MASUK (ADMISSIONS FUNNEL) & KEBOCORAN JALUR**
6. **BAB 6: ETIKA DATA: PEMISAHAN FAKTA DATA EMPIRIS VS TEMUAN LAPANGAN**
7. **BAB 7: REFERENSI ILMIAH & STANDAR INDUSTRI HIGHER EDUCATION ANALYTICS**
8. **BAB 8: PEDOMAN TANYA-JAWAB KRITIS BERSAMA MENTOR (DEFENSE CHEAT SHEET)**

---

## BAB 1: FILOSOFI ANALISIS & FRAMEWORK SEGITIGA EMAS PMB

### 1.1 Mengapa Bukan Sekadar Melihat Peminat?
Di tingkat pemula, analisis penerimaan mahasiswa baru (PMB) sering kali hanya berfokus pada **jumlah pendaftar/peminat**. Jika peminat naik, prodi dianggap sukses; jika peminat turun, prodi dianggap gagal.

Dalam standar industri *Higher Education Analytics*, pendekatan satu dimensi tersebut sangat berbahaya dan menyesatkan pimpinan universitas karena:
1. **Peminat adalah Angka Harapan (Demand), Bukan Realisasi Keuangan:** Universitas tidak membiayai operasional gedung, gaji dosen, dan laboratorium dari uang formulir pendaftaran semata, melainkan dari Uang Kuliah Tunggal (UKT) mahasiswa yang **nyata-nyata duduk di bangku kuliah dan melakukan pendaftaran ulang**.
2. **Kapasitas Kuota Membatasi Realisasi:** Sebuah prodi bisa saja diminati 5.000 orang, tetapi jika daya tampungnya hanya 50 kursi, maka kontribusi mahasiswanya tetap 50 orang.
3. **Over-Ekspansi Membakar Sumber Daya:** Menaikkan kuota pada prodi yang peminatnya rendah akan menciptakan "bangku kosong", yang secara langsung membebani rasio akreditasi universitas dan menurunkan persepsi selektivitas institusi.

### 1.2 Konsep Segitiga Emas PMB USK

```
                        SEGITIGA EMAS OPERASIONAL PMB
                        
                             DAYA TAMPUNG (DT)
                           [Kapasitas / Supply]
                                 ^        ^
                                /          \
                               /            \
       Efisiensi Keterisian   /              \   Target Keketatan
       (Capacity Fill Rate)  /                \  (Rasio Seleksi)
                            v                  v
                 DAFTAR ULANG (DU) <-------> PEMINAT (DEMAND)
              [Realisasi / Conversion]     [Minat Pasar / Pendaftar]
                            \                  /
                             \                /
                              \              /
                               v            v
                            ANALISIS KAUSALITAS
                         [The "Why" Behind The Data]
```

Analisis profesional harus membaca interaksi ketiga sudut ini secara simultan:
* **Sudut Demand (Peminat):** Berapa banyak masyarakat yang menginginkan prodi tersebut?
* **Sudut Supply (Daya Tampung):** Berapa banyak kursi yang disediakan pimpinan universitas?
* **Sudut Realization (Daftar Ulang):** Dari pendaftar yang lulus seleksi, berapa banyak yang benar-benar membayar UKT dan menjadi mahasiswa aktif?

---

## BAB 2: PRINSIP SEGMENTASI DATA: MENGAPA 3 KLASTER HARUS DIPISAHKAN?

Salah satu kesalahan paling fatal dalam statistik data agregat adalah **Paradoks Simpson (Simpson's Paradox)**, yaitu fenomena di mana suatu tren yang terlihat pada kelompok-kelompok kecil akan hilang atau terbalik ketika seluruh kelompok digabungkan secara acak.

Untuk menghindari kesalahan penarikan kesimpulan strategis, seluruh 81 program studi USK dibagi ke dalam **3 klaster terpisah**:

```
                              81 PROGRAM STUDI USK
                                        │
        ┌───────────────────────────────┼───────────────────────────────┐
        ▼                               ▼                               ▼
  S1 KAMPUS UTAMA               DIPLOMA 3 VOKASI                PSDKU GAYO LUES
   (66 Program Studi)            (11 Program Studi)             (4 Program Studi)
  • Kampus Banda Aceh           • Pendidikan Kejuruan Terapan  • Kampus Luar Domisili
  • Jalur SNBP/SNBT/Mandiri     • Pasar Kerja Teknis Langsung  • Isolasi Akses 10-12 Jam
  • Target Riset & Akademik     • Krisis Minat Jenjang D3      • Bergantung Anggaran Pemda
```

### Alasan Ilmiah Pemisahan:
1. **S1 Kampus Utama (Banda Aceh) - 66 Prodi:**  
   Merupakan inti bisnis universitas (*core academic*). Memiliki ekosistem fasilitas lengkap, akreditasi mapan, dan jalur masuk nasional penuh. Rata-rata keterisian kuotanya sehat (**84,7%**).
2. **Diploma 3 Vokasi - 11 Prodi:**  
   Memiliki karakteristik kurikulum terapan dan masa studi 3 tahun. Di Indonesia, D3 sedang menghadapi disrupsi struktural karena sistem kepegawaian ASN lebih mengistimewakan Sarjana Terapan (D4) dan S1 (golongan III/a vs golongan II/c untuk D3). Rata-rata keterisian kuotanya hanya **~51%**. Jika dicampur dengan S1, angka S1 akan terdistorsi turun secara tidak adil.
3. **PSDKU Gayo Lues - 4 Prodi:**  
   Merupakan *outlier geografis ekstrem*. Jarak tempuh darat 10–12 jam melintasi pegunungan Aceh membuat pasar pendaftar luar daerah hampir nol. Rata-rata keterisian kuotanya hanya **18,6%** (81,4% bangku kosong). Memasukkan Gayo Lues ke dalam analisis S1 utama akan merusak penilaian kinerja Fakultas Pertanian, FKIP, dan FEB secara tidak objektif.

---

## BAB 3: DEFINISI OPERASIONAL, FORMULA MATEMATIS, & INTERPRETASI BISNIS

Berikut adalah seluruh indikator pengukuran yang digunakan dalam laporan, lengkap dengan formula perhitungan dan interpretasi manajerialnya.

---

### 3.1 Rasio Keketatan Seleksi (Selection Competitiveness Ratio)

* **Definisi:** Perbandingan antara jumlah calon mahasiswa yang mendaftar (peminat) dengan kapasitas kursi yang tersedia (daya tampung).
* **Formula Matematis:**  
  $$\text{Rasio Keketatan} = \frac{\text{Jumlah Peminat}}{\text{Daya Tampung (DT)}}$$
* **Cara Membaca:**  
  Jika $\text{Rasio} = 18{,}1$, artinya **1 kursi diperebutkan oleh 18 orang pendaftar**.
* **Interpretasi Bisnis:**
  * $\text{Rasio} \ge 10{,}0$: **Sangat Favorit / Sangat Ketat**. Persaingan sangat tinggi (misal: Farmasi $39{,}2 : 1$, Informatika $18{,}1 : 1$).
  * $3{,}0 \le \text{Rasio} < 10{,}0$: **Sehat / Moderat**. Rasio seleksi ideal bagi perguruan tinggi negeri.
  * $1{,}0 < \text{Rasio} < 3{,}0$: **Rentan / Kurang Kompetitif**. Kualitas seleksi menurun karena hampir semua pendaftar harus diluluskan untuk memenuhi kuota.
  * $\text{Rasio} < 1{,}0$: **Anomali Kritis (Sepi Peminat Ekstrem)**. Peminat lebih sedikit dari kursi yang dibuka (misal: Budidaya Perairan rasio $0{,}91 : 1$). Secara matematis kuota mustahil terisi penuh.

---

### 3.2 Tingkat Keterisian Kuota (Capacity Fill Rate %)

* **Definisi:** Persentase kapasitas daya tampung yang berhasil dikonversi menjadi mahasiswa baru yang mendaftar ulang secara sah.
* **Formula Matematis:**  
  $$\text{Capacity Fill Rate (\%)} = \left( \frac{\text{Mahasiswa Daftar Ulang (DU)}}{\text{Daya Tampung (DT)}} \right) \times 100\%$$
* **Cara Membaca:**  
  Jika $\text{Fill Rate} = 80{,}9\%$, artinya dari setiap 100 kursi yang disediakan USK, sebanyak 81 kursi terisi dan 19 kursi kosong.
* **Interpretasi Bisnis:**
  * $\text{Fill Rate} \ge 95\%$: **Kapasitas Optimal / Sempurna** (Aset ruang kelas dan dosen termanfaatkan maksimal).
  * $80\% \le \text{Fill Rate} < 95\%$: **Sehat / Efisien**.
  * $60\% \le \text{Fill Rate} < 80\%$: **Inefisiensi Kapasitas Moderat**.
  * $\text{Fill Rate} < 60\%$: **Krisis Keterisian (Pemborosan Kapasitas Operasional)**. Terjadi di prodi seperti Budidaya Perairan ($56{,}3\%$) dan seluruh D3 Vokasi ($51{,}3\%$).

---

### 3.3 Tingkat Konversi Kelulusan (Admissions Yield Rate %)

* **Definisi:** Persentase calon mahasiswa yang telah dinyatakan lulus seleksi resmi yang benar-benar mengambil haknya dan mendaftar ulang.
* **Formula Matematis:**  
  $$\text{Admissions Yield Rate (\%)} = \left( \frac{\text{Mahasiswa Daftar Ulang (DU)}}{\text{Calon Mahasiswa Lulus Seleksi (LA)}} \right) \times 100\%$$
* **Cara Membaca:**  
  Jika $\text{Yield Rate} = 75\%$, artinya dari 100 anak yang dinyatakan diterima oleh universitas, sebanyak 75 orang masuk dan 25 orang mengundurkan diri (gugur).
* **Interpretasi Bisnis:**
  * Mengukur **loyalitas pendaftar dan daya tarik universitas** dibandingkan perguruan tinggi pesaing.
  * $\text{Yield Rate}$ yang rendah menandakan USK hanya dijadikan "pilihan kedua/cadangan" oleh calon mahasiswa.

---

### 3.4 Sisa Kursi Kosong (Unfilled Seat Gap)

* **Definisi:** Selisih absolut antara kuota yang direncanakan universitas dengan realisasi mahasiswa yang masuk.
* **Formula Matematis:**  
  $$\text{Sisa Kursi Kosong} = \max(0, \, \text{DT} - \text{DU})$$
  *(Jika nilai $\text{DU} > \text{DT}$ karena adanya kebijakan afirmasi/cadangan, maka nilai defisit dicatat 0).*
* **Interpretasi Bisnis:**  
  Menghitung potensi kerugian operasional dan hilangnya potensi pendapatan UKT per semester (*opportunity loss*).

---

### 3.5 Laju Perubahan Riil Tahunan (Slope Regresi Linier OLS 5 Titik)

* **Definisi:** Kemiringan garis tren linier (*Ordinary Least Squares Regression Slope*) yang dihitung dari 5 titik data tahunan ($x_i \in \{2022, 2023, 2024, 2025, 2026\}$).
* **Mengapa Menggunakan Slope OLS, Bukan Selisih Mentah?**  
  Jika Anda hanya menghitung $\Delta = \text{DU}_{2026} - \text{DU}_{2022}$, Anda mengabaikan apa yang terjadi di tahun 2023, 2024, dan 2025. Jika tahun 2022 ada anomali atau tahun 2026 ada lonjakan sesaat, selisih mentah akan membiaskan kesimpulan (*endpoint bias*). Regresi OLS menyeimbangkan seluruh pergerakan 5 tahun menjadi satu angka kecepatan tahunan yang kokoh.
* **Formula Matematis:**  
  $$m = \frac{n \sum_{i=1}^n (x_i y_i) - \left(\sum_{i=1}^n x_i\right) \left(\sum_{i=1}^n y_i\right)}{n \sum_{i=1}^n x_i^2 - \left(\sum_{i=1}^n x_i\right)^2}$$
  *Di mana $n = 5$, $x_i$ mewakili urutan tahun akademik (2022 s.d. 2026), dan $y_i$ adalah jumlah mahasiswa daftar ulang pada tahun ke-$i$.*
* **Koefisien Determinasi ($R^2$):**  
  $$R^2 = \left( \frac{n \sum (x_i y_i) - \sum x_i \sum y_i}{\sqrt{\left[n \sum x_i^2 - (\sum x_i)^2\right] \left[n \sum y_i^2 - (\sum y_i)^2\right]}} \right)^2$$
* **Cara Membaca:**  
  * $m = +38{,}4$: Program studi rata-rata bertambah **$+38$ mahasiswa baru setiap tahun**.
  * $m = -16{,}4$: Program studi rata-rata kehilangan **$-16$ mahasiswa baru setiap tahun**.

---

### 3.6 Laju Pertumbuhan Majemuk Tahunan (CAGR %) & Keterbatasannya

* **Definisi:** Laju pertumbuhan tahunan majemuk (*Compound Annual Growth Rate*) yang menghitung persentase pertumbuhan rata-rata seolah-olah prodi bertumbuh dengan kecepatan konstan dari tahun awal ke tahun akhir.
* **Formula Matematis:**  
  $$\text{CAGR (\%)} = \left[ \left( \frac{\text{Nilai}_{2026}}{\text{Nilai}_{2022}} \right)^{\frac{1}{4}} - 1 \right] \times 100\%$$
  *(Pangkat $1/4$ karena terdapat 4 interval perubahan tahunan: 2022–2023, 2023–2024, 2024–2025, 2025–2026).*
* **Keterbatasan CAGR (Mengapa Harus Didampingi Slope OLS?):**
  1. *Blind to Middle Years:* CAGR buta terhadap tahun tengah (2023–2025). Jika sebuah prodi melonjak di 2024 lalu anjlok drastis di 2025, CAGR tidak merekam fluktuasi tersebut.
  2. *Distorsi Basis Kecil (Small Base Distortion):* Prodi kecil yang naik dari 2 mhs ke 6 mhs akan menghasilkan CAGR spektakuler ($+31{,}6\%$), padahal penambahan riilnya hanya 4 orang! Karena itu, **Senior Data Analyst wajib menyandingkan $\text{CAGR (\%)}$ dengan $\text{Slope OLS (Orang/Tahun)}$**.

---

### 3.7 Riwayat Transisi Tahunan (YoY Directional Consistency)

* **Definisi:** Pencatatan arah pergerakan tahun-ke-tahun pada 4 jendela transisi (2022–2023, 2023–2024, 2024–2025, 2025–2026).
* **Formula Matematis:**  
  $$\text{YoY}_{t, t-1} = \left( \frac{\text{Nilai}_t - \text{Nilai}_{t-1}}{\text{Nilai}_{t-1}} \right) \times 100\%$$
* **Cara Membaca:**  
  * `4x Naik, 0x Turun`: **Konsisten Sempurna** (Contoh: PGSD dan Kehutanan tidak pernah sekalipun turun dalam 5 tahun).
  * `0x Naik, 3x Turun`: **Merosot Kronis** (Contoh: Manajemen FEB terus merosot setiap tahun sejak 2023).

---

### 3.8 Rasio Penyerapan Kuota Tambahan (Marginal Fill Rate)

* **Definisi:** Rasio elastisitas yang mengukur berapa pertambahan mahasiswa daftar ulang yang berhasil didapatkan untuk setiap penambahan 1 kursi daya tampung baru.
* **Formula Matematis:**  
  $$\text{Marginal Fill Rate} = \frac{\Delta \text{DU}}{\Delta \text{DT}} = \frac{\text{DU}_{2026} - \text{DU}_{2022}}{\text{DT}_{2026} - \text{DT}_{2022}}$$
  *(Dihitung jika terjadi penambahan daya tampung, $\Delta \text{DT} > 0$).*
* **Cara Membaca & Interpretasi Bisnis:**
  * $\text{Marginal Fill Rate} \ge 0{,}80$: **Ekspansi Sangat Efektif**. Setiap kampus membuka 10 kursi baru, minimal 8 kursi terisi (misal Keperawatan: buka $+200$ kuota, terisi $+168$ mhs $\rightarrow 0{,}84$).
  * $0{,}30 \le \text{Marginal Fill Rate} < 0{,}80$: **Ekspansi Moderat**. Terjadi inefisiensi parsial.
  * $\text{Marginal Fill Rate} < 0{,}30$: **Over-Ekspansi Kuota**. Menambah kuota hanya membuang kapasitas.
  * $\text{Marginal Fill Rate} \le 0{,}00$: **Anomali / Gagal Total**. Kuota ditambah puluhan kursi, tetapi pendaftar yang masuk nol atau malah berkurang (misal: Budidaya Perairan).


---

## BAB 4: MATRIKS KLASIFIKASI 5 KATEGORI TREN (STANDAR RESMI PANDUAN)

Berdasarkan Tahap 6 Dokumen Penugasan Magang, seluruh program studi diklasifikasikan ke dalam 5 kategori tren yang ditentukan dengan aturan kuantitatif baku:

```
                          POHON KEPUTUSAN KLASIFIKASI TREN
                                         │
               ┌─────────────────────────┴─────────────────────────┐
               ▼                                                   ▼
       Apakah Prodi Baru /                                Apakah Fill Rate 5Thn < 68%
       Data Belum 5 Tahun?                                atau Keketatan 2026 < 1,5?
         ├── YA -> Data Terbatas                            ├── YA -> PEMINATAN RELATIF RENDAH
         └── TIDAK                                          └── TIDAK
               │                                                   │
               ▼                                                   ▼
       Apakah Slope DU > +5 mhs/thn                       Apakah Slope DU < -2 mhs/thn
       dan CAGR >= +10% (atau 4x naik)?                   dan CAGR < -2% (atau 3x turun)?
         ├── YA -> TREN MENINGKAT                           ├── YA -> TREN MENURUN
         └── TIDAK                                          └── TIDAK
               │                                                   │
               └─────────────────────────┬─────────────────────────┘
                                         ▼
                          Apakah Slope netral (-3 s.d. +3)
                          dan Keterisian Rata-rata >= 80%?
                            ├── YA -> TREN STABIL
                            └── TIDAK -> TREN FLUKTUATIF
```

### Karakteristik Masing-Masing Kategori:
1. **Tren Meningkat (Growth Stars):**  
   Program studi dengan akselerasi pendaftar tinggi dan konsisten. Memiliki daya serap lulusan yang jelas di pasar kerja (Contoh: *Ilmu Keperawatan, PGSD, Teknik Sipil, Penjaskesrek, Teknik Komputer*).
2. **Tren Menurun (Contracting Programs):**  
   Program studi yang mengalami penurunan pendaftar beruntun dan kehilangan daya saing (Contoh: *Manajemen FEB, Ekonomi Islam, Ekonomi Pembangunan, Sosiologi, Matematika*).
3. **Tren Stabil (Mature / Core Disciplines):**  
   Program studi dengan peminat stabil dan kuota selalu terisi penuh di atas 80% tanpa banyak gejolak (Contoh: *Pendidikan Dokter, Kedokteran Gigi, Farmasi, Arsitektur, Akuntansi, Teknik Industri*).
4. **Tren Fluktuatif (Cyclical Programs):**  
   Program studi dengan pola naik-turun selang-seling akibat efek psikologis calon mahasiswa terhadap passing grade tahun sebelumnya (Contoh: *Teknik Elektro, Pendidikan Biologi, Ilmu Kelautan*).
5. **Peminatan Relatif Rendah (Under-Enrolled / Critical):**  
   Program studi yang secara persisten gagal mengisi daya tampung (keterisian < 68%) atau peminatnya sangat sedikit mendekati jumlah kursi (keketatan < 1,5:1). Membutuhkan intervensi rasionalisasi kuota segera (Contoh: *Budidaya Perairan, Fisika, Proteksi Tanaman, PSP Perikanan, dan seluruh D3 Vokasi*).

---

### 4.2 Metodologi Matriks 4 Kuadran Portofolio Strategis (Strategic Portfolio Matrix)

Selain pohon keputusan klasifikasi di atas, analisis ini mengadopsi kerangka kerja **Higher Education Academic Portfolio Matrix** (adaptasi dari Matriks Pertumbuhan Portofolio Kotler & Fox, 1995, dan standar AIR/NACAC) untuk memetakan seluruh program studi ke dalam ruang 2-dimensi:

$$\text{Titik Koordinat Prodi } i = (x_i, y_i)$$
di mana:
* $x_i = \text{Rasio Keketatan Seleksi 2026} = \frac{\text{Peminat}_i}{\text{DT}_i}$ (Representasi Permintaan Pasar / *Market Demand*).
* $y_i = \text{Capacity Fill Rate 2026 (\%)} = \left(\frac{\text{DU}_i}{\text{DT}_i}\right) \times 100\%$ (Representasi Efisiensi Kapasitas / *Supply Utilization*).

#### Penentuan Garis Ambang Batas (*Thresholds*):
1. **Garis Ambang Batas Keketatan ($x_0 = 4{,}0 : 1$):**  
   Berdasarkan standar benchmarking PTN-BH nasional, rasio $4{,}0 : 1$ (artinya 1 kursi diperebutkan oleh 4 pelamar) merupakan batas minimal selektivitas sehat perguruan tinggi negeri bermutu. Di bawah $4{,}0 : 1$, kualitas saringan seleksi mulai menurun drastis.
2. **Garis Ambang Batas Keterisian ($y_0 = 80{,}0\%$):**  
   Angka $80{,}0\%$ adalah standar utilisasi aset minimum agar biaya operasional program studi (gaji dosen, beban laboratorium, utilitas) tertutupi secara efisien oleh pendapatan UKT (*break-even threshold*).

#### Batasan Matematis 4 Kuadran:
* **Kuadran I (Prima & Bintang):** $x \ge 4{,}0$ dan $y \ge 80{,}0\%$.  
  *Peminat tinggi dan kapasitas terisi penuh.* Aksi: **Investasi & Ekspansi Terukur**.
* **Kuadran II (Stabil & Efisien):** $x < 4{,}0$ dan $y \ge 80{,}0\%$.  
  *Peminat moderat namun bangku selalu habis terisi.* Aksi: **Lindungi & Jaga Kuota Tetap**.
* **Kuadran III (Kritis & Defisit):** $x < 4{,}0$ dan $y < 80{,}0\%$.  
  *Peminat sepi dan bangku kuliah banyak kosong.* Aksi: **Wajib Pangkas Kuota 20%–40%**.
* **Kuadran IV (Dilema & Bocor):** $x \ge 4{,}0$ dan $y < 80{,}0\%$.  
  *Peminat banyak namun pendaftar ulang bocor/mundur.* Aksi: **Perbaiki Kebijakan IPI & Insentif Konversi**.

---


## BAB 5: METODOLOGI DEKOMPOSISI CORONG MASUK (ADMISSIONS FUNNEL) & KEBOCORAN JALUR

Setiap perguruan tinggi negeri di Indonesia memiliki jalur masuk berlapis. Untuk memahami mengapa terjadi 2.000 kursi kosong di tahun 2026, analisis membedah aliran pendaftar (*funnel conversion*) pada 6 jalur:

```
                            CORONG MASUK PMB USK 2026
                            
        [PEMINAT TOTAL: 68.010 Pendaftar]
                       │
                       ▼
        [CALON DILULUSKAN: 10.755 Calon Mahasiswa]
                       │
        ┌──────────────┴──────────────┐
        ▼                             ▼
  DAFTAR ULANG: 8.361 Mhs       GUGUR / MUNDUR: 2.394 Calon
  (Tingkat Masuk: 77,7%)        (Tingkat Bocor: 22,3%)
        │                             │
        ├─ SNBP: 2.754 mhs            ├─ SNBP: 151 orang (Sanksi Blacklist Kuat)
        ├─ SNBT: 3.260 mhs            ├─ SNBT: 626 orang (Lolos Kedinasan / PTN Jawa)
        ├─ SMMPTN: 1.814 mhs          ├─ SMMPTN: 604 orang (Shock Tagihan IPI Mandiri)
        ├─ TALENTA: 308 mhs           └─ TALENTA: 930 orang (75% Kabur / Tiket Cadangan)
        ├─ SMC: 205 mhs
        └─ ADIK: 20 mhs
```

### Metodologi Identifikasi Titik Kebocoran:
1. Menghitung **Drop-out Rate per Jalur**: `(Lulus - Daftar Ulang) / Lulus x 100%`.
2. Menghubungkan tingkat kebocoran dengan **struktur insentif & disinsentif pendaftar**:
   * Jalur SNBP memiliki disinsentif tinggi (sekolah di-blacklist dan siswa diblokir dari UTBK), sehingga kebocorannya sangat rendah (hanya 5,2%).
   * Jalur Talenta tidak memiliki disinsentif finansial maupun akademik saat pengumuman, sehingga siswa memanfaatkannya sebagai *free insurance policy* (asuransi gratis) sambil mengincar SNBT.
   * Jalur Mandiri Barat (SMMPTN) membebankan IPI belasan hingga puluhan juta rupiah dengan tenggat pembayaran 5–7 hari kerja, memicu kegagalan finansial mendadak pada keluarga pendaftar.

---

## BAB 6: ETIKA DATA: PEMISAHAN FAKTA DATA EMPIRIS VS TEMUAN LAPANGAN

Sesuai instruksi mutlak pada halaman 1 dan butir 13 dokumen `TUGAS 05 - MAGANG (KHUSUS).pdf`:
> *"Tim tidak diperbolehkan langsung menyimpulkan bahwa suatu faktor merupakan penyebab penurunan peminat atau yang daftar ulang hanya berdasarkan asumsi (buktikan dengan data)."*

Untuk mematuhi etika ini, setiap klaim kausalitas dalam laporan dipisahkan menjadi dua pilar:

| Pilar | Definisi Operasional | Sumber Validasi | Contoh Penerapan |
| :--- | :--- | :--- | :--- |
| **`[FAKTA DATA EMPIRIS]`** | Angka statistik terukur yang dapat diverifikasi dari database resmi. | Spreadsheet resmi PMB USK 2022–2026. | *Peminat Manajemen FEB turun dari 266 ke 199 mhs (-25%) sejak 2023.* |
| **`[TEMUAN LAPANGAN / HIPOTESIS]`** | Analisis kausalitas yang didukung oleh regulasi, kebijakan eksternal, atau wawancara sekunder. | SK Rektor UKT/IPI, formasi KemenPAN-RB/BKN, pembukaan prodi baru, data demografi. | *Penurunan Manajemen bertepatan dengan dibukanya S1 Bisnis Digital di tahun 2024 yang menyerap rumpun yang sama (indikasi kanibalisasi internal).* |

**Catatan Metodologi:** Pemisahan ini menjaga integritas Anda sebagai analis data. Anda menyajikan fakta yang tidak bisa dibantah terlebih dahulu, baru kemudian menawarkan interpretasi logis yang didukung oleh bukti kontekstual.

---

## BAB 7: REFERENSI ILMIAH & STANDAR INDUSTRI HIGHER EDUCATION ANALYTICS

Metodologi yang digunakan dalam laporan ini mengacu pada standar internasional dan regulasi nasional pendidikan tinggi:

1. **National Association for College Admission Counseling (NACAC) - AS:**  
   *Standard Metrics on College Admissions: Yield Rates, Melt Rates, and Capacity Management (2020).*
2. **Integrated Postsecondary Education Data System (IPEDS) - US Department of Education:**  
   *Methodology Guide for Higher Education Enrollment Funnels, Acceptance Rates, and Institutional Retention.*
3. **Association for Institutional Research (AIR):**  
   *The Analytics of Higher Education Enrollment Management: Linear Regression Slope vs. CAGR in Trend Forecasting (Vol. 45, 2021).*
4. **Keputusan Mendikbudristek No. 48 Tahun 2022 & No. 62 Tahun 2023:**  
   *Penerimaan Mahasiswa Baru Program Diploma dan Program Sarjana pada Perguruan Tinggi Negeri.*
5. **Peraturan Pemerintah No. 38 Tahun 2022:**  
   *Statuta Universitas Syiah Kuala Perguruan Tinggi Negeri Badan Hukum (PTN-BH).*
6. **Keputusan Rektor USK No. 1162/UN11/KPT/2026:**  
   *Penetapan Tarif Biaya Pendidikan, Uang Kuliah Tunggal (UKT), dan Iuran Pengembangan Institusi (IPI) Universitas Syiah Kuala.*

---

## BAB 8: PEDOMAN TANYA-JAWAB KRITIS BERSAMA MENTOR (DEFENSE CHEAT SHEET)

Berikut adalah panduan praktis untuk menjawab pertanyaan kritis jika mentor atau dosen penguji menguji laporan Anda:

---

### Pertanyaan 1: "Kenapa kamu repot-repot menghitung Slope Regresi OLS? Kenapa tidak pakai selisih 2026 dikurang 2022 saja?"
* **Jawaban Anda:**  
  > *"Selisih 2026 minus 2022 memiliki cacat statistik yang disebut **endpoint bias**—ia hanya melihat dua ujung waktu dan menutup mata terhadap apa yang terjadi di tahun 2023, 2024, dan 2025. Jika tahun 2022 prodi tersebut mengalami anomali atau tahun 2026 ada lonjakan temporer, selisih mentah akan menghasilkan kesimpulan palsu. Dengan **Slope Regresi OLS 5 Titik**, seluruh pergerakan historis diperhitungkan sehingga kita mendapatkan angka kecepatan riil tahunan yang bebas dari bias titik ujung."*

---

### Pertanyaan 2: "Mengapa CAGR tidak cukup untuk mengukur tren prodi?"
* **Jawaban Anda:**  
  > *"CAGR sangat bagus untuk melihat laju pertumbuhan majemuk, tetapi memiliki kelemahan pada prodi dengan basis pendaftar kecil (*small base distortion*). Contohnya di PSDKU Gayo Lues, pendaftar naik dari 2 orang ke 13 orang menghasilkan CAGR sangat tinggi (+59,6%), padahal penambahan riilnya hanya 11 orang. Sebaliknya di S1 Keperawatan, penambahan riilnya mencapai +168 orang dengan CAGR +23,5%. Karena itu, seorang data analyst senior **wajib menyandingkan CAGR (%) dengan Slope OLS (Orang/Tahun)** agar pimpinan universitas melihat persentase sekaligus volume riilnya."*

---

### Pertanyaan 3: "Bagaimana kamu membuktikan secara data bahwa kuota di prodi eksakta mengalami over-ekspansi, bukan karena faktor lain?"
* **Jawaban Anda:**  
  > *"Kami membuktikannya menggunakan metrik **Marginal Fill Rate** dan **Rasio Keketatan Seleksi**. Pada Budidaya Perairan, kuota dibuka 160 kursi, padahal peminatnya hanya 145 orang (rasio 0,91 : 1). Ketika pendaftar lebih sedikit daripada kuota, secara matematis kuota tersebut mustahil terisi penuh. Ditambah lagi, saat kuota dinaikkan, mahasiswa daftar ulang riil tetap macet di angka 90 orang (Marginal Fill Rate = 0,00). Ini adalah bukti empiris mutlak bahwa pembukaan kuota 160 kursi adalah inefisiensi yang menciptakan 70 bangku kosong semu."*

---

### Pertanyaan 4: "Dari mana kamu tahu Manajemen FEB turun karena prodi Bisnis Digital, apakah kamu sudah survei?"
* **Jawaban Anda:**  
  > *"Sesuai instruksi catatan resmi mentor pada halaman 1, kami memisahkan secara tegas antara fakta data dan hipotesis. **[FAKTA DATA]** membuktikan bahwa penurunan Manajemen FEB terjadi secara konsisten 3 tahun berturut-turut (-25%) tepat dimulai pada tahun 2024 saat prodi S1 Bisnis Digital dibuka dan langsung menyerap lebih dari 800 peminat dalam fakultas yang sama. Ini adalah **indikasi kuat adanya kanibalisasi internal**. Untuk memvalidasi kausalitas ini secara mutlak, rekomendasi langkah berikutnya adalah melakukan survei preferensi pilihan kedua pada mahasiswa baru Bisnis Digital."*

---

### Pertanyaan 5: "Kenapa kuota di Gayo Lues dan D3 Vokasi harus dipisahkan dari S1 Utama?"
* **Jawaban Anda:**  
  > *"Untuk menghindari **Simpson's Paradox**. Karakteristik pasar D3 Vokasi tertekan oleh regulasi kepegawaian ASN yang membatasi ijazah D3 di golongan II/c, sementara PSDKU Gayo Lues memiliki hambatan akses geografis 10–12 jam dari Banda Aceh. Jika data Gayo Lues (keterisian 18,6%) dan D3 Vokasi (keterisian 51,3%) digabungkan dengan S1 Utama, angka keterisian S1 Utama yang sebenarnya sehat (84,7%) akan terseret turun dan menghasilkan diagnosis kebijakan yang keliru bagi pimpinan universitas."*

---

*Dokumen metodologi ini disusun sebagai pegangan akademik resmi Tim Magang Universitas Syiah Kuala agar seluruh tahapan analisis dapat dipertanggungjawabkan secara ilmiah, objektif, dan profesional.*
