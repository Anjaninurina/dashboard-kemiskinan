from utils import (muat_data, pilih_periode, nasional_periode,
                   ringkasan, hitung_korelasi, interpretasi)

prov, nas = muat_data()
print('Jumlah provinsi:', len(prov), '(harus 38)')

df = pilih_periode(prov, 'September', 'Agustus')
print('Nasional:', nasional_periode(nas, 'September', 'Agustus'))

for kode in ['kemiskinan', 'ipm', 'tpt', 'rls']:
    print(kode, ringkasan(df, kode))

r, n = hitung_korelasi(df, 'kemiskinan', 'ipm')
print('r kemiskinan dan IPM:', round(r, 3), '| n =', n)
print(interpretasi(r))