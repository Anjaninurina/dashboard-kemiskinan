import pandas as pd

def norm(nama):
    return str(nama).strip().upper().replace('KEPULAUAN', 'KEP.')

# Kemiskinan: header di baris 1, ada 1 kolom kosong di ujung, metadata di bawah baris INDONESIA
k = pd.read_excel('data/raw/kemiskinan.xlsx').iloc[:, :7]
k.columns = ['provinsi', 'garis_maret', 'garis_sept',
             'jumlah_miskin_maret', 'jumlah_miskin_sept',
             'kemiskinan_maret', 'kemiskinan_sept']
baris_akhir = k.index[k['provinsi'].astype(str).str.strip().str.upper() == 'INDONESIA'][0]
k = k.iloc[:baris_akhir + 1]

# IPM dan RLS: 3 baris judul, lalu dua kolom (provinsi, nilai)
ipm = pd.read_excel('data/raw/ipm.xlsx', header=None, skiprows=3, names=['provinsi', 'ipm'])
rls = pd.read_excel('data/raw/rls.xlsx', header=None, skiprows=3, names=['provinsi', 'rls'])

# TPT: 3 baris judul + 1 baris header (Februari, Agustus, Tahunan)
tpt = pd.read_excel('data/raw/tpt.xlsx', header=None, skiprows=4,
                    names=['provinsi', 'tpt_feb', 'tpt_agt', 'tpt_tahunan']).drop(columns='tpt_tahunan')

# Seragamkan nama provinsi dan ubah ke angka ('...' dan '-' menjadi kosong)
for df in (k, ipm, tpt, rls):
    df['provinsi'] = df['provinsi'].map(norm)
    for kolom in df.columns.drop('provinsi'):
        df[kolom] = pd.to_numeric(df[kolom], errors='coerce')

gabung = (k.merge(ipm, on='provinsi', how='outer')
           .merge(tpt, on='provinsi', how='outer')
           .merge(rls, on='provinsi', how='outer'))

prov = gabung[gabung['provinsi'] != 'INDONESIA']
nas = gabung[gabung['provinsi'] == 'INDONESIA']

# Pemeriksaan
print('Total baris:', len(gabung), '(harus 39)')
print('Provinsi:', len(prov), '| sel kosong:', prov.isna().sum().sum(), '(harus 38 dan 6)')
bermasalah = prov[prov[['kemiskinan_maret', 'ipm', 'tpt_feb', 'rls']].isna().any(axis=1)]
print('Provinsi bermasalah (harus kosong):', bermasalah['provinsi'].tolist())

prov.to_csv('data/data_bersih.csv', index=False)
nas.to_csv('data/nasional.csv', index=False)
print('Selesai: data_bersih.csv dan nasional.csv dibuat.')