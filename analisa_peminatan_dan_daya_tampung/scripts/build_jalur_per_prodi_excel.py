import os
import pandas as pd
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))
base_data_dir = os.path.abspath(os.path.join(script_dir, '..', 'data'))
excel_master = os.path.join(base_data_dir, 'master_analisa_peminatan_dan_daya_tampung_2022_2026.xlsx')
out_excel = os.path.join(base_data_dir, 'analisa_jalur_masuk_dan_kebocoran_per_prodi_2022_2026.xlsx')

print("Loading data from master Excel...")
df_all = pd.read_excel(excel_master, sheet_name='Rincian_Jalur_Semua_Tahun')
years = [2022, 2023, 2024, 2025, 2026]
jalurs = ['SNBP', 'SNBT', 'SMMPTN', 'TALENTA', 'SMC', 'ADIK']

writer = pd.ExcelWriter(out_excel, engine='openpyxl')

# -------------------------------------------------------------
# SHEET 1: RINGKASAN MAKRO JALUR TAHUNAN & 5 TAHUN
# -------------------------------------------------------------
print("Creating Sheet 1: Ringkasan_Makro_Jalur...")
rekap_makro = []
for yr in years:
    df_yr = df_all[df_all['Tahun Akademik'] == yr]
    for j in df_yr['Jalur Penerimaan'].unique():
        sub = df_yr[df_yr['Jalur Penerimaan'] == j]
        pem = sub['Jumlah Peminat'].sum()
        dt = sub['Target Daya Tampung'].sum()
        lulus = sub['Calon Lulus Seleksi'].sum()
        du = sub['Mahasiswa Daftar Ulang'].sum()
        gugur = sub['Mundur / Gugur'].sum()
        y_rate = round(du / lulus * 100, 1) if lulus > 0 else 0
        d_rate = round(gugur / lulus * 100, 1) if lulus > 0 else 0
        rekap_makro.append({
            'Tahun': yr,
            'Jalur Penerimaan': j,
            'Jumlah Peminat': pem,
            'Target Daya Tampung': dt,
            'Calon Lulus Seleksi': lulus,
            'Mahasiswa Daftar Ulang': du,
            'Mundur / Gugur': gugur,
            'Yield Rate (%)': y_rate,
            'Tingkat Kebocoran (%)': d_rate
        })

df_makro = pd.DataFrame(rekap_makro)

# Add 5-year macro total per jalur
rekap_5y_makro = []
for j in jalurs:
    sub = df_all[df_all['Jalur Penerimaan'] == j]
    if len(sub) > 0:
        pem = sub['Jumlah Peminat'].sum()
        dt = sub['Target Daya Tampung'].sum()
        lulus = sub['Calon Lulus Seleksi'].sum()
        du = sub['Mahasiswa Daftar Ulang'].sum()
        gugur = sub['Mundur / Gugur'].sum()
        y_rate = round(du / lulus * 100, 1) if lulus > 0 else 0
        d_rate = round(gugur / lulus * 100, 1) if lulus > 0 else 0
        rekap_5y_makro.append({
            'Tahun': 'Total 5-Tahun (2022-2026)',
            'Jalur Penerimaan': j,
            'Jumlah Peminat': pem,
            'Target Daya Tampung': dt,
            'Calon Lulus Seleksi': lulus,
            'Mahasiswa Daftar Ulang': du,
            'Mundur / Gugur': gugur,
            'Yield Rate (%)': y_rate,
            'Tingkat Kebocoran (%)': d_rate
        })
df_makro = pd.concat([df_makro, pd.DataFrame(rekap_5y_makro)], ignore_index=True)
df_makro.to_excel(writer, sheet_name='Ringkasan_Makro_Jalur', index=False)

# -------------------------------------------------------------
# SHEET 2: PIVOT 5 TAHUN PER PRODI (DAFTAR ULANG & KEBOCORAN)
# -------------------------------------------------------------
print("Creating Sheet 2: Pivot_5Thn_Per_Prodi...")
# Group by prodi across 5 years
prodi_list = df_all[['Fakultas', 'Nama Program Studi', 'Jenjang']].drop_duplicates().sort_values(by=['Fakultas', 'Nama Program Studi'])

rows_pivot = []
for _, p in prodi_list.iterrows():
    fak = p['Fakultas']
    nm = p['Nama Program Studi']
    jnj = p['Jenjang']
    
    sub = df_all[(df_all['Fakultas'] == fak) & (df_all['Nama Program Studi'] == nm) & (df_all['Jenjang'] == jnj)]
    
    row = {
        'Fakultas': fak,
        'Nama Program Studi': nm,
        'Jenjang': jnj
    }
    
    # Fill DU per jalur
    total_du = 0
    total_lulus = 0
    total_gugur = 0
    du_dict = {}
    
    for j in jalurs:
        sub_j = sub[sub['Jalur Penerimaan'] == j]
        du_val = sub_j['Mahasiswa Daftar Ulang'].sum()
        gugur_val = sub_j['Mundur / Gugur'].sum()
        lulus_val = sub_j['Calon Lulus Seleksi'].sum()
        
        row[f'DU_{j}'] = du_val
        row[f'Gugur_{j}'] = gugur_val
        
        total_du += du_val
        total_gugur += gugur_val
        total_lulus += lulus_val
        du_dict[j] = du_val
        
    row['Total_DU_5Thn'] = total_du
    row['Total_Gugur_5Thn'] = total_gugur
    row['Total_Lulus_5Thn'] = total_lulus
    row['Yield_Rate_5Thn (%)'] = round(total_du / total_lulus * 100, 1) if total_lulus > 0 else 0
    row['Tingkat_Kebocoran_5Thn (%)'] = round(total_gugur / total_lulus * 100, 1) if total_lulus > 0 else 0
    
    # Find dominant intake pathway
    if total_du > 0:
        max_j = max(du_dict, key=du_dict.get)
        pct_dom = round(du_dict[max_j] / total_du * 100, 1)
        row['Jalur_Dominan'] = f"{max_j} ({pct_dom}%)"
    else:
        row['Jalur_Dominan'] = "-"
        
    rows_pivot.append(row)

df_pivot_5y = pd.DataFrame(rows_pivot)
df_pivot_5y.to_excel(writer, sheet_name='Pivot_5Thn_Per_Prodi', index=False)

# -------------------------------------------------------------
# SHEET 3: REKAP 5 TAHUN DETAIL PER PRODI PER JALUR
# -------------------------------------------------------------
print("Creating Sheet 3: Detail_5Thn_Prodi_Jalur...")
df_5y_detail = df_all.groupby(['Fakultas', 'Nama Program Studi', 'Jenjang', 'Jalur Penerimaan']).agg({
    'Jumlah Peminat': 'sum',
    'Target Daya Tampung': 'sum',
    'Calon Lulus Seleksi': 'sum',
    'Mahasiswa Daftar Ulang': 'sum',
    'Mundur / Gugur': 'sum'
}).reset_index()

df_5y_detail['Yield Rate (%)'] = (df_5y_detail['Mahasiswa Daftar Ulang'] / df_5y_detail['Calon Lulus Seleksi'].replace(0, 1) * 100).round(1)
df_5y_detail['Tingkat Kebocoran (%)'] = (df_5y_detail['Mundur / Gugur'] / df_5y_detail['Calon Lulus Seleksi'].replace(0, 1) * 100).round(1)
df_5y_detail = df_5y_detail.sort_values(by=['Fakultas', 'Nama Program Studi', 'Jalur Penerimaan'])
df_5y_detail.to_excel(writer, sheet_name='Detail_5Thn_Prodi_Jalur', index=False)

# -------------------------------------------------------------
# SHEETS 4-8: DETAIL TAHUNAN (2022 s.d. 2026)
# -------------------------------------------------------------
for yr in [2026, 2025, 2024, 2023, 2022]:
    print(f"Creating Sheet: Rincian_Tahun_{yr}...")
    df_yr = df_all[df_all['Tahun Akademik'] == yr].copy()
    df_yr = df_yr.sort_values(by=['Fakultas', 'Nama Program Studi', 'Jalur Penerimaan'])
    cols_order = ['Tahun Akademik', 'Fakultas', 'Nama Program Studi', 'Jenjang', 'Jalur Penerimaan', 
                  'Jumlah Peminat', 'Target Daya Tampung', 'Calon Lulus Seleksi', 'Mahasiswa Daftar Ulang', 
                  'Mundur / Gugur', 'Yield Rate (%)']
    existing_cols = [c for c in cols_order if c in df_yr.columns]
    df_yr[existing_cols].to_excel(writer, sheet_name=f'Rincian_Tahun_{yr}', index=False)

writer.close()
print("Excel workbook successfully created at:", out_excel)
