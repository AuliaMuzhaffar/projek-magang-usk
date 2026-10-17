# 📖 Kamus Data & Definisi Metrik (DATA_DICTIONARY)
**Repositori Analisis Peminatan, Daya Tampung, dan Jalur Masuk USK (2022–2026)**

Dokumen ini menjadi rujukan resmi mengenai arti setiap kolom, formula perhitungan, dan aturan bisnis analitik agar tidak terjadi kerancuan definisi di masa depan.

---

## 1. Definisi Rumus & Metrik Utama

| Nama Metrik | Formula / Rumus | Satuan | Makna Analitis |
| :--- | :--- | :---: | :--- |
| **Keketatan Seleksi** | `Peminat / Daya Tampung` | Rasio&nbsp;`(x:1)` | Mengukur intensitas persaingan pasar di hulu. Semakin tinggi rasio, semakin bergengsi/diminati prodi tersebut. |
| **Tingkat Keterisian (Fill Rate)** | `(Daftar Ulang / Daya Tampung) * 100` | Persen&nbsp;`(%)` | Mengukur efisiensi pemanfaatan kapasitas kuota universitas. Target ideal universitas adalah $\ge 80\%$. |
| **Tingkat Konversi (Yield Rate)** | `(Daftar Ulang / Lulus Seleksi) * 100` | Persen&nbsp;`(%)` | Mengukur komitmen calon mahasiswa yang lulus seleksi untuk melakukan registrasi ulang (kebocoran kelulusan). |
| **Defisit Bangku / Sisa Kursi** | `max(0, Daya Tampung - Daftar Ulang)` | Kursi / Orang | Jumlah kapasitas kuota yang terbuang sia-sia karena tidak terisi oleh mahasiswa baru. |
| **Tingkat Mundur / Gugur** | `Lulus Seleksi - Daftar Ulang` | Orang | Jumlah calon mahasiswa yang lulus tetapi menolak/tidak mengambil kursi USK. |

---

## 2. Aturan Khusus Program Studi Baru (< 5 Tahun Beroperasi)

Dalam analisis longitudinal 5 tahun (2022–2026), terdapat **6 program studi baru** yang belum memiliki data penuh selama 5 tahun:

1. **BISNIS DIGITAL** (FEB)
2. **HUBUNGAN INTERNASIONAL** (FISIP)
3. **TEKNIK LINGKUNGAN** (FT)
4. **TEKNIK PERMINYAKAN** (FT)
5. **TEKNIK SUMBER DAYA AIR** (FT)
6. **TEKNOLOGI INDUSTRI HASIL PERIKANAN** (FPK)

### 📌 Aturan Perhitungan Rata-rata (*Fair Evaluation Rule*):
- Untuk prodi baru, **rata-rata Fill Rate dan Keketatan dihitung berdasarkan JUMLAH TAHUN AKTIF BEROPERASI**, **bukan dibagi 5 tahun**.
- **Rasional Kebijakan:** Jika tahun-tahun sebelum prodi berdiri dihitung sebagai `0%`, maka nilai rata-rata prodi akan tertekan secara artifisial (penalti data kosong). Contoh:
  - *Teknik Lingkungan:* Aktif 2025 dan 2026. Rata-rata fill rate aktif = `(66,7% + 64,5%) / 2 = 65,6%`.
  - Jika dipaksa dibagi 5 tahun, nilainya akan menjadi `26,2%`, yang tidak mencerminkan daya serap aktual prodi tersebut saat menerima mahasiswa.
- Dalam grafik matriks strategi, disediakan 2 sudut pandang resmi:
  1. **Versi 66 Program Studi:** Menampilkan seluruh prodi S1 Kampus Utama.
  2. **Versi 60 Program Studi Mapan:** Mengecualikan 6 prodi baru untuk membandingkan kinerja program studi yang sudah beroperasi stabil selama 5 tahun penuh.

---

## 3. Ambang Batas & Definisi Matriks 4 Kuadran

| Kuadran | Ambang Batas Keketatan & Fill Rate | Warna Standar | Makna Posisi Pasar | Rekomendasi Kebijakan untuk Pimpinan |
| :---: | :---: | :---: | :--- | :--- |
| **Kuadran I<br>(Unggulan)** | Keketatan $\ge 4.0\text{x}$<br>Fill Rate $\ge 80.0\%$ | `#059669`<br>(Emerald Green) | **PRIMA & POPULER**<br>Peminat sangat tinggi dan kuota selalu terserap penuh. | Pertahankan kualitas akreditasi internasional, perkuat fasilitas laboratorium, dan buka kelas internasional / kerjasama industri. |
| **Kuadran II<br>(Stabil)** | Keketatan $< 4.0\text{x}$<br>Fill Rate $\ge 80.0\%$ | `#2563EB`<br>(Royal Blue) | **EQUILIBRIUM IDEAL**<br>Peminat moderat (niche market), namun kursi terisi penuh. | **JANGAN NAIKKAN KUOTA**. Pertahankan kapasitas saat ini agar keseimbangan pasar tidak terganggu. |
| **Kuadran III<br>(Belum Optimal)** | Keketatan $\ge 4.0\text{x}$<br>Fill Rate $< 80.0\%$ | `#D97706`<br>(Amber / Orange) | **KEBOCORAN HILIR**<br>Peminat sangat tinggi, namun banyak yang tidak daftar ulang. | **JANGAN PANGKAS KUOTA**. Buka fasilitas cicilan Uang Pangkal (IPI) dan percepat sistem pemanggilan cadangan mandiri. |
| **Kuadran IV<br>(Perlu Ditingkatkan)** | Keketatan $< 4.0\text{x}$<br>Fill Rate $< 80.0\%$ | `#E11D48`<br>(Rose Red) | **KRISIS KRONIS**<br>Peminat rendah dan kursi banyak terbuang kosong. | **WAJIB PANGKAS KUOTA 20%–40%** di SPMB 2027 untuk menaikkan rasio keketatan dan melindungi akreditasi prodi. |

---

## 4. Struktur Sheet File Master Excel
File: `data/master/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`

1. **`Master_Semua_Prodi`:** Gabungan seluruh jenjang (S1 Kampus Utama, D3 Vokasi, PSDKU Gayo Lues) dengan metrik komparatif.
2. **`S1_Kampus_Utama`:** 66 program studi sarjana reguler kampus Banda Aceh (rujukan utama visualisasi Matriks 4 Kuadran).
3. **`Diploma_3_Vokasi`:** 11 program studi diploma vokasi.
4. **`PSDKU_Gayo_Lues`:** 4 program studi di kampus luar domisili Gayo Lues.
5. **`Rincian_Jalur_Semua_Tahun`:** Data historis terdisagregasi per jalur seleksi (SNBP, SNBT, Mandiri) tahun 2022–2026.
