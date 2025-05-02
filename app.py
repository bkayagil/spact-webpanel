import streamlit as st
import pandas as pd

# Excel dosyasını yükle
uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type=["xlsx"])

# Eğer dosya yüklendiyse
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Sütun isimlerini kontrol et
    st.write("Sütun İsimleri:", df.columns)

    # Boşlukları temizle
    df.columns = df.columns.str.strip()

    # Görüşme Notu sütununda anahtar kelimelere göre Ülke, Ticaret Türü ve Taşıma Yöntemi çıkarma
    def extract_country(note):
        countries = [
            "Almanya", "Fransa", "İngiltere", "İtalya", "Amerika", "Hollanda", "İspanya", 
            "Polonya", "Çek Cumhuriyeti", "Belçika", "Avusturya", "İsviçre", "Yunanistan", 
            "Portekiz", "Norveç", "Danimarka", "İsveç", "Finlandiya", "Avustralya", "Kanada", 
            "Japonya", "Hindistan", "Çin", "Güney Kore", "Brezilya", "Meksika", "Rusya", "Tayland"
        ]  # Buraya istediğiniz kadar ülke ekleyebilirsiniz
        for country in countries:
            if country.lower() in note.lower():
                return country
        return "Diğer"  # Ülke bulunmazsa "Diğer" olarak dönecek

    def extract_trade_type(note):
        if "ihracat" in note.lower():
            return "İhracat"
        elif "ithalat" in note.lower():
            return "İthalat"
        return "Diğer"  # Ticaret türü bulunmazsa "Diğer"

    def extract_transport_type(note):
        if "denizyolu" in note.lower():
            return "Denizyolu"
        elif "havayolu" in note.lower():
            return "Havayolu"
        return "Diğer"  # Taşıma türü bulunmazsa "Diğer"

    # Yeni sütunlar ekleyelim
    df['Ülke'] = df['Görüşme Notu'].apply(extract_country)
    df['Ticaret Türü'] = df['Görüşme Notu'].apply(extract_trade_type)
    df['Taşıma Yöntemi'] = df['Görüşme Notu'].apply(extract_transport_type)

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

    # Ülke filtrelemesi
    if selected_country != "Hepsi":
        filtered_df = filtered_df[filtered_df['Ülke'] == selected_country]

    # Ticaret türü filtrelemesi
    if trade_type != "Hepsi":
        filtered_df = filtered_df[filtered_df['Ticaret Türü'] == trade_type]

    # Taşıma yöntemi filtrelemesi
    if transport_type != "Hepsi":
        filtered_df = filtered_df[filtered_df['Taşıma Yöntemi'] == transport_type]

    # Filtrelenmiş veriyi göster
    st.write(f"Seçilen Ülke: {selected_country}")
    st.write(f"Seçilen Ticaret Türü: {trade_type}")
    st.write(f"Seçilen Taşıma Yöntemi: {transport_type}")
    
    # Filtrelenmiş veriyi kullanıcıya göster
    st.write(filtered_df)
