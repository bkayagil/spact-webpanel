import streamlit as st
import pandas as pd
import numpy as np

# Görüşme Notu'ndan ülke çıkaran fonksiyon
def extract_country(note):
    if pd.isna(note):  # Eğer görüşme notu NaN veya None ise
        return "Diğer"  # "Diğer" olarak döndürelim
    
    countries = [
        "Almanya", "Fransa", "İngiltere", "İtalya", "Amerika", "Hollanda", "İspanya", 
        "Polonya", "Çek Cumhuriyeti", "Belçika", "Avusturya", "İsviçre", "Yunanistan", 
        "Portekiz", "Norveç", "Danimarka", "İsveç", "Finlandiya", "Avustralya", "Kanada", 
        "Japonya", "Hindistan", "Çin", "Güney Kore", "Brezilya", "Meksika", "Rusya", "Tayland"
    ]
    
    for country in countries:
        if country.lower() in note.lower():
            return country
    return "Diğer"  # Ülke bulunmazsa "Diğer" olarak dönecek

# Görüşme notundan ihracat, ithalat ve intermodal durumlarını çıkaran fonksiyon
def extract_trade_type(note):
    if pd.isna(note):
        return "Diğer"
    
    note = note.lower()
    
    if "ihracat" in note:
        return "İhracat"
    elif "ithalat" in note:
        return "İthalat"
    elif "intermodal" in note:
        return "Intermodal"
    
    return "Diğer"  # Eğer hiçbiri yoksa "Diğer"

# Veri dosyasını yükleme
uploaded_file = st.file_uploader("Excel dosyanızı yükleyin", type="xlsx")

if uploaded_file is not None:
    # Veriyi yükleyelim
    df = pd.read_excel(uploaded_file)

    # Verideki 'Görüşme Notu' sütununu kontrol edelim
    if 'Görüşme Notu' in df.columns:
        # Ülke ve İhracat/İthalat bilgilerini çıkaralım
        df['Ülke'] = df['Görüşme Notu'].apply(extract_country)
        df['Ticaret Türü'] = df['Görüşme Notu'].apply(extract_trade_type)

        # Ülkeleri ve ticaret türlerini seçmek için filtreler ekleyelim
        countries = df['Ülke'].dropna().unique()
        trade_types = df['Ticaret Türü'].dropna().unique()

        # Ülke filtreleme
        selected_country = st.selectbox('Bir ülke seçin', countries)
        df_filtered_by_country = df[df['Ülke'] == selected_country]

        # Ticaret türü filtreleme
        selected_trade_type = st.selectbox('Bir ticaret türü seçin', trade_types)
        df_filtered_by_trade = df_filtered_by_country[df_filtered_by_country['Ticaret Türü'] == selected_trade_type]

        # Filtrelenmiş veriyi gösterelim
        st.write(f"{selected_country} için {selected_trade_type} ticareti verileri", df_filtered_by_trade)

    else:
        st.error("'Görüşme Notu' sütunu bulunamadı.")
