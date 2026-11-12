import pandas as pd
import streamlit as st
import plotly.express as px
from utils import (NAMA, muat_data, pilih_periode, nasional_periode,
                   ringkasan, hitung_korelasi, interpretasi)

st.set_page_config(page_title='Dashboard Kemiskinan Indonesia 2024', layout='wide')

prov, nas = muat_data()

st.title('Dashboard Kemiskinan Indonesia 2024')
st.caption('Sumber: Badan Pusat Statistik (BPS), 2024. Kemiskinan, IPM, TPT, dan RLS tingkat provinsi.')

# Sidebar: filter
st.sidebar.header('Filter')
pilihan_prov = st.sidebar.selectbox('Provinsi', ['Semua provinsi'] + sorted(prov['provinsi']))
periode_miskin = st.sidebar.radio('Periode kemiskinan', ['September', 'Maret'])
periode_tpt = st.sidebar.radio('Periode TPT', ['Agustus', 'Februari'])

df = pilih_periode(prov, periode_miskin, periode_tpt)
nasional = nasional_periode(nas, periode_miskin, periode_tpt)

def fmt(x):
    return 'tidak tersedia' if pd.isna(x) else f'{x:.2f}'

# Kartu ringkasan
for kol, kode in zip(st.columns(4), ['kemiskinan', 'ipm', 'tpt', 'rls']):
    r = ringkasan(df, kode)
    if pilihan_prov == 'Semua provinsi':
        nilai = r['rata']
        ket = 'Rata-rata 38 provinsi'
    else:
        nilai = df.loc[df['provinsi'] == pilihan_prov, kode].iloc[0]
        ket = pilihan_prov
    kol.metric(NAMA[kode], fmt(nilai))
    kol.caption(ket + '. Nasional: ' + fmt(nasional[kode]))
    kol.caption('Tertinggi: ' + r['tertinggi'][0] + '. Terendah: ' + r['terendah'][0] + '.')

tab1, tab2, tab3, tab4 = st.tabs(['Ringkasan', 'Korelasi', 'Data', 'Tentang Data'])