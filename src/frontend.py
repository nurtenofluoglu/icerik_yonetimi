import streamlit as st
import requests
import os

# 1. Bağlantı Ayarları
BASE_URL = "https://icerik-yonetimi.onrender.com"
STRAPI_TOKEN = "ce52b94fd9281753f6544d42db558e87e22f83c09bc5f2088ff9a68504f7251d5380eb2e6965e7da56f15110f4d6bf65b8e1b61fd8c6c245712a51873041e58478e350f8877d05d4631eac1a15a3e5faec5777167b5c001a184e616c31fcf847731e5f7293f0a592c81b87769afa90441035e34525d801e023b6aa4e001d1690"

headers = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json"
}

# 🎨 Sayfa Yapısı
st.set_page_config(page_title="Doğanın Kalbi | Makfaliguri", page_icon="🌿", layout="wide")

# ==================================================
# 🔥 1. ADIM: INDEX.HTML'İ OKUMA VE SİHİRLİ JAVASCRIPT YAMASI
# ==================================================
html_icerigi = None
yollar = ["../public/index.html", "public/index.html", "index.html"]
for yol in yollar:
    if os.path.exists(yol):
        with open(yol, "r", encoding="utf-8") as f:
            html_icerigi = f.read()
        break

if html_icerigi:
    # 🛠️ HTML içindeki localhost adresini doğrudan canlı linke çekiyoruz
    html_icerigi = html_icerigi.replace("http://localhost:1337", BASE_URL)
    html_icerigi = html_icerigi.replace("https://icerik-yonetimi.onrender.com", BASE_URL)

    # 🪄 SİHİRLİ ENJEKSİYON: HTML'in kapanış etiketinden hemen önce tarayıcıyı zorlayacak tamir kodumuzu yerleştiriyoruz.
    # Bu script: Hem CSS hatasını düzeltecek hem de arama motoru çalışırken kırılan resimleri yakalayıp tamir edecek.
    tamir_scripti = f"""
    <script>
        // 1. Giriş Sayfası Arka Plan CSS Hatasını ve Resmini Kesin Tamir Etme Motoru
        window.addEventListener('DOMContentLoaded', () => {{
            const hero = document.getElementById('anaGirisEkrani');
            if (hero) {{
                hero.style.background = "linear-gradient(rgba(0, 0, 0, 0.35), rgba(0, 0, 0, 0.45)), url('{BASE_URL}/uploads/makfaliguri-logo.png')";
                hero.style.backgroundSize = "cover";
                hero.style.backgroundPosition = "center";
                hero.style.backgroundAttachment = "fixed";
            }}
        }});

        // 2. Arama Yapıldığında Kırılan Resimleri Havada Yakalayıp Düzeltme Motoru
        const observer = new MutationObserver((mutations) => {{
            mutations.forEach((mutation) => {{
                mutation.addedNodes.forEach((node) => {{
                    if (node.nodeType === 1) {{
                        // Yeni eklenen kartların içindeki resimleri tara
                        const imgs = node.querySelectorAll('img');
                        imgs.forEach(img => {{
                            let src = img.getAttribute('src');
                            if (src && src.startsWith('uploads/')) {{
                                img.src = '{BASE_URL}/' + src;
                            }}
                        }});
                    }}
                }});
            }});
        }});
        
        window.addEventListener('DOMContentLoaded', () => {{
            const liste = document.getElementById('bitki-listesi');
            if (liste) {{
                observer.observe(liste, {{ childList: true, subtree: true }});
            }}
        }});
    </script>
    """
    
    # Tamir kodunu HTML'e dahil ediyoruz
    html_icerigi = html_icerigi.replace("</body>", f"{tamir_scripti}</body>")

    # 🚀 Çalıştırıyoruz
    st.components.v1.html(html_icerigi, height=780, scrolling=True)
else:
    st.title("🌿 Doğan'ın Kalbi | Makfaliguri")
    st.error("💡 Hata: 'public/index.html' dosyası bulunamadı.")

st.divider()

# ==================================================
# 🔄 2. ADIM: VERİTABANI MAKALELERİ (ALT AKIŞ)
# ==================================================
@st.cache_data
def makaleleri_getir():
    url = f"{BASE_URL}/api/articles?populate=*"
    try:
        res = requests.get(url, headers=headers)
        if res.ok:  
            return res.json().get("data", [])
    except:
        pass
    return []

articles = makaleleri_getir()

if articles:
    st.header("📚 Sitedeki Güncel Makaleler & Genel Akış")
    col1, col2 = st.columns(2)
    for index, a in enumerate(articles):
        aktif_sutun = col1 if index % 2 == 0 else col2
        title = a.get("Title", "Başlıksız Makale")
        
        with aktif_sutun.container(border=True):
            st.subheader(f"🌿 {title}")
            
            makale_resmi = None
            for key, val in a.items():
                if isinstance(val, dict) and "url" in val:
                    makale_resmi = val.get("url")
                    break
                elif isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                    makale_resmi = val[0].get("url")
                    break
            
            if makale_resmi:
                if not makale_resmi.startswith("http"):
                    makale_resmi = f"{BASE_URL}{makale_resmi}"
                st.image(makale_resmi, use_container_width=True)
            
            content_blocks = a.get("Content", [])
            if isinstance(content_blocks, list):
                for block in content_blocks:
                    if block.get("type") == "paragraph":
                        children = block.get("children", [])
                        for child in children:
                            text_data = child.get("text", "")
                            if "✍️ Yazar:" in text_data or "━━━━━━━━" in text_data:
                                st.markdown(f"**{text_data}**")
                            else:
                                st.write(text_data)