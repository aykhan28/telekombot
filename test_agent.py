#!/usr/bin/env python3
"""
Telekom Ajan Sistemi Test Dosyası
Bu dosya ajanın farklı senaryolarda nasıl çalıştığını test eder.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.central_agent import CentralAgent
from src.chat.ollama_client import ollama_chat
from src.mock_apis import MockTelecomAPIs

def test_ollama_connection():
    """Ollama bağlantısını test eder"""
    print("🔍 Ollama bağlantısı test ediliyor...")
    try:
        response = ollama_chat("Merhaba, bu bir test mesajıdır.")
        print(f"✅ Ollama yanıtı: {response[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Ollama bağlantı hatası: {e}")
        return False

def test_mock_apis():
    """Mock API'leri test eder"""
    print("\n🔍 Mock API'ler test ediliyor...")
    
    # Test müşteri ID'leri
    test_customers = ["05551234567", "05559876543", "05551112233"]
    
    for customer_id in test_customers:
        print(f"\n📱 Müşteri {customer_id} test ediliyor...")
        
        # Müşteri bilgileri
        from src.mock_apis import getUserInfo
        customer_info = getUserInfo(customer_id)
        if customer_info["success"]:
            print(f"✅ Müşteri bilgileri: {customer_info['data']['name']} {customer_info['data']['surname']}")
        else:
            print(f"❌ Müşteri bilgileri hatası: {customer_info['error']}")
        
        # Paket bilgileri
        from src.mock_apis import getAvailablePackages
        packages_info = getAvailablePackages(customer_id)
        if packages_info["success"]:
            print(f"✅ Paket sayısı: {len(packages_info['data'])}")
        else:
            print(f"❌ Paket bilgileri hatası: {packages_info['error']}")
        
        # Fatura bilgileri
        from src.mock_apis import getBillingInfo
        billing_info = getBillingInfo(customer_id)
        if billing_info["success"]:
            print(f"✅ Fatura sayısı: {billing_info['data']['bill_count']}")
        else:
            print(f"❌ Fatura bilgileri hatası: {billing_info['error']}")

def test_agent_scenarios():
    """Ajan senaryolarını test eder"""
    print("\n🤖 Ajan senaryoları test ediliyor...")
    
    # Ajan oluştur
    agent = CentralAgent(ollama_chat_func=ollama_chat)
    
    # Test senaryoları
    scenarios = [
        {
            "user_id": "05551234567",
            "message": "Faturamı öğrenmek istiyorum",
            "description": "Fatura sorgulama"
        },
        {
            "user_id": "05551234567", 
            "message": "Paketimi değiştirmek istiyorum",
            "description": "Paket değiştirme"
        },
        {
            "user_id": "05559876543",
            "message": "Şifremi unuttum, sıfırlamak istiyorum",
            "description": "Şifre sıfırlama"
        },
        {
            "user_id": "05551112233",
            "message": "İnternet hızım çok yavaş",
            "description": "Teknik destek"
        },
        {
            "user_id": "05551234567",
            "message": "Faturamı ödemek istiyorum",
            "description": "Ödeme işlemi"
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📝 Senaryo: {scenario['description']}")
        print(f"👤 Müşteri: {scenario['user_id']}")
        print(f"💬 Mesaj: {scenario['message']}")
        
        try:
            response = agent.generate_response(scenario['message'], scenario['user_id'])
            print(f"🤖 Yanıt: {response[:200]}...")
            print("✅ Başarılı")
        except Exception as e:
            print(f"❌ Hata: {e}")

def test_conversation_flow():
    """Konuşma akışını test eder"""
    print("\n🔄 Konuşma akışı test ediliyor...")
    
    agent = CentralAgent(ollama_chat_func=ollama_chat)
    user_id = "05551234567"
    
    # Konuşma akışı
    conversation = [
        "Merhaba, faturamı öğrenmek istiyorum",
        "Paketimi değiştirmek istiyorum, hangi paketler var?",
        "Premium 5G paketine geçmek istiyorum",
        "Teşekkürler, başka bir sorum yok"
    ]
    
    print(f"👤 Test müşterisi: {user_id}")
    
    for i, message in enumerate(conversation, 1):
        print(f"\n💬 Mesaj {i}: {message}")
        
        try:
            response = agent.generate_response(message, user_id)
            print(f"🤖 Yanıt {i}: {response[:150]}...")
        except Exception as e:
            print(f"❌ Hata: {e}")

def main():
    """Ana test fonksiyonu"""
    print("🚀 Telekom Ajan Sistemi Test Başlatılıyor...")
    print("=" * 50)
    
    # Ollama bağlantı testi
    if not test_ollama_connection():
        print("❌ Ollama bağlantısı başarısız. Testler durduruluyor.")
        return
    
    # Mock API testleri
    test_mock_apis()
    
    # Ajan senaryo testleri
    test_agent_scenarios()
    
    # Konuşma akışı testi
    test_conversation_flow()
    
    print("\n" + "=" * 50)
    print("✅ Tüm testler tamamlandı!")

if __name__ == "__main__":
    main()