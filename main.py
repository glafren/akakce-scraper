import requests
from bs4 import BeautifulSoup
import pandas as pd

# İşlenecek URL'ler listesi
urls = [
    "https://www.akakce.com/utu/en-ucuz-philips-azur-dst7511-80-7500-serisi-siyah-3200-w-buharli-fiyati,350070322.html",
    "https://www.akakce.com/utu/en-ucuz-philips-azur-8000-serisi-dst8050-20-3000-w-buharli-fiyati,102560874.html",
    "https://www.akakce.com/utu/en-ucuz-philips-5000-serisi-dst5010-10-2400-w-buharli-fiyati,1159918117.html"
]

# Kullanıcı aracısı başlığını ayarlayın
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Sonuçları saklayacak liste
results = []

# Her URL için fiyatları çekme
for url in urls:
    print(f"İşleniyor: {url}")
    
    # URL'ye bir istek gönder
    response = requests.get(url, headers=headers)
    
    # HTTP durum kodunu kontrol edin
    if response.status_code == 200:
        print("Sayfa başarıyla yüklendi.")
    else:
        print(f"Sayfa yüklenemedi. HTTP Durum Kodu: {response.status_code}")
        results.append({"URL": url, "Ortalama Fiyat": "Yüklenemedi"})
        continue

    # Sayfanın içeriğini BeautifulSoup ile parse et
    soup = BeautifulSoup(response.text, 'html.parser')

    # Fiyat bilgilerini içeren elementleri bul
    prices = soup.find_all('span', class_='pt_v8')
    
    # Fiyatları temizleyip, sayısal değere dönüştürme
    cleaned_prices = []
    for i, price in enumerate(prices):
        # İlk ve ikinci fiyatı atla, yalnızca üçüncü ve sonrasını dikkate al
        if i >= 2:
            price_text = price.get_text(strip=True).replace('\n', '').replace('  ', '').replace(' TL', '').replace('.', '').replace(',', '.')
            try:
                price_value = float(price_text)
                cleaned_prices.append(price_value)
            except ValueError:
                continue

    # Fiyatları küçükten büyüğe doğru sıralama
    sorted_prices = sorted(cleaned_prices)

    # İlk 3 fiyatın ortalamasını hesaplama
    if len(sorted_prices) >= 3:
        first_three_avg = sum(sorted_prices[:3]) / 3
        results.append({"URL": url, "Ortalama Fiyat": f"{first_three_avg:.2f} TL"})
    else:
        results.append({"URL": url, "Ortalama Fiyat": "Yeterli fiyat bulunamadı"})

# DataFrame oluşturma ve Excel dosyasına yazma
df = pd.DataFrame(results)
df.to_excel('ortalama_fiyatlar.xlsx', index=False, engine='openpyxl')

print("Sonuçlar 'ortalama_fiyatlar.xlsx' dosyasına kaydedildi.")
