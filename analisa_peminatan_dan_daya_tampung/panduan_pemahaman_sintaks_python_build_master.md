# PANDUAN LENGKAP SINTAKS PYTHON: BEDAH KODINGAN `build_master_dataset.py`
## Modul Pembelajaran "Learning by Doing" Khusus Lulusan Informatika (*Fresh Graduate*)

Panduan ini dibuat khusus agar kamu memahami **setiap baris, setiap fungsi, dan setiap simbol sintaks** di dalam skrip [`build_master_dataset.py`](file:///Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisa_peminatan_dan_daya_tampung/scripts/build_master_dataset.py). Dokumen ini membandingkan "Cara Pemula (Panjang)" dengan "Cara Pythonic (Ringkas)", sehingga kamu memiliki fondasi pemrograman yang kuat dan percaya diri saat menjelaskan proses data ke pimpinan (WR / Direktur).

---

## DAFTAR ISI MODUL
1. [Bagian 1: Bedah Import Pustaka (Library)](#bagian-1-bedah-import-pustaka-library)
2. [Bagian 2: Fungsi Helper Pembersih Teks & Logika If-Elif](#bagian-2-fungsi-helper-pembersih-teks--logika-if-elif)
3. [Bagian 3: Fungsi Statistik Lanjutan (Regresi OLS & CAGR)](#bagian-3-fungsi-statistik-lanjutan-regresi-ols--cagr)
4. [Bagian 4: Cara Python Membaca Excel (openpyxl & Zero-Indexed)](#bagian-4-cara-python-membaca-excel-openpyxl--zero-indexed)
5. [Bagian 5: Operator Ternary & Pengaman Nilai Kosong (None)](#bagian-5-operator-ternary--pengaman-nilai-kosong-none)
6. [Bagian 6: List Comprehension & Filter Kondisional](#bagian-6-list-comprehension--filter-kondisional)
7. [Bagian 7: Pola Data Engineering (List of Dictionaries → Pandas DataFrame)](#bagian-7-pola-data-engineering-list-of-dictionaries--pandas-dataframe)
8. [Bagian 8: Automasi Styling Excel Eksekutif (openpyxl Formatting)](#bagian-8-automasi-styling-excel-eksekutif-openpyxl-formatting)
9. [Bagian 9: Kamus Istilah Penting untuk Jawaban ke Pimpinan](#bagian-9-kamus-istilah-penting-untuk-jawaban-ke-pimpinan)

---

## BAGIAN 1: BEDAH IMPORT PUSTAKA (LIBRARY)

Di baris 1–5:
```python
import os
import openpyxl
import pandas as pd
import numpy as np
from scipy import stats
```

### Apa fungsi masing-masing pustaka ini?
1. **`import os`** (*Operating System*): Pustaka bawaan Python untuk mengelola file dan folder di komputer (misal: menggabungkan alamat folder dengan `os.path.join`, atau membuat folder baru dengan `os.makedirs`).
2. **`import openpyxl`**: Pustaka khusus untuk membaca, mengedit sel demi sel, dan menghias (styling) file Excel (`.xlsx`).
3. **`import pandas as pd`**: Pustaka standar industri untuk analisis data berbentuk tabel (DataFrame). Mirip seperti membuat tabel SQL atau Excel di dalam memori RAM komputer.
4. **`import numpy as np`**: Pustaka komputasi numerik berkecepatan tinggi. Di skrip ini digunakan fungsi `np.mean` (rata-rata) dan `np.nan` (penanda nilai kosong/Not a Number).
5. **`from scipy import stats`**: Modul statistik ilmiah. Di skrip ini dipakai untuk fungsi `stats.linregress` (menghitung kemiringan garis regresi tren OLS).

---

## BAGIAN 2: FUNGSI HELPER PEMBERSIH TEKS & LOGIKA IF-ELIF

### 1. Fungsi `clean_str(val)` (Baris 7–10)
```python
def clean_str(val):
    if val is None or pd.isna(val):
        return ""
    return str(val).strip()
```

#### Cara Kerjanya:
* **Masalah di Excel:** Sering kali ada sel yang kosong melompong. Python membacanya sebagai `None`, sedangkan Pandas membacanya sebagai `NaN` (*Not a Number*).
* **Solusi:** `if val is None or pd.isna(val): return ""` artinya: *"Jika datanya kosong, ubah jadi teks kosong (`""`), jangan biarkan bernilai None agar program tidak error."*
* `str(val).strip()`: Ubah nilai jadi string, lalu fungsi `.strip()` akan **membuang spasi liar** di awal atau akhir teks (misal teks `" MANAJEMEN "` dibersihkan menjadi `"MANAJEMEN"`).

---

### 2. Fungsi `get_fakultas_and_klaster(kd, nm, jenjang)` (Baris 12–58)
Fungsi ini bertugas memetakan program studi ke Fakultas dan Klaster secara otomatis.

#### Bedah Baris 20–26 (Jenjang D3 Vokasi):
```python
if jenjang == 'D3' or 'D3' in nm_upper:
    if any(x in nm_upper for x in ['LISTRIK', 'MESIN', 'SIPIL']): return 'Teknik', 'Diploma 3 Vokasi'
    if any(x in nm_upper for x in ['SEKRETARI', 'PERUSAHAAN', 'AKUNTANSI', 'PERBANKAN']): return 'Ekonomi dan Bisnis', 'Diploma 3 Vokasi'
```

#### Apa maksud `any(x in nm_upper for x in [...])`?
Ini adalah cara ringkas (*Pythonic*) untuk mengecek apakah salah satu kata kunci ada di dalam nama prodi.

* **Cara Pemula (Panjang & Melelahkan):**
  ```python
  if 'LISTRIK' in nm_upper or 'MESIN' in nm_upper or 'SIPIL' in nm_upper:
      return 'Teknik', 'Diploma 3 Vokasi'
  ```
* **Cara Pythonic (Ringkas dengan `any`):**
  Python melakukan perulangan kecil: cek satu per satu kata di dalam list `['LISTRIK', 'MESIN', 'SIPIL']`. Jika **salah satu saja cocok** (`any`), maka kondisi dianggap `True`.

#### Bedah Baris 30–41 (Prefix Kode Prodi S1):
```python
if kd.startswith('01'): return 'Ekonomi dan Bisnis', klaster
if kd.startswith('02'): return 'Kedokteran Hewan', klaster
if kd.startswith('04'): return 'Teknik', klaster
```
* `kd.startswith('01')`: Mengecek apakah kode prodi **diawali dengan angka '01'**. Di USK, prodi di bawah FEB diawali kode 01, FKH kode 02, Fakultas Teknik kode 04, dst.

---

## BAGIAN 3: FUNGSI STATISTIK LANJUTAN (REGRESI OLS & CAGR)

### 1. Fungsi `calculate_ols_slope(y_values)` (Baris 59–74)
```python
def calculate_ols_slope(y_values):
    valid_pairs = []
    x_coords = [2022, 2023, 2024, 2025, 2026]
    for x, y in zip(x_coords, y_values):
        if y > 0:
            valid_pairs.append((x, y))
    
    if len(valid_pairs) < 3:
        return 0.0, 0.0
    
    xs = [p[0] for p in valid_pairs]
    ys = [p[1] for p in valid_pairs]
    
    slope, intercept, r_val, p_val, std_err = stats.linregress(xs, ys)
    return round(slope, 2), round(r_val**2, 3)
```

#### Bedah Langkah demi Langkah:
1. `zip(x_coords, y_values)`: Menggabungkan tahun dan nilainya menjadi pasangan koordinat `(x, y)`:
   * Misal: `(2022, 100), (2023, 120), (2024, 150), ...`
2. `if y > 0: valid_pairs.append((x, y))`: Hanya ambil tahun yang datanya aktif (> 0).
3. `if len(valid_pairs) < 3: return 0.0, 0.0`: **Aturan Validitas Statistik.** Secara teori matematika, kita tidak boleh menarik garis tren linier jika titik datanya kurang dari 3 titik. Untuk prodi baru yang datanya cuma 1 atau 2 tahun, kemiringannya langsung diset `0.0`.
4. `stats.linregress(xs, ys)`: Fungsi SciPy yang otomatis menghitung formula regresi:
   * `slope`: Kemiringan garis (kecepatan perubahan: bertambah/berkurang berapa orang per tahun).
   * `r_val`: Nilai korelasi r.
   * `r_val**2`: Nilai R² (Koefisien Determinasi / stabilitas tren). Operator `**2` di Python artinya pangkat 2 (kuadrat).

---

### 2. Fungsi `calculate_cagr(start_val, end_val, periods=4)` (Baris 76–79)
```python
def calculate_cagr(start_val, end_val, periods=4):
    if start_val <= 0 or end_val <= 0:
        return np.nan
    return round(((end_val / start_val) ** (1.0 / periods) - 1.0) * 100.0, 2)
```

#### Bedah Rumus Matematika:
Rumus CAGR (Compound Annual Growth Rate) adalah:
```text
CAGR = ((Nilai_Akhir / Nilai_Awal) ^ (1 / Periode)) - 1
```
* Di Python, simbol pangkat bukan tanda `^`, melainkan tanda bintang ganda `**`.
* `(1.0 / periods)`: Pangkat 1/4 (karena ada 4 lompatan tahun dari 2022 ke 2026).
* `if start_val <= 0 or end_val <= 0: return np.nan`: Perlindungan agar tidak terjadi error matematika jika ada nilai 0 (karena angka 0 tidak bisa dipangkatkan pecahan).

---

## BAGIAN 4: CARA PYTHON MEMBACA EXCEL (openpyxl & ZERO-INDEXED)

Di baris 96–97:
```python
rows_old = list(ws_old.iter_rows(min_row=7, max_row=87, values_only=True))
```

### Konsep Memori Komputer:
File Excel diubah oleh Python menjadi **List of Tuples**. Setiap baris adalah tuple angka.

Ingat aturan utama Informatika: **Python memulai urutan indeks dari 0 (Zero-indexed)**:

| Kolom Excel Asli | Nama Kolom di Dokumen | Indeks Tuple di Python (`r_old`) |
|:---:|:---|:---:|
| **Kolom A** | No Urut | `r_old[0]` |
| **Kolom B** | Kode Prodi | `r_old[1]` |
| **Kolom C** | Nama Prodi | `r_old[2]` |
| **Kolom D** | Jenjang | `r_old[3]` |
| **Kolom E** | Peminat SNMPTN 2022 | `r_old[4]` |
| ... | ... | ... |
| **Kolom T (ke-20)** | Total Peminat 2022 | `r_old[19]` |
| **Kolom W (ke-23)** | Total Daya Tampung 2022 | `r_old[22]` |

Itulah sebabnya di baris 119 tertulis:
```python
pm_22 = float(r_old[19]) if r_old[19] is not None else 0.0
dt_22 = float(r_old[22]) if r_old[22] is not None else 0.0
```
Artinya: Ambil nilai total peminat 2022 dari kolom ke-20 (`[19]`) dan daya tampung 2022 dari kolom ke-23 (`[22]`).

---

## BAGIAN 5: OPERATOR TERNARY & PENGAMAN NILAI KOSONG

Perhatikan baris 121–122:
```python
la_22 = (float(r_old[6] or 0) + float(r_old[11] or 0) + float(r_old[16] or 0))
du_22 = (float(r_old[7] or 0) + float(r_old[12] or 0) + float(r_old[17] or 0))
```

### Mengapa ditulis `float(r_old[6] or 0)`?
Ini adalah trik cerdas Python (*Short-circuit Evaluation*):
* Jika sel `r_old[6]` berisi angka `45`, maka Python mengambil `45`.
* Tetapi jika sel `r_old[6]` berisi `None` (kosong), ekspresi `None or 0` otomatis menghasilkan angka `0`.
* Ini mencegah program error saat menjumlahkan nilai sel yang kosong.

### Mengapa ada 3 angka yang dijumlahkan untuk tahun 2022?
Karena pada tahun 2022, mahasiswa yang lulus seleksi (`la_22`) dan daftar ulang (`du_22`) berasal dari 3 jalur masuk:
1. `r_old[6]` = Jalur SNMPTN
2. `r_old[11]` = Jalur SBMPTN
3. `r_old[16]` = Jalur SMMPTN Barat

Ketiganya dijumlahkan untuk mendapatkan total mahasiswa masuk universitas pada tahun tersebut.

---

## BAGIAN 6: LIST COMPREHENSION & FILTER KONDISIONAL

Di baris 348–352 terdapat sintaks yang sangat sering dipakai di data science:

```python
rec["Rata_Peminat_5Thn"] = round(np.mean([p for p in pem_vals if p > 0]), 1) if any(p > 0 for p in pem_vals) else 0.0
rec["Rata_FillRate_5Thn_Persen"] = round(np.mean([rec[f"FillRate_{yr}_Persen"] for yr in [2022, 2023, 2024, 2025, 2026] if rec[f"DT_{yr}"] > 0]), 1)
```

Mari kita bedah anatomi **List Comprehension**: `[p for p in pem_vals if p > 0]`

### Perbandingan dengan Gaya Pemula:
* **Gaya Pemula (5 Baris):**
  ```python
  daftar_baru = []
  for p in pem_vals:
      if p > 0:
          daftar_baru.append(p)
  ```
* **Gaya Pythonic (1 Baris Ringkas):**
  ```python
  daftar_baru = [p for p in pem_vals if p > 0]
  ```
Keduanya menghasilkan output yang 100% sama! List comprehension memadatkan *loop* dan *filter* menjadi satu baris ekspresif.

### Apa maksud `rec[f"FillRate_{yr}_Persen"]`?
Itu adalah **Formatted String (f-string)**.  
Di dalam perulangan `for yr in [2022, 2023, 2024, 2025, 2026]`:
* Saat `yr = 2022`, Python mengakses kunci: `rec["FillRate_2022_Persen"]`
* Saat `yr = 2023`, Python mengakses kunci: `rec["FillRate_2023_Persen"]`
* Dan seterusnya.

Dengan trik ini, kita tidak perlu mengetik nama variabel satu per satu sampai 5 kali.

---

## BAGIAN 7: POLA DATA ENGINEERING (DICTIONARY → DATAFRAME)

Di baris 267–376, skrip menggunakan pola arsitektur standar data engineering:

```mermaid
flowchart LR
    A["Baris Data Mentah"] --> B["Dictionary per Prodi (rec)"]
    B --> C["Kumpulan List (master_records)"]
    C --> D["Pandas DataFrame (df_master)"]
    D --> E["Excel Multi-Sheet (.to_excel)"]
```

### Langkah 1: Buat Dictionary untuk 1 Prodi (`rec`)
```python
rec = {
    "No": no,
    "Fakultas": fakultas,
    "Program_Studi": nm_prodi,
    "Jenjang": jenjang,
    "Segmen_Analisis": klaster
}
# Lalu tambahkan data tahunan ke dalam dictionary:
rec["Peminat_2026"] = pm_26
rec["FillRate_2026_Persen"] = fill_rate
```

### Langkah 2: Masukkan ke List Utama
```python
master_records.append(rec)
```
Setelah perulangan 81 prodi selesai, `master_records` berisi 81 buah dictionary.

### Langkah 3: Konversi Sekaligus ke Pandas DataFrame (Baris 378)
```python
df_master = pd.DataFrame(master_records)
```
Seketika itu juga, Python mengubah tumpukan dictionary menjadi sebuah **tabel data raksasa** yang memiliki baris dan kolom rapi!

### Langkah 4: Filter Sheet per Klaster (Baris 379–381)
```python
df_s1 = df_master[df_master["Segmen_Analisis"] == "S1 Kampus Utama"].copy()
df_d3 = df_master[df_master["Segmen_Analisis"] == "Diploma 3 Vokasi"].copy()
df_psdku = df_master[df_master["Segmen_Analisis"] == "PSDKU Gayo Lues"].copy()
```
Ini mirip dengan perintah SQL:
`SELECT * FROM master WHERE Segmen_Analisis = 'S1 Kampus Utama'`.

---

## BAGIAN 8: AUTOMASI STYLING EXCEL EKSEKUTIF (`openpyxl`)

Fungsi `format_master_workbook(file_path)` (Baris 410–686) adalah mesin pemercantik tampilan.

### 1. Mengubah Nama Header Teknis jadi Bahasa Manusia (Baris 416–519)
Di memori Python kita memakai nama kolom seperti `FillRate_2026_Persen`.  
Pimpinan kampus tidak boleh melihat nama variabel seperti itu di Excel.
```python
nice_val = HEADER_MAP.get(raw_val, raw_val.replace('_', ' '))
cell.value = nice_val
```
Kamus `HEADER_MAP` otomatis mengubahnya menjadi: **`Fill Rate 2026 (%)`**.

### 2. Memberi Warna Selang-Seling / Zebra Striping (Baris 613–622)
```python
row_fill = FILL_ZEBRA_EVEN if (row_idx % 2 == 0) else FILL_ZEBRA_ODD
cell.fill = row_fill
```
* Operator `%` adalah **Modulo (Sisa Bagi)**.
* Jika `row_idx % 2 == 0` (nomor baris genap), beri warna putih bersih (`#FFFFFF`).
* Jika ganjil, beri warna abu-abu sangat muda (`#F8F9FA`).
* Hasilnya adalah tabel zebra striping yang sangat mudah dan nyaman dibaca oleh mata pimpinan.

### 3. Mengunci Kolom / Freeze Panes (Baris 602–605)
```python
ws.freeze_panes = "D2"
```
Artinya: **Kunci kolom A, B, dan C serta baris ke-1**.  
Saat pimpinan menggeser kursor ke kanan untuk melihat data tahun 2026 atau data tren, nama Fakultas dan Program Studi di sebelah kiri akan tetap diam di tempat dan tidak menghilang.

### 4. Format Angka Otomatis (Baris 641–653)
Excel secara default menampilkan angka desimal apa adanya (misal `83.333333333%`). Skrip memperbaikinya secara otomatis:
```python
if any(k in raw_h for k in ["Persen", "YoY", "Rate", "CAGR"]):
    cell.number_format = '0.0"%"'  # Tampil: 83.3%
elif any(k in raw_h for k in ["Keketatan", "Slope", "R2", "Marginal"]):
    cell.number_format = '0.00'     # Tampil: 4.12
else:
    cell.number_format = '#,##0'    # Tampil: 1,450 (ada titik pemisah ribuan)
```

---

## BAGIAN 9: KAMUS ISTILAH PENTING UNTUK JAWABAN KE PIMPINAN

Gunakan kalimat-kalimat di bawah ini saat kamu ditanya oleh dekan, dosen pembimbing, atau rektorat:

| Jika Ditanya: | Jangan Jawab: | Jawaban Terbaik Lulusan Informatika: |
|:---|:---|:---|
| *"Dari mana asal data tabel ini?"* | *"Saya copas dari Excel lama, Pak."* | *"Data ini diproses otomatis melalui pipeline ETL Python yang menyatukan data historis PMB 2022–2025 dan data daya tampung riil 2026 secara terprogram dan auditable."* |
| *"Kenapa prodi baru tidak dihitung trennya?"* | *"Soalnya datanya kosong, Pak."* | *"Secara kaidah statistika, analisis tren linier OLS memerlukan minimal 3 titik observasi. Prodi baru berada dalam masa adaptasi/inkubasi pasar sehingga kami beri label khusus 'Data Terbatas'."* |
| *"Kenapa format Excel-nya bisa rapi sekali?"* | *"Saya edit manual di Excel."* | *"Format styling diterapkan otomatis melalui pustaka openpyxl dengan standar korporat: palet warna USK, freeze panes dinamis, dan penyesuaian lebar kolom otomatis berbasis panjang karakter."* |
