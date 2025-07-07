import time
import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import statistics
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import defaultdict, Counter

logger = logging.getLogger(__name__)

class MetricType(Enum):
    SUCCESS_RATE = "başarı_oranı"
    DECISION_ACCURACY = "karar_doğruluğu"
    ERROR_HANDLING = "hata_yönetimi"
    DIALOG_DURATION = "diyalog_süresi"
    TOOL_USAGE = "araç_kullanımı"
    USER_SATISFACTION = "kullanıcı_memnuniyeti"
    RESPONSE_TIME = "yanıt_süresi"
    CONTEXT_RETENTION = "bağlam_koruma"
    INTENT_RECOGNITION = "niyet_tanıma"
    MULTI_STEP_SUCCESS = "çok_adımlı_başarı"

@dataclass
class ConversationMetrics:
    """Tek konuşma için metrikler"""
    conversation_id: str
    user_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    message_count: int = 0
    total_duration: float = 0.0
    success: bool = False
    intent_recognized: bool = False
    tools_used: List[str] = None
    errors_encountered: List[str] = None
    user_satisfaction_score: Optional[float] = None
    context_retention_score: Optional[float] = None
    decision_accuracy_score: Optional[float] = None
    
    def __post_init__(self):
        if self.tools_used is None:
            self.tools_used = []
        if self.errors_encountered is None:
            self.errors_encountered = []

@dataclass
class SystemMetrics:
    """Sistem geneli metrikler"""
    total_conversations: int = 0
    successful_conversations: int = 0
    total_duration: float = 0.0
    average_response_time: float = 0.0
    tool_usage_frequency: Dict[str, int] = None
    error_frequency: Dict[str, int] = None
    intent_recognition_rate: float = 0.0
    user_satisfaction_average: float = 0.0
    context_retention_average: float = 0.0
    decision_accuracy_average: float = 0.0
    
    def __post_init__(self):
        if self.tool_usage_frequency is None:
            self.tool_usage_frequency = defaultdict(int)
        if self.error_frequency is None:
            self.error_frequency = defaultdict(int)

class PerformanceTracker:
    """Performans takip sistemi"""
    
    def __init__(self):
        self.conversations: Dict[str, ConversationMetrics] = {}
        self.system_metrics = SystemMetrics()
        self.start_time = datetime.now()
        self.response_times: List[float] = []
        self.satisfaction_scores: List[float] = []
        
    def start_conversation(self, conversation_id: str, user_id: str) -> str:
        """Yeni konuşma başlatır"""
        self.conversations[conversation_id] = ConversationMetrics(
            conversation_id=conversation_id,
            user_id=user_id,
            start_time=datetime.now()
        )
        return conversation_id
    
    def end_conversation(self, conversation_id: str, success: bool = True):
        """Konuşmayı sonlandırır"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.end_time = datetime.now()
            conv.total_duration = (conv.end_time - conv.start_time).total_seconds()
            conv.success = success
            
            # Sistem metriklerini güncelle
            self.system_metrics.total_conversations += 1
            if success:
                self.system_metrics.successful_conversations += 1
            self.system_metrics.total_duration += conv.total_duration
    
    def record_message(self, conversation_id: str, response_time: float = None):
        """Mesaj kaydı"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.message_count += 1
            if response_time:
                self.response_times.append(response_time)
    
    def record_tool_usage(self, conversation_id: str, tool_name: str):
        """Araç kullanımını kaydeder"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.tools_used.append(tool_name)
            self.system_metrics.tool_usage_frequency[tool_name] += 1
    
    def record_error(self, conversation_id: str, error_type: str, error_message: str):
        """Hata kaydı"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.errors_encountered.append(f"{error_type}: {error_message}")
            self.system_metrics.error_frequency[error_type] += 1
    
    def record_intent_recognition(self, conversation_id: str, recognized: bool):
        """Niyet tanıma kaydı"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.intent_recognized = recognized
            if recognized:
                self.system_metrics.intent_recognition_rate += 1
    
    def record_satisfaction(self, conversation_id: str, score: float):
        """Kullanıcı memnuniyet skoru"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.user_satisfaction_score = score
            self.satisfaction_scores.append(score)
    
    def record_context_retention(self, conversation_id: str, score: float):
        """Bağlam koruma skoru"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.context_retention_score = score
    
    def record_decision_accuracy(self, conversation_id: str, score: float):
        """Karar doğruluğu skoru"""
        if conversation_id in self.conversations:
            conv = self.conversations[conversation_id]
            conv.decision_accuracy_score = score
    
    def calculate_system_metrics(self) -> SystemMetrics:
        """Sistem metriklerini hesaplar"""
        if self.system_metrics.total_conversations > 0:
            self.system_metrics.average_response_time = statistics.mean(self.response_times) if self.response_times else 0.0
            self.system_metrics.intent_recognition_rate /= self.system_metrics.total_conversations
            self.system_metrics.user_satisfaction_average = statistics.mean(self.satisfaction_scores) if self.satisfaction_scores else 0.0
            
            # Bağlam koruma ve karar doğruluğu ortalamaları
            context_scores = [conv.context_retention_score for conv in self.conversations.values() if conv.context_retention_score is not None]
            decision_scores = [conv.decision_accuracy_score for conv in self.conversations.values() if conv.decision_accuracy_score is not None]
            
            self.system_metrics.context_retention_average = statistics.mean(context_scores) if context_scores else 0.0
            self.system_metrics.decision_accuracy_average = statistics.mean(decision_scores) if decision_scores else 0.0
        
        return self.system_metrics
    
    def generate_report(self) -> Dict[str, Any]:
        """Kapsamlı performans raporu oluşturur"""
        system_metrics = self.calculate_system_metrics()
        
        # KPI hesaplamaları
        success_rate = (system_metrics.successful_conversations / system_metrics.total_conversations * 100) if system_metrics.total_conversations > 0 else 0
        avg_duration = system_metrics.total_duration / system_metrics.total_conversations if system_metrics.total_conversations > 0 else 0
        
        # En çok kullanılan araçlar
        top_tools = sorted(system_metrics.tool_usage_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # En çok karşılaşılan hatalar
        top_errors = sorted(system_metrics.error_frequency.items(), key=lambda x: x[1], reverse=True)[:5]
        
        report = {
            "rapor_tarihi": datetime.now().isoformat(),
            "test_süresi": (datetime.now() - self.start_time).total_seconds(),
            "toplam_konuşma": system_metrics.total_conversations,
            "başarılı_konuşma": system_metrics.successful_conversations,
            "kpi_metrikleri": {
                "başarı_oranı": f"{success_rate:.2f}%",
                "ortalama_yanıt_süresi": f"{system_metrics.average_response_time:.2f} saniye",
                "ortalama_konuşma_süresi": f"{avg_duration:.2f} saniye",
                "niyet_tanıma_oranı": f"{system_metrics.intent_recognition_rate * 100:.2f}%",
                "kullanıcı_memnuniyeti": f"{system_metrics.user_satisfaction_average:.2f}/5.0",
                "bağlam_koruma_skoru": f"{system_metrics.context_retention_average:.2f}/5.0",
                "karar_doğruluğu": f"{system_metrics.decision_accuracy_average:.2f}/5.0"
            },
            "araç_kullanım_istatistikleri": {
                "top_5_araç": top_tools,
                "toplam_araç_kullanımı": sum(system_metrics.tool_usage_frequency.values())
            },
            "hata_istatistikleri": {
                "top_5_hata": top_errors,
                "toplam_hata": sum(system_metrics.error_frequency.values())
            },
            "performans_analizi": {
                "hızlı_yanıtlar": len([rt for rt in self.response_times if rt < 2.0]),
                "yavaş_yanıtlar": len([rt for rt in self.response_times if rt > 5.0]),
                "ortalama_yanıt_süresi": statistics.mean(self.response_times) if self.response_times else 0.0
            }
        }
        
        return report
    
    def save_metrics(self, filename: str = None):
        """Metrikleri dosyaya kaydeder"""
        if filename is None:
            filename = f"performance_metrics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = self.generate_report()
        
        # Konuşma detaylarını da ekle
        conversations_data = []
        for conv in self.conversations.values():
            conv_dict = asdict(conv)
            conv_dict['start_time'] = conv_dict['start_time'].isoformat()
            if conv_dict['end_time']:
                conv_dict['end_time'] = conv_dict['end_time'].isoformat()
            conversations_data.append(conv_dict)
        
        report['konuşma_detayları'] = conversations_data
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Metrikler {filename} dosyasına kaydedildi.")
        return filename
    
    def generate_visualizations(self, save_path: str = "performance_charts"):
        """Performans görselleştirmeleri oluşturur"""
        import os
        os.makedirs(save_path, exist_ok=True)
        
        # 1. Başarı Oranı Grafiği
        plt.figure(figsize=(10, 6))
        success_rate = (self.system_metrics.successful_conversations / self.system_metrics.total_conversations * 100) if self.system_metrics.total_conversations > 0 else 0
        plt.pie([success_rate, 100-success_rate], labels=['Başarılı', 'Başarısız'], autopct='%1.1f%%', colors=['lightgreen', 'lightcoral'])
        plt.title('Konuşma Başarı Oranı')
        plt.savefig(f"{save_path}/success_rate.png")
        plt.close()
        
        # 2. Yanıt Süresi Dağılımı
        if self.response_times:
            plt.figure(figsize=(10, 6))
            plt.hist(self.response_times, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            plt.xlabel('Yanıt Süresi (saniye)')
            plt.ylabel('Frekans')
            plt.title('Yanıt Süresi Dağılımı')
            plt.axvline(statistics.mean(self.response_times), color='red', linestyle='--', label=f'Ortalama: {statistics.mean(self.response_times):.2f}s')
            plt.legend()
            plt.savefig(f"{save_path}/response_time_distribution.png")
            plt.close()
        
        # 3. Araç Kullanım Grafiği
        if self.system_metrics.tool_usage_frequency:
            plt.figure(figsize=(12, 6))
            tools = list(self.system_metrics.tool_usage_frequency.keys())
            counts = list(self.system_metrics.tool_usage_frequency.values())
            plt.bar(tools, counts, color='lightblue')
            plt.xlabel('Araçlar')
            plt.ylabel('Kullanım Sayısı')
            plt.title('Araç Kullanım İstatistikleri')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{save_path}/tool_usage.png")
            plt.close()
        
        # 4. Hata Dağılımı
        if self.system_metrics.error_frequency:
            plt.figure(figsize=(10, 6))
            errors = list(self.system_metrics.error_frequency.keys())
            counts = list(self.system_metrics.error_frequency.values())
            plt.bar(errors, counts, color='lightcoral')
            plt.xlabel('Hata Türleri')
            plt.ylabel('Hata Sayısı')
            plt.title('Hata Dağılımı')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(f"{save_path}/error_distribution.png")
            plt.close()
        
        logger.info(f"Görselleştirmeler {save_path} klasörüne kaydedildi.")
    
    def record_test_result(self, test_result: Dict[str, Any]):
        """Test sonucunu kaydeder"""
        # Yanıt sürelerini topla
        if test_result.get("responses"):
            for response in test_result["responses"]:
                if "response_time" in response:
                    self.response_times.append(response["response_time"])
        
        # Test başarısını kaydet
        if test_result.get("success"):
            self.system_metrics.successful_conversations += 1
        self.system_metrics.total_conversations += 1
    
    def get_summary(self) -> Dict[str, Any]:
        """Test özeti döndürür"""
        return {
            "average_response_time": statistics.mean(self.response_times) if self.response_times else 0.0,
            "fastest_response": min(self.response_times) if self.response_times else 0.0,
            "slowest_response": max(self.response_times) if self.response_times else 0.0,
            "total_tests": self.system_metrics.total_conversations,
            "successful_tests": self.system_metrics.successful_conversations,
            "success_rate": (self.system_metrics.successful_conversations / self.system_metrics.total_conversations * 100) if self.system_metrics.total_conversations > 0 else 0.0
        }

# Global performans takipçisi
performance_tracker = PerformanceTracker()