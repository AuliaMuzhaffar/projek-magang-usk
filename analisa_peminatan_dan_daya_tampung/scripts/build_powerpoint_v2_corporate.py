#!/usr/bin/env python3
"""
Build PowerPoint V2 Corporate Edition
======================================
Generates a 24-slide corporate-style presentation for USK PMB analysis.
Output: presentasi_v2_corporate.pptx (does NOT overwrite existing files)

Design: Navy-Gold corporate palette with frosted glass cards, section dividers,
        gold separator lines, and persistent footer bar.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# =============================================================================
# DESIGN SYSTEM — COLOR PALETTE & CONSTANTS
# =============================================================================
# Primary
NAVY        = RGBColor(13, 31, 60)     # #0D1F3C
ROYAL_BLUE  = RGBColor(27, 59, 111)    # #1B3B6F
GOLD        = RGBColor(201, 168, 76)   # #C9A84C
TEAL        = RGBColor(16, 149, 193)   # #1095C1
WARM_WHITE  = RGBColor(245, 240, 232)  # #F5F0E8

# Accent
ALERT_RED   = RGBColor(192, 57, 43)    # #C0392B
DEEP_RED    = RGBColor(185, 28, 28)    # #B91C1C
SUCCESS_GRN = RGBColor(22, 101, 52)    # #166534
ORANGE_ACC  = RGBColor(230, 81, 0)     # #E65100

# Neutral
LIGHT_GRAY  = RGBColor(232, 224, 212)  # #E8E0D4
SLATE_700   = RGBColor(55, 65, 81)     # #374151
SLATE_500   = RGBColor(100, 116, 139)  # #64748B
WHITE       = RGBColor(255, 255, 255)
CARD_BG     = RGBColor(255, 255, 255)
CARD_BORDER = RGBColor(226, 232, 240)

# Slide dimensions (16:9 widescreen)
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)

# Footer height
FOOTER_H = Inches(0.35)
FOOTER_Y = SLIDE_H - FOOTER_H

# Content area
CONTENT_TOP = Inches(1.65)
MARGIN_L = Inches(0.8)
MARGIN_R = Inches(0.8)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def set_shape_flat(shape, fill_color, line_color=None, line_width=1):
    """Apply flat fill and optional border to a shape."""
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(line_width)
    else:
        shape.line.fill.background()


def add_bg(slide, color=NAVY):
    """Add full-slide background rectangle."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    set_shape_flat(bg, color)
    return bg


def add_footer(slide, slide_num, total=24):
    """Add persistent navy footer bar with branding and slide number."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, FOOTER_Y, SLIDE_W, FOOTER_H)
    set_shape_flat(bar, NAVY)

    # Left text: branding
    tb_l = slide.shapes.add_textbox(Inches(0.8), FOOTER_Y + Pt(4), Inches(8), FOOTER_H - Pt(8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = False
    p = tf_l.paragraphs[0]
    p.text = "UNIVERSITAS SYIAH KUALA  |  RAPAT PIMPINAN PMB  |  ANALISA PEMINATAN & DAYA TAMPUNG 2022–2026"
    p.font.size = Pt(8)
    p.font.color.rgb = GOLD
    p.font.bold = True
    p.alignment = PP_ALIGN.LEFT

    # Right text: slide number
    tb_r = slide.shapes.add_textbox(Inches(11.5), FOOTER_Y + Pt(4), Inches(1.5), FOOTER_H - Pt(8))
    tf_r = tb_r.text_frame
    p_r = tf_r.paragraphs[0]
    p_r.text = f"{slide_num} / {total}"
    p_r.font.size = Pt(8)
    p_r.font.color.rgb = WARM_WHITE
    p_r.font.bold = True
    p_r.alignment = PP_ALIGN.RIGHT


def add_gold_line(slide, y, left=None, width=None):
    """Add a thin gold horizontal separator line."""
    left = left or MARGIN_L
    width = width or (SLIDE_W - MARGIN_L - MARGIN_R)
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, y, width, Pt(1.5))
    set_shape_flat(line, GOLD)
    return line


def create_header_v2(slide, title_text, subtitle_text=None):
    """Create a corporate header with category tag, title, and gold separator."""
    # Category tag
    tb_cat = slide.shapes.add_textbox(MARGIN_L, Inches(0.3), Inches(11.7), Inches(0.3))
    tf_cat = tb_cat.text_frame
    tf_cat.word_wrap = False
    p_cat = tf_cat.paragraphs[0]
    p_cat.text = "UNIVERSITAS SYIAH KUALA  |  RAPAT PIMPINAN PMB"
    p_cat.font.size = Pt(9)
    p_cat.font.bold = True
    p_cat.font.color.rgb = GOLD

    # Title
    tb_title = slide.shapes.add_textbox(MARGIN_L, Inches(0.55), Inches(11.7), Inches(0.8))
    tf_title = tb_title.text_frame
    tf_title.word_wrap = True
    p_title = tf_title.paragraphs[0]
    p_title.text = title_text
    p_title.font.size = Pt(20)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

    if subtitle_text:
        p_sub = tf_title.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(11)
        p_sub.font.color.rgb = SLATE_500
        p_sub.space_before = Pt(2)

    # Gold separator line
    add_gold_line(slide, Inches(1.45))


def add_card_v2(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER,
                border_width=1, opacity_fill=True):
    """Add a premium card shape with rounded corners."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_shape_flat(card, bg_color, border_color, line_width=border_width)
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.18)
    tf.margin_top = tf.margin_bottom = Inches(0.15)
    return card, tf


def add_bullet_v2(tf, bold_prefix, text_content, font_size=11, space_after=6,
                  bold_color=ROYAL_BLUE, norm_color=SLATE_700, indent=0):
    """Add a formatted bullet point with bold prefix and normal text."""
    p = tf.add_paragraph()
    p.font.size = Pt(font_size)
    p.space_after = Pt(space_after)
    p.level = indent

    if bold_prefix:
        r_bold = p.add_run()
        r_bold.text = bold_prefix + " "
        r_bold.font.bold = True
        r_bold.font.size = Pt(font_size)
        r_bold.font.color.rgb = bold_color

    r_norm = p.add_run()
    r_norm.text = text_content
    r_norm.font.size = Pt(font_size)
    r_norm.font.color.rgb = norm_color
    return p


def add_card_title(tf, title_text, color=ROYAL_BLUE, font_size=13):
    """Set the first paragraph of a card's text frame as a styled title."""
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.bold = True
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.space_after = Pt(8)
    return p


def add_banner_callout(slide, left, top, width, height, title, subtitle=None,
                       bg_color=RGBColor(248, 250, 252), border_color=RGBColor(203, 213, 225),
                       title_color=ROYAL_BLUE, title_size=10, sub_size=8.8):
    """Add a sleek, high-impact horizontal callout banner under a chart."""
    card, tf = add_card_v2(slide, left, top, width, height, bg_color=bg_color, border_color=border_color)
    p_t = tf.paragraphs[0]
    p_t.text = title
    p_t.font.bold = True
    p_t.font.size = Pt(title_size)
    p_t.font.color.rgb = title_color
    p_t.space_after = Pt(3)
    if subtitle:
        p_s = tf.add_paragraph()
        p_s.text = subtitle
        p_s.font.size = Pt(sub_size)
        p_s.font.color.rgb = SLATE_700
    return card, tf


def add_section_divider(prs, blank_layout, section_num, section_title, slide_num, total=24):
    """Create a section divider slide with large number and gold rule."""
    s = prs.slides.add_slide(blank_layout)
    add_bg(s, NAVY)

    # Large number
    tb_num = s.shapes.add_textbox(Inches(4.5), Inches(1.8), Inches(4.3), Inches(2.0))
    tf_num = tb_num.text_frame
    p_num = tf_num.paragraphs[0]
    p_num.text = f"{section_num:02d}"
    p_num.font.size = Pt(96)
    p_num.font.bold = True
    p_num.font.color.rgb = GOLD
    p_num.alignment = PP_ALIGN.CENTER

    # Gold line
    add_gold_line(s, Inches(3.95), left=Inches(4.5), width=Inches(4.3))

    # Section title
    tb_title = s.shapes.add_textbox(Inches(2.5), Inches(4.2), Inches(8.3), Inches(1.0))
    tf_title = tb_title.text_frame
    p_title = tf_title.paragraphs[0]
    p_title.text = section_title.upper()
    p_title.font.size = Pt(22)
    p_title.font.bold = True
    p_title.font.color.rgb = WARM_WHITE
    p_title.alignment = PP_ALIGN.CENTER

    add_footer(s, slide_num, total)
    return s


def add_img(slide, chart_dir, filename, left, top, width=None, height=None):
    """Add an image if it exists, with optional width/height."""
    path = os.path.join(chart_dir, filename)
    if os.path.exists(path):
        kwargs = {}
        if width:
            kwargs['width'] = width
        if height:
            kwargs['height'] = height
        slide.shapes.add_picture(path, left, top, **kwargs)
        return True
    else:
        print(f"  [WARN] Image not found: {filename}")
        return False


# =============================================================================
# MAIN BUILDER
# =============================================================================

def main():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    prs_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung")
    chart_dir = os.path.join(prs_dir, "grafik")
    out_pptx = os.path.join(prs_dir, "presentasi_v2_corporate.pptx")

    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    blank = prs.slide_layouts[6]  # blank layout

    TOTAL = 24
    sn = 0  # slide number counter

    # =================================================================
    # SLIDE 1: COVER / TITLE SLIDE
    # =================================================================
    sn += 1
    s1 = prs.slides.add_slide(blank)
    add_bg(s1, NAVY)

    # Decorative accent corner (top-right)
    corner = s1.shapes.add_shape(MSO_SHAPE.RIGHT_TRIANGLE, Inches(10.5), 0, Inches(2.833), Inches(2.5))
    set_shape_flat(corner, RGBColor(20, 42, 80))  # slightly lighter navy

    # Left gold accent bar
    bar_l = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.15), SLIDE_H)
    set_shape_flat(bar_l, GOLD)

    # Title area
    tb = s1.shapes.add_textbox(Inches(1.2), Inches(1.0), Inches(10.5), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "TUGAS 05 — MAGANG (KHUSUS)  |  AUDIT-GRADE DECISION ANALYTICS"
    p0.font.size = Pt(11)
    p0.font.bold = True
    p0.font.color.rgb = GOLD
    p0.space_after = Pt(16)

    p1 = tf.add_paragraph()
    p1.text = "ANALISA PEMINATAN DAN\nDAYA TAMPUNG PROGRAM STUDI\nUNIVERSITAS SYIAH KUALA"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Evaluasi Tren Multi-Tahun (2022–2026), Rasio Keketatan Seleksi, Matriks Portofolio\nKuadran, Dekonstruksi Kebocoran Desil KIP-Kuliah, dan Rekomendasi Kebijakan PTN-BH"
    p2.font.size = Pt(13)
    p2.font.color.rgb = RGBColor(180, 190, 210)
    p2.space_after = Pt(8)

    # Gold separator
    add_gold_line(s1, Inches(4.6), left=Inches(1.2), width=Inches(6.0))

    # Metadata card
    _, meta_tf = add_card_v2(s1, Inches(1.2), Inches(5.0), Inches(10.5), Inches(1.8),
                              bg_color=RGBColor(20, 42, 80), border_color=RGBColor(60, 80, 120))
    add_card_title(meta_tf, "INFORMASI EKSEKUTIF PENUGASAN", GOLD, font_size=11)
    add_bullet_v2(meta_tf, "Target Peserta Rapat:", "Rektor, Para Wakil Rektor, Ketua Senat Akademik, dan Para Dekan Fakultas",
                  font_size=10, space_after=3, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))
    add_bullet_v2(meta_tf, "Dasar Dataset:", "Data Empiris PMB USK 2022–2026, Dataset Jalur Masuk & Kebocoran, Data Induk KIP-Kuliah 2025–2026",
                  font_size=10, space_after=3, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))
    add_bullet_v2(meta_tf, "Penyusun & Tujuan:", "Data Analyst PMB — Tim Magang USK | Pengambilan Keputusan Strategis Rasionalisasi Kuota & Efisiensi Finansial PTN-BH",
                  font_size=10, space_after=2, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))

    add_footer(s1, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Cover")

    # =================================================================
    # SLIDE 2: RINGKASAN EKSEKUTIF (3 PILAR)
    # =================================================================
    sn += 1
    s2 = prs.slides.add_slide(blank)
    create_header_v2(s2, "Ringkasan Eksekutif: Tiga Dimensi Evaluasi PMB USK Pasca Transformasi PTN-BH",
                     "Sintesis Temuan Kunci Permintaan Pasar, Kapasitas Kuota, dan Resolusi Kausalitas Kebocoran")

    col_w = Inches(3.64)
    card_y = CONTENT_TOP
    card_h = Inches(5.15)

    # Card 1: Permintaan Pasar
    _, tf1 = add_card_v2(s2, MARGIN_L, card_y, col_w, card_h,
                         bg_color=RGBColor(248, 250, 252), border_color=RGBColor(203, 213, 225))
    add_card_title(tf1, "1. PERMINTAAN PASAR (DEMAND)", ROYAL_BLUE, 12)
    add_bullet_v2(tf1, "Lonjakan Peminat:", "Total peminat USK naik +39,5% dalam 5 tahun dari 48.769 (2022) ke 68.010 (2026), rekor 70.945 di 2025.", font_size=9.5, space_after=4)
    add_bullet_v2(tf1, "Polarisasi Ekstrem:", "Farmasi capai rasio 39,2:1, sebaliknya Budidaya Perairan hanya 0,91:1 (defisit pendaftar di bawah kuota).", font_size=9.5, space_after=4)
    add_bullet_v2(tf1, "Pergeseran Minat Gen Z:", "Permintaan terkonsentrasi ke kesehatan, teknologi digital, dan prodi dengan kepastian formasi ASN/PPPK daerah.", font_size=9.5, space_after=4)
    add_bullet_v2(tf1, "Disparitas Klaster:", "Rumpun teknik & sains murni konvensional mengalami stagnasi minat yang persisten selama setengah dekade.", font_size=9.5, space_after=8)
    add_bullet_v2(tf1, "📌 IMPERATIF STRATEGIS:", "Re-alokasi kuota ke prodi berdaya serap tinggi; stop pemborosan kapasitas di sains dasar.",
                  font_size=9.5, space_after=2, bold_color=ROYAL_BLUE, norm_color=ROYAL_BLUE)

    # Card 2: Kapasitas & Efisiensi
    _, tf2 = add_card_v2(s2, Inches(4.84), card_y, col_w, card_h,
                         bg_color=RGBColor(255, 247, 237), border_color=RGBColor(254, 215, 170))
    add_card_title(tf2, "2. KAPASITAS & EFISIENSI (SUPPLY)", ORANGE_ACC, 12)
    add_bullet_v2(tf2, "Ekspansi Agresif PTN-BH:", "Daya tampung dinaikkan +32,7% (7.863 → 10.435 kursi), namun tidak diimbangi kenaikan daftar ulang proporsional.", font_size=9.5, space_after=4)
    add_bullet_v2(tf2, "Akumulasi 10.984 Kursi Kosong:", "Persisten ~2.000 bangku kosong/tahun (23,0% dari 47.738 total kuota 5 tahun berujung mubazir).", font_size=9.5, space_after=4)
    add_bullet_v2(tf2, "Krisis Segmen Vokasi & PSDKU:", "D3 Vokasi hanya terisi 51,3% (1.320 kursi terbuang), PSDKU Gayo Lues krisis ekstrem 18,6% (783 kursi terbuang).", font_size=9.5, space_after=4)
    add_bullet_v2(tf2, "Konsentrasi Episentrum:", "3 Fakultas (FKIP, FT, Pertanian) menyumbang 65,1% seluruh kursi kosong S1 kampus utama.", font_size=9.5, space_after=8)
    add_bullet_v2(tf2, "📌 IMPERATIF STRATEGIS:", "Rasionalisasi kuota 20–40% pada 22 prodi Kuadran III untuk menghapus 450 bangku kosong semu.",
                  font_size=9.5, space_after=2, bold_color=DEEP_RED, norm_color=DEEP_RED)

    # Card 3: Plot Twist KIP
    _, tf3 = add_card_v2(s2, Inches(8.88), card_y, col_w, card_h,
                         bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(tf3, "3. RESOLUSI \"PLOT TWIST\" KEBOCORAN", ALERT_RED, 12)
    add_bullet_v2(tf3, "Kausalitas 97,60% Terbukti:", "626 kursi kosong SNBT 2026 secara empiris hampir identik 1-to-1 dengan 611 calon KIP yang ditolak beasiswanya.", font_size=9.5, space_after=4)
    add_bullet_v2(tf3, "Cliff-Edge Desil 5 & 6:", "Pemangkasan kuota KIP (-11,2%) membantai Desil 5 & 6 (>98% ditolak). 526 calon mahasiswa berprestasi terhempas.", font_size=9.5, space_after=4)
    add_bullet_v2(tf3, "Economic Forced Drop-Out:", "Bukan siswa kabur ke PTS, melainkan shock biaya saat dialihkan ke UKT Kel. III–V (Rp2,5–5 jt/semester).", font_size=9.5, space_after=4)
    add_bullet_v2(tf3, "Beban Kuadran III:", "Prodi rentan menanggung beban sosial KIP tertinggi (31,1%), sehingga paling rapuh terhadap guncangan beasiswa.", font_size=9.5, space_after=8)
    add_bullet_v2(tf3, "📌 IMPERATIF STRATEGIS:", "SK Rektor UKT Penyelamat Rp500rb–1jt + Subsidi Silang 5% IPI Mandiri untuk selamatkan pendaftaran.",
                  font_size=9.5, space_after=2, bold_color=ALERT_RED, norm_color=ALERT_RED)

    add_footer(s2, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Ringkasan Eksekutif")

    # =================================================================
    # SLIDE 3: SECTION DIVIDER — ANALISIS TREN & PORTOFOLIO
    # =================================================================
    sn += 1
    add_section_divider(prs, blank, 1, "Analisis Tren & Portofolio Program Studi", sn, TOTAL)
    print(f"  [OK] Slide {sn}: Section Divider 01")

    # =================================================================
    # SLIDE 4: TREN MAKRO 5 TAHUN
    # =================================================================
    sn += 1
    s4 = prs.slides.add_slide(blank)
    create_header_v2(s4, "Evaluasi Tren Makro 5 Tahun USK (2022–2026)",
                     "Kapasitas Melompat ke 10.435 Kursi, Beban ~2.000 Bangku Kosong Tetap Berulang Setiap Tahun")

    chart_w4 = Inches(8.0)
    add_img(s4, chart_dir, "01_tren_makro_peminat_dt_du_usk.png", MARGIN_L, CONTENT_TOP, width=chart_w4)

    # Bottom Banner under Chart
    add_banner_callout(s4, MARGIN_L, Inches(5.25), chart_w4, Inches(1.60),
                       "AKUMULASI 5 TAHUN: 10.984 KURSI KOSONG (23,0% KUOTA TERBUANG)",
                       "• Peminat tumbuh pesat +39,5% (48.769 → 68.010), Daya Tampung melonjak +32,7% (5.485 → 7.280 S1).\n"
                       "• Peningkatan kuota tidak diimbangi daya serap riil mahasiswa yang mendaftar ulang.\n"
                       "• Implikasi: Terjadi structural capacity mismatch persisten ~2.000 bangku kosong setiap tahun akademik.",
                       title_color=ALERT_RED, title_size=10.5, sub_size=9)

    # Right Card
    _, tf4 = add_card_v2(s4, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf4, "EVOLUSI METRIK 5 TAHUN:", ROYAL_BLUE)
    add_bullet_v2(tf4, "2022:", "48.769 Peminat | 7.863 Kuota | 6.197 DU | 1.666 Kosong (Fill 78,8%)", font_size=10, space_after=4)
    add_bullet_v2(tf4, "2023:", "44.653 Peminat | 8.780 Kuota | 6.299 DU | 2.481 Kosong (Fill 71,7%)", font_size=10, space_after=4)
    add_bullet_v2(tf4, "2024:", "65.495 Peminat | 10.240 Kuota | 7.791 DU | 2.449 Kosong (Fill 76,1%)", font_size=10, space_after=4)
    add_bullet_v2(tf4, "2025:", "70.945 Peminat | 10.420 Kuota | 8.027 DU | 2.393 Kosong (Fill 77,0%)", font_size=10, space_after=4)
    add_bullet_v2(tf4, "2026:", "68.010 Peminat | 10.435 Kuota | 8.440 DU | 1.995 Kosong (Fill 80,9%)", font_size=10, space_after=6)
    add_bullet_v2(tf4, "Kesimpulan Audit:", "USK tidak kekurangan peminat, melainkan over-ekspansi kuota pada program studi yang salah.",
                  font_size=10, space_after=3, bold_color=DEEP_RED)

    add_footer(s4, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Tren Makro (Upgraded)")

    # =================================================================
    # SLIDE 5: PETA KEKETATAN SELEKSI & MFR 2026
    # =================================================================
    sn += 1
    s5 = prs.slides.add_slide(blank)
    create_header_v2(s5, "Peta Keketatan Seleksi 2026: Disparitas Rasio 39:1 vs Peminat di Bawah Kuota",
                     "Polarisasi Ekstrem Antara Program Studi Favorit Industri vs Rumpun Ilmu Dasar & Maritim")

    chart_w5 = Inches(8.0)
    add_img(s5, chart_dir, "04_rasio_keketatan_peminatan_vs_daya_tampung.png", MARGIN_L, CONTENT_TOP, width=chart_w5)

    add_banner_callout(s5, MARGIN_L, Inches(5.45), chart_w5, Inches(1.40),
                       "DISPARITAS PASAR EKSTREM: JURANG SELEKSI HINGGA 43× LIPAT",
                       "• Top Favorit (Farmasi 39,2:1, Akuntansi Pajak 22,4:1, Informatika 18,1:1) menghadapi persaingan sangat ketat.\n"
                       "• Rumpun Rentan (Budidaya Perairan 0,91:1) justru mengalami defisit pendaftar — kuota lebih banyak dari peminat!",
                       title_color=ORANGE_ACC, title_size=10.5, sub_size=9)

    _, tf5 = add_card_v2(s5, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf5, "TOP 8 PALING FAVORIT:", SUCCESS_GRN)
    add_bullet_v2(tf5, "", "1. Farmasi (39,18:1)\n2. D4 Akuntansi Pajak (22,43:1)\n3. Informatika (18,12:1)\n4. Psikologi (17,31:1)\n5. T. Perminyakan (15,50:1)\n6. T. Pertambangan (14,46:1)\n7. Manajemen (14,12:1)\n8. Bisnis Digital (12,79:1)",
                  font_size=9.5, space_after=8, norm_color=SLATE_700)

    p_sep = tf5.add_paragraph()
    p_sep.text = "─────── vs ───────"
    p_sep.font.size = Pt(8)
    p_sep.font.color.rgb = GOLD
    p_sep.alignment = PP_ALIGN.CENTER
    p_sep.space_after = Pt(5)

    add_card_title_inline = tf5.add_paragraph()
    add_card_title_inline.text = "TOP 8 PALING RENTAN:"
    add_card_title_inline.font.bold = True
    add_card_title_inline.font.size = Pt(12)
    add_card_title_inline.font.color.rgb = ALERT_RED
    add_card_title_inline.space_after = Pt(5)

    add_bullet_v2(tf5, "", "1. Budidaya Perairan (0,91:1 — MINUS!)\n2. PSP Perikanan (1,08:1)\n3. Fisika (1,18:1)\n4. Pend. Fisika (1,29:1)\n5. Proteksi Tanaman (1,31:1)\n6. Ilmu Tanah (1,35:1)\n7. Pend. Kimia (1,52:1)\n8. Pend. Geografi (1,56:1)",
                  font_size=9.5, space_after=3, norm_color=SLATE_700)

    add_footer(s5, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Keketatan 2026 (Upgraded)")

    # =================================================================
    # SLIDE 6: BENCHMARK KEKETATAN 5 TAHUN
    # =================================================================
    sn += 1
    s6 = prs.slides.add_slide(blank)
    create_header_v2(s6, "Benchmark Keketatan 5 Tahun (2022–2026): Eliminasi Bias Anomali Tahunan",
                     "Polarisasi minat bukan fenomena insidental — ini ketimpangan preferensi struktural selama setengah dekade")

    chart_w6 = Inches(8.0)
    add_img(s6, chart_dir, "12_tren_keketatan_seleksi_5_tahun_2022_2026.png", MARGIN_L, CONTENT_TOP, width=chart_w6)

    add_banner_callout(s6, MARGIN_L, Inches(5.75), chart_w6, Inches(1.10),
                       "TEMUAN BENCHMARK 5 TAHUN: KEGAGALAN PASAR KRONIS PERMANEN",
                       "• Fisika (0,85:1) & Budidaya Perairan (1,01:1) selama 5 tahun berturut-turut mencatat rasio di bawah atau setara 1:1.\n"
                       "• Tanpa seleksi pun pendaftar tidak mencukupi kuota. Kebijakan menambah daya tampung di prodi ini terbukti kontra-produktif.",
                       title_color=DEEP_RED, title_size=10.5, sub_size=9)

    _, tf6 = add_card_v2(s6, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf6, "RATA-RATA 5 TAHUN:", ROYAL_BLUE)
    add_bullet_v2(tf6, "Top 5 Favorit:", "Farmasi (44,1:1), Informatika (21,5:1), Psikologi (17,3:1), P. Dokter Gigi (17,2:1), Akuntansi Pajak (14,2:1)",
                  font_size=10, space_after=8, bold_color=SUCCESS_GRN)
    add_bullet_v2(tf6, "Bottom 5 Sepi:", "Fisika (0,85:1), Budidaya Perairan (1,01:1), PSP Perikanan (1,13:1), Pend. Fisika (1,31:1), Proteksi Tanaman (1,40:1)",
                  font_size=10, space_after=8, bold_color=ALERT_RED)
    add_bullet_v2(tf6, "Aksi Rekomendasi:", "Hentikan alokasi kuota berbasis kebiasaan historis; pangkas kuota Fisika & BDP minimal 35–40%.",
                  font_size=10, space_after=3, bold_color=ORANGE_ACC)

    add_footer(s6, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Benchmark Keketatan 5 Tahun (Upgraded)")

    # =================================================================
    # SLIDE 7: BINTANG PERTUMBUHAN VS SINYAL WASPADA
    # =================================================================
    sn += 1
    s7 = prs.slides.add_slide(blank)
    create_header_v2(s7, "Bintang Pertumbuhan vs Sinyal Waspada: Analisis Slope OLS & CAGR Multi-Tahun")

    add_img(s7, chart_dir, "02_top_tren_peningkatan_pendaftar_dan_peminat.png", MARGIN_L, CONTENT_TOP, width=Inches(5.75))
    add_img(s7, chart_dir, "03_top_tren_penurunan_pendaftar_dan_peminat.png", Inches(6.78), CONTENT_TOP, width=Inches(5.75))

    # Bottom cards placed snugly
    y7 = Inches(5.05)
    h7 = Inches(2.05)
    _, tf7_l = add_card_v2(s7, MARGIN_L, y7, Inches(5.75), h7,
                            bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    add_card_title(tf7_l, "🟢 BINTANG PERTUMBUHAN (OLS POSITIF)", SUCCESS_GRN, 10.5)
    add_bullet_v2(tf7_l, "1. Keperawatan:", "+38,4 mhs/thn (CAGR +23,5%). Pasar ners global Jepang/Jerman.", font_size=9.5, space_after=2)
    add_bullet_v2(tf7_l, "2. PGSD:", "+27,4 mhs/thn (CAGR +19,9%). 4 thn beruntun naik! Formasi PPPK daerah.", font_size=9.5, space_after=2)
    add_bullet_v2(tf7_l, "Rekor R² Sempurna:", "PGSD, Kehutanan, Pend. Geografi, PPKn — 4 thn berturut naik tanpa pernah turun.", font_size=9.5, space_after=1, bold_color=ORANGE_ACC)

    # Bottom red card
    _, tf7_r = add_card_v2(s7, Inches(6.78), y7, Inches(5.75), h7,
                            bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(tf7_r, "🔴 SINYAL WASPADA (OLS NEGATIF / ZERO REBOUND)", DEEP_RED, 10.5)
    add_bullet_v2(tf7_r, "1. Manajemen FEB:", "-16,2 mhs/thn. Zero rebound! Terkanibalisasi Bisnis Digital.", font_size=9.5, space_after=2)
    add_bullet_v2(tf7_r, "2. Ekonomi Islam & Pembangunan:", "-9,3 dan -6,4 mhs/thn. Anomali di daerah bersyariat.", font_size=9.5, space_after=2)
    add_bullet_v2(tf7_r, "Aksi Strategis:", "Restrukturisasi kurikulum FEB ke arah Fintech & Business Analytics.", font_size=9.5, space_after=1, bold_color=DEEP_RED)

    add_footer(s7, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Growth vs Decline (Upgraded)")

    # =================================================================
    # SLIDE 8: KAUSALITAS LAPANGAN
    # =================================================================
    sn += 1
    s8 = prs.slides.add_slide(blank)
    create_header_v2(s8, "Eksplorasi Kausalitas Lapangan: Fakta Data Empiris vs Temuan Desk Research",
                     "Memisahkan bukti terukur dari analisis penyebab kontekstual (pasar kerja, regulasi, biaya)")

    # Two-column layout
    col_w8 = Inches(5.75)
    card_h8 = Inches(5.15)

    # Left: Prodi NAIK
    _, tf8_l = add_card_v2(s8, MARGIN_L, CONTENT_TOP, col_w8, card_h8,
                            bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    add_card_title(tf8_l, "FAKTOR PENDORONG PRODI TUMBUH TINGGI (DEMAND SURGE)", SUCCESS_GRN, 11)
    add_bullet_v2(tf8_l, "Keperawatan (+132%, 127→295 mhs):", "Program G-to-G ners ke Jepang & Jerman dengan gaji tinggi. Kuota dinaikkan karena pasar menyerap habis 100%.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_l, "PGSD (+106%, 105→217 mhs):", "Formasi PPPK guru SD daerah di Aceh mencapai ribuan; kepastian karir langsung mendorong lonjakan minat 4 tahun beruntun.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_l, "Teknik Komputer (+71%, 85→145 mhs):", "Megatren kecerdasan buatan (AI), IoT, cloud engineering, & otomatisasi industri menarik minat pelamar saintek.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_l, "Kehutanan (+92%, 103→198 mhs):", "Peluang karir baru di sektor ESG, sertifikasi bursa karbon Ekosistem Leuser, dan valuasi jasa lingkungan global.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_l, "Teknik Sipil (+64%, 154→252 mhs):", "Penyerapan masif proyek infrastruktur strategis Aceh, konektivitas tol, dan rehabilitasi pasca-PON XXI.", font_size=9.2, space_after=5)
    add_bullet_v2(tf8_l, "📌 KESIMPULAN:", "Prodi tumbuh karena relevansi langsung dengan kebutuhan pasar kerja, regulasi formasi ASN, & standar global.",
                  font_size=9.2, space_after=1, bold_color=SUCCESS_GRN, norm_color=SUCCESS_GRN)

    # Right: Prodi TURUN
    _, tf8_r = add_card_v2(s8, Inches(6.78), CONTENT_TOP, col_w8, card_h8,
                            bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(tf8_r, "AKAR PENYEBAB PRODI MENURUN / BOCOR (DEFICIT DRIVERS)", DEEP_RED, 11)
    add_bullet_v2(tf8_r, "Manajemen FEB (-25%, 266→199 mhs):", "Kanibalisasi internal masif oleh S1 Bisnis Digital (baru 2024, sedot 800+ peminat) ditambah saturasi lulusan PTS.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_r, "Ekonomi Pembangunan & Islam (-20% s.d. -26%):", "Kurikulum teori konvensional belum adaptif terhadap revolusi Fintech, Islamic Digital Banking, & data analytics.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_r, "Budidaya Perairan & Fisika (Krisis Peminat):", "Persepsi minimnya lapangan kerja formal. Generasi Z menghindari sains murni teoritis tanpa applied skills.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_r, "Jalur Mandiri SMMPTN (25% Gugur):", "SK Rektor 1162/2026 mewajibkan IPI Rp10–35 jt lunas dalam 5 hari kerja, memicu liquidity shock bagi orang tua.", font_size=9.2, space_after=3)
    add_bullet_v2(tf8_r, "Jalur TALENTA (75% Kabur / 935 Gugur):", "Pendaftaran gratis tanpa commitment fee; dijadikan cadangan spekulatif sebelum siswa kabur ke pengumuman UTBK.", font_size=9.2, space_after=5)
    add_bullet_v2(tf8_r, "📌 KESIMPULAN:", "Penurunan dipicu kanibalisasi internal tanpa penyesuaian kuota, kurikulum usang, & friksi skema pembayaran IPI.",
                  font_size=9.2, space_after=1, bold_color=DEEP_RED, norm_color=DEEP_RED)

    add_footer(s8, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Kausalitas Lapangan (Enriched)")

    # =================================================================
    # SLIDE 9: OVER-EKSPANSI & MARGINAL FILL RATE
    # =================================================================
    sn += 1
    s9 = prs.slides.add_slide(blank)
    create_header_v2(s9, "Fenomena Over-Ekspansi Kuota & Marginal Fill Rate (MFR)",
                     "Menambah daya tampung TIDAK otomatis menambah mahasiswa — bukti inefisiensi alokasi kuota")

    add_img(s9, chart_dir, "05_over_ekspansi_kuota_vs_daftar_ulang_riil.png", MARGIN_L, CONTENT_TOP, width=Inches(7.8))

    _, tf9 = add_card_v2(s9, Inches(8.85), CONTENT_TOP, Inches(3.68), Inches(5.2))
    add_card_title(tf9, "\"THE BIG FOUR\" OVER-EKSPANSI:", ROYAL_BLUE)
    add_bullet_v2(tf9, "Formulasi:", "MFR = ΔDaftar Ulang / ΔDaya Tampung\n(Benchmark: MFR ≥ 0,80 = sehat)", font_size=10, space_after=8)
    add_bullet_v2(tf9, "Budidaya Perairan:", "Kuota 160, DU macet 90 → MFR 0,00 (GAGAL TOTAL). 70 Kursi Kosong.", font_size=10, space_after=5)
    add_bullet_v2(tf9, "THP Pertanian:", "Kuota 2x lipat (80→160), DU +50 → MFR 0,62. 58 Kursi Kosong.", font_size=10, space_after=5)
    add_bullet_v2(tf9, "Pend. Ekonomi:", "Kuota +60 kursi, DU hanya +24 → MFR 0,40. 57 Kursi Kosong.", font_size=10, space_after=5)
    add_bullet_v2(tf9, "Teknik Kimia:", "Kuota +40, DU +24 → MFR 0,60. 60 Kursi Kosong.", font_size=10, space_after=8)
    add_bullet_v2(tf9, "Dampak Rasionalisasi:", "Merasionalkan 4 prodi ini = hapus 245 bangku kosong semu (25% masalah kursi kosong seluruh USK)!",
                  font_size=10, space_after=4, bold_color=ORANGE_ACC)

    add_footer(s9, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Over-Ekspansi & MFR")

    # =================================================================
    # SLIDE 10: MATRIKS 4 KUADRAN SNAPSHOT VS LONGITUDINAL
    # =================================================================
    sn += 1
    s10 = prs.slides.add_slide(blank)
    create_header_v2(s10, "Matriks 4 Kuadran Portofolio: Snapshot 2026 vs Longitudinal 5 Tahun",
                     "Evaluasi Posisi Program Studi Berdasarkan Tingkat Keketatan Seleksi vs Daya Serap Pendaftaran Ulang")

    # Dual Charts side-by-side
    chart_w10 = Inches(5.75)
    add_img(s10, chart_dir, "10_matriks_4_kuadran_prodi_usk.png", MARGIN_L, CONTENT_TOP, width=chart_w10)
    add_img(s10, chart_dir, "13_matriks_4_kuadran_5_tahun_2022_2026.png", Inches(6.78), CONTENT_TOP, width=chart_w10)

    # 4 Quadrant Action Cards below
    y10 = Inches(4.50)
    h10 = Inches(2.35)
    w10 = Inches(2.78)
    gap10 = Inches(0.20)

    # Card 1: Kuadran I
    _, t10_1 = add_card_v2(s10, MARGIN_L, y10, w10, h10,
                            bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    add_card_title(t10_1, "KUADRAN I (31 PRODI)", SUCCESS_GRN, 11)
    add_bullet_v2(t10_1, "Prima:", "Keketatan ≥ 4,0 & Fill ≥ 80%. Farmasi, Informatika, PGSD, Kedokteran, Hukum.", font_size=9, space_after=3)
    add_bullet_v2(t10_1, "Aksi:", "MAINTAIN & INVEST. Buka Kelas Internasional & Fast Track S1-S2.", font_size=9, space_after=2, bold_color=SUCCESS_GRN)

    # Card 2: Kuadran II
    _, t10_2 = add_card_v2(s10, MARGIN_L + w10 + gap10, y10, w10, h10,
                            bg_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    add_card_title(t10_2, "KUADRAN II (6 PRODI)", ROYAL_BLUE, 11)
    add_bullet_v2(t10_2, "Stabil:", "Keketatan < 4,0 & Fill ≥ 80%. Arsitektur, HI, Pend. Dokter Hewan.", font_size=9, space_after=3)
    add_bullet_v2(t10_2, "Aksi:", "PROTECT & CONTROL. Pertahankan kuota, cegah kanibalisasi peminat.", font_size=9, space_after=2, bold_color=ROYAL_BLUE)

    # Card 3: Kuadran III
    _, t10_3 = add_card_v2(s10, MARGIN_L + (w10 + gap10)*2, y10, w10, h10,
                            bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(t10_3, "KUADRAN III (22→26 PRODI)", ALERT_RED, 11)
    add_bullet_v2(t10_3, "Defisit Kronis:", "Keketatan < 4,0 & Fill < 80%. Budidaya Perairan, Fisika, PSP, THP.", font_size=9, space_after=3)
    add_bullet_v2(t10_3, "Aksi:", "PANGKAS KUOTA 20%–40%! 5 tahun membuktikan 26 prodi defisit akut.", font_size=9, space_after=2, bold_color=ALERT_RED)

    # Card 4: Kuadran IV
    _, t10_4 = add_card_v2(s10, MARGIN_L + (w10 + gap10)*3, y10, w10, h10,
                            bg_color=RGBColor(255, 247, 237), border_color=RGBColor(254, 215, 170))
    add_card_title(t10_4, "KUADRAN IV (7 PRODI)", ORANGE_ACC, 11)
    add_bullet_v2(t10_4, "Bocor Finansial:", "Keketatan ≥ 4,0 & Fill < 80%. Akuntansi Pajak (22,4x tapi FR 73,8%), PWK.", font_size=9, space_after=3)
    add_bullet_v2(t10_4, "Aksi:", "RETAIN & CONVERT. Cicilan IPI 3 tahap & fast-track auto-call cadangan.", font_size=9, space_after=2, bold_color=ORANGE_ACC)

    add_footer(s10, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Matriks 4 Kuadran (Dual-Chart Upgraded)")

    # =================================================================
    # SLIDE 11: SINTESIS LINTAS DIMENSI
    # =================================================================
    sn += 1
    s11 = prs.slides.add_slide(blank)
    create_header_v2(s11, "Sintesis Lintas Dimensi: Menyilangkan Dinamika Tren dengan Posisi Kuadran",
                     "Menggabungkan Klasifikasi Tren (Velocity) dengan Matriks Kuadran (Position) untuk diagnosa manajerial tajam")

    # 4 cards in 2x2 grid
    cw = Inches(5.75)
    ch = Inches(2.45)
    y11_top = CONTENT_TOP
    y11_bot = Inches(4.25)

    # Card 1: Tren Meningkat x Kuadran I
    _, t11_1 = add_card_v2(s11, MARGIN_L, y11_top, cw, ch,
                            bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    add_card_title(t11_1, "TREN MENINGKAT × KUADRAN I (GROWTH CHAMPIONS)", SUCCESS_GRN, 11)
    add_bullet_v2(t11_1, "Prodi Kunci:", "PGSD, Keperawatan, Teknik Sipil, Teknik Komputer, Ilmu Hukum.", font_size=9.2, space_after=2)
    add_bullet_v2(t11_1, "Karakteristik:", "Rasio keketatan tinggi (>4,0), keterisian prima (>80%), dan slope OLS positif (+15 s.d. +38 mhs/thn).", font_size=9.2, space_after=2)
    add_bullet_v2(t11_1, "Aksi Strategis:", "AGGRESSIVE EXPANSION — Tambah kuota selektif +5–10%, rintis Kelas Internasional, dan Fast Track S1-S2.", font_size=9.2, space_after=2, bold_color=SUCCESS_GRN)
    add_bullet_v2(t11_1, "Target 2027:", "Pertahankan Fill Rate 100% dan tingkatkan penerimaan IPI Mandiri non-subsidi.", font_size=9.2, space_after=1, bold_color=ROYAL_BLUE)

    # Card 2: Tren Menurun x Kuadran I
    _, t11_2 = add_card_v2(s11, Inches(6.78), y11_top, cw, ch,
                            bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(t11_2, "TREN MENURUN × KUADRAN I (MATURE / THREATENED)", DEEP_RED, 11)
    add_bullet_v2(t11_2, "Prodi Kunci:", "Manajemen FEB, Ekonomi Pembangunan, Ekonomi Islam.", font_size=9.2, space_after=2)
    add_bullet_v2(t11_2, "Karakteristik:", "Kapasitas saat ini masih terisi (>80%) karena reputasi lama, namun tren peminat merosot kontinu (Zero Rebound).", font_size=9.2, space_after=2)
    add_bullet_v2(t11_2, "Aksi Strategis:", "CONTROLLED DOWNSIZING — Moratorium penambahan kuota; rampingkan kapasitas agar kelas tetap padat 100%.", font_size=9.2, space_after=2, bold_color=DEEP_RED)
    add_bullet_v2(t11_2, "Target 2027:", "Re-engineering kurikulum ke Digital Business Analytics; hentikan kanibalisasi internal Bisnis Digital.", font_size=9.2, space_after=1, bold_color=ALERT_RED)

    # Card 3: Tren Fluktuatif x Kuadran IV
    _, t11_3 = add_card_v2(s11, MARGIN_L, y11_bot, cw, ch,
                            bg_color=RGBColor(255, 247, 237), border_color=RGBColor(253, 230, 138))
    add_card_title(t11_3, "TREN FLUKTUATIF × KUADRAN IV (HIGH-RISK CASH COWS)", ORANGE_ACC, 11)
    add_bullet_v2(t11_3, "Prodi Kunci:", "D4 Akuntansi Perpajakan (Keketatan 22,4x tapi Fill 73,8%), Teknik Perminyakan, PWK, PAUD.", font_size=9.2, space_after=2)
    add_bullet_v2(t11_3, "Karakteristik:", "Peminat sangat banyak, namun yield pendaftaran ulang anjlok akibat seleksi Mandiri yang bocor parah.", font_size=9.2, space_after=2)
    add_bullet_v2(t11_3, "Aksi Strategis:", "FINANCIAL & YIELD OPTIMIZATION — Terapkan cicilan IPI 3 tahap dan sistem fast-track auto-call cadangan 48 jam.", font_size=9.2, space_after=2, bold_color=ORANGE_ACC)
    add_bullet_v2(t11_3, "Target 2027:", "Naikkan Fill Rate dari 73% ke ≥90%; selamatkan potensi penerimaan IPI Rp4,5–6 Miliar yang hilang.", font_size=9.2, space_after=1, bold_color=ROYAL_BLUE)

    # Card 4: Peminatan Rendah x Kuadran III
    _, t11_4 = add_card_v2(s11, Inches(6.78), y11_bot, cw, ch,
                            bg_color=RGBColor(254, 226, 226), border_color=RGBColor(252, 165, 165))
    add_card_title(t11_4, "PEMINATAN RENDAH × KUADRAN III (CHRONIC DEFICIT)", ALERT_RED, 11)
    add_bullet_v2(t11_4, "Prodi Kunci:", "Budidaya Perairan (56%), Fisika (65%), Teknik Kimia (67%), THP (64%), Pend. Kimia, Pend. Fisika.", font_size=9.2, space_after=2)
    add_bullet_v2(t11_4, "Karakteristik:", "Keketatan <4,0 dan keterisian <80% persisten 5 tahun; menyumbang 48,4% seluruh bangku kosong universitas.", font_size=9.2, space_after=2)
    add_bullet_v2(t11_4, "Aksi Strategis:", "RADICAL CAPACITY RATIONALIZATION — Pangkas kuota 20%–40% segera; hapus 400+ kursi kosong semu.", font_size=9.2, space_after=2, bold_color=ALERT_RED)
    add_bullet_v2(t11_4, "Target 2027:", "Sehatkan rasio dosen-mahasiswa nasional & internasional demi menyelamatkan akreditasi unggul.", font_size=9.2, space_after=1, bold_color=DEEP_RED)

    add_footer(s11, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Sintesis Tren × Kuadran (Enriched)")

    # =================================================================
    # SLIDE 12: SECTION DIVIDER — DEKONSTRUKSI KEBOCORAN PMB
    # =================================================================
    sn += 1
    add_section_divider(prs, blank, 2, "Dekonstruksi Kebocoran Penerimaan Mahasiswa Baru", sn, TOTAL)
    print(f"  [OK] Slide {sn}: Section Divider 02")

    # =================================================================
    # SLIDE 13: DINAMIKA JALUR MASUK 5 TAHUN
    # =================================================================
    sn += 1
    s13 = prs.slides.add_slide(blank)
    create_header_v2(s13, "Dinamika Jalur Masuk & Corong Kebocoran: Panorama 5 Tahun (2022–2026)",
                     "Komposisi 8.440 Mahasiswa Baru 2026 dan Evaluasi Yield Rate per Jalur")

    chart_w13 = Inches(8.0)
    add_img(s13, chart_dir, "06_dinamika_jalur_masuk_dan_kebocoran_2026.png", MARGIN_L, CONTENT_TOP, width=chart_w13)

    add_banner_callout(s13, MARGIN_L, Inches(5.25), chart_w13, Inches(1.60),
                       "KEBOCORAN PMB MEMBENGKAK +94,9% DALAM 5 TAHUN (1.231 → 2.399 CALON)",
                       "• SNBP (Yield 94,8%): Sangat loyal & stabil karena didukung sanksi tegas sekolah/siswa.\n"
                       "• TALENTA (Yield 24,9%): Keruntuhan total akibat pendaftaran tanpa commitment fee di awal (dijadikan tiket cadangan).\n"
                       "• SMMPTN Mandiri (Yield 75,0%): Tenggat pembayaran IPI 5 hari menimbulkan liquidity shock bagi keluarga.",
                       title_color=ALERT_RED, title_size=10.5, sub_size=9)

    _, tf13 = add_card_v2(s13, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf13, "KOMPOSISI & KEBOCORAN 2026:", ROYAL_BLUE, 12)
    add_bullet_v2(tf13, "SNBT (38,6%):", "3.260 mhs. Kebocoran 626 calon (Yield 83,9%).", font_size=10, space_after=4)
    add_bullet_v2(tf13, "SNBP (32,6%):", "2.754 mhs. Paling loyal (Yield 94,8%). Sanksi blacklist efektif.", font_size=10, space_after=4)
    add_bullet_v2(tf13, "SMMPTN (21,5%):", "1.814 mhs. Bocor 604 calon (Yield 75,0%). IPI 5 hari terlalu mepet.", font_size=10, space_after=4)
    add_bullet_v2(tf13, "TALENTA (3,7%):", "308 mhs. CRASH! 935 calon gugur (Yield 24,9%). Yield jatuh dari 88,3% (2024) → 24,9% (2026).",
                  font_size=10, space_after=4, bold_color=ALERT_RED)
    add_bullet_v2(tf13, "Kebocoran 5 Tahun:", "Membengkak dari 1.231 (2022) menjadi 2.399 (2026) = +94,9% dalam 5 tahun!",
                  font_size=10, space_after=3, bold_color=ORANGE_ACC)

    add_footer(s13, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Jalur Masuk (Upgraded)")

    # =================================================================
    # SLIDE 14: KOMPARATIF KIP + PLOT TWIST
    # =================================================================
    sn += 1
    s14 = prs.slides.add_slide(blank)
    create_header_v2(s14, "Resolusi \"Plot Twist\": Kursi Kosong SNBT Bukan Siswa Kabur — Terhempas KIP!",
                     "Korelasi 97,6%: 626 Calon Gugur SNBT ≈ 611 Pelamar KIP Ditolak Beasiswa")

    chart_w14 = Inches(8.0)
    add_img(s14, chart_dir, "20_analisis_desil_dan_rejection_kip_snbt.png", MARGIN_L, CONTENT_TOP, width=chart_w14)

    add_banner_callout(s14, MARGIN_L, Inches(5.25), chart_w14, Inches(1.60),
                       "RESOLUSI PLOT TWIST: KORELASI ANOMALI 97,60% TERBUKTI SECARA STATISTIK",
                       "• Premis 'calon mahasiswa kabur ke PTS' terbantahkan secara telak oleh data empiris.\n"
                       "• 626 Kursi Kosong SNBT hampir identik 1-to-1 dengan 611 Pelamar KIP-K yang Ditolak Beasiswanya.\n"
                       "• Kesimpulan: Kursi kosong SNBT bukan kegagalan daya tarik universitas, melainkan kegagalan daya beli siswa miskin.",
                       title_color=DEEP_RED, title_size=10.5, sub_size=9)

    _, tf14 = add_card_v2(s14, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf14, "KOMPARATIF KIP 2025 VS 2026:", ROYAL_BLUE, 12)
    add_bullet_v2(tf14, "Kuota KIP 2025:", "1.846 kursi. Penolakan SNBT hanya 370 orang (29,0%).", font_size=10, space_after=4)
    add_bullet_v2(tf14, "Kuota KIP 2026:", "DIPANGKAS -207 kursi (-11,2%) menjadi 1.639. Pendaftar KIP SNBT justru naik ke 1.361 orang.",
                  font_size=10, space_after=4, bold_color=ALERT_RED)
    add_bullet_v2(tf14, "Efek Penyerapan SNBP:", "893 kursi KIP terserap SNBP di awal → sisa KIP untuk SNBT hanya 746 kursi.",
                  font_size=10, space_after=4)
    add_bullet_v2(tf14, "Ledakan Penolakan:", "611 siswa KIP SNBT ditolak (+65,1% dari 2025!). Kesesuaian dengan 626 kursi kosong = 97,60%.",
                  font_size=10, space_after=4, bold_color=DEEP_RED)
    add_bullet_v2(tf14, "Kesimpulan:", "Kursi kosong SNBT = kegagalan daya beli (economic forced drop-out), bukan siswa kabur ke PTS.",
                  font_size=10, space_after=3, bold_color=ORANGE_ACC)

    add_footer(s14, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Plot Twist KIP (Upgraded)")

    # =================================================================
    # SLIDE 15: CLIFF-EDGE DESIL 5 & 6
    # =================================================================
    sn += 1
    s15 = prs.slides.add_slide(blank)
    create_header_v2(s15, "\"The Smoking Gun\": Penolakan KIP Terkonsentrasi pada Desil 5 & 6 (>98% Ditolak!)")

    # Left: Desil data card
    _, tf15_l = add_card_v2(s15, MARGIN_L, CONTENT_TOP, Inches(6.0), Inches(5.2))
    add_card_title(tf15_l, "PROFIL PENERIMAAN KIP SNBT 2026 PER DESIL DTKS:", ROYAL_BLUE, 11)

    add_bullet_v2(tf15_l, "Desil 1 (Sangat Miskin):", "221 Pendaftar | 200 Diterima (90,5%) — Aman ✓", font_size=10.5, space_after=4, bold_color=SUCCESS_GRN)
    add_bullet_v2(tf15_l, "Desil 2 (Miskin):", "186 Pendaftar | 162 Diterima (87,1%) — Aman ✓", font_size=10.5, space_after=4, bold_color=SUCCESS_GRN)
    add_bullet_v2(tf15_l, "Desil 3 (Hampir Miskin):", "219 Pendaftar | 204 Diterima (93,2%) — Aman ✓", font_size=10.5, space_after=4, bold_color=SUCCESS_GRN)
    add_bullet_v2(tf15_l, "Desil 4 (Rentan Miskin):", "176 Pendaftar | 160 Diterima (90,9%) — Aman ✓", font_size=10.5, space_after=8, bold_color=SUCCESS_GRN)

    p_cut = tf15_l.add_paragraph()
    p_cut.text = "━━━━━━━━━ GARIS CUTOFF AMBANG KUOTA KIP APBN ━━━━━━━━━"
    p_cut.font.size = Pt(9)
    p_cut.font.bold = True
    p_cut.font.color.rgb = ALERT_RED
    p_cut.space_after = Pt(8)

    add_bullet_v2(tf15_l, "Desil 5:", "149 Pendaftar | HANYA 3 DITERIMA (2,0%) | 146 DITOLAK (98,0%)!", font_size=10.5, space_after=4, bold_color=DEEP_RED)
    add_bullet_v2(tf15_l, "Desil 6:", "385 Pendaftar | HANYA 5 DITERIMA (1,3%) | 380 DITOLAK (98,7%)!", font_size=10.5, space_after=6, bold_color=DEEP_RED)
    add_bullet_v2(tf15_l, "TOTAL DESIL 5 & 6:", "526 CALON MAHASISWA BERPRESTASI UTBK DITOLAK!", font_size=11, space_after=3, bold_color=DEEP_RED)

    # Right: Economic Drop-Out mechanism
    _, tf15_r = add_card_v2(s15, Inches(7.05), CONTENT_TOP, Inches(5.48), Inches(5.2),
                             bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(tf15_r, "MEKANISME ECONOMIC FORCED DROP-OUT", DEEP_RED, 12)
    add_bullet_v2(tf15_r, "1. Dialihkan ke UKT Reguler:", "526 calon Desil 5-6 yang ditolak KIP langsung dikenakan UKT Kelompok III–V (Rp 2,5–5 Juta/semester).", font_size=10.5, space_after=8)
    add_bullet_v2(tf15_r, "2. Profil Prasejahtera:", "Keluarga petani kecil, buruh harian, nelayan tradisional, pedagang mikro — tanpa bantalan tabungan darurat.", font_size=10.5, space_after=8)
    add_bullet_v2(tf15_r, "3. Mundur Terpaksa:", "Tagihan UKT jutaan rupiah dalam tempo verifikasi sempit → 526 calon terpaksa tidak mendaftar ulang.", font_size=10.5, space_after=8)
    add_bullet_v2(tf15_r, "4. Sumber 84% Kursi Kosong:", "526 dari 626 bangku kosong SNBT (84,0%) tercipta langsung dari mekanisme ini!",
                  font_size=11, space_after=3, bold_color=DEEP_RED)

    add_footer(s15, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Cliff-Edge Desil 5 & 6")

    # =================================================================
    # SLIDE 16: DAMPAK SEKTORAL TOP 20 PRODI
    # =================================================================
    sn += 1
    s16 = prs.slides.add_slide(blank)
    create_header_v2(s16, "Sinkronisasi Sektoral: Korelasi Calon Gugur vs Penolakan KIP Desil 5–6 per Prodi",
                     "Evaluasi Lintas Program Studi Membuktikan Paralelisme Sempurna Antara Penolakan Beasiswa dan Bangku Kosong")

    chart_w16 = Inches(8.0)
    add_img(s16, chart_dir, "23_korelasi_prodi_calon_gugur_vs_kip_desil.png", MARGIN_L, CONTENT_TOP, width=chart_w16)

    add_banner_callout(s16, MARGIN_L, Inches(5.90), chart_w16, Inches(0.95),
                       "BUKTI PARALELISME 100%: FAKULTAS KEPERAWATAN & RUMPUN AGRO-MARITIM",
                       "• Keperawatan (20 gugur ↔ 20 KIP ditolak) dan Sospol membuktikan korelasi 1-to-1 sempurna.\n"
                       "• Mahasiswa di prodi-prodi ini mundur murni karena ketiadaan beasiswa pasca penetapan UKT reguler.",
                       title_color=ROYAL_BLUE, title_size=10, sub_size=8.5)

    _, tf16 = add_card_v2(s16, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf16, "BUKTI PARALELISME PER PRODI:", ROYAL_BLUE, 12)
    add_bullet_v2(tf16, "Keperawatan:", "20 Gugur ↔ 20 KIP Desil 5-6 Ditolak (Korelasi 100%!)", font_size=10, space_after=4, bold_color=ALERT_RED)
    add_bullet_v2(tf16, "PGSD:", "9 Gugur ↔ 20 KIP Desil 5-6 Ditolak", font_size=10, space_after=4)
    add_bullet_v2(tf16, "Akuntansi:", "20 Gugur ↔ 14 KIP Desil 5-6 Ditolak", font_size=10, space_after=4)
    add_bullet_v2(tf16, "Budidaya Perairan:", "16 Gugur ↔ 12 KIP Desil 5-6 Ditolak", font_size=10, space_after=4)
    add_bullet_v2(tf16, "Ilmu Hukum:", "14 Gugur ↔ 15 KIP Desil 5-6 Ditolak", font_size=10, space_after=4)
    add_bullet_v2(tf16, "D3 Agribisnis:", "40 Gugur dari 57 Lulus — 17 KIP ditolak. Vokasi paling parah!", font_size=10, space_after=4, bold_color=ALERT_RED)
    add_bullet_v2(tf16, "Ilmu Pemerintahan:", "12 Gugur ↔ 14 KIP (100% Desil 5-6)", font_size=10, space_after=6)
    add_bullet_v2(tf16, "Kesimpulan:", "Prodi rumpun keguruan, kesehatan, pertanian, & sospol bocor murni karena benturan ekonomi, bukan ketiadaan peminat.",
                  font_size=10, space_after=3, bold_color=ORANGE_ACC)

    add_footer(s16, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Dampak Sektoral (Upgraded)")

    # =================================================================
    # SLIDE 17: SECTION DIVIDER — DIMENSI SOSIAL-EKONOMI & KINERJA
    # =================================================================
    sn += 1
    add_section_divider(prs, blank, 3, "Dimensi Sosial-Ekonomi & Kinerja Institusi", sn, TOTAL)
    print(f"  [OK] Slide {sn}: Section Divider 03")

    # =================================================================
    # SLIDE 18: STRATIFIKASI KIP ANTAR KUADRAN
    # =================================================================
    sn += 1
    s18 = prs.slides.add_slide(blank)
    create_header_v2(s18, "Stratifikasi Sosial-Ekonomi: Kuadran III Sebagai Jaring Pengaman Sosial USK",
                     "Distribusi Mahasiswa Prasejahtera Sangat Timpang — Kuadran III Menanggung Beban Sosial Terbesar")

    chart_w18 = Inches(8.0)
    add_img(s18, chart_dir, "21_ketergantungan_kip_antar_kuadran_dan_top_prodi.png", MARGIN_L, CONTENT_TOP, width=chart_w18)

    add_banner_callout(s18, MARGIN_L, Inches(5.50), chart_w18, Inches(1.35),
                       "KUADRAN III = JARING PENGAMAN SOSIAL & DEMOKRATISASI KAMPUS USK",
                       "• Penetrasi beasiswa Kuadran III (31,1%) mencapai 2,4× Kuadran I (13,2%). PSP Perikanan bahkan 56,7%!\n"
                       "• Program studi Kuadran III menampung anak-anak keluarga nelayan, petani, dan buruh prasejahtera Aceh.\n"
                       "• Alokasi beasiswa KIP harus diproteksi dan disinkronkan untuk menjaga kelangsungan program studi rentan.",
                       title_color=ROYAL_BLUE, title_size=10.5, sub_size=9)

    _, tf18 = add_card_v2(s18, Inches(9.05), CONTENT_TOP, Inches(3.48), Inches(5.2))
    add_card_title(tf18, "PENETRASI KIP PER KUADRAN:", ROYAL_BLUE, 12)
    add_bullet_v2(tf18, "Kuadran I (Unggulan):", "13,19% (515 KIP dari 3.905 mhs). Mandiri finansial, didominasi pembayar UKT tinggi dan IPI.", font_size=10, space_after=5)
    add_bullet_v2(tf18, "Kuadran II (Stabil):", "14,63% (153 KIP dari 1.046 mhs).", font_size=10, space_after=5)
    add_bullet_v2(tf18, "Kuadran IV (Bocor):", "24,47% (163 KIP dari 666 mhs).", font_size=10, space_after=5)
    add_bullet_v2(tf18, "Kuadran III (Defisit):", "31,11% (734 KIP dari 2.359 mhs). 2,4× Kuadran I!", font_size=10, space_after=6, bold_color=ALERT_RED)
    add_bullet_v2(tf18, "Top KIP Dependency:", "PSP Perikanan 56,7%, Pend. Fisika 53,9%, Budidaya Perairan 51,1%, Pend. Ekonomi 49,5%", font_size=9.5, space_after=4)
    add_bullet_v2(tf18, "Lowest KIP (Elite):", "P. Dokter Gigi 1,0%, P. Dokter 2,4%, Informatika 3,4%, T. Perminyakan 3,9%", font_size=9.5, space_after=3)

    add_footer(s18, sn, TOTAL)
    print(f"  [OK] Slide {sn}: KIP Kuadran (Upgraded)")

    # =================================================================
    # SLIDE 19: DEMOGRAFI KIP + KINERJA FAKULTAS (DUAL-CHART UPGRADE)
    # =================================================================
    sn += 1
    s19 = prs.slides.add_slide(blank)
    create_header_v2(s19, "Demografi Penerima KIP-Kuliah & Evaluasi Kinerja 12 Fakultas S1 (2026)",
                     "Profil Sebaran Mahasiswa Prasejahtera dan Diagnostik Pemenuhan Kuota di 12 Fakultas")

    # Dual Charts side-by-side (generous size, crystal clear, vertically centered)
    chart_w19 = Inches(5.75)
    add_img(s19, chart_dir, "22_demografi_fakultas_dan_gender_kip_2026.png", MARGIN_L, CONTENT_TOP, width=chart_w19)
    add_img(s19, chart_dir, "07_analisa_peminatan_dan_keterisian_fakultas.png", Inches(6.78), Inches(1.88), width=chart_w19)

    # Bottom 3 Executive Cards across full width
    y19 = Inches(4.50)
    h19 = Inches(2.35)
    w19 = Inches(3.75)
    gap19 = Inches(0.24)

    # Card 1: Demografi KIP
    _, t19_1 = add_card_v2(s19, MARGIN_L, y19, w19, h19,
                            bg_color=RGBColor(239, 246, 255), border_color=RGBColor(191, 219, 254))
    add_card_title(t19_1, "1. PROFIL DEMOGRAFI KIP", ROYAL_BLUE, 11)
    add_bullet_v2(t19_1, "FKIP Dominan:", "651 KIP (39,7% total universitas) — hampir 40% beasiswa kampus!", font_size=9.5, space_after=3)
    add_bullet_v2(t19_1, "Gender 3,4:1:", "Perempuan 1.268 (77,4%) vs Pria 371 (22,6%). KIP = pilar mobilitas perempuan Aceh.", font_size=9.5, space_after=3, bold_color=ORANGE_ACC)
    add_bullet_v2(t19_1, "Pintu Masuk:", "SNBP menyerap 54,5% di awal, menyisakan kuota KIP ketat di SNBT.", font_size=9.5, space_after=2)

    # Card 2: Kinerja Fakultas
    _, t19_2 = add_card_v2(s19, MARGIN_L + w19 + gap19, y19, w19, h19,
                            bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    add_card_title(t19_2, "2. ZONASI KINERJA 12 FAKULTAS", SUCCESS_GRN, 11)
    add_bullet_v2(t19_2, "Prima (98–100%):", "FKG (100%), Hukum (99,6%), Kedokteran (98,8%). Sangat diminati & presisi.", font_size=9.5, space_after=3, bold_color=SUCCESS_GRN)
    add_bullet_v2(t19_2, "Sehat (>80%):", "FISIP 89,6%, FKH 88,5%, FKep 81,9%, FMIPA 81,9%.", font_size=9.5, space_after=3)
    add_bullet_v2(t19_2, "Kritis (<80%):", "FEB 77,2%, FPK 62,4%, Pertanian 62,1%. Perlu restrukturisasi.", font_size=9.5, space_after=2, bold_color=ALERT_RED)

    # Card 3: Episentrum Defisit
    _, t19_3 = add_card_v2(s19, MARGIN_L + (w19 + gap19)*2, y19, w19, h19,
                            bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(t19_3, "3. KONSENTRASI KURSI KOSONG", DEEP_RED, 11)
    add_bullet_v2(t19_3, "Tiga Episenter:", "FKIP (421 kursi) + Teknik (302) + Pertanian (299).", font_size=9.5, space_after=3, bold_color=DEEP_RED)
    add_bullet_v2(t19_3, "Porsi 65,1%:", "3 fakultas ini menyumbang hampir dua pertiga seluruh bangku kosong USK!", font_size=9.5, space_after=3)
    add_bullet_v2(t19_3, "Arah Kebijakan:", "Rasionalisasi kuota terfokus pada 3 fakultas ini akan menyelesaikan 65% masalah kampus.", font_size=9.5, space_after=2, bold_color=DEEP_RED)

    add_footer(s19, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Demografi KIP + Fakultas (Dual-Chart Upgraded)")

    # =================================================================
    # SLIDE 20: PARETO 80/20 + D3/PSDKU (BALANCED TWO-CARD LAYOUT)
    # =================================================================
    sn += 1
    s20 = prs.slides.add_slide(blank)
    create_header_v2(s20, "Prinsip Pareto: 15 Prodi = 48,4% Seluruh Kursi Kosong | Krisis D3 & PSDKU",
                     "Diagnostik tingkat program studi mengungkap konsentrasi defisit yang sangat tajam")

    # Chart 16A: Focused on the 15 Pareto prodi with generous padding (zero clipping on rank 1 & 2!)
    c16a_name = "16a_episentrum_kursi_kosong_15_prodi.png"
    img_w20 = Inches(6.55)
    add_img(s20, chart_dir, c16a_name, MARGIN_L, CONTENT_TOP, width=img_w20)

    # Right Side: 2 balanced executive cards
    card_l20 = MARGIN_L + img_w20 + Inches(0.25)  # 0.8 + 6.55 + 0.25 = 7.60"
    card_w20 = SLIDE_W - MARGIN_R - card_l20      # 13.333 - 0.8 - 7.60 = 4.933"

    # Card 1: Pareto S1
    _, tf20_1 = add_card_v2(s20, card_l20, CONTENT_TOP, card_w20, Inches(2.45),
                            bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(tf20_1, "EPISENTRUM DEFISIT S1 (PARETO 80/20):", DEEP_RED, 11)
    add_bullet_v2(tf20_1, "15 Prodi = 759 Kursi Kosong:", "48,4% dari total 1.569 kursi kosong S1 Kampus Utama 2026.", font_size=9.5, space_after=3, bold_color=DEEP_RED)
    add_bullet_v2(tf20_1, "Top 5 Defisit Terbesar:", "Budidaya Perairan (70), Keperawatan (65), T. Kimia (60), THP (58), Pend. Ekonomi (57).", font_size=9.5, space_after=3)
    add_bullet_v2(tf20_1, "Akumulasi 5 Tahun:", "3.850 kursi kosong terkonsentrasi di 15 prodi ini (43,4% dari total 8.881 defisit kampus).", font_size=9.5, space_after=2)

    # Card 2: Segmen Khusus D3 & PSDKU
    y20_2 = CONTENT_TOP + Inches(2.55)
    _, tf20_2 = add_card_v2(s20, card_l20, y20_2, card_w20, Inches(2.65),
                            bg_color=RGBColor(255, 247, 237), border_color=RGBColor(254, 215, 170))
    add_card_title(tf20_2, "SEGMEN KHUSUS: KRISIS D3 VOKASI & PSDKU:", ORANGE_ACC, 11)
    add_bullet_v2(tf20_2, "D3 Vokasi (Keterisian 48,5%):", "1.320 kursi terbuang dari 2.565 kuota (4 tahun). D3 Agribisnis hanya 36,8%!\n→ Rekomendasi: Konversi D3→D4 Sarjana Terapan (Golongan III/a).",
                  font_size=9.5, space_after=4, bold_color=ORANGE_ACC)
    add_bullet_v2(tf20_2, "PSDKU Gayo Lues (25,4%):", "783 kursi mubazir dari 1.050 kuota (5 tahun). 74,6% bangku kosong melompong!\n→ Rekomendasi: Pangkas kuota 50% + Wajibkan MoU beasiswa Pemkab.",
                  font_size=9.5, space_after=2, bold_color=ALERT_RED)

    add_footer(s20, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Pareto + D3/PSDKU (Two-Card Balanced Layout)")

    # =================================================================
    # SLIDE 21: SECTION DIVIDER — REKOMENDASI STRATEGIS
    # =================================================================
    sn += 1
    add_section_divider(prs, blank, 4, "Rekomendasi Kebijakan Strategis", sn, TOTAL)
    print(f"  [OK] Slide {sn}: Section Divider 04")

    # =================================================================
    # SLIDE 22: 6 REKOMENDASI KEBIJAKAN
    # =================================================================
    sn += 1
    s22 = prs.slides.add_slide(blank)
    create_header_v2(s22, "6 Rekomendasi Kebijakan Terintegrasi Menuju PMB 2027 yang Efisien & Berkeadilan")

    # 3x2 grid
    cw22 = Inches(3.75)
    ch22 = Inches(2.4)
    gap_x = Inches(0.2)
    gap_y = Inches(0.15)
    y1 = CONTENT_TOP
    y2 = CONTENT_TOP + ch22 + gap_y

    recs = [
        ("AKSI 1:\nRASIONALISASI KUOTA", ALERT_RED,
         "Pangkas 20–40% pada 22 prodi Kuadran III. Budidaya Perairan 160→90, THP 160→100, Pend. Ekonomi 160→100, T. Kimia 180→120, Fisika 80→50.",
         "Hapus ~450 kursi kosong semu tanpa kehilangan mahasiswa riil."),
        ("AKSI 2:\nUKT PENYELAMAT DESIL 5&6", ORANGE_ACC,
         "SK Rektor: Pelamar KIP SNBT Desil 5-6 yang tidak tertampung APBN otomatis ditetapkan UKT Kel.1 (Rp500rb) atau Kel.2 (Rp1jt) semester 1.",
         "Menyelamatkan 300+ calon mahasiswa berprestasi UTBK."),
        ("AKSI 3:\nSUBSIDI SILANG IPI", ROYAL_BLUE,
         "Alokasikan 5% dari total penerimaan IPI Mandiri Kuadran I (~Rp2,0 Miliar) untuk KIP Kemitraan PTN-BH USK.",
         "Mendanai 833 beasiswa mandiri bagi mahasiswa prasejahtera Kuadran III."),
        ("AKSI 4:\nFINANCIAL ENGINEERING KD.IV", TEAL,
         "Cicilan IPI 3 Tahap (50%-25%-25%). Fast-Track Auto-Call cadangan 48 jam. Commitment Fee Rp1jt untuk TALENTA.",
         "Menyelamatkan penerimaan Rp4,5–6,0 Miliar/tahun yang selama ini hilang."),
        ("AKSI 5:\nSINKRONISASI KIP × DT SNBT", RGBColor(139, 92, 246),
         "Kuota kelulusan SNBT pada prodi Kuadran III disinkronkan dengan sisa kuota definitif KIP-K pasca-SNBP.",
         "Mencegah over-promising kelulusan pada prodi padat KIP."),
        ("AKSI 6:\nSINERGI BAITUL MAL & OTSUS", SUCCESS_GRN,
         "Ajukan daftar 526 calon mahasiswa Desil 5-6 kepada Baitul Mal Aceh & Pemprov sebagai mustahik Fisabilillah.",
         "Mengintegrasikan dana otonomi daerah dengan misi pengentasan kemiskinan via pendidikan tinggi."),
    ]

    positions = [
        (MARGIN_L, y1), (MARGIN_L + cw22 + gap_x, y1), (MARGIN_L + 2*(cw22 + gap_x), y1),
        (MARGIN_L, y2), (MARGIN_L + cw22 + gap_x, y2), (MARGIN_L + 2*(cw22 + gap_x), y2),
    ]

    for i, (title, color, desc, result) in enumerate(recs):
        x, y = positions[i]
        _, tf_r = add_card_v2(s22, x, y, cw22, ch22)
        p_t = tf_r.paragraphs[0]
        p_t.text = title
        p_t.font.bold = True
        p_t.font.size = Pt(10)
        p_t.font.color.rgb = color
        p_t.space_after = Pt(5)
        add_bullet_v2(tf_r, "", desc, font_size=9, space_after=4)
        add_bullet_v2(tf_r, "Hasil:", result, font_size=9, space_after=2, bold_color=color)

    add_footer(s22, sn, TOTAL)
    print(f"  [OK] Slide {sn}: 6 Rekomendasi")

    # =================================================================
    # SLIDE 23: RESTRUKTURISASI FEB + D3 + PSDKU
    # =================================================================
    sn += 1
    s23 = prs.slides.add_slide(blank)
    create_header_v2(s23, "Agenda Transformasi: Restrukturisasi FEB, Konversi D3→D4, dan Rasionalisasi PSDKU")

    # Three-column cards
    cw23 = Inches(3.75)
    ch23 = Inches(5.0)

    # FEB
    _, tf23_1 = add_card_v2(s23, MARGIN_L, CONTENT_TOP, cw23, ch23,
                             bg_color=RGBColor(254, 242, 242), border_color=RGBColor(254, 202, 202))
    add_card_title(tf23_1, "⚠️ ALARM SENAT FEB", DEEP_RED, 12)
    add_bullet_v2(tf23_1, "Fakta Krisis:", "3 prodi utama (Manajemen, Eko Islam, Eko Pembangunan) kehilangan 144 mhs/angkatan (-24% dari basis 2022).", font_size=10, space_after=5)
    add_bullet_v2(tf23_1, "Zero-Rebound:", "Manajemen & Eko Islam tidak pernah sekalipun naik dalam 4 transisi tahunan!", font_size=10, space_after=5, bold_color=DEEP_RED)
    add_bullet_v2(tf23_1, "Kanibalisasi:", "S1 Bisnis Digital (baru 2024) menyedot 800+ peminat langsung dari Manajemen.", font_size=10, space_after=6)
    add_bullet_v2(tf23_1, "Rekomendasi:", "Re-engineering kurikulum → Digital Marketing, Business Analytics, Islamic FinTech untuk membalikkan tren peminat Gen Z.",
                  font_size=10, space_after=3, bold_color=ORANGE_ACC)

    # D3→D4
    _, tf23_2 = add_card_v2(s23, Inches(4.75), CONTENT_TOP, cw23, ch23,
                             bg_color=RGBColor(240, 253, 244), border_color=RGBColor(187, 247, 208))
    add_card_title(tf23_2, "🔄 KONVERSI D3 → D4", SUCCESS_GRN, 12)
    add_bullet_v2(tf23_2, "Akar Masalah:", "Lulusan D3 = Golongan II/c ASN, kalah dari D4/S1 = Golongan III/a. Kurikulum D3 hanya 'versi ringkas' S1 tanpa sertifikasi industri.", font_size=10, space_after=5)
    add_bullet_v2(tf23_2, "Target Konversi:", "• D3 Manajemen Informatika → D4 Sains Data Terapan\n• D3 Teknik Sipil → D4 Manajemen Rekayasa Konstruksi\n• D3 Akuntansi → D4 Akuntansi Sektor Publik", font_size=10, space_after=5)
    add_bullet_v2(tf23_2, "Moratorium:", "D3 Manajemen Agribisnis (keterisian 36,8%) dan D3 Budidaya Peternakan (32,0%).", font_size=10, space_after=5, bold_color=ALERT_RED)
    add_bullet_v2(tf23_2, "Kurikulum Dual System:", "Magang industri 1 tahun penuh + sertifikasi kompetensi BNSP.", font_size=10, space_after=3)

    # PSDKU
    _, tf23_3 = add_card_v2(s23, Inches(8.7), CONTENT_TOP, cw23, ch23,
                             bg_color=RGBColor(255, 247, 237), border_color=RGBColor(253, 230, 138))
    add_card_title(tf23_3, "📍 RASIONALISASI PSDKU", ORANGE_ACC, 12)
    add_bullet_v2(tf23_3, "Fakta Inefisiensi:", "5 tahun: 1.050 kursi dibuka, hanya 267 mahasiswa masuk. 783 kursi (74,6%) terbuang sia-sia.", font_size=10, space_after=5)
    add_bullet_v2(tf23_3, "Kendala Geografis:", "Blangkejeren berjarak 10–12 jam darat dari Banda Aceh/Medan. Isolated dari pasar pendaftar nasional.", font_size=10, space_after=5)
    add_bullet_v2(tf23_3, "Downsizing 50%:", "Pangkas dari 220 → 100–110 kursi/tahun (rata-rata 25/prodi).", font_size=10, space_after=5, bold_color=ALERT_RED)
    add_bullet_v2(tf23_3, "MoU Pemkab:", "Ikat kuota dengan beasiswa penuh APBD Gayo Lues / Aceh Tenggara.", font_size=10, space_after=3)
    add_bullet_v2(tf23_3, "Fokus Niche Lokal:", "Kurikulum Agribisnis Kopi Gayo & Konservasi Ekosistem Leuser.", font_size=10, space_after=2)

    add_footer(s23, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Transformasi FEB/D3/PSDKU")

    # =================================================================
    # SLIDE 24: CLOSING / PESAN KUNCI PIMPINAN
    # =================================================================
    sn += 1
    s24 = prs.slides.add_slide(blank)
    add_bg(s24, NAVY)

    # Quote area
    q_box = s24.shapes.add_textbox(Inches(1.2), Inches(0.6), Inches(10.9), Inches(2.5))
    q_tf = q_box.text_frame
    q_tf.word_wrap = True

    p_qt0 = q_tf.paragraphs[0]
    p_qt0.text = "UNIVERSITAS SYIAH KUALA  |  PESAN KUNCI PIMPINAN"
    p_qt0.font.size = Pt(11)
    p_qt0.font.bold = True
    p_qt0.font.color.rgb = GOLD
    p_qt0.alignment = PP_ALIGN.CENTER
    p_qt0.space_after = Pt(14)

    p_qt = q_tf.add_paragraph()
    p_qt.text = "\"Tolak ukur keberhasilan PMB PTN-BH bukanlah seberapa besar daya tampung yang kita umumkan di atas kertas, melainkan seberapa presisi kuota tersebut terisi oleh mahasiswa yang nyata, berdaya beli, atau terlindungi beasiswanya hingga lulus tepat waktu.\""
    p_qt.font.size = Pt(16)
    p_qt.font.italic = True
    p_qt.font.bold = True
    p_qt.font.color.rgb = WHITE
    p_qt.alignment = PP_ALIGN.CENTER

    # Gold line
    add_gold_line(s24, Inches(3.35), left=Inches(4.0), width=Inches(5.3))

    # 3 Takeaway cards
    col_w24 = Inches(3.45)
    y24 = Inches(3.65)
    h24 = Inches(3.1)

    _, t24_1 = add_card_v2(s24, Inches(1.2), y24, col_w24, h24,
                            bg_color=RGBColor(20, 42, 80), border_color=RGBColor(60, 80, 120))
    add_card_title(t24_1, "1. AUDIT DATA MEMBUKTIKAN", GOLD, 12)
    add_bullet_v2(t24_1, "Bukan Masalah Minat:", "Kebocoran SNBT = keterbatasan kuota beasiswa (cutoff Desil 5-6), bukan ketidakmampuan universitas menarik peminat.",
                  font_size=10.5, space_after=5, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))
    add_bullet_v2(t24_1, "Kausalitas 97,6%:", "Siswa yang gugur adalah anak prasejahtera terhempas ketiadaan beasiswa.",
                  font_size=10.5, space_after=3, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))

    _, t24_2 = add_card_v2(s24, Inches(4.94), y24, col_w24, h24,
                            bg_color=RGBColor(20, 42, 80), border_color=RGBColor(60, 80, 120))
    add_card_title(t24_2, "2. EFISIENSI MENYELAMATKAN AKREDITASI", ORANGE_ACC, 12)
    add_bullet_v2(t24_2, "Hapus Bangku Semu:", "Rasionalisasi kuota Kuadran III = penyehatan mutu akademik, bukan pelemahan fakultas.",
                  font_size=10.5, space_after=5, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))
    add_bullet_v2(t24_2, "Rasio Optimal:", "Kapasitas yang pas menjaga rasio dosen-mahasiswa dan instrumen akreditasi unggul internasional.",
                  font_size=10.5, space_after=3, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))

    _, t24_3 = add_card_v2(s24, Inches(8.68), y24, col_w24, h24,
                            bg_color=RGBColor(20, 42, 80), border_color=RGBColor(60, 80, 120))
    add_card_title(t24_3, "3. KEBERPIHAKAN SOSIAL PTN-BH", SUCCESS_GRN, 12)
    add_bullet_v2(t24_3, "Kemandirian Berkeadilan:", "Fleksibilitas finansial PTN-BH harus menjadi berkah bagi mahasiswa prasejahtera melalui subsidi silang IPI mandiri.",
                  font_size=10.5, space_after=5, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))
    add_bullet_v2(t24_3, "Jantong Hate Rakyat Aceh:", "Menjaga marwah USK sebagai benteng kesempatan pendidikan tinggi bagi seluruh lapisan masyarakat Aceh.",
                  font_size=10.5, space_after=3, bold_color=WARM_WHITE, norm_color=RGBColor(180, 190, 210))

    add_footer(s24, sn, TOTAL)
    print(f"  [OK] Slide {sn}: Closing")

    # =================================================================
    # SAVE
    # =================================================================
    prs.save(out_pptx)
    print(f"\n{'='*70}")
    print(f"  [SUCCESS] Built {sn}-slide corporate presentation:")
    print(f"  {out_pptx}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
