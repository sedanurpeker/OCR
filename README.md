# Belge Bilgisi OCR Projesi

Bu proje, **belgelerdeki metinleri otomatik okuyarak** (örneğin faturalar, dekontlar, fişler)  
tarih, tutar ve belge numarası gibi önemli bilgileri çıkartır ve bir CSV dosyasına kaydeder.  
 **Tek tuşla OCR + Regex + CSV çıktısı!**

---

##  Özellikler
-  **Görselden metin okuma (OCR):** EasyOCR ile Türkçe ve İngilizce destekli metin tanıma  
-  **Bilgi çıkarımı:**  
  - Tarih (örn. `12.05.2024`)  
  - Tutar (örn. `1450.75 TL`)  
  - Belge / Fatura Numarası  
-  **Regex (Düzenli İfadeler):** Metin içinde akıllı desen arama  
-  **Sonuç kaydı:** Tüm belgelerden çıkarılan veriler `belge_bilgileri.csv` dosyasına kaydedilir  
-  **Kutucuklu ön izleme:** OCR ile tespit edilen metinler görsel üzerinde renklendirilir

---

##  Kullanılan Teknolojiler
- **Python 3.9+**
- **EasyOCR**
- **OpenCV**
- **Pandas**
- **Regex (re kütüphanesi)**

---

##  Kurulum ve Çalıştırma

### 1️. Gerekli kütüphaneleri yükle
```bash
pip install easyocr opencv-python pandas
```

### 2️. Klasör yapısını oluştur
```bash
OCR
 ┣  belgeler/              # OCR yapılacak görsellerin bulunduğu klasör
 ┣  ocr.py                 # Ana Python dosyası
 ┗  belge_bilgileri.csv    # Çıktı dosyası (otomatik oluşturulur)
```

### 3️. Görselleri ekle
belgeler klasörüne .jpg, .jpeg veya .png dosyalarını ekle.
  
### 4️. OCR işlemini başlat
```bash
python ocr.py
```
Çıkarılan bilgiler belge_bilgileri.csv dosyasına otomatik kaydedilecektir.


Developer: Sedanur Peker
