import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.colors as mcolors
from matplotlib.patches import Patch

plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

def main():
    base_dir = "/Users/auliamuzhaffar/Documents/maganghub"
    excel_path = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "data", "master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx")
    chart_dir = os.path.join(base_dir, "tugas-5", "analisa_peminatan_dan_daya_tampung", "grafik")
    os.makedirs(chart_dir, exist_ok=True)

    print("Loading data from Excel...")
    df_master = pd.read_excel(excel_path, sheet_name="Master_Semua_Prodi")
    df_s1 = pd.read_excel(excel_path, sheet_name="S1_Kampus_Utama")
    df_d3 = pd.read_excel(excel_path, sheet_name="Diploma_3_Vokasi")
    df_psdku = pd.read_excel(excel_path, sheet_name="PSDKU_Gayo_Lues")
    df_jalur = pd.read_excel(excel_path, sheet_name="Rincian_Jalur_Masuk_2026")
    df_jalur_all = pd.read_excel(excel_path, sheet_name="Rincian_Jalur_Semua_Tahun")

    def normalize_cols(df):
        rev_map = {
            "Nama Program Studi": "Program_Studi",
            "Klaster Analisis": "Segmen_Analisis",
            "Jalur Masuk Standar": "Jalur_Penerimaan",
            "Jalur Penerimaan": "Jalur_Penerimaan",
            "Nama Jalur di Dokumen": "Nama_Asli_Jalur",
            "Jumlah Peminat": "Peminat",
            "Target Daya Tampung": "Daya_Tampung",
            "Calon Lulus Seleksi": "Lulus_Seleksi",
            "Mahasiswa Daftar Ulang": "Daftar_Ulang",
            "Mundur / Gugur": "Tidak_Daftar_Ulang",
            "Klasifikasi Tren Resmi": "Kategori_Tren"
        }
        for yr in [2022, 2023, 2024, 2025, 2026]:
            rev_map[f"Peminat {yr}"] = f"Peminat_{yr}"
            rev_map[f"Daya Tampung {yr}"] = f"DT_{yr}"
            rev_map[f"Lulus Seleksi {yr}"] = f"LA_{yr}"
            rev_map[f"Daftar Ulang {yr}"] = f"DU_{yr}"
            rev_map[f"Mundur/Gugur {yr}"] = f"Gugur_{yr}"
            rev_map[f"Keketatan {yr}"] = f"Keketatan_{yr}"
            rev_map[f"Fill Rate {yr} (%)"] = f"FillRate_{yr}_Persen"
            rev_map[f"Yield Rate {yr} (%)"] = f"YieldRate_{yr}_Persen"
            rev_map[f"Kursi Kosong {yr}"] = f"Sisa_Kosong_{yr}"
        for pair in ["22_23", "23_24", "24_25", "25_26"]:
            p_dash = pair.replace("_", "-")
            rev_map[f"YoY DU {p_dash} (%)"] = f"YoY_DU_{pair}"
            rev_map[f"YoY Peminat {p_dash} (%)"] = f"YoY_Peminat_{pair}"
        rev_map["Slope DU (Orang/Thn)"] = "Slope_Tren_DU_Orang_Thn"
        rev_map["R² Stabilitas DU"] = "R2_Stabilitas_DU"
        rev_map["Slope Peminat (Orang/Thn)"] = "Slope_Tren_Peminat_Orang_Thn"
        rev_map["R² Stabilitas Peminat"] = "R2_Stabilitas_Peminat"
        rev_map["CAGR DU (%)"] = "CAGR_DU_Persen"
        rev_map["CAGR DT (%)"] = "CAGR_DT_Persen"
        rev_map["CAGR Peminat (%)"] = "CAGR_Peminat_Persen"
        rev_map["Marginal Fill Rate"] = "Marginal_Fill_Rate"
        rev_map["Rata Peminat 5-Thn"] = "Rata_Peminat_5Thn"
        rev_map["Rata DT 5-Thn"] = "Rata_DT_5Thn"
        rev_map["Rata DU 5-Thn"] = "Rata_DU_5Thn"
        rev_map["Rata Fill Rate 5-Thn (%)"] = "Rata_FillRate_5Thn_Persen"
        rev_map["Rata Keketatan 5-Thn"] = "Rata_Keketatan_5Thn"
        return df.rename(columns=rev_map)

    df_master = normalize_cols(df_master)
    df_s1 = normalize_cols(df_s1)
    df_d3 = normalize_cols(df_d3)
    df_psdku = normalize_cols(df_psdku)
    df_jalur = normalize_cols(df_jalur)
    df_jalur_all = normalize_cols(df_jalur_all)

    def clean_name(p, f):
        fak_map = {
            'MIPA': 'FMIPA',
            'Ekonomi dan Bisnis': 'FEB',
            'Kedokteran': 'FK',
            'Kedokteran Gigi': 'FKG',
            'Teknik': 'FT',
            'FKIP': 'FKIP',
            'Pertanian': 'FP',
            'Kelautan dan Perikanan': 'FPK',
            'Keperawatan': 'FKEP',
            'Hukum': 'FH',
            'Kedokteran Hewan': 'FKH',
            'ISIP': 'FISIP'
        }
        short_fak = fak_map.get(str(f).strip(), str(f).strip())
        p_title = str(p).strip().title()
        p_title = p_title.replace('Psp', 'PSP').replace('Tsda', 'TSDA').replace('Fkip', 'FKIP').replace('Pgsd', 'PGSD').replace('Pkk', 'PKK')
        return f"{p_title} ({short_fak})"

    years = [2022, 2023, 2024, 2025, 2026]

    # -------------------------------------------------------------
    # CHART 1: TREN MAKRO 5 TAHUN USK
    # -------------------------------------------------------------
    print("[1/9] Generating 01_tren_makro_peminat_dt_du_usk.png...")
    tot_pm = [df_master[f"Peminat_{yr}"].sum() for yr in years]
    tot_dt = [df_master[f"DT_{yr}"].sum() for yr in years]
    tot_du = [df_master[f"DU_{yr}"].sum() for yr in years]
    fill_rates = [tot_du[i] / tot_dt[i] * 100.0 for i in range(5)]

    fig, ax1 = plt.subplots(figsize=(12, 6.5), dpi=300)
    ax2 = ax1.twinx()

    x = np.arange(len(years))
    w = 0.25

    b1 = ax1.bar(x - w, [p / 1000.0 for p in tot_pm], width=w, label="Total Peminat (Ribu Orang)", color="#4A90E2", alpha=0.85)
    b2 = ax1.bar(x, [d / 1000.0 for d in tot_dt], width=w, label="Daya Tampung (Ribu Kursi)", color="#F5A623", alpha=0.9)
    b3 = ax1.bar(x + w, [u / 1000.0 for u in tot_du], width=w, label="Daftar Ulang Riil (Ribu Mhs)", color="#2ECC71", alpha=0.9)

    line = ax2.plot(x, fill_rates, color="#D0021B", marker="o", linewidth=2.5, markersize=8, label="Tingkat Keterisian Kuota (Fill Rate %)")

    for i in range(len(years)):
        gap = tot_dt[i] - tot_du[i]
        ax1.annotate(f"{tot_pm[i]:,}\npeminat", (x[i] - w, tot_pm[i]/1000.0 + 0.5), ha='center', fontsize=8, color="#2C3E50")
        ax1.annotate(f"{tot_dt[i]:,}\nkuota", (x[i], tot_dt[i]/1000.0 + 0.5), ha='center', fontsize=8, color="#B7791F")
        ax1.annotate(f"{tot_du[i]:,}\nmasuk", (x[i] + w, tot_du[i]/1000.0 + 0.5), ha='center', fontsize=8, color="#1E824C", fontweight='bold')
        ax2.annotate(f"{fill_rates[i]:.1f}%\n({gap:,} kosong)", (x[i], fill_rates[i] + 1.2), ha='center', fontsize=9, color="#900C3F", fontweight='bold')

    ax1.set_xlabel("Tahun Akademik", fontweight='bold', labelpad=10)
    ax1.set_ylabel("Jumlah Peminat & Kuota (Ribu Orang)", fontweight='bold', labelpad=10)
    ax2.set_ylabel("Tingkat Keterisian Kuota (Fill Rate %)", fontweight='bold', color="#D0021B", labelpad=10)
    ax1.set_xticks(x)
    ax1.set_xticklabels([str(y) for y in years], fontweight='bold')
    ax1.set_ylim(0, max(tot_pm)/1000.0 * 1.25)
    ax2.set_ylim(50, 100)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left", framealpha=0.9)

    plt.title("Evaluasi Tren Makro Universitas Syiah Kuala (2022–2026)\nPeminat, Daya Tampung, Daftar Ulang, dan Keterisian Kuota", fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(chart_dir, "01_tren_makro_peminat_dt_du_usk.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 2: TOP TREN PENINGKATAN DAFTAR ULANG & PEMINAT
    # -------------------------------------------------------------
    print("[2/9] Generating 02_top_tren_peningkatan_pendaftar_dan_peminat.png...")
    # Filter S1 that have complete 5-year data
    df_s1_growth = df_s1[(df_s1["DU_2022"] > 0) & (df_s1["CAGR_DU_Persen"] > 10.0)].copy()
    df_s1_growth = df_s1_growth.sort_values(by="Slope_Tren_DU_Orang_Thn", ascending=False).head(6)

    fig, ax = plt.subplots(figsize=(16, 9.2), dpi=300)
    colors = ["#0284C7", "#7C3AED", "#059669", "#D97706", "#DC2626", "#0D9488"]
    markers = ['o', 's', '^', 'D', 'v', 'P']
    
    offsets_map = {
        0: [(0, 13), (0, -15), (0, 13), (0, 13), (0, 13)],     # Keperawatan
        1: [(0, 13), (0, 13), (0, 13), (0, 13), (0, 13)],       # Teknik Sipil
        2: [(-15, 12), (-15, 12), (0, 13), (0, 13), (0, 13)],   # PGSD
        3: [(15, -13), (-15, -14), (0, 13), (0, -14), (0, -14)],# Penjaskesrek
        4: [(0, -14), (15, -14), (16, 8), (0, 13), (0, 13)],    # PKK
        5: [(0, -14), (0, -14), (0, -15), (0, -14), (0, -14)]   # Pend. B. Indonesia
    }

    ax.set_xlim(2021.65, 2027.1)
    ax.set_ylim(40, 340)
    ax.grid(True, linestyle="--", alpha=0.45, color="#CBD5E1")

    for idx, (_, row) in enumerate(df_s1_growth.iterrows()):
        y_series = [row[f"DU_{yr}"] for yr in years]
        c = colors[idx % len(colors)]
        m = markers[idx % len(markers)]
        lbl = f"{row['Program_Studi']}\nSlope: +{row['Slope_Tren_DU_Orang_Thn']} mhs/thn | CAGR: +{row['CAGR_DU_Persen']}%"
        
        ax.plot(years, y_series, marker=m, linewidth=3.0, markersize=8.5,
                color=c, markeredgecolor='white', markeredgewidth=2.0, alpha=0.95, label=lbl)
        
        # Label every point with clean contrasting pill
        offsets = offsets_map.get(idx, [(0, 12)] * 5)
        for yr, val, (ox, oy) in zip(years, y_series, offsets):
            ax.annotate(f"{int(val)}", xy=(yr, val), xytext=(ox, oy), textcoords='offset points',
                        ha='center', va='center', fontsize=9.2, fontweight='bold', color=c,
                        bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFFFFF', edgecolor=c, alpha=0.95, linewidth=1.0))

        # End-of-line summary badge
        growth_pct = (y_series[-1] - y_series[0]) / y_series[0] * 100
        ax.annotate(f"  {int(y_series[-1])} mhs (+{growth_pct:.0f}%)", xy=(2026, y_series[-1]), xytext=(10, 0),
                    textcoords='offset points', va='center', ha='left', fontsize=10, fontweight='bold', color=c)

    ax.set_xticks(years)
    ax.set_xticklabels(['2022', '2023', '2024', '2025', '2026'], fontsize=11.5, fontweight='bold', color='#1E293B')
    ax.tick_params(axis='y', labelsize=10.5, labelcolor='#1E293B')
    ax.set_xlabel("Tahun Akademik Penerimaan", fontsize=12, fontweight='bold', labelpad=12, color='#0F172A')
    ax.set_ylabel("Jumlah Mahasiswa Baru Daftar Ulang (Orang)", fontsize=12, fontweight='bold', labelpad=12, color='#0F172A')
    ax.set_title("TREN PERTUMBUHAN PROGRAM STUDI S1 DENGAN PENINGKATAN TERTINGGI (2022–2026)\nEvaluasi Berdasarkan Slope Regresi Linier OLS (Pertambahan Mahasiswa/Tahun) & Laju CAGR Majemuk", 
                 fontsize=13.5, fontweight='bold', pad=22, color='#0F172A')

    legend = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=True, 
                       fontsize=9.2, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.98, 
                       columnspacing=2.0, labelspacing=0.8, handlelength=2.5, handletextpad=0.8)
    legend.get_frame().set_linewidth(1.2)

    plt.tight_layout(rect=[0.02, 0.10, 0.98, 0.96])
    plt.savefig(os.path.join(chart_dir, "02_top_tren_peningkatan_pendaftar_dan_peminat.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 3: TOP TREN PENURUNAN DAFTAR ULANG
    # -------------------------------------------------------------
    print("[3/9] Generating 03_top_tren_penurunan_pendaftar_dan_peminat.png...")
    df_s1_decline = df_s1[(df_s1["DU_2022"] > 0) & (df_s1["CAGR_DU_Persen"] < 0)].copy()
    df_s1_decline = df_s1_decline.sort_values(by="Slope_Tren_DU_Orang_Thn", ascending=True).head(6)

    fig, ax = plt.subplots(figsize=(13, 7), dpi=300)
    decline_colors = ["#C0392B", "#E67E22", "#D35400", "#8E44AD", "#2C3E50", "#16A085"]

    for idx, (_, row) in enumerate(df_s1_decline.iterrows()):
        y_series = [row[f"DU_{yr}"] for yr in years]
        lbl = f"{row['Program_Studi']} (Slope: {row['Slope_Tren_DU_Orang_Thn']} mhs/thn | CAGR: {row['CAGR_DU_Persen']}%)"
        ax.plot(years, y_series, marker='s', linewidth=2.5, markersize=7, color=decline_colors[idx % len(decline_colors)], label=lbl)
        ax.annotate(f"{int(y_series[-1])} mhs", (years[-1] + 0.05, y_series[-1]), va='center', fontsize=9, fontweight='bold', color=decline_colors[idx % len(decline_colors)])

    ax.set_xlabel("Tahun Akademik", fontweight='bold', labelpad=10)
    ax.set_ylabel("Jumlah Mahasiswa Daftar Ulang (Orang)", fontweight='bold', labelpad=10)
    ax.set_title("Program Studi S1 Kampus Utama yang Mengalami Penurunan Pendaftaran Ulang\n(Berdasarkan Slope Negatif dan Kontraksi Berkelanjutan 2022–2026)", fontsize=13, fontweight='bold', pad=15)
    ax.set_xticks(years)
    ax.set_xlim(2021.8, 2026.6)
    ax.grid(True, linestyle="--", alpha=0.5)
    ax.legend(loc="upper right", framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    plt.savefig(os.path.join(chart_dir, "03_top_tren_penurunan_pendaftar_dan_peminat.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 4: RASIO KEKETATAN PEMINATAN (PEMINAT / DT)
    # -------------------------------------------------------------
    print("[4/9] Generating 04_rasio_keketatan_peminatan_vs_daya_tampung.png...")
    top_ketat = df_s1.sort_values(by="Keketatan_2026", ascending=False).head(8).reset_index(drop=True)
    low_ketat = df_s1[df_s1["DT_2026"] > 0].sort_values(by="Keketatan_2026", ascending=True).head(8).reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(19, 8.8), dpi=300)

    # Panel 1: Top 8 Favorit & Ketat
    y_pos1 = np.arange(len(top_ketat))
    bars1 = ax1.barh(y_pos1, top_ketat["Keketatan_2026"], color='#1E40AF', alpha=0.9, height=0.58, edgecolor='#1E3A8A', linewidth=1.2, zorder=2)
    ax1.set_yticks(y_pos1)
    labels1 = [clean_name(r['Program_Studi'], r['Fakultas']) for _, r in top_ketat.iterrows()]
    ax1.set_yticklabels(labels1, fontsize=10, fontweight='bold', color='#1E293B')
    ax1.invert_yaxis()
    ax1.set_xlabel('Rasio Keketatan Seleksi (Peminat per 1 Kursi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax1.set_title('A. Top 8 Program Studi Paling Favorit & Ketat (Tahun 2026)', fontsize=12.5, fontweight='bold', pad=15, color='#1E40AF')
    ax1.set_xlim(0, 56)
    ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#94A3B8')
    ax1.spines['bottom'].set_color('#94A3B8')
    line_ref1 = ax1.axvline(10.0, color='#16A34A', linestyle='--', linewidth=1.6, alpha=0.85, zorder=1, label='Batas Sangat Ketat (10 : 1)')

    for i, r in top_ketat.iterrows():
        val = r['Keketatan_2026']
        pem = int(r['Peminat_2026'])
        dt = int(r['DT_2026'])
        ax1.annotate(f"{val:.1f} : 1", xy=(val, i), xytext=(8, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=9.2, fontweight='bold', color='#1E3A8A',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.0), zorder=4)
        ax1.annotate(f"({pem:,} peminat | {dt} kuota)", xy=(val, i), xytext=(60, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=8.8, color='#475569', zorder=4)

    # Panel 2: Bottom 8 Sepi Peminat
    y_pos2 = np.arange(len(low_ketat))
    colors_bot = ['#991B1B' if r['Keketatan_2026'] < 1.0 else '#DC2626' if r['Keketatan_2026'] < 1.5 else '#EA580C' for _, r in low_ketat.iterrows()]
    bars2 = ax2.barh(y_pos2, low_ketat["Keketatan_2026"], color=colors_bot, alpha=0.88, height=0.58, edgecolor='#7F1D1D', linewidth=1.2, zorder=2)
    ax2.set_yticks(y_pos2)
    labels2 = [clean_name(r['Program_Studi'], r['Fakultas']) for _, r in low_ketat.iterrows()]
    ax2.set_yticklabels(labels2, fontsize=10, fontweight='bold', color='#1E293B')
    ax2.invert_yaxis()
    ax2.set_xlabel('Rasio Keketatan Seleksi (Peminat per 1 Kursi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax2.set_title('B. Top 8 Program Studi Paling Sepi Peminat (Tahun 2026)', fontsize=12.5, fontweight='bold', pad=15, color='#991B1B')
    ax2.set_xlim(0, 3.8)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#94A3B8')
    ax2.spines['bottom'].set_color('#94A3B8')
    line_ref2 = ax2.axvline(1.0, color='#7F1D1D', linestyle='-', linewidth=2.4, zorder=1, label='Garis Kritis Mutlak 1,0 : 1 (Peminat < Kuota)')
    line_ref3 = ax2.axvline(1.5, color='#DC2626', linestyle='--', linewidth=1.8, zorder=1, label='Batas Minimal BAN-PT (1,5 : 1)')

    for i, r in low_ketat.iterrows():
        val = r['Keketatan_2026']
        pem = int(r['Peminat_2026'])
        dt = int(r['DT_2026'])
        is_kritis = val < 1.0
        bg_col = '#FEF2F2' if is_kritis else '#FFF7ED'
        border_col = '#EF4444' if is_kritis else '#F97316'
        txt_col = '#991B1B' if is_kritis else '#C2410C'
        status = 'KRITIS' if is_kritis else 'SEPI'
        ax2.annotate(f"{val:.2f} : 1", xy=(val, i), xytext=(8, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=9.2, fontweight='bold', color=txt_col,
                     bbox=dict(boxstyle='round,pad=0.25', facecolor=bg_col, edgecolor=border_col, linewidth=1.0), zorder=4)
        ax2.annotate(f"({pem} peminat vs {dt} kuota - {status})", xy=(val, i), xytext=(58, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=8.8, fontweight='bold' if is_kritis else 'normal', color=txt_col,
                     bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor='none', alpha=0.9), zorder=4)

    handles = [bars1, line_ref1, line_ref2, line_ref3]
    labels = [
        'Rasio Seleksi 2026',
        'Batas Sangat Ketat (10 : 1)',
        'Garis Kritis Mutlak (1,0 : 1)',
        'Batas Minimal BAN-PT (1,5 : 1)'
    ]
    fig.legend(handles, labels, loc='lower center', bbox_to_anchor=(0.5, 0.015), ncol=4, frameon=True,
               fontsize=9.8, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.98)

    plt.suptitle('PETA TINGKAT KEKETATAN SELEKSI PROGRAM STUDI S1 USK (TAHUN 2026)\nRasio Persaingan Calon Mahasiswa (Peminat per 1 Kursi Daya Tampung)', 
                 fontsize=14, fontweight='bold', y=0.98, color='#0F172A')
    plt.tight_layout(rect=[0.01, 0.07, 0.99, 0.93])
    plt.savefig(os.path.join(chart_dir, "04_rasio_keketatan_peminatan_vs_daya_tampung.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 5: OVER-EKSPANSI KUOTA VS DAFTAR ULANG
    # -------------------------------------------------------------
    print("[5/9] Generating 05_over_ekspansi_kuota_vs_daftar_ulang_riil.png...")
    prodi_map_05 = {
        'BUDIDAYA PERAIRAN': {'fak': 'FPK', 'label': 'Budidaya Perairan (FPK)', 'status': 'Gagal Total (MFR: 0,00)'},
        'TEKNOLOGI HASIL PERTANIAN': {'fak': 'FP', 'label': 'Teknologi Hasil Pertanian (FP)', 'status': 'Over-Ekspansi Parsial (MFR: 0,62)'},
        'PENDIDIKAN EKONOMI': {'fak': 'FKIP', 'label': 'Pendidikan Ekonomi (FKIP)', 'status': 'Over-Ekspansi Berat (MFR: 0,40)'},
        'TEKNIK KIMIA': {'fak': 'FT', 'label': 'Teknik Kimia (FT)', 'status': 'Over-Ekspansi Parsial (MFR: 0,60)'}
    }
    order_05 = ['BUDIDAYA PERAIRAN', 'TEKNOLOGI HASIL PERTANIAN', 'PENDIDIKAN EKONOMI', 'TEKNIK KIMIA']

    fig, axes = plt.subplots(2, 2, figsize=(18.5, 11.2), dpi=300)
    axes = axes.flatten()

    l1_05, l2_05 = None, None
    for i, p_name in enumerate(order_05):
        row = df_s1[df_s1["Program_Studi"] == p_name].iloc[0]
        ax = axes[i]
        info = prodi_map_05[p_name]

        dt_s = [int(row[f"DT_{yr}"]) for yr in years]
        du_s = [int(row[f"DU_{yr}"]) for yr in years]
        gap_26 = int(row["Sisa_Kosong_2026"])
        fill_val = float(row["FillRate_2026_Persen"])
        fill_str = f"{fill_val:.1f}".replace('.', ',')

        # Shaded area
        ax.fill_between(years, du_s, dt_s, color='#FCA5A5', alpha=0.32, zorder=1)

        # Plot lines
        l1_05, = ax.plot(years, dt_s, color='#1E3A8A', linewidth=2.8, marker='s', markersize=8.5,
                         markerfacecolor='#1E3A8A', markeredgecolor='#0F172A', markeredgewidth=1.2,
                         label='Target Kuota (Daya Tampung)', zorder=3)
        l2_05, = ax.plot(years, du_s, color='#0D9488', linewidth=2.8, marker='o', markersize=8.5,
                         markerfacecolor='#0D9488', markeredgecolor='#042F2E', markeredgewidth=1.2,
                         label='Realisasi Masuk (Daftar Ulang)', zorder=3)

        # Annotate points for each year
        for yr_idx, yr in enumerate(years):
            dt_val = dt_s[yr_idx]
            du_val = du_s[yr_idx]

            # DT label (above)
            ax.annotate(f"{dt_val}", xy=(yr, dt_val), xytext=(0, 9), textcoords='offset points',
                        ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#1E3A8A',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='#EFF6FF', edgecolor='#93C5FD', linewidth=0.9, alpha=0.95), zorder=4)

            # DU label (below)
            ax.annotate(f"{du_val}", xy=(yr, du_val), xytext=(0, -15), textcoords='offset points',
                        ha='center', va='top', fontsize=9.2, fontweight='bold', color='#0F766E',
                        bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0FDFA', edgecolor='#99F6E4', linewidth=0.9, alpha=0.95), zorder=4)

        # 2026 Gap callout card inside shaded area
        mid_y = (dt_s[-1] + du_s[-1]) / 2.0
        ax.annotate('', xy=(2026.06, dt_s[-1]), xytext=(2026.06, du_s[-1]),
                    arrowprops=dict(arrowstyle='<->', color='#B91C1C', lw=1.8), zorder=4)
        ax.annotate(f"Defisit 2026: {gap_26} Kursi\n(Keterisian: {fill_str}%)",
                    xy=(2026.06, mid_y), xytext=(-42, 0), textcoords='offset points',
                    ha='right', va='center', fontsize=9.2, fontweight='bold', color='#991B1B',
                    bbox=dict(boxstyle='round,pad=0.32', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.2, alpha=0.96),
                    arrowprops=dict(arrowstyle='->', color='#DC2626', lw=1.2), zorder=5)

        # Subplot Titles with pill badge
        ax.set_title(f"{info['label']}  |  {info['status']}\nDefisit Terkini: {gap_26} Kursi Kosong (Keterisian {fill_str}%)",
                     fontsize=11.5, fontweight='bold', pad=12, color='#0F172A')

        ax.set_xlim(2021.65, 2026.40)
        ax.set_xticks(years)
        ax.set_xticklabels(years, fontsize=10, fontweight='bold', color='#334155')
        ax.set_xlabel('Tahun Akademik', fontsize=10, fontweight='bold', color='#475569', labelpad=6)
        ax.set_ylabel('Jumlah Mahasiswa / Kursi', fontsize=10, fontweight='bold', color='#475569', labelpad=6)

        min_val = min(min(du_s), min(dt_s))
        max_val = max(max(du_s), max(dt_s))
        y_pad = (max_val - min_val) * 0.38
        ax.set_ylim(max(0, min_val - y_pad), max_val + y_pad)

        ax.grid(True, linestyle='--', alpha=0.45, color='#CBD5E1', zorder=0)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#94A3B8')
        ax.spines['bottom'].set_color('#94A3B8')

    # Global single legend at the bottom
    from matplotlib.patches import Patch
    legend_elements_05 = [
        l1_05,
        l2_05,
        Patch(facecolor='#FCA5A5', edgecolor='#EF4444', alpha=0.45, label='Area Defisit Kursi Kosong (Kapasitas Menganggur / Idle Capacity)')
    ]
    fig.legend(legend_elements_05, [e.get_label() for e in legend_elements_05],
               loc='lower center', bbox_to_anchor=(0.5, 0.015), ncol=3, frameon=True,
               fontsize=10.5, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.98)

    plt.suptitle('FENOMENA OVER-EKSPANSI KUOTA: DAYA TAMPUNG VS REALISASI DAFTAR ULANG (2022–2026)\nBukti Empiris Kasus Penambahan Kuota Pasca PTN-BH yang Tidak Terserap Pasar dan Menimbulkan Defisit Bangku Kosong', 
                 fontsize=13.5, fontweight='bold', y=0.98, color='#0F172A')
    plt.tight_layout(rect=[0.01, 0.055, 0.99, 0.93])
    plt.savefig(os.path.join(chart_dir, "05_over_ekspansi_kuota_vs_daftar_ulang_riil.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 6: DINAMIKA JALUR MASUK & KEBOCORAN (2022–2026 TAHUNAN)
    # -------------------------------------------------------------
    print("[6/9] Generating 06_dinamika_jalur_masuk_dan_kebocoran annual charts (2022–2026)...")
    jalur_colors_map = {
        'SNBT': '#1D4ED8',      # Royal Blue
        'SNBP': '#059669',      # Emerald Green
        'SMMPTN': '#EA580C',    # Amber / Orange
        'TALENTA': '#7C3AED',   # Royal Purple
        'SMC': '#0D9488',       # Dark Teal
        'ADIK': '#64748B'       # Slate Gray
    }

    for yr in [2022, 2023, 2024, 2025, 2026]:
        df_yr = df_jalur_all[df_jalur_all['Tahun Akademik'] == yr]
        grp_yr = df_yr.groupby('Jalur_Penerimaan').agg({
            'Daftar_Ulang': 'sum',
            'Lulus_Seleksi': 'sum',
            'Tidak_Daftar_Ulang': 'sum'
        }).reset_index()

        tot_du = grp_yr['Daftar_Ulang'].sum()
        tot_gugur = grp_yr['Tidak_Daftar_Ulang'].sum()
        tot_lulus = grp_yr['Lulus_Seleksi'].sum()
        overall_yield = (tot_du / tot_lulus * 100.0) if tot_lulus > 0 else 0

        grp_yr['Share_DU'] = grp_yr['Daftar_Ulang'] / tot_du * 100.0
        grp_yr['Yield_Rate'] = grp_yr['Daftar_Ulang'] / grp_yr['Lulus_Seleksi'] * 100.0
        grp_yr = grp_yr.sort_values('Daftar_Ulang', ascending=False).reset_index(drop=True)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=300)

        # Panel 1: Kontribusi Mahasiswa Masuk Riil
        x = np.arange(len(grp_yr))
        bar_cols = [jalur_colors_map.get(j, '#3B82F6') for j in grp_yr['Jalur_Penerimaan']]
        bars1 = ax1.bar(x, grp_yr['Daftar_Ulang'], color=bar_cols, width=0.55, edgecolor='#0F172A', linewidth=1.1, zorder=2)

        ax1.set_xticks(x)
        ax1.set_xticklabels(grp_yr['Jalur_Penerimaan'], fontsize=11, fontweight='bold', color='#1E293B')
        max_du = grp_yr['Daftar_Ulang'].max()
        ax1.set_ylim(0, max_du * 1.25)
        ax1.set_ylabel('Jumlah Mahasiswa Daftar Ulang (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
        ax1.set_title(f'A. Kontribusi Mahasiswa Masuk Riil per Jalur ({yr})\nTotal Registrasi: {tot_du:,} Mahasiswa', 
                      fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
        ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        for i, r in grp_yr.iterrows():
            du_val = int(r['Daftar_Ulang'])
            share_val = r['Share_DU']
            ax1.annotate(f"{du_val:,} mhs\n({share_val:.1f}%)", xy=(i, du_val), xytext=(0, 7), textcoords='offset points',
                         ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0F172A',
                         bbox=dict(boxstyle='round,pad=0.25', facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=0.8, alpha=0.95),
                         zorder=4)

        # Panel 2: Kebocoran Calon Mahasiswa (Gugur / Mundur) & Yield Rate
        grp_leak = grp_yr.sort_values('Tidak_Daftar_Ulang', ascending=False).reset_index(drop=True)
        x2 = np.arange(len(grp_leak))
        leak_c = ['#EF4444' if r['Yield_Rate'] < 65.0 else '#F59E0B' if r['Yield_Rate'] < 80.0 else '#3B82F6' for _, r in grp_leak.iterrows()]
        bars2 = ax2.bar(x2, grp_leak['Tidak_Daftar_Ulang'], color=leak_c, alpha=0.85, width=0.55, edgecolor='#7F1D1D', linewidth=1.1, zorder=2)

        ax2.set_xticks(x2)
        ax2.set_xticklabels(grp_leak['Jalur_Penerimaan'], fontsize=11, fontweight='bold', color='#1E293B')
        max_leak = grp_leak['Tidak_Daftar_Ulang'].max()
        ax2.set_ylim(0, max_leak * 1.25)
        ax2.set_ylabel('Jumlah Calon Mahasiswa Mengundurkan Diri (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
        ax2.set_title(f'B. Tingkat Kebocoran & Konversi Pendaftaran per Jalur ({yr})\nTotal Gugur: {tot_gugur:,} Orang | Rata-rata Yield Rate: {overall_yield:.1f}%', 
                      fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
        ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        for i, r in grp_leak.iterrows():
            leak_val = int(r['Tidak_Daftar_Ulang'])
            yield_val = r['Yield_Rate']
            badge_bg = '#FEE2E2' if yield_val < 65.0 else '#FEF3C7' if yield_val < 80.0 else '#EFF6FF'
            badge_border = '#EF4444' if yield_val < 65.0 else '#F59E0B' if yield_val < 80.0 else '#3B82F6'
            txt_c = '#991B1B' if yield_val < 65.0 else '#92400E' if yield_val < 80.0 else '#1E40AF'
            
            ax2.annotate(f"{leak_val:,} gugur\n(Yield: {yield_val:.1f}%)", xy=(i, leak_val), xytext=(0, 7), textcoords='offset points',
                         ha='center', va='bottom', fontsize=10, fontweight='bold', color=txt_c,
                         bbox=dict(boxstyle='round,pad=0.25', facecolor=badge_bg, edgecolor=badge_border, linewidth=0.9, alpha=0.95),
                         zorder=4)

        plt.suptitle(f'DINAMIKA JALUR MASUK & KEBOCORAN PENERIMAAN MAHASISWA BARU USK ({yr})\nKomparasi Kontribusi Mahasiswa Masuk Riil vs Tingkat Kelulusan yang Mengundurkan Diri',
                     fontsize=14, fontweight='bold', y=0.98, color='#0F172A')
        plt.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
        out_name = f"06_dinamika_jalur_masuk_dan_kebocoran_{yr}.png"
        plt.savefig(os.path.join(chart_dir, out_name), dpi=300)
        plt.close()

    # -------------------------------------------------------------
    # CHART 7: EVALUASI KINERJA 12 FAKULTAS (DUAL PANEL)
    # -------------------------------------------------------------
    print("[7/15] Generating 07_analisa_peminatan_dan_keterisian_fakultas.png...")
    agg_dict = {
        "Peminat_2026": "sum",
        "Rata_DU_5Thn": "sum", "Rata_DT_5Thn": "sum"
    }
    for y in years:
        agg_dict[f"DT_{y}"] = "sum"
        agg_dict[f"DU_{y}"] = "sum"
        agg_dict[f"Peminat_{y}"] = "sum"
    fak_agg = df_s1.groupby("Fakultas").agg(agg_dict).reset_index()

    fak_agg["FR_2022"] = (fak_agg["DU_2022"] / fak_agg["DT_2022"] * 100.0).round(1)
    fak_agg["FR_2026"] = (fak_agg["DU_2026"] / fak_agg["DT_2026"] * 100.0).round(1)
    fak_agg["Sisa_2026"] = fak_agg["DT_2026"] - fak_agg["DU_2026"]

    fak_sorted_7 = fak_agg.sort_values("FR_2026", ascending=True).reset_index(drop=True)

    fig7, (ax7_1, ax7_2) = plt.subplots(1, 2, figsize=(23, 9.2), dpi=300, gridspec_kw={'width_ratios': [1.38, 1.0]})
    y_p7 = np.arange(len(fak_sorted_7))
    h7 = 0.38

    # Panel 1: Perbandingan Keterisian Kuota (2022 vs 2026) & Delta
    bars22 = ax7_1.barh(y_p7 - h7/2.0, fak_sorted_7["FR_2022"], height=h7, label='Tingkat Keterisian 2022 (%)', 
                        color='#94A3B8', alpha=0.85, edgecolor='#64748B', linewidth=1.0, zorder=2)
    colors_26 = ['#DC2626' if fr < 80.0 else '#2563EB' for fr in fak_sorted_7["FR_2026"]]
    bars26 = ax7_1.barh(y_p7 + h7/2.0, fak_sorted_7["FR_2026"], height=h7, label='Tingkat Keterisian 2026 (%)', 
                        color=colors_26, alpha=0.92, edgecolor='#1E3A8A', linewidth=1.1, zorder=2)

    ax7_1.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Batas Minimal Keterisian Sehat (80%)', zorder=3)
    ax7_1.axvspan(0, 80.0, color='#FEF2F2', alpha=0.35, zorder=0)

    ax7_1.set_yticks(y_p7)
    ax7_1.set_yticklabels(fak_sorted_7["Fakultas"], fontsize=11, fontweight='bold', color='#1E293B')
    ax7_1.set_xlim(0, 135)
    ax7_1.set_xlabel('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax7_1.set_title('A. Perbandingan Keterisian Kuota per Fakultas (2022 vs 2026)\nEvaluasi Efisiensi Serapan Kuota Pasca Penetapan PTN-BH', 
                    fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
    ax7_1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax7_1.spines['top'].set_visible(False)
    ax7_1.spines['right'].set_visible(False)
    ax7_1.legend(loc='lower left', bbox_to_anchor=(0.02, 0.02), frameon=True, fontsize=9.5, framealpha=0.95)

    for i, r in fak_sorted_7.iterrows():
        f22 = r['FR_2022']
        f26 = r['FR_2026']
        delta = f26 - f22
        delta_str = f"+{delta:.1f}%" if delta > 0 else f"{delta:.1f}%"
        du26 = int(r['DU_2026'])
        dt26 = int(r['DT_2026'])
        badge_txt = f"{f26:.1f}% ({du26:,}/{dt26:,})  |  Δ: {delta_str}"
        border_c = '#EF4444' if f26 < 80.0 else '#93C5FD'
        bg_c = '#FEF2F2' if f26 < 80.0 else '#FFFFFF'
        txt_c = '#991B1B' if f26 < 80.0 else '#0F172A'
        
        ax7_1.annotate(badge_txt, xy=(f26, i + h7/2.0), xytext=(7, 0), textcoords='offset points',
                       va='center', ha='left', fontsize=8.8, fontweight='bold', color=txt_c,
                       bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.95),
                       zorder=4)

    # Panel 2: Beban Kursi Kosong Absolut per Fakultas Tahun 2026
    fak_sisa_sorted = fak_agg.sort_values('Sisa_2026', ascending=True).reset_index(drop=True)
    y_pos2 = np.arange(len(fak_sisa_sorted))
    sisa_cols = ['#991B1B' if s >= 200 else '#EA580C' if s >= 70 else '#059669' for s in fak_sisa_sorted['Sisa_2026']]
    bars_sisa = ax7_2.barh(y_pos2, fak_sisa_sorted['Sisa_2026'], color=sisa_cols, height=0.62, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

    ax7_2.set_yticks(y_pos2)
    ax7_2.set_yticklabels(fak_sisa_sorted['Fakultas'], fontsize=11, fontweight='bold', color='#1E293B')
    max_sisa = fak_sisa_sorted['Sisa_2026'].max()
    ax7_2.set_xlim(0, max_sisa * 1.30)
    ax7_2.set_xlabel('Jumlah Kursi Kosong Absolut (Bangku Tidak Terisi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax7_2.set_title('B. Kontribusi Beban Kursi Kosong per Fakultas (Tahun 2026)\nTotal 1,569 Bangku Kosong di 12 Fakultas S1 Kampus Utama', 
                    fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
    ax7_2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax7_2.spines['top'].set_visible(False)
    ax7_2.spines['right'].set_visible(False)

    tot_sisa = fak_sisa_sorted['Sisa_2026'].sum()
    for i, r in fak_sisa_sorted.iterrows():
        s_val = int(r['Sisa_2026'])
        pct_share = (s_val / tot_sisa * 100.0) if tot_sisa > 0 else 0
        txt_col = '#991B1B' if s_val >= 200 else '#92400E' if s_val >= 70 else '#065F46'
        label_txt = "0 kursi (Penuh 100%)" if s_val == 0 else f"{s_val:,} kursi ({pct_share:.1f}% total defisit)"
            
        ax7_2.annotate(label_txt, xy=(s_val, i), xytext=(7, 0), textcoords='offset points',
                       va='center', ha='left', fontsize=9.0, fontweight='bold', color=txt_col,
                       bbox=dict(boxstyle='round,pad=0.22', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.7, alpha=0.92),
                       zorder=4)

    plt.suptitle('EVALUASI KOMPREHENSIF DAYA SERAP & DEFISIT KUOTA 12 FAKULTAS S1 USK (2022–2026)\nKomparasi Efisiensi Keterisian Kuota vs Beban Riil Kursi Kosong yang Ditanggung Fakultas',
                 fontsize=14, fontweight='bold', y=0.985, color='#0F172A')

    fig7.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
    fig7.savefig(os.path.join(chart_dir, "07_analisa_peminatan_dan_keterisian_fakultas.png"), dpi=300)
    plt.close(fig7)

    # -------------------------------------------------------------
    # CHART 8: EVALUASI DIPLOMA 3 VOKASI (DUAL-PANEL DASHBOARD)
    # -------------------------------------------------------------
    print("[8/9] Generating 08_evaluasi_multi_tahun_d3_vokasi.png...")
    d3_years = [2023, 2024, 2025, 2026]
    macro_dt = [df_d3[f"DT_{yr}"].sum() for yr in d3_years]
    macro_du = [df_d3[f"DU_{yr}"].sum() for yr in d3_years]
    macro_sisa = [dt - du for dt, du in zip(macro_dt, macro_du)]
    macro_fr = [du / dt * 100.0 for dt, du in zip(macro_dt, macro_du)]

    df_d3_clean = df_d3.copy()
    df_d3_clean['Total_DT_4Y'] = sum(df_d3_clean[f'DT_{y}'] for y in d3_years)
    df_d3_clean['Total_DU_4Y'] = sum(df_d3_clean[f'DU_{y}'] for y in d3_years)
    df_d3_clean['Total_Sisa_4Y'] = df_d3_clean['Total_DT_4Y'] - df_d3_clean['Total_DU_4Y']
    df_d3_clean['Rata_FR_4Y'] = (df_d3_clean['Total_DU_4Y'] / df_d3_clean['Total_DT_4Y'] * 100.0).round(1)
    df_d3_clean['FR_2026'] = (df_d3_clean['DU_2026'] / df_d3_clean['DT_2026'] * 100.0).round(1)
    df_d3_clean['Sisa_2026'] = df_d3_clean['DT_2026'] - df_d3_clean['DU_2026']

    def clean_d3_name(name):
        n = str(name).title().replace('D3 ', '').replace('D-Iii ', '')
        return f"D3 {n}"

    df_d3_clean['Label_Prodi'] = df_d3_clean['Program_Studi'].apply(clean_d3_name)
    d3_sorted = df_d3_clean.sort_values('Rata_FR_4Y', ascending=True).reset_index(drop=True)

    fig8, (ax8_1, ax8_2) = plt.subplots(1, 2, figsize=(26, 10.5), dpi=300, gridspec_kw={'width_ratios': [1.0, 1.35]})

    # Panel A: Makro Tahunan
    x_pos1 = np.arange(len(d3_years))
    w1 = 0.36

    ax8_1.bar(x_pos1 - w1/2, macro_dt, width=w1, color='#F59E0B', edgecolor='#0F172A', linewidth=1.0, label='Target Daya Tampung D3', zorder=2)
    ax8_1.bar(x_pos1 + w1/2, macro_du, width=w1, color='#10B981', edgecolor='#0F172A', linewidth=1.0, label='Daftar Ulang Riil D3', zorder=2)

    ax8_1.set_xticks(x_pos1)
    ax8_1.set_xticklabels([f"Tahun {y}" for y in d3_years], fontsize=11, fontweight='bold', color='#1E293B')
    ax8_1.set_ylim(0, 850)
    ax8_1.set_ylabel('Jumlah Mahasiswa / Kuota Kursi', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax8_1.set_title('A. Kinerja Agregat & Defisit Kuota Tahunan D3 Vokasi (2023–2026)\nAkumulasi 4 Tahun: 1,320 Kursi Kosong (Keterisian Kumulatif Hanya 48.5%)', 
                  fontsize=12.5, fontweight='bold', pad=12, color='#0F172A')
    ax8_1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax8_1.spines['top'].set_visible(False)
    ax8_1.spines['right'].set_visible(False)

    for idx, y in enumerate(d3_years):
        dt_v = int(macro_dt[idx])
        du_v = int(macro_du[idx])
        sisa_v = int(macro_sisa[idx])
        fr_v = macro_fr[idx]
        
        ax8_1.annotate(f"{dt_v} kursi", xy=(x_pos1[idx] - w1/2, dt_v), xytext=(0, 5), textcoords='offset points',
                     ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#B45309')
        ax8_1.annotate(f"{du_v} mhs\n({fr_v:.1f}%)", xy=(x_pos1[idx] + w1/2, du_v), xytext=(0, 5), textcoords='offset points',
                     ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#047857')
        ax8_1.annotate(f"Defisit: {sisa_v} kursi", xy=(x_pos1[idx], max(dt_v, du_v)), xytext=(0, 32), textcoords='offset points',
                     ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#991B1B',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.0),
                     arrowprops=dict(arrowstyle='->', color='#EF4444', lw=1.0, shrinkA=2, shrinkB=4))

    tot_kuota = sum(macro_dt)
    tot_mhs = sum(macro_du)
    tot_defisit = sum(macro_sisa)
    ax8_1.text(0.5, 0.04, f"TOTAL KUOTA 4 TAHUN: {tot_kuota} Kursi  |  TERISI: {tot_mhs} Mahasiswa  |  KOSONG: {tot_defisit} Kursi (51.5% Mubazir)",
             transform=ax8_1.transAxes, ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#991B1B',
             bbox=dict(boxstyle='square,pad=0.35', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.1))

    ax8_1.legend(loc='upper left', frameon=True, fontsize=9.5, framealpha=0.95)

    # Panel B: Diagnostik 11 Prodi D3
    y_pos2 = np.arange(len(d3_sorted))
    colors_bars2 = ['#991B1B' if fr < 45.0 else '#D97706' if fr < 60.0 else '#059669' for fr in d3_sorted['Rata_FR_4Y']]

    ax8_2.barh(y_pos2, d3_sorted['Rata_FR_4Y'], color=colors_bars2, height=0.62, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)
    ax8_2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.6, label='Standar Keterisian Sehat (80%)', zorder=3)
    ax8_2.axvline(50.0, color='#64748B', linestyle=':', linewidth=1.4, label='Batas Kritis Kelayakan (50%)', zorder=3)
    ax8_2.axvspan(0, 50.0, color='#FEF2F2', alpha=0.4, zorder=0)

    ax8_2.set_yticks(y_pos2)
    ax8_2.set_yticklabels(d3_sorted['Label_Prodi'], fontsize=10.5, fontweight='bold', color='#1E293B')
    ax8_2.set_xlim(0, 135)
    ax8_2.set_ylim(-0.8, len(d3_sorted) - 0.2)
    ax8_2.set_xlabel('Rata-rata Tingkat Keterisian Kuota 4 Tahun (2023–2026, %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax8_2.set_title('B. Diagnostik 11 Program Studi D3 Vokasi (Kinerja Historis 2023–2026)\nMembedah Jurang Pemisah: Dari D3 Budidaya Peternakan (32.0%) hingga D3 Manajemen Informatika (68.8%)', 
                  fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
    ax8_2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax8_2.spines['top'].set_visible(False)
    ax8_2.spines['right'].set_visible(False)

    for i, r in d3_sorted.iterrows():
        fr4 = r['Rata_FR_4Y']
        du4 = int(r['Total_DU_4Y'])
        dt4 = int(r['Total_DT_4Y'])
        sisa4 = int(r['Total_Sisa_4Y'])
        fr26 = r['FR_2026']
        du26 = int(r['DU_2026'])
        dt26 = int(r['DT_2026'])
        
        badge_txt = f"Rata 4Y: {fr4:.1f}% ({du4}/{dt4})  |  2026: {fr26:.1f}% ({du26}/{dt26})  |  Kosong: {sisa4} kursi"
        txt_c = '#991B1B' if fr4 < 45.0 else '#92400E' if fr4 < 60.0 else '#065F46'
        border_c = '#EF4444' if fr4 < 45.0 else '#F59E0B' if fr4 < 60.0 else '#10B981'
        bg_c = '#FEF2F2' if fr4 < 45.0 else '#FFFBEB' if fr4 < 60.0 else '#F0FDF4'
        
        ax8_2.annotate(badge_txt, xy=(fr4, i), xytext=(7, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=8.4, fontweight='bold', color=txt_c,
                     bbox=dict(boxstyle='round,pad=0.20', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.92),
                     zorder=4)

    legend_elements2 = [
        Patch(facecolor='#059669', edgecolor='#0F172A', label='Keterisian Moderat/Tinggi (≥60%)'),
        Patch(facecolor='#D97706', edgecolor='#0F172A', label='Keterisian Rentan (45%–59%)'),
        Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Keterisian Kritis (<45%) - Urgensi Penutupan/Konversi D4')
    ]
    ax8_2.legend(handles=legend_elements2, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

    fig8.suptitle('EVALUASI MENYELURUH DAYA SERAP & KRISIS KUOTA 11 PROGRAM STUDI DIPLOMA 3 VOKASI USK (2023–2026)\nKombinasi Tren Makro Tahunan & Diagnostik Defisit per Program Studi Menuju Rasionalisasi Kuota 2027',
                 fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

    fig8.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
    fig8.savefig(os.path.join(chart_dir, "08_evaluasi_multi_tahun_d3_vokasi.png"), dpi=300)
    plt.close(fig8)

    # -------------------------------------------------------------
    # CHART 9: SUB-ANALISIS PSDKU GAYO LUES (DUAL-PANEL DASHBOARD)
    # -------------------------------------------------------------
    print("[9/10] Generating 09_subanalisis_psdku_gayo_lues.png...")
    macro_dt_psdku = [df_psdku[f"DT_{yr}"].sum() for yr in years]
    macro_du_psdku = [df_psdku[f"DU_{yr}"].sum() for yr in years]
    macro_sisa_psdku = [dt - du for dt, du in zip(macro_dt_psdku, macro_du_psdku)]
    macro_fr_psdku = [du / dt * 100.0 for dt, du in zip(macro_dt_psdku, macro_du_psdku)]

    df_clean_psdku = df_psdku.copy()
    df_clean_psdku['Total_DT_5Y'] = sum(df_clean_psdku[f'DT_{y}'] for y in years)
    df_clean_psdku['Total_DU_5Y'] = sum(df_clean_psdku[f'DU_{y}'] for y in years)
    df_clean_psdku['Total_Sisa_5Y'] = df_clean_psdku['Total_DT_5Y'] - df_clean_psdku['Total_DU_5Y']
    df_clean_psdku['Rata_FR_5Y'] = (df_clean_psdku['Total_DU_5Y'] / df_clean_psdku['Total_DT_5Y'] * 100.0).round(1)
    df_clean_psdku['FR_2026'] = (df_clean_psdku['DU_2026'] / df_clean_psdku['DT_2026'] * 100.0).round(1)
    df_clean_psdku['Sisa_2026'] = df_clean_psdku['DT_2026'] - df_clean_psdku['DU_2026']

    def clean_psdku_name_fn(name):
        n = str(name).replace('(PDD GAYO LUES)', '').replace('(Gayo Lues)', '').strip().title()
        return f"{n} (Gayo Lues)"

    df_clean_psdku['Label_Prodi'] = df_clean_psdku['Program_Studi'].apply(clean_psdku_name_fn)
    psdku_sorted = df_clean_psdku.sort_values('Rata_FR_5Y', ascending=True).reset_index(drop=True)

    fig9, (ax9_1, ax9_2) = plt.subplots(1, 2, figsize=(25, 10), dpi=300, gridspec_kw={'width_ratios': [1.05, 1.25]})

    # Panel A: Tren Jurang Kuota vs Realisasi PSDKU
    x_pos1_9 = np.arange(len(years))
    w1_9 = 0.35

    ax9_1.bar(x_pos1_9 - w1_9/2, macro_dt_psdku, width=w1_9, color='#F59E0B', edgecolor='#0F172A', linewidth=1.0, label='Target Daya Tampung Kuota', zorder=2)
    ax9_1.bar(x_pos1_9 + w1_9/2, macro_du_psdku, width=w1_9, color='#0284C7', edgecolor='#0F172A', linewidth=1.0, label='Daftar Ulang Riil Mahasiswa', zorder=2)

    ax9_1.set_xticks(x_pos1_9)
    ax9_1.set_xticklabels([f"Tahun {y}" for y in years], fontsize=11, fontweight='bold', color='#1E293B')
    ax9_1.set_ylim(0, 275)
    ax9_1.set_ylabel('Jumlah Mahasiswa / Kuota Kursi', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax9_1.set_title('A. Jurang Daya Tampung vs Mahasiswa Masuk Riil PSDKU Gayo Lues (2022–2026)\nAkumulasi 5 Tahun: 783 Kursi Kosong (Keterisian Kumulatif Hanya 25.4% / 74.6% Mubazir)', 
                  fontsize=12.2, fontweight='bold', pad=12, color='#0F172A')
    ax9_1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax9_1.spines['top'].set_visible(False)
    ax9_1.spines['right'].set_visible(False)

    for idx, y in enumerate(years):
        dt_v = int(macro_dt_psdku[idx])
        du_v = int(macro_du_psdku[idx])
        sisa_v = int(macro_sisa_psdku[idx])
        fr_v = macro_fr_psdku[idx]
        
        ax9_1.annotate(f"{dt_v} kursi", xy=(x_pos1_9[idx] - w1_9/2, dt_v), xytext=(0, 4), textcoords='offset points',
                     ha='center', va='bottom', fontsize=9.2, fontweight='bold', color='#B45309')
        ax9_1.annotate(f"{du_v} mhs\n({fr_v:.1f}%)", xy=(x_pos1_9[idx] + w1_9/2, du_v), xytext=(0, 4), textcoords='offset points',
                     ha='center', va='bottom', fontsize=9.0, fontweight='bold', color='#0369A1')
        ax9_1.annotate(f"Defisit: {sisa_v} kursi\n({100-fr_v:.1f}% Kosong)", xy=(x_pos1_9[idx], dt_v), xytext=(0, 24), textcoords='offset points',
                     ha='center', va='bottom', fontsize=8.6, fontweight='bold', color='#991B1B',
                     bbox=dict(boxstyle='round,pad=0.22', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.0),
                     arrowprops=dict(arrowstyle='->', color='#EF4444', lw=1.0, shrinkA=2, shrinkB=4))

    tot_kuota_9 = sum(macro_dt_psdku)
    tot_mhs_9 = sum(macro_du_psdku)
    tot_defisit_9 = sum(macro_sisa_psdku)
    ax9_1.text(0.5, 0.04, f"TOTAL KUOTA 5 TAHUN: {tot_kuota_9} Kursi  |  TERISI: {tot_mhs_9} Mahasiswa  |  KOSONG: {tot_defisit_9} Kursi (74.6% Mubazir)",
             transform=ax9_1.transAxes, ha='center', va='bottom', fontsize=8.8, fontweight='bold', color='#991B1B',
             bbox=dict(boxstyle='square,pad=0.35', facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.1))

    ax9_1.legend(loc='upper left', frameon=True, fontsize=9.5, framealpha=0.95)

    # Panel B: Diagnostik 4 Prodi PSDKU Gayo Lues
    y_pos2_9 = np.arange(len(psdku_sorted))
    colors_bars2_9 = ['#991B1B' for _ in range(len(psdku_sorted))]

    ax9_2.barh(y_pos2_9, psdku_sorted['Rata_FR_5Y'], color=colors_bars2_9, height=0.55, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)
    ax9_2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.6, label='Standar Keterisian Sehat (80%)', zorder=3)
    ax9_2.axvline(50.0, color='#EA580C', linestyle=':', linewidth=1.4, label='Batas Kritis Kelayakan Kelas Mandiri (50%)', zorder=3)
    ax9_2.axvspan(0, 50.0, color='#FEF2F2', alpha=0.45, zorder=0)

    ax9_2.set_yticks(y_pos2_9)
    ax9_2.set_yticklabels(psdku_sorted['Label_Prodi'], fontsize=11.0, fontweight='bold', color='#1E293B')
    ax9_2.set_xlim(0, 115)
    ax9_2.set_ylim(-0.8, len(psdku_sorted) - 0.2)
    ax9_2.set_xlabel('Rata-rata Tingkat Keterisian Kuota 5 Tahun (2022–2026, %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax9_2.set_title('B. Diagnostik 4 Program Studi PSDKU Gayo Lues (Kinerja Historis 5 Tahun)\nSeluruh Program Studi Berada di Bawah 30% Keterisian (Zona Krisis Akut Permanen)', 
                  fontsize=12.2, fontweight='bold', pad=12, color='#991B1B')
    ax9_2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax9_2.spines['top'].set_visible(False)
    ax9_2.spines['right'].set_visible(False)

    for i, r in psdku_sorted.iterrows():
        fr5 = r['Rata_FR_5Y']
        du5 = int(r['Total_DU_5Y'])
        dt5 = int(r['Total_DT_5Y'])
        sisa5 = int(r['Total_Sisa_5Y'])
        fr26 = r['FR_2026']
        du26 = int(r['DU_2026'])
        dt26 = int(r['DT_2026'])
        
        badge_txt = f"Rata 5-Thn: {fr5:.1f}% ({du5}/{dt5})  |  2026: {fr26:.1f}% ({du26}/{dt26})  |  Defisit 5-Thn: {sisa5} kursi"
        txt_c = '#991B1B'
        border_c = '#EF4444'
        bg_c = '#FEF2F2'
        
        ax9_2.annotate(badge_txt, xy=(fr5, i), xytext=(7, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=8.6, fontweight='bold', color=txt_c,
                     bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.95),
                     zorder=4)

    legend_elements2_9 = [
        Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Krisis Akut Ekstrem (<30%) — Seluruh Prodi PSDKU Terperangkap di Zona Ini')
    ]
    ax9_2.legend(handles=legend_elements2_9, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=1, frameon=True, fontsize=9.0, framealpha=0.95)

    fig9.suptitle('EVALUASI MENYELURUH DAYA SERAP & INEFISIENSI OPERASIONAL PSDKU GAYO LUES (2022–2026)\nAnomali Geografis & Isolasi Demografis: Pembuktian Ilmiah Krisis Kuota Kampus Cabang Terpencil',
                 fontsize=14.0, fontweight='bold', y=0.985, color='#0F172A')

    fig9.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
    fig9.savefig(os.path.join(chart_dir, "09_subanalisis_psdku_gayo_lues.png"), dpi=300)
    plt.close(fig9)

    # -------------------------------------------------------------
    # CHART 10: MATRIKS 4 KUADRAN STRATEGIS PORTOFOLIO PRODI (2026)
    # -------------------------------------------------------------
    print("[10/10] Generating 10_matriks_4_kuadran_prodi_usk.png...")
    import matplotlib.gridspec as gridspec
    from matplotlib.patches import FancyBboxPatch

    fig = plt.figure(figsize=(24, 11.5), dpi=300)
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.75, 1.0], wspace=0.16)

    ax = fig.add_subplot(gs[0])
    ax_cards = fig.add_subplot(gs[1])
    ax_cards.axis('off')

    x_max = 42
    y_min, y_max = 44, 110

    # Pastel Quadrant Backgrounds
    ax.axvspan(4.0, x_max, ymin=(80 - y_min)/(y_max - y_min), ymax=1.0, color='#ECFDF5', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=(80 - y_min)/(y_max - y_min), ymax=1.0, color='#EFF6FF', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=0.0, ymax=(80 - y_min)/(y_max - y_min), color='#FEF2F2', alpha=0.55, zorder=0)
    ax.axvspan(4.0, x_max, ymin=0.0, ymax=(80 - y_min)/(y_max - y_min), color='#FFFBEB', alpha=0.55, zorder=0)

    # Dividing lines
    ax.axvline(x=4.0, color='#64748B', linestyle='--', linewidth=2.0, zorder=1)
    ax.axhline(y=80.0, color='#64748B', linestyle='--', linewidth=2.0, zorder=1)

    # Subtle Quadrant Watermark Headers
    ax.text(39.5, 107.5, 'KUADRAN I: PRIMA & BINTANG (31 Prodi)',
            ha='right', va='top', fontsize=11, fontweight='bold', color='#065F46', alpha=0.85, zorder=2)
    ax.text(0.5, 107.5, 'KUADRAN II: STABIL (6 Prodi)',
            ha='left', va='top', fontsize=11, fontweight='bold', color='#1E40AF', alpha=0.85, zorder=2)
    ax.text(0.5, 45.5, 'KUADRAN III: KRITIS (22 Prodi)',
            ha='left', va='bottom', fontsize=11, fontweight='bold', color='#991B1B', alpha=0.85, zorder=2)
    ax.text(39.5, 45.5, 'KUADRAN IV: DILEMA (7 Prodi)',
            ha='right', va='bottom', fontsize=11, fontweight='bold', color='#92400E', alpha=0.85, zorder=2)

    # Calculate quadrant colors and bubble sizes based on DT
    pt_cols = []
    for _, r in df_s1.iterrows():
        x = r['Keketatan_2026']
        y = r['FillRate_2026_Persen']
        if x >= 4.0 and y >= 80.0:
            pt_cols.append('#059669') # Emerald Green
        elif x < 4.0 and y >= 80.0:
            pt_cols.append('#2563EB') # Blue
        elif x < 4.0 and y < 80.0:
            pt_cols.append('#DC2626') # Red
        else:
            pt_cols.append('#D97706') # Amber

    sizes = 45 + (df_s1['DT_2026'] / 560.0) * 190
    ax.scatter(df_s1['Keketatan_2026'], df_s1['FillRate_2026_Persen'], s=sizes, c=pt_cols,
               edgecolors='#0F172A', linewidths=1.1, alpha=0.88, zorder=4)

    # Key representative annotations
    key_annots = [
        # Kuadran I (Prima)
        ('Farmasi (FMIPA)', 39.18, 98.9, (-15, 12), 'right'),
        ('Informatika (FMIPA)', 18.12, 97.5, (12, -10), 'left'),
        ('Psikologi (FK)', 17.31, 95.0, (-10, -18), 'right'),
        ('Pendidikan Dokter (FK)', 8.01, 100.0, (14, 8), 'left'),
        ('Ilmu Hukum (FH)', 6.64, 99.6, (-12, 14), 'right'),
        ('PGSD (FKIP)', 9.46, 94.3, (14, 0), 'left'),
        ('Teknik Sipil (FT)', 5.06, 90.0, (12, -12), 'left'),
        
        # Kuadran II (Stabil)
        ('Dokter Hewan (FKH)', 3.74, 93.3, (-14, 10), 'right'),
        ('Arsitektur (FT)', 3.14, 81.9, (-14, -14), 'right'),
        ('HI (FISIP)', 2.35, 91.2, (-12, 10), 'right'),
        ('TSDA (FT)', 2.03, 86.7, (12, -10), 'left'),
        
        # Kuadran III (Kritis)
        ('Budidaya Perairan (FPK)', 0.91, 56.2, (12, -8), 'left'),
        ('Fisika (FMIPA)', 1.18, 52.5, (12, 8), 'left'),
        ('PSP Perikanan (FPK)', 1.07, 55.8, (-10, 14), 'right'),
        ('THP (FP)', 3.19, 63.7, (12, 8), 'left'),
        ('Pend. Ekonomi (FKIP)', 2.52, 64.4, (-12, 12), 'right'),
        ('Pend. Kimia (FKIP)', 1.72, 62.5, (12, -10), 'left'),
        ('Teknik Kimia (FT)', 2.43, 66.7, (12, 10), 'left'),
        
        # Kuadran IV (Dilema)
        ('Akuntansi Perpajakan (FEB)', 22.43, 73.8, (12, 10), 'left'),
        ('PWK (FT)', 5.58, 75.0, (12, 10), 'left'),
        ('Pend. Guru PAUD (FKIP)', 5.46, 73.6, (-12, -14), 'right'),
        ('Teknik Elektro (FT)', 4.43, 70.0, (12, -12), 'left'),
        ('Agroteknologi (FP)', 5.14, 78.3, (12, 6), 'left')
    ]

    for label, px, py, (ox, oy), ha_align in key_annots:
        ax.annotate(label, xy=(px, py), xytext=(ox, oy), textcoords='offset points',
                    ha=ha_align, va='center', fontsize=8.2, fontweight='bold', color='#0F172A',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.8, alpha=0.94),
                    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.9, shrinkA=2, shrinkB=3),
                    zorder=5)

    ax.set_xlim(0, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Rasio Keketatan Seleksi 2026 (Peminat per 1 Kursi Daya Tampung) -> Daya Tarik Pasar (Demand)', 
                  fontsize=10.5, fontweight='bold', color='#0F172A', labelpad=10)
    ax.set_ylabel('Capacity Fill Rate 2026 (%) -> Realisasi Keterisian Kuota Riil (Supply)', 
                  fontsize=10.5, fontweight='bold', color='#0F172A', labelpad=10)
    ax.set_title('Peta Sebaran 66 Program Studi S1 Kampus Utama USK (2026) | Ukuran Bubble = Daya Tampung Kuota (50 s.d. 560 Kursi)', 
                 fontsize=11.5, fontweight='bold', pad=12, color='#0F172A')
    ax.grid(True, linestyle=':', alpha=0.55, color='#94A3B8', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')

    # Executive Cards
    cards_data = [
        {
            'title': 'KUADRAN I: PRIMA & BINTANG (31 PRODI | 47%)',
            'color_border': '#10B981', 'color_bg': '#ECFDF5', 'color_text': '#065F46',
            'desc': 'Demand Tinggi (>=4,0x) & Kuota Penuh (>=80%)\nPeminat membludak dan kelas terisi optimal.',
            'examples': 'Farmasi, Informatika, Kedokteran, Hukum, Psikologi, PGSD, Sipil.',
            'action': 'AKSI: Pertahankan & Investasi.\nBoleh naikkan kuota terukur (+5% s.d. +10%)\natau buka Kelas Internasional.'
        },
        {
            'title': 'KUADRAN II: STABIL & EFISIEN (6 PRODI | 9%)',
            'color_border': '#3B82F6', 'color_bg': '#EFF6FF', 'color_text': '#1E40AF',
            'desc': 'Demand Terbatas (<4,0x) tapi Kuota Penuh (>=80%)\nKompetisi tidak ekstrem namun kelas terisi penuh.',
            'examples': 'Dokter Hewan, Arsitektur, HI, Ilmu Politik, TSDA.',
            'action': 'AKSI: Proteksi Kuota.\nKuota saat ini sudah seimbang sempurna.\nJangan latah menaikkan kuota!'
        },
        {
            'title': 'KUADRAN III: KRITIS & DEFISIT (22 PRODI | 33%)',
            'color_border': '#EF4444', 'color_bg': '#FEF2F2', 'color_text': '#991B1B',
            'desc': 'Demand Lemah (<4,0x) & Kursi Banyak Bolong (<80%)\nPeminat lesu dan kelas mengalami idle capacity parah.',
            'examples': 'Budidaya Perairan, Fisika, PSP, THP, Pend. Ekonomi, Kimia.',
            'action': 'AKSI: WAJIB PANGKAS KUOTA (20%-40%).\nHapus 400+ kursi kosong semu dan\namankan nilai akreditasi prodi!'
        },
        {
            'title': 'KUADRAN IV: DILEMA & BOCOR (7 PRODI | 11%)',
            'color_border': '#F59E0B', 'color_bg': '#FFFBEB', 'color_text': '#92400E',
            'desc': 'Demand Tinggi (>=4,0x) tapi Keterisian Rendah (<80%)\nPeminat ada, namun calon mahasiswa gugur di jalur mandiri.',
            'examples': 'Akuntansi Perpajakan, PWK, PAUD, Agroteknologi, Elektro.',
            'action': 'AKSI: Reformasi Biaya & Cicilan IPI.\nSediakan fasilitas cicilan uang pangkal\ndan percepat panggilan cadangan.'
        }
    ]

    y_positions = [0.77, 0.52, 0.27, 0.02]
    box_height = 0.22

    for idx, c in enumerate(cards_data):
        y = y_positions[idx]
        rect = FancyBboxPatch((0.01, y), 0.98, box_height, boxstyle='round,pad=0.025',
                              facecolor=c['color_bg'], edgecolor=c['color_border'], linewidth=1.5,
                              transform=ax_cards.transAxes, zorder=2)
        ax_cards.add_patch(rect)
        ax_cards.text(0.05, y + box_height - 0.032, c['title'],
                      fontsize=9.5, fontweight='bold', color=c['color_text'],
                      transform=ax_cards.transAxes, zorder=3)
        ax_cards.text(0.05, y + box_height - 0.075, c['desc'],
                      fontsize=8.3, color='#334155', linespacing=1.2,
                      transform=ax_cards.transAxes, zorder=3)
        ax_cards.text(0.05, y + box_height - 0.122, f"Prodi: {c['examples']}",
                      fontsize=8.0, fontstyle='italic', color='#475569',
                      transform=ax_cards.transAxes, zorder=3)
        ax_cards.text(0.05, y + 0.022, c['action'],
                      fontsize=8.3, fontweight='bold', color=c['color_text'], linespacing=1.2,
                      transform=ax_cards.transAxes, zorder=3)

    fig.suptitle('MATRIKS 4 KUADRAN PORTOFOLIO STRATEGIS PROGRAM STUDI S1 UNIVERSITAS SYIAH KUALA (2026)\nPemetaan Daya Tarik Peminatan (Demand) vs Realisasi Keterisian Kuota (Supply) untuk Navigasi Kebijakan PMB 2027',
                 fontsize=13.5, fontweight='bold', y=0.975, color='#0F172A')

    fig.subplots_adjust(left=0.055, right=0.985, top=0.89, bottom=0.075, wspace=0.15)
    plt.savefig(os.path.join(chart_dir, "10_matriks_4_kuadran_prodi_usk.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 12: BENCHMARK KEKETATAN 5 TAHUN (2022–2026)
    # -------------------------------------------------------------
    print("[12/12] Generating 12_tren_keketatan_seleksi_5_tahun_2022_2026.png...")
    top10_5y = df_s1.sort_values('Rata_Keketatan_5Thn', ascending=False).head(10).reset_index(drop=True)
    bot10_5y = df_s1[df_s1['Rata_Keketatan_5Thn'] > 0].sort_values('Rata_Keketatan_5Thn', ascending=True).head(10).reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), dpi=300)

    # Panel 1: Top 10 Favorit 5 Tahun
    y_pos1 = np.arange(len(top10_5y))
    bars12 = ax1.barh(y_pos1, top10_5y['Rata_Keketatan_5Thn'], color='#1E40AF', alpha=0.9, height=0.60, edgecolor='#1E3A8A', linewidth=1.2, zorder=2)
    ax1.set_yticks(y_pos1)
    labels1 = [clean_name(r['Program_Studi'], r['Fakultas']) for _, r in top10_5y.iterrows()]
    ax1.set_yticklabels(labels1, fontsize=10, fontweight='bold', color='#1E293B')
    ax1.invert_yaxis()
    ax1.set_xlabel('Rasio Keketatan Seleksi (Rata-rata Peminat per 1 Kursi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax1.set_title('A. Top 10 Program Studi Paling Favorit & Ketat (Benchmark 5 Tahun)', fontsize=12.5, fontweight='bold', pad=15, color='#1E40AF')
    ax1.set_xlim(0, 62)
    ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#94A3B8')
    ax1.spines['bottom'].set_color('#94A3B8')
    line12_ref1 = ax1.axvline(10.0, color='#16A34A', linestyle='--', linewidth=1.6, alpha=0.85, zorder=1, label='Batas Sangat Ketat (10 : 1)')

    for i, r in top10_5y.iterrows():
        val = r['Rata_Keketatan_5Thn']
        pem = int(r['Rata_Peminat_5Thn'])
        k22 = r['Keketatan_2022']
        k26 = r['Keketatan_2026']
        trend_symbol = '▲' if k26 >= k22 else '▼'
        ax1.annotate(f"{val:.1f} : 1", xy=(val, i), xytext=(8, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=9.2, fontweight='bold', color='#1E3A8A',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.0), zorder=4)
        ax1.annotate(f"({pem:,} pelamar/thn | {k22:.1f}x → {k26:.1f}x {trend_symbol})", xy=(val, i), xytext=(60, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=8.8, color='#475569', zorder=4)

    # Panel 2: Bottom 10 Sepi 5 Tahun
    y_pos2 = np.arange(len(bot10_5y))
    colors_bot5 = ['#991B1B' if r['Rata_Keketatan_5Thn'] <= 1.05 else '#DC2626' if r['Rata_Keketatan_5Thn'] < 1.5 else '#EA580C' for _, r in bot10_5y.iterrows()]
    bars12_bot = ax2.barh(y_pos2, bot10_5y['Rata_Keketatan_5Thn'], color=colors_bot5, alpha=0.88, height=0.60, edgecolor='#7F1D1D', linewidth=1.2, zorder=2)
    ax2.set_yticks(y_pos2)
    labels2 = [clean_name(r['Program_Studi'], r['Fakultas']) for _, r in bot10_5y.iterrows()]
    ax2.set_yticklabels(labels2, fontsize=10, fontweight='bold', color='#1E293B')
    ax2.invert_yaxis()
    ax2.set_xlabel('Rasio Keketatan Seleksi (Rata-rata Peminat per 1 Kursi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax2.set_title('B. Top 10 Program Studi Paling Sepi Peminat (Benchmark 5 Tahun)', fontsize=12.5, fontweight='bold', pad=15, color='#991B1B')
    ax2.set_xlim(0, 4.6)
    ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_color('#94A3B8')
    ax2.spines['bottom'].set_color('#94A3B8')
    line12_ref2 = ax2.axvline(1.0, color='#7F1D1D', linestyle='-', linewidth=2.4, zorder=1, label='Garis Kritis Mutlak 1,0 : 1 (Peminat < Kuota)')
    line12_ref3 = ax2.axvline(1.5, color='#DC2626', linestyle='--', linewidth=1.8, zorder=1, label='Batas Minimal BAN-PT (1,5 : 1)')
    line12_ref4 = ax2.axvline(3.0, color='#16A34A', linestyle=':', linewidth=1.6, zorder=1, label='Batas Standar Sehat PTN (3,0 : 1)')

    for i, r in bot10_5y.iterrows():
        val = r['Rata_Keketatan_5Thn']
        pem = int(r['Rata_Peminat_5Thn'])
        dt = int(r['Rata_DT_5Thn'])
        is_kritis = val <= 1.05
        bg_col = '#FEF2F2' if is_kritis else '#FFF7ED'
        border_col = '#EF4444' if is_kritis else '#F97316'
        txt_col = '#991B1B' if is_kritis else '#C2410C'
        status = 'KRITIS' if is_kritis else 'SEPI'
        ax2.annotate(f"{val:.2f} : 1", xy=(val, i), xytext=(8, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=9.2, fontweight='bold', color=txt_col,
                     bbox=dict(boxstyle='round,pad=0.25', facecolor=bg_col, edgecolor=border_col, linewidth=1.0), zorder=4)
        ax2.annotate(f"{pem} peminat / {dt} kursi ({status})", xy=(val, i), xytext=(58, 0), textcoords='offset points',
                     va='center', ha='left', fontsize=8.8, fontweight='bold' if is_kritis else 'normal', color=txt_col,
                     bbox=dict(boxstyle='round,pad=0.18', facecolor='#FFFFFF', edgecolor='none', alpha=0.92), zorder=4)

    handles12 = [bars12, line12_ref1, line12_ref2, line12_ref3, line12_ref4]
    labels12 = [
        'Rata-rata Rasio 5 Tahun (2022–2026)',
        'Batas Sangat Ketat (10 : 1)',
        'Garis Kritis Mutlak 1,0 : 1 (Peminat < Kuota)',
        'Batas Minimal BAN-PT (1,5 : 1)',
        'Batas Standar Sehat PTN (3,0 : 1)'
    ]
    fig.legend(handles12, labels12, loc='lower center', bbox_to_anchor=(0.5, 0.015), ncol=5, frameon=True,
               fontsize=9.5, facecolor='#F8FAFC', edgecolor='#CBD5E1', framealpha=0.98)

    plt.suptitle('BENCHMARK TINGKAT KEKETATAN SELEKSI 5 TAHUN (2022–2026)\nKomparasi Program Studi S1 Paling Favorit vs Paling Sepi Peminat di Universitas Syiah Kuala', 
                 fontsize=14, fontweight='bold', y=0.98, color='#0F172A')
    plt.tight_layout(rect=[0.01, 0.07, 0.99, 0.93])
    plt.savefig(os.path.join(chart_dir, "12_tren_keketatan_seleksi_5_tahun_2022_2026.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 13: MATRIKS 4 KUADRAN STRATEGIS 5 TAHUN (2022–2026)
    # -------------------------------------------------------------
    print("[13/13] Generating 13_matriks_4_kuadran_5_tahun_2022_2026.png...")
    fig = plt.figure(figsize=(24, 11.5), dpi=300)
    gs = gridspec.GridSpec(1, 2, width_ratios=[1.75, 1.0], wspace=0.16)

    ax = fig.add_subplot(gs[0])
    ax_cards = fig.add_subplot(gs[1])
    ax_cards.axis('off')

    x_max = 48
    y_min, y_max = 38, 108

    # Pastel Quadrant Backgrounds
    ax.axvspan(4.0, x_max, ymin=(80 - y_min)/(y_max - y_min), ymax=1.0, color='#ECFDF5', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=(80 - y_min)/(y_max - y_min), ymax=1.0, color='#EFF6FF', alpha=0.55, zorder=0)
    ax.axvspan(0.0, 4.0, ymin=0.0, ymax=(80 - y_min)/(y_max - y_min), color='#FEF2F2', alpha=0.55, zorder=0)
    ax.axvspan(4.0, x_max, ymin=0.0, ymax=(80 - y_min)/(y_max - y_min), color='#FFFBEB', alpha=0.55, zorder=0)

    # Dividing lines
    ax.axvline(x=4.0, color='#64748B', linestyle='--', linewidth=2.0, zorder=1)
    ax.axhline(y=80.0, color='#64748B', linestyle='--', linewidth=2.0, zorder=1)

    # Subtle Quadrant Watermark Headers
    ax.text(x_max - 2.5, 105.5, 'KUADRAN I: PRIMA & BINTANG KONSISTEN (28 Prodi)',
            ha='right', va='top', fontsize=11, fontweight='bold', color='#065F46', alpha=0.85, zorder=2)
    ax.text(0.5, 105.5, 'KUADRAN II: STABIL & EFISIEN (4 Prodi)',
            ha='left', va='top', fontsize=11, fontweight='bold', color='#1E40AF', alpha=0.85, zorder=2)
    ax.text(0.5, 40.0, 'KUADRAN III: KRITIS & DEFISIT KRONIS (26 Prodi)',
            ha='left', va='bottom', fontsize=11, fontweight='bold', color='#991B1B', alpha=0.85, zorder=2)
    ax.text(x_max - 2.5, 40.0, 'KUADRAN IV: DILEMA & BOCOR BERULANG (8 Prodi)',
            ha='right', va='bottom', fontsize=11, fontweight='bold', color='#92400E', alpha=0.85, zorder=2)

    # Assign colors based on 5-year averages
    pt_cols_5y = []
    for _, r in df_s1.iterrows():
        x = r['Rata_Keketatan_5Thn']
        y = r['Rata_FillRate_5Thn_Persen']
        if x >= 4.0 and y >= 80.0:
            pt_cols_5y.append('#059669') # Emerald
        elif x < 4.0 and y >= 80.0:
            pt_cols_5y.append('#2563EB') # Blue
        elif x < 4.0 and y < 80.0:
            pt_cols_5y.append('#DC2626') # Red
        else:
            pt_cols_5y.append('#D97706') # Amber

    sizes_5y = 45 + (df_s1['Rata_DT_5Thn'] / 500.0) * 190
    ax.scatter(df_s1['Rata_Keketatan_5Thn'], df_s1['Rata_FillRate_5Thn_Persen'], s=sizes_5y, c=pt_cols_5y,
               edgecolors='#0F172A', linewidths=1.1, alpha=0.88, zorder=4)

    # Key representative annotations 5Y
    key_annots_5y = [
        # Kuadran I (Prima Konsisten)
        ('Farmasi (FMIPA)', 44.06, 98.0, (-16, 12), 'right'),
        ('Informatika (FMIPA)', 21.49, 95.1, (12, -10), 'left'),
        ('Psikologi (FK)', 17.30, 91.7, (-10, -16), 'right'),
        ('Pend. Dokter Gigi (FKG)', 17.25, 97.5, (12, 10), 'left'),
        ('Pend. Dokter (FK)', 14.12, 98.6, (12, -8), 'left'),
        ('Ilmu Hukum (FH)', 8.08, 97.4, (-12, 14), 'right'),
        ('PGSD (FKIP)', 10.38, 93.3, (12, 6), 'left'),
        ('Teknik Pertambangan (FT)', 13.19, 92.3, (-12, -14), 'right'),
        
        # Kuadran II (Stabil Konsisten)
        ('Penjaskesrek (FKIP)', 3.50, 91.6, (12, 12), 'left'),
        ('Sendratasik (FKIP)', 2.95, 83.3, (12, -8), 'left'),
        ('Ilmu Politik (FISIP)', 2.86, 83.6, (12, 12), 'left'),
        ('HI (FISIP)', 2.35, 91.2, (12, -8), 'left'),
        
        # Kuadran III (Kritis Kronis)
        ('Budidaya Perairan (FPK)', 0.94, 57.5, (14, -12), 'left'),
        ('Fisika (FMIPA)', 1.34, 56.4, (14, 10), 'left'),
        ('PSP Perikanan (FPK)', 1.09, 58.4, (-8, 14), 'center'),
        ('THP (FP)', 2.94, 63.8, (12, -8), 'left'),
        ('Pend. Matematika (FKIP)', 3.65, 66.6, (-12, 10), 'right'),
        ('Biologi (FMIPA)', 3.62, 71.9, (12, 10), 'left'),
        ('Teknik Pertanian (FP)', 3.34, 67.0, (12, -12), 'left'),
        ('Kehutanan (FP)', 3.30, 64.9, (-12, -12), 'right'),
        
        # Kuadran IV (Dilema Berulang)
        ('Akuntansi Perpajakan (FEB)', 14.22, 58.8, (12, 10), 'left'),
        ('Teknik Perminyakan (FT)', 8.64, 43.4, (12, 8), 'left'),
        ('Pend. Bhs Indonesia (FKIP)', 6.49, 79.5, (12, 8), 'left'),
        ('Pend. Guru PAUD (FKIP)', 5.46, 73.9, (-12, -14), 'right'),
        ('Teknik Mesin (FT)', 4.62, 78.2, (12, -10), 'left'),
        ('Agroteknologi (FP)', 4.14, 71.3, (12, 6), 'left')
    ]

    for label, px, py, (ox, oy), ha_align in key_annots_5y:
        ax.annotate(label, xy=(px, py), xytext=(ox, oy), textcoords='offset points',
                    ha=ha_align, va='center', fontsize=8.2, fontweight='bold', color='#0F172A',
                    bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#CBD5E1', linewidth=0.8, alpha=0.94),
                    arrowprops=dict(arrowstyle='->', color='#475569', lw=0.9, shrinkA=2, shrinkB=3),
                    zorder=5)

    ax.set_xlim(0, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_xlabel('Rata-rata Rasio Keketatan Seleksi 5 Tahun (2022–2026: Peminat/Kursi) -> Daya Tarik Pasar Struktural', 
                  fontsize=10.5, fontweight='bold', color='#0F172A', labelpad=10)
    ax.set_ylabel('Rata-rata Capacity Fill Rate 5 Tahun (2022–2026: %) -> Realisasi Keterisian Kuota Riil Jangka Panjang', 
                  fontsize=10.5, fontweight='bold', color='#0F172A', labelpad=10)
    ax.set_title('Peta Sebaran Longitudinal 66 Program Studi S1 Kampus Utama USK (Rata-rata 5 Tahun: 2022–2026)\nUkuran Bubble = Rata-rata Kapasitas Kuota Daya Tampung 5 Tahun (50 s.d. 450 Kursi)', 
                 fontsize=11.5, fontweight='bold', pad=12, color='#0F172A')
    ax.grid(True, linestyle=':', alpha=0.55, color='#94A3B8', zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#94A3B8')
    ax.spines['bottom'].set_color('#94A3B8')

    # Executive Cards 5Y
    cards_data_5y = [
        {
            'title': 'KUADRAN I: PRIMA & BINTANG KONSISTEN (28 PRODI | 42%)',
            'color_border': '#10B981', 'color_bg': '#ECFDF5', 'color_text': '#065F46',
            'desc': 'Demand Konsisten Tinggi (>=4,0x) & Kuota Penuh (>=80%)\nTahan banting terhadap fluktuasi kebijakan selama 5 tahun.',
            'examples': 'Farmasi, Informatika, Kedokteran, FKG, Psikologi, Hukum, PGSD.',
            'action': 'STRATEGI: Star Assets Berkelanjutan.\nInvestasi fasilitas laboratorium mutakhir,\nakreditasi internasional, dan ekspansi kelas internasional.'
        },
        {
            'title': 'KUADRAN II: STABIL & EFISIEN (4 PRODI | 6%)',
            'color_border': '#3B82F6', 'color_bg': '#EFF6FF', 'color_text': '#1E40AF',
            'desc': 'Demand Moderat (<4,0x) tapi Konsisten Terisi Penuh (>=80%)\nNiche market yang solid dan tidak terpengaruh tren sesaat.',
            'examples': 'Penjaskesrek, Pend. Sendratasik, Ilmu Politik, HI.',
            'action': 'STRATEGI: Niche Market Protection.\nJangan memaksakan menaikkan kuota.\nJaga stabilitas rasio dosen-mahasiswa & mutu lulusan.'
        },
        {
            'title': 'KUADRAN III: KRITIS & DEFISIT KRONIS (26 PRODI | 39%)',
            'color_border': '#EF4444', 'color_bg': '#FEF2F2', 'color_text': '#991B1B',
            'desc': 'Demand Lemah (<4,0x) & Kursi Kosong Kronis (<80%)\nBukan anomali 1 tahun! Terbukti defisit selama 5 tahun beruntun.',
            'examples': 'Budidaya Perairan, Fisika, PSP, THP, Pend. Matematika, Kehutanan.',
            'action': 'STRATEGI: Restrukturisasi / Pemangkasan Kuota Permanen.\nPangkas kuota 25%-40% secara permanen\nagar tidak terus menggerus akreditasi universitas.'
        },
        {
            'title': 'KUADRAN IV: DILEMA & BOCOR BERULANG (8 PRODI | 12%)',
            'color_border': '#F59E0B', 'color_bg': '#FFFBEB', 'color_text': '#92400E',
            'desc': 'Demand Tinggi (>=4,0x) tapi Keterisian Bocor Terus (<80%)\nMinat besar namun konversi daftar ulang selalu rontok.',
            'examples': 'Akuntansi Perpajakan, T. Perminyakan, PAUD, Sejarah, Agrotek.',
            'action': 'STRATEGI: Reformasi Biaya Kuliah & Cadangan Cepat.\nPerbaiki skema biaya/IPI jalur Mandiri dan percepat pemanggilan kuota cadangan sebelum registrasi ditutup.'
        }
    ]

    y_positions = [0.77, 0.52, 0.27, 0.02]
    box_height = 0.22

    for idx, c in enumerate(cards_data_5y):
        y = y_positions[idx]
        rect = FancyBboxPatch((0.01, y), 0.98, box_height, boxstyle='round,pad=0.025',
                              facecolor=c['color_bg'], edgecolor=c['color_border'], linewidth=1.5,
                              transform=ax_cards.transAxes, zorder=2)
        ax_cards.add_patch(rect)
        ax_cards.text(0.05, y + box_height - 0.032, c['title'],
                      fontsize=9.5, fontweight='bold', color=c['color_text'],
                      transform=ax_cards.transAxes, zorder=3)
        ax_cards.text(0.05, y + box_height - 0.075, c['desc'],
                      fontsize=8.3, color='#334155', linespacing=1.2,
                      transform=ax_cards.transAxes, zorder=3)
        ax_cards.text(0.05, y + box_height - 0.122, f"Prodi: {c['examples']}",
                      fontsize=8.0, fontstyle='italic', color='#475569',
                      transform=ax_cards.transAxes, zorder=3)
        ax_cards.text(0.05, y + 0.022, c['action'],
                      fontsize=8.3, fontweight='bold', color=c['color_text'], linespacing=1.2,
                      transform=ax_cards.transAxes, zorder=3)

    fig.suptitle('MATRIKS 4 KUADRAN PORTOFOLIO STRATEGIS 5 TAHUN PROGRAM STUDI S1 USK (2022–2026)\nPemetaan Longitudinal Bebas Bias: Daya Tarik Pasar (Demand) vs Realisasi Keterisian Kuota (Supply)',
                 fontsize=13.5, fontweight='bold', y=0.975, color='#0F172A')

    fig.subplots_adjust(left=0.075, right=0.985, top=0.89, bottom=0.075, wspace=0.15)
    plt.savefig(os.path.join(chart_dir, "13_matriks_4_kuadran_5_tahun_2022_2026.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 14: PANORAMA DINAMIKA JALUR MASUK & KEBOCORAN 5 TAHUN (2022–2026)
    # -------------------------------------------------------------
    print("[14/14] Generating 14_tren_jalur_masuk_dan_kebocoran_5_tahun_2022_2026.png...")
    jalurs_order = ['SNBT', 'SNBP', 'SMMPTN', 'TALENTA', 'SMC', 'ADIK']
    data_du_5y = {j: [] for j in jalurs_order}
    data_gugur_5y = {j: [] for j in jalurs_order}
    data_yield_5y = {j: [] for j in jalurs_order}
    tot_du_5y = []
    tot_gugur_5y = []

    for y in years:
        df_y = df_jalur_all[df_jalur_all['Tahun Akademik'] == y]
        grp_y = df_y.groupby('Jalur_Penerimaan').agg({
            'Daftar_Ulang': 'sum',
            'Lulus_Seleksi': 'sum',
            'Tidak_Daftar_Ulang': 'sum'
        }).to_dict(orient='index')
        
        y_du = 0
        y_gugur = 0
        for j in jalurs_order:
            if j in grp_y:
                du = grp_y[j]['Daftar_Ulang']
                lulus = grp_y[j]['Lulus_Seleksi']
                gugur = grp_y[j]['Tidak_Daftar_Ulang']
                y_rate = (du / lulus * 100.0) if lulus > 0 else np.nan
            else:
                du = 0
                gugur = 0
                y_rate = np.nan
            data_du_5y[j].append(du)
            data_gugur_5y[j].append(gugur)
            data_yield_5y[j].append(y_rate)
            y_du += du
            y_gugur += gugur
        tot_du_5y.append(y_du)
        tot_gugur_5y.append(y_gugur)

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 8.5), dpi=300)
    x_5y = np.arange(len(years))
    w_5y = 0.52

    # Panel 1: Evolusi Komposisi Mahasiswa Baru
    bottoms1 = np.zeros(len(years))
    for j in jalurs_order:
        vals = np.array(data_du_5y[j])
        ax1.bar(x_5y, vals, bottom=bottoms1, label=j, color=jalur_colors_map[j], width=w_5y, edgecolor='#FFFFFF', linewidth=1.0, zorder=2)
        for idx, (v, b) in enumerate(zip(vals, bottoms1)):
            if v >= 600:
                pct = v / tot_du_5y[idx] * 100.0
                ax1.text(idx, b + v/2.0, f"{v:,}\n({pct:.0f}%)", ha='center', va='center',
                         fontsize=8.8, fontweight='bold', color='#FFFFFF', zorder=3)
            elif v >= 150:
                ax1.text(idx, b + v/2.0, f"{v:,}", ha='center', va='center',
                         fontsize=8.0, fontweight='bold', color='#FFFFFF', zorder=3)
        bottoms1 += vals

    for idx, tot in enumerate(tot_du_5y):
        ax1.annotate(f"Total:\n{tot:,}", xy=(idx, tot), xytext=(0, 7), textcoords='offset points',
                     ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#0F172A',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#EFF6FF', edgecolor='#3B82F6', linewidth=1.0),
                     zorder=4)

    ax1.set_xticks(x_5y)
    ax1.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
    ax1.set_ylim(0, max(tot_du_5y) * 1.25)
    ax1.set_ylabel('Jumlah Mahasiswa Baru Daftar Ulang (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax1.set_title('A. Dinamika Serapan Mahasiswa Baru per Jalur (2022–2026)\nIntake Tumbuh +34.9% (6,197 → 8,361 Mahasiswa)', 
                  fontsize=12, fontweight='bold', pad=12, color='#1E40AF')
    ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.legend(loc='lower left', bbox_to_anchor=(0.02, 0.65), frameon=True, fontsize=9, framealpha=0.92)

    # Panel 2: Tren Yield Rate 5 Tahun
    markers_map = {'SNBT': 's', 'SNBP': 'o', 'SMMPTN': '^', 'TALENTA': 'D', 'SMC': 'v', 'ADIK': 'p'}
    for j in jalurs_order:
        y_vals = data_yield_5y[j]
        valid_pts = [(years[i], y_vals[i]) for i in range(len(years)) if not np.isnan(y_vals[i])]
        if valid_pts:
            vx, vy = zip(*valid_pts)
            lw = 3.0 if j in ['SNBP', 'SNBT', 'TALENTA', 'SMMPTN'] else 2.0
            ms = 8 if j in ['SNBP', 'SNBT', 'TALENTA', 'SMMPTN'] else 6
            ax2.plot(vx, vy, label=f"{j}", color=jalur_colors_map[j], marker=markers_map[j],
                     linewidth=lw, markersize=ms, zorder=4)
            for px, py in valid_pts:
                offset_y = 10 if j in ['SNBP', 'SNBT'] else -15 if j == 'TALENTA' and px == 2026 else 8
                ax2.annotate(f"{py:.1f}%", xy=(px, py), xytext=(0, offset_y), textcoords='offset points',
                             ha='center', va='center', fontsize=8.5, fontweight='bold', color=jalur_colors_map[j],
                             bbox=dict(boxstyle='round,pad=0.15', facecolor='#FFFFFF', edgecolor=jalur_colors_map[j], linewidth=0.7, alpha=0.9),
                             zorder=5)

    ax2.axhline(80.0, color='#64748B', linestyle='--', linewidth=1.5, alpha=0.85, label='Batas Standar Sehat (80%)', zorder=2)
    ax2.set_xticks(years)
    ax2.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
    ax2.set_ylim(15, 105)
    ax2.set_ylabel('Tingkat Konversi Registrasi (Yield Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax2.set_title('B. Tren Efisiensi Konversi Pendaftaran (Yield Rate 2022–2026)\nSorotan: Anjloknya Jalur TALENTA 2026 ke Titik Kritis 24.9%', 
                  fontsize=12, fontweight='bold', pad=12, color='#065F46')
    ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.legend(loc='lower left', frameon=True, fontsize=8.8, framealpha=0.92)

    ax2.annotate('CRASH KONVERSI TALENTA:\n935 dari 1,238 Calon Mhs\nMengundurkan Diri (75.1% Bocor)',
                 xy=(2026, 24.9), xytext=(2024.5, 34.0),
                 arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
                 fontsize=8.5, fontweight='bold', color='#991B1B',
                 bbox=dict(boxstyle='round,pad=0.3', facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=1.2),
                 zorder=6)

    # Panel 3: Eskalasi Kebocoran Calon Mhs Gugur 5 Tahun
    bottoms_g = np.zeros(len(years))
    for j in jalurs_order:
        vals_g = np.array(data_gugur_5y[j])
        ax3.bar(x_5y, vals_g, bottom=bottoms_g, label=j, color=jalur_colors_map[j], width=w_5y, edgecolor='#FFFFFF', linewidth=1.0, zorder=2)
        for idx, (v, b) in enumerate(zip(vals_g, bottoms_g)):
            if v >= 350:
                ax3.text(idx, b + v/2.0, f"{v:,}", ha='center', va='center',
                         fontsize=8.8, fontweight='bold', color='#FFFFFF', zorder=3)
            elif v >= 100:
                ax3.text(idx, b + v/2.0, f"{v:,}", ha='center', va='center',
                         fontsize=8.0, fontweight='bold', color='#FFFFFF', zorder=3)
        bottoms_g += vals_g

    for idx, tot in enumerate(tot_gugur_5y):
        ax3.annotate(f"Gugur:\n{tot:,}", xy=(idx, tot), xytext=(0, 7), textcoords='offset points',
                     ha='center', va='bottom', fontsize=10.5, fontweight='bold', color='#991B1B',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEF2F2', edgecolor='#EF4444', linewidth=1.0),
                     zorder=4)

    ax3.set_xticks(x_5y)
    ax3.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
    ax3.set_ylim(0, max(tot_gugur_5y) * 1.25)
    ax3.set_ylabel('Jumlah Calon Mahasiswa Mengundurkan Diri (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax3.set_title('C. Eskalasi Kebocoran Pendaftaran per Jalur (2022–2026)\nKebocoran Membengkak +94.9% (1,231 → 2,399 Calon Mhs)', 
                  fontsize=12, fontweight='bold', pad=12, color='#991B1B')
    ax3.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.legend(loc='upper left', frameon=True, fontsize=9, framealpha=0.92)

    plt.suptitle('PANORAMA DINAMIKA JALUR MASUK & ESKALASI KEBOCORAN PMB USK (2022–2026)\nAnalisis 5 Tahun: Pergeseran Kontribusi Intake Riil, Tren Yield Rate, dan Ledakan Calon Mahasiswa yang Mundur',
                 fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

    fig.tight_layout(rect=[0.01, 0.03, 0.99, 0.93])
    plt.savefig(os.path.join(chart_dir, "14_tren_jalur_masuk_dan_kebocoran_5_tahun_2022_2026.png"), dpi=300)
    plt.close()

    # -------------------------------------------------------------
    # CHART 15: MASTER 5-YEAR FACULTY TRAJECTORY HEATMAP & TRENDS
    # -------------------------------------------------------------
    print("[15/15] Generating 15_evaluasi_kinerja_fakultas_5_tahun_2022_2026.png...")
    for yr in years:
        fak_agg[f'FR_{yr}'] = (fak_agg[f'DU_{yr}'] / fak_agg[f'DT_{yr}'] * 100.0).round(1)
    fak_agg['Rata_FR_5Thn'] = (fak_agg['Rata_DU_5Thn'] / fak_agg['Rata_DT_5Thn'] * 100.0).round(1)

    fak_5y_sorted = fak_agg.sort_values('Rata_FR_5Thn', ascending=False).reset_index(drop=True)

    fig15, (ax_heat, ax_line) = plt.subplots(1, 2, figsize=(26, 9.5), dpi=300, gridspec_kw={'width_ratios': [1.12, 1.28]})

    # Panel 1: Heatmap 12 Fakultas x 5 Tahun
    matrix_data = fak_5y_sorted[['FR_2022', 'FR_2023', 'FR_2024', 'FR_2025', 'FR_2026', 'Rata_FR_5Thn']].values
    col_labels = ['2022', '2023', '2024', '2025', '2026', 'Rata 5-Thn']
    row_labels = fak_5y_sorted['Fakultas'].tolist()

    im = ax_heat.imshow(matrix_data, cmap=plt.cm.RdYlGn, norm=mcolors.Normalize(vmin=55, vmax=102), aspect='auto')

    ax_heat.set_xticks(np.arange(len(col_labels)))
    ax_heat.set_yticks(np.arange(len(row_labels)))
    ax_heat.set_xticklabels(col_labels, fontsize=11, fontweight='bold', color='#1E293B')
    ax_heat.set_yticklabels(row_labels, fontsize=11, fontweight='bold', color='#1E293B')
    ax_heat.set_title('A. Heatmap Keterisian Kuota 12 Fakultas (2022–2026)\nIdentifikasi Zona Hijau (Prima), Kuning (Rentan), & Merah Kronis', 
                      fontsize=12.5, fontweight='bold', pad=14, color='#065F46')

    for r in range(len(row_labels)):
        for c in range(len(col_labels)):
            val = matrix_data[r, c]
            tc = '#FFFFFF' if (val < 62 or val > 95) else '#0F172A'
            fw = 'bold' if c == 5 else 'normal'
            ax_heat.text(c, r, f"{val:.1f}%", ha='center', va='center', fontsize=9.5, fontweight=fw, color=tc)

    cbar = fig15.colorbar(im, ax=ax_heat, orientation='horizontal', pad=0.08, shrink=0.75)
    cbar.set_label('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=10, fontweight='bold')

    # Panel 2: Lintasan Tren 5 Tahun dengan Anti-Collision Spacing
    colors_faculty = {
        'Hukum': '#1E40AF', 'Kedokteran': '#047857', 'Kedokteran Gigi': '#0D9488',
        'Kedokteran Hewan': '#0284C7', 'Ekonomi dan Bisnis': '#4338CA', 'FISIP': '#6D28D9',
        'Keperawatan': '#B45309', 'Teknik': '#D97706', 'FKIP': '#EA580C', 'MIPA': '#E11D48',
        'Pertanian': '#C026D3', 'Kelautan dan Perikanan': '#DC2626'
    }

    raw_endpoints = []
    for _, r in fak_5y_sorted.iterrows():
        fak_name = r['Fakultas']
        y_trajectory = [r[f'FR_{yr}'] for yr in years]
        is_bottom = fak_name in ['Pertanian', 'Kelautan dan Perikanan']
        is_giant = fak_name in ['FKIP', 'Teknik', 'MIPA']
        lw = 3.2 if is_bottom or is_giant else 1.8
        alpha_val = 0.95 if is_bottom or is_giant else 0.75
        col = colors_faculty.get(fak_name, '#475569')
        
        ax_line.plot(years, y_trajectory, marker='o', linewidth=lw, alpha=alpha_val, color=col, 
                     label=f"{fak_name} ({r['Rata_FR_5Thn']:.1f}%)", zorder=4)
        raw_endpoints.append({'fak': fak_name, 'val': y_trajectory[-1], 'col': col})

    ax_line.axhline(80.0, color='#DC2626', linestyle='--', linewidth=2.0, alpha=0.85, label='Batas Keterisian Sehat (80%)', zorder=2)
    ax_line.axvspan(2022, 2026, ymin=0, ymax=(80-50)/(107-50), color='#FEF2F2', alpha=0.45, zorder=0)

    ax_line.set_xticks(years)
    ax_line.set_xticklabels([str(y) for y in years], fontsize=11, fontweight='bold', color='#1E293B')
    ax_line.set_ylim(50, 107)
    ax_line.set_xlim(2021.8, 2028.0)
    ax_line.set_ylabel('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax_line.set_title('B. Lintasan Historis Keterisian Kuota 12 Fakultas (2022–2026)\nMenyingkap Krisis 2023–2024 dan Pemulihan Rentan Menuju 2026', 
                      fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
    ax_line.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax_line.spines['top'].set_visible(False)
    ax_line.spines['right'].set_visible(False)

    raw_endpoints.sort(key=lambda x: x['val'])
    min_dist = 2.4
    adjusted_y = [ep['val'] for ep in raw_endpoints]

    for _ in range(15):
        for i in range(1, len(adjusted_y)):
            if adjusted_y[i] - adjusted_y[i-1] < min_dist:
                overlap = min_dist - (adjusted_y[i] - adjusted_y[i-1])
                adjusted_y[i] += overlap / 2.0
                adjusted_y[i-1] -= overlap / 2.0

    for ep, y_adj in zip(raw_endpoints, adjusted_y):
        if abs(y_adj - ep['val']) > 0.4:
            ax_line.plot([2026, 2026.25], [ep['val'], y_adj], color=ep['col'], linestyle=':', linewidth=0.9, alpha=0.8, zorder=4)
            x_text = 2026.3
        else:
            x_text = 2026.15
            
        ax_line.annotate(f"{ep['fak']}: {ep['val']:.1f}%", xy=(2026, ep['val']), xytext=(x_text, y_adj),
                         textcoords='data', va='center', ha='left', fontsize=8.4, fontweight='bold', color=ep['col'],
                         bbox=dict(boxstyle='round,pad=0.18', facecolor='#FFFFFF', edgecolor=ep['col'], linewidth=0.7, alpha=0.92),
                         zorder=5)

    ax_line.annotate('Anjloknya Pertanian (63.6%):\nTitik krisis pendaftaran 2023-2024',
                     xy=(2024, 63.6), xytext=(2022.6, 53.5),
                     arrowprops=dict(facecolor='#DC2626', edgecolor='#DC2626', shrink=0.08, width=1.5, headwidth=6),
                     fontsize=8.5, fontweight='bold', color='#991B1B',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#FEE2E2', edgecolor='#EF4444', linewidth=1.1),
                     zorder=6)

    plt.suptitle('PANORAMA EVALUASI LONGITUDINAL 5 TAHUN DAYA SERAP KUOTA 12 FAKULTAS USK (2022–2026)\nMenghilangkan Bias Titik Tunggal: Memetakan Konsistensi Fakultas Prima vs Krisis Kapasitas Kronis',
                 fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

    fig15.tight_layout(rect=[0.01, 0.02, 0.99, 0.93])
    fig15.savefig(os.path.join(chart_dir, "15_evaluasi_kinerja_fakultas_5_tahun_2022_2026.png"), dpi=300)
    plt.close(fig15)

    # -------------------------------------------------------------
    # CHART 16: DIAGNOSTIK KINERJA KUOTA TINGKAT PRODI (DUAL PANEL)
    # -------------------------------------------------------------
    print("[16/16] Generating 16_analisa_keterisian_dan_kursi_kosong_program_studi.png...")
    df_s1_c16 = df_s1.copy()
    df_s1_c16['Sisa_2026'] = df_s1_c16['DT_2026'] - df_s1_c16['DU_2026']
    df_s1_c16['FR_2026'] = (df_s1_c16['DU_2026'] / df_s1_c16['DT_2026'] * 100.0).round(1)
    df_s1_c16['Rata_FR_5Thn'] = (df_s1_c16['Rata_DU_5Thn'] / df_s1_c16['Rata_DT_5Thn'] * 100.0).round(1)

    def clean_prodi_c16(row):
        p = row['Program_Studi']
        f = row['Fakultas']
        fak_abbr = {
            'Kedokteran Gigi': 'FKG', 'Kedokteran': 'FK', 'Hukum': 'FH',
            'Kedokteran Hewan': 'FKH', 'Ekonomi dan Bisnis': 'FEB', 'FISIP': 'FISIP',
            'Keperawatan': 'FKep', 'Teknik': 'FT', 'FKIP': 'FKIP', 'MIPA': 'FMIPA',
            'Pertanian': 'FP', 'Kelautan dan Perikanan': 'FPK'
        }
        short_f = fak_abbr.get(f, f)
        p_title = p.title().replace('Pgsd', 'PGSD').replace('Pendidikan', 'Pend.').replace('Teknologi', 'Teknol.')
        return f"{p_title} ({short_f})"

    df_s1_c16['Label_Prodi'] = df_s1_c16.apply(clean_prodi_c16, axis=1)

    top15_sisa = df_s1_c16.sort_values('Sisa_2026', ascending=True).tail(15).reset_index(drop=True)
    bottom12_fr = df_s1_c16.sort_values('FR_2026', ascending=False).tail(12).reset_index(drop=True)
    top12_fr = df_s1_c16.sort_values('FR_2026', ascending=True).tail(12).reset_index(drop=True)

    fig16, (ax16_1, ax16_2) = plt.subplots(1, 2, figsize=(27, 11.5), dpi=300, gridspec_kw={'width_ratios': [1.22, 1.18]})

    # Panel 1: Top 15 Kursi Kosong Terbanyak
    y_pos1 = np.arange(len(top15_sisa))
    colors_sisa = ['#991B1B' if fr < 65.0 else '#D97706' if fr < 80.0 else '#2563EB' for fr in top15_sisa['FR_2026']]
    ax16_1.barh(y_pos1, top15_sisa['Sisa_2026'], color=colors_sisa, height=0.64, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

    ax16_1.set_yticks(y_pos1)
    ax16_1.set_yticklabels(top15_sisa['Label_Prodi'], fontsize=10.5, fontweight='bold', color='#1E293B')
    max_s1 = top15_sisa['Sisa_2026'].max()
    ax16_1.set_xlim(0, max_s1 * 1.65)
    ax16_1.set_ylim(-0.8, len(top15_sisa) - 0.2)
    ax16_1.set_xlabel('Jumlah Kursi Kosong Absolut (Bangku Tidak Terisi)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax16_1.set_title('A. Episentrum Kursi Kosong Terbesar per Program Studi (Tahun 2026)\n15 Prodi Ini Menyumbang 759 Kursi Kosong (48.4% dari Total Defisit 1,569 Kampus)', 
                     fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
    ax16_1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax16_1.spines['top'].set_visible(False)
    ax16_1.spines['right'].set_visible(False)

    for i, r in top15_sisa.iterrows():
        s_val = int(r['Sisa_2026'])
        du = int(r['DU_2026'])
        dt = int(r['DT_2026'])
        fr = r['FR_2026']
        r5 = r['Rata_FR_5Thn']
        
        badge_txt = f"{s_val} kursi kosong  |  Terisi: {du}/{dt} ({fr:.1f}%)  |  Rata 5-Thn: {r5:.1f}%"
        txt_c = '#991B1B' if fr < 65.0 else '#92400E' if fr < 80.0 else '#1E40AF'
        border_c = '#EF4444' if fr < 65.0 else '#F59E0B' if fr < 80.0 else '#3B82F6'
        bg_c = '#FEF2F2' if fr < 65.0 else '#FFFBEB' if fr < 80.0 else '#EFF6FF'
        
        ax16_1.annotate(badge_txt, xy=(s_val, i), xytext=(7, 0), textcoords='offset points',
                        va='center', ha='left', fontsize=8.6, fontweight='bold', color=txt_c,
                        bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.92),
                        zorder=4)

    legend_elements1 = [
        Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Keterisian Kritis (<65%) - Defisit Berat'),
        Patch(facecolor='#D97706', edgecolor='#0F172A', label='Keterisian Rentan (65%–79%) - Defisit Sedang'),
        Patch(facecolor='#2563EB', edgecolor='#0F172A', label='Keterisian Sehat (≥80%) tapi Kuota Terlampau Besar (Over-Ekspansi)')
    ]
    ax16_1.legend(handles=legend_elements1, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

    # Panel 2: Polaritas Keterisian Kuota
    combined_fr = pd.concat([bottom12_fr, top12_fr]).reset_index(drop=True)
    y_pos2 = np.arange(len(combined_fr))

    colors_fr2 = ['#DC2626' if i < 12 else '#059669' for i in range(len(combined_fr))]
    ax16_2.barh(y_pos2, combined_fr['FR_2026'], color=colors_fr2, height=0.64, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

    ax16_2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Batas Keterisian Sehat (80%)', zorder=3)
    ax16_2.axvspan(0, 80.0, color='#FEF2F2', alpha=0.35, zorder=0)

    ax16_2.axhline(11.5, color='#475569', linestyle='-', linewidth=1.2, alpha=0.75, zorder=3)
    ax16_2.annotate('JURANG POLARISASI PORTOFOLIO: Selisih Keterisian Ekstrem 30% s.d. 48%',
                    xy=(2, 11.5), xytext=(4, 11.5), textcoords='data', va='center', ha='left',
                    fontsize=8.5, fontweight='bold', color='#1E293B',
                    bbox=dict(boxstyle='square,pad=0.25', facecolor='#F1F5F9', edgecolor='#64748B', linewidth=0.8),
                    zorder=5)

    ax16_2.set_yticks(y_pos2)
    ax16_2.set_yticklabels(combined_fr['Label_Prodi'], fontsize=9.8, fontweight='bold', color='#1E293B')
    ax16_2.set_xlim(0, 148)
    ax16_2.set_ylim(-0.8, len(combined_fr) - 0.2)
    ax16_2.set_xlabel('Tingkat Keterisian Kuota (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax16_2.set_title('B. Polaritas Ekstrem Keterisian Kuota: 12 Bintang Penuh vs 12 Krisis Akut (2026)\nMembedah Polarisasi Daya Tarik Nyata Program Studi di Pasar Pendidikan', 
                     fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
    ax16_2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax16_2.spines['top'].set_visible(False)
    ax16_2.spines['right'].set_visible(False)

    for i, r in combined_fr.iterrows():
        fr = r['FR_2026']
        r5 = r['Rata_FR_5Thn']
        du = int(r['DU_2026'])
        dt = int(r['DT_2026'])
        
        badge_txt2 = f"{fr:.1f}% ({du}/{dt})  |  Rata 5-Thn: {r5:.1f}%"
        txt_c2 = '#991B1B' if fr < 80.0 else '#065F46'
        border_c2 = '#EF4444' if fr < 80.0 else '#10B981'
        bg_c2 = '#FEF2F2' if fr < 80.0 else '#F0FDF4'
        
        ax16_2.annotate(badge_txt2, xy=(fr, i), xytext=(7, 0), textcoords='offset points',
                        va='center', ha='left', fontsize=8.4, fontweight='bold', color=txt_c2,
                        bbox=dict(boxstyle='round,pad=0.20', facecolor=bg_c2, edgecolor=border_c2, linewidth=0.8, alpha=0.92),
                        zorder=4)

    legend_elements2 = [
        Patch(facecolor='#059669', edgecolor='#0F172A', label='Top 12 Prodi Prima (Penuh 95% s.d. 100%)'),
        Patch(facecolor='#DC2626', edgecolor='#0F172A', label='Bottom 12 Prodi Krisis Akut (Keterisian 52% s.d. 67%)'),
    ]
    ax16_2.legend(handles=legend_elements2, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

    plt.suptitle('DIAGNOSTIK MENDALAM DAYA SERAP & DEFISIT KUOTA TINGKAT PROGRAM STUDI S1 USK (2026)\nMenyentuh Akar Masalah: 15 Prodi Episentrum Kursi Kosong & Jurang Pemisah Bintang vs Krisis Akut',
                 fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

    fig16.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
    fig16.savefig(os.path.join(chart_dir, "16_analisa_keterisian_dan_kursi_kosong_program_studi.png"), dpi=300)
    plt.close(fig16)

    # -------------------------------------------------------------
    # CHART 17: PANORAMA 5 TAHUN KINERJA KUOTA PRODI (DUAL PANEL)
    # -------------------------------------------------------------
    print("[17/17] Generating 17_evaluasi_kinerja_program_studi_5_tahun_2022_2026.png...")
    df_s1_c17 = df_s1.copy()
    for y in years:
        df_s1_c17[f'Sisa_{y}'] = df_s1_c17[f'DT_{y}'] - df_s1_c17[f'DU_{y}']
        df_s1_c17[f'FR_{y}'] = (df_s1_c17[f'DU_{y}'] / df_s1_c17[f'DT_{y}'] * 100.0).round(1)

    df_s1_c17['Total_Sisa_5Thn'] = sum(df_s1_c17[f'Sisa_{y}'] for y in years)
    df_s1_c17['Total_DT_5Thn'] = sum(df_s1_c17[f'DT_{y}'] for y in years)
    df_s1_c17['Total_DU_5Thn'] = sum(df_s1_c17[f'DU_{y}'] for y in years)
    df_s1_c17['Rata_FR_5Thn'] = (df_s1_c17['Total_DU_5Thn'] / df_s1_c17['Total_DT_5Thn'] * 100.0).round(1)
    df_s1_c17['Label_Prodi'] = df_s1_c17.apply(clean_prodi_c16, axis=1)

    top15_sisa_5y = df_s1_c17.sort_values('Total_Sisa_5Thn', ascending=True).tail(15).reset_index(drop=True)
    df_est_c17 = df_s1_c17[df_s1_c17['DT_2022'] > 0].copy()
    bottom12_fr_5y = df_est_c17.sort_values('Rata_FR_5Thn', ascending=False).tail(12).reset_index(drop=True)
    top12_fr_5y = df_est_c17.sort_values('Rata_FR_5Thn', ascending=True).tail(12).reset_index(drop=True)

    fig17, (ax17_1, ax17_2) = plt.subplots(1, 2, figsize=(27, 11.5), dpi=300, gridspec_kw={'width_ratios': [1.22, 1.18]})

    # Panel 1: Top 15 Akumulasi Kursi Kosong 5 Tahun
    y_pos1_17 = np.arange(len(top15_sisa_5y))
    colors_sisa_17 = ['#991B1B' if fr < 65.0 else '#D97706' if fr < 80.0 else '#2563EB' for fr in top15_sisa_5y['Rata_FR_5Thn']]
    ax17_1.barh(y_pos1_17, top15_sisa_5y['Total_Sisa_5Thn'], color=colors_sisa_17, height=0.64, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

    ax17_1.set_yticks(y_pos1_17)
    ax17_1.set_yticklabels(top15_sisa_5y['Label_Prodi'], fontsize=10.5, fontweight='bold', color='#1E293B')
    max_s1_17 = top15_sisa_5y['Total_Sisa_5Thn'].max()
    ax17_1.set_xlim(0, max_s1_17 * 1.65)
    ax17_1.set_ylim(-0.8, len(top15_sisa_5y) - 0.2)
    ax17_1.set_xlabel('Akumulasi Kursi Kosong 5 Tahun (Bangku Terbuang 2022–2026)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax17_1.set_title('A. Akumulasi Kursi Kosong 5 Tahun per Program Studi (2022–2026)\n15 Prodi Ini Menyumbang 3,850 Kursi Kosong (43.4% dari Total Defisit 8,881 Kampus)', 
                     fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
    ax17_1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax17_1.spines['top'].set_visible(False)
    ax17_1.spines['right'].set_visible(False)

    for i, r in top15_sisa_5y.iterrows():
        s_val = int(r['Total_Sisa_5Thn'])
        du = int(r['Total_DU_5Thn'])
        dt = int(r['Total_DT_5Thn'])
        fr = r['Rata_FR_5Thn']
        
        badge_txt = f"{s_val} kursi kosong (5 Thn)  |  Rata Keterisian: {fr:.1f}%  |  Total Terisi: {du}/{dt}"
        txt_c = '#991B1B' if fr < 65.0 else '#92400E' if fr < 80.0 else '#1E40AF'
        border_c = '#EF4444' if fr < 65.0 else '#F59E0B' if fr < 80.0 else '#3B82F6'
        bg_c = '#FEF2F2' if fr < 65.0 else '#FFFBEB' if fr < 80.0 else '#EFF6FF'
        
        ax17_1.annotate(badge_txt, xy=(s_val, i), xytext=(7, 0), textcoords='offset points',
                        va='center', ha='left', fontsize=8.6, fontweight='bold', color=txt_c,
                        bbox=dict(boxstyle='round,pad=0.22', facecolor=bg_c, edgecolor=border_c, linewidth=0.8, alpha=0.92),
                        zorder=4)

    legend_elements1_17 = [
        Patch(facecolor='#991B1B', edgecolor='#0F172A', label='Rata-rata 5-Thn Kritis (<65%) - Defisit Kronis'),
        Patch(facecolor='#D97706', edgecolor='#0F172A', label='Rata-rata 5-Thn Rentan (65%–79%) - Defisit Sedang'),
        Patch(facecolor='#2563EB', edgecolor='#0F172A', label='Rata-rata 5-Thn Sehat (≥80%) tapi Kuota Kumulatif Sangat Besar')
    ]
    ax17_1.legend(handles=legend_elements1_17, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

    # Panel 2: Polaritas Keterisian Rata-rata 5 Tahun
    combined_fr_5y = pd.concat([bottom12_fr_5y, top12_fr_5y]).reset_index(drop=True)
    y_pos2_17 = np.arange(len(combined_fr_5y))

    colors_fr2_17 = ['#DC2626' if i < 12 else '#059669' for i in range(len(combined_fr_5y))]
    ax17_2.barh(y_pos2_17, combined_fr_5y['Rata_FR_5Thn'], color=colors_fr2_17, height=0.64, alpha=0.9, edgecolor='#0F172A', linewidth=1.0, zorder=2)

    ax17_2.axvline(80.0, color='#DC2626', linestyle='--', linewidth=1.8, label='Batas Keterisian Sehat (80%)', zorder=3)
    ax17_2.axvspan(0, 80.0, color='#FEF2F2', alpha=0.35, zorder=0)

    ax17_2.axhline(11.5, color='#475569', linestyle='-', linewidth=1.2, alpha=0.75, zorder=3)
    ax17_2.annotate('JURANG POLARISASI HISTORIS 5 TAHUN: Bintang Konsisten vs Penyakit Kronis',
                    xy=(2, 11.5), xytext=(4, 11.5), textcoords='data', va='center', ha='left',
                    fontsize=8.5, fontweight='bold', color='#1E293B',
                    bbox=dict(boxstyle='square,pad=0.25', facecolor='#F1F5F9', edgecolor='#64748B', linewidth=0.8),
                    zorder=5)

    ax17_2.set_yticks(y_pos2_17)
    ax17_2.set_yticklabels(combined_fr_5y['Label_Prodi'], fontsize=9.8, fontweight='bold', color='#1E293B')
    ax17_2.set_xlim(0, 148)
    ax17_2.set_ylim(-0.8, len(combined_fr_5y) - 0.2)
    ax17_2.set_xlabel('Rata-rata Tingkat Keterisian Kuota 5 Tahun (Fill Rate %)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax17_2.set_title('B. Polaritas Historis 5 Tahun: 12 Bintang Konsisten vs 12 Krisis Kronis (2022–2026)\nMenghilangkan Bias 1 Tahun: Membuktikan Kinerja Reputasi Jangka Panjang Program Studi', 
                     fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
    ax17_2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax17_2.spines['top'].set_visible(False)
    ax17_2.spines['right'].set_visible(False)

    for i, r in combined_fr_5y.iterrows():
        fr = r['Rata_FR_5Thn']
        du = int(r['Total_DU_5Thn'])
        dt = int(r['Total_DT_5Thn'])
        s_tot = int(r['Total_Sisa_5Thn'])
        
        badge_txt2 = f"Rata 5-Thn: {fr:.1f}%  |  Total Terisi: {du}/{dt}  |  Kosong: {s_tot} kursi"
        txt_c2 = '#991B1B' if fr < 80.0 else '#065F46'
        border_c2 = '#EF4444' if fr < 80.0 else '#10B981'
        bg_c2 = '#FEF2F2' if fr < 80.0 else '#F0FDF4'
        
        ax17_2.annotate(badge_txt2, xy=(fr, i), xytext=(7, 0), textcoords='offset points',
                        va='center', ha='left', fontsize=8.4, fontweight='bold', color=txt_c2,
                        bbox=dict(boxstyle='round,pad=0.20', facecolor=bg_c2, edgecolor=border_c2, linewidth=0.8, alpha=0.92),
                        zorder=4)

    legend_elements2_17 = [
        Patch(facecolor='#059669', edgecolor='#0F172A', label='Top 12 Prodi Konsisten Prima (Rata 5-Thn 92% s.d. 99%)'),
        Patch(facecolor='#DC2626', edgecolor='#0F172A', label='Bottom 12 Prodi Krisis Kronis (Rata 5-Thn 42% s.d. 65%)'),
    ]
    ax17_2.legend(handles=legend_elements2_17, loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2, frameon=True, fontsize=8.8, framealpha=0.95)

    plt.suptitle('PANORAMA LONGITUDINAL 5 TAHUN KINERJA KUOTA PROGRAM STUDI S1 USK (2022–2026)\nMenghilangkan Bias Titik Tunggal: Membedah Akumulasi 8,881 Bangku Kosong & Konsistensi Reputasi Pasar',
                 fontsize=14.5, fontweight='bold', y=0.985, color='#0F172A')

    fig17.tight_layout(rect=[0.01, 0.05, 0.99, 0.94])
    fig17.savefig(os.path.join(chart_dir, "17_evaluasi_kinerja_program_studi_5_tahun_2022_2026.png"), dpi=300)
    plt.close(fig17)

    print("All charts successfully created!")

if __name__ == "__main__":
    main()

