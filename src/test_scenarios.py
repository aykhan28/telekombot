#!/usr/bin/env python3
"""
100 Farklı Test Senaryosu
Yarışma gereksinimleri için çeşitli zorluk seviyelerinde gerçekçi müşteri diyalogları
"""

import random
from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class TestScenario:
    scenario_id: int
    user_id: str
    messages: List[str]
    expected_intent: str
    expected_tools: List[str]
    difficulty: str  # "kolay", "orta", "zor"
    category: str
    description: str
    expected_success: bool = True

class TestScenarioGenerator:
    """100 farklı test senaryosu oluşturur"""
    
    def __init__(self):
        self.test_customers = ["05551234567", "05559876543", "05551112233"]
        self.scenarios = []
        self.generate_all_scenarios()
    
    def generate_all_scenarios(self):
        """Tüm test senaryolarını oluşturur"""
        
        # 1-20: Fatura Sorgulama Senaryoları (Kolay)
        self._generate_billing_scenarios()
        
        # 21-40: Paket Değiştirme Senaryoları (Orta)
        self._generate_package_change_scenarios()
        
        # 41-60: Teknik Destek Senaryoları (Orta-Zor)
        self._generate_technical_support_scenarios()
        
        # 61-80: Ödeme İşlemleri (Orta)
        self._generate_payment_scenarios()
        
        # 81-100: Karmaşık Senaryolar (Zor)
        self._generate_complex_scenarios()
    
    def _generate_billing_scenarios(self):
        """Fatura sorgulama senaryoları"""
        billing_messages = [
            "Faturamı öğrenmek istiyorum",
            "Bu ayki faturam ne kadar?",
            "Son faturalarımı görebilir miyim?",
            "Fatura borcum var mı?",
            "Geçen ayki faturamı öğrenmek istiyorum",
            "Fatura detaylarını görmek istiyorum",
            "Bu ay fatura ödemem gerekiyor mu?",
            "Fatura geçmişimi görebilir miyim?",
            "Son 3 ayın faturalarını öğrenmek istiyorum",
            "Fatura tutarımı kontrol etmek istiyorum",
            "Ödenmemiş faturalarım var mı?",
            "Fatura ödeme tarihini öğrenmek istiyorum",
            "Bu ayki faturam ne zaman gelecek?",
            "Fatura bilgilerimi görmek istiyorum",
            "Son fatura tutarımı öğrenmek istiyorum",
            "Fatura ödemelerimi kontrol etmek istiyorum",
            "Geçmiş faturalarımı görebilir miyim?",
            "Fatura durumumu öğrenmek istiyorum",
            "Bu ay fatura ödemem gerekiyor mu?",
            "Fatura detaylarını öğrenmek istiyorum"
        ]
        
        for i, message in enumerate(billing_messages, 1):
            self.scenarios.append(TestScenario(
                scenario_id=i,
                user_id=random.choice(self.test_customers),
                messages=[message],
                expected_intent="fatura_sorgula",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al"],
                difficulty="kolay",
                category="fatura_sorgulama",
                description=f"Fatura sorgulama - {message}"
            ))
    
    def _generate_package_change_scenarios(self):
        """Paket değiştirme senaryoları"""
        package_messages = [
            "Paketimi değiştirmek istiyorum",
            "Daha hızlı internet istiyorum",
            "Paket yükseltmek istiyorum",
            "Tarifemi değiştirmek istiyorum",
            "Daha ekonomik paket var mı?",
            "5G paketine geçmek istiyorum",
            "Paket düşürmek istiyorum",
            "Hangi paketler mevcut?",
            "Aile paketi istiyorum",
            "Öğrenci paketine geçmek istiyorum",
            "Sınırsız internet paketi istiyorum",
            "Paket önerileriniz neler?",
            "Mevcut paketimden memnun değilim",
            "Daha uygun fiyatlı paket var mı?",
            "Paket karşılaştırması yapabilir misiniz?",
            "Premium pakete geçmek istiyorum",
            "Ekonomik paket önerisi istiyorum",
            "Paket değişikliği yapabilir miyim?",
            "Hangi paket bana uygun?",
            "Paket bilgilerini görmek istiyorum"
        ]
        
        for i, message in enumerate(package_messages, 21):
            self.scenarios.append(TestScenario(
                scenario_id=i,
                user_id=random.choice(self.test_customers),
                messages=[message],
                expected_intent="paket_degistir",
                expected_tools=["musteri_bilgi_al", "paket_listesi_al"],
                difficulty="orta",
                category="paket_degistirme",
                description=f"Paket değiştirme - {message}"
            ))
    
    def _generate_technical_support_scenarios(self):
        """Teknik destek senaryoları"""
        tech_messages = [
            "İnternet hızım çok yavaş",
            "Bağlantı sorunu yaşıyorum",
            "İnternet kesiliyor",
            "WiFi şifremi unuttum",
            "Modem çalışmıyor",
            "İnternet bağlantım yok",
            "Hız testi yapabilir misiniz?",
            "Teknik sorun yaşıyorum",
            "İnternet yavaş geliyor",
            "Bağlantı problemi var",
            "Modem ışıkları yanmıyor",
            "İnternet sürekli kesiliyor",
            "Hız sorunu yaşıyorum",
            "Bağlantı kalitesi kötü",
            "Teknik destek istiyorum",
            "İnternet problemi var",
            "Modem ayarlarını değiştirmek istiyorum",
            "Bağlantı sorunumu çözmek istiyorum",
            "İnternet hızımı artırmak istiyorum",
            "Teknik yardım istiyorum",
            "Bağlantı problemi yaşıyorum"
        ]
        
        for i, message in enumerate(tech_messages, 41):
            self.scenarios.append(TestScenario(
                scenario_id=i,
                user_id=random.choice(self.test_customers),
                messages=[message],
                expected_intent="teknik_destek",
                expected_tools=["musteri_bilgi_al", "ticket_olustur"],
                difficulty="orta",
                category="teknik_destek",
                description=f"Teknik destek - {message}"
            ))
    
    def _generate_payment_scenarios(self):
        """Ödeme işlemleri senaryoları"""
        payment_messages = [
            "Faturamı ödemek istiyorum",
            "Online ödeme yapmak istiyorum",
            "Kredi kartı ile ödeme",
            "Banka kartı ile ödeme yapabilir miyim?",
            "Otomatik ödeme kurmak istiyorum",
            "Ödeme planı yapmak istiyorum",
            "Taksitli ödeme seçeneği var mı?",
            "Fatura ödememi yapmak istiyorum",
            "Ödeme yöntemlerini öğrenmek istiyorum",
            "Kredi kartı bilgilerimi güncellemek istiyorum",
            "Otomatik ödeme iptal etmek istiyorum",
            "Ödeme geçmişimi görmek istiyorum",
            "Fatura ödememi yapmak istiyorum",
            "Ödeme seçeneklerini öğrenmek istiyorum",
            "Kredi kartı ile ödeme yapmak istiyorum",
            "Banka havalesi ile ödeme",
            "Ödeme planı değiştirmek istiyorum",
            "Fatura ödememi yapmak istiyorum",
            "Ödeme yöntemi değiştirmek istiyorum",
            "Otomatik ödeme kurmak istiyorum"
        ]
        
        for i, message in enumerate(payment_messages, 61):
            self.scenarios.append(TestScenario(
                scenario_id=i,
                user_id=random.choice(self.test_customers),
                messages=[message],
                expected_intent="odeme",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al", "odeme_islem"],
                difficulty="orta",
                category="odeme_islemleri",
                description=f"Ödeme işlemi - {message}"
            ))
    
    def _generate_complex_scenarios(self):
        """Karmaşık senaryolar (çok adımlı)"""
        complex_scenarios = [
            # Senaryo 81: Fatura sorgulama + Ödeme
            TestScenario(
                scenario_id=81,
                user_id="05551234567",
                messages=[
                    "Faturamı öğrenmek istiyorum",
                    "Bu faturayı şimdi ödemek istiyorum"
                ],
                expected_intent="odeme",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al", "odeme_islem"],
                difficulty="zor",
                category="karmaşık_ödeme",
                description="Fatura sorgulama + Ödeme işlemi"
            ),
            
            # Senaryo 82: Paket sorgulama + Değiştirme
            TestScenario(
                scenario_id=82,
                user_id="05559876543",
                messages=[
                    "Hangi paketler mevcut?",
                    "Premium 5G paketine geçmek istiyorum"
                ],
                expected_intent="paket_degistir",
                expected_tools=["musteri_bilgi_al", "paket_listesi_al", "paket_degistir"],
                difficulty="zor",
                category="karmaşık_paket",
                description="Paket sorgulama + Değiştirme"
            ),
            
            # Senaryo 83: Teknik sorun + Destek talebi
            TestScenario(
                scenario_id=83,
                user_id="05551112233",
                messages=[
                    "İnternet hızım çok yavaş",
                    "Bu sorunu çözmek için ne yapabilirim?"
                ],
                expected_intent="teknik_destek",
                expected_tools=["musteri_bilgi_al", "ticket_olustur", "bilgi_tabanı_ara"],
                difficulty="zor",
                category="karmaşık_teknik",
                description="Teknik sorun + Çözüm arama"
            ),
            
            # Senaryo 84: Şifre sıfırlama + Güvenlik
            TestScenario(
                scenario_id=84,
                user_id="05551234567",
                messages=[
                    "Şifremi unuttum",
                    "Güvenlik ayarlarımı da kontrol etmek istiyorum"
                ],
                expected_intent="sifre_sifirla",
                expected_tools=["sifre_sifirla", "musteri_bilgi_al"],
                difficulty="orta",
                category="karmaşık_güvenlik",
                description="Şifre sıfırlama + Güvenlik kontrolü"
            ),
            
            # Senaryo 85: Sözleşme sorgulama + Yenileme
            TestScenario(
                scenario_id=85,
                user_id="05559876543",
                messages=[
                    "Sözleşme bilgilerimi öğrenmek istiyorum",
                    "Sözleşmemi yenilemek istiyorum"
                ],
                expected_intent="sozlesme_yenile",
                expected_tools=["musteri_bilgi_al", "sozlesme_bilgi_al"],
                difficulty="zor",
                category="karmaşık_sözleşme",
                description="Sözleşme sorgulama + Yenileme"
            ),
            
            # Senaryo 86: Hizmet aktivasyonu + Paket değişikliği
            TestScenario(
                scenario_id=86,
                user_id="05551112233",
                messages=[
                    "TV hizmeti eklemek istiyorum",
                    "Paketimi de değiştirmek istiyorum"
                ],
                expected_intent="hizmet_aktifleştir",
                expected_tools=["musteri_bilgi_al", "hizmet_aktifleştir", "paket_listesi_al"],
                difficulty="zor",
                category="karmaşık_hizmet",
                description="Hizmet aktivasyonu + Paket değişikliği"
            ),
            
            # Senaryo 87: Fatura itirazı + Çözüm
            TestScenario(
                scenario_id=87,
                user_id="05551234567",
                messages=[
                    "Bu fatura çok yüksek",
                    "İtiraz etmek istiyorum"
                ],
                expected_intent="sikayet",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al", "ticket_olustur"],
                difficulty="zor",
                category="karmaşık_şikayet",
                description="Fatura itirazı + Şikayet süreci"
            ),
            
            # Senaryo 88: Çoklu hizmet sorgulama
            TestScenario(
                scenario_id=88,
                user_id="05559876543",
                messages=[
                    "Tüm hizmetlerimi görmek istiyorum",
                    "Hangi hizmetler aktif?"
                ],
                expected_intent="musteri_bilgi",
                expected_tools=["musteri_bilgi_al"],
                difficulty="orta",
                category="karmaşık_hizmet_sorgulama",
                description="Çoklu hizmet sorgulama"
            ),
            
            # Senaryo 89: Ödeme planı + Paket değişikliği
            TestScenario(
                scenario_id=89,
                user_id="05551112233",
                messages=[
                    "Ödeme planı yapmak istiyorum",
                    "Aynı zamanda paketimi değiştirmek istiyorum"
                ],
                expected_intent="odeme",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al", "paket_listesi_al"],
                difficulty="zor",
                category="karmaşık_ödeme_paket",
                description="Ödeme planı + Paket değişikliği"
            ),
            
            # Senaryo 90: Acil durum + Teknik destek
            TestScenario(
                scenario_id=90,
                user_id="05551234567",
                messages=[
                    "İnternet hiç çalışmıyor",
                    "Acil yardım istiyorum"
                ],
                expected_intent="teknik_destek",
                expected_tools=["musteri_bilgi_al", "ticket_olustur"],
                difficulty="zor",
                category="karmaşık_acil",
                description="Acil durum + Teknik destek"
            ),
            
            # Senaryo 91: Bilgi sorgulama + Aksiyon
            TestScenario(
                scenario_id=91,
                user_id="05559876543",
                messages=[
                    "5G hizmeti hakkında bilgi istiyorum",
                    "Bu hizmeti aktifleştirmek istiyorum"
                ],
                expected_intent="hizmet_aktifleştir",
                expected_tools=["bilgi_tabanı_ara", "musteri_bilgi_al", "hizmet_aktifleştir"],
                difficulty="orta",
                category="karmaşık_bilgi_aksiyon",
                description="Bilgi sorgulama + Hizmet aktivasyonu"
            ),
            
            # Senaryo 92: Fatura sorgulama + İndirim talebi
            TestScenario(
                scenario_id=92,
                user_id="05551112233",
                messages=[
                    "Faturamı öğrenmek istiyorum",
                    "İndirim yapabilir misiniz?"
                ],
                expected_intent="sikayet",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al"],
                difficulty="orta",
                category="karmaşık_indirim",
                description="Fatura sorgulama + İndirim talebi"
            ),
            
            # Senaryo 93: Paket karşılaştırma + Seçim
            TestScenario(
                scenario_id=93,
                user_id="05551234567",
                messages=[
                    "Paketleri karşılaştırmak istiyorum",
                    "En uygun paketi seçmek istiyorum"
                ],
                expected_intent="paket_degistir",
                expected_tools=["musteri_bilgi_al", "paket_listesi_al"],
                difficulty="orta",
                category="karmaşık_karşılaştırma",
                description="Paket karşılaştırma + Seçim"
            ),
            
            # Senaryo 94: Güvenlik + Şifre değişikliği
            TestScenario(
                scenario_id=94,
                user_id="05559876543",
                messages=[
                    "Hesabımın güvenliğini kontrol etmek istiyorum",
                    "Şifremi değiştirmek istiyorum"
                ],
                expected_intent="sifre_sifirla",
                expected_tools=["musteri_bilgi_al", "sifre_sifirla"],
                difficulty="orta",
                category="karmaşık_güvenlik_şifre",
                description="Güvenlik kontrolü + Şifre değişikliği"
            ),
            
            # Senaryo 95: Çoklu sorun + Çözüm
            TestScenario(
                scenario_id=95,
                user_id="05551112233",
                messages=[
                    "Hem internet hem fatura sorunum var",
                    "Her ikisini de çözmek istiyorum"
                ],
                expected_intent="teknik_destek",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al", "ticket_olustur"],
                difficulty="zor",
                category="karmaşık_çoklu_sorun",
                description="Çoklu sorun + Çözüm arama"
            ),
            
            # Senaryo 96: Bilgi + Uygulama
            TestScenario(
                scenario_id=96,
                user_id="05551234567",
                messages=[
                    "İnternet hızını artırma yöntemlerini öğrenmek istiyorum",
                    "Bu yöntemleri uygulamak istiyorum"
                ],
                expected_intent="teknik_destek",
                expected_tools=["bilgi_tabanı_ara", "musteri_bilgi_al"],
                difficulty="orta",
                category="karmaşık_bilgi_uygulama",
                description="Bilgi alma + Uygulama"
            ),
            
            # Senaryo 97: Ödeme + Doğrulama
            TestScenario(
                scenario_id=97,
                user_id="05559876543",
                messages=[
                    "Faturamı ödedim",
                    "Ödemenin alındığını doğrulayabilir misiniz?"
                ],
                expected_intent="odeme",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al"],
                difficulty="orta",
                category="karmaşık_ödeme_doğrulama",
                description="Ödeme + Doğrulama"
            ),
            
            # Senaryo 98: Hizmet + Sorun bildirimi
            TestScenario(
                scenario_id=98,
                user_id="05551112233",
                messages=[
                    "TV hizmetim çalışmıyor",
                    "Bu sorunu bildirmek istiyorum"
                ],
                expected_intent="teknik_destek",
                expected_tools=["musteri_bilgi_al", "ticket_olustur"],
                difficulty="orta",
                category="karmaşık_hizmet_sorun",
                description="Hizmet sorunu + Bildirim"
            ),
            
            # Senaryo 99: Paket + Fatura sorgulama
            TestScenario(
                scenario_id=99,
                user_id="05551234567",
                messages=[
                    "Paketimi değiştirdim",
                    "Yeni faturamı öğrenmek istiyorum"
                ],
                expected_intent="fatura_sorgula",
                expected_tools=["musteri_bilgi_al", "fatura_bilgi_al"],
                difficulty="orta",
                category="karmaşık_paket_fatura",
                description="Paket değişikliği + Fatura sorgulama"
            ),
            
            # Senaryo 100: Genel bilgi + Aksiyon
            TestScenario(
                scenario_id=100,
                user_id="05559876543",
                messages=[
                    "Tüm hizmetleriniz hakkında bilgi istiyorum",
                    "En uygun paketi seçmek istiyorum"
                ],
                expected_intent="genel_soru",
                expected_tools=["bilgi_tabanı_ara", "musteri_bilgi_al", "paket_listesi_al"],
                difficulty="zor",
                category="karmaşık_genel_aksiyon",
                description="Genel bilgi + Paket seçimi"
            )
        ]
        
        self.scenarios.extend(complex_scenarios)
    
    def get_scenarios(self) -> List[TestScenario]:
        """Tüm senaryoları döndürür"""
        return self.scenarios
    
    def get_scenarios_by_difficulty(self, difficulty: str) -> List[TestScenario]:
        """Zorluk seviyesine göre senaryoları döndürür"""
        return [s for s in self.scenarios if s.difficulty == difficulty]
    
    def get_scenarios_by_category(self, category: str) -> List[TestScenario]:
        """Kategoriye göre senaryoları döndürür"""
        return [s for s in self.scenarios if s.category == category]
    
    def get_random_scenarios(self, count: int) -> List[TestScenario]:
        """Rastgele senaryolar döndürür"""
        return random.sample(self.scenarios, min(count, len(self.scenarios)))
    
    def get_statistics(self) -> Dict[str, Any]:
        """Senaryo istatistiklerini döndürür"""
        total = len(self.scenarios)
        difficulties = {}
        categories = {}
        
        for scenario in self.scenarios:
            difficulties[scenario.difficulty] = difficulties.get(scenario.difficulty, 0) + 1
            categories[scenario.category] = categories.get(scenario.category, 0) + 1
        
        return {
            "toplam_senaryo": total,
            "zorluk_dağılımı": difficulties,
            "kategori_dağılımı": categories,
            "müşteri_dağılımı": {
                "05551234567": len([s for s in self.scenarios if s.user_id == "05551234567"]),
                "05559876543": len([s for s in self.scenarios if s.user_id == "05559876543"]),
                "05551112233": len([s for s in self.scenarios if s.user_id == "05551112233"])
            }
        }

# Global senaryo üreticisi
scenario_generator = TestScenarioGenerator()

def get_all_test_scenarios() -> List[TestScenario]:
    """Tüm test senaryolarını döndürür"""
    return scenario_generator.get_scenarios()

def get_scenario_statistics() -> Dict[str, Any]:
    """Senaryo istatistiklerini döndürür"""
    return scenario_generator.get_statistics() 