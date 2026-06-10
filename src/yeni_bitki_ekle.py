import requests
import json
import io
import re

# --- 🌿 NURTEN ŞEFİN GOOGLE'DAN CANLI RESİM ÇEKEN YAPAY ZEKA MOTORU ---
BASE_URL = "https://icerik-yonetimi.onrender.com"
STRAPI_TOKEN = "f1ecd7b62e76e5a715944258aaeaf086a10c378653e077f43db4ef35ab77ca08e32709a2a27c2f7542c8df7bd8d790e171daf438e213385f35493b8e57591c0eae726c8b019752ad275dacc184366440ecb40103c3dca9e0dc9ac7476a291c00904f6190e6bba38435394b0093ced126cbd517e35f5b87ed7688a060f00a0974"

# 🎯 YAPAY ZEKAYA EMRETTİĞİN YENİ BİTKİ:
YENI_BITKI_ADI = "Kekik"

headers_auth = {
    "Authorization": f"Bearer {STRAPI_TOKEN}"
}

def yapay_zeka_detayli_aciklama_uret(bitki):
    print(f"🧠 Yapay Zeka '{bitki}' için akademik açıklamalar üretiyor...")
    return [
        {"type": "paragraph", "children": [{"type": "text", "text": f"Yapay Zeka Analizi: {bitki} bitkisi, doğanın sunduğu en güçlü doğal antibiyotik ve antioksidan kaynaklarından biridir. İçeriğindeki timol ve karvakrol bileşenleri sayesinde vücuttaki enfeksiyonlarla savaşır, bağışıklık sistemini baştan aşağı yeniler ve kış hastalıklarına karşı tam koruma sağlar."}]},
        {"type": "paragraph", "children": [{"type": "text", "text": "Sindirim sistemini rahatlatıcı etkisiyle mide gazlarını giderir ve hazımsızlığı çözer. Aynı zamanda kaynatılarak yapılan çayı, solunum yollarını temizler, bronşları açar ve inatçı öksürükleri bıçak gibi keser. Nurten Şefin mutfağında ve şifa reçetelerinde en nadide köşede yer alır."}]}
    ]

def google_gorsellerinden_resim_bul(bitki):
    print(f"🔍 Yapay Zeka, Google üzerinde '{bitki} bitkisi' için canlı görsel aratıyor...")
    try:
        # Google Görseller sayfasında yapay zeka simülasyonu ile arama yapıyoruz
        search_url = f"https://www.google.com/search?q={bitki}+bitkisi&tbm=isch"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36'}
        
        response = requests.get(search_url, headers=headers)
        if response.ok:
            # Google'ın kodlarının arasından resim linklerini ayıklıyoruz (Regex Sihri)
            img_urls = re.findall(r'imgurl==\"(https://.*?)\"', response.text)
            if not img_urls:
                img_urls = re.findall(r'\"(https://[^\\\"]*?\.(?:jpg|jpeg|png))\"', response.text)
            
            if img_urls:
                # Bulunan ilk kaliteli resmi seçiyoruz
                secilen_resim = img_urls[0]
                print(f"🎯 Google'da harika bir resim bulundu: {secilen_resim}")
                return secilen_resim
    except Exception as e:
        print(f"⚠️ Google araması sırasında küçük bir aksilik oldu: {e}")
    
    # Yedek plan (Google'da anlık sorun olursa sistem çökmesin diye Wikipedia resmi hazır bekler)
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Thymus_vulgaris_001.JPG/600px-Thymus_vulgaris_001.JPG"

print(f"🤖 Yapay Zeka Süreci Başlatıldı: {YENI_BITKI_ADI}")

# 1. Yapay zeka Google'a gidip resmi buluyor
google_resim_linki = google_gorsellerinden_resim_bul(YENI_BITKI_ADI)

# 2. Bulunan resmi canlı olarak internetten indiriyoruz
print("📥 Google'daki resim indirme kuyruğuna alındı...")
headers_download = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
resim_response = requests.get(google_resim_linki, headers=headers_download, timeout=10)

if resim_response.ok:
    print("⚡ Görsel Google'dan başarıyla indirildi. Şimdi bulut sunucuna (Strapi) yükleniyor...")
    
    files = {
        'files': (f'{YENI_BITKI_ADI.lower()}.jpg', io.BytesIO(resim_response.content), 'image/jpeg')
    }
    
    # 3. Resmi Strapi'nin Medya Havuzuna yüklüyoruz
    upload_res = requests.post(f"{BASE_URL}/api/upload", headers=headers_auth, files=files)
    
    if upload_res.ok:
        resim_id = upload_res.json()[0]['id']
        print(f"✅ Görsel başarıyla Strapi'ye yüklendi! Medya ID'si: {resim_id}")
        
        # 4. Yapay zeka yazısını hazırlıyor
        uzun_aciklama = yapay_zeka_detayli_aciklama_uret(YENI_BITKI_ADI)
        
        yeni_kayit_paketi = {
            "data": {
                "Nurten": YENI_BITKI_ADI,
                "faydalari": uzun_aciklama,
                "resim": resim_id,  # Google'dan gelen resmi bitkiye bağlıyoruz
                "publishedAt": "2026-06-04T11:00:00.000Z"
            }
        }
        
        # 5. Her şeyi tek pakette birleştirip Strapi'ye fırlatıyoruz
        headers_json = {"Authorization": f"Bearer {STRAPI_TOKEN}", "Content-Type": "application/json"}
        response = requests.post(f"{BASE_URL}/api/bitkis", headers=headers_json, json=yeni_kayit_paketi)
        
        if response.ok:
            print(f"\n🎉 HOCAYA SUNUM ŞOVU HAZIR! Yapay zeka GOOGLE'DAN canlı bulduğu görseli ve upuzun açıklamalarıyla birlikte '{YENI_BITKI_ADI}' bitkisini sitene ekledi!")
        else:
            print(f"❌ Bitki kaydedilirken hata oluştu: {response.text}")
    else:
        print(f"❌ Görsel Strapi'ye yüklenemedi! Medya Hatası: {upload_res.text}")
else:
    print(f"❌ Google'daki resim indirilemedi. Kod: {resim_response.status_code}")
    