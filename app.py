import streamlit as st
import pandas as pd

# Excel dosyasını yükle
uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

# Eğer dosya yüklendiyse
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Filtreleme seçeneklerini oluştur
    st.sidebar.title("Filtreleme Seçenekleri")
    
    # Ülke filtrelemesi
    countries = df['Ülke'].dropna().unique()
    selected_country = st.sidebar.selectbox("Ülke Seçin", countries)

    # İhracat / İthalat filtrelemesi
    trade_type = st.sidebar.selectbox("Ticaret Türü Seçin", ["Hepsi", "İhracat", "İthalat"])

    # Taşıma Yöntemi filtrelemesi
    transport_type = st.sidebar.selectbox("Taşıma Yöntemi Seçin", ["Hepsi", "Denizyolu", "Havayolu"])

    # Seçilen filtreleri uygulayarak veri çekeceğiz
    filtered_df = df

    if selected_country != "Hepsi":
        filtered_df = filtered_df[filtered_df['Ülke'] == selected_country]

    if trade_type != "Hepsi":
        filtered_df = filtered_df[filtered_df['Görüşme Notu'].str.contains(trade_type, case=False, na=False)]

    if transport_type != "Hepsi":
        filtered_df = filtered_df[filtered_df['Görüşme Notu'].str.contains(transport_type, case=False, na=False)]

    # Filtrelenmiş veriyi göster
    st.write(f"Seçilen Ülke: {selected_country}")
    st.write(f"Seçilen Ticaret Türü: {trade_type}")
    st.write(f"Seçilen Taşıma Yöntemi: {transport_type}")
    
    # Filtrelenmiş veriyi göster
    st.write(filtered_df)
