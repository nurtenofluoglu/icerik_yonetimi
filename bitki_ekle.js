const STRAPI_URL = 'http://localhost:1337';

async function tumBitkileriYukle() {
    try {
        console.log('Strapi sunucusundan veriler çekiliyor...');
        const response = await fetch(`${STRAPI_URL}/api/bitkis?populate=*`);
        
        if (!response.ok) {
            throw new Error(`HTTP hatası! Durum: ${response.status}`);
        }

        const result = await response.json();
        const listeAlani = document.getElementById('bitki-listesi');
        listeAlani.innerHTML = ''; // Yükleniyor yazısını siliyoruz

        if (!result.data || result.data.length === 0) {
            listeAlani.innerHTML = '<p>Henüz veritabanında bitki bulunmuyor.</p>';
            return;
        }

        result.data.forEach(bitki => {
            const kart = document.createElement('div');
            kart.className = 'bitki-kart';

            // 🔍 1. GÖRSEL KONTROLÜ (Multiple Media olduğu için dizi olarak işliyoruz)
            let gorselHtml = '';
            
            if (bitki.gorsel && Array.isArray(bitki.gorsel) && bitki.gorsel.length > 0) {
                // Çoklu medyadan ilk resmi seçiyoruz
                const ilkGorsel = bitki.gorsel[0];
                const gorselYolu = ilkGorsel.url;

                if (gorselYolu) {
                    const tamGorselUrl = gorselYolu.startsWith('http') 
                        ? gorselYolu 
                        : `${STRAPI_URL}${gorselYolu}`;
                    
                    gorselHtml = `<img src="${tamGorselUrl}" alt="${bitki.Nurten || 'Bitki'}" style="max-width: 100%; max-height: 250px; object-fit: cover; border-radius: 8px; margin-top: 10px; display: block;">`;
                }
            }

            // 🔍 2. METİN KONTROLLERİ (Paneldeki Nurten ve faydalari alanlarına eşitledik)
            const bitkiAdi = bitki.Nurten || 'Başlıksız Bitki';
            const bitkiAciklamasi = bitki.faydalari || 'Açıklama girilmemiş.';

            kart.innerHTML = `
                <h2>${bitkiAdi}</h2>
                <p>${bitkiAciklamasi}</p>
                ${gorselHtml}
            `;

            listeAlani.appendChild(kart);
        });

    } catch (error) {
        console.error('Hata:', error);
        document.getElementById('bitki-listesi').innerHTML = '<p>Bağlantı hatası! Strapi arka planda açık mı?</p>';
    }
}

// Fonksiyonu çalıştır
tumBitkileriYukle();