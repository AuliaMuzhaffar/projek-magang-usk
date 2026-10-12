# Panduan Eksekutif: Antigravity Customization & Workflow Workflow
**Dokumen Referensi Masa Depan untuk Produktivitas Maksimal Tanpa Mengganggu Delivery Proyek Saat Ini**

---

## 1. Pendahuluan: Mengapa Dokumen Ini Dibuat?

Ketika kita bekerja bersama AI coding assistant (seperti Antigravity), seringkali AI bekerja sangat cepat namun berisiko membuat kesalahan sepele (misalnya lupa membersihkan *state* tooltip, memanipulasi DOM secara ceroboh, atau tidak menguji *edge case*).

Dokumen ini disusun sebagai **panduan referensi mandiri** bagi Anda yang dapat dipelajari nanti setelah proyek magang saat ini selesai. Prinsip utamanya:
- **Sekarang**: Tetap fokus penuh menyelesaikan target dan pengiriman (*delivery*) proyek Tugas-5 tanpa terdistraksi mencoba-coba konfigurasi baru.
- **Nanti (Proyek Mendatang)**: Anda tinggal membuka dokumen ini untuk langsung menerapkan cara mengontrol AI agar menghasilkan kode berkualitas tinggi sejak detik pertama.

---

## 2. Konsep Dasar Antigravity: Bagaimana AI Bekerja?

### A. Mengapa AI Bisa "Lupa" atau "Ceroboh"?
Secara default, AI memulai percakapan baru dengan pemahaman umum tentang pemrograman, namun **tidak mengetahui standar baku personal Anda**, kecuali Anda mendiktenya berulang kali di setiap obrolan. 

Jika Anda tidak memberi aturan tertulis, AI cenderung mengambil jalan pintas (*happy path*) demi menyelesaikan fitur secepat mungkin, yang seringkali mengabaikan skenario gangguan (*interrupted state* / *edge cases*).

### B. Solusi Antigravity: Sistem Customization (Rules & Skills)
Antigravity memiliki fitur bawaan untuk membaca file pedoman otomatis sebelum AI mulai menjawab. Ibaratnya, ini adalah **SOP (Standar Operasional Prosedur)** yang wajib dibaca AI sebelum menulis sebaris kode pun.

Komponen utamanya ada dua:
1. **Rules (Aturan)**: File Markdown (`.md`) berisi instruksi permanen, batasan kualitas, gaya penulisan, dan larangan teknis.
2. **Skills (Keahlian)**: Paket cheatsheet / alur kerja khusus yang dipanggil AI saat menangani domain tertentu (misalnya manipulasi SVG, debugging performa, akses database).

---

## 3. Memahami Folder `.agents/rules/` (Hidden Folder di Mac)

### A. Apa itu Hidden Folder?
Di macOS dan Linux, setiap folder atau file yang diawali dengan tanda titik (`.`) dianggap sebagai **berkas sistem/konfigurasi** sehingga sengaja disembunyikan oleh sistem agar tampilan desktop/Finder tidak berantakan. Contoh populer: `.git/`, `.vscode/`, `.env`, dan `.agents/`.

### B. Cara Melihat Folder Tersembunyi di Mac
Anda tidak perlu membuka terminal jika tidak terbiasa. Di Finder Mac:
1. Buka folder proyek Anda di Finder biasa.
2. Tekan kombinasi tombol keyboard: **Cmd + Shift + . (titik)**
3. Seluruh folder tersembunyi (termasuk `.agents`) akan seketika muncul dengan warna transparan/abu-abu.
4. Tekan tombol yang sama lagi untuk menyembunyikannya kembali.

> **Catatan Menarik:** Di dalam text editor / IDE (seperti VS Code atau Antigravity IDE), folder `.agents` **tidak tersembunyi**. Folder tersebut akan langsung muncul di panel sebelah kiri (File Explorer) seperti folder biasa.

---

## 4. Dua Tingkatan Aturan (*Scope*): Workspace vs Global

Ini adalah konsep terpenting yang wajib dipahami saat menyusun aturan AI:

```
Tingkatan Aturan di Antigravity:
│
├── 1. GLOBAL SCOPE (Semua Proyek)
│   └── Lokasi: ~/.gemini/config/rules/
│   └── Efek: Mengikat di SEMUA proyek yang Anda buka di laptop ini.
│
└── 2. WORKSPACE SCOPE (Khusus 1 Proyek Ini Saja)
    └── Lokasi: .agents/rules/ (di dalam folder proyek)
    └── ATAU: AGENTS.md (di root folder proyek)
    └── Efek: HANYA aktif saat Anda membuka proyek tersebut.
```

### Tabel Perbandingan Penggunaan

| Kategori | Workspace Scope (`.agents/rules/`) | Global Scope (`~/.gemini/config/rules/`) |
|---|---|---|
| **Cakupan** | Hanya untuk 1 repositori/folder aktif. | Berlaku untuk semua repositori di komputer Anda. |
| **Kapan Digunakan?** | Untuk aturan bisnis spesifik proyek (misal: "Dataset USK S1 memiliki 60 prodi utama dan 6 prodi baru", "Skema warna kuadran USK wajib hijau-biru-kuning-merah"). | Untuk standar mutu teknis universal (misal: "Setiap tooltip wajib auto-dismiss saat reset", "Dilarang memanipulasi DOM saat hover"). |
| **Portabilitas** | Ikut tersimpan jika folder proyek dikirim/di-push ke Git (tim lain bisa ikut menikmati aturan ini). | Tersimpan di profil laptop pribadi Anda saja. |

---

## 5. Alternatif Tanpa Folder Tersembunyi: File `AGENTS.md`

Jika Anda merasa folder `.agents/` membingungkan atau takut lupa menekan shortcut di Finder, Antigravity menyediakan alternatif resmi yang **100% kasat mata (bukan hidden file)**:

Cukup buat file bernama:
`AGENTS.md` (atau `GEMINI.md`) langsung di folder utama proyek Anda.

File ini diletakkan sejajar dengan file `index.html` atau file python Anda. Antigravity akan membaca file ini dengan prioritas yang sama persis seperti file di dalam folder `.agents/rules/`.

---

## 6. Contoh Nyata Implementasi: SOP Frontend Anti-Bug

Berikut adalah contoh isi file aturan yang sangat ideal Anda pasang di proyek-proyek Anda selanjutnya agar bug tooltip/UI serupa tidak pernah terjadi lagi.

Simpan file ini dengan nama: `frontend_quality.md` (di `.agents/rules/` atau secara global di `~/.gemini/config/rules/`):

```markdown
# SOP Kualitas Frontend & Interaktivitas UI

## 1. Arsitektur Komponen Overlay (Tooltip, Modal, Dropdown)
- Setiap komponen melayang (overlay) WAJIB memiliki Controller/Manager terpusat (Single Source of Truth).
- Dilarang membuat fungsi hover yang mengubah struktur urutan pohon DOM (seperti appendChild/insertBefore) karena akan memutus rantai event mouseleave browser. Gunakan CSS class untuk efek visual.

## 2. Siklus Hidup Pembersihan (Cleanup Lifecycle)
- Setiap aksi global (Reset Tampilan, Toggle Label, Switch Tab Filter, Search Input) WAJIB memanggil fungsi pembersihan overlay di baris pertamanya.
- Kontainer visual (misalnya kanvas SVG) WAJIB memiliki boundary listener: jika kursor keluar kanvas atau berada di ruang kosong, seluruh overlay transient wajib otomatis hilang.

## 3. Responsive Positioning (Smart Clamping & Flip)
- Tooltip atau popover tidak boleh statis. Wajib memiliki kalkulasi batas layar (boundary check):
  - Jika elemen berada di tepi atas, posisi wajib membalik ke bawah kursor (flipped-down).
  - Jika berada di tepi kiri/kanan, posisi wajib di-clamp agar tidak terpotong.

## 4. Standar Pembuktian Sebelum Menyatakan Selesai (Definition of Done)
- Jangan hanya menguji skenario ideal (happy path).
- Wajib uji skenario interupsi: lakukan hover pada elemen, lalu klik tombol Reset/Filter. Pastikan tidak ada elemen yang menggantung atau menjadi zombie DOM.
```

---

## 7. Fitur Rahasia Antigravity: Slash Commands untuk Efisiensi

Selain file aturan, Antigravity memiliki perintah cepat (*slash commands*) yang bisa Anda ketikkan di kolom chat untuk memandu proses kerja:

### 1. `/learn` (Menyimpan Pelajaran Saat AI Bikin Salah)
- **Kapan Dipakai**: Ketika AI baru saja memperbaiki bug dan Anda ingin AI mengingatnya selamanya.
- **Cara Pakai**: Ketik di chat:
  `/learn Selalu buat TooltipManager terpusat dan pastikan auto-dismiss saat tombol reset ditekan.`
- **Hasilnya**: AI akan otomatis menuliskan aturan tersebut ke sistem konfigurasi global tanpa Anda harus membuat file manual.

### 2. `/plan` (Mencegah AI Terburu-buru Menulis Kode)
- **Kapan Dipakai**: Saat Anda punya fitur baru yang cukup rumit.
- **Cara Pakai**: Ketik `/plan Buatkan fitur pencarian cerdas dengan dropdown rekomendasi.`
- **Hasilnya**: AI tidak akan langsung menulis kode acak. AI wajib menyusun dokumen rencana terstruktur langkah demi langkah dan meminta persetujuan Anda dulu.

### 3. `/grill-me` (Wawancara Kebutuhan)
- **Kapan Dipakai**: Saat Anda punya ide kasar tetapi belum yakin detail teknisnya.
- **Cara Pakai**: Ketik `/grill-me Saya ingin merombak tampilan kartu metrik ini.`
- **Hasilnya**: AI akan mewawancarai Anda satu per satu dengan opsi pilihan ganda yang cerdas sampai spesifikasinya matang.

---

## 8. Rencana Aksi Praktis (Action Plan) untuk Anda

Untuk menjaga fokus Anda saat ini:

1. **Fase Sekarang (Fokus Proyek Utama)**:
   - Abaikan dulu pengaturan folder `.agents` atau file konfigurasi baru.
   - Selesaikan seluruh evaluasi data, kuadran, dan laporan presentasi proyek magang USK Anda hingga tuntas.
   - Jangan melakukan eksperimen konfigurasi yang berisiko mengubah environment kerja saat ini.

2. **Fase Mendatang (Saat Memulai Proyek Baru)**:
   - Buka kembali file `planning-workflow.md` ini.
   - Saat membuat folder proyek baru, buatlah satu file `AGENTS.md` sederhana di root folder.
   - Tuliskan 3–5 poin aturan kerja Anda di file tersebut.
   - Rasakan perbedaannya: AI akan langsung bekerja jauh lebih rapi, disiplin, dan minim bug sejak hari pertama.

---
*Dokumen ini dibuat dan disimpan di repositori proyek Anda sebagai aset pengetahuan permanen.*
