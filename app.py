import streamlit as st
import pandas as pd

# Genişletilmiş ülke listesi
country_list = [
    "Amerika", "Almanya", "Fransa", "İngiltere", "Kanada", "İtalya", 
    "İspanya", "Hindistan", "Japonya", "Çin", "Brezilya", "Rusya", 
    "Türkiye", "Arjantin", "Avusturya", "Belçika", "Danimarka", "Fas", 
    "Hollanda", "İsveç", "İsviçre", "Meksika", "Polonya", "Portekiz", 
    "Romanya", "Suriye", "Çek Cumhuriyeti", "Yunanistan", "Ukrayna", 
    "Güney Kore", "Endonezya", "Malezya", "Singapur", "Filipinler", 
    "Mısır", "Venezuela", "Pakistan", "Birleşik Arap Emirlikleri", 
    "Suudi Arabistan", "Katar", "Irak", "Libya", "Bangladeş", "Küba", 
    "Nijerya", "Kenya", "Tanzanya", "Jamaika", "Yeni Zelanda", "Avustralya", 
    "Güney Afrika", "Kolombiya", "Peru", "Kosta Rika", "El Salvador"
]

# Ülke çekme fonksiyonu
def extract_country_from_notes(note):
    if not note:  # Eğer 'note' boşsa, hiçbir şey yapma
        return ""
    countries_found = []
    for country in country_list:
        if country.lower() in note.lower():  # Küçük harflerle kontrol ediyoruz
            countries_found.append(country)
    return ", ".join(countries_found)  # Bulunan ülkeleri virgülle ayırarak döndürüyoruz

# Streamlit arayüzü
st.title('Ülke Çekme Uygulaması')

# Dosya yükleme
uploaded_file = st.file_uploader("Excel dosyasını yükleyin", type="xlsx")

if uploaded_file is not None:
    # Dosyayı okuma
    df = pd.read_excel(uploaded_file)

    # 'Görüşme Notu' sütununu kontrol et
    if 'Görüşme Notu' in df.columns:
        # Ülke isimlerini çıkarmak için 'Görüşme Notu' sütununu kullanıyoruz
        df['Ülke'] = df['Görüşme Notu'].apply(extract_country_from_notes)
        
        # Sonuçları göster
        st.write(df)
    else:
        st.error("'Görüşme Notu' sütunu bulunamadı.")
