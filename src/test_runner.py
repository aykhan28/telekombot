#!/usr/bin/env python3
"""
Test Runner - 100 Test Senaryosunu Çalıştırır ve Performans Ölçümleri Yapar
"""

import time
import json
import logging
from typing import Dict, List, Any
from datetime import datetime
from test_scenarios import get_all_test_scenarios, get_scenario_statistics
from central_agent import CentralAgent
from chat.ollama_client import ollama_chat
from performance_metrics import PerformanceTracker
from mock_apis import MockTelecomAPIs
import argparse
import sys

# Logging ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestRunner:
    """100 test senaryosunu çalıştırır ve performans ölçümleri yapar"""
    
    def __init__(self):
        self.agent = CentralAgent(ollama_chat_func=ollama_chat)
        self.metrics = PerformanceTracker()
        self.test_results = []
        self.scenarios = get_all_test_scenarios()
        
    def run_single_test(self, scenario) -> Dict[str, Any]:
        """Tek bir test senaryosunu çalıştırır"""
        start_time = time.time()
        
        try:
            # Test başlangıç zamanı
            test_start = datetime.now()
            
            # Her mesaj için ajan yanıtını al
            responses = []
            for message in scenario.messages:
                response_start = time.time()
                response = self.agent.generate_response(message, scenario.user_id)
                response_time = time.time() - response_start
                
                responses.append({
                    "message": message,
                    "response": response,
                    "response_time": response_time
                })
            
            # Test bitiş zamanı
            test_end = datetime.now()
            total_time = time.time() - start_time
            
            # Sonuçları kaydet
            result = {
                "scenario_id": scenario.scenario_id,
                "user_id": scenario.user_id,
                "category": scenario.category,
                "difficulty": scenario.difficulty,
                "expected_intent": scenario.expected_intent,
                "expected_tools": scenario.expected_tools,
                "description": scenario.description,
                "start_time": test_start.isoformat(),
                "end_time": test_end.isoformat(),
                "total_time": total_time,
                "responses": responses,
                "success": True,
                "error": None
            }
            
            # Performans metriklerini güncelle
            self.metrics.record_test_result(result)
            
            return result
            
        except Exception as e:
            error_time = time.time() - start_time
            logger.error(f"Test {scenario.scenario_id} hatası: {e}")
            
            result = {
                "scenario_id": scenario.scenario_id,
                "user_id": scenario.user_id,
                "category": scenario.category,
                "difficulty": scenario.difficulty,
                "expected_intent": scenario.expected_intent,
                "expected_tools": scenario.expected_tools,
                "description": scenario.description,
                "start_time": datetime.now().isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_time": error_time,
                "responses": [],
                "success": False,
                "error": str(e)
            }
            
            self.metrics.record_test_result(result)
            return result
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Tüm test senaryolarını çalıştırır"""
        logger.info("100 test senaryosu başlatılıyor...")
        
        start_time = time.time()
        total_scenarios = len(self.scenarios)
        
        for i, scenario in enumerate(self.scenarios, 1):
            logger.info(f"Test {i}/{total_scenarios}: {scenario.description}")
            
            result = self.run_single_test(scenario)
            self.test_results.append(result)
            
            # Her 10 testte bir ilerleme raporu
            if i % 10 == 0:
                elapsed = time.time() - start_time
                remaining = (elapsed / i) * (total_scenarios - i)
                logger.info(f"İlerleme: {i}/{total_scenarios} (%{i/total_scenarios*100:.1f}) - Kalan süre: {remaining/60:.1f} dakika")
        
        total_time = time.time() - start_time
        
        # Final raporu oluştur
        final_report = {
            "test_summary": {
                "total_scenarios": total_scenarios,
                "total_time": total_time,
                "average_time_per_test": total_time / total_scenarios,
                "successful_tests": len([r for r in self.test_results if r["success"]]),
                "failed_tests": len([r for r in self.test_results if not r["success"]]),
                "success_rate": len([r for r in self.test_results if r["success"]]) / total_scenarios * 100
            },
            "performance_metrics": self.metrics.get_summary(),
            "detailed_results": self.test_results
        }
        
        return final_report
    
    def run_tests_by_difficulty(self, difficulty: str) -> Dict[str, Any]:
        """Belirli zorluk seviyesindeki testleri çalıştırır"""
        filtered_scenarios = [s for s in self.scenarios if s.difficulty == difficulty]
        logger.info(f"{difficulty} zorluk seviyesinde {len(filtered_scenarios)} test çalıştırılıyor...")
        
        start_time = time.time()
        results = []
        
        for scenario in filtered_scenarios:
            result = self.run_single_test(scenario)
            results.append(result)
        
        total_time = time.time() - start_time
        
        return {
            "difficulty": difficulty,
            "total_scenarios": len(filtered_scenarios),
            "total_time": total_time,
            "successful_tests": len([r for r in results if r["success"]]),
            "failed_tests": len([r for r in results if not r["success"]]),
            "results": results
        }
    
    def run_tests_by_category(self, category: str) -> Dict[str, Any]:
        """Belirli kategorideki testleri çalıştırır"""
        filtered_scenarios = [s for s in self.scenarios if s.category == category]
        logger.info(f"{category} kategorisinde {len(filtered_scenarios)} test çalıştırılıyor...")
        
        start_time = time.time()
        results = []
        
        for scenario in filtered_scenarios:
            result = self.run_single_test(scenario)
            results.append(result)
        
        total_time = time.time() - start_time
        
        return {
            "category": category,
            "total_scenarios": len(filtered_scenarios),
            "total_time": total_time,
            "successful_tests": len([r for r in results if r["success"]]),
            "failed_tests": len([r for r in results if not r["success"]]),
            "results": results
        }
    
    def save_results(self, filename: str = None):
        """Test sonuçlarını JSON dosyasına kaydeder"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"test_results_{timestamp}.json"
        
        report = {
            "test_summary": {
                "total_scenarios": len(self.scenarios),
                "successful_tests": len([r for r in self.test_results if r["success"]]),
                "failed_tests": len([r for r in self.test_results if not r["success"]]),
                "success_rate": len([r for r in self.test_results if r["success"]]) / len(self.scenarios) * 100
            },
            "performance_metrics": self.metrics.get_summary(),
            "detailed_results": self.test_results,
            "scenario_statistics": get_scenario_statistics()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Test sonuçları {filename} dosyasına kaydedildi.")
        return filename
    
    def print_summary(self):
        """Test özetini konsola yazdırır"""
        total = len(self.test_results)
        successful = len([r for r in self.test_results if r["success"]])
        failed = total - successful
        
        print("\n" + "="*60)
        print("TEST SONUÇLARI ÖZETİ")
        print("="*60)
        print(f"Toplam Test: {total}")
        print(f"Başarılı: {successful}")
        print(f"Başarısız: {failed}")
        print(f"Başarı Oranı: {successful/total*100:.1f}%")
        
        # Zorluk seviyesine göre dağılım
        difficulties = {}
        for result in self.test_results:
            diff = result["difficulty"]
            if diff not in difficulties:
                difficulties[diff] = {"total": 0, "success": 0}
            difficulties[diff]["total"] += 1
            if result["success"]:
                difficulties[diff]["success"] += 1
        
        print("\nZorluk Seviyesine Göre:")
        for diff, stats in difficulties.items():
            success_rate = stats["success"] / stats["total"] * 100
            print(f"  {diff.capitalize()}: {stats['success']}/{stats['total']} (%{success_rate:.1f})")
        
        # Kategoriye göre dağılım
        categories = {}
        for result in self.test_results:
            cat = result["category"]
            if cat not in categories:
                categories[cat] = {"total": 0, "success": 0}
            categories[cat]["total"] += 1
            if result["success"]:
                categories[cat]["success"] += 1
        
        print("\nKategoriye Göre:")
        for cat, stats in categories.items():
            success_rate = stats["success"] / stats["total"] * 100
            print(f"  {cat}: {stats['success']}/{stats['total']} (%{success_rate:.1f})")
        
        # Performans metrikleri
        metrics = self.metrics.get_summary()
        print(f"\nOrtalama Yanıt Süresi: {metrics['average_response_time']:.2f} saniye")
        print(f"En Hızlı Yanıt: {metrics['fastest_response']:.2f} saniye")
        print(f"En Yavaş Yanıt: {metrics['slowest_response']:.2f} saniye")
        
        print("="*60)

def main():
    """Ana test fonksiyonu"""
    print("🤖 Telekom Çağrı Merkezi AI Test Runner")
    print("100 test senaryosu çalıştırılıyor...")
    
    runner = TestRunner()
    
    # Tüm testleri çalıştır
    report = runner.run_all_tests()
    
    # Özeti yazdır
    runner.print_summary()
    
    # Sonuçları kaydet
    filename = runner.save_results()
    print(f"\nDetaylı sonuçlar {filename} dosyasına kaydedildi.")
    
    # Başarısız senaryoları özetle
    failed = [r for r in runner.test_results if not r.get("success", True)]
    if failed:
        print("\n--- Başarısız Senaryolar Özeti ---")
        for fail in failed:
            print(f"Senaryo: {fail.get('scenario_name', 'Bilinmiyor')}")
            print(f"Hata: {fail.get('error', 'Bilinmiyor')}")
            print("---")
        # Ayrıca dosyaya da yaz
        with open("failed_scenarios_summary.txt", "w", encoding="utf-8") as fsum:
            for fail in failed:
                fsum.write(f"Senaryo: {fail.get('scenario_name', 'Bilinmiyor')}\n")
                fsum.write(f"Hata: {fail.get('error', 'Bilinmiyor')}\n---\n")
    else:
        print("Tüm senaryolar başarıyla geçti!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TelekomBot Test Runner")
    parser.add_argument('--output', type=str, default=None, help='Sonuçları kaydetmek için dosya adı')
    parser.add_argument('--summary', action='store_true', help='Sadece özet çıktı')
    args = parser.parse_args()

    report = runner.run_all_tests()
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            import json
            json.dump(report, f, ensure_ascii=False, indent=2)
    if args.summary:
        total = report['test_summary']['total_scenarios']
        passed = report['test_summary']['successful_tests']
        failed = report['test_summary']['failed_tests']
        print(f"Toplam: {total}, Başarılı: {passed}, Başarısız: {failed}")
        if failed > 0:
            print("Başarısız senaryolar:")
            for fail in report['detailed_results']:
                if not fail.get('success', True):
                    print(f"- {fail.get('scenario_name', 'Bilinmiyor')}: {fail.get('error', 'Bilinmiyor')}")
    # CI/CD için çıkış kodu
    sys.exit(0 if report['test_summary']['failed_tests'] == 0 else 1) 