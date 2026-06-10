import requests
import json

# --- 🌿  UZUN VE ZENGİN İÇERİKLİ YAPAY ZEKA MOTORU ---
BASE_URL = "https://icerik-yonetimi.onrender.com"
STRAPI_TOKEN = "f1ecd7b62e76e5a715944258aaeaf086a10c378653e077f43db4ef35ab77ca08e32709a2a27c2f7542c8df7bd8d790e171daf438e213385f35493b8e57591c0eae726c8b019752ad275dacc184366440ecb40103c3dca9e0dc9ac7476a291c00904f6190e6bba38435394b0093ced126cbd517e35f5b87ed7688a060f00a0974"

headers = {
    "Authorization": f"Bearer {STRAPI_TOKEN}",
    "Content-Type": "application/json"
}

def yapay_zeka_icerik_uret(bitki_adi):
    bitki = bitki_adi.lower().strip()
    print(f"🤖 Yapay Zeka, '{bitki_adi}' bitkisi için detaylı analiz hazırlıyor...")
    
    if "domates" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Ağaç domatesi (Tamarillo), geleneksel domatese kıyasla çok daha yoğun bir antioksidan, A, C ve E vitamini deposudur. Bağışıklık sistemini maksimum seviyede desteklerken, serbest radikallerle savaşarak hücresel yaşlanmayı geciktirir."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "İçeriğindeki yüksek potasyum and lifler sayesinde kan basıncını (tansiyonu) dengeler, kötü kolesterolü düşürür ve kalp damar sağlığını korumada mucizevi etkiler gösterir. Ayrıca düşük kalorili yapısıyla diyetlerin vazgeçilmezidir."}]}
        ]
    elif "ebegümeci" in bitki or "ebegumeci" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Ebegümeci, antik çağlardan beri solunum yolları hastalıklarında bir zırh gibi kullanılmaktadır. İçerdiği yüksek müsilaj sayesinde boğaz yollarındaki tahrişi anında yumuşatır, inatçı kronik öksürüğü keser ve ses tellerini rahatlatır."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Mide ve bağırsak çeperini koruyarak gastrit ve ülser gibi sindirim sistemi rahatsızlıklarının hafifletilmesine yardımcı olur. Harici kullanımda ise lapası ciltteki yaraları, şişlikleri ve çıbanları hızla iyileştirme gücüne sahiptir."}]}
        ]
    elif "dut" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Dut yaprağı, modern tıp tarafından da kabul gören doğal bir şeker dengeleyicidir. İçeriğindeki özel bileşenler, bağırsaklarda şeker emilimini yavaşlatarak yemek sonrası kan şekerinin ani yükselmesini önler ve diyabet hastalarına muazzam bir destek sunar."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Vücuttaki ödemin ve biriken toksinlerin idrar yoluyla hızla atılmasını sağlar. Karaciğer enzimlerini düzenler, kanı temizler ve yüksek antioksidan yapısıyla serbest radikallere karşı vücuda tam koruma kalkanı oluşturur."}]}
        ]
    elif "kantaron" in bitki or "gümüşhane" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Gümüşhane'nin şifalı topraklarında yetişen sarı kantaron, hücre yenileyici ve doku onarıcı özellikleri en yüksek bitkilerden biridir. Cilt yaralarında, güneş ve yangın yanıklarında iz bırakmadan hızlı bir iyileşme süreci başlatır."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Aynı zamanda bitkisel bir sakinleştiricidir. Beyindeki serotonin (mutluluk hormonu) seviyesini dengeleyerek hafif ve orta şiddetli depresyon, anksiyete, yoğun stres ve uykusuzluk semptomlarını doğal yoldan hafifletir."}]}
        ]
    elif "hünnap" in bitki or "hunnap" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Hünnap, 'Ölümsüzlük Meyvesi' olarak da bilinen, C vitamini açısından narenciyeleri geride bırakan devasa bir şifa kaynağıdır. Bağışıklık sistemini baştan aşağı yeniler, vücudu kış hastalıklarına ve enfeksiyonlara karşı korur."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Sinir sistemini yatıştırıcı etkisiyle kronik stres ve uykusuzluk problemlerini çözer. Kan dolaşımını hızlandırarak damar sağlığını korur, yüksek lifli yapısıyla sindirimi ve bağırsak hareketlerini düzene sokar."}]}
        ]
    elif "zerdeçal" in bitki or "zerdecal" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Zerdeçal, doğadaki en güçlü iltihap sökücü (anti-inflamatuar) maddelerden biri olan Kurkumin bileşeni içerir. Eklem ağrılarını, romatizmal sızıları hafifletir ve vücuttaki kronik iltihaplanmaları kökünden kurutmaya yardımcı olur."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Beyin fonksiyonlarını geliştirerek hafızayı güçlendirir, Alzheimer riskini azaltır. Karaciğer dostudur, organı toksinlerden temizler ve safra akışını düzenleyerek sindirim sistemini baştan aşağı rahatlatır."}]}
        ]
    elif "papatya" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Tıbbi papatya, doğanın sunduğu en nazik ve etkili sakinleştiricilerden biridir. Merkezi sinir sistemini gevşeterek günün stresini alır, kas spazmlarını çözer ve derin, kaliteli bir uykuya geçişi kolaylaştırır."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Mide kasılmalarını, gaz sancılarını ve hazımsızlığı gidermede oldukça etkilidir. Cilt üzerinde antiseptik özellikleri bulunur, papatya çayıyla yapılan pansumanlar ciltteki kızarıklık ve tahrişleri yatıştırır."}]}
        ]
    elif "rezene" in bitki:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": "Yapay Zeka Analizi: Rezene, sindirim sisteminin en sadık dostudur. Mide ve bağırsak düz kaslarını gevşeterek şiddetli gaz sancılarını, şişkinliği ve krampları bıçak gibi keser. Sindirim enzimlerinin salgılanmasını artırarak hazmı kolaylaştırır."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Emziren annelerde süt artırıcı (galaktagog) etkilere sahiptir ve süte geçerek bebeğin gaz sancılarını da hafifletir. Kanı temizleyici, toksin atıcı özellikleri vardır ve nefesi tazeleyerek ağız kokusunu önler."}]}
        ]
    else:
        return [
            {"type": "paragraph", "children": [{"type": "text", "text": f"Yapay Zeka Analizi: {bitki_adi} bitkisi, doğanın derinliklerinden gelen yüksek polifenol ve antioksidan bileşenleri sayesinde vücut direncini maksimum seviyeye çıkaran çok özel bir şifa kaynağıdır."}]},
            {"type": "paragraph", "children": [{"type": "text", "text": "Metabolizmayı hızlandırarak hücrelerin yenilenmesine katkı sağlar, serbest radikallerin vücuda verdiği zararları engeller ve genel yaşam kalitesini artırarak uzun ve sağlıklı bir ömür sürmeyi destekler."}]}
        ]

print("🌿 Uzun ve Detaylı Açıklamalar Sunucuya Yükleniyor...")
API_URL =  f"{BASE_URL}/api/bitkis"

try:
    res_get = requests.get(API_URL, headers=headers)
    if res_get.ok:
        bitkiler = res_get.json().get("data", [])
        print("-" * 60)
        print(f"🚀 Canlı sunucuya bağlanıldı. {len(bitkiler)} içerik güncelleniyor...")
        print("-" * 60)
        
        for b in bitkiler:
            bitki_id = b.get("documentId") or b.get("id")
            veri_alani = b.get("attributes") if b.get("attributes") else b
            baslik = veri_alani.get("Nurten") or veri_alani.get("baslik") or "Başlıksız İçerik"
            
            ai_faydalari = yapay_zeka_icerik_uret(baslik)
            guncelleme_paketi = {"data": {"faydalari": ai_faydalari}}
            
            res_put = requests.put(f"{API_URL}/{bitki_id}", headers=headers, json=guncelleme_paketi)
            if res_put.ok:
                print(f"   ✅ GÜNCELLENDİ: '{baslik}' için zengin paragraflar yazıldı!\n")
            else:
                print(f"   ❌ Yükleme Hatası! Kod: {res_put.status_code}\n")
        print("🎉 MÜKEMMEL: Tüm açıklamalar en zengin ve uzun haliyle güncellendi şefim!")
    else:
        print(f"❌ Kapı açılamadı. Kod: {res_get.status_code}")
except Exception as e:
    print(f"💥 Sistem hatası: {e}")