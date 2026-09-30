#!/usr/bin/env python3
"""
generate_pptx_deck.py
Mengenerate presentasi PowerPoint (.pptx) 16:9 eksekutif lengkap.
100% KONSISTEN dengan template tim:
- Logo resmi USK & Maganghub di kiri atas setiap slide
- Pattern dot grid di kanan atas setiap slide
- Aksen garis vertikal kuning emas (|) sebelum judul
- Font Cerebri Sans di seluruh teks dan judul
- Warna judul resmi USK Forest Green (#1B4332)
- Dilengkapi speaker notes lengkap untuk setiap slide
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

def create_deck():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub/tugas-5/analisa_peminatan_dan_daya_tampung"
    grafik_dir = os.path.join(base_dir, "grafik")
    pdf_slides_dir = os.path.join(grafik_dir, "pdf_slides")
    output_pptx = os.path.join(base_dir, "ANALISIS_DAYA_TAMPUNG_DAN_PEMINATAN_USK_2022_2026.pptx")

    logo_path = os.path.join(grafik_dir, "header_logos_trans.png")
    dots_path = os.path.join(grafik_dir, "header_dots_trans.png")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Palet Warna Resmi
    c_forest = RGBColor(27, 67, 50)       # #1B4332 - USK Forest Green
    c_dark_green = RGBColor(15, 43, 31)   # #0F2B1F
    c_gold = RGBColor(245, 158, 11)       # #F59E0B - Mustard Accent Yellow
    c_slate = RGBColor(15, 23, 42)        # #0F172A
    c_sub_slate = RGBColor(71, 85, 105)   # #475569
    c_card_bg = RGBColor(248, 250, 252)   # #F8FAFC
    c_white = RGBColor(255, 255, 255)
    c_border = RGBColor(203, 213, 225)    # #CBD5E1

    FONT_NAME = "Cerebri Sans"

    def add_notes(slide, text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = text.strip()

    def add_standard_header(slide, title_text):
        """Menambahkan Header Standar yang 100% seragam dengan slide tim"""
        # 1. Background putih bersih
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_white
        bg.line.fill.background()

        # 2. Logo USK + Maganghub (kiri atas)
        if os.path.exists(logo_path):
            slide.shapes.add_picture(logo_path, Inches(0.45), Inches(0.32), width=Inches(2.75), height=Inches(0.58))

        # 3. Dots pattern dekoratif (kanan atas)
        if os.path.exists(dots_path):
            slide.shapes.add_picture(dots_path, Inches(12.20), Inches(0.35), width=Inches(0.55), height=Inches(0.55))

        # 4. Aksen Garis Kuning Emas (|)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.55), Inches(1.10), Inches(0.10), Inches(0.40))
        bar.fill.solid()
        bar.fill.fore_color.rgb = c_gold
        bar.line.fill.background()

        # 5. Judul Slide dalam Font Cerebri Sans, Warna USK Forest Green
        tb = slide.shapes.add_textbox(Inches(0.78), Inches(1.02), Inches(11.2), Inches(0.58))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.name = FONT_NAME
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = c_forest

    print("Membangun Master Deck 100% Konsisten...")

    # =========================================================================
    # SLIDE 1: COVER
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    cover_img = os.path.join(pdf_slides_dir, "slide_01.png")
    if os.path.exists(cover_img):
        s1.shapes.add_picture(cover_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s1, """Assalamu’alaikum Warahmatullahi Wabarakatuh. Selamat pagi Bapak Rektor, Bapak/Ibu Wakil Rektor, dan para Dekan Fakultas yang kami hormati.

Hari ini kami menyajikan evaluasi komprehensif 5 tahun perjalanan penerimaan mahasiswa baru USK dari tahun 2022 hingga 2026. Analisis ini kami dedikasikan untuk menjawab satu pertanyaan penting: bagaimana USK pasca-status PTN-BH dapat menata daya tampung secara presisi, meminimalisir kursi kosong, dan mengoptimalkan mutu mahasiswa baru.

Mari kita mulai dengan melihat potret besar universitas di Slide 2.""")

    # =========================================================================
    # SLIDE 2: TREN MAKRO
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    s2_img = os.path.join(pdf_slides_dir, "slide_02.png")
    if os.path.exists(s2_img):
        s2.shapes.add_picture(s2_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s2, """Bapak Rektor dan Bapak Dekan, di permukaan, USK tampak sangat sehat. Dalam 5 tahun terakhir, minat pendaftar melonjak hampir 40%, mendekati 68 ribu peminat.

Sebagai respons transisi PTN-BH, kita menaikkan kuota agresif sebesar lebih dari 2.500 kursi. Namun, grafik ini menunjukkan alarm: garis keterisian kita tertahan di angka 76% hingga 80%. Artinya, ada sekitar 2.000 bangku kuliah yang setiap tahunnya kita sediakan tapi berakhir kosong tanpa mahasiswa.

Lalu, di titik mana sebenarnya calon mahasiswa ini mulai berkurang? Mari kita bedah corong seleksinya di Slide 3.""")

    # =========================================================================
    # SLIDE 3: FUNNEL PIPELINE (CHART A1) - DENGAN LOGO & FONT KONSISTEN
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_standard_header(s3, "Corong Seleksi dan Kebocoran Kelulusan Mahasiswa Baru")
    a1_img = os.path.join(grafik_dir, "A1_funnel_perjalanan_calon_mahasiswa.png")
    if os.path.exists(a1_img):
        # Center horizontally: width=11.0 in, left=(13.333-11.0)/2 = 1.16 in
        s3.shapes.add_picture(a1_img, Inches(1.16), Inches(1.72), width=Inches(11.0), height=Inches(5.45))
    add_notes(s3, """Slide ini membedah seluruh siklus hidup calon mahasiswa kita selama 5 tahun. Dari 272 ribu orang yang mendaftar, panitia meluluskan 41.745 orang (S1 Kampus Utama).

Namun perhatikan celah merah paling bawah: ada 6.651 calon mahasiswa yang sudah lulus seleksi tetapi TIDAK mendaftar ulang. Ini setara dengan hilangnya potensi 133 rombongan belajar (kelas).

Pada tahun 2026, angka pembatalan pendaftaran ulang tercatat 1.368 orang (S1 Kampus Utama) dengan yield rate stabil di 85,4%.

Ke mana perginya para mahasiswa yang mundur ini dan di jalur mana kebocoran terbesar terjadi? Kita lihat di Slide 4.""")

    # =========================================================================
    # SLIDE 4: JALUR MASUK & KEBOCORAN PER JALUR (DATA 2026 TERVERIFIKASI)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_standard_header(s4, "Dinamika Penerimaan dan Mahasiswa Daftar Ulang per Jalur")
    s4_chart = os.path.join(grafik_dir, "14_dual_panel_jalur_masuk_dan_kebocoran.png")
    if os.path.exists(s4_chart):
        s4.shapes.add_picture(s4_chart, Inches(0.6), Inches(1.52), width=Inches(12.133), height=Inches(4.0))

    # Add 2 Executive Takeaway Cards below chart
    card_y = Inches(5.62)
    card_h = Inches(1.52)
    card_w = Inches(5.95)

    # Card 1 (Left): Pertumbuhan Intake & Dominasi SNBT
    c1 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), card_y, card_w, card_h)
    c1.fill.solid()
    c1.fill.fore_color.rgb = RGBColor(236, 253, 245) # Soft Green
    c1.line.color.rgb = RGBColor(16, 185, 129)
    c1.line.width = Pt(1.2)
    tf1 = c1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = Inches(0.2)
    tf1.margin_right = Inches(0.2)
    tf1.margin_top = Inches(0.12)
    tf1.margin_bottom = Inches(0.1)

    p1 = tf1.paragraphs[0]
    p1.text = "• Total mahasiswa baru yang mendaftar ulang terus meningkat, dari 6.197 (2022) menjadi 8.361 (2026) mahasiswa atau bertumbuh +34,9%."
    p1.font.name = FONT_NAME
    p1.font.size = Pt(10.5)
    p1.font.color.rgb = RGBColor(15, 23, 42)

    p2 = tf1.add_paragraph()
    p2.text = "• SNBT menjadi jalur masuk paling dominan selama 5 tahun, menyerap 3.260 mahasiswa pada 2026 (~39,0% total intake)."
    p2.font.name = FONT_NAME
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = RGBColor(15, 23, 42)

    # Card 2 (Right): Dinamika Kebocoran & Realisasi Jalur Talenta
    c2 = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.78), card_y, card_w, card_h)
    c2.fill.solid()
    c2.fill.fore_color.rgb = RGBColor(241, 245, 249) # Soft Slate
    c2.line.color.rgb = RGBColor(148, 163, 184)
    c2.line.width = Pt(1.2)
    tf2 = c2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = Inches(0.2)
    tf2.margin_right = Inches(0.2)
    tf2.margin_top = Inches(0.12)
    tf2.margin_bottom = Inches(0.1)

    p3 = tf2.paragraphs[0]
    p3.text = "• Jalur SNBT (626 mhs) dan SMMPTN (604 mhs) menyumbang angka gugur terbesar pada 2026 akibat dinamika persaingan antar-kampus nasional."
    p3.font.name = FONT_NAME
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = RGBColor(15, 23, 42)

    p4 = tf2.add_paragraph()
    p4.text = "• Jalur Talenta 2026 mencatat konversi sehat: dari 461 peserta lulus seleksi, 308 mahasiswa mendaftar ulang (Yield Rate 66,8% | 153 gugur)."
    p4.font.name = FONT_NAME
    p4.font.size = Pt(10.5)
    p4.font.color.rgb = RGBColor(15, 23, 42)

    add_notes(s4, """Ketika kita bedah per jalur masuk, kita menemukan peta riil dinamika serapan dan kebocoran. Di panel kiri, intake riil kita tumbuh impresif +34,9% dari 6.197 menjadi 8.361 mahasiswa. Jalur SNBT dan SNBP konsisten menjadi tulang punggung penerimaan USK dengan kontribusi di atas 70%.

Di panel kanan, kita melihat dinamika kebocoran kelulusan. Pada tahun 2026, total calon mahasiswa yang mundur terkendali di angka 1.617 orang, dengan kebocoran terbesar berasal dari SNBT (626 orang) dan SMMPTN (604 orang) akibat persaingan pilihan kampus lain.

Khusus untuk Jalur Talenta 2026, data menunjukkan konversi yang sehat: dari 461 peserta yang dinyatakan lulus seleksi, 308 mahasiswa resmi mendaftar ulang (yield rate 66,8%), sementara 153 peserta mengundurkan diri.

Setelah melihat gambaran makro universitas, pertanyaan pimpinan berikutnya: apakah masalah keterisian ini merata di semua fakultas? Jawabannya ada di Slide 5.""")

    # =========================================================================
    # SLIDE 5: KETERISIAN FAKULTAS
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    s5_img = os.path.join(pdf_slides_dir, "slide_04.png")
    if os.path.exists(s5_img):
        s5.shapes.add_picture(s5_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s5, """Grafik ini menunjukkan ketimpangan yang sangat nyata di antara 12 fakultas kita. Fakultas Kedokteran Gigi, Kedokteran, Hukum, dan FEB beroperasi sangat sehat di atas 90% hingga 100%.

Namun di sisi bawah, perhatikan Fakultas Pertanian dan khususnya Fakultas Kelautan dan Perikanan (FPK). Selama 5 tahun berturut-turut, keterisian FPK tidak pernah mampu menembus 65%, dengan rata-rata 5 tahun hanya 59,7%. Ada kesenjangan struktural yang membutuhkan perlakuan khusus antar-fakultas.

Mengapa kesenjangan ini terjadi? Kita lihat perbandingan minat pelamar di level program studi pada Slide 6.""")

    # =========================================================================
    # SLIDE 6: KEKETATAN PRODI (TOP 8 VS BOTTOM 8)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    s6_img = os.path.join(pdf_slides_dir, "slide_05.png")
    if os.path.exists(s6_img):
        s6.shapes.add_picture(s6_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s6, """Di Slide ini kita melihat disparitas yang mencengangkan. Di sisi kiri, Farmasi, Informatika, dan Bisnis Digital sangat diminati hingga 39 orang memperebutkan 1 kursi.

Namun lihat sisi kanan: Budidaya Perairan mencatatkan rasio 0,91:1. Peminatnya hanya 145 orang, tetapi kuota yang dibuka mencapai 160 bangku. Bahkan jika panitia meluluskan seluruh pendaftar tanpa seleksi pun, kelas tetap tidak akan pernah penuh. Ini adalah alarm nyata adanya over-ekspansi kuota.

Mari kita lihat bukti riil over-ekspansi kuota ini pada beberapa program studi di Slide 7.""")

    # =========================================================================
    # SLIDE 7: KASUS EMPIRIS OVER-EKSPANSI KUOTA
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    s7_img = os.path.join(pdf_slides_dir, "slide_06.png")
    if os.path.exists(s7_img):
        s7.shapes.add_picture(s7_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s7, """Slide 7 ini adalah bukti paling nyata. Perhatikan 4 program studi dari 4 fakultas berbeda. Polanya persis sama: sejak USK menjadi PTN-BH di tahun 2024, garis biru kuota dinaikkan tinggi-tinggi ke angka 160 hingga 180 kursi.

Namun perhatikan garis hijau realisasi daftar ulang: garisnya mendatar dan tidak bergeming. Area merah muda di antara kedua garis ini adalah 'kursi hantu'—kapasitas ruang kuliah dan beban dosen yang disiapkan, tetapi tidak pernah terisi oleh mahasiswa.

Untuk memetakan seluruh 66 program studi S1 secara komprehensif, mari kita gunakan Matriks 4 Kuadran di Slide 8.""")

    # =========================================================================
    # SLIDE 8: MATRIKS 4 KUADRAN 5 TAHUN (GRAFIK 13 REVISI BERSIH)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_standard_header(s8, "Pemetaan 66 Program Studi S1 Berdasarkan Peminat & Kuota")
    g13_img = os.path.join(grafik_dir, "13_matriks_4_kuadran_5_tahun_2022_2026.png")
    if os.path.exists(g13_img):
        # 16:11 aspect ratio -> width=8.0 in, left=(13.333-8.0)/2 = 2.66 in
        s8.shapes.add_picture(g13_img, Inches(2.66), Inches(1.72), width=Inches(8.0), height=Inches(5.45))
    add_notes(s8, """Bapak Rektor dan Bapak Dekan, ini adalah peta kompas strategis universitas kita selama 5 tahun. Dari 66 prodi S1 Kampus Utama, kita punya 28 prodi bintang di Kuadran I yang menjadi tulang punggung reputasi dan penerimaan USK.

Namun yang menjadi pekerjaan rumah besar kita adalah 26 prodi di Kuadran III (hampir 40% portofolio kampus!). Prodi-prodi ini mengalami tantangan ganda: peminatnya di bawah rata-rata, dan keterisian kuotanya konsisten di bawah 80%.

Pertanyaannya: apakah posisi 66 prodi ini statis dari tahun ke tahun? Mari kita lihat pergerakannya di Slide 9.""")

    # =========================================================================
    # SLIDE 9: DINAMIKA MIGRASI KUADRAN (CHART A4)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_standard_header(s9, "Dinamika Migrasi Kuadran Program Studi (2022 vs 2026)")
    a4_img = os.path.join(grafik_dir, "A4_slope_migrasi_kuadran_2022_2026.png")
    if os.path.exists(a4_img):
        s9.shapes.add_picture(a4_img, Inches(1.16), Inches(1.72), width=Inches(11.0), height=Inches(5.45))
    add_notes(s9, """Kabar baiknya di Slide 9: posisi prodi tidak permanen. Sebanyak 14 prodi berhasil naik kelas (upgrade), di mana Agribisnis, Teknik Komputer, dan Proteksi Tanaman kini telah menjadi prodi unggulan berdaya saing tinggi.

Namun perhatian serius Dekan Fakultas Teknik dan FKIP wajib tertuju pada kotak merah: 8 prodi kita mengalami kemerosotan. Yang paling mengkhawatirkan adalah prodi keteknikan mapan—Teknik Mesin, Industri, dan Elektro—yang di tahun 2022 aman, tetapi pada 2026 tergelincir ke zona krisis karena peminatnya menyusut.

Seberapa konsisten masalah keterisian ini berlangsung? Kita lihat rekam jejaknya di Slide 10.""")

    # =========================================================================
    # SLIDE 10: HEATMAP KONSISTENSI FILL RATE 66 PRODI (CHART A2)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_standard_header(s10, "Konsistensi Keterisian Kuota 66 Program Studi (2022–2026)")
    a2_img = os.path.join(grafik_dir, "A2_heatmap_fill_rate_prodi_tahun.png")
    if os.path.exists(a2_img):
        s10.shapes.add_picture(a2_img, Inches(1.16), Inches(1.72), width=Inches(11.0), height=Inches(5.45))
    add_notes(s10, """Heatmap ini menyajikan rekam medis seluruh 66 prodi S1 tanpa ada yang terlewat. Di panel kanan, prodi unggulan kita selalu hijau dan penuh.

Namun di panel kiri atas, ada 5 prodi yang selama setengah dekade berwarna merah pekat dengan keterisian di bawah 50%. Ini membuktikan bahwa masalah ini bukan fluktuasi sesaat, melainkan masalah kurikulum dan relevansi pasar yang sudah kronis.

Lalu, berapa sebenarnya total kursi yang hilang akibat prodi-prodi krisis ini? Mari kita lihat analisis Pareto di Slide 11.""")

    # =========================================================================
    # SLIDE 11: PARETO 80/20 KURSI KOSONG (CHART A3)
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_standard_header(s11, "Episentrum Kursi Kosong: Analisis Pareto 80/20")
    a3_img = os.path.join(grafik_dir, "A3_pareto_kursi_kosong.png")
    if os.path.exists(a3_img):
        s11.shapes.add_picture(a3_img, Inches(1.16), Inches(1.72), width=Inches(11.0), height=Inches(5.45))
    add_notes(s11, """Bapak Rektor dan Pimpinan RKAT, ini adalah temuan paling actionable dalam presentasi kami. Dari 8.944 bangku kuliah yang terbuang sia-sia selama 5 tahun, hampir tiga perempatnya (74,5%) terkonsentrasi HANYA di empat fakultas: FKIP, Teknik, Pertanian, dan FPK.

Artinya, manajemen universitas tidak perlu menyebar energi dan anggaran ke 66 prodi. Cukup fokuskan restrukturisasi daya tampung dan subsidi beasiswa pada 4 fakultas ini, maka 75% masalah inefisiensi kampus langsung terselesaikan.

Banyak yang menduga kursi kosong ini terjadi karena mahasiswa yang lulus seleksi batal daftar ulang. Apakah benar demikian? Mari kita uji hipotesis ini di Slide 12.""")

    # =========================================================================
    # SLIDE 12: MEMATAHKAN MITOS - KORELASI (CHART A5)
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_standard_header(s12, "Uji Korelasi: Keterisian Kuota vs Angka Mahasiswa Mundur")
    a5_img = os.path.join(grafik_dir, "A5_scatter_kebocoran_vs_fill_rate.png")
    if os.path.exists(a5_img):
        # 18:11 aspect ratio -> width=8.9 in, left=(13.333-8.9)/2 = 2.21 in
        s12.shapes.add_picture(a5_img, Inches(2.21), Inches(1.72), width=Inches(8.9), height=Inches(5.45))
    add_notes(s12, """Slide 12 ini mematahkan mitos terbesar yang selama ini sering diperdebatkan. Seringkali muncul asumsi bahwa kursi kosong terjadi karena calon mahasiswa lari atau batal daftar ulang.

Data ekonometrika membuktikan korelasinya adalah minus 0,067—artinya nol korelasi! Dokter Gigi dan Farmasi tingkat mundurnya sangat tinggi (di atas 25%), tapi kelasnya tetap 100% penuh karena peminatnya melimpah.

Sebaliknya, prodi di Fakultas Pertanian dan Perikanan sepi bukan karena mahasiswanya kabur, tapi karena sejak awal pendaftar yang lulus memang tidak mencukupi kuota. Jadi solusinya bukan sekadar menahan mahasiswa agar tidak mundur, melainkan merampingkan kuota sejak tahap penetapan daya tampung.

Selain ukuran kuota, apa saja faktor lingkungan yang mempengaruhi preferensi calon mahasiswa? Kita lihat di Slide 13.""")

    # =========================================================================
    # SLIDE 13: KIP KULIAH & PROSPEK KERJA TEKNOLOGI
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    s13_img = os.path.join(pdf_slides_dir, "slide_10.png")
    if os.path.exists(s13_img):
        s13.shapes.add_picture(s13_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s13, """Dua faktor penjelas tambahan ada di Slide 13. Pertama, faktor daya beli: prodi-prodi di Kuadran III sangat bergantung pada KIP-Kuliah (mencapai 50% populasi kelas). Ketika kuota KIP nasional dipangkas, pendaftar di prodi-prodi ini langsung terpukul.

Kedua, pergeseran tren kerja: siswa SMA hari ini sangat melek digital. Mereka berbondong-bondong memilih Informatika, Bisnis Digital, dan Manajemen karena fleksibilitas karirnya. Prodi sains murni dan keguruan yang tidak memperbarui kurikulumnya ke arah digital mulai ditinggalkan peminat.

Berdasarkan seluruh diagnosis data tadi, apa langkah konkret yang harus diambil pimpinan USK di RKAT mendatang? Mari kita masuk ke Babak Solusi di Slide 14.""")

    # =========================================================================
    # SLIDE 14: MATRIKS STRATEGI RKAT 4 KUADRAN (NATIVE TABLE)
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_standard_header(s14, "Matriks Strategi Daya Tampung Berdasarkan 4 Kuadran")

    # Tambahkan Tabel 4 Kuadran
    rows = 5
    cols = 4
    left = Inches(0.6)
    top = Inches(1.72)
    width = Inches(12.133)
    height = Inches(5.35)

    tbl_shape = s14.shapes.add_table(rows, cols, left, top, width, height)
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.6)
    tbl.columns[1].width = Inches(3.1)
    tbl.columns[2].width = Inches(3.2)
    tbl.columns[3].width = Inches(3.233)

    headers_14 = [
        "KLASIFIKASI PORTOFOLIO",
        "KEBIJAKAN DAYA TAMPUNG (KUOTA)",
        "MITIGASI REGISTRASI & JALUR MASUK",
        "RESTRUKTURISASI KURIKULUM & BRANDING"
    ]

    for j, h in enumerate(headers_14):
        cell = tbl.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = c_forest
        p = cell.text_frame.paragraphs[0]
        p.font.name = FONT_NAME
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_white
        p.alignment = PP_ALIGN.CENTER
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE

    matrix_data = [
        ("KUADRAN I: UNGGULAN PRIMA\n(28 Prodi / 42.4%)\nContoh: Kedokteran, Hukum, FEB, Informatika, Psikologi",
         "• PERTAHANKAN KUOTA (Kapasitas Maksimal).\n• Jangan diekspansi berlebihan agar rasio dosen tetap unggul dan mutu terjaga.",
         "• Terapkan SISTEM CADANGAN (Waiting List) 10–15% pada SNBP & SNBT.\n• Mencegah kursi mahal hangus akibat peserta lolos PTN lain.",
         "• Akselerasi akreditasi internasional (ASIIN, ABEST21).\n• Perluas kemitraan magang industri terkemuka & double-degree."),

        ("KUADRAN II: STABIL / NICHE\n(4 Prodi / 6.1%)\nContoh: Penjaskesrek, Seni Sendratasik, Ilmu Politik, HI",
         "• KUOTA MODERAT & TERKENDALI.\n• Pertahankan daya serap tanpa ekspansi agresif.",
         "• Perkuat jalur seleksi berbasis portofolio bakat & minat khusus.\n• Kunci komitmen awal mahasiswa di tahap seleksi.",
         "• Branding sebagai 'Pusat Keunggulan Seni & Olahraga Regional'.\n• Pertahankan kekhasan kurikulum yang tidak dimiliki kampus lain."),

        ("KUADRAN III: KURANG DIMINATI\n(26 Prodi / 39.4%)\nContoh: Agro, Kelautan, Sains Dasar, Beberapa Keguruan",
         "• MORATORIUM PENAMBAHAN KUOTA.\n• Kunci batas kuota di angka realisasi riil tahun sebelumnya.",
         "• Alokasikan prioritas kuota KIP-Kuliah sebagai jaring pengaman sosial.\n• Galang beasiswa ikatan dinas dari Pemda daerah 3T.",
         "• RESTRUKTURISASI KURIKULUM: Wajibkan peminatan terapan (misal: Agrotech, Sains Data Lingkungan).\n• Re-branding nama peminatan."),

        ("KUADRAN IV: KRISIS & DEGRADASI\n(8 Prodi / 12.1%)\nContoh: Geofisika, Fisika, Mesin, Elektro, Industri, THP",
         "• PANGKAS KUOTA 30%–40% SECARA REALISTIS di RKAT 2027.\n• Selamatkan rasio akreditasi LAM dan efisiensi ruang kuliah.",
         "• Perketat komitmen uang jaminan/UKT awal pada jalur mandiri.\n• Hilangkan jalur penerimaan yang terbukti mengalami kebocoran 100%.",
         "• AUDIT KURIKULUM TOTAL: Sesuaikan dengan industri otomasi & digital.\n• Opsi penggabungan (merger) peminatan serumpun jika tidak pulih 2 thn.")
    ]

    for i, row in enumerate(matrix_data):
        bg_col = RGBColor(241, 245, 249) if i % 2 == 1 else c_white
        if i == 3: # Kuadran IV highlight merah muda
            bg_col = RGBColor(254, 242, 242)
        elif i == 0: # Kuadran I hijau muda
            bg_col = RGBColor(240, 253, 244)

        for j, text in enumerate(row):
            cell = tbl.cell(i + 1, j)
            cell.text = text
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            for p in cell.text_frame.paragraphs:
                p.font.name = FONT_NAME
                p.font.size = Pt(10)
                p.font.color.rgb = c_slate
                if j == 0:
                    p.font.bold = True
                    if i == 3:
                        p.font.color.rgb = RGBColor(185, 28, 28)
                    elif i == 0:
                        p.font.color.rgb = RGBColor(4, 120, 87)

    add_notes(s14, """Bapak Rektor dan para Dekan, ini adalah resep obat berbasis data untuk draft RKAT 2027. Kita membagi perlakuan menjadi 4 kebijakan terarah:

Untuk Kuadran I: Jangan tambah kuota fisik, tapi terapkan over-booking 10-15% agar kursi mahal tidak hangus saat peserta lulus diterima di kampus lain.

Untuk Kuadran III: Jangan tambah kuota lagi. Pasang kuota KIP-K sebagai jaring pengaman sosial, dan modernisasi kurikulum mereka.

Dan yang paling berani, untuk Kuadran IV: Pangkas kuota 30% hingga 40% di RKAT 2027. Memangkas kuota di prodi sepi bukan tanda kegagalan, melainkan langkah penyelamatan efisiensi kelas, penyelamatan rasio akreditasi LAM, dan penghentian pemborosan anggaran operasional.

Sebagai penutup, inilah 4 pilar rekomendasi utama yang kami serahkan kepada pimpinan universitas di Slide 15.""")

    # =========================================================================
    # SLIDE 15: 4 PILAR REKOMENDASI STRATEGIS & CLOSING
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_standard_header(s15, "4 Pilar Rekomendasi Kebijakan RKAT 2027")

    pillars = [
        ("PILAR 1", "Rasionalisasi Kuota Berbasis Data",
         "Pangkas kuota 30%–40% di 4 fakultas surplus (FKIP, FT, FP, FPK) dan alihkan kapasitas ke prodi defisit kuota (FEB, Hukum, Keperawatan, Kedokteran). Hentikan ekspansi kuota tanpa dasar pasar riil.",
         RGBColor(239, 68, 68), RGBColor(254, 242, 242)),
        ("PILAR 2", "Sistem Cadangan Over-Booking",
         "Terapkan kuota cadangan dinamis (Waiting List) 10%–15% pada jalur mandiri dan seleksi prodi Kuadran I, guna memitigasi risiko gugur daftar ulang (6.651 calon mhs mundur) agar kursi tidak hangus.",
         RGBColor(217, 119, 6), RGBColor(255, 251, 235)),
        ("PILAR 3", "Subsidi Terarah KIP-Kuliah",
         "Fokuskan alokasi KIP-Kuliah dan beasiswa Pemda ke prodi agro-maritim dan keguruan sains (Kuadran III) sebagai jaring pengaman sosial daya beli untuk mengamankan 50% populasi kelas.",
         RGBColor(59, 130, 246), RGBColor(239, 246, 255)),
        ("PILAR 4", "Revitalisasi Kurikulum & AI",
         "Modernisasi kurikulum rumpun keteknikan dan sains murni dengan konsentrasi terapan industri (AI, Robotika, Bioinformatika, Renewable Energy) agar relevan dengan tren pilihan karir Gen Z.",
         RGBColor(16, 185, 129), RGBColor(236, 253, 245))
    ]

    card_w = Inches(2.85)
    card_h = Inches(3.6)
    card_y = Inches(1.72)

    for idx, (p_num, p_title, p_desc, border_c, bg_c) in enumerate(pillars):
        card_x = Inches(0.6 + idx * 3.09)
        rect = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, card_x, card_y, card_w, card_h)
        rect.fill.solid()
        rect.fill.fore_color.rgb = bg_c
        rect.line.color.rgb = border_c
        rect.line.width = Pt(1.5)

        tb = s15.shapes.add_textbox(card_x + Inches(0.18), card_y + Inches(0.18), card_w - Inches(0.36), card_h - Inches(0.36))
        tf = tb.text_frame
        tf.word_wrap = True

        p1 = tf.paragraphs[0]
        p1.text = p_num
        p1.font.name = FONT_NAME
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = border_c

        p2 = tf.add_paragraph()
        p2.text = p_title
        p2.font.name = FONT_NAME
        p2.font.size = Pt(14)
        p2.font.bold = True
        p2.font.color.rgb = c_slate
        p2.space_before = Pt(6)
        p2.space_after = Pt(10)

        p3 = tf.add_paragraph()
        p3.text = p_desc
        p3.font.name = FONT_NAME
        p3.font.size = Pt(10.5)
        p3.font.color.rgb = c_sub_slate

    # Executive Closing Box
    cta_box = s15.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.50), Inches(12.133), Inches(1.5))
    cta_box.fill.solid()
    cta_box.fill.fore_color.rgb = c_forest
    cta_box.line.color.rgb = c_gold
    cta_box.line.width = Pt(2)

    tb_cta = s15.shapes.add_textbox(Inches(0.8), Inches(5.60), Inches(11.733), Inches(1.3))
    tf_cta = tb_cta.text_frame
    tf_cta.word_wrap = True

    p_cta1 = tf_cta.paragraphs[0]
    p_cta1.text = "EXECUTIVE TAKEAWAY BAGI PIMPINAN UNIVERSITAS SYIAH KUALA:"
    p_cta1.font.name = FONT_NAME
    p_cta1.font.size = Pt(12)
    p_cta1.font.bold = True
    p_cta1.font.color.rgb = c_gold

    p_cta2 = tf_cta.add_paragraph()
    p_cta2.text = "\"Optimalisasi daya tampung USK pasca-status PTN-BH bukanlah tentang membuka kuota kursi sebanyak-banyaknya, melainkan menaruh kapasitas di tempat yang tepat secara presisi berbasis permintaan pasar riil.\""
    p_cta2.font.name = FONT_NAME
    p_cta2.font.size = Pt(14)
    p_cta2.font.bold = True
    p_cta2.font.italic = True
    p_cta2.font.color.rgb = c_white
    p_cta2.space_before = Pt(4)

    add_notes(s15, """Sebagai kesimpulan, kami merangkum 4 pilar aksi untuk pimpinan universitas:
1. Rasionalisasi kuota: Sesuaikan daya tampung dengan permintaan pasar riil.
2. Terapkan over-booking: Cegah hilangnya 7.200 calon mahasiswa dengan sistem cadangan.
3. Alokasikan beasiswa KIP-K secara terarah pada prodi yang membutuhkan.
4. Revitalisasi kurikulum agar prodi keteknikan dan sains kembali relevan di era industri 4.0.

Dengan 4 langkah ini, insya Allah USK akan mengeliminasi 2.000 kursi kosong per tahun, meningkatkan pendapatan riil BLU/PTN-BH, dan memastikan seluruh ruang kuliah terisi oleh mahasiswa-mahasiswa terbaik bangsa.

Terima kasih. Kami membuka ruang untuk diskusi dan masukan dari Bapak Rektor dan para Dekan. Wassalamu’alaikum Warahmatullahi Wabarakatuh.""")

    # =========================================================================
    # SLIDE 16: PENUTUP (TERIMA KASIH)
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    s16_img = os.path.join(pdf_slides_dir, "slide_14.png")
    if os.path.exists(s16_img):
        s16.shapes.add_picture(s16_img, 0, 0, width=Inches(13.333), height=Inches(7.5))
    add_notes(s16, "Sesi Tanya Jawab (Q&A) dibuka. Siapkan slide lampiran (Slide 17-20) jika ada pertanyaan spesifik.")

    # =========================================================================
    # SLIDE 17-20: APPENDIX / LAMPIRAN Q&A DEFENSE
    # =========================================================================
    appendix_slides = [
        ("Evaluasi Multi-Tahun Program D3 Vokasi",
         os.path.join(grafik_dir, "08_evaluasi_multi_tahun_d3_vokasi.png"),
         "Slide pendukung jika ada Dekan/Direktur menanyakan kinerja program diploma 3."),

        ("Sub-Analisis Program PSDKU Gayo Lues",
         os.path.join(grafik_dir, "09_subanalisis_psdku_gayo_lues.png"),
         "Slide pendukung jika ada pertanyaan tentang keterisian kampus PSDKU Gayo Lues."),

        ("Top Program Studi Pertumbuhan Peminat Tertinggi",
         os.path.join(grafik_dir, "02_top_tren_peningkatan_pendaftar_dan_peminat.png"),
         "Slide pendukung jika pimpinan bertanya prodi mana saja yang tumbuh eksplosif."),

        ("Analisis Desil Ekonomi & Penolakan KIP-Kuliah SNBT",
         os.path.join(grafik_dir, "20_analisis_desil_dan_rejection_kip_snbt.png"),
         "Slide pendukung jika ditanyakan mengenai korelasi desil ekonomi pendaftar.")
    ]

    for title, img_path, note_text in appendix_slides:
        s_app = prs.slides.add_slide(blank_layout)
        add_standard_header(s_app, title)
        if os.path.exists(img_path):
            s_app.shapes.add_picture(img_path, Inches(1.16), Inches(1.72), width=Inches(11.0), height=Inches(5.45))
        add_notes(s_app, note_text)

    # Simpan File
    prs.save(output_pptx)
    print(f"\n[SUKSES REVISI] File presentasi berhasil disimpan di:\n{output_pptx}")
    print(f"Total Slide: {len(prs.slides)} Slide (16 Slide Utama + 4 Slide Lampiran)")
    print("Seluruh slide kini 100% konsisten dengan logo USK, Maganghub, dots grid, aksen kuning, dan font Cerebri Sans!")

if __name__ == '__main__':
    create_deck()
