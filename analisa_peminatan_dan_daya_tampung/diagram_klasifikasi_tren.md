# Bagan Algoritma: Klasifikasi Tren Prodi (Decision Tree)

Bagan di bawah ini menggambarkan alur penyaringan otomatis yang digunakan untuk mengklasifikasikan tren 81 program studi selama 5 tahun terakhir (2022-2026).

```mermaid
graph TD
    Start((Mulai Evaluasi Prodi)) --> C1

    %% Tahap 1
    C1{"Tahap 1: Cek Status Kritis <br> (Fill Rate < 68% ATAU Keketatan < 1,5?)"}
    C1 -- YA --> R1["🔴 PEMINATAN RELATIF RENDAH <br> (Sakit Parah - Segera Pangkas)"]
    C1 -- TIDAK (Aman) --> C2

    %% Tahap 2
    C2{"Tahap 2: Cek Pertumbuhan Pesat <br> (Slope > +5 DAN CAGR >= +10%?)"}
    C2 -- YA --> R2["📈 TREN MENINGKAT <br> (Growth Star - Berpotensi Ekspansi)"]
    C2 -- TIDAK --> C3

    %% Tahap 3
    C3{"Tahap 3: Cek Kemerosotan <br> (Slope < -2 DAN CAGR < -2%?)"}
    C3 -- YA --> R3["📉 TREN MENURUN <br> (Waspada - Jangan Tambah Kuota)"]
    C3 -- TIDAK --> C4

    %% Tahap 4
    C4{"Tahap 4: Cek Kestabilan <br> (Slope Netral -3 s.d +3 DAN <br> Fill Rate Rata-rata >= 80%?)"}
    C4 -- YA --> R4["🛡️ TREN STABIL <br> (Tulang Punggung - Lindungi Kuota)"]
    C4 -- TIDAK --> R5

    %% Tahap 5
    R5["🌊 TREN FLUKTUATIF <br> (Naik Turun Selang-Seling)"]

    %% Styling
    style Start fill:#333,stroke:#fff,stroke-width:2px,color:#fff
    style C1 fill:#f9f9f9,stroke:#666,stroke-width:2px,color:#000
    style C2 fill:#f9f9f9,stroke:#666,stroke-width:2px,color:#000
    style C3 fill:#f9f9f9,stroke:#666,stroke-width:2px,color:#000
    style C4 fill:#f9f9f9,stroke:#666,stroke-width:2px,color:#000
    
    style R1 fill:#ffcccc,stroke:#ff0000,stroke-width:2px,color:#000
    style R2 fill:#ccffcc,stroke:#009900,stroke-width:2px,color:#000
    style R3 fill:#ffebcc,stroke:#ff9900,stroke-width:2px,color:#000
    style R4 fill:#cce5ff,stroke:#0066cc,stroke-width:2px,color:#000
    style R5 fill:#e6ccff,stroke:#9933ff,stroke-width:2px,color:#000
```

## Mengapa Menggunakan Pendekatan Ini?

Algoritma *Decision Tree* ini dirancang untuk memastikan analisis yang **terstruktur dan objektif (M.E.C.E - Mutually Exclusive, Collectively Exhaustive)**:

1. **Mutually Exclusive:** Tidak ada satupun prodi yang bisa masuk ke dua kategori sekaligus karena sistem penyaringannya berjalan berurutan. Begitu sebuah prodi tertangkap di satu saringan, ia tidak akan dievaluasi di saringan berikutnya.
2. **Collectively Exhaustive:** Tidak ada satupun prodi yang terlewat. Jika sebuah prodi gagal memenuhi kriteria ekstrem (sangat buruk, sangat bagus, merosot tajam, atau sangat stabil), maka ia akan otomatis ditangkap oleh keranjang terakhir (Tren Fluktuatif).

Dengan visualisasi ini, keputusan pimpinan dalam menambah atau memangkas kuota tidak lagi didasarkan pada asumsi, melainkan pada pembuktian algoritma yang matematis.
