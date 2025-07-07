# 🤖 Telekom Çağrı Merkezi AI Ajanı

Yarışma gereksinimleri doğrultusunda geliştirilmiş, LLM tabanlı niyet analizi ve dinamik araç seçimi yapabilen telekom operatörü çağrı merkezi yapay zeka ajanı.

## 🚀 Özellikler

### 🤖 Merkezi Ajan Sistemi
- **LLM Tabanlı Niyet Analizi**: Kullanıcı mesajlarını analiz ederek niyet belirleme
- **Dinamik Araç Seçimi**: Konuşma bağlamına göre otomatik araç seçimi
- **Çok Adımlı Karar Mekanizması**: Karmaşık senaryoları yönetme
- **Konuşma Durumu Takibi**: Kullanıcı konuşma geçmişini saklama

### 🎤 Ses İşleme
- **STT (Speech-to-Text)**: Google Speech Recognition entegrasyonu
- **TTS (Text-to-Speech)**: pyttsx3 ile Türkçe sesli yanıt
- **Gerçek Zamanlı Ses Kaydı**: Mikrofon entegrasyonu

### 📊 KPI Ölçümleme ve Raporlama
- **Kapsamlı Performans Metrikleri**: Yanıt süresi, başarı oranı, hata analizi
- **Gerçek Zamanlı İzleme**: Canlı performans takibi
- **Detaylı Raporlama**: JSON formatında kapsamlı raporlar
- **Görselleştirme**: Plotly ile interaktif grafikler

### 🧪 100 Test Senaryosu
- **Çeşitli Zorluk Seviyeleri**: Kolay, orta, zor senaryolar
- **Farklı Kategoriler**: Fatura, paket, teknik destek, ödeme, karmaşık senaryolar
- **Gerçekçi Diyaloglar**: Telekom sektörüne özel senaryolar
- **Otomatik Test Runner**: Toplu test çalıştırma

### 🎯 Desteklenen İşlemler
- **Fatura Sorgulama**: Güncel ve geçmiş faturalar
- **Paket Değiştirme**: Mevcut paketler ve öneriler
- **Teknik Destek**: Sorun bildirimi ve çözüm önerileri
- **Ödeme İşlemleri**: Online ödeme ve plan yönetimi
- **Şifre Sıfırlama**: Güvenlik işlemleri
- **Sözleşme Yönetimi**: Sözleşme bilgileri ve yenileme

## 📁 Proje Yapısı

```
telekombot/
├── src/
│   ├── app.py                 # Ana Streamlit uygulaması
│   ├── central_agent.py       # Merkezi ajan sistemi
│   ├── mock_apis.py           # Mock API fonksiyonları
│   ├── performance_metrics.py # KPI ölçümleme sistemi
│   ├── test_scenarios.py      # 100 test senaryosu
│   ├── test_runner.py         # Test çalıştırıcı
│   ├── test_dashboard.py      # Test sonuçları dashboard
│   ├── chat/
│   │   ├── context.py         # Konuşma bağlamı yönetimi
│   │   ├── prompt.py          # Prompt oluşturma
│   │   └── ollama_client.py   # Ollama entegrasyonu
│   ├── stt/
│   │   └── speech_to_text.py  # Ses tanıma
│   ├── tts/
│   │   └── text_to_speech.py  # Sesli yanıt
│   └── db/
│       └── mongo_client.py    # MongoDB bağlantısı
├── requirements.txt           # Python bağımlılıkları
└── README.md                 # Bu dosya
```

## 🛠️ Kurulum

### 1. Gereksinimler
- Python 3.8+
- MongoDB
- Ollama (llama3 modeli)

### 2. Bağımlılıkları Yükle
```bash
pip install -r requirements.txt
```

### 3. MongoDB'yi Başlat
```bash
# Windows
mongod

# Linux/Mac
sudo systemctl start mongod
```

### 4. Ollama'yı Başlat
```bash
ollama serve
ollama pull llama3
```

## 🚀 Kullanım

### Ana Uygulama
```bash
cd src
streamlit run app.py
```

### Test Dashboard
```bash
cd src
streamlit run test_dashboard.py
```

### 100 Test Senaryosunu Çalıştır
```bash
cd src
python test_runner.py
```

## 📊 Test Senaryoları

### Zorluk Seviyeleri
- **Kolay (20 senaryo)**: Basit fatura sorgulama
- **Orta (60 senaryo)**: Paket değiştirme, ödeme işlemleri
- **Zor (20 senaryo)**: Karmaşık çok adımlı senaryolar

### Kategoriler
- **Fatura Sorgulama**: 20 senaryo
- **Paket Değiştirme**: 20 senaryo
- **Teknik Destek**: 20 senaryo
- **Ödeme İşlemleri**: 20 senaryo
- **Karmaşık Senaryolar**: 20 senaryo

## 📈 Performans Metrikleri

### Ölçülen KPI'lar
- **Yanıt Süresi**: Ortalama, en hızlı, en yavaş
- **Başarı Oranı**: Kategori ve zorluk seviyesine göre
- **Hata Analizi**: Başarısız testlerin detaylı analizi
- **Araç Kullanımı**: Hangi araçların ne sıklıkla kullanıldığı

### Raporlama
- **JSON Raporları**: Detaylı test sonuçları
- **Görsel Dashboard**: Interaktif grafikler ve tablolar
- **Gerçek Zamanlı İzleme**: Canlı performans takibi

## 🎯 Yarışma Gereksinimleri

### ✅ Tamamlanan Özellikler
- [x] LLM tabanlı niyet analizi
- [x] Dinamik araç seçimi
- [x] Çok adımlı karar mekanizması
- [x] STT/TTS entegrasyonu
- [x] Karmaşık senaryo yönetimi
- [x] KPI ölçümleme sistemi
- [x] 100 farklı test senaryosu
- [x] Performans raporlama
- [x] Görselleştirme dashboard

### 🔧 Teknik Özellikler
- **Mimari**: Modüler ve genişletilebilir
- **Dil**: Python 3.8+
- **Veritabanı**: MongoDB
- **LLM**: Ollama (llama3)
- **UI**: Streamlit
- **Ses**: Google Speech Recognition + pyttsx3

## 📝 Örnek Kullanım

### Test Müşterisi ile Sohbet
```python
from central_agent import CentralAgent
from chat.ollama_client import ollama_chat

# Ajan oluştur
agent = CentralAgent(ollama_chat_func=ollama_chat)

# Test müşterisi ile sohbet
user_id = "05551234567"
response = agent.generate_response("Faturamı öğrenmek istiyorum", user_id)
print(response)
```

### Test Senaryosu Çalıştırma
```python
from test_runner import TestRunner

# Test runner oluştur
runner = TestRunner()

# Tüm testleri çalıştır
report = runner.run_all_tests()

# Sonuçları kaydet
filename = runner.save_results()
```

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit yapın (`git commit -m 'Add amazing feature'`)
4. Push yapın (`git push origin feature/amazing-feature`)
5. Pull Request oluşturun

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 📞 İletişim

Proje hakkında sorularınız için issue açabilirsiniz.

---

**Not**: Bu proje yarışma gereksinimleri doğrultusunda geliştirilmiştir ve gerçek telekom operatörü sistemleriyle entegrasyon için ek geliştirme gerektirebilir.
