import streamlit as st
import requests

# Sayfa genişlik ve sekme ayarları
st.set_page_config(layout="wide", page_title="Doğan'ın Kalbi - Şifalı Bitkiler")

# --- STRAPI BAĞLANTI AYARLARI ---
BASE_URL = "https://icerik-yonetimi.onrender.com"
STRAPI_TOKEN = "ce52b94fd9281753f6544d42db558e87e22f83c09bc5f2088ff9a68504f7251d5380eb2e6965e7da56f15110f4d6bf65b8e1b61fd8c6c245712a51873041e58478e350f8877d05d4631eac1a15a3e5faec5777167b5c001a184e616c31fcf847731e5f7293f0a592c81b87769afa90441035e34525d801e023b6aa4e001d1690"
headers = {"Authorization": f"Bearer {STRAPI_TOKEN}"}

# --- TÜRKÇE HARF DUYARSIZLAŞTIRMA SİGORTASI ---
def turkce_kucult(metin):
    if not metin:
        return ""
    metin = metin.replace("İ", "i").replace("I", "ı").replace("Ğ", "ğ").replace("ğ", "ğ")
    metin = metin.replace("Ü", "ü").replace("Ş", "ş").replace("Ç", "ç").replace("Ö", "ö")
    return metin.lower()

# --- SENİN ORİJİNAL HTML/CSS BANNER TASARIMIN ---
st.markdown("""
    <style>
    #root [data-testid="stHeader"] { display: none; }
    .block-container { padding-top: 1rem !important; }
    
    /* Senin meşhur kavanozlu arka plan resmin */
    .banner-tasarim {
        background-image: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1546842931-886c185b4c8c?q=80&w=1200');
        background-size: cover;
        background-position: center;
        padding: 50px 30px;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-family: 'Segoe UI', sans-serif;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .ana-baslik { font-size: 48px; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.7); }
    .alt-slogan { font-size: 18px; font-style: italic; opacity: 0.9; margin-top: 5px; }
    .logo-makfa { font-size: 26px; font-weight: bold; letter-spacing: 3px; margin-top: 25px; }
    
    /* Strapi'den gelen verilerin basılacağı kartlar */
    .bitki-kart {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 8px;
        border-left: 6px solid #2e7d32;
        margin-top: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .bitki-kart h3 { color: #2e7d32; margin-top: 0; font-size: 22px; }
    </style>
""", unsafe_allow_html=True)

# HTML Tasarımı Devreye Sokuyoruz
st.markdown("""
    <div class="banner-tasarim">
        <div class="ana-baslik">🌿 Doğan'ın Kalbi</div>
        <div class="alt-slogan">Şifalı bitkilerin özünü ve gizli dünyasını keşfedin.</div>
        <div class="logo-makfa">MAKFALIGURI</div>
        <div style="font-size: 11px; letter-spacing: 2px; opacity: 0.8; margin-top: 5px;">ŞİFALI BİTKİLERİN ÖZÜ</div>
    </div>
""", unsafe_allow_html=True)

# --- SEKME VE BUTON YAPILARI ---
sekme1, sekme2, sekme3 = st.tabs(["🌱 Şifalı Bitkiler Kataloğu", "ℹ️ Hakkımızda", "📞 İletişim"])

with sekme1:
    # Arama Çubuğu
    arama_terimi = st.text_input("🔍 Veritabanında Şifalı Bitki Ara:", placeholder="Örn: yedi damar...")
    st.markdown("---")

    try:
        # Strapi REST API ile Canlı Bağlantı Kuruluyor
        response = requests.get(f"{BASE_URL}/api/bitkis", headers=headers, timeout=15)
        
        if response.status_code == 200:
            veriler = response.json().get("data", [])
            
            # Arama filtresi motoru (Türkçe harfe duyarlı kontrol)
            if arama_terimi:
                temiz_arama = turkce_kucult(arama_terimi.strip())
                filtrelenmis_veriler = []
                
                for b in veriler:
                    strapi_bitki_adi = b.get("attributes", {}).get("Nurten", "")
                    if temiz_arama in turkce_kucult(strapi_bitki_adi):
                        filtrelenmis_veriler.append(b)
                veriler = filtrelenmis_veriler

            if not veriler:
                st.info("Aradığınız isimde bir şifalı bitki veritabanında bulunamadı.")
            
            # Dinamik olarak verileri kart yapısında ekrana basıyoruz
            for bitki in veriler:
                detay = bitki.get("attributes", {})
                bitki_adi = detay.get("Nurten", "İsimsiz Bitki")
                
                fayda_verisi = detay.get("faydalari", "")
                fayda_metni = ""
                
                if isinstance(fayda_verisi, list):
                    for blok in fayda_verisi:
                        if blok.get("type") == "paragraph":
                            for child in blok.get("children", []):
                                fayda_metni += child.get("text", "") + "\n"
                else:
                    fayda_metni = str(fayda_verisi)
                    
                st.markdown(f"""
                    <div class="bitki-kart">
                        <h3>🌱 {bitki_adi}</h3>
                        <p style="color:#333; line-height:1.7; font-family: sans-serif; font-size:15px; white-space: pre-line;">{fayda_metni if fayda_metni.strip() else 'İçerik açıklaması yükleniyor...'}</p>
                    </div>
                """, unsafe_allow_html=True)
                
        else:
            st.error("Strapi veritabanı API bağlantı hatası.")
    except Exception as e:
        st.error(f"Sunucu bağlantısı koptu: {e}")

with sekme2:
    st.subheader("Doğan'ın Kalbi Hakkında")
    st.write("Bu platform, doğanın derinliklerinde saklı kalan şifalı bitki kültürünü dijital dünyaya taşımak amacıyla geliştirilmiştir.")

with sekme3:
    st.subheader("İletişim Bilgileri")
    st.write("📬 **E-Posta:** iletisim@doganinkalbi.com | 📍 **Merkez Kampüs:** Rize, Türkiye")