# Servis Formu Uygulaması - Kullanım Kılavuzu

## 📱 Uygulama Hakkında

Bu mobil uygulama, servis teknisyenlerinin kolayca servis formları oluşturmasına, müşteri ve teknisyen imzalarını almasına ve formları PDF olarak paylaşmasına olanak tanır.

## ✨ Özellikler

### 1. Ana Ekran (Geçmiş Formlar)
- Kaydedilmiş tüm servis formlarının listesi
- Her form kartında: Müşteri adı, yetkili, servis türü ve tarih
- Sağ alt köşedeki **mavi (+) butonu** ile yeni form oluşturma
- Forma tıklayarak detay görüntüleme

### 2. Yeni Form Oluşturma
#### Müşteri Bilgileri (Otomatik Tamamlama)
- **MÜŞTERİ - PROJE**: Yazmaya başladığınızda önceki müşteriler önerilir
- Müşteri seçildiğinde tüm bilgiler otomatik doldurulur:
  - Yetkili
  - Adres
  - Telefon
  - Proje No
  - E-mail

#### Servis Detayları
- Tarih seçimi (varsayılan: bugün)
- Başlama ve bitiş saatleri
- Hizmet türü seçimi:
  - ANLAŞMALI
  - GARANTİ
  - ÜCRETLİ
- Hizmet özeti, açıklama ve notlar

#### Kullanılan Malzemeler
- **"+" butonu** ile yeni malzeme ekleme
- Her malzeme için:
  - Malzeme adı (otomatik tamamlama)
  - Miktar
  - Birim
  - Birim fiyatı
  - Toplam fiyat (otomatik hesaplanır)
- **Çöp kutusu** ikonu ile malzeme silme

#### Fiyat Hesaplama (Otomatik)
- Malzeme toplamı
- Servis bedeli
- Ara toplam
- KDV (varsayılan %20, değiştirilebilir)
- **GENEL TOPLAM**

#### İmzalar
- **MÜŞTERİ YETKİLİSİ**
  - İsim girişi
  - İmza alanına tıklayarak imza atma
  - "Temizle" butonu ile imzayı silme
  
- **SİNAPSEN SERVİS YETKİLİSİ**
  - İsim girişi
  - İmza alanına tıklayarak imza atma
  - "Temizle" butonu ile imzayı silme

#### Kaydetme
- Sağ üstteki **✓ (tick)** butonuna tıklayarak formu kaydedin
- Yeni müşteri bilgileri otomatik olarak gelecek kullanım için kaydedilir

### 3. Form Detayı ve PDF
- Kaydedilmiş formu görüntüleme
- **Düzenle** butonu (kalem ikonu) ile formu düzenleme
- **Sil** butonu (çöp kutusu ikonu) ile formu silme
- **"PDF Oluştur ve Paylaş"** butonu:
  - Formu profesyonel PDF'e dönüştürür
  - Görseldeki formata uygun çıktı
  - Tüm bilgiler, malzeme listesi ve imzalar dahil
  - Paylaşma menüsü açılır (WhatsApp, Email, vb.)

## 🎯 Kullanım Senaryosu

1. **İlk Kullanım**: Yeni müşteri için form oluştur → Tüm bilgileri gir → Kaydet
2. **Tekrar Eden Müşteri**: Müşteri adını yazmaya başla → Önerilen müşteriyi seç → Bilgiler otomatik doldu → Sadece servis detaylarını gir
3. **Malzeme Ekleme**: "+" butonuna tıkla → Malzeme bilgilerini gir → Fiyatlar otomatik hesaplanır
4. **İmza Alma**: İmza alanına tıkla → Parmakla veya kalemle imza at → "Kaydet"
5. **PDF Paylaşma**: Form detayına git → "PDF Oluştur ve Paylaş" → Paylaşma yöntemini seç

## 💾 Veri Saklama

- Tüm veriler **cihazda** saklanır (AsyncStorage)
- İnternet bağlantısı gerekmez
- Müşteri bilgileri otomatik olarak kaydedilir
- Malzeme listesi gelecek kullanım için tutulur

## 📝 Logo Değiştirme

Logo dosyasını değiştirmek için:
```
/app/frontend/assets/images/logo.png
```
dosyasını kendi logonuzla değiştirin.

## 🔧 Teknik Detaylar

**Platform**: React Native + Expo SDK 53
**Navigasyon**: Expo Router (file-based routing)
**Depolama**: AsyncStorage
**İmza**: react-native-signature-canvas
**PDF**: expo-print
**Paylaşım**: expo-sharing

## 📲 Uygulamayı Kullanma

### Web Önizleme
- Tarayıcınızda açın: `http://localhost:3000`
- Masaüstü tarayıcıdan test edebilirsiniz

### Mobil Cihazda Test
1. Expo Go uygulamasını indirin (iOS/Android)
2. QR kodu tarayın (geliştirilecek)
3. Uygulamayı cihazınızda test edin

## 🎨 Tasarım Özellikleri

- **Modern iOS Stili**: Native görünüm ve his
- **Dokunma Dostu**: Minimum 44x44pt dokunma alanları
- **Responsive**: Farklı ekran boyutlarına uyumlu
- **Temiz Arayüz**: Basit ve kullanımı kolay
- **Türkçe**: Tam Türkçe dil desteği

## 🚀 Geliştirme Notları

Uygulama tamamen çalışır durumda ve aşağıdaki özellikleri içerir:
✅ Form oluşturma ve düzenleme
✅ Müşteri otomatik tamamlama
✅ Malzeme otomatik tamamlama
✅ Dinamik malzeme listesi
✅ Otomatik fiyat hesaplama
✅ İmza alma
✅ PDF oluşturma ve paylaşma
✅ Form listeleme ve silme
✅ Yerel veri saklama

## 🎉 Kullanıma Hazır!

Uygulamanız kullanıma hazır. İyi çalışmalar!
