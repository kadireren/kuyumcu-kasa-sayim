# Kuyumcu Kasa Sayım Programı

Kuyumcu işletmeleri için geliştirilmiş günlük kasa sayım programı. PyQt5 GUI ile modern ve kullanıcı dostu arayüz.

## 🏆 Özellikler

### 📊 Sayım Kalemleri
- **22 Ayar Tel Bilezik** (gram)
- **Çeyrek Lira** (adet)
- **Yarım Lira** (adet)
- **Zinet Lira** (adet)
- **Ata Lira** (adet)
- **Gramse** (adet)
- **Yarım Beşli** (adet)
- **Beşli** (adet)
- **24 Ayar Has Altın** (gram)
- **22 Ayar Hurda** (gram)
- **18 Ayar Hurda** (gram)
- **14 Ayar Hurda** (gram)
- **Türk Lirası** (adet)
- **Dolar** (adet)
- **Euro** (adet)

### ⚡ Ana Özellikler
- ✅ **5'li Grup Girişi**: Her kalem için 5 ayrı giriş alanı
- ✅ **Otomatik Toplam**: 5'li grupların otomatik toplamı
- ✅ **Fark Hesaplama**: Mevcut vs Olması Gereken karşılaştırması
- ✅ **Veri Doğrulama**: Sayısal giriş kontrolü ve hata gösterimi
- ✅ **JSON Kaydetme**: Tarih ve saat bilgisi ile otomatik dosya adlandırma
- ✅ **Veri Yükleme**: Önceki kayıtları geri yükleme
- ✅ **Detaylı Rapor**: Kompakt ve kapsamlı rapor penceresi
- ✅ **Türkçe Format**: TL için binlik ayırıcı (1.000.000)
- ✅ **Modern Arayüz**: PyQt5 ile geliştirilmiş kullanıcı dostu tasarım

## 🚀 Kurulum

### Gereksinimler
```bash
pip install PyQt5
```

### Çalıştırma
```bash
python3 kuyumcu_kasa_sayim_pyqt.py
```

## 📱 Kullanım

1. **Veri Girişi**: Her kalem için 5 ayrı giriş alanına değerleri girin
2. **Toplam Kontrol**: Otomatik hesaplanan toplamları kontrol edin
3. **Beklenen Değer**: "Olması Gereken" alanına beklenen değeri girin
4. **Fark Analizi**: Pozitif/negatif farkları renkli olarak görün
5. **Kaydetme**: Tarih ve saat bilgisi ile otomatik kayıt
6. **Rapor**: Detaylı rapor penceresi ile özet görünüm

## 🎨 Arayüz Özellikleri

- **Renkli Fark Gösterimi**:
  - 🟢 Pozitif fark (yeşil)
  - 🔴 Negatif fark (kırmızı)
  - 🟡 Sıfır fark (sarı)
- **Veri Doğrulama**:
  - ❌ Geçersiz girişlerde kırmızı border
  - ✅ Geçerli girişlerde normal görünüm
- **Responsive Tasarım**: Farklı ekran boyutlarına uyumlu

## 📁 Dosya Formatı

Kayıtlar JSON formatında saklanır:
```json
{
  "tarih": "07.09.2025 14:30",
  "kalemler": {
    "22 Ayar Tel Bilezik": {
      "degerler": [10.5, 15.2, 8.7, 12.3, 9.1],
      "toplam": 55.8,
      "olmasi_gereken": 55.0
    }
  }
}
```

## 🔧 Teknik Detaylar

- **Framework**: PyQt5
- **Dil**: Python 3
- **Platform**: Cross-platform (Windows, macOS, Linux)
- **Dosya Formatı**: JSON
- **Kodlama**: UTF-8

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

Abdulkadir Eren

---

**Not**: Bu program kuyumcu işletmelerinin günlük kasa sayım işlemlerini kolaylaştırmak için geliştirilmiştir.