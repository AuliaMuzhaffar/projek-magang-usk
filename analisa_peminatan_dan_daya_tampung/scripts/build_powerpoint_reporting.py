import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def set_shape_flat(shape, fill_color, line_color=None, line_width=1):
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()

def create_header(slide, title_text, category_text="UNIVERSITAS SYIAH KUALA | RAPAT PIMPINAN PMB"):
    header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.7), Inches(1.15))
    tf = header_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(10)
    p_cat.font.bold = True
    p_cat.font.color.rgb = RGBColor(230, 81, 0) # Orange accent

    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = RGBColor(27, 59, 111) # Navy Primary

def add_bullet(tf, bold_prefix, text_content, font_size=11.5, space_after=8, bold_color=RGBColor(27, 59, 111), norm_color=RGBColor(55, 65, 81)):
    p = tf.add_paragraph()
    p.font.size = Pt(font_size)
    p.space_after = Pt(space_after)
    
    if bold_prefix:
        r_bold = p.add_run()
        r_bold.text = bold_prefix + " "
        r_bold.font.bold = True
        r_bold.font.color.rgb = bold_color

    r_norm = p.add_run()
    r_norm.text = text_content
    r_norm.font.color.rgb = norm_color

def add_card(slide, left, top, width, height, bg_color=RGBColor(255, 255, 255), border_color=RGBColor(226, 232, 240)):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_shape_flat(card, bg_color, border_color, line_width=1)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.2)
    return card, tf

def main():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    prs_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung")
    chart_dir = os.path.join(prs_dir, "grafik")
    out_pptx = os.path.join(prs_dir, "presentasi_analisa_peminatan_dan_daya_tampung.pptx")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6] # blank layout

    # =============================================================
    # SLIDE 1: JUDUL & IDENTITAS PENUGASAN
    # =============================================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_shape_flat(bg1, RGBColor(248, 250, 252))

    # Left decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.4), Inches(7.5))
    set_shape_flat(bar, RGBColor(27, 59, 111))

    # Title box
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.3), Inches(11.2), Inches(5.2))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "TUGAS 05 - MAGANG (KHUSUS) | AUDIT-GRADE DECISION ANALYTICS"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = RGBColor(230, 81, 0)
    p0.space_after = Pt(12)

    p1 = tf.add_paragraph()
    p1.text = "ANALISA PEMINATAN DAN DAYA TAMPUNG\nPROGRAM STUDI UNIVERSITAS SYIAH KUALA"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(27, 59, 111)
    p1.space_after = Pt(14)

    p2 = tf.add_paragraph()
    p2.text = "Evaluasi Tren Multi-Tahun (2022–2026), Rasio Keketatan Seleksi, Matriks Portofolio Kuadran, Dekonstruksi Kebocoran Desil KIP-Kuliah, dan Rekomendasi Kebijakan PTN-BH"
    p2.font.size = Pt(14)
    p2.font.color.rgb = RGBColor(71, 85, 105)
    p2.space_after = Pt(24)

    # Metadata card inside slide 1
    meta_card, meta_tf = add_card(s1, Inches(1.2), Inches(4.5), Inches(10.8), Inches(2.2), bg_color=RGBColor(255, 255, 255), border_color=RGBColor(203, 213, 225))
    p_m_title = meta_tf.paragraphs[0]
    p_m_title.text = "INFORMASI EKSEKUTIF PENUGASAN"
    p_m_title.font.bold = True
    p_m_title.font.size = Pt(12)
    p_m_title.font.color.rgb = RGBColor(27, 59, 111)
    p_m_title.space_after = Pt(8)
    add_bullet(meta_tf, "Target Peserta Rapat:", "Rektor, Para Wakil Rektor, Ketua Senat Akademik, dan Para Dekan Fakultas", font_size=11, space_after=4)
    add_bullet(meta_tf, "Dasar Dataset Analisis:", "Data Empiris PMB USK 2022–2026, Dataset Jalur Masuk & Kebocoran, serta Data Induk KIP-Kuliah 2025–2026", font_size=11, space_after=4)
    add_bullet(meta_tf, "Penyusun & Tujuan Dokumen:", "Data Analyst PMB — Tim Magang USK | Pengambilan Keputusan Strategis Rasionalisasi Kuota, Penyelamatan Mahasiswa Prasejahtera, dan Efisiensi Finansial PTN-BH", font_size=11, space_after=2)

    # =============================================================
    # SLIDE 2: RINGKASAN EKSEKUTIF — MEMBEDAH SEGITIGA EMAS PMB USK
    # =============================================================
    s2 = prs.slides.add_slide(blank_layout)
    create_header(s2, "Ringkasan Eksekutif: Tiga Dimensi Evaluasi PMB USK Pasca Transformasi PTN-BH")

    col_w = Inches(3.64)
    card_y = Inches(1.65)
    card_h = Inches(5.3)

    # Card 1: Permintaan Pasar
    _, tf1 = add_card(s2, Inches(0.8), card_y, col_w, card_h)
    p = tf1.paragraphs[0]
    p.text = "1. DIMENSI PERMINTAAN PASAR"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(12)
    add_bullet(tf1, "Lonjakan Peminat:", "Total peminat USK melonjak dari 48.769 (2022) menjadi 68.010 (2026), sempat mencatat rekor 70.945 di 2025 (+39,5% dalam 5 tahun).")
    add_bullet(tf1, "Polarisasi Ekstrem:", "Terjadi ketimpangan tajam: Farmasi mencapai rasio 39 : 1, sedangkan Budidaya Perairan hanya 0,91 : 1 (jumlah peminat di bawah daya tampung).")
    add_bullet(tf1, "Pergeseran Minat:", "Peminat bergeser kuat ke prodi kesehatan, teknologi digital, dan kepastian formasi kerja ASN/PPPK (PGSD).")

    # Card 2: Kapasitas & Efisiensi Kuota
    _, tf2 = add_card(s2, Inches(4.84), card_y, col_w, card_h)
    p = tf2.paragraphs[0]
    p.text = "2. KAPASITAS & EFISIENSI KUOTA"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(230, 81, 0)
    p.space_after = Pt(12)
    add_bullet(tf2, "Ekspansi Kuota PTN-BH:", "Daya tampung dinaikkan agresif sebesar +32,7% (dari 7.863 menjadi 10.435 kursi) pasca transformasi PTN-BH.")
    add_bullet(tf2, "Realisasi Pendaftar Ulang:", "Realisasi mahasiswa riil naik dari 6.197 ke 8.440 mhs, namun persisten menyisakan beban ~2.000 bangku kosong per tahun.")
    add_bullet(tf2, "Disparitas Antar Segmen:", "S1 Kampus Utama relatif sehat (84,7% keterisian), namun Vokasi D3 terpuruk (51,3%) dan PSDKU Gayo Lues krisis akut (18,6%).")

    # Card 3: Resolusi Plot Twist KIP
    _, tf3 = add_card(s2, Inches(8.88), card_y, col_w, card_h)
    p = tf3.paragraphs[0]
    p.text = "3. RESOLUSI \"PLOT TWIST\" KEBOCORAN"
    p.font.bold = True
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(16, 149, 193)
    p.space_after = Pt(12)
    add_bullet(tf3, "Kesesuaian Kausalitas 97,6%:", "Anomali 626 kursi kosong di SNBT 2026 secara akurat identik dengan 611 calon mahasiswa KIP yang ditolak beasiswanya.")
    add_bullet(tf3, "Tragedi Desil 5 & 6:", "526 orang (84% kursi kosong SNBT) berasal dari keluarga prasejahtera Desil 5 dan 6 yang ditolak massal (>98%).")
    add_bullet(tf3, "Economic Forced Drop-Out:", "Terbukti kursi kosong bukan karena siswa kabur ke PTS/kedinasan, melainkan kegagalan daya beli akibat pemotongan kuota beasiswa.")

    # =============================================================
    # SLIDE 3: EVALUASI TREN MAKRO 5 TAHUN USK (2022–2026)
    # =============================================================
    s3 = prs.slides.add_slide(blank_layout)
    create_header(s3, "Evaluasi Tren Makro 5 Tahun USK: Kapasitas Melompat, Beban ~2.000 Bangku Kosong Tetap Berulang")
    
    img1 = os.path.join(chart_dir, "01_tren_makro_peminat_dt_du_usk.png")
    if os.path.exists(img1):
        s3.shapes.add_picture(img1, Inches(0.8), Inches(1.6), width=Inches(7.8))

    _, tf3_t = add_card(s3, Inches(8.85), Inches(1.6), Inches(3.68), Inches(5.3))
    p = tf3_t.paragraphs[0]
    p.text = "EVOLUSI METRIK 5 TAHUN USK:"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(10)
    add_bullet(tf3_t, "2022:", "48.769 Peminat | 7.863 Kuota | 6.197 DU | 1.666 Kosong (Fill Rate 78,8%)", font_size=10.5, space_after=6)
    add_bullet(tf3_t, "2023:", "44.653 Peminat | 8.780 Kuota | 6.299 DU | 2.481 Kosong (Fill Rate 71,7%)", font_size=10.5, space_after=6)
    add_bullet(tf3_t, "2024:", "65.495 Peminat | 10.240 Kuota | 7.791 DU | 2.449 Kosong (Fill Rate 76,1%)", font_size=10.5, space_after=6)
    add_bullet(tf3_t, "2025:", "70.945 Peminat | 10.420 Kuota | 8.027 DU | 2.393 Kosong (Fill Rate 77,0%)", font_size=10.5, space_after=6)
    add_bullet(tf3_t, "2026:", "68.010 Peminat | 10.435 Kuota | 8.440 DU | 1.995 Kosong (Fill Rate 80,9%)", font_size=10.5, space_after=8)
    add_bullet(tf3_t, "Pesan Kunci Pimpinan:", "Menambah daya tampung tanpa sinkronisasi daya serap pasar riil dan kuota beasiswa hanya menciptakan 'kursi kosong semu' yang merugikan efisiensi beban dosen, akreditasi, dan utilisasi fasilitas kampus.", font_size=10.5, space_after=4, bold_color=RGBColor(230, 81, 0))

    # =============================================================
    # SLIDE 4: PETA KEKETATAN SELEKSI & MFR 2026
    # =============================================================
    s4 = prs.slides.add_slide(blank_layout)
    create_header(s4, "Peta Keketatan Seleksi & Market Fulfillment Ratio (MFR) 2026: Disparitas 39:1 vs Peminat < Kuota")
    
    img4 = os.path.join(chart_dir, "04_rasio_keketatan_peminatan_vs_daya_tampung.png")
    if os.path.exists(img4):
        s4.shapes.add_picture(img4, Inches(0.8), Inches(1.6), width=Inches(8.0))

    _, tf4_t = add_card(s4, Inches(9.05), Inches(1.6), Inches(3.48), Inches(5.3))
    p = tf4_t.paragraphs[0]
    p.text = "FORMULASI & DISPARITAS MFR:"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf4_t, "Formulasi:", "MFR = Peminat / Kuota (Benchmark Ideal >= 3,0)", font_size=10.5, space_after=6)
    add_bullet(tf4_t, "Top 8 Paling Favorit / Ketat:", "1. Farmasi (39,18:1)\n2. D4 Akuntansi Pajak (22,43:1)\n3. Informatika (18,12:1)\n4. Psikologi (17,31:1)\n5. T. Perminyakan (15,50:1)\n6. T. Pertambangan (14,46:1)\n7. Manajemen (14,12:1)\n8. Bisnis Digital (12,79:1)", font_size=10.5, space_after=8)
    add_bullet(tf4_t, "Top 8 Paling Sepi / Rawan:", "1. Budidaya Perairan (0,91:1 - Minus!)\n2. PSP Perikanan (1,08:1)\n3. Fisika (1,18:1)\n4. Pendidikan Fisika (1,29:1)\n5. Proteksi Tanaman (1,31:1)\n6. Ilmu Tanah (1,35:1)\n7. Pendidikan Kimia (1,52:1)\n8. Pendidikan Geografi (1,56:1)", font_size=10.5, space_after=4, bold_color=RGBColor(192, 57, 43))

    # =============================================================
    # SLIDE 5: SINTESIS MATRIKS 4 KUADRAN & KLASIFIKASI TREN MULTI-TAHUN
    # =============================================================
    s5 = prs.slides.add_slide(blank_layout)
    create_header(s5, "Sintesis Matriks 4 Kuadran Portofolio & Klasifikasi Tren Multi-Tahun Program Studi")

    img10 = os.path.join(chart_dir, "10_matriks_4_kuadran_prodi_usk.png")
    if os.path.exists(img10):
        s5.shapes.add_picture(img10, Inches(0.8), Inches(1.55), width=Inches(8.2))

    _, tf5_t = add_card(s5, Inches(9.2), Inches(1.55), Inches(3.33), Inches(5.45))
    p = tf5_t.paragraphs[0]
    p.text = "AKSI MANAJERIAL PIMPINAN:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(6)
    add_bullet(tf5_t, "Kuadran I (Prime - 25 Prodi):", "MFR >= 3,2 & Fill >= 84,7%. Kedokteran, Farmasi, Informatika, PGSD, T. Sipil, Keperawatan, Hukum, Akuntansi, Tambang.\n-> AKSI: Maintain & Invest (Kelas Internasional).", font_size=10, space_after=6, bold_color=RGBColor(39, 174, 96))
    add_bullet(tf5_t, "Kuadran II (Niche - 8 Prodi):", "MFR < 3,2 & Fill >= 84,7%. Arsitektur, T. Mesin, Pend. Bahasa Indo, Peternakan.\n-> AKSI: Protect & Control (Kunci Kuota).", font_size=10, space_after=6, bold_color=RGBColor(41, 128, 185))
    add_bullet(tf5_t, "Kuadran III (Defisit - 25 Prodi):", "MFR < 3,2 & Fill < 84,7%. Budidaya Perairan, Fisika, PSP, Pend Fisika/Kimia, THP, Pend Ekonomi.\n-> AKSI: Downsize Kuota 20%-40%!", font_size=10, space_after=6, bold_color=RGBColor(192, 57, 43))
    add_bullet(tf5_t, "Kuadran IV (Bocor - 8 Prodi):", "MFR >= 3,2 & Fill < 84,7%. Manajemen FEB, Eko Islam, Eko Pembangunan, Sosiologi, Agribisnis.\n-> AKSI: Retain & Convert (Cicilan IPI).", font_size=10, space_after=4, bold_color=RGBColor(230, 81, 0))

    # =============================================================
    # SLIDE 6: BINTANG PERTUMBUHAN VS SINYAL WASPADA (ANALISIS TREN OLS)
    # =============================================================
    s6 = prs.slides.add_slide(blank_layout)
    create_header(s6, "Bintang Pertumbuhan vs Sinyal Waspada: Analisis Slope OLS & CAGR Multi-Tahun")

    img2 = os.path.join(chart_dir, "02_top_tren_peningkatan_pendaftar_dan_peminat.png")
    img3 = os.path.join(chart_dir, "03_top_tren_penurunan_pendaftar_dan_peminat.png")
    if os.path.exists(img2):
        s6.shapes.add_picture(img2, Inches(0.8), Inches(1.55), width=Inches(5.75))
    if os.path.exists(img3):
        s6.shapes.add_picture(img3, Inches(6.78), Inches(1.55), width=Inches(5.75))

    # 2 Bottom Summary Cards
    _, tf6_l = add_card(s6, Inches(0.8), Inches(5.6), Inches(5.75), Inches(1.55), bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    p = tf6_l.paragraphs[0]
    p.text = "TOP BINTANG PERTUMBUHAN RIIL (OLS POSITIF)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(22, 101, 52)
    p.space_after = Pt(4)
    add_bullet(tf6_l, "1. Keperawatan:", "Slope +38,4 mhs/thn (CAGR +23,5%, 127 -> 295 mhs). Pasar ners global.", font_size=10, space_after=2)
    add_bullet(tf6_l, "2. PGSD (FKIP):", "Slope +27,4 mhs/thn (CAGR +19,9%, 105 -> 217 mhs). 4 thn beruntun naik! Kepastian PPPK.", font_size=10, space_after=2)
    add_bullet(tf6_l, "3. Sipil & Komputer:", "Masing-masing tumbuh konsisten (+23,0 & +14,8 mhs/thn) sejalan digitalisasi & infrastruktur.", font_size=10, space_after=1)

    _, tf6_r = add_card(s6, Inches(6.78), Inches(5.6), Inches(5.75), Inches(1.55), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    p = tf6_r.paragraphs[0]
    p.text = "TOP SINYAL WASPADA (KONTRAKSI BERKELANJUTAN)"
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(153, 27, 27)
    p.space_after = Pt(4)
    add_bullet(tf6_r, "1. Manajemen FEB:", "Slope -16,4 mhs/thn (CAGR -7,0%, 266 -> 199 mhs). Terkanibalisasi Bisnis Digital.", font_size=10, space_after=2)
    add_bullet(tf6_r, "2. Ekonomi Islam & Pembangunan:", "Turun konsisten 3 thn beruntun (Slope -10,3 & -7,7 mhs/thn).", font_size=10, space_after=2)
    add_bullet(tf6_r, "3. Sains Murni & Perikanan:", "Matematika (-2,9 mhs/thn) & PSP (-3,7 mhs/thn) mengalami pelemahan minat.", font_size=10, space_after=1)

    # =============================================================
    # SLIDE 7: FENOMENA OVER-EKSPANSI KUOTA PADA KUADRAN III
    # =============================================================
    s7 = prs.slides.add_slide(blank_layout)
    create_header(s7, "Fenomena Over-Ekspansi Kuota: Tambah Daya Tampung Tidak Menambah Mahasiswa")

    img5 = os.path.join(chart_dir, "05_over_ekspansi_kuota_vs_daftar_ulang_riil.png")
    if os.path.exists(img5):
        s7.shapes.add_picture(img5, Inches(0.8), Inches(1.6), width=Inches(8.0))

    _, tf7_t = add_card(s7, Inches(9.05), Inches(1.6), Inches(3.48), Inches(5.3))
    p = tf7_t.paragraphs[0]
    p.text = "BUKTI EMPIRIS OVER-EKSPANSI:"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf7_t, "Budidaya Perairan:", "Kuota dipatok 160 kursi, mahasiswa masuk macet di 90 mhs -> 70 Kursi Kosong (Keterisian 56,3%).", font_size=10.5, space_after=6)
    add_bullet(tf7_t, "THP Pertanian:", "Kuota dinaikkan 2x (80 ke 160), daftar ulang hanya 102 mhs -> 58 Kursi Kosong.", font_size=10.5, space_after=6)
    add_bullet(tf7_t, "Pendidikan Ekonomi:", "Kuota dinaikkan ke 160, daftar ulang hanya 103 mhs -> 57 Kursi Kosong.", font_size=10.5, space_after=6)
    add_bullet(tf7_t, "Teknik Kimia:", "Kuota dinaikkan ke 180, daftar ulang hanya 120 mhs -> 60 Kursi Kosong.", font_size=10.5, space_after=6)
    add_bullet(tf7_t, "PSP Perikanan:", "Kuota dipatok 120, daftar ulang hanya 67 mhs -> 53 Kursi Kosong.", font_size=10.5, space_after=6)
    add_bullet(tf7_t, "Dampak Manajerial:", "Merasionalkan kuota 5 prodi ini ke angka 80–120 menghapus ~300 kursi kosong semu tanpa kehilangan 1 pun mahasiswa riil!", font_size=10.5, space_after=4, bold_color=RGBColor(230, 81, 0))

    # =============================================================
    # SLIDE 8: DINAMIKA JALUR MASUK & CORONG KEBOCORAN RESMI USK (2026)
    # =============================================================
    s8 = prs.slides.add_slide(blank_layout)
    create_header(s8, "Dinamika Jalur Masuk & Corong Kebocoran Calon Mahasiswa Resmi USK (2026)")

    img6 = os.path.join(chart_dir, "06_dinamika_jalur_masuk_dan_kebocoran_2026.png")
    if os.path.exists(img6):
        s8.shapes.add_picture(img6, Inches(0.8), Inches(1.6), width=Inches(8.1))

    _, tf8_t = add_card(s8, Inches(9.12), Inches(1.6), Inches(3.41), Inches(5.3))
    p = tf8_t.paragraphs[0]
    p.text = "KOMPOSISI & KEBOCORAN JALUR:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf8_t, "SNBT (38,6%):", "Kontributor volume terbesar (3.260 mhs). Mengalami kebocoran 626 calon (Yield 83,9%).", font_size=10.5, space_after=6)
    add_bullet(tf8_t, "SNBP (32,6%):", "Penopang mutu akademik (2.754 mhs). Paling loyal (Yield 94,8%), hanya 151 orang gugur berkat sanksi blacklist SNPMB.", font_size=10.5, space_after=6)
    add_bullet(tf8_t, "SMMPTN Mandiri (21,5%):", "1.814 mhs masuk. Bocor 604 calon (Yield 75,0%) akibat batas bayar IPI 5 hari yang sangat sempit.", font_size=10.5, space_after=6)
    add_bullet(tf8_t, "TALENTA (Bocor Parah):", "930 calon gugur (Yield hanya 24,9%). 3 dari 4 calon kabur karena dijadikan tiket cadangan gratis menjelang UTBK.", font_size=10.5, space_after=6)
    add_bullet(tf8_t, "SMC & ADIK (2,6%):", "Menyerap 205 mhs mandiri cadangan dan 20 mhs afirmasi 3T Papua/3T Aceh.", font_size=10.5, space_after=4)

    # =============================================================
    # SLIDE 9: RESOLUSI "PLOT TWIST": INVESTIGASI KEBOCORAN SNBT 2026
    # =============================================================
    s9 = prs.slides.add_slide(blank_layout)
    create_header(s9, "Resolusi \"Plot Twist\": Kursi Kosong SNBT Akibat Terhempas Pemotongan Kuota KIP-Kuliah!")

    img20 = os.path.join(chart_dir, "20_analisis_desil_dan_rejection_kip_snbt.png")
    if os.path.exists(img20):
        s9.shapes.add_picture(img20, Inches(0.8), Inches(1.6), width=Inches(7.8))

    _, tf9_t = add_card(s9, Inches(8.85), Inches(1.6), Inches(3.68), Inches(5.3))
    p = tf9_t.paragraphs[0]
    p.text = "KORELASI KAUSALITAS 97,6%:"
    p.font.bold = True
    p.font.size = Pt(13.5)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf9_t, "Kesesuaian Matematis:", "Calon Gugur SNBT 2026 (626 Orang) nyaris 100% identik dengan Pendaftar KIP SNBT Ditolak Kampus (611 Orang).\n-> Rasio Kesesuaian = 611 / 626 = 97,60%!", font_size=10.5, space_after=8, bold_color=RGBColor(230, 81, 0))
    add_bullet(tf9_t, "Mengapa Penolakan KIP Meledak?", "Pada 2025: Kuota KIP USK = 1.846 kursi, penolakan KIP SNBT hanya 370 orang (29,0%).\nPada 2026: Kuota KIP USK dipangkas 207 kursi (-11,2%) menjadi 1.639 kursi.", font_size=10.5, space_after=6)
    add_bullet(tf9_t, "Efek Penyerapan SNBP:", "Karena 893 kursi KIP terserap di SNBP, kuota sisa KIP untuk SNBT terpangkas menjadi 746 kursi, sementara pendaftar KIP UTBK naik ke 1.361 orang -> 611 siswa KIP ditolak (+65,1%!).", font_size=10.5, space_after=4)

    # =============================================================
    # SLIDE 10: "THE SMOKING GUN": EFEK JURANG (CLIFF-EDGE) CUTOFF DESIL 5 & 6
    # =============================================================
    s10 = prs.slides.add_slide(blank_layout)
    create_header(s10, "\"The Smoking Gun\": Penolakan KIP Terkonsentrasi Penuh pada Siswa Prasejahtera Desil 5 & 6")

    # Left visual card: Desil acceptance breakdown
    _, tf10_l = add_card(s10, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.3), bg_color=RGBColor(255, 255, 255), border_color=RGBColor(203, 213, 225))
    p = tf10_l.paragraphs[0]
    p.text = "PROFIL PENERIMAAN KIP SNBT 2026 BERDASARKAN DESIL DTKS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(10)

    add_bullet(tf10_l, "Desil 1 (Sangat Miskin):", "221 Pendaftar | 200 Diterima (90,5%) | 21 Ditolak [Lolos Aman]", font_size=11, space_after=6, bold_color=RGBColor(22, 101, 52))
    add_bullet(tf10_l, "Desil 2 (Miskin):", "186 Pendaftar | 162 Diterima (87,1%) | 24 Ditolak [Lolos Aman]", font_size=11, space_after=6, bold_color=RGBColor(22, 101, 52))
    add_bullet(tf10_l, "Desil 3 (Hampir Miskin):", "219 Pendaftar | 204 Diterima (93,2%) | 15 Ditolak [Lolos Aman]", font_size=11, space_after=6, bold_color=RGBColor(22, 101, 52))
    add_bullet(tf10_l, "Desil 4 (Rentan Miskin):", "176 Pendaftar | 160 Diterima (90,9%) | 16 Ditolak [Lolos Aman]", font_size=11, space_after=10, bold_color=RGBColor(22, 101, 52))

    p_div = tf10_l.add_paragraph()
    p_div.text = "------------------ GARIS CUTOFF AMBANG KUOTA KIP APBN ------------------"
    p_div.font.size = Pt(9.5)
    p_div.font.bold = True
    p_div.font.color.rgb = RGBColor(220, 38, 38)
    p_div.space_after = Pt(10)

    add_bullet(tf10_l, "Desil 5 (Prasejahtera Menengah):", "149 Pendaftar | HANYA 3 DITERIMA (2,0%) | 146 DITOLAK (98,0%)!", font_size=11, space_after=6, bold_color=RGBColor(220, 38, 38))
    add_bullet(tf10_l, "Desil 6 (Prasejahtera Menengah):", "385 Pendaftar | HANYA 5 DITERIMA (1,3%) | 380 DITOLAK (98,7%)!", font_size=11, space_after=8, bold_color=RGBColor(220, 38, 38))
    add_bullet(tf10_l, "TOTAL DESIL 5 & 6 DITOLAK:", "526 CALON MAHASISWA BERPRESTASI UTBK!", font_size=11.5, space_after=2, bold_color=RGBColor(185, 28, 28))

    # Right explanatory card: Economic Forced Drop-Out
    _, tf10_r = add_card(s10, Inches(7.05), Inches(1.6), Inches(5.48), Inches(5.3), bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    p = tf10_r.paragraphs[0]
    p.text = "MEKANISME ECONOMIC FORCED DROP-OUT"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(185, 28, 28)
    p.space_after = Pt(12)
    add_bullet(tf10_r, "1. Pengalihan Otomatis ke UKT Reguler:", "Sebanyak 526 calon mahasiswa Desil 5 & 6 yang ditolak beasiswanya langsung dialihkan ke tagihan UKT Kelompok 3-5 (Rp 2,5 – 5 Juta/semester).", font_size=11, space_after=10)
    add_bullet(tf10_r, "2. Profil Keluarga Prasejahtera:", "Desil 5 dan 6 di Aceh adalah keluarga petani kecil, buruh harian, nelayan tradisional, dan pedagang mikro yang tidak memiliki kesiapan dana tunai jutaan rupiah.", font_size=11, space_after=10)
    add_bullet(tf10_r, "3. Mundur Terpaksa (Bukan Kabur):", "Menghadapi tagihan UKT tanpa beasiswa dalam tempo verifikasi yang sempit, 526 calon mahasiswa ini terpaksa tidak mendaftar ulang.", font_size=11, space_after=10)
    add_bullet(tf10_r, "4. Sumber 84% Kursi Kosong SNBT:", "526 dari 626 bangku kosong SNBT (84,0%) secara langsung tercipta dari tragedi keterbatasan kuota KIP ini!", font_size=11.5, space_after=4, bold_color=RGBColor(185, 28, 28))

    # =============================================================
    # SLIDE 11: SINKRONISASI SEKTORAL: PROGRAM STUDI PALING TERDAMPAK
    # =============================================================
    s11 = prs.slides.add_slide(blank_layout)
    create_header(s11, "Sinkronisasi Sektoral: Korelasi Riil Calon Gugur vs Penolakan KIP Desil 5–6 per Prodi")

    img23 = os.path.join(chart_dir, "23_korelasi_prodi_calon_gugur_vs_kip_desil.png")
    if os.path.exists(img23):
        s11.shapes.add_picture(img23, Inches(0.8), Inches(1.6), width=Inches(7.8))

    _, tf11_t = add_card(s11, Inches(8.85), Inches(1.6), Inches(3.68), Inches(5.3))
    p = tf11_t.paragraphs[0]
    p.text = "BUKTI PARALELISME PER PRODI:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf11_t, "Keperawatan:", "20 Calon Gugur <-> 20 KIP Desil 5–6 Ditolak (Korelasi 100% Presisi!)", font_size=10.5, space_after=5, bold_color=RGBColor(220, 38, 38))
    add_bullet(tf11_t, "Akuntansi:", "20 Calon Gugur <-> 14 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "Budidaya Perairan:", "16 Calon Gugur <-> 12 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "Ilmu Politik:", "16 Calon Gugur <-> 12 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "Ilmu Hukum:", "14 Calon Gugur <-> 15 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "Ilmu Pemerintahan:", "12 Calon Gugur <-> 14 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "PGSD FKIP:", "9 Calon Gugur <-> 20 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "THP Pertanian:", "8 Calon Gugur <-> 19 KIP Desil 5–6 Ditolak", font_size=10.5, space_after=5)
    add_bullet(tf11_t, "Kesimpulan Audit:", "Terbukti bahwa prodi rumpun kesehatan, keguruan, pertanian, dan sospol mengalami kursi kosong murni karena benturan ekonomi siswa, bukan ketiadaan peminat.", font_size=10, space_after=2, bold_color=RGBColor(230, 81, 0))

    # =============================================================
    # SLIDE 12: STRATIFIKASI SOSIAL-EKONOMI ANTAR KUADRAN PORTOFOLIO USK
    # =============================================================
    s12 = prs.slides.add_slide(blank_layout)
    create_header(s12, "Stratifikasi Sosial-Ekonomi: Kuadran III Berperan Sebagai Jaring Pengaman Sosial USK")

    img21 = os.path.join(chart_dir, "21_ketergantungan_kip_antar_kuadran_dan_top_prodi.png")
    if os.path.exists(img21):
        s12.shapes.add_picture(img21, Inches(0.8), Inches(1.6), width=Inches(7.8))

    _, tf12_t = add_card(s12, Inches(8.85), Inches(1.6), Inches(3.68), Inches(5.3))
    p = tf12_t.paragraphs[0]
    p.text = "PENETRASI KIP PER KUADRAN:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf12_t, "Kuadran I (Unggulan):", "Penetrasi KIP 13,19% (515 KIP dari 3.905 mhs). Mandiri finansial, didominasi pembayar UKT tinggi dan IPI puluhan juta.", font_size=10.5, space_after=6)
    add_bullet(tf12_t, "Kuadran II (Niche):", "Penetrasi KIP 14,63% (153 KIP dari 1.046 mhs).", font_size=10.5, space_after=6)
    add_bullet(tf12_t, "Kuadran IV (Bocor):", "Penetrasi KIP 24,47% (163 KIP dari 666 mhs).", font_size=10.5, space_after=6)
    add_bullet(tf12_t, "Kuadran III (Defisit/Rentan):", "Penetrasi KIP 31,11% (734 KIP dari 2.359 mhs). Sangat bergantung beasiswa! Penetrasi KIP mencapai 2,4x lipat Kuadran I.", font_size=10.5, space_after=8, bold_color=RGBColor(220, 38, 38))
    add_bullet(tf12_t, "Top KIP Dependency (Kuadran III):", "PSP Perikanan (56,7%), Pend. Fisika (53,9%), Budidaya Perairan (51,1%), Pend. Ekonomi (49,5%), Pend. Kimia (48,0%).", font_size=10, space_after=6)
    add_bullet(tf12_t, "Lowest KIP (Kuadran I Elite):", "Dokter Gigi (1,0%), Dokter (2,4%), Informatika (3,4%), T. Perminyakan (3,9%), Tambang (5,1%).", font_size=10, space_after=2)

    # =============================================================
    # SLIDE 13: PROFIL DEMOGRAFIS PENERIMA KIP-KULIAH USK 2026
    # =============================================================
    s13 = prs.slides.add_slide(blank_layout)
    create_header(s13, "Profil Demografis Penerima KIP-Kuliah: Sebaran Fakultas, Gender, dan Jalur Masuk")

    img22 = os.path.join(chart_dir, "22_demografi_fakultas_dan_gender_kip_2026.png")
    if os.path.exists(img22):
        s13.shapes.add_picture(img22, Inches(0.8), Inches(1.6), width=Inches(7.8))

    _, tf13_t = add_card(s13, Inches(8.85), Inches(1.6), Inches(3.68), Inches(5.3))
    p = tf13_t.paragraphs[0]
    p.text = "RINGKASAN DEMOGRAFIS KIP:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf13_t, "1. FKIP Penyerap Utama (39,7%):", "FKIP menyerap 651 mahasiswa KIP (hampir 40% kuota seluruh universitas!). Disusul Pertanian (218), FEB (153), FT (152), FPK (133), FISIP (118), FMIPA (70), Keperawatan (63), Hukum (55), FKH (15), FK (10), FKG (1).", font_size=10.5, space_after=8)
    add_bullet(tf13_t, "2. Feminisme Pendidikan Tinggi:", "Perempuan: 1.268 mhs (77,36%) vs Laki-laki: 371 mhs (22,64%). Rasio 3,4 : 1 membuktikan KIP-Kuliah adalah lokomotif utama mobilitas sosial anak perempuan prasejahtera di Aceh.", font_size=10.5, space_after=8, bold_color=RGBColor(230, 81, 0))
    add_bullet(tf13_t, "3. Distribusi Jalur Masuk:", "SNBP (Prestasi Rapor): 893 mhs (54,48%) vs SNBT (Tes UTBK): 746 mhs (45,52%). Penyerapan dini di SNBP memangkas jatah KIP untuk SNBT.", font_size=10.5, space_after=4)

    # =============================================================
    # SLIDE 14: KINERJA FAKULTAS, VOKASI D3, & PSDKU GAYO LUES
    # =============================================================
    s14 = prs.slides.add_slide(blank_layout)
    create_header(s14, "Evaluasi Kinerja 12 Fakultas dan Pemetaan Krisis Akut Dua Segmen Khusus")

    img7 = os.path.join(chart_dir, "07_analisa_peminatan_dan_keterisian_fakultas.png")
    if os.path.exists(img7):
        s14.shapes.add_picture(img7, Inches(0.8), Inches(1.6), width=Inches(7.8))

    _, tf14_t = add_card(s14, Inches(8.85), Inches(1.6), Inches(3.68), Inches(5.3))
    p = tf14_t.paragraphs[0]
    p.text = "ZONASI FAKULTAS & SEGMEN KHUSUS:"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(tf14_t, "Zona Prima (98-100%):", "FKG (100%), Fakultas Hukum (99,6%), dan Kedokteran (98,8%). Kursi terisi penuh sempurna.", font_size=10.5, space_after=5, bold_color=RGBColor(22, 101, 52))
    add_bullet(tf14_t, "Zona Sehat (>80%):", "FISIP (89,6%), FKH (88,5%), Keperawatan (81,9%), FMIPA (81,9%), FKIP (81,5%), FT (81,4%).", font_size=10.5, space_after=5)
    add_bullet(tf14_t, "Zona Kritis (<80%):", "FEB (77,2%), FPK (62,4%), Fakultas Pertanian (62,1%). Perlu rasionalisasi kuota.", font_size=10.5, space_after=6, bold_color=RGBColor(220, 38, 38))
    add_bullet(tf14_t, "Krisis Vokasi D3 (51,3%):", "Dari 665 kuota tersisa 324 kursi kosong. Lulusan terbentur golongan II/c ASN. Solusi: Konversi bertahap ke D4 Sarjana Terapan (Golongan III/a).", font_size=10.5, space_after=6)
    add_bullet(tf14_t, "Krisis PSDKU Gayo Lues (18,6%):", "Dari 220 kuota hanya terisi 41 mhs (81,4% kosong melompong). Wajib diikat MoU beasiswa Pemkab atau dirampingkan ke 2 prodi lokal.", font_size=10.5, space_after=2)

    # =============================================================
    # SLIDE 15: REKOMENDASI KEBIJAKAN STRATEGIS BAGI REKTORAT & PTN-BH USK
    # =============================================================
    s15 = prs.slides.add_slide(blank_layout)
    create_header(s15, "5 Rekomendasi Kebijakan Strategis Rektorat & PTN-BH Menuju PMB 2027 yang Efisien & Berkeadilan")

    card_w5 = Inches(2.26)
    card_y5 = Inches(1.6)
    card_h5 = Inches(5.35)

    # Rec 1: Rasionalisasi Kuota
    _, r1 = add_card(s15, Inches(0.8), card_y5, card_w5, card_h5)
    p = r1.paragraphs[0]
    p.text = "AKSI 1:\nRASIONALISASI KUOTA"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(192, 57, 43)
    p.space_after = Pt(8)
    add_bullet(r1, "Pangkas Kuadran III:", "Kurangi kuota 20%-40% pada: Budidaya Perairan (160->90), THP (160->100), Pend. Ekonomi (160->100), T. Kimia (180->120), Fisika (80->50), PSP (120->75).", font_size=10, space_after=6)
    add_bullet(r1, "Hasil Strategis:", "Menghapus ~300 bangku kosong semu tanpa mengurangi mahasiswa riil, mendongkrak Fill Rate institusi.", font_size=10, space_after=2)

    # Rec 2: UKT Penyelamat Desil 5-6
    _, r2 = add_card(s15, Inches(3.18), card_y5, card_w5, card_h5)
    p = r2.paragraphs[0]
    p.text = "AKSI 2:\nUKT PENYELAMAT DESIL 5 & 6"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(230, 81, 0)
    p.space_after = Pt(8)
    add_bullet(r2, "SK Rektor Transisi:", "Pelamar KIP SNBT Desil 5-6 yang tidak tertampung kuota APBN otomatis masuk UKT 1 (Rp500rb) atau UKT 2 (Rp1jt) di semester 1.", font_size=10, space_after=6)
    add_bullet(r2, "Hasil Strategis:", "Menyelamatkan 300+ calon mahasiswa berprestasi UTBK agar tidak putus kuliah akibat tagihan jutaan rupiah.", font_size=10, space_after=2)

    # Rec 3: Subsidi Silang IPI
    _, r3 = add_card(s15, Inches(5.56), card_y5, card_w5, card_h5)
    p = r3.paragraphs[0]
    p.text = "AKSI 3:\nSUBSIDI SILANG IPI MANDIRI"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(r3, "KIP Kemitraan PTN-BH:", "Alokasikan 5% dari surplus penerimaan IPI Mandiri Kuadran I (~Rp 2,0 Miliar) sebagai beasiswa mandiri USK.", font_size=10, space_after=6)
    add_bullet(r3, "Hasil Strategis:", "Mendanai UKT 800+ mahasiswa prasejahtera di prodi Kuadran III penopang ketahanan pangan dan sains.", font_size=10, space_after=2)

    # Rec 4: Cicilan IPI & Kunci TALENTA
    _, r4 = add_card(s15, Inches(7.94), card_y5, card_w5, card_h5)
    p = r4.paragraphs[0]
    p.text = "AKSI 4:\nCICILAN IPI & KUNCI TALENTA"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(41, 128, 185)
    p.space_after = Pt(8)
    add_bullet(r4, "Sosialisasi Cicilan:", "Masifkan prosedur cicilan IPI sejak awal pendaftaran mandiri untuk cegah liquidity shock orang tua.", font_size=10, space_after=6)
    add_bullet(r4, "Kunci TALENTA:", "Terapkan uang komitmen registrasi Rp 1 Juta agar tidak dijadikan tiket cadangan gratis menjelang UTBK.", font_size=10, space_after=2)

    # Rec 5: Baitul Mal Aceh & Otsus
    _, r5 = add_card(s15, Inches(10.32), card_y5, card_w5, card_h5)
    p = r5.paragraphs[0]
    p.text = "AKSI 5:\nSINERGI BAITUL MAL & OTSUS"
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(22, 101, 52)
    p.space_after = Pt(8)
    add_bullet(r5, "Advokasi Dana Daerah:", "Ajukan daftar 526 calon mahasiswa Desil 5-6 kepada Baitul Mal Aceh & Pemprov sebagai mustahik beasiswa Fisabilillah/Fakir Miskin.", font_size=10, space_after=6)
    add_bullet(r5, "Hasil Strategis:", "Mengintegrasikan dana otonomi daerah dengan misi pengentasan kemiskinan berbasis pendidikan tinggi.", font_size=10, space_after=2)

    # =============================================================
    # SLIDE 16: PENUTUP & PESAN KUNCI PIMPINAN
    # =============================================================
    s16 = prs.slides.add_slide(blank_layout)
    bg16 = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    set_shape_flat(bg16, RGBColor(27, 59, 111))

    # Quote Box
    q_box = s16.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(10.9), Inches(2.3))
    q_tf = q_box.text_frame
    q_tf.word_wrap = True

    p_qt0 = q_tf.paragraphs[0]
    p_qt0.text = "UNIVERSITAS SYIAH KUALA | PESAN KUNCI PIMPINAN"
    p_qt0.font.size = Pt(12)
    p_qt0.font.bold = True
    p_qt0.font.color.rgb = RGBColor(230, 81, 0)
    p_qt0.alignment = PP_ALIGN.CENTER
    p_qt0.space_after = Pt(12)

    p_qt = q_tf.add_paragraph()
    p_qt.text = "\"Tolak ukur keberhasilan PMB PTN-BH bukanlah seberapa besar daya tampung yang kita umumkan di atas kertas, melainkan seberapa presisi kuota tersebut terisi oleh mahasiswa yang nyata, berdaya beli, atau terlindungi beasiswanya hingga lulus tepat waktu.\""
    p_qt.font.size = Pt(16.5)
    p_qt.font.italic = True
    p_qt.font.bold = True
    p_qt.font.color.rgb = RGBColor(255, 255, 255)
    p_qt.alignment = PP_ALIGN.CENTER

    # 3 Takeaway Cards at bottom
    col_w16 = Inches(3.45)
    y16 = Inches(3.4)
    h16 = Inches(3.4)

    # Card 1
    _, t1 = add_card(s16, Inches(1.2), y16, col_w16, h16, bg_color=RGBColor(255, 255, 255), border_color=RGBColor(203, 213, 225))
    p = t1.paragraphs[0]
    p.text = "1. AUDIT DATA MEMBUKTIKAN"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(27, 59, 111)
    p.space_after = Pt(8)
    add_bullet(t1, "Bukan Masalah Minat:", "Kebocoran SNBT adalah masalah keterbatasan kuota beasiswa (pemotongan KIP & cutoff Desil 5-6), bukan ketidakmampuan universitas menarik minat calon mahasiswa berprestasi.", font_size=11, space_after=6)
    add_bullet(t1, "Data Empiris:", "Kausalitas 97,6% membuktikan bahwa siswa yang gugur adalah anak prasejahtera yang terhempas ketiadaan beasiswa.", font_size=11, space_after=2)

    # Card 2
    _, t2 = add_card(s16, Inches(4.94), y16, col_w16, h16, bg_color=RGBColor(255, 255, 255), border_color=RGBColor(203, 213, 225))
    p = t2.paragraphs[0]
    p.text = "2. EFISIENSI MENYELAMATKAN AKREDITASI"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(230, 81, 0)
    p.space_after = Pt(8)
    add_bullet(t2, "Menghapus Bangku Semu:", "Merasionalkan kuota Kuadran III adalah strategi penyehatan mutu akademik dan efisiensi institusi, bukan bentuk pelemahan prodi atau fakultas.", font_size=11, space_after=6)
    add_bullet(t2, "Optimalisasi Rasio Dosen:", "Kapasitas yang pas menjaga rasio dosen-mahasiswa dan instrumen akreditasi unggul internasional.", font_size=11, space_after=2)

    # Card 3
    _, t3 = add_card(s16, Inches(8.68), y16, col_w16, h16, bg_color=RGBColor(255, 255, 255), border_color=RGBColor(203, 213, 225))
    p = t3.paragraphs[0]
    p.text = "3. KEBERPIHAKAN SOSIAL PTN-BH"
    p.font.bold = True
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(22, 101, 52)
    p.space_after = Pt(8)
    add_bullet(t3, "Kemandirian Berkeadilan:", "Fleksibilitas finansial PTN-BH harus menjadi berkah bagi mahasiswa prasejahtera melalui subsidi silang IPI mandiri ke program beasiswa universitas.", font_size=11, space_after=6)
    add_bullet(t3, "Jantong Hate Rakyat Aceh:", "Menjaga marwah USK sebagai benteng kesempatan pendidikan tinggi bagi seluruh lapisan masyarakat Aceh.", font_size=11, space_after=2)

    # Save presentation
    prs.save(out_pptx)
    print(f"[OK] Successfully built 16-slide presentation: {out_pptx}")

if __name__ == "__main__":
    main()
