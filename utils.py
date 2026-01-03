import streamlit as st
from datetime import datetime

def get_countdown_data(target_date_str):
    """計算倒數時間邏輯"""
    try:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d %H:%M:%S")
        diff = target_date - datetime.now()
        if diff.total_seconds() > 0:
            days, rem = divmod(int(diff.total_seconds()), 86400)
            hours, rem = divmod(rem, 3600)
            minutes, seconds = divmod(rem, 60)
            return {"days": days, "hours": hours, "min": minutes, "sec": seconds}
    except Exception:
        return None
    return None

@st.fragment(run_every=1.0)
def render_countdown_ui(target_date_str):
    """渲染倒數 UI 區塊"""
    data = get_countdown_data(target_date_str)
    if data:
        st.markdown(f"""
        <div class="flip-container">
            <div class="flip-card"><div class="flip-value">{data['days']:02d}</div><div class="flip-label">Days</div></div>
            <div class="flip-card"><div class="flip-value">{data['hours']:02d}</div><div class="flip-label">Hours</div></div>
            <div class="flip-card"><div class="flip-value">{data['min']:02d}</div><div class="flip-label">Min</div></div>
            <div class="flip-card"><div class="flip-value">{data['sec']:02d}</div><div class="flip-label">Sec</div></div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("🎉 派對已經開始囉！")

def weather_widget():
    """渲染天氣組件"""
    html_code = """
    <div style="
        background: rgba(0, 0, 0, 0.6); backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px; padding: 20px; color: white;
        display: flex; align-items: center; justify-content: space-between;
        font-family: sans-serif;
    ">
        <div style="flex: 1; text-align: left;">
            <div style="font-size: 0.8rem; opacity: 0.8;">📍 嘉義中埔鄉</div>
            <div style="font-size: 2.5rem; font-weight: bold; margin: 5px 0;">22°C</div>
            <div style="font-size: 1rem; color: #FF4B4B; font-weight: bold;">多雲轉晴</div>
        </div>
        <div style="text-align: right;">
            <svg width="70" height="70" viewBox="0 0 64 64">
                <defs>
                    <linearGradient id="sunGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" style="stop-color:#FFD200;" />
                        <stop offset="100%" style="stop-color:#F7971E;" />
                    </linearGradient>
                </defs>
                <circle cx="32" cy="32" r="14" fill="url(#sunGradient)">
                    <animateTransform attributeName="transform" type="rotate" from="0 32 32" to="360 32 32" dur="10s" repeatCount="indefinite"/>
                </circle>
                <path d="M48,40c0-6.6-5.4-12-12-12c-0.9,0-1.8,0.1-2.7,0.3C30.6,22.6,24.8,19,18,19c-8.3,0-15,6.7-15,15c0,0.5,0,0.9,0.1,1.4 C1.3,36.5,0,38.6,0,41c0,3.9,3.1,7,7,7h38c5.5,0,10-4.5,10-10C55,42.4,52,38.5,48,40z" fill="white" opacity="0.9" />
            </svg>
            <div style="font-size: 0.7rem; opacity: 0.7; margin-top: 5px;">濕度 65% | 體感溫和</div>
        </div>
    </div>
    """.strip()
    st.components.v1.html(html_code, height=160)