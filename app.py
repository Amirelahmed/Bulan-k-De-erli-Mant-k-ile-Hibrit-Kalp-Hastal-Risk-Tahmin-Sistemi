import streamlit as st
import pandas as pd
import joblib

# ==========================================
# LOAD MODEL
# ==========================================
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")

# ==========================================
# CUSTOM CSS – MODERN PROFESSIONAL DESIGN
# ==========================================
st.markdown(
    """
    <style>
    /* Global background & font */
    body {
        background-color: #f0f2f6;
        font-family: 'Segoe UI', Roboto, Helvetica, sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9eef3 100%);
    }
    /* Main title styling */
    h1 {
        background: linear-gradient(90deg, #c31432, #240b36);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem !important;
        margin-bottom: 0rem;
    }
    /* Custom card for results */
    .result-card {
        background: white;
        border-radius: 24px;
        padding: 1.5rem 2rem;
        box-shadow: 0 20px 35px -10px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        text-align: center;
        transition: all 0.3s ease;
    }
    .risk-high {
        border-left: 8px solid #e74c3c;
        background: linear-gradient(145deg, #fff, #fef2f0);
    }
    .risk-mid {
        border-left: 8px solid #f39c12;
        background: linear-gradient(145deg, #fff, #fff8e7);
    }
    .risk-low {
        border-left: 8px solid #2ecc71;
        background: linear-gradient(145deg, #fff, #ebf9f0);
    }
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background: rgba(255,255,255,0.9);
        backdrop-filter: blur(2px);
        border-radius: 20px;
        padding: 1rem;
    }
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #1f4037, #99f2c8);
        color: black;
        font-weight: bold;
        border: none;
        border-radius: 40px;
        padding: 0.6rem 2rem;
        font-size: 1.2rem;
        transition: 0.2s;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        transform: scale(1.02);
        background: linear-gradient(90deg, #2c5e4a, #b8f2d4);
        color: #000;
    }
    /* Input labels */
    .stSlider label, .stSelectbox label, .stNumberInput label {
        font-weight: 600;
        color: #2c3e50;
    }
    /* status icons */
    .icon-big {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    hr {
        margin: 1rem 0;
        background: linear-gradient(90deg, #ccc, transparent);
        height: 2px;
        border: none;
    }
    /* Metric card */
    .metric-box {
        background: #ffffffcc;
        border-radius: 20px;
        padding: 1rem;
        text-align: center;
        backdrop-filter: blur(5px);
        font-weight: 500;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ==========================================
# APP HEADER
# ==========================================
st.markdown("<h1>❤️ Kalp Hastalığı Risk Tahmini Sistemi</h1>", unsafe_allow_html=True)
st.markdown("#### 🤖 Fuzzy Logic + Machine Learning + Rule‑Based Expert System")
st.markdown("---")

# ==========================================
# SIDEBAR (original inputs – untouched logic)
# ==========================================
with st.sidebar:
    st.markdown("## 📋 Kullanıcı Bilgileri")
    st.markdown("---")
    mode = st.radio("🎯 Tahmin Türü", ["Rule-Based", "ML Model"], index=0)

    age = st.slider("🧓 Yaş", 18, 100, 30)
    gender = st.selectbox("⚧ Cinsiyet", ["Kadın", "Erkek"])

    smoke = st.selectbox("🚬 Sigara", ["Hayır", "Evet"])
    alco = st.selectbox("🍷 Alkol", ["Hayır", "Evet"])
    active = st.selectbox("🏃 Fiziksel Aktivite", ["Aktif", "Pasif"])

    st.markdown("### ❤️‍🩹 Tansiyon & Biyokimya")
    ap_hi = st.number_input("📈 Sistolik Tansiyon", 80, 200, 120)
    ap_lo = st.number_input("📉 Diastolik Tansiyon", 50, 150, 80)

    cholesterol = st.selectbox("🩸 Kolesterol (1-3)", [1, 2, 3])
    gluc = st.selectbox("🍬 Glukoz (1-3)", [1, 2, 3])

    st.markdown("### ⚖️ Vücut Ölçüleri")
    height = st.number_input("📏 Boy (cm)", 140, 210, 170)
    weight = st.number_input("⚖️ Kilo (kg)", 40, 150, 70)

# ==========================================
# VALUE TRANSFORM (unchanged)
# ==========================================
gender_val = 1 if gender == "Kadın" else 2
smoke_val = 1 if smoke == "Evet" else 0
alco_val = 1 if alco == "Evet" else 0
active_val = 1 if active == "Aktif" else 0

# ==========================================
# BMI calculation
# ==========================================
bmi = weight / ((height / 100) ** 2)

# ==========================================
# FUZZY (original)
# ==========================================
def fuzzy(x, y, z):
    z = 1 - z
    if x == y == z == 0:
        return 0
    elif x == y == z == 1:
        return 1
    else:
        return 0.5

# ==========================================
# RULE SYSTEM (original)
# ==========================================
def rule_system(age, gender, smoke, alco, active):
    other = fuzzy(smoke, alco, active)

    if gender == 1:  # Kadın
        if age < 55:
            if other == 0:
                return "Risk Yok"
            elif other == 0.5:
                return "Risk Olabilir"
            else:
                return "Risk Var"
        else:
            return "Risk Var"
    else:  # Erkek
        if age < 45:
            if other == 0:
                return "Risk Yok"
            elif other == 0.5:
                return "Risk Olabilir"
            else:
                return "Risk Var"
        else:
            return "Risk Var"

# ==========================================
# PREDICTION BUTTON & DISPLAY (enhanced design only)
# ==========================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    predict_click = st.button("🚀 Tahmin Et", use_container_width=True)

if predict_click:

    # --- Display small metrics (informative, no logic change) ---
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(f"<div class='metric-box'>🧬 VKİ: {bmi:.1f}</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown(f"<div class='metric-box'>❤️ Tansiyon: {ap_hi}/{ap_lo}</div>", unsafe_allow_html=True)
    with col_c:
        st.markdown(f"<div class='metric-box'>📊 Kolesterol: {cholesterol} | Glukoz: {gluc}</div>", unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📊 Klinik Değerlendirme Sonucu")

    # =========================
    # RULE MODE (original result)
    # =========================
    if mode == "Rule-Based":
        result = rule_system(age, gender_val, smoke_val, alco_val, active_val)

        if result == "Risk Var":
            icon = "🔴"
            risk_class = "risk-high"
            message = "Yüksek Risk"
            detail = "Acilen bir kardiyoloji uzmanına danışın. Yaşam tarzınızı değiştirmelisiniz."
        elif result == "Risk Olabilir":
            icon = "🟡"
            risk_class = "risk-mid"
            message = "Orta Risk"
            detail = "Düzenli kontroller önerilir. Risk faktörlerini azaltmaya çalışın."
        else:
            icon = "🟢"
            risk_class = "risk-low"
            message = "Düşük Risk"
            detail = "Sağlıklı yaşam tarzınızı koruyun, yıllık kontrollerinizi ihmal etmeyin."

        st.markdown(f"""
        <div class="result-card {risk_class}">
            <div class="icon-big">{icon}</div>
            <h2 style="margin:0">{message}</h2>
            <p style="margin-top:0.8rem; color:#2c3e50;">{detail}</p>
            <hr>
            <span style="font-size:0.9rem;">🧠 Kural tabanlı sistem (Fuzzy Logic + Uzman kuralları)</span>
        </div>
        """, unsafe_allow_html=True)

    # =========================
    # ML MODE (original prediction)
    # =========================
    else:
        input_data = pd.DataFrame([[
            age,
            gender_val,
            ap_hi,
            ap_lo,
            cholesterol,
            gluc,
            bmi
        ]], columns=[
            "age", "gender", "ap_hi", "ap_lo",
            "cholesterol", "gluc", "bmi"
        ])

        input_scaled = scaler.transform(input_data)
        pred = model.predict(input_scaled)[0]

        if pred == 0:
            icon = "🟢"
            risk_class = "risk-low"
            message = "Risk Yok"
            detail = "Modelin tahminine göre kalp hastalığı riski düşük. Sağlıklı alışkanlıklarınızı sürdürün."
        elif pred == 1:
            icon = "🔴"
            risk_class = "risk-high"
            message = "Risk Var"
            detail = "Yüksek risk tespit edildi. Derhal doktora başvurmanız önerilir."
        else:
            icon = "🟡"
            risk_class = "risk-mid"
            message = "Risk Olabilir"
            detail = "Sınırda risk grubu. Detaylı inceleme ve takip gereklidir."

        st.markdown(f"""
        <div class="result-card {risk_class}">
            <div class="icon-big">{icon}</div>
            <h2 style="margin:0">{message}</h2>
            <p style="margin-top:0.8rem; color:#2c3e50;">{detail}</p>
            <hr>
            <span style="font-size:0.9rem;">🤖 Makine Öğrenmesi tahmini (sınıf: {pred})</span>
        </div>
        """, unsafe_allow_html=True)

        # progress bar (kept as original but styled)
        st.markdown("**Model Güven Seviyesi**")
        st.progress((pred + 1) / 3)

# ==========================================
# FOOTER INFO (unchanged message)
# ==========================================
st.markdown("---")
st.info("💡 Bu sistem hem Rule‑Based hem de Machine Learning modeli kullanır. Tüm veriler lokal işlenir, kaydedilmez.")