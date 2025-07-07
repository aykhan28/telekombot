import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio
import time
from tools import (
    get_customer_info,
    get_billing_info,
    get_packages,
    change_package,
    reset_password,
    create_ticket,
    process_payment,
    get_contract_info,
    activate_service,
    search_knowledge_base
)
import re
import random

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentType(Enum):
    BILLING_INQUIRY = "fatura_sorgula"
    PACKAGE_CHANGE = "paket_degistir"
    PASSWORD_RESET = "sifre_sifirla"
    TECHNICAL_SUPPORT = "teknik_destek"
    COMPLAINT = "sikayet"
    GENERAL_QUESTION = "genel_soru"
    CUSTOMER_INFO = "musteri_bilgi"
    PAYMENT = "odeme"
    CONTRACT_RENEWAL = "sozlesme_yenile"
    SERVICE_ACTIVATION = "hizmet_aktifleştir"
    CONTRACT_INFO = "sozlesme_bilgi_al"

class ToolType(Enum):
    GET_CUSTOMER_INFO = "musteri_bilgi_al"
    GET_BILLING_INFO = "fatura_bilgi_al"
    GET_PACKAGES = "paket_listesi_al"
    CHANGE_PACKAGE = "paket_degistir"
    RESET_PASSWORD = "sifre_sifirla"
    CREATE_TICKET = "ticket_olustur"
    PROCESS_PAYMENT = "odeme_islem"
    GET_CONTRACT_INFO = "sozlesme_bilgi_al"
    ACTIVATE_SERVICE = "hizmet_aktifleştir"
    SEARCH_KNOWLEDGE_BASE = "bilgi_tabanı_ara"

@dataclass
class Tool:
    name: str
    description: str
    parameters: Dict[str, Any]
    function: callable

@dataclass
class ConversationState:
    user_id: str
    current_intent: Optional[IntentType] = None
    context: Dict[str, Any] = None
    pending_actions: List[str] = None
    conversation_history: List[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.context is None:
            self.context = {}
        if self.pending_actions is None:
            self.pending_actions = []
        if self.conversation_history is None:
            self.conversation_history = []

class CentralAgent:
    def __init__(self, ollama_chat_func, external_services=None):
        self.ollama_chat = ollama_chat_func
        self.external_services = external_services or {}
        self.conversation_states: Dict[str, ConversationState] = {}
        self.tools = self._initialize_tools()
        # Memnuniyet verilerini agent içinde sakla
        self.satisfaction_ratings = {}
        self.sentiment_results = {}
        self.satisfaction_survey_shown = {}
        
    def _initialize_tools(self) -> Dict[str, Tool]:
        """Kullanılabilir araçları tanımlar"""
        return {
            ToolType.GET_CUSTOMER_INFO.value: Tool(
                name="Müşteri Bilgilerini Al",
                description="Müşterinin hesap bilgilerini, paket durumunu ve fatura geçmişini getirir",
                parameters={"user_id": "string"},
                function=get_customer_info
            ),
            ToolType.GET_BILLING_INFO.value: Tool(
                name="Fatura Bilgilerini Al",
                description="Müşterinin güncel ve geçmiş faturalarını getirir",
                parameters={"user_id": "string", "period": "string"},
                function=get_billing_info
            ),
            ToolType.GET_PACKAGES.value: Tool(
                name="Paket Listesini Al",
                description="Müşterinin mevcut paketini ve değiştirebileceği paketleri listeler",
                parameters={"user_id": "string"},
                function=get_packages
            ),
            ToolType.CHANGE_PACKAGE.value: Tool(
                name="Paket Değiştir",
                description="Müşterinin paketini değiştirir",
                parameters={"user_id": "string", "new_package_id": "string"},
                function=change_package
            ),
            ToolType.RESET_PASSWORD.value: Tool(
                name="Şifre Sıfırla",
                description="Müşterinin şifresini sıfırlar ve e-posta gönderir",
                parameters={"user_id": "string"},
                function=reset_password
            ),
            ToolType.CREATE_TICKET.value: Tool(
                name="Destek Talebi Oluştur",
                description="Teknik destek talebi oluşturur",
                parameters={"user_id": "string", "issue_type": "string", "description": "string"},
                function=create_ticket
            ),
            ToolType.PROCESS_PAYMENT.value: Tool(
                name="Ödeme İşlemi",
                description="Fatura ödemesi işlemi yapar",
                parameters={"user_id": "string", "amount": "float", "payment_method": "string"},
                function=process_payment
            ),
            ToolType.GET_CONTRACT_INFO.value: Tool(
                name="Sözleşme Bilgilerini Al",
                description="Müşterinin sözleşme detaylarını getirir",
                parameters={"user_id": "string"},
                function=get_contract_info
            ),
            ToolType.ACTIVATE_SERVICE.value: Tool(
                name="Hizmet Aktifleştir",
                description="Yeni hizmet aktifleştirir",
                parameters={"user_id": "string", "service_type": "string"},
                function=activate_service
            ),
            ToolType.SEARCH_KNOWLEDGE_BASE.value: Tool(
                name="Bilgi Tabanında Ara",
                description="Genel sorular için bilgi tabanında arama yapar",
                parameters={"query": "string"},
                function=search_knowledge_base
            )
        }

    def _get_conversation_state(self, user_id: str) -> ConversationState:
        """Kullanıcının konuşma durumunu alır veya oluşturur"""
        if user_id not in self.conversation_states:
            self.conversation_states[user_id] = ConversationState(user_id=user_id)
        return self.conversation_states[user_id]

    def _analyze_intent_with_llm(self, user_message: str, conversation_history: List[Dict[str, str]]) -> Dict[str, Any]:
        logger.info(f"Niyet analizi başlatıldı. Kullanıcı mesajı: {user_message}")
        context = "\n".join([f"{msg['role']}: {msg['message']}" for msg in conversation_history[-5:]])
        
        analysis_prompt = f"""
        Aşağıdaki konuşma geçmişini ve kullanıcının son mesajını analiz et:
        
        Konuşma Geçmişi:
        {context}
        
        Kullanıcının Son Mesajı: {user_message}
        
        Bu mesajın niyetini belirle ve hangi araçların kullanılması gerektiğini öner.
        
        Kullanabileceğin araçlar ve isimleri:
        - musteri_bilgi_al
        - fatura_bilgi_al
        - paket_listesi_al
        - paket_degistir
        - sifre_sifirla
        - ticket_olustur
        - odeme_islem
        - sozlesme_bilgi_al
        - hizmet_aktifleştir
        - bilgi_tabanı_ara
        
        Yanıtını JSON formatında ver:
        {{
            "intent": "niyet_tipi",
            "confidence": 0.95,
            "required_tools": ["araç1", "araç2"],
            "parameters": {{"param1": "değer1"}},
            "context_update": {{"key": "value"}},
            "response_type": "immediate|multi_step|clarification"
        }}
        
        Niyet tipleri: fatura_sorgula, paket_degistir, sifre_sifirla, teknik_destek, sikayet, genel_soru, musteri_bilgi, odeme, sozlesme_yenile, hizmet_aktifleştir
        """
        
        try:
            response = self.ollama_chat(analysis_prompt)
            logger.info(f"LLM yanıtı: {response}")
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"LLM analiz hatası: {e}")
        
        # Fallback analiz
        return self._fallback_intent_analysis(user_message)

    def _fallback_intent_analysis(self, user_message: str) -> Dict[str, Any]:
        """Basit anahtar kelime tabanlı analiz (fallback)"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["fatura", "ödeme", "borç", "para"]):
            return {
                "intent": "fatura_sorgula",
                "confidence": 0.8,
                "required_tools": ["musteri_bilgi_al", "fatura_bilgi_al"],
                "parameters": {},
                "context_update": {},
                "response_type": "multi_step"
            }
        elif any(word in message_lower for word in ["paket", "tarife", "değiştir", "yükselt", "düşür"]):
            return {
                "intent": "paket_degistir",
                "confidence": 0.85,
                "required_tools": ["musteri_bilgi_al", "paket_listesi_al"],
                "parameters": {},
                "context_update": {},
                "response_type": "multi_step"
            }
        elif any(word in message_lower for word in ["şifre", "parola", "giriş", "unut"]):
            return {
                "intent": "sifre_sifirla",
                "confidence": 0.9,
                "required_tools": ["sifre_sifirla"],
                "parameters": {},
                "context_update": {},
                "response_type": "immediate"
            }
        else:
            return {
                "intent": "genel_soru",
                "confidence": 0.6,
                "required_tools": ["bilgi_tabanı_ara"],
                "parameters": {"query": user_message},
                "context_update": {},
                "response_type": "immediate"
            }

    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any], user_id: str) -> Dict[str, Any]:
        logger.info(f"Araç çağrılıyor: {tool_name}, Parametreler: {parameters}")
        if tool_name not in self.tools:
            return {"success": False, "error": f"İlgili işlem için gerekli araç sistemde tanımlı değil. Lütfen tekrar deneyin veya destek ekibiyle iletişime geçin.", "tool_used": tool_name}
        try:
            tool = self.tools[tool_name]
            if "user_id" not in parameters:
                parameters["user_id"] = user_id
            # Parametre validasyonu
            for param, typ in tool.parameters.items():
                if param not in parameters or parameters[param] in [None, ""]:
                    return {"success": False, "error": f"Gerekli parametre eksik: '{param}'. Lütfen doğru ve eksiksiz bilgi giriniz. Örnek: {param}={typ}", "tool_used": tool_name}
                # Tip kontrolü (sadece temel tipler için)
                if typ == "float":
                    try:
                        float(parameters[param])
                    except Exception:
                        return {"success": False, "error": f"Parametre tipi hatalı: '{param}' sayısal olmalı. Örnek: {param}=100.0", "tool_used": tool_name}
                if typ == "string":
                    if not isinstance(parameters[param], str):
                        return {"success": False, "error": f"Parametre tipi hatalı: '{param}' metin olmalı. Örnek: {param}='değer'", "tool_used": tool_name}
            # Fazla parametreleri çıkar
            filtered_params = {k: v for k, v in parameters.items() if k in tool.parameters}
            result = tool.function(**filtered_params)
            logger.info(f"Araç sonucu: {tool_name}, Sonuç: {result}")
            return {"success": True, "result": result, "tool_used": tool_name}
        except Exception as e:
            logger.error(f"Araç çalıştırma hatası {tool_name}: {e}")
            user_friendly_error = (
                "Üzgünüz, işleminiz sırasında bir hata oluştu. Lütfen bilgilerinizi kontrol ederek tekrar deneyin. "
                "Sorun devam ederse, farklı bir işlem deneyebilir veya destek ekibimizle iletişime geçebilirsiniz."
            )
            return {"success": False, "error": user_friendly_error, "tool_used": tool_name}

    def _generate_response_with_context(self, user_message: str, tool_results: List[Dict[str, Any]], 
                                    conversation_state: ConversationState, clarification: str = None) -> str:
        logger.info(f"Yanıt oluşturuluyor. Kullanıcı mesajı: {user_message}, Araç sonuçları: {tool_results}")
        # Şifre sıfırlama varsa sadece onun çıktısını kullan
        sifre_sonucu = None
        for result in tool_results:
            if result.get("success") and result.get("tool_used") == "sifre_sifirla":
                sifre_sonucu = result["result"]
                break
        if sifre_sonucu:
            # Sadece şifre sıfırlama mesajı dön
            return sifre_sonucu + "\n\nBaşka bir isteğiniz var mı?"
        else:
            # Diğer öncelik sırasına göre devam et
            oncelik = ["odeme_islem", "paket_degistir", "fatura_bilgi_al", "musteri_bilgi_al"]
            secili_sonuc = None
            secili_tool = None
            for tool in oncelik:
                for result in tool_results:
                    if result.get("success") and result.get("tool_used") == tool:
                        secili_sonuc = result["result"]
                        secili_tool = tool
                        break
                if secili_sonuc:
                    break
            if secili_sonuc:
                teknik_sonuc = secili_sonuc
                tool_names = [secili_tool]
            else:
                teknik_sonuclar = []
                tool_names = []
                for result in tool_results:
                    if result.get("success") and result.get("result"):
                        teknik_sonuclar.append(result["result"])
                        tool_names.append(result["tool_used"])
                teknik_sonuc = "\n".join(teknik_sonuclar)
        if teknik_sonuc:
            # Daha sade ve profesyonel Türkçe için promptu güncelliyorum
            prompt = (
                "Sen profesyonel bir telekom müşteri temsilcisisin. Cevabın sadece Türkçe ve kısa, net olmalı. "
                "Kullanıcıya teknik detayları değil, anlaşılır ve özet bilgi ver. "
                "Fatura, bakiye, paket gibi bilgileri gereksiz tekrar ve detay olmadan açıkla. "
                "Örneğin: 'Faturanızı ödemişsiniz, şu an borcunuz bulunmuyor.' veya 'Bu ayki faturanız 250 TL ve ödenmiş.' gibi. "
                "'Her şey yolunda', 'aktif bir şekilde kullanıyorsunuz' gibi yapay ifadeler kullanma. "
                "Gereksiz ek sorular sorma, sadece bilgi ver ve kibarca kapanış yap. "
                "Yanıtında tırnak, parantez veya İngilizce kelime kullanma. "
                "Resmi ama samimi bir ton kullan. "
                f"Kullanıcıya iletilecek bilgi: {teknik_sonuc}"
            )
            try:
                yanit = self.ollama_chat(prompt)
                otomatik_odeme_oner = False
                if "fatura_bilgi_al" in tool_names and "Ödenmedi" in teknik_sonuc:
                    if teknik_sonuc.count("Ödenmedi") >= 2:
                        otomatik_odeme_oner = True
                if otomatik_odeme_oner:
                    yanit += "\n\nDilerseniz otomatik ödeme talimatı vermek ister misiniz?"
                yanit = yanit.strip().strip('"')
                return yanit + "\n\nBaşka bir isteğiniz var mı?"
            except Exception as e:
                logger.error(f"LLM özetleme hatası: {e}")
                return teknik_sonuc + "\n\nBaşka bir isteğiniz var mı?"
        # Eksik parametre durumu için sade Türkçe örnekli cümle
        if clarification:
            return f"Hangi ayın faturasını öğrenmek istiyorsunuz? Örnek: Temmuz\n\nBaşka bir isteğiniz var mı?"
        # Genel sorular ve insansı diyalog için LLM'e gönder
        context_info = ""
        for result in tool_results:
            if result.get("success"):
                context_info += f"\nAraç Sonucu ({result.get('tool_used', 'bilinmeyen')}): {result.get('result', '')}"
            else:
                context_info += f"\nHata ({result.get('tool_used', 'bilinmeyen')}): {result.get('error', '')}"
        conversation_history = "\n".join([
            f"{msg['role']}: {msg['message']}"
            for msg in conversation_state.conversation_history[-3:]
        ])
        response_prompt = f"Sen profesyonel bir telekom operatörü müşteri temsilcisisin. Tüm cevaplarını sadece Türkçe ver. İngilizce veya başka bir dil kullanma! Aşağıdaki bilgileri kullanarak kullanıcıya yanıt ver: Kullanıcının Mesajı: {user_message} Son Konuşma Geçmişi: {conversation_history} Sistem Bilgileri: {context_info} Kullanıcının Mevcut Durumu: {conversation_state.context} Lütfen: 1. Tüm yanıtlarını Türkçe ver 2. Profesyonel ve samimi ol 3. Hata durumlarını kibar bir şekilde açıkla 4. Gerekirse ek bilgi iste 5. Çözüm önerileri sun 6. Resmi ama anlaşılır bir dil kullan Unutma: Tüm cevaplarını sadece Türkçe ver. İngilizce veya başka bir dil kullanma! Yanıtın:"
        try:
            response = self.ollama_chat(response_prompt)
            logger.info(f"Oluşturulan yanıt: {response}")
            return response.strip() + "\n\nBaşka bir isteğiniz var mı?"
        except Exception as e:
            logger.error(f"Yanıt oluşturma hatası: {e}")
            return "Üzgünüm, şu anda size yardımcı olamıyorum. Lütfen daha sonra tekrar deneyin."

    def _analyze_sentiment(self, user_message: str) -> Dict[str, Any]:
        """Kullanıcı mesajından duygu analizi yapar"""
        sentiment_prompt = f"""
        Aşağıdaki kullanıcı mesajının duygu durumunu analiz et:
        
        Mesaj: {user_message}
        
        Yanıtını JSON formatında ver:
        {{
            "sentiment": "positive|negative|neutral",
            "confidence": 0.95,
            "emotion": "satisfied|frustrated|happy|angry|neutral|confused",
            "satisfaction_score": 8.5
        }}
        
        satisfaction_score: 1-10 arası, 10 en memnun
        """
        
        try:
            response = self.ollama_chat(sentiment_prompt)
            if "{" in response and "}" in response:
                start = response.find("{")
                end = response.rfind("}") + 1
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception as e:
            logger.error(f"Duygu analizi hatası: {e}")
        
        # Fallback analiz
        message_lower = user_message.lower()
        positive_words = ["teşekkür", "güzel", "iyi", "memnun", "harika", "süper", "çok iyi"]
        negative_words = ["kötü", "berbat", "memnun değil", "sorun", "problem", "kızgın", "sinirli"]
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return {"sentiment": "positive", "confidence": 0.7, "emotion": "satisfied", "satisfaction_score": 8.0}
        elif negative_count > positive_count:
            return {"sentiment": "negative", "confidence": 0.7, "emotion": "frustrated", "satisfaction_score": 3.0}
        else:
            return {"sentiment": "neutral", "confidence": 0.6, "emotion": "neutral", "satisfaction_score": 5.0}

    def _process_satisfaction_rating(self, user_message: str, user_id: str) -> str:
        """Memnuniyet puanını işler"""
        try:
            # Sayısal puanı çıkar
            import re
            numbers = re.findall(r'\b(?:10|[1-9])\b', user_message)
            if numbers:
                rating = int(numbers[0])
                if 1 <= rating <= 10:
                    # Puanı kaydet
                    self.satisfaction_ratings[user_id] = rating
                    
                    if rating >= 8:
                        return "Çok teşekkür ederiz! Memnuniyetiniz bizi mutlu ediyor. Size en iyi hizmeti sunmaya devam edeceğiz. İyi günler dileriz."
                    elif rating >= 6:
                        return "Teşekkür ederiz! Görüşleriniz bizim için değerli. Daha iyi hizmet vermek için sürekli çalışıyoruz. İyi günler dileriz."
                    else:
                        return "Görüşleriniz için teşekkür ederiz. Daha iyi hizmet vermek için çalışacağız. İyi günler dileriz."
            
            return "Lütfen 1-10 arası bir sayı yazın."
        except Exception as e:
            logger.error(f"Memnuniyet puanı işleme hatası: {e}")
            return "Puanınızı işlerken bir hata oluştu. İyi günler dileriz."

    def get_satisfaction_rating(self, user_id: str) -> Optional[int]:
        """Kullanıcının memnuniyet puanını döndürür"""
        return self.satisfaction_ratings.get(user_id)
    
    def get_sentiment_result(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Kullanıcının duygu analizi sonucunu döndürür"""
        return self.sentiment_results.get(user_id)
    
    def clear_satisfaction_data(self, user_id: str):
        """Kullanıcının memnuniyet verilerini temizler"""
        self.satisfaction_ratings.pop(user_id, None)
        self.sentiment_results.pop(user_id, None)
        self.satisfaction_survey_shown.pop(user_id, None)

    def generate_response(self, user_message: str, user_id: str) -> str:
        logger.info(f"Yanıt üretme süreci başladı. Kullanıcı: {user_id}, Mesaj: {user_message}")
        try:
            # Her mesajda duygu analizi yap ve kaydet
            sentiment_result = self._analyze_sentiment(user_message)
            self.sentiment_results[user_id] = sentiment_result
            
            # Memnuniyet puanı kontrolü
            import re
            if re.match(r'^\s*(?:10|[1-9])\s*$', user_message.strip()):
                yanit = self._process_satisfaction_rating(user_message, user_id)
                # Puan girildiğinde de sentiment_results güncellensin
                self.sentiment_results[user_id] = {"sentiment": "manual_rating", "satisfaction_score": int(user_message.strip()), "emotion": "-", "confidence": 1.0}
                return yanit
            
            # Duygu analizi yap
            sentiment_result = self._analyze_sentiment(user_message)
            self.sentiment_results[user_id] = sentiment_result
            
            # Kapanış ve teşekkür mesajı kontrolü
            user_message_lower = user_message.lower()
            tesekkur_list = [
                "Rica ederim, size yardımcı olmaktan memnuniyet duydum.",
                "Ne demek, her zaman hizmetinizdeyiz.",
                "Yardımcı olabildiysem ne mutlu bana. Başka bir konuda destek gerekirse çekinmeden yazabilirsiniz.",
                "Teşekkür ederim, size en iyi hizmeti sunmaya devam edeceğiz."
            ]
            kapanis_list = [
                "Size yardımcı olmaktan memnuniyet duydum. İyi günler dilerim.",
                "Görüşmek üzere, sağlıklı günler dilerim.",
                "Size hizmet vermekten mutluluk duydum. Hoşça kalın.",
                "İyi günler, tekrar görüşmek dileğiyle."
            ]
            # Kapanış ve teşekkür mesajı kontrolü
            user_message_lower = user_message.lower()
            kapanis_ifadeleri = [
                "başka bir isteğim yok", "başka bir sorum yok", "yok teşekkürler", "hepsi bu", "bu kadar",
                "hoşcakal", "hoşça kal", "görüşürüz", "bye", "güle güle", "elveda", "selametle", "kendine iyi bak",
                "hayır teşekkürler", "hayır sağol", "hayır sağ olun"
            ]
            if any(x in user_message_lower for x in kapanis_ifadeleri):
                # Memnuniyet anketi göster
                if user_id not in self.satisfaction_survey_shown:
                    self.satisfaction_survey_shown[user_id] = False
                if not self.satisfaction_survey_shown[user_id]:
                    self.satisfaction_survey_shown[user_id] = True
                    return "Birkaç dakika ayırıp hizmetimizi 10 puan üzerinden değerlendirir misiniz? (1-10 arası bir sayı yazın)"
                # Eğer anket zaten gösterildiyse ve kullanıcı tekrar kapanış yazdıysa, teşekkür veya kapanış mesajı gönder
                return random.choice(kapanis_list)
            # Teşekkür mesajı kontrolü (kapanıştan sonra gelmemesi için sona aldık)
            if any(x in user_message_lower for x in ["teşekkür", "sağ ol", "eyvallah"]):
                # Eğer kapanış cümlesi de içeriyorsa, sadece anket sorulsun, teşekkür mesajı gönderilmesin
                if any(x in user_message_lower for x in kapanis_ifadeleri):
                    if user_id not in self.satisfaction_survey_shown or not self.satisfaction_survey_shown[user_id]:
                        self.satisfaction_survey_shown[user_id] = True
                        return "Birkaç dakika ayırıp hizmetimizi 10 puan üzerinden değerlendirir misiniz? (1-10 arası bir sayı yazın)"
                    return random.choice(kapanis_list)
                return random.choice(tesekkur_list)
            # Kapanış/teşekkür mesajı return ile fonksiyonu sonlandırdığı için, aşağıdaki telekom uyarısı asla tetiklenmez.
            conversation_state = self._get_conversation_state(user_id)
            conversation_state.conversation_history.append({
                "role": "user",
                "message": user_message,
                "timestamp": time.time()
            })
            intent_analysis = self._analyze_intent_with_llm(user_message, conversation_state.conversation_history)
            # Enum'a güvenli atama
            intent_str = intent_analysis.get("intent", "genel_soru")
            try:
                conversation_state.current_intent = IntentType(intent_str)
            except ValueError:
                conversation_state.current_intent = IntentType.GENERAL_QUESTION
            conversation_state.context.update(intent_analysis.get("context_update", {}))
            tool_results = []
            required_tools = intent_analysis.get("required_tools", [])
            clarification = None
            if intent_analysis.get("response_type") == "clarification":
                clarification = "Daha fazla bilgiye ihtiyacım var: "
                if intent_analysis.get("parameters"):
                    eksik = ", ".join([k for k, v in intent_analysis["parameters"].items() if not v])
                    if eksik:
                        clarification += f"({eksik})"
            for tool_name in required_tools:
                parameters = intent_analysis.get("parameters", {})
                result = self._execute_tool(tool_name, parameters, user_id)
                tool_results.append(result)
                if not result.get("success") and tool_name in ["musteri_bilgi_al"]:
                    return (
                        "Üzgünüz, müşteri bilgilerinize erişimde bir sorun yaşadık. Lütfen müşteri numaranızı kontrol ederek tekrar deneyin. "
                        "Sorun devam ederse, destek ekibimizle iletişime geçebilirsiniz."
                    )
            # Alakasız soru kontrolü
            if intent_str == "genel_soru" and required_tools == ["bilgi_tabanı_ara"]:
                # Tool sonucu boşsa veya çok alakasızsa (ör. result yok veya result'ta telekom anahtar kelimesi yok)
                if tool_results and (not tool_results[0].get("result") or not any(word in tool_results[0].get("result", "").lower() for word in ["fatura", "paket", "internet", "hat", "ödeme", "sözleşme", "müşteri", "teknik"])):
                    telekom_uyari_list = [
                        "Ben bir telekom asistanıyım, sadece telekomünikasyon işlemleriyle ilgili yardımcı olabilirim. Fatura, paket, internet, ödeme gibi konularda sorularınızı beklerim.",
                        "Size ancak telekom hizmetleriyle ilgili konularda yardımcı olabilirim. Fatura, paket, internet, ödeme veya sözleşme gibi sorularınız varsa memnuniyetle yanıtlarım.",
                        "Yalnızca telekomünikasyon işlemleriyle ilgili destek verebiliyorum. Fatura, paket, internet, ödeme ve sözleşme konularında yardımcı olabilirim.",
                        "Benim uzmanlık alanım telekom hizmetleri. Fatura, paket, internet, ödeme veya sözleşme hakkında sorularınızı yanıtlayabilirim.",
                        "Telekomünikasyon dışında bir konuda yardımcı olamıyorum. Fatura, paket, internet, ödeme ve sözleşme gibi işlemler için buradayım."
                    ]
                    response = random.choice(telekom_uyari_list)
                    conversation_state.conversation_history.append({
                        "role": "bot",
                        "message": response,
                        "timestamp": time.time()
                    })
                    logger.info(f"Yanıt üretildi ve konuşma geçmişine eklendi. Yanıt: {response}")
                    return response
            response = self._generate_response_with_context(user_message, tool_results, conversation_state, clarification)
            conversation_state.conversation_history.append({
                "role": "bot",
                "message": response,
                "timestamp": time.time()
            })
            logger.info(f"Yanıt üretildi ve konuşma geçmişine eklendi. Yanıt: {response}")
            return response
        except Exception as e:
            logger.error(f"Yanıt üretme hatası: {e}")
            return (
                "Sistemde geçici bir sorun oluştu. Lütfen daha sonra tekrar deneyin veya destek ekibimizle iletişime geçin."
            )

# Harici servis örnekleri (gerçek sistem entegrasyonları için)
class BillingService:
    def get_invoice_info(self, user_id: str) -> str:
        logger.info(f"Fatura bilgisi isteniyor. Kullanıcı: {user_id}")
        try:
            from mock_apis import getBillingInfo
            result = getBillingInfo(user_id, "current") # Mock API'ye göre sadece mevcut fatura bilgisi döndür
            if not result.get("success"):
                raise Exception(result.get("error", "Bilinmeyen hata"))
            logger.info(f"Fatura bilgisi başarıyla alındı. Kullanıcı: {user_id}")
            return result["data"]["bills"][0]["amount"] # Mock API'ye göre sadece mevcut fatura tutarını döndür
        except Exception as e:
            logger.error(f"Fatura bilgisi alınamadı. Kullanıcı: {user_id}, Hata: {e}")
            raise Exception(f"Fatura bilgisi alınamadı: {e}")

class AuthService:
    def reset_password(self, user_id: str) -> str:
        logger.info(f"Şifre sıfırlama isteniyor. Kullanıcı: {user_id}")
        try:
            from mock_apis import resetPassword
            result = resetPassword(user_id)
            if not result.get("success"):
                raise Exception(result.get("error", "Bilinmeyen hata"))
            logger.info(f"Şifre sıfırlama başarıyla tamamlandı. Kullanıcı: {user_id}")
            return result["message"]
        except Exception as e:
            logger.error(f"Şifre sıfırlama başarısız. Kullanıcı: {user_id}, Hata: {e}")
            raise Exception(f"Şifre sıfırlama başarısız: {e}")

class CustomerService:
    def get_customer_details(self, user_id: str) -> Dict[str, Any]:
        logger.info(f"Müşteri detayları isteniyor. Kullanıcı: {user_id}")
        try:
            from mock_apis import getUserInfo
            result = getUserInfo(user_id)
            if not result.get("success"):
                raise Exception(result.get("error", "Bilinmeyen hata"))
            logger.info(f"Müşteri detayları başarıyla alındı. Kullanıcı: {user_id}")
            return result["data"]
        except Exception as e:
            logger.error(f"Müşteri detayları alınamadı. Kullanıcı: {user_id}, Hata: {e}")
            raise Exception(f"Müşteri detayları alınamadı: {e}")