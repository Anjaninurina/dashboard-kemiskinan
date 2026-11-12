import pandas as pd
import streamlit as st

PERIODE_MISKIN = {'Maret': 'kemiskinan_maret', 'September': 'kemiskinan_sept'}
PERIODE_TPT = {'Februari': 'tpt_feb', 'Agustus': 'tpt_agt'}
NAMA = {
    'kemiskinan': 'Penduduk miskin (%)',
    'ipm': 'IPM (indeks)',
    'tpt': 'TPT (%)',
    'rls': 'RLS (tahun)',
}

@st.cache_data
def muat_data():
    prov = pd.read_csv('data/data_bersih.csv')
    nas = pd.read_csv('data/nasional.csv').iloc[0]
    return prov, nas 

def pilih_periode(df, periode_miskin, periode_tpt):
    return pd.DataFrame({
        'provinsi': df['provinsi'],
        'kemiskinan': df[PERIODE_MISKIN[periode_miskin]],
        'ipm': df['ipm'],
        'tpt': df[PERIODE_TPT[periode_tpt]],
        'rls': df['rls'],
    })

def nasional_periode(nas, periode_miskin, periode_tpt):
    return {
        'kemiskinan': nas[PERIODE_MISKIN[periode_miskin]],
        'ipm': nas['ipm'],
        'tpt': nas[PERIODE_TPT[periode_tpt]],
        'rls': nas['rls'],
    }

def ringkasan(df, kolom):
    seri = df.set_index('provinsi')[kolom].dropna()
    return {
        'rata': seri.mean(),
        'tertinggi': (seri.idxmax(), seri.max()),
        'terendah': (seri.idxmin(), seri.min()),
    }

def hitung_korelasi(df, x, y):
    data = df[[x, y]].dropna()
    return data[x].corr(data[y]), len(data)

def interpretasi(r):
    a = abs(r)
    kekuatan = 'lemah' if a < 0.3 else 'sedang' if a < 0.7 else 'kuat'
    arah = 'positif' if r > 0 else 'negatif'
    return 'Hubungan ' + kekuatan + ' dan ' + arah + '.'