import streamlit as st
import pandas as pd
import pycountry

def extract_country(text):
    countries = [country.name for country in pycountry.countries]
    for country in countries:
        if country.lower() in text.lower():
            return country
    return ""

st.set_page_config(page_title="Country Extractor", layout="wide")
st.title("Excel'den Ülke Çıkarıcı Web Paneli")

uploaded_file = st.file_uploader("Excel dosyasını yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    if "Görüşme Notu" in df.columns:
        df["Ülke"] = df["Görüşme Notu"].astype(str).apply(extract_country)
        st.dataframe(df)

        country_filter = st.selectbox("Bir ülke seçerek filtrele", ["Hepsi"] + sorted(df["Ülke"].dropna().unique().tolist()))
        if country_filter != "Hepsi":
            df = df[df["Ülke"] == country_filter]
            st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("CSV olarak indir", csv, "export.csv", "text/csv")
    else:
        st.error("Excel dosyasında 'Görüşme Notu' sütunu bulunamadı.")
