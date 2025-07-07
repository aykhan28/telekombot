"""
Sanal Telekom Çağrı Merkezi Uygulaması
- Streamlit tabanlı modern arayüz
- MongoDB ile sohbet geçmişi
- CentralAgent ile LLM tabanlı akıllı müşteri temsilcisi
- Mock API araçları ile uçtan uca test edilebilirlik
"""
import streamlit as st
from pymongo import MongoClient
import uuid
from chat.context import ChatContext
from chat.prompt import build_prompt
from chat.ollama_client import ollama_chat
from central_agent import CentralAgent, BillingService, AuthService
from mock_apis import MockTelecomAPIs
import tempfile
import asyncio
import edge_tts
import base64

services = {
    "billing": BillingService(),
    "auth": AuthService()
}
agent = CentralAgent(ollama_chat_func=ollama_chat, external_services=services)

st.set_page_config(page_title="Sanal Telekom Çağrı Merkezi", page_icon="📞", layout="wide")

st.markdown("""
    <style>
    body { background-color: #f5f7fa; }
    .main { background-color: #f5f7fa; }
    .block-container { padding-top: 2rem; }
    .stButton > button {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(106,17,203,0.08);
        transition: 0.2s;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%);
        color: #fff;
        box-shadow: 0 4px 16px rgba(37,117,252,0.12);
    }
    .sohbet-bubble-user {
        background: #e3f2fd;
        border-radius: 16px 16px 6px 16px;
        padding: 16px 22px;
        margin: 12px 0;
        box-shadow: 0 2px 12px rgba(33,150,243,0.10);
        text-align: left;
        font-size: 1.12rem;
        max-width: 70%;
        margin-left: auto;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .sohbet-bubble-bot {
        background: #f3e5f5;
        border-radius: 16px 16px 16px 6px;
        padding: 16px 22px;
        margin: 12px 0;
        box-shadow: 0 2px 12px rgba(156,39,176,0.10);
        text-align: left;
        font-size: 1.12rem;
        max-width: 70%;
        margin-right: auto;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .sohbet-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #6a11cb;
        margin-bottom: 0.5rem;
    }
    .sohbet-input-bottom {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100vw;
        background: #f5f7fa;
        z-index: 100;
        padding: 1.2rem 0.5rem 1.2rem 18vw;
        box-shadow: 0 -2px 12px rgba(106,17,203,0.04);
    }
    .stTextInput > div > input {
        border-radius: 8px;
        border: 1.5px solid #6a11cb;
        padding: 0.5rem 1rem;
        font-size: 1.1rem;
    }
    .stSelectbox > div {
        border-radius: 8px;
        border: 1.5px solid #2575fc;
    }
    .stSidebar {
        background: #f5f7fa;
    }
    .stSidebar .stHeader {
        color: #2575fc;
    }
    .stSidebar .stButton > button {
        background: linear-gradient(90deg, #2575fc 0%, #6a11cb 100%);
        color: white;
    }
    .stSidebar .stButton > button:hover {
        background: linear-gradient(90deg, #6a11cb 0%, #2575fc 100%);
    }
    .test-senaryo-card {
        background: #fff;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(37,117,252,0.07);
        padding: 0.8rem 1.2rem;
        margin-bottom: 0.7rem;
        display: flex;
        flex-direction: column;
        gap: 0.3rem;
    }
    .senaryo-etiket {
        display: inline-block;
        background: #e3f2fd;
        color: #2575fc;
        border-radius: 8px;
        padding: 0.1rem 0.7rem;
        font-size: 0.95rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .senaryo-etiket-fatura { background: #e3f2fd; color: #1976d2; }
    .senaryo-etiket-paket { background: #ede7f6; color: #6a11cb; }
    .senaryo-etiket-teknik { background: #fce4ec; color: #c2185b; }
    .senaryo-etiket-odeme { background: #e8f5e9; color: #388e3c; }
    .senaryo-etiket-diger { background: #fffde7; color: #fbc02d; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<script>
window.scrollTo(0, document.body.scrollHeight);
</script>
""", unsafe_allow_html=True)

OLLAMA_URL = "http://localhost:11434/api/generate"

# MongoDB bağlantısı
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot"]
messages_col = db["messages"]

def get_user_id():
    if "user_id" not in st.session_state:
        st.session_state.user_id = f"user_{uuid.uuid4()}"
    return st.session_state.user_id

st.markdown("""
<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem;">
    <span style="font-size:2.2rem;">🤖</span>
    <span style="font-size:2.2rem; font-weight:700; color:#2575fc; letter-spacing:1px;">Sanal Telekom Çağrı Merkezi</span>
</div>
""", unsafe_allow_html=True)

user_id = get_user_id()

chat_context = ChatContext("mongodb://localhost:27017/", "callcenter")

# Sohbet geçmişini getir
def get_chat_history(user_id):
    history = []
    for msg in messages_col.find({"user_id": user_id}, {"_id": 0, "role": 1, "message": 1}):
        sender = "You" if msg["role"] == "user" else "Bot"
        history.append((sender, msg["message"]))
    return history

# Test müşteri ID'leri
test_customers = ["05551234567", "05559876543", "05551112233"]

# Sidebar - Test ayarları ve müşteri seçimi
with st.sidebar:
    st.header("🧪 Test Ayarları")
    selected_customer = st.selectbox(
        "Test Müşterisi Seçin:",
        test_customers,
        format_func=lambda x: f"{x} - {MockTelecomAPIs().customers[x]['name']} {MockTelecomAPIs().customers[x]['surname']}"
    )
    if st.button("Müşteri Bilgilerini Göster"):
        from mock_apis import getUserInfo
        customer_info = getUserInfo(selected_customer)
        if customer_info["success"]:
            st.json(customer_info["data"])
        else:
            st.error(customer_info["error"])
    st.divider()
    st.markdown("**Test Senaryoları:**")
    # Senaryoları göster
    senaryo_listesi = [
        ("Fatura sorgulama", "senaryo-etiket senaryo-etiket-fatura", "Faturanızla ilgili bilgi alın"),
        ("Paket değiştirme", "senaryo-etiket senaryo-etiket-paket", "Paketinizi yükseltin veya değiştirin"),
        ("Şifre sıfırlama", "senaryo-etiket senaryo-etiket-diger", "Şifrenizi sıfırlayın"),
        ("Teknik destek", "senaryo-etiket senaryo-etiket-teknik", "Bağlantı ve teknik sorunlar"),
        ("Ödeme işlemi", "senaryo-etiket senaryo-etiket-odeme", "Fatura ödemelerinizi yönetin")
    ]
    for ad, etiket, aciklama in senaryo_listesi:
        st.markdown(f'<div class="test-senaryo-card"><span class="{etiket}">{ad}</span><span style="font-size:0.97rem; color:#666;">{aciklama}</span></div>', unsafe_allow_html=True)

def clear_input():
    st.session_state["sohbet_input"] = ""

# Sohbet geçmişini ekrana yazdır
if "chat_history" not in st.session_state:
    st.session_state.chat_history = get_chat_history(selected_customer)
st.markdown('<div class="sohbet-header">💬 Sohbet Geçmişi</div>', unsafe_allow_html=True)
for i, (sender, msg) in enumerate(st.session_state.chat_history):
    if sender == "You":
        st.markdown(f'<div class="sohbet-bubble-user"><span style="font-size:1.3rem;">👤</span> <span><strong>Siz:</strong> {msg}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="sohbet-bubble-bot"><span style="font-size:1.3rem;">🤖</span> <span><strong>Bot:</strong> {msg}</span></div>', unsafe_allow_html=True)
        # Seslendir butonu ve ses oynatıcı (edge-tts)
        if msg.strip():
            @st.cache_data(show_spinner=False)
            def tts_synthesize_edge(text):
                voice = "tr-TR-AhmetNeural"  # Türkçe erkek ses, dilerse "tr-TR-EmelNeural" da kullanılabilir
                output_path = tempfile.mktemp(suffix=".mp3")
                async def _synth():
                    communicate = edge_tts.Communicate(text, voice)
                    await communicate.save(output_path)
                asyncio.run(_synth())
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                return audio_bytes
            col1, col2 = st.columns([0.15, 0.85])
            with col1:
                if f"tts_play_{i}" not in st.session_state:
                    st.session_state[f"tts_play_{i}"] = False
                if st.button(f"🔊 Dinle", key=f"tts_{i}"):
                    st.session_state[f"tts_play_{i}"] = not st.session_state[f"tts_play_{i}"]
            with col2:
                if st.session_state.get(f"tts_play_{i}"):
                    audio_bytes = tts_synthesize_edge(msg)
                    st.audio(audio_bytes, format="audio/mp3")

st.markdown("<div style='height: 2.5rem;'></div>", unsafe_allow_html=True)

# Sohbet input ve Gönder butonu
with st.container():
    st.markdown('<div class="sohbet-input-bottom">', unsafe_allow_html=True)
    with st.form(key="sohbet_form", clear_on_submit=True):
        user_input = st.text_input(
            "Mesajınızı yazın",
            placeholder="💬 Sorunuzu yazın...",
            key="sohbet_input",
            label_visibility="collapsed"
        )
        send = st.form_submit_button("Gönder")
        if send and user_input:
            messages_col.insert_one({"user_id": selected_customer, "role": "user", "message": user_input})
            with st.spinner("🤖 Ajan düşünüyor..."):
                bot_response = agent.generate_response(user_input, selected_customer)
                messages_col.insert_one({"user_id": selected_customer, "role": "bot", "message": bot_response})
            st.session_state.chat_history = get_chat_history(selected_customer)
            st.rerun()
    col_temizle, col_durum = st.columns([1,1])
    with col_temizle:
        if st.button("🗑️ Sohbeti Temizle"):
            messages_col.delete_many({"user_id": selected_customer})
            st.session_state.chat_history = []
            # Memnuniyet verilerini de temizle
            agent.clear_satisfaction_data(selected_customer)
            st.rerun()
    with col_durum:
        if "sistem_durumu_goster" not in st.session_state:
            st.session_state["sistem_durumu_goster"] = False
        if st.button("📊 Sistem Durumu"):
            st.session_state["sistem_durumu_goster"] = not st.session_state["sistem_durumu_goster"]
        if st.session_state["sistem_durumu_goster"]:
            st.info(f"Seçili Müşteri: {selected_customer}")
            st.info(f"Toplam Mesaj: {len(st.session_state.chat_history)}")
            st.info("Sistem: Aktif")
    
    # Memnuniyet analizi butonu
    col_memnuniyet, _ = st.columns([1,1])
    with col_memnuniyet:
        if "memnuniyet_analizi_goster" not in st.session_state:
            st.session_state["memnuniyet_analizi_goster"] = False
        if st.button("📊 Memnuniyet Analizi"):
            st.session_state["memnuniyet_analizi_goster"] = not st.session_state["memnuniyet_analizi_goster"]
        if st.session_state["memnuniyet_analizi_goster"]:
            # Duygu analizi sonuçları
            sentiment = agent.get_sentiment_result(selected_customer)
            if sentiment:
                st.info(f"📈 Duygu Durumu: {sentiment.get('sentiment', 'N/A')}")
                st.info(f"😊 Duygu: {sentiment.get('emotion', 'N/A')}")
                st.info(f"⭐ Memnuniyet Skoru: {sentiment.get('satisfaction_score', 'N/A')}/10")
                st.info(f"🎯 Güven: %{sentiment.get('confidence', 0) * 100:.1f}")
            else:
                st.info("Henüz duygu analizi yapılmamış")
            
            # Memnuniyet puanları
            rating = agent.get_satisfaction_rating(selected_customer)
            if rating:
                st.success(f"🎯 Verilen Puan: {rating}/10")
                if rating >= 8:
                    st.success("Müşteri çok memnun! 🎉")
                elif rating >= 6:
                    st.warning("Müşteri orta düzeyde memnun")
                else:
                    st.error("Müşteri memnun değil, iyileştirme gerekli")
            else:
                st.info("Henüz memnuniyet puanı verilmemiş")
    st.markdown('</div>', unsafe_allow_html=True)

