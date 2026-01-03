import streamlit as st
import pandas as pd
from datetime import datetime
import utils

# --- 配置區 ---
TARGET_DATE = "2026-02-14 09:00:00"
EVENT_LOCATION = {"lat": 23.4416322, "lon": 120.5189539}

st.set_page_config(page_title="2026 新年派對", layout="centered")

@st.cache_data
def load_css(file_path):
    """快取 CSS 內容，避免重複讀取磁碟"""
    try:
        with open(file_path, encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        st.error(f"無法載入 CSS: {e}")
        return ""

# --- 主題邏輯 ---
default_dark = 18 <= datetime.now().hour or datetime.now().hour < 6
is_dark = st.checkbox("🌙 Dark Mode", value=default_dark)

# 顏色配置物件
themes = {
    "dark": {
        "bg": "#121212", "text": "#FFFFFF", "card": "#262626", 
        "accent": "#FF4B4B", "sub_text": "#AAAAAA"
    },
    "light": {
        "bg": "#FDFDFD", "text": "#262730", "card": "#FFFFFF", 
        "accent": "#FF4B4B", "sub_text": "#555555"
    }
}
t = themes["dark"] if is_dark else themes["light"]

# 注入 CSS 與 動態 CSS 變數
css_content = load_css("styles.css")
st.markdown(f"""
<style>
    {css_content}
    
    /* 強制顯示切換按鈕 */
    div[data-testid="stCheckbox"] {{
        position: fixed !important; 
        top: 20px !important; 
        right: 20px !important; 
        z-index: 999999 !important; /* 極高層級 */
        background: {t['card']} !important; 
        padding: 8px 16px !important; 
        border-radius: 50px !important;
        border: 1px solid {t['accent']} !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5) !important;
        display: block !important;
    }}

    :root {{
        --bg-color: {t['bg']}; 
        --text-color: {t['text']};
        --card-bg: {t['card']}; 
        --accent-color: {t['accent']};
        --sub-text-color: {t['sub_text']};
    }}
</style>
""", unsafe_allow_html=True)

# --- 頁面渲染 ---
st.title("🎓 2026 新年派對")
st.header("📍 嘉義包棟時光")

# 幻燈片 (封裝在 div 中以利 CSS 控制)
st.markdown('''
<div class="slideshow-container">
    <div class="slide"></div><div class="slide"></div><div class="slide"></div>
</div>
''', unsafe_allow_html=True)

st.write("### ⏳ 距離出發還有")
utils.render_countdown_ui(TARGET_DATE)

st.write("### 🌦️ 即時天氣預報")
utils.weather_widget()

st.divider()

st.subheader("🗺️ 集合地點：小艾山青 I’s Home")
st.map(pd.DataFrame([EVENT_LOCATION]), zoom=14)
st.link_button("🚀 開啟 Google 地圖導航", "https://maps.google.com/?q=23.4416322,120.5189539")