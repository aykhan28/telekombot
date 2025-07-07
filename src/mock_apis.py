import json
import time
import random
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class MockTelecomAPIs:
    """Telekom operatörü sistemleri için mock API'ler"""
    
    def __init__(self):
        # Sahte veritabanı
        self.customers = {
            "05551234567": {
                "name": "Ahmet",
                "surname": "Yılmaz",
                "current_package": "Sınırsız 4G",
                "contract_end_date": "2025-08-01",
                "payment_status": "Ödendi",
                "balance": 150.50,
                "address": "İstanbul, Kadıköy",
                "email": "ahmet.yilmaz@email.com",
                "phone_number": "05551234567",
                "customer_since": "2020-03-15",
                "last_payment_date": "2024-12-01",
                "credit_limit": 500.0,
                "active_services": ["internet", "mobile", "tv"]
            },
            "05559876543": {
                "name": "Fatma",
                "surname": "Demir",
                "current_package": "Ekonomik Paket",
                "contract_end_date": "2024-12-31",
                "payment_status": "Gecikmiş",
                "balance": -75.25,
                "address": "Ankara, Çankaya",
                "email": "fatma.demir@email.com",
                "phone_number": "05559876543",
                "customer_since": "2022-07-20",
                "last_payment_date": "2024-11-01",
                "credit_limit": 300.0,
                "active_services": ["internet", "mobile"]
            },
            "05551112233": {
                "name": "Mehmet",
                "surname": "Kaya",
                "current_package": "Premium 5G",
                "contract_end_date": "2025-06-15",
                "payment_status": "Ödendi",
                "balance": 0.0,
                "address": "İzmir, Konak",
                "email": "mehmet.kaya@email.com",
                "phone_number": "05551112233",
                "customer_since": "2019-11-10",
                "last_payment_date": "2024-12-01",
                "credit_limit": 1000.0,
                "active_services": ["internet", "mobile", "tv", "landline"]
            }
        }
        
        self.packages = {
            "PN1": {
                "id": "PN1",
                "name": "Sınırsız 4G",
                "price": 250.0,
                "details": "Sınırsız internet, 1000 dakika konuşma, 100 SMS",
                "internet_speed": "100Mbps",
                "data_limit": "Sınırsız",
                "voice_minutes": 1000,
                "sms_count": 100,
                "contract_duration": 12,
                "activation_fee": 0.0,
                "available_regions": ["İstanbul", "Ankara", "İzmir", "Bursa"]
            },
            "PN2": {
                "id": "PN2",
                "name": "Premium 5G",
                "price": 350.0,
                "details": "Sınırsız 5G internet, sınırsız konuşma, sınırsız SMS",
                "internet_speed": "1Gbps",
                "data_limit": "Sınırsız",
                "voice_minutes": -1,  # Sınırsız
                "sms_count": -1,  # Sınırsız
                "contract_duration": 24,
                "activation_fee": 50.0,
                "available_regions": ["İstanbul", "Ankara", "İzmir"]
            },
            "PN3": {
                "id": "PN3",
                "name": "Ekonomik Paket",
                "price": 150.0,
                "details": "10GB internet, 500 dakika konuşma, 50 SMS",
                "internet_speed": "50Mbps",
                "data_limit": "10GB",
                "voice_minutes": 500,
                "sms_count": 50,
                "contract_duration": 12,
                "activation_fee": 0.0,
                "available_regions": ["Tüm Türkiye"]
            },
            "PN4": {
                "id": "PN4",
                "name": "Aile Paketi",
                "price": 400.0,
                "details": "4 hataya sınırsız internet, sınırsız konuşma",
                "internet_speed": "200Mbps",
                "data_limit": "Sınırsız",
                "voice_minutes": -1,
                "sms_count": 200,
                "contract_duration": 24,
                "activation_fee": 25.0,
                "available_regions": ["Tüm Türkiye"]
            },
            "PN5": {
                "id": "PN5",
                "name": "Öğrenci Paketi",
                "price": 120.0,
                "details": "5GB internet, 300 dakika konuşma, 30 SMS",
                "internet_speed": "25Mbps",
                "data_limit": "5GB",
                "voice_minutes": 300,
                "sms_count": 30,
                "contract_duration": 12,
                "activation_fee": 0.0,
                "available_regions": ["Tüm Türkiye"]
            }
        }
        
        self.bills = {
            "05551234567": [
                {"month": "Aralık 2024", "amount": 250.0, "due_date": "2024-12-15", "status": "Ödendi", "paid_date": "2024-12-10"},
                {"month": "Kasım 2024", "amount": 250.0, "due_date": "2024-11-15", "status": "Ödendi", "paid_date": "2024-11-12"},
                {"month": "Ekim 2024", "amount": 250.0, "due_date": "2024-10-15", "status": "Ödendi", "paid_date": "2024-10-14"}
            ],
            "05559876543": [
                {"month": "Aralık 2024", "amount": 150.0, "due_date": "2024-12-15", "status": "Gecikmiş", "paid_date": None},
                {"month": "Kasım 2024", "amount": 150.0, "due_date": "2024-11-15", "status": "Gecikmiş", "paid_date": None},
                {"month": "Ekim 2024", "amount": 150.0, "due_date": "2024-10-15", "status": "Ödendi", "paid_date": "2024-10-20"}
            ],
            "05551112233": [
                {"month": "Aralık 2024", "amount": 350.0, "due_date": "2024-12-15", "status": "Ödendi", "paid_date": "2024-12-01"},
                {"month": "Kasım 2024", "amount": 350.0, "due_date": "2024-11-15", "status": "Ödendi", "paid_date": "2024-11-01"},
                {"month": "Ekim 2024", "amount": 350.0, "due_date": "2024-10-15", "status": "Ödendi", "paid_date": "2024-10-01"}
            ]
        }
        
        self.pending_changes = {}
        self.support_tickets = {}
        self.ticket_counter = 1000

    def getUserInfo(self, user_id: str) -> Dict[str, Any]:
        """
        Kullanıcı bilgilerini getirir
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            
        Returns:
            Kullanıcı bilgileri sözlüğü veya hata mesajı
        """
        try:
            # Simüle edilmiş API gecikmesi
            time.sleep(random.uniform(0.1, 0.5))
            
            if user_id == '00000000000':
                return {"success": False, "error": "Müşteri bulunamadı. Lütfen geçerli bir müşteri numarası giriniz."}

            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "error_code": "CUSTOMER_NOT_FOUND"
                }
            
            customer = self.customers[user_id]
            return {
                "success": True,
                "data": {
                    "name": customer["name"],
                    "surname": customer["surname"],
                    "current_package": customer["current_package"],
                    "contract_end_date": customer["contract_end_date"],
                    "payment_status": customer["payment_status"],
                    "balance": customer["balance"],
                    "address": customer["address"],
                    "email": customer["email"],
                    "phone_number": customer["phone_number"],
                    "customer_since": customer["customer_since"],
                    "last_payment_date": customer["last_payment_date"],
                    "credit_limit": customer["credit_limit"],
                    "active_services": customer["active_services"]
                }
            }
        except Exception as e:
            logger.error(f"getUserInfo hatası: {e}")
            return {
                "success": False,
                "error": "Sistem hatası oluştu",
                "error_code": "SYSTEM_ERROR"
            }

    def getAvailablePackages(self, user_id: str) -> Dict[str, Any]:
        """
        Kullanıcının mevcut durumuna göre uygun paketleri listeler
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            
        Returns:
            Uygun paketler listesi
        """
        try:
            time.sleep(random.uniform(0.2, 0.8))
            
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "error_code": "CUSTOMER_NOT_FOUND"
                }
            
            customer = self.customers[user_id]
            available_packages = []
            
            # Müşterinin durumuna göre paket filtreleme
            for package_id, package in self.packages.items():
                # Gecikmiş ödemesi olan müşteriler için kısıtlama
                if customer["payment_status"] == "Gecikmiş" and package["price"] > 200:
                    continue
                
                # Müşterinin adresine göre bölge kontrolü
                customer_region = self._get_region_from_address(customer["address"])
                if customer_region not in package["available_regions"] and "Tüm Türkiye" not in package["available_regions"]:
                    continue
                
                available_packages.append(package)
            
            return {
                "success": True,
                "data": available_packages,
                "current_package": customer["current_package"],
                "recommendations": self._get_package_recommendations(customer, available_packages)
            }
        except Exception as e:
            logger.error(f"getAvailablePackages hatası: {e}")
            return {
                "success": False,
                "error": "Paket bilgileri alınamadı",
                "error_code": "SYSTEM_ERROR"
            }

    def initiatePackageChange(self, user_id: str, package_id: str) -> Dict[str, Any]:
        """
        Paket değişikliği başlatır
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            package_id: Değiştirilmek istenen paketin ID'si
            
        Returns:
            İşlem sonucu
        """
        try:
            time.sleep(random.uniform(0.5, 1.5))
            
            # Müşteri kontrolü
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "error_code": "CUSTOMER_NOT_FOUND"
                }
            
            # Paket kontrolü
            if package_id not in self.packages:
                return {
                    "success": False,
                    "error": "Paket bulunamadı",
                    "error_code": "PACKAGE_NOT_FOUND"
                }
            
            customer = self.customers[user_id]
            package = self.packages[package_id]
            
            # Kontroller
            checks = self._validate_package_change(customer, package)
            if not checks["valid"]:
                return {
                    "success": False,
                    "error": checks["reason"],
                    "error_code": checks["error_code"]
                }
            
            # Paket değişikliği kaydetme
            change_id = f"CHG-{int(time.time())}"
            self.pending_changes[change_id] = {
                "user_id": user_id,
                "old_package": customer["current_package"],
                "new_package": package["name"],
                "package_id": package_id,
                "request_date": datetime.now().isoformat(),
                "status": "Beklemede",
                "activation_date": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            
            return {
                "success": True,
                "message": f"Paket değişikliği talebiniz alınmıştır. 24 saat içinde aktifleşecektir.",
                "change_id": change_id,
                "activation_date": self.pending_changes[change_id]["activation_date"],
                "new_package_details": package
            }
        except Exception as e:
            logger.error(f"initiatePackageChange hatası: {e}")
            return {
                "success": False,
                "error": "Paket değişikliği işlemi başarısız",
                "error_code": "SYSTEM_ERROR"
            }

    def getBillingInfo(self, user_id: str, period: str = "current") -> Dict[str, Any]:
        """
        Fatura bilgilerini getirir
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            period: Dönem (current, last_3_months, last_6_months)
            
        Returns:
            Fatura bilgileri
        """
        try:
            time.sleep(random.uniform(0.2, 0.6))
            
            if user_id not in self.bills:
                return {
                    "success": False,
                    "error": "Fatura bilgisi bulunamadı",
                    "error_code": "BILLING_NOT_FOUND"
                }
            
            bills = self.bills[user_id]
            
            if period == "current":
                bills = bills[:1]
            elif period == "last_3_months":
                bills = bills[:3]
            elif period == "last_6_months":
                bills = bills[:6]
            
            total_amount = sum(bill["amount"] for bill in bills)
            unpaid_amount = sum(bill["amount"] for bill in bills if bill["status"] == "Gecikmiş")
            
            return {
                "success": True,
                "data": {
                    "bills": bills,
                    "total_amount": total_amount,
                    "unpaid_amount": unpaid_amount,
                    "bill_count": len(bills)
                }
            }
        except Exception as e:
            logger.error(f"getBillingInfo hatası: {e}")
            return {
                "success": False,
                "error": "Fatura bilgileri alınamadı",
                "error_code": "SYSTEM_ERROR"
            }

    def processPayment(self, user_id: str, amount: float, payment_method: str) -> Dict[str, Any]:
        """
        Ödeme işlemi yapar
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            amount: Ödeme tutarı
            payment_method: Ödeme yöntemi (credit_card, bank_transfer, etc.)
            
        Returns:
            Ödeme sonucu
        """
        try:
            time.sleep(random.uniform(1.0, 2.0))
            
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "error_code": "CUSTOMER_NOT_FOUND"
                }
            
            # Ödeme simülasyonu
            payment_success = random.random() > 0.05  # %95 başarı oranı
            
            if not payment_success:
                return {
                    "success": False,
                    "error": "Ödeme işlemi başarısız. Lütfen kart bilgilerinizi kontrol edin.",
                    "error_code": "PAYMENT_FAILED"
                }
            
            # Müşteri bakiyesini güncelle
            self.customers[user_id]["balance"] += amount
            self.customers[user_id]["last_payment_date"] = datetime.now().strftime("%Y-%m-%d")
            
            # Ödeme geçmişi kaydetme
            payment_id = f"PAY-{int(time.time())}"
            
            return {
                "success": True,
                "message": f"{amount} TL ödeme {payment_method} ile başarıyla işleme alındı.",
                "payment_id": payment_id,
                "new_balance": self.customers[user_id]["balance"],
                "payment_date": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"processPayment hatası: {e}")
            return {
                "success": False,
                "error": "Ödeme işlemi başarısız",
                "error_code": "SYSTEM_ERROR"
            }

    def createSupportTicket(self, user_id: str, issue_type: str, description: str) -> Dict[str, Any]:
        """
        Destek talebi oluşturur
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            issue_type: Sorun tipi
            description: Sorun açıklaması
            
        Returns:
            Talep sonucu
        """
        try:
            time.sleep(random.uniform(0.3, 0.8))
            
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "error_code": "CUSTOMER_NOT_FOUND"
                }
            
            self.ticket_counter += 1
            ticket_id = f"TKT-{self.ticket_counter}"
            
            self.support_tickets[ticket_id] = {
                "user_id": user_id,
                "issue_type": issue_type,
                "description": description,
                "status": "Açık",
                "priority": self._determine_priority(issue_type),
                "created_date": datetime.now().isoformat(),
                "estimated_resolution": (datetime.now() + timedelta(days=2)).isoformat()
            }
            
            return {
                "success": True,
                "message": f"Destek talebiniz oluşturuldu. Talep numarası: {ticket_id}",
                "ticket_id": ticket_id,
                "priority": self.support_tickets[ticket_id]["priority"],
                "estimated_resolution": self.support_tickets[ticket_id]["estimated_resolution"]
            }
        except Exception as e:
            logger.error(f"createSupportTicket hatası: {e}")
            return {
                "success": False,
                "error": "Destek talebi oluşturulamadı",
                "error_code": "SYSTEM_ERROR"
            }

    def resetPassword(self, user_id: str) -> Dict[str, Any]:
        """
        Şifre sıfırlama işlemi
        
        Args:
            user_id: Telefon numarası veya müşteri ID'si
            
        Returns:
            İşlem sonucu
        """
        try:
            time.sleep(random.uniform(0.5, 1.0))
            
            if user_id not in self.customers:
                return {
                    "success": False,
                    "error": "Müşteri bulunamadı",
                    "error_code": "CUSTOMER_NOT_FOUND"
                }
            
            customer = self.customers[user_id]
            
            # Şifre sıfırlama bağlantısı oluşturma
            reset_token = f"RESET-{int(time.time())}"
            reset_link = f"https://selfcare.telekom.com/reset-password?token={reset_token}"
            
            return {
                "success": True,
                "message": "Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.",
                "email": customer["email"],
                "reset_link": reset_link,
                "expires_in": "24 saat"
            }
        except Exception as e:
            logger.error(f"resetPassword hatası: {e}")
            return {
                "success": False,
                "error": "Şifre sıfırlama işlemi başarısız",
                "error_code": "SYSTEM_ERROR"
            }

    # Yardımcı fonksiyonlar
    def _get_region_from_address(self, address: str) -> str:
        """Adresten bölge bilgisini çıkarır"""
        if "İstanbul" in address:
            return "İstanbul"
        elif "Ankara" in address:
            return "Ankara"
        elif "İzmir" in address:
            return "İzmir"
        elif "Bursa" in address:
            return "Bursa"
        else:
            return "Diğer"

    def _get_package_recommendations(self, customer: Dict[str, Any], available_packages: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Müşteri için paket önerileri oluşturur"""
        recommendations = []
        
        # Mevcut pakete göre öneriler
        current_package_name = customer["current_package"]
        
        for package in available_packages:
            if package["name"] != current_package_name:
                if package["price"] > self._get_package_price(current_package_name) * 1.2:
                    recommendations.append({
                        "package": package,
                        "reason": "Daha yüksek performans için",
                        "priority": "medium"
                    })
                elif package["price"] < self._get_package_price(current_package_name) * 0.8:
                    recommendations.append({
                        "package": package,
                        "reason": "Tasarruf için",
                        "priority": "high"
                    })
        
        return recommendations[:3]

    def _get_package_price(self, package_name: str) -> float:
        """Paket adından fiyat bilgisini alır"""
        for package in self.packages.values():
            if package["name"] == package_name:
                return package["price"]
        return 0.0

    def _validate_package_change(self, customer: Dict[str, Any], new_package: Dict[str, Any]) -> Dict[str, Any]:
        """Paket değişikliği için validasyon yapar"""
        # Gecikmiş ödeme kontrolü
        if customer["payment_status"] == "Gecikmiş":
            return {
                "valid": False,
                "reason": "Gecikmiş ödemeniz nedeniyle paket değişikliği yapılamıyor.",
                "error_code": "OUTSTANDING_PAYMENT"
            }
        
        # Sözleşme bitiş tarihi kontrolü
        contract_end = datetime.strptime(customer["contract_end_date"], "%Y-%m-%d")
        if contract_end > datetime.now() + timedelta(days=30):
            return {
                "valid": False,
                "reason": "Sözleşmeniz henüz bitmemiş. Paket değişikliği için 30 gün beklemelisiniz.",
                "error_code": "CONTRACT_NOT_EXPIRED"
            }
        
        # Kredi limiti kontrolü
        if new_package["price"] > customer["credit_limit"]:
            return {
                "valid": False,
                "reason": "Kredi limitiniz yeni paket için yeterli değil.",
                "error_code": "INSUFFICIENT_CREDIT"
            }
        
        return {"valid": True, "reason": "", "error_code": ""}

    def _determine_priority(self, issue_type: str) -> str:
        """Sorun tipine göre öncelik belirler"""
        high_priority = ["internet_outage", "no_service", "billing_error"]
        medium_priority = ["slow_internet", "package_change", "technical_issue"]
        
        if issue_type in high_priority:
            return "Yüksek"
        elif issue_type in medium_priority:
            return "Orta"
        else:
            return "Düşük"

# Global API instance
mock_apis = MockTelecomAPIs()

# Kolay erişim fonksiyonları
def getUserInfo(user_id: str) -> Dict[str, Any]:
    return mock_apis.getUserInfo(user_id)

def getAvailablePackages(user_id: str) -> Dict[str, Any]:
    return mock_apis.getAvailablePackages(user_id)

def initiatePackageChange(user_id: str, package_id: str) -> Dict[str, Any]:
    return mock_apis.initiatePackageChange(user_id, package_id)

def getBillingInfo(user_id: str, period: str = "current") -> Dict[str, Any]:
    return mock_apis.getBillingInfo(user_id, period)

def processPayment(user_id: str, amount: float, payment_method: str) -> Dict[str, Any]:
    return mock_apis.processPayment(user_id, amount, payment_method)

def createSupportTicket(user_id: str, issue_type: str, description: str) -> Dict[str, Any]:
    return mock_apis.createSupportTicket(user_id, issue_type, description)

def resetPassword(user_id: str) -> Dict[str, Any]:
    return mock_apis.resetPassword(user_id)