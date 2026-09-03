import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

# Set high-quality styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94A3B8'
plt.rcParams['axes.linewidth'] = 1.0

excel_path = 'tugas-5/analisa_peminatan_dan_daya_tampung/data/master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx'
chart_dir = 'tugas-5/analisa_peminatan_dan_daya_tampung/grafik'
df_all = pd.read_excel(excel_path, sheet_name='Rincian_Jalur_Semua_Tahun')

# Consistent Brand Colors for Jalur
jalur_colors = {
    'SNBT': '#1D4ED8',      # Royal Blue
    'SNBP': '#059669',      # Emerald Green
    'SMMPTN': '#EA580C',    # Amber / Orange
    'TALENTA': '#7C3AED',   # Royal Purple
    'SMC': '#0D9488',       # Dark Teal
    'ADIK': '#64748B'       # Slate Gray
}

leak_colors = {
    'SNBT': '#93C5FD',
    'SNBP': '#A7F3D0',
    'SMMPTN': '#FDBA74',
    'TALENTA': '#C4B5FD',
    'SMC': '#99F6E4',
    'ADIK': '#CBD5E1'
}

# -------------------------------------------------------------
# 1. GENERATE ANNUAL CHARTS (2022, 2023, 2024, 2025, 2026)
# -------------------------------------------------------------
for yr in [2022, 2023, 2024, 2025, 2026]:
    df_yr = df_all[df_all['Tahun Akademik'] == yr]
    grp = df_yr.groupby('Jalur Penerimaan').agg({
        'Mahasiswa Daftar Ulang': 'sum',
        'Calon Lulus Seleksi': 'sum',
        'Mundur / Gugur': 'sum',
        'Target Daya Tampung': 'sum',
        'Jumlah Peminat': 'sum'
    }).reset_index()

    tot_du = grp['Mahasiswa Daftar Ulang'].sum()
    tot_gugur = grp['Mundur / Gugur'].sum()
    tot_lulus = grp['Calon Lulus Seleksi'].sum()
    overall_yield = (tot_du / tot_lulus * 100.0) if tot_lulus > 0 else 0

    grp['Share_DU'] = grp['Mahasiswa Daftar Ulang'] / tot_du * 100.0
    grp['Yield_Rate'] = grp['Mahasiswa Daftar Ulang'] / grp['Calon Lulus Seleksi'] * 100.0

    # Sort descending by Mahasiswa Daftar Ulang
    grp = grp.sort_values('Mahasiswa Daftar Ulang', ascending=False).reset_index(drop=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), dpi=300)

    # Panel 1: Kontribusi Mahasiswa Masuk Riil (Daftar Ulang)
    x = np.arange(len(grp))
    bar_cols = [jalur_colors.get(j, '#3B82F6') for j in grp['Jalur Penerimaan']]
    bars1 = ax1.bar(x, grp['Mahasiswa Daftar Ulang'], color=bar_cols, width=0.55, edgecolor='#0F172A', linewidth=1.1, zorder=2)

    ax1.set_xticks(x)
    ax1.set_xticklabels(grp['Jalur Penerimaan'], fontsize=11, fontweight='bold', color='#1E293B')
    max_du = grp['Mahasiswa Daftar Ulang'].max()
    ax1.set_ylim(0, max_du * 1.25)  # Generous headroom (+25%)
    ax1.set_ylabel('Jumlah Mahasiswa Daftar Ulang (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax1.set_title(f'A. Kontribusi Mahasiswa Masuk Riil per Jalur ({yr})\nTotal Registrasi: {tot_du:,} Mahasiswa', 
                  fontsize=12.5, fontweight='bold', pad=12, color='#1E40AF')
    ax1.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)

    for i, r in grp.iterrows():
        du_val = int(r['Mahasiswa Daftar Ulang'])
        share_val = r['Share_DU']
        ax1.annotate(f"{du_val:,} mhs\n({share_val:.1f}%)", xy=(i, du_val), xytext=(0, 7), textcoords='offset points',
                     ha='center', va='bottom', fontsize=10, fontweight='bold', color='#0F172A',
                     bbox=dict(boxstyle='round,pad=0.25', facecolor='#F8FAFC', edgecolor='#CBD5E1', linewidth=0.8, alpha=0.95),
                     zorder=4)

    # Panel 2: Kebocoran Calon Mahasiswa (Gugur / Mundur) & Yield Rate
    # Sort panel 2 by Mundur / Gugur descending
    grp_leak = grp.sort_values('Mundur / Gugur', ascending=False).reset_index(drop=True)
    x2 = np.arange(len(grp_leak))
    leak_c = ['#EF4444' if r['Yield_Rate'] < 65.0 else '#F59E0B' if r['Yield_Rate'] < 80.0 else '#3B82F6' for _, r in grp_leak.iterrows()]
    bars2 = ax2.bar(x2, grp_leak['Mundur / Gugur'], color=leak_c, alpha=0.85, width=0.55, edgecolor='#7F1D1D', linewidth=1.1, zorder=2)

    ax2.set_xticks(x2)
    ax2.set_xticklabels(grp_leak['Jalur Penerimaan'], fontsize=11, fontweight='bold', color='#1E293B')
    max_leak = grp_leak['Mundur / Gugur'].max()
    ax2.set_ylim(0, max_leak * 1.25)  # Generous headroom (+25%)
    ax2.set_ylabel('Jumlah Calon Mahasiswa Mengundurkan Diri (Orang)', fontsize=11, fontweight='bold', color='#0F172A', labelpad=10)
    ax2.set_title(f'B. Tingkat Kebocoran & Konversi Pendaftaran per Jalur ({yr})\nTotal Gugur: {tot_gugur:,} Orang | Rata-rata Yield Rate: {overall_yield:.1f}%', 
                  fontsize=12.5, fontweight='bold', pad=12, color='#991B1B')
    ax2.grid(True, linestyle='--', alpha=0.4, color='#CBD5E1', zorder=0)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)

    for i, r in grp_leak.iterrows():
        leak_val = int(r['Mundur / Gugur'])
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
    print(f"Generated {out_name}")

print("All annual charts created successfully.")
