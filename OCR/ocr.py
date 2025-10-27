import easyocr
import pandas as pd
import re
import cv2
import os

# Belge görsellerinizin bulunduğu klasör
BELGE_KLASORU = "belgeler"

# EasyOCR okuyucusunu başlatın
# Bu işlem biraz zaman alabilir, sadece bir kere yapılması yeterlidir.
okuyucu = easyocr.Reader(['tr', 'en'])

def ocr_ve_bilgi_cikart(gorsel_yolu):
    """
    Belge görselinden OCR yaparak metin ve yapılandırılmış bilgi çıkarır.
    """
    print(f"\n--- '{gorsel_yolu}' işleniyor... ---")
    
    # OCR işlemi
    sonuclar = okuyucu.readtext(gorsel_yolu)
    
    # Tüm metinleri birleştirerek daha kolay arama yapın
    tum_metin = "\n".join([sonuc[1] for sonuc in sonuclar])
    print("OCR ile çıkarılan tüm metin:\n", tum_metin)

    # Regex (Düzenli İfadeler) ile bilgi çıkarma
    bilgiler = {
        "Dosya Adı": os.path.basename(gorsel_yolu),
        "Tarih": "Bulunamadı",
        "Tutar": "Bulunamadı",
        "Belge No": "Bulunamadı"
    }
    
    # --- Tarih arama ---
    tarih_eslesme = re.search(r'(?:TARİH|TARIH|Date)[:\s]*(\d{1,2}[./-]\d{1,2}[./-]\d{4})', tum_metin, re.IGNORECASE)
    if tarih_eslesme:
        bilgiler["Tarih"] = tarih_eslesme.group(1)
    else:
        tarih_eslesme = re.search(r'\d{1,2}[./-]\d{1,2}[./-]\d{4}', tum_metin)
        if tarih_eslesme:
            bilgiler["Tarih"] = tarih_eslesme.group(0)

    # --- Tutar arama ---
    # Bu regex, "TOPLAM" kelimesinden sonra gelen ve boşluklarla ayrılmış sayıları da yakalar
    tutar_eslesme = re.search(r'(?:TOPLAM|GENEL\s?TOPLAM|TUTAR|TOTAL)\s*[\D\s]*?(\d{1,3}(?:,?\s?\d{3})*(?:[.,]\s?\d{2}))', tum_metin, re.IGNORECASE)
    if tutar_eslesme:
        tutar_str = tutar_eslesme.group(1)
        tutar_str = tutar_str.replace(' ', '').replace(',', '.')
        bilgiler["Tutar"] = tutar_str
    else:
        # Alternatif olarak para birimi sembolleriyle arama yap
        tutar_eslesme = re.search(r'(\d{1,3}(?:,?\s?\d{3})*(?:[.,]\s?\d{2}))\s?(?:TL|\$|EURO)', tum_metin, re.IGNORECASE)
        if tutar_eslesme:
            tutar_str = tutar_eslesme.group(1)
            tutar_str = tutar_str.replace(' ', '').replace(',', '.')
            bilgiler["Tutar"] = tutar_str

    # --- Belge No arama ---
    belge_no_eslesme = re.search(r'(?:NO|No\.|Numara|Fatura\s?No|Belge\s?No|ISYERI\s?No)[:\s]*(\S+)', tum_metin, re.IGNORECASE)
    if belge_no_eslesme:
        belge_no = belge_no_eslesme.group(1).replace('-', '').replace(':', '')
        bilgiler["Belge No"] = belge_no
    
    print("Çıkarılan Bilgiler:", bilgiler)
    
    return bilgiler, sonuclar


def gorsel_uzerine_kutucuk_ciz(gorsel_yolu, ocr_sonuclari):
    """
    OCR sonuçlarını kullanarak orijinal görsel üzerine kutucuk ve metin çizer.
    """
    img = cv2.imread(gorsel_yolu)
    
    if img is None:
        print(f"Hata: '{gorsel_yolu}' dosyası okunamadı.")
        return

    # Her bir OCR sonucunu işleyin
    for (bbox, metin, olasilik) in ocr_sonuclari:
        # Kutucuk koordinatlarını al
        (sol_ust, sag_ust, sag_alt, sol_alt) = bbox
        p1 = (int(sol_ust[0]), int(sol_ust[1]))
        p2 = (int(sag_alt[0]), int(sag_alt[1]))
        
        # Kutucuk ve metin ekle
        cv2.rectangle(img, p1, p2, (0, 255, 0), 2)
        cv2.putText(img, metin, p1, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Kutucuklu görüntüyü gösterin
    pencere_adi = f"OCR Sonucu: {os.path.basename(gorsel_yolu)}"
    cv2.imshow(pencere_adi, img)
    print("Görsel üzerinde kutucuklar gösteriliyor. Kapatmak için bir tuşa basın.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def ana_program():
    """
    Ana program akışını yönetir.
    """
    if not os.path.exists(BELGE_KLASORU):
        print(f"'{BELGE_KLASORU}' klasörü bulunamadı. Lütfen belge görsellerinizi bu klasöre ekleyin.")
        return
        
    belge_listesi = [os.path.join(BELGE_KLASORU, f) for f in os.listdir(BELGE_KLASORU) if f.endswith(('.jpg', '.jpeg', '.png'))]

    if not belge_listesi:
        print(f"'{BELGE_KLASORU}' klasöründe belge görseli bulunamadı. Lütfen dosya ekleyip tekrar deneyin.")
        return

    cikartilan_bilgiler = []
    
    for belge_yolu in belge_listesi:
        bilgiler, ocr_sonuclari = ocr_ve_bilgi_cikart(belge_yolu)
        cikartilan_bilgiler.append(bilgiler)
        
        gorsel_uzerine_kutucuk_ciz(belge_yolu, ocr_sonuclari)
        
    df = pd.DataFrame(cikartilan_bilgiler)
    df.to_csv("belge_bilgileri.csv", index=False, encoding='utf-8')
    print("\n--------------------------")
    print("İşlem tamamlandı!")
    print("Tüm belgelerden çıkarılan bilgiler 'belge_bilgileri.csv' dosyasına kaydedildi.")
    print("--------------------------")
    

if __name__ == "__main__":
    ana_program()