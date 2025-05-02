import pandas as pd
import streamlit as st

# Görüşme Notu'ndan ülke çıkaran fonksiyon
def extract_country(note):
    if note is None:  # Eğer görüşme notu None ise
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

# Excel dosyasını yükle
uploaded_file = st.file_uploader("Excel dosyanızı yükleyin", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Görüşme Notu'ndan ülke sütununu çıkar
    df['Ülke'] = df['Görüşme Notu'].apply(extract_country)
    
    # Ülke listesi
    countries = df['Ülke'].dropna().unique()
    
    # Streamlit için filtreleme seçenekleri
    selected_country = st.selectbox("Ülke seçin", options=countries)
    filtered_df = df[df['Ülke'] == selected_country]
    
    # Ülkeye göre filtrelenmiş veriyi göster
    st.write(f"Seçilen Ülke: {selected_country}")
    st.dataframe(filtered_df)

    # İhracat/İthalat filtreleme
    export_or_import = st.radio("İhracat mı İthalat mı?", ["İhracat", "İthalat"])
    filtered_export_import_df = filtered_df[filtered_df['Görüşme Notu'].str.contains(export_or_import, na=False)]
    
    st.write(f"Filtrelenmiş {export_or_import} Verileri:")
    st.dataframe(filtered_export_import_df)
