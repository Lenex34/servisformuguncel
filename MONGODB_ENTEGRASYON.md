# MongoDB Entegrasyonu - Frontend Değişiklikleri

## ✅ Backend Hazır!

Backend'e şu endpoint'ler eklendi:

- `POST /api/forms` - Yeni form kaydet
- `GET /api/forms` - Formları listele (admin hepsini, user kendininkini görür)
- `GET /api/forms/{id}` - Tek form getir
- `PUT /api/forms/{id}` - Form güncelle (yetki kontrolü ile)
- `DELETE /api/forms/{id}` - Form sil (yetki kontrolü ile)

## Frontend'de Yapılması Gerekenler

### 1. service-form.tsx - Form Kaydetme

**Önceki:** AsyncStorage'a kaydediyordu
**Yeni:** Backend API'ye POST

```typescript
// ESKİ (service-form.tsx içinde):
await AsyncStorage.setItem('forms', JSON.stringify(allForms));

// YENİ:
const response = await fetch(`${BACKEND_URL}/api/forms`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    formNumber,
    customerName,
    authorizedPerson,
    // ... tüm form dataları
  }),
});
```

### 2. index.tsx - Form Listeleme

**Önceki:** AsyncStorage'dan oku
**Yeni:** Backend API'den GET

```typescript
// ESKİ:
const forms = await AsyncStorage.getItem('forms');

// YENİ:
const response = await fetch(`${BACKEND_URL}/api/forms`, {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
const forms = await response.json();
```

### 3. form-detail.tsx - Form Detay

**Önceki:** AsyncStorage'dan oku
**Yeni:** Backend API'den GET

```typescript
// ESKİ:
const forms = await AsyncStorage.getItem('forms');
const form = forms.find(f => f.id === id);

// YENİ:
const response = await fetch(`${BACKEND_URL}/api/forms/${id}`, {
  headers: {
    'Authorization': `Bearer ${token}`,
  },
});
const form = await response.json();
```

### 4. Form Silme - Yetki Kontrolü Ekle

```typescript
const handleDelete = async (formId: string, hasCustomerSignature: boolean) => {
  // Frontend'de kontrol
  if (hasCustomerSignature && !isAdmin) {
    Alert.alert('Hata', 'Müşteri imzalı formlar silinemez');
    return;
  }

  const response = await fetch(`${BACKEND_URL}/api/forms/${formId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });
  
  if (response.status === 403) {
    Alert.alert('Hata', 'Bu formu silme yetkiniz yok');
  }
};
```

### 5. Form Düzenleme - Yetki Kontrolü Ekle

```typescript
// Form düzenleme ekranında
if (formData.customerSignature && !isAdmin) {
  // Düzenleme butonlarını disable et
  Alert.alert('Bilgi', 'Müşteri imzalı formlar düzenlenemez');
  return;
}

// Güncelleme isteği
const response = await fetch(`${BACKEND_URL}/api/forms/${formId}`, {
  method: 'PUT',
  headers: {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(updatedFormData),
});
```

### 6. Müşteri İmzası Zorunlu Değil

**service-form.tsx içinde:**

```typescript
// ESKİ:
if (!customerSignature) {
  Alert.alert('Hata', 'Lütfen müşteri imzasını alın');
  return;
}

// YENİ: Bu kontrolü kaldır!
// Müşteri imzası zorunlu değil, boş olabilir
```

## Yetki Kuralları (Backend'de Kontrol Ediliyor)

### Form Silme:
- ✅ Admin: Tüm formları silebilir
- ✅ User: Sadece kendi formlarını (müşteri imzası yoksa)
- ❌ User: Müşteri imzalı formları silemez

### Form Düzenleme:
- ✅ Admin: Tüm formları düzenleyebilir
- ✅ User: Sadece kendi formlarını (müşteri imzası yoksa)
- ❌ User: Müşteri imzalı formları düzenleyemez

### Form Görüntüleme:
- ✅ Admin: Tüm formları görebilir
- ✅ User: Sadece kendi formlarını görebilir

## Örnek Kod Yapısı

### service-form.tsx - handleSaveForm:

```typescript
const handleSaveForm = async () => {
  // Validasyon (Müşteri imzası ZORUNLU DEĞİL!)
  if (!customerName || !technicianSignature) {
    Alert.alert('Hata', 'Gerekli alanları doldurun');
    return;
  }

  try {
    const response = await fetch(`${BACKEND_URL}/api/forms`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        formNumber,
        customerName,
        authorizedPerson,
        address,
        phone,
        projectNo,
        email,
        date,
        startTime,
        endTime,
        serviceType,
        serviceSummary,
        description,
        note,
        materials,
        materialTotal,
        serviceFee,
        amount,
        kdv,
        grandTotal,
        customerSignature: customerSignature || "", // Boş olabilir!
        technicianSignature,
        customerFeedback,
      }),
    });

    if (response.ok) {
      Alert.alert('Başarılı', 'Form kaydedildi');
      router.back();
    }
  } catch (error) {
    Alert.alert('Hata', 'Form kaydedilemedi');
  }
};
```

### index.tsx - loadForms:

```typescript
const loadForms = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/api/forms`, {
      headers: {
        'Authorization': `Bearer ${token}`,
      },
    });

    if (response.ok) {
      const forms = await response.json();
      
      // Grupla ve göster
      const grouped = forms.reduce((acc, form) => {
        const company = form.customerName;
        if (!acc[company]) acc[company] = [];
        acc[company].push(form);
        return acc;
      }, {});

      setCompanyGroups(Object.keys(grouped).map(name => ({
        companyName: name,
        forms: grouped[name],
      })));
    }
  } catch (error) {
    Alert.alert('Hata', 'Formlar yüklenemedi');
  }
};
```

## Test Senaryoları

1. **Yeni Form Kaydet** (müşteri imzasız) → MongoDB'ye kayıt edilmeli
2. **Admin Girişi** → Tüm formları görmeli
3. **User Girişi** → Sadece kendi formlarını görmeli
4. **User imzasız form sil** → Silebilmeli
5. **User imzalı form sil** → Silemeyip hata almalı
6. **Admin imzalı form sil** → Silebilmeli
7. **User imzasız form düzenle** → Düzenleyebilmeli
8. **User imzalı form düzenle** → Düzenleyemeyip hata almalı

## Dikkat Edilmesi Gerekenler

1. **Token:** Tüm isteklerde `Authorization: Bearer ${token}` header'ı ekleyin
2. **Error Handling:** 401 (Unauthorized), 403 (Forbidden), 404 (Not Found) hatalarını handle edin
3. **AsyncStorage Migration:** Mevcut AsyncStorage'daki formları MongoDB'ye taşımak isterseniz ayrı bir migration script yazılabilir
4. **Form Counter:** FormNumber'ı backend'de otomatik artırabilirsiniz (opsiyonel)

## AsyncStorage Temizleme (Opsiyonel)

Eğer eski formları taşımak istemiyorsanız:

```typescript
await AsyncStorage.removeItem('forms');
await AsyncStorage.removeItem('formCounter');
```

---

**Backend Hazır, Frontend'i Güncellemeye Başlayabilirsiniz! 🚀**
