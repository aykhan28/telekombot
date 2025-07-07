import logging

def get_customer_info(user_id: str) -> str:
    """Müşteri bilgilerini getirir (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Müşteri bilgileri alınıyor. Kullanıcı: {user_id}")
    try:
        from mock_apis import getUserInfo
        result = getUserInfo(user_id)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        customer = result["data"]
        logger.info(f"Müşteri bilgileri başarıyla alındı. Kullanıcı: {user_id}")
        return f"Müşteri: {customer['name']} {customer['surname']}, Paket: {customer['current_package']}, Bakiye: {customer['balance']} TL, Durum: {customer['payment_status']}"
    except Exception as e:
        logger.error(f"Müşteri bilgileri alınamadı. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Müşteri bilgileri alınamadı: {e}")

def get_billing_info(user_id: str, period: str = "current") -> str:
    """Fatura bilgilerini getirir (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Fatura bilgileri alınıyor. Kullanıcı: {user_id}, Dönem: {period}")
    try:
        from mock_apis import getBillingInfo
        result = getBillingInfo(user_id, period)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        billing_data = result["data"]
        bills_text = ", ".join([f"{bill['month']}: {bill['amount']} TL ({bill['status']})" for bill in billing_data["bills"]])
        logger.info(f"Fatura bilgileri başarıyla alındı. Kullanıcı: {user_id}")
        return f"Fatura bilgileri: {bills_text}. Toplam: {billing_data['total_amount']} TL, Ödenmemiş: {billing_data['unpaid_amount']} TL"
    except Exception as e:
        logger.error(f"Fatura bilgileri alınamadı. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Fatura bilgileri alınamadı: {e}")

def get_packages(user_id: str) -> str:
    """Mevcut paketleri listeler (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Paket bilgileri alınıyor. Kullanıcı: {user_id}")
    try:
        from mock_apis import getAvailablePackages
        result = getAvailablePackages(user_id)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        packages = result["data"]
        packages_text = ", ".join([f"{pkg['name']} ({pkg['price']} TL)" for pkg in packages])
        recommendations = result.get("recommendations", [])
        response = f"Mevcut paketler: {packages_text}"
        if recommendations:
            rec_text = ", ".join([f"{rec['package']['name']} ({rec['reason']})" for rec in recommendations[:2]])
            response += f". Öneriler: {rec_text}"
        logger.info(f"Paket bilgileri başarıyla alındı. Kullanıcı: {user_id}")
        return response
    except Exception as e:
        logger.error(f"Paket bilgileri alınamadı. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Paket bilgileri alınamadı: {e}")

def change_package(user_id: str, new_package_id: str) -> str:
    """Paket değiştirir (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Paket değişikliği başlatılıyor. Kullanıcı: {user_id}, Yeni Paket: {new_package_id}")
    try:
        from mock_apis import initiatePackageChange
        result = initiatePackageChange(user_id, new_package_id)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        logger.info(f"Paket değişikliği başarıyla tamamlandı. Kullanıcı: {user_id}")
        return result["message"]
    except Exception as e:
        logger.error(f"Paket değişikliği yapılamadı. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Paket değişikliği yapılamadı: {e}")

def reset_password(user_id: str) -> str:
    """Şifre sıfırlar (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Şifre sıfırlama işlemi başlatılıyor. Kullanıcı: {user_id}")
    try:
        from mock_apis import resetPassword
        result = resetPassword(user_id)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        logger.info(f"Şifre sıfırlama işlemi başarıyla tamamlandı. Kullanıcı: {user_id}")
        return result["message"]
    except Exception as e:
        logger.error(f"Şifre sıfırlama işlemi başarısız. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Şifre sıfırlama işlemi başarısız: {e}")

def create_ticket(user_id: str, issue_type: str, description: str) -> str:
    """Destek talebi oluşturur (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Destek talebi oluşturuluyor. Kullanıcı: {user_id}, Sorun Tipi: {issue_type}, Açıklama: {description}")
    try:
        from mock_apis import createSupportTicket
        result = createSupportTicket(user_id, issue_type, description)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        logger.info(f"Destek talebi başarıyla oluşturuldu. Kullanıcı: {user_id}")
        return result["message"]
    except Exception as e:
        logger.error(f"Destek talebi oluşturulamadı. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Destek talebi oluşturulamadı: {e}")

def process_payment(user_id: str, amount: float, payment_method: str) -> str:
    """Ödeme işlemi yapar (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Ödeme işlemi başlatılıyor. Kullanıcı: {user_id}, Tutar: {amount}, Ödeme Yöntemi: {payment_method}")
    try:
        from mock_apis import processPayment
        result = processPayment(user_id, amount, payment_method)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        logger.info(f"Ödeme işlemi başarıyla tamamlandı. Kullanıcı: {user_id}")
        return result["message"]
    except Exception as e:
        logger.error(f"Ödeme işlemi başarısız. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Ödeme işlemi başarısız: {e}")

def get_contract_info(user_id: str) -> str:
    """Sözleşme bilgilerini getirir (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Sözleşme bilgileri alınıyor. Kullanıcı: {user_id}")
    try:
        from mock_apis import getUserInfo
        result = getUserInfo(user_id)
        if not result.get("success"):
            raise Exception(result.get("error", "Bilinmeyen hata"))
        customer = result["data"]
        logger.info(f"Sözleşme bilgileri başarıyla alındı. Kullanıcı: {user_id}")
        return f"Sözleşme bitiş tarihi: {customer['contract_end_date']}, Müşteri olma tarihi: {customer['customer_since']}"
    except Exception as e:
        logger.error(f"Sözleşme bilgileri alınamadı. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Sözleşme bilgileri alınamadı: {e}")

def activate_service(user_id: str, service_type: str) -> str:
    """Hizmet aktifleştirir (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Hizmet aktifleştirme işlemi başlatılıyor. Kullanıcı: {user_id}, Hizmet Tipi: {service_type}")
    try:
        # Bu fonksiyon için özel bir mock API yok, genel bir yanıt döndür
        logger.info(f"Hizmet aktifleştirme işlemi başarıyla tamamlandı. Kullanıcı: {user_id}")
        return f"{service_type} hizmeti başarıyla aktifleştirildi. Aktivasyon 24 saat içinde tamamlanacak."
    except Exception as e:
        logger.error(f"Hizmet aktifleştirilemedi. Kullanıcı: {user_id}, Hata: {e}")
        raise Exception(f"Hizmet aktifleştirilemedi: {e}")

def search_knowledge_base(query: str) -> str:
    """Bilgi tabanında arama yapar (Mock API)"""
    logger = logging.getLogger(__name__)
    logger.info(f"Bilgi tabanı araması başlatılıyor. Arama sorgusu: {query}")
    try:
        # Basit bilgi tabanı simülasyonu
        knowledge_base = {
            "internet": "İnternet hızınızı artırmak için router'ınızı yeniden başlatabilirsiniz.",
            "fatura": "Faturalarınızı online olarak ödeyebilir veya banka şubelerinden yatırabilirsiniz.",
            "paket": "Paket değişikliği için müşteri hizmetlerimizi arayabilirsiniz.",
            "şifre": "Şifrenizi unuttuysanız, web sitemizden sıfırlayabilirsiniz.",
            "5g": "5G hizmeti şu anda sadece belirli şehirlerde mevcuttur.",
            "tv": "Dijital TV hizmetimiz için özel bir set-top box gereklidir."
        }
        for keyword, answer in knowledge_base.items():
            if keyword.lower() in query.lower():
                logger.info(f"Bilgi tabanı araması başarılı. Arama sorgusu: {query}, Bulunan anahtar: {keyword}")
                return answer
        logger.info(f"Bilgi tabanı araması başarısız. Arama sorgusu: {query}")
        return f"'{query}' ile ilgili bilgi bulundu: Bu konuda size yardımcı olabilirim."
    except Exception as e:
        logger.error(f"Bilgi tabanı araması başarısız: {e}")
        raise Exception(f"Bilgi tabanı araması başarısız: {e}") 