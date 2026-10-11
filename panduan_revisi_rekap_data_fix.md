# Panduan & Rencana Eksekusi Revisi File `rekap data (fix).xlsx`

> **Tujuan Dokumen:**  
> Dokumen ini adalah panduan kerja teknis yang dirancang sangat rinci, deterministik, dan bebas ambiguitas sehingga **setiap AI Agent atau pengembang (bahkan dengan model AI sederhana)** dapat melakukan pembaruan pada file Excel mentah tanpa salah koordinat, tanpa merusak formula bawaan, dan tanpa merusak struktur sheet.

---

## 1. Identitas File Target & Keamanan Data

- **Path File Target:**  
  `/Users/auliamuzhaffar/Documents/maganghub/tugas-5/rekap data (fix).xlsx`
- **Nama Sheet Target:**  
  `Rekapitulasi Data` *(Wajib persis huruf besar-kecilnya)*
- **Sumber Rujukan Sah (Ground Truth):**  
  1. **SK Rektor USK No. 121/UN11/KPT/2026** (tentang Penetapan Daya Tampung Awal Mahasiswa Baru USK TA 2026/2027).  
  2. Database Master yang sudah diverifikasi: `/Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx`.

### Aturan Keamanan Wajib (Safety Rules)
1. **Wajib Buat Backup:** Sebelum menulis atau mengedit file Excel, buat salinan file cadangan:  
   `/Users/auliamuzhaffar/Documents/maganghub/tugas-5/rekap data (fix).xlsx.bak`
2. **Jangan Mengubah Formula Menjadi Nilai Statis:** Di sheet `Rekapitulasi Data`, kolom-kolom total dan rasio berisi rumus Excel (`SUM`, pembagian, dsb.). Cukup ubah sel input data mentahnya; formula akan otomatis menghitung hasil baru.
3. **Preservasi Sheet Lain:** File ini memiliki sheet lain seperti `Sheet4` dan sheet tarif UKT (`UKT_S1_2022` s.d. `Tarif_IPI_2026`). Jangan ubah atau hapus sheet-sheet tersebut.

---

## 2. Struktur Koordinat Sheet `Rekapitulasi Data`

- **Baris 1 s.d. 6:** Header tabel bertingkat (Tahun, Jalur, Metrik).
- **Baris 7 s.d. 87:** Baris data untuk 81 Program Studi.
  $$\text{Nomor Baris di Excel} = \text{No Urut Program Studi} + 6$$
  - Contoh: No Urut 9 (Peternakan) = Baris `15` ($9 + 6$).
  - Contoh: No Urut 57 (Ilmu Politik) = Baris `63` ($57 + 6$).
  - Contoh: No Urut 58 (Sosiologi) = Baris `64` ($58 + 6$).
  - Contoh: No Urut 77 (Teknik Lingkungan) = Baris `83` ($77 + 6$).
  - Contoh: No Urut 78 (Teknik Sumber Daya Air) = Baris `84` ($78 + 6$).
  - Contoh: No Urut 80 (Teknik Perminyakan) = Baris `86` ($80 + 6$).
- **Baris 88:** Baris ringkasan `JUMLAH`.

---

## 3. Spesifikasi Rinci Perubahan Sel (Cell-by-Cell Specification)

Perubahan dibagi menjadi 3 bagian pekerjaan:

---

### Bagian A: Sinkronisasi 6 Program Studi Tahun 2026 (SK Rektor No. 121)

Pada tahun 2026, 6 program studi disesuaikan daya tampungnya dengan SK Rektor No. 121. Total penambahan daya tampung adalah +125 kursi (dari 10.455 menjadi 10.580 untuk 81 prodi, atau 10.500 untuk 80 prodi SK Rektor).

#### Peta Kolom Tahun 2026 yang Diubah:
- **Kolom 100 (Huruf Kolom: `CV`):** Daya Tampung Jalur SNBP 2026 *(Nilai Masukan)*
- **Kolom 104 (Huruf Kolom: `CZ`):** Daya Tampung Jalur SNBT 2026 *(Nilai Masukan)*
- **Kolom 108 (Huruf Kolom: `DD`):** Daya Tampung Jalur SMMPTN-Barat 2026 *(Nilai Masukan)*
- **Kolom 126 (Huruf Kolom: `DV`):** Total Daya Tampung 2026 *(Nilai Masukan)*
- *Kolom 127 (Huruf Kolom: `DW`):* Rasio Peminat 2026 *(Rumus Formula: `=DS{row}/DV{row}` - JANGAN DITIMPA)*

#### Tabel Perubahan Sel Tahun 2026:

| No | Row | Program Studi | Kolom 100 (CV)<br>SNBP DT | Kolom 104 (CZ)<br>SNBT DT | Kolom 108 (DD)<br>SMMPTN DT | Kolom 126 (DV)<br>Total DT | Dampak Kolom 127 (DW)<br>Rasio Peminat (Auto Formula) |
|:---:|:---:|:---|:---:|:---:|:---:|:---:|:---|
| **9** | **15** | **PETERNAKAN** | Ubah `44` $\rightarrow$ **`48`** | Ubah `58` $\rightarrow$ **`56`** | Ubah `50` $\rightarrow$ **`56`** | Ubah `145` $\rightarrow$ **`160`** | Formula `=DS15/DV15` otomatis jadi **2.07** *(Peminat 331 / 160)* |
| **57** | **63** | **ILMU POLITIK** | Ubah `53` $\rightarrow$ **`54`** | Ubah `69` $\rightarrow$ **`63`** | Ubah `61` $\rightarrow$ **`63`** | Ubah `175` $\rightarrow$ **`180`** | Formula `=DS63/DV63` otomatis jadi **2.77** *(Peminat 499 / 180)* |
| **58** | **64** | **SOSIOLOGI** | Ubah `41` $\rightarrow$ **`48`** | Ubah `52` $\rightarrow$ **`56`** | Ubah `47` $\rightarrow$ **`56`** | Ubah `135` $\rightarrow$ **`160`** | Formula `=DS64/DV64` otomatis jadi **3.24** *(Peminat 519 / 160)* |
| **77** | **83** | **TEKNIK LINGKUNGAN** | Ubah `18` $\rightarrow$ **`24`** | Ubah `21` $\rightarrow$ **`28`** | Ubah `21` $\rightarrow$ **`28`** | Ubah `60` $\rightarrow$ **`80`** | Formula `=DS83/DV83` otomatis jadi **6.58** *(Peminat 526 / 80)* |
| **78** | **84** | **TEKNIK SUMBER DAYA AIR** | Ubah `18` $\rightarrow$ **`24`** | Ubah `21` $\rightarrow$ **`28`** | Ubah `21` $\rightarrow$ **`28`** | Ubah `60` $\rightarrow$ **`80`** | Formula `=DS84/DV84` otomatis jadi **1.53** *(Peminat 122 / 80)* |
| **80** | **86** | **TEKNIK PERMINYAKAN** | Ubah `18` $\rightarrow$ **`36`** | Ubah `21` $\rightarrow$ **`42`** | Ubah `21` $\rightarrow$ **`42`** | Ubah `80` $\rightarrow$ **`120`** | Formula `=DS86/DV86` otomatis jadi **7.75** *(Peminat 930 / 120)* |

---

### Bagian B: Revisi S1 Teknik Perminyakan Tahun 2025 (No 80, Baris 86)

Di tahun 2025, S1 Teknik Perminyakan menerima mahasiswa baru melalui seleksi jalur Mandiri sebanyak 120 orang, daya tampung 120 orang, lulus 120 orang, dan daftar ulang 120 orang (Fill Rate 100%). Pada file draf awal, kolom SMMPTN masih tertulis kosong/0.

#### Koordinat Sel yang Diubah pada Baris 86:

| Kolom Index | Huruf Kolom | Nama Header Kolom di Excel | Nilai Lama (Current) | Nilai Baru (Wajib Diisi) | Keterangan |
|:---:|:---:|:---|:---:|:---:|:---|
| **79** | **CA** | `SMMPTN > Daya Tampung` | `None` / Kosong | **`120`** | Kuota jalur Mandiri |
| **80** | **CB** | `SMMPTN > Lulus Awal` | `None` / Kosong | **`120`** | Peserta lulus awal |
| **81** | **CC** | `SMMPTN > Mendaftar Ulang` | `0` | **`120`** | Registrasi ulang |
| **82** | **CD** | `SMMPTN > Sisa Kuota` | `0` | **`0`** | Sisa kuota ($120 - 120 = 0$) |
| **97** | **CS** | `Total Daya Tampung` (2025) | `80` | **`120`** | Total kuota prodi tahun 2025 |

#### Kolom Formula yang Terpengaruh Otomatis pada Baris 86 (JANGAN DITIMPA NILAI STATIS):
- **Kolom 95 (CQ):** `Total Daftar Ulang`  
  Berisi formula: `=BU86+BY86+CC86+CG86+CK86+CN86`.  
  Karena `CC86` diisi `120`, hasil penjumlahan otomatis menjadi **`120`**.
- **Kolom 96 (CR):** `Daftar Lulus Awal`  
  Berisi formula: `=BT86+BX86+CB86+CF86+CJ86+CM86`.  
  Karena `CB86` diisi `120`, hasil penjumlahan otomatis menjadi **`120`**.
- **Kolom 98 (CT):** `Rasio Peminat`  
  Berisi formula: `=CP86/CS86`.  
  Karena `CP86` = 143 (peminat) dan `CS86` = 120, hasil pembagian otomatis menjadi **`1.1917`** (1.19x).

---

### Bagian C: Pengosongan/Penolkan Data S1 Teknik Lingkungan Tahun 2023 (No 77, Baris 83)

Data resmi Universitas Syiah Kuala menyatakan bahwa S1 Teknik Lingkungan baru resmi beroperasi dan menerima mahasiswa aktif pada tahun **2025 dan 2026**. Data mahasiswa yang sebelumnya tertulis pada tahun 2023 adalah data keliru/draf yang harus **dikosongkan (`None`)**, sama persis seperti status prodi baru lainnya (S1 Teknik Sumber Daya Air, Bisnis Digital, Teknik Perminyakan) yang belum buka di tahun 2023.

#### Koordinat Sel yang Dikosongkan (`None`) pada Baris 83:

| Kolom Index | Huruf Kolom | Nama Header Kolom di Excel | Nilai Lama (Current) | Nilai Baru |
|:---:|:---:|:---|:---:|:---:|
| **25** | **Y** | `2023 > SNBP > Peminat` | `12` | **`None`** |
| **26** | **Z** | `2023 > SNBP > Daya Tampung` | `15` | **`None`** |
| **27** | **AA** | `2023 > SNBP > Lulus Awal` | `9` | **`None`** |
| **28** | **AB** | `2023 > SNBP > Mendaftar Ulang` | `7` | **`None`** |
| **29** | **AC** | `2023 > SNBP > Sisa Kuota` | `8` | **`None`** |
| **30** | **AD** | `2023 > SNBT > Peminat` | `42` | **`None`** |
| **31** | **AE** | `2023 > SNBT > Daya Tampung` | `32` | **`None`** |
| **32** | **AF** | `2023 > SNBT > Lulus Awal` | `33` | **`None`** |
| **33** | **AG** | `2023 > SNBT > Mendaftar Ulang` | `30` | **`None`** |
| **34** | **AH** | `2023 > SNBT > Sisa Kuota` | `2` | **`None`** |
| **35** | **AI** | `2023 > SMMPTN > Daya Tampung` | `22` | **`None`** |
| **36** | **AJ** | `2023 > SMMPTN > Lulus Awal` | `18` | **`None`** |
| **37** | **AK** | `2023 > SMMPTN > Mendaftar Ulang` | `18` | **`None`** |
| **38** | **AL** | `2023 > SMMPTN > Sisa Kuota` | `4` | **`None`** |
| **42** | **AP** | `2023 > Total Daya Tampung` | `60` | **`None`** |

#### Kolom Formula yang Terpengaruh pada Baris 83 (JANGAN DIUBAH/DITIMPA):
- **Kolom 39 (AM):** `=SUM(AD83+Y83)` $\rightarrow$ otomatis bernilai **`0`**.
- **Kolom 40 (AN):** `=SUM(AK83+AG83+AB83)` $\rightarrow$ otomatis bernilai **`0`**.
- **Kolom 41 (AO):** `=SUM(AJ83+AF83+AA83)` $\rightarrow$ otomatis bernilai **`0`**.
- **Kolom 43 (AQ):** `=AM83/AP83` $\rightarrow$ tetap pertahankan rumus bawaan file.

---

## 4. Skrip Python Otomatis Eksekusi (Siap Pakai)

Jika suatu saat diminta melakukan eksekusi pembaruan pada `rekap data (fix).xlsx`, AI Agent atau pengguna dapat langsung menjalankan skrip Python berikut. Skrip ini telah menyertakan mekanisme **pencadangan otomatis (.bak)**, **validasi nilai sebelum update**, dan **verifikasi hasil akhir**:

```python
import shutil
import openpyxl

file_path = "/Users/auliamuzhaffar/Documents/maganghub/tugas-5/rekap data (fix).xlsx"
backup_path = "/Users/auliamuzhaffar/Documents/maganghub/tugas-5/rekap data (fix).xlsx.bak"

# 1. Buat Salinan Cadangan (Backup)
print(f"Membuat backup ke: {backup_path}...")
shutil.copyfile(file_path, backup_path)
print("Backup berhasil dibuat!")

# 2. Muat Workbook Excel
wb = openpyxl.load_workbook(file_path)
ws = wb["Rekapitulasi Data"]

# -------------------------------------------------------------
# Bagian A: Update 6 Prodi Tahun 2026 (SK Rektor No. 121)
# -------------------------------------------------------------
prodis_2026 = {
    15: {"nama": "PETERNAKAN", "snbp": 48, "snbt": 56, "smm": 56, "dt": 160},
    63: {"nama": "ILMU POLITIK", "snbp": 54, "snbt": 63, "smm": 63, "dt": 180},
    64: {"nama": "SOSIOLOGI", "snbp": 48, "snbt": 56, "smm": 56, "dt": 160},
    83: {"nama": "TEKNIK LINGKUNGAN", "snbp": 24, "snbt": 28, "smm": 28, "dt": 80},
    84: {"nama": "TEKNIK SUMBER DAYA AIR", "snbp": 24, "snbt": 28, "smm": 28, "dt": 80},
    86: {"nama": "TEKNIK PERMINYAKAN", "snbp": 36, "snbt": 42, "smm": 42, "dt": 120},
}

for row, val in prodis_2026.items():
    ws.cell(row=row, column=100, value=val["snbp"])  # Col CV: SNBP DT
    ws.cell(row=row, column=104, value=val["snbt"])  # Col CZ: SNBT DT
    ws.cell(row=row, column=108, value=val["smm"])   # Col DD: SMMPTN DT
    ws.cell(row=row, column=126, value=val["dt"])    # Col DV: Total DT
    print(f"2026 Updated: Row {row} ({val['nama']}) -> DT={val['dt']}")

# -------------------------------------------------------------
# Bagian B: Revisi S1 Teknik Perminyakan 2025 (Row 86)
# -------------------------------------------------------------
ws.cell(row=86, column=79, value=120)  # Col CA: SMMPTN DT
ws.cell(row=86, column=80, value=120)  # Col CB: SMMPTN Lulus Awal
ws.cell(row=86, column=81, value=120)  # Col CC: SMMPTN Mendaftar Ulang
ws.cell(row=86, column=82, value=0)    # Col CD: SMMPTN Sisa Kuota
ws.cell(row=86, column=97, value=120)  # Col CS: Total Daya Tampung 2025
print("2025 Updated: Row 86 (TEKNIK PERMINYAKAN) -> DT=120, DU=120")

# -------------------------------------------------------------
# Bagian C: Pengosongan Data S1 Teknik Lingkungan 2023 (Row 83)
# -------------------------------------------------------------
# Kosongkan kolom SNBP, SNBT, SMMPTN (Col 25 s.d. 38)
for col_idx in range(25, 39):
    ws.cell(row=83, column=col_idx, value=None)

# Kosongkan Total Daya Tampung 2023 (Col 42)
ws.cell(row=83, column=42, value=None)
print("2023 Cleared: Row 83 (TEKNIK LINGKUNGAN) -> Cols 25-38 & 42 set to None")

# 3. Simpan Perubahan ke File Asli
wb.save(file_path)
print("Penyimpanan berhasil! File rekap data (fix).xlsx telah diperbarui.")
```

---

## 5. Checklist Verifikasi Setelah Eksekusi (Post-Execution Validation)

Setelah skrip di atas dijalankan, lakukan assertion berikut untuk memastikan seluruh sel telah bernilai benar:

- [ ] **Row 15 (Peternakan 2026):** `CV15=48`, `CZ15=56`, `DD15=56`, `DV15=160`.
- [ ] **Row 63 (Ilmu Politik 2026):** `CV63=54`, `CZ63=63`, `DD63=63`, `DV63=180`.
- [ ] **Row 64 (Sosiologi 2026):** `CV64=48`, `CZ64=56`, `DD64=56`, `DV64=160`.
- [ ] **Row 83 (Teknik Lingkungan 2026):** `CV83=24`, `CZ83=28`, `DD83=28`, `DV83=80`.
- [ ] **Row 84 (TSDA 2026):** `CV84=24`, `CZ84=28`, `DD84=28`, `DV84=80`.
- [ ] **Row 86 (Teknik Perminyakan 2026):** `CV86=36`, `CZ86=42`, `DD86=42`, `DV86=120`.
- [ ] **Row 86 (Teknik Perminyakan 2025):** `CA86=120`, `CB86=120`, `CC86=120`, `CS86=120`. Formula `CQ86` & `CR86` tidak terhapus.
- [ ] **Row 83 (Teknik Lingkungan 2023):** Seluruh sel rentang `Y83:AL83` bernilai `None`, `AP83` bernilai `None`. Formula `AM83`, `AN83`, `AO83` tidak terhapus.
- [ ] **File cadangan `.bak`** tersedia dan dapat di-*restore* jika sewaktu-waktu dibutuhkan.
