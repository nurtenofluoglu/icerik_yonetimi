const strapiUrl = 'http://localhost:1337/api/bitkis'; 

const yeniBitki = {
  data: {
    Nurten: "Kudret Narı (Kodla Eklenen Şifa)", 
    faydalari: "Mideyi rahatlatır, sindirim sistemine çok iyi gelir. Bu veri kod yazarak eklenmiştir!", 
    tarih: "2026-05-20" 
  }
};

fetch(strapiUrl, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(yeniBitki),
})
.then(response => response.json())
.then(data => {
  console.log('=========================================');
  console.log('🎉 BAŞARILI! Bitki kodla Strapiye gönderildi.');
  console.log('=========================================');
})
.catch((error) => {
  console.error('Eyvah! Bir hata oluştu:', error);
});