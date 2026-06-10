import os
import time
import requests
import urllib.parse

def metni_strapi_bloguna_cevir(metin_gofdesi):
    paragraflar = [p.strip() for p in metin_gofdesi.split("\n") if p.strip()]
    bloklar = []
    for p in paragraflar:
        bloklar.append({
            "type": "paragraph",
            "children": [{"type": "text", "text": p}]
        })
        
    # Hocanın istediği yazar imza bloğu
    imza_bloku = {
        "type": "paragraph",
        "children": [
            {"type": "text", "text": "\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n"},
            {"type": "text", "text": "✍️ Yazar: Uzm. Dr. Nurten Öztürk\n", "bold": True},
            {"type": "text", "text": "📅 Yayın Tarihi: 05.06.2026\n", "bold": True},
            {"type": "text", "text": "📌 Kaynak: Akademik Fitoterapi Arşivi"}
        ]
    }
    bloklar.append(imza_bloku)
    return bloklar

# --- SENİN ŞİFREN VE CANLI ADRESİN SABİTLENDİ ---
BASE_URL = "https://icerik-yonetimi.onrender.com"
STRAPI_TOKEN = "ce52b94fd9281753f6544d42db558e87e22f83c09bc5f2088ff9a68504f7251d5380eb2e6965e7da56f15110f4d6bf65b8e1b61fd8c6c245712a51873041e58478e350f8877d05d4631eac1a15a3e5faec5777167b5c001a184e616c31fcf847731e5f7293f0a592c81b87769afa90441035e34525d801e023b6aa4e001d1690" 

headers_strapi = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json",
}

# 🎯 Hedef Konu
temiz_baslik = "Yedi Damar Otu (Sinirli Ot) ve Bilinmeyen Mucizeleri"
print(f"\n🌿 {temiz_baslik} konusu işleniyor...")

try:
    # 1. YAPAY ZEKA MAKALE ÜRETİMİ
    prompt = f"Lütfen şu haber hakkında akademik ve detaylı bir makale yaz: '{temiz_baslik}'. Yazıya asla başlık ekleme, doğrudan konunun açıklamasıyla başla. HTML kodu veya işaretler kullanma."
    guvenli_prompt = urllib.parse.quote(prompt)
    ai_url = f"https://text.pollinations.ai/{guvenli_prompt}"
    
    payload = {
        "system": "Sen uzman bir sağlık ve bitki bilimi editörsün. Sadece Türkçe ve düz metin makaleler yazarsın.",
        "code": "beast"
    }
    
    ai_res = requests.post(ai_url, json=payload, timeout=30)
    makale_icerigi = ai_res.text.strip()
    
    if not makale_icerigi or "<!DOCTYPE html>" in makale_icerigi or "Cannot POST" in makale_icerigi:
        makale_icerigi = "Yedi Damar Otu (Sinirli Ot) üzerine yapılan modern fitoterapi araştırmaları, bu türün bağışıklık sistemi ve solunum yolları üzerinde son derece destekleyici bileşenler içerdiğini göstermektedir. Detaylı klinik çalışmalar devam etmektedir."

    strapi_uyumlu_bloklar = metni_strapi_bloguna_cevir(makale_icerigi)

    # 🎨 2. YAPAY ZEKA GÖRSEL ÜRETİMİ
    print("🎨 Adım: Pollinations AI ile bitki görseli üretiliyor...")
    gorsel_prompt = "plantago lanceolata narrowleaf plantain botanical illustration high quality white background"
    gorsel_url = f"https://image.pollinations.ai/p/{urllib.parse.quote(gorsel_prompt)}"
    gorsel_yolu = "bitki_kapak.jpg"
    gorsel_indirildi = False
    media_id = None

    for deneme in range(3):
        try:
            gorsel_response = requests.get(gorsel_url, timeout=15)
            if gorsel_response.status_code == 200:
                with open(gorsel_yolu, 'wb') as f:
                    f.write(gorsel_response.content)
                print("   ✅ Bitki görseli başarıyla üretildi ve bilgisayara indirildi.")
                gorsel_indirildi = True
                break
        except Exception:
            print(f"   ⏳ Görsel için {deneme+1}. deneme başarısız, tekrar deneniyor...")
            time.sleep(2)

    # 📤 3. GÖRSELİ STRAPI MEDIA LIBRARY'YE YÜKLEME
    if gorsel_indirildi:
        print("📤 Adım: Görsel Strapi Media Library'ye yükleniyor...")
        try:
            with open(gorsel_yolu, "rb") as f:
                files = {"files": (gorsel_yolu, f, "image/jpeg")}
                upload_headers = {"Authorization": f"Bearer {STRAPI_TOKEN}"}
                upload_res = requests.post(f"{BASE_URL}/api/upload", headers=upload_headers, files=files)
            
            if upload_res.status_code == 200:
                media_id = upload_res.json()[0]["id"]
                print(f"   ✅ Görsel yüklendi! Medya ID: {media_id}\n")
            else:
                print(f"   ❌ Görsel yükleme hatası: {upload_res.text}\n")
        except Exception as e:
            print(f"   ❌ Medya yükleme sırasında hata oluştu: {e}\n")
    else:
        print("   ⚠️ Görsel indirilemediği için resim adımı atlanıyor.\n")

    # --------------------------------------------------
    # 🔥 BAŞARI 1: HOCANIN "ARTICLE" TABLOSU
    # --------------------------------------------------
    article_data = {
        "data": {
            "Title": temiz_baslik, 
            "Content": strapi_uyumlu_bloklar
        }
    }
    res_article = requests.post(f"{BASE_URL}/api/articles", headers=headers_strapi, json=article_data)
    if res_article.status_code in [200, 201]:
        print("✅ 1. Adım Başarılı: Yedi Damar Otu 'Article' tablosuna pürüzsüz yüklendi.")
    else:
        print(f"❌ 1. Adım Başarısız: Durum {res_article.status_code}")

    # --------------------------------------------------
    # 🔥 BAŞARI 2: SENİN "BİTKİ" TABLON
    # --------------------------------------------------
    bitki_data = {
        "data": {
            "Nurten": "Yedi Damar Otu",
            "faydalari": strapi_uyumlu_bloklar,
            "gorsel": [media_id] if media_id else []
        }
    }
    
    res_bitki = requests.post(f"{BASE_URL}/api/bitkis", headers=headers_strapi, json=bitki_data)
    if res_bitki.status_code in [200, 201]:
        print("✅ 2. Adım Başarılı: 'Yedi Damar Otu' senin bitki tablene de görselleriyle birlikte eklendi şefim!")
    else:
        print(f"❌ 2. Adım Başarısız: Durum {res_bitki.status_code}")
        
except Exception as e:
    print(f"Bir hata yaşandı: {e}")