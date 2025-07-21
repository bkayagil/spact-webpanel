import streamlit as st
import pandas as pd
import numpy as np

# Görüşme Notu'ndan ülke çıkaran fonksiyon
def extract_country(note):
    if pd.isna(note):
        return "Diğer"
    
    countries = [
        "Almanya", "Fransa", "İngiltere", "İtalya", "Amerika", "Hollanda", "İspanya", 
        "Polonya", "Çek Cumhuriyeti", "Belçika", "Avusturya", "İsviçre", "Yunanistan", 
        "Portekiz", "Norveç", "Danimarka", "İsveç", "Finlandiya", "Avustralya", "Kanada", 
        "Japonya", "Hindistan", "Çin", "Güney Kore", "Brezilya", "Meksika", "Rusya", "Tayland"
    ]
    
    note_lower = note.lower()
    for country in countries:
        if country.lower() in note_lower:
            return country
    return "Diğer"

# Ticaret türü çıkarma fonksiyonu (parsiyel ve ltl eklendi)
def extract_trade_type(note):
    if pd.isna(note):
        return "Diğer"

    result = []
    note_lower = note.lower()

    if all(keyword in note_lower for keyword in ["ihracat", "ithalat", "intermodal", "havayolu"]):
        return "Tümü"

    if "ihracat" in note_lower:
        result.append("İhracat")
    if "ithalat" in note_lower:
        result.append("İthalat")
    if "intermodal" in note_lower:
        result.append("Intermodal")
    if "havayolu" in note_lower:
        result.append("Havayolu")
    if "parsiyel" in note_lower or "ltl" in note_lower:
        result.append("Parsiyel")

    return ", ".join(result) if result else "Diğer"

# Streamlit uygulaması
st.title("Görüşme Notu Analizi")

uploaded_file = st.file_uploader("Excel dosyanızı yükleyin", type="xlsx")

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    if 'Görüşme Notu' in df.columns:
        # Boş hücreleri boş string ile doldur
        df['Görüşme Notu'] = df['Görüşme Notu'].fillna("")

        # Ülke ve ticaret türü çıkarımı
        df['Ülke'] = df['Görüşme Notu'].apply(extract_country)
        df['Ticaret Türü'] = df['Görüşme Notu'].apply(extract_trade_type)

        # Filtre seçenekleri
        countries = sorted(df['Ülke'].dropna().unique())
        trade_types = sorted({t.strip() for types in df['Ticaret Türü'] for t in types.split(",")})

        selected_countries = st.multiselect('Ülke(ler) seçin', countries, default=countries)
        selected_trade_types = st.multiselect('Ticaret tür(ler)ini seçin', trade_types, default=trade_types)

        # Filtreleme (ticaret türü kısmı "içeren" şekilde çalışır)
        df_filtered = df[
            df['Ülke'].isin(selected_countries) &
            df['Ticaret Türü'].apply(lambda x: any(tt in x for tt in selected_trade_types))
        ]

        # Sonuçları göster
        st.write(f"Filtrelenmiş veri ({len(df_filtered)} kayıt):")
        st.dataframe(df_filtered)

        # UTF-8 BOM ile CSV çıktısı (Excel karakter bozulmasını önler)
        csv = df_filtered.to_csv(index=False).encode('utf-8-sig')
        st.download_button("CSV olarak indir", csv, "filtrelenmis_veri.csv", "text/csv")

    else:
        st.error("'Görüşme Notu' sütunu bulunamadı.")
