# 🚀 Servis Formu Uygulaması - Kurulum Kılavuzu

## 📋 İçindekiler
1. [Sistem Gereksinimleri](#sistem-gereksinimleri)
2. [MongoDB Kurulumu](#mongodb-kurulumu)
3. [Backend Kurulumu](#backend-kurulumu)
4. [Frontend Kurulumu](#frontend-kurulumu)
5. [Servisleri Başlatma](#servisleri-başlatma)
6. [İlk Kullanım](#ilk-kullanım)
7. [Sorun Giderme](#sorun-giderme)

---

## 🖥️ Sistem Gereksinimleri

### Zorunlu Yazılımlar:
- **Node.js** v18+ ([İndir](https://nodejs.org/))
- **Python** 3.9+ ([İndir](https://www.python.org/))
- **MongoDB** 6.0+ ([İndir](https://www.mongodb.com/try/download/community))
- **Yarn** package manager ([İndir](https://yarnpkg.com/))

### Kontrol Edin:
```bash
node --version    # v18.0.0 veya üstü
python --version  # Python 3.9 veya üstü
mongo --version   # 6.0 veya üstü
yarn --version    # 1.22.0 veya üstü
```

---

## 🗄️ MongoDB Kurulumu

### Windows:
1. MongoDB Community Edition'ı indirin ve kurun
2. MongoDB Compass (GUI) ile birlikte gelir
3. Servis otomatik başlar (port: 27017)

### macOS:
```bash
# Homebrew ile
brew tap mongodb/brew
brew install mongodb-community@6.0
brew services start mongodb-community@6.0
```

### Linux (Ubuntu/Debian):
```bash
# MongoDB repository ekle
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Kur ve başlat
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

### MongoDB Bağlantı Kontrolü:
```bash
mongosh
# veya eski sürümlerde
mongo
```

**Çıktı:** `MongoDB shell version v6.0.x` görmelisiniz.

---

## 🔧 Backend Kurulumu

### 1. Backend Klasörüne Gidin:
```bash
cd backend
```

### 2. Python Virtual Environment Oluşturun:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Python Paketlerini Kurun:
```bash
pip install -r requirements.txt
```

### 4. .env Dosyasını Yapılandırın:

`.env` dosyası zaten mevcut, kontrol edin:
```bash
cat .env
```

**İçerik:**
```env
MONGO_URL=mongodb://localhost:27017/servis_formu
SECRET_KEY=sinapsen-2024-super-secret-key-change-in-production
```

**Önemli:** `SECRET_KEY`'i üretim ortamında mutlaka değiştirin!

```bash
# Güvenli key üretmek için:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Backend'i Test Edin:
```bash
python server.py
```

**Çıktı:**
```
INFO:     Uvicorn running on http://0.0.0.0:8001
INFO:     Application startup complete.
```

✅ Backend hazır! (Şimdilik Ctrl+C ile durdurun)

---

## 📱 Frontend Kurulumu

### 1. Frontend Klasörüne Gidin:
```bash
cd ../frontend
```

### 2. Node Paketlerini Kurun:
```bash
yarn install
# veya
npm install
```

### 3. .env Dosyasını Yapılandırın:

`.env` dosyasını açın ve düzenleyin:

**Geliştirme Ortamı (Local):**
```env
EXPO_PUBLIC_BACKEND_URL=http://localhost:8001
```

**Mobil Cihazda Test İçin:**
```env
# Bilgisayarınızın local IP adresini kullanın
EXPO_PUBLIC_BACKEND_URL=http://192.168.1.100:8001
```

**Local IP Nasıl Bulunur:**

**Windows:**
```bash
ipconfig
# "IPv4 Address" satırını bulun (örn: 192.168.1.100)
```

**macOS:**
```bash
ifconfig | grep "inet "
# 127.0.0.1 olmayan IP'yi kullanın
```

**Linux:**
```bash
hostname -I
```

### 4. Frontend'i Test Edin:
```bash
yarn start
# veya
npx expo start
```

**Çıktı:**
```
Metro waiting on exp://192.168.x.x:8081
Scan the QR code above with Expo Go (Android) or the Camera app (iOS)
```

✅ Frontend hazır!

---

## ▶️ Servisleri Başlatma

### Yöntem 1: Manuel (Geliştirme İçin)

**Terminal 1 - MongoDB (Zaten Çalışıyor Olmalı)**
```bash
# MongoDB servis olarak çalışıyorsa gerek yok
# Manuel başlatmak için:
mongod --dbpath /path/to/data/db
```

**Terminal 2 - Backend:**
```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
python server.py
```

**Terminal 3 - Frontend:**
```bash
cd frontend
yarn start
```

### Yöntem 2: Otomatik (Üretim İçin)

**PM2 ile Backend (Önerilir):**
```bash
# PM2 kur (global)
npm install -g pm2

# Backend'i başlat
cd backend
pm2 start server.py --name servis-backend --interpreter python

# Frontend'i başlat
cd ../frontend
pm2 start "yarn start" --name servis-frontend

# Servis durumunu kontrol et
pm2 status

# Log'ları görüntüle
pm2 logs servis-backend
pm2 logs servis-frontend

# Bilgisayar açılışında otomatik başlat
pm2 startup
pm2 save
```

---

## 🎯 İlk Kullanım

### 1. Expo Go ile Mobil Test:

**Android:**
- Google Play'den **Expo Go** uygulamasını indirin
- Terminal'deki QR kodu tarayın

**iOS:**
- App Store'dan **Expo Go** uygulamasını indirin
- Kamera ile QR kodu tarayın

### 2. İlk Admin Girişi:

Backend ilk başlatıldığında otomatik admin kullanıcısı oluşturur:

```
Kullanıcı Adı: lenex
Şifre: NTAG424DNA.3423
```

### 3. SMTP Ayarları:

**Gmail ile Mail Gönderimi:**

1. Google Hesap → Güvenlik → 2-Step Verification (Aktif edin)
2. App Passwords: https://myaccount.google.com/apppasswords
3. "Mail" seçin, cihaz adı girin (örn: "Sinapsen")
4. 16 haneli şifre kopyalayın

**Uygulamada:**
- Admin Panel → ⚙️ SMTP Ayarları
- Host: `smtp.gmail.com`
- Port: `587`
- Email: `servis@sinapsen.com`
- Password: `[16 haneli app password]`
- TLS: ✅ Aktif
- Kaydet → Test başarılı olmalı!

### 4. Mail Gövdesi:

- Admin Panel → 📧 Mail Gövdesi
- İstediğiniz metni girin
- Firma logonuz otomatik eklenecek

---

## 🐛 Sorun Giderme

### Backend Başlamıyor:

**Hata:** `ModuleNotFoundError: No module named 'fastapi'`
```bash
cd backend
pip install -r requirements.txt
```

**Hata:** `pymongo.errors.ServerSelectionTimeoutError`
```bash
# MongoDB çalışıyor mu kontrol et
mongosh
# veya
sudo systemctl status mongod
```

### Frontend Bağlanamıyor:

**Mobil cihazda "Network request failed":**

1. Backend URL'i düzeltin:
```bash
# .env dosyasında
EXPO_PUBLIC_BACKEND_URL=http://192.168.1.100:8001  # local IP kullanın
```

2. Firewall'da 8001 portunu açın:

**Windows:**
```
Windows Defender Firewall → Advanced Settings → Inbound Rules → New Rule
→ Port → TCP → 8001 → Allow
```

**macOS:**
```bash
# Firewall genelde sorun çıkarmaz, gerekirse:
sudo pfctl -d  # Geçici olarak kapat
```

**Linux:**
```bash
sudo ufw allow 8001/tcp
```

3. Her iki cihaz aynı WiFi ağında olmalı!

### MongoDB Bağlantı Sorunu:

```bash
# MongoDB loglarını kontrol et
tail -f /var/log/mongodb/mongod.log

# Manuel başlat
mongod --dbpath ~/data/db --logpath ~/data/log/mongod.log
```

### Port Zaten Kullanımda:

**Backend (8001):**
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8001 | xargs kill -9
```

**Frontend (8081/19000):**
```bash
# Expo cache temizle
cd frontend
npx expo start --clear
```

---

## 🚀 Üretim Ortamına Alma (Production)

### 1. Environment Variables:

**Backend (.env):**
```env
MONGO_URL=mongodb://localhost:27017/servis_formu_prod
SECRET_KEY=<GÜVENLI_KEY_BURAYA>
```

**Frontend (.env):**
```env
EXPO_PUBLIC_BACKEND_URL=https://api.sirketiniz.com
```

### 2. MongoDB Güvenlik:

```bash
# MongoDB authentication aktif et
mongosh
use admin
db.createUser({
  user: "servis_admin",
  pwd: "güvenli_şifre",
  roles: ["readWrite", "dbAdmin"]
})

# mongod.conf'da auth'u aktif et
security:
  authorization: enabled
```

**.env'de:**
```env
MONGO_URL=mongodb://servis_admin:güvenli_şifre@localhost:27017/servis_formu_prod
```

### 3. HTTPS (SSL) Kurulumu:

**Backend için Nginx:**
```nginx
server {
    listen 443 ssl;
    server_name api.sirketiniz.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 4. Expo Build:

**Android APK:**
```bash
cd frontend
eas build --platform android
```

**iOS (macOS gerekli):**
```bash
eas build --platform ios
```

---

## 📞 Destek

**GitHub Repository:** [Repository URL buraya]

**Sorunlar için:**
1. Logları kontrol edin (`pm2 logs`)
2. MongoDB loglarını kontrol edin
3. GitHub'da issue açın

---

## 📝 Notlar

- **Yedekleme:** MongoDB'yi düzenli yedekleyin
  ```bash
  mongodump --db servis_formu --out /backup/path
  ```

- **Logo Değiştirme:** `/frontend/assets/images/logo.png` dosyasını değiştirin

- **Port Değiştirme:** 
  - Backend: `server.py` → `uvicorn.run(port=8001)`
  - Frontend: `.env` → `EXPO_PUBLIC_BACKEND_URL`

- **Admin Şifre Değiştirme:** `backend/server.py` → `startup_event()` fonksiyonu

---

## ✅ Kurulum Tamamlandı!

Artık sisteminiz kendi sunucunuzda çalışıyor! 🎉

**Sonraki Adımlar:**
1. SMTP ayarlarını yapılandırın
2. Mail gövdesini özelleştirin
3. Yeni kullanıcılar ekleyin
4. İlk servis formunuzu oluşturun

**Başarılar! 🚀**
