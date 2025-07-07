#!/usr/bin/env python3
"""
Test Dashboard - Test Sonuçlarını Görselleştirir
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from datetime import datetime
from test_runner import TestRunner
from test_scenarios import get_scenario_statistics
import os

st.set_page_config(
    page_title="Telekom AI Test Dashboard",
    page_icon="🤖",
    layout="wide"
)

def load_test_results(filename=None):
    """Test sonuçlarını yükler"""
    if filename and os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def main():
    st.title("🤖 Telekom Çağrı Merkezi AI Test Dashboard")
    st.markdown("---")
    
    # Sidebar - Test seçenekleri
    with st.sidebar:
        st.header("🧪 Test Kontrolleri")
        
        # Test çalıştırma
        if st.button("🚀 100 Test Senaryosunu Çalıştır"):
            with st.spinner("Testler çalıştırılıyor..."):
                runner = TestRunner()
                report = runner.run_all_tests()
                
                # Sonuçları kaydet
                filename = runner.save_results()
                st.success(f"Testler tamamlandı! Sonuçlar {filename} dosyasına kaydedildi.")
                st.session_state.test_results = report
                st.session_state.filename = filename
        
        st.divider()
        
        # Dosya yükleme
        st.header("📁 Sonuç Dosyası Yükle")
        uploaded_file = st.file_uploader("JSON dosyası seçin", type=['json'])
        
        if uploaded_file:
            try:
                data = json.load(uploaded_file)
                st.session_state.test_results = data
                st.success("Dosya başarıyla yüklendi!")
            except Exception as e:
                st.error(f"Dosya yükleme hatası: {e}")
        
        st.divider()
        
        # Senaryo istatistikleri
        st.header("📊 Senaryo İstatistikleri")
        stats = get_scenario_statistics()
        
        st.metric("Toplam Senaryo", stats["toplam_senaryo"])
        
        # Zorluk dağılımı
        st.subheader("Zorluk Dağılımı")
        for diff, count in stats["zorluk_dağılımı"].items():
            st.metric(diff.capitalize(), count)
        
        # Kategori dağılımı
        st.subheader("Kategori Dağılımı")
        for cat, count in stats["kategori_dağılımı"].items():
            st.metric(cat.replace("_", " ").title(), count)
    
    # Ana içerik
    if "test_results" not in st.session_state:
        st.info("👈 Sol panelden test çalıştırın veya sonuç dosyası yükleyin")
        return
    
    results = st.session_state.test_results
    
    # Genel özet
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Toplam Test",
            results["test_summary"]["total_scenarios"]
        )
    
    with col2:
        st.metric(
            "Başarılı",
            results["test_summary"]["successful_tests"],
            delta=f"%{results['test_summary']['success_rate']:.1f}"
        )
    
    with col3:
        st.metric(
            "Başarısız",
            results["test_summary"]["failed_tests"]
        )
    
    with col4:
        avg_time = results['test_summary'].get('average_response_time') or results['test_summary'].get('average_time_per_test')
        st.metric(
            "Ortalama Süre",
            f"{avg_time:.2f}s" if avg_time is not None else "-"
        )
    
    st.markdown("---")
    
    # Grafikler
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Zorluk Seviyesine Göre Başarı Oranı")
        
        # Zorluk seviyesi verilerini hazırla
        difficulty_data = []
        for result in results["detailed_results"]:
            difficulty_data.append({
                "Zorluk": result["difficulty"].capitalize(),
                "Başarılı": result["success"],
                "Başarısız": not result["success"]
            })
        
        df_difficulty = pd.DataFrame(difficulty_data)
        
        if not df_difficulty.empty:
            # Başarı oranlarını hesapla
            success_rates = df_difficulty.groupby("Zorluk").agg({
                "Başarılı": "sum",
                "Başarısız": "sum"
            }).reset_index()
            
            success_rates["Toplam"] = success_rates["Başarılı"] + success_rates["Başarısız"]
            success_rates["Başarı Oranı"] = (success_rates["Başarılı"] / success_rates["Toplam"]) * 100
            
            fig = px.bar(
                success_rates,
                x="Zorluk",
                y="Başarı Oranı",
                title="Zorluk Seviyesine Göre Başarı Oranı (%)",
                color="Başarı Oranı",
                color_continuous_scale="RdYlGn"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Kategoriye Göre Dağılım")
        
        # Kategori verilerini hazırla
        category_data = []
        for result in results["detailed_results"]:
            category_data.append({
                "Kategori": result["category"].replace("_", " ").title(),
                "Başarılı": result["success"],
                "Başarısız": not result["success"]
            })
        
        df_category = pd.DataFrame(category_data)
        
        if not df_category.empty:
            # Kategori başarı oranlarını hesapla
            category_success = df_category.groupby("Kategori").agg({
                "Başarılı": "sum",
                "Başarısız": "sum"
            }).reset_index()
            
            category_success["Toplam"] = category_success["Başarılı"] + category_success["Başarısız"]
            category_success["Başarı Oranı"] = (category_success["Başarılı"] / category_success["Toplam"]) * 100
            
            fig = px.pie(
                category_success,
                values="Toplam",
                names="Kategori",
                title="Kategoriye Göre Test Dağılımı"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Performans metrikleri
    st.markdown("---")
    st.subheader("⚡ Performans Metrikleri")
    
    metrics = results["performance_metrics"]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Ortalama Yanıt Süresi", f"{metrics['average_response_time']:.2f}s")
    
    with col2:
        st.metric("En Hızlı Yanıt", f"{metrics['fastest_response']:.2f}s")
    
    with col3:
        st.metric("En Yavaş Yanıt", f"{metrics['slowest_response']:.2f}s")
    
    # Yanıt süresi dağılımı
    st.subheader("⏱️ Yanıt Süresi Dağılımı")
    
    response_times = []
    for result in results["detailed_results"]:
        if result["success"] and result["responses"]:
            for response in result["responses"]:
                response_times.append(response["response_time"])
    
    if response_times:
        df_times = pd.DataFrame({"Yanıt Süresi (s)": response_times})
        
        fig = px.histogram(
            df_times,
            x="Yanıt Süresi (s)",
            nbins=20,
            title="Yanıt Süresi Dağılımı"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detaylı sonuçlar
    st.markdown("---")
    st.subheader("📋 Detaylı Test Sonuçları")
    
    # Filtreler
    col1, col2, col3 = st.columns(3)
    
    with col1:
        difficulty_filter = st.selectbox(
            "Zorluk Seviyesi",
            ["Tümü"] + list(set([r["difficulty"] for r in results["detailed_results"]]))
        )
    
    with col2:
        category_filter = st.selectbox(
            "Kategori",
            ["Tümü"] + list(set([r["category"] for r in results["detailed_results"]]))
        )
    
    with col3:
        success_filter = st.selectbox(
            "Durum",
            ["Tümü", "Başarılı", "Başarısız"]
        )
    
    # Filtreleme
    filtered_results = results["detailed_results"]
    
    if difficulty_filter != "Tümü":
        filtered_results = [r for r in filtered_results if r["difficulty"] == difficulty_filter]
    
    if category_filter != "Tümü":
        filtered_results = [r for r in filtered_results if r["category"] == category_filter]
    
    if success_filter == "Başarılı":
        filtered_results = [r for r in filtered_results if r["success"]]
    elif success_filter == "Başarısız":
        filtered_results = [r for r in filtered_results if not r["success"]]
    
    # Sonuçları tablo olarak göster
    if filtered_results:
        # Tablo verilerini hazırla
        table_data = []
        for result in filtered_results:
            table_data.append({
                "ID": result["scenario_id"],
                "Kategori": result["category"].replace("_", " ").title(),
                "Zorluk": result["difficulty"].capitalize(),
                "Durum": "✅ Başarılı" if result["success"] else "❌ Başarısız",
                "Süre": f"{result['total_time']:.2f}s",
                "Açıklama": result["description"][:50] + "..." if len(result["description"]) > 50 else result["description"]
            })
        
        df_table = pd.DataFrame(table_data)
        st.dataframe(df_table, use_container_width=True)
    else:
        st.info("Seçilen filtrelere uygun sonuç bulunamadı.")
    
    # Hata analizi
    failed_tests = [r for r in results["detailed_results"] if not r["success"]]
    
    if failed_tests:
        st.markdown("---")
        st.subheader("❌ Başarısız Testler Analizi")
        
        error_data = []
        for result in failed_tests:
            error_data.append({
                "ID": result["scenario_id"],
                "Kategori": result["category"].replace("_", " ").title(),
                "Hata": result["error"][:100] + "..." if len(result["error"]) > 100 else result["error"]
            })
        
        df_errors = pd.DataFrame(error_data)
        st.dataframe(df_errors, use_container_width=True)

if __name__ == "__main__":
    main()