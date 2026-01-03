import streamlit as st
import pandas as pd
from datetime import datetime
import base64
import utils

# --- 配置區 ---
TARGET_DATE = "2026-02-14 09:00:00"
EVENT_LOCATION = {"lat": 23.4416322, "lon": 120.5189539}

st.set_page_config(page_title="2026 新年派對", layout="centered")

# --- 自動主題切換 (移除手動按鈕) ---
is_dark = 18 <= datetime.now().hour or datetime.now().hour < 6

themes = {
    "dark": {"bg": "#121212", "text": "#FFFFFF", "card": "#262626", "accent": "#FF4B4B", "sub_text": "#AAAAAA"},
    "light": {"bg": "#FDFDFD", "text": "#262730", "card": "#FFFFFF", "accent": "#FF4B4B", "sub_text": "#555555"}
}
t = themes["dark"] if is_dark else themes["light"]

# --- 圖片處理 (Base64 注入) ---
def get_base64_img(path):
    try:
        with open(path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

img1 = get_base64_img("static/img_1.jpg")
img2 = get_base64_img("static/img_2.jpg")
img3 = get_base64_img("static/img_3.jpg")

# --- 注入 CSS 與 動態變數 ---
try:
    with open("styles.css", encoding="utf-8") as f:
        css_content = f.read()
except:
    css_content = ""

st.markdown(f"""
<style>
    {css_content}
    :root {{
        --bg-color: {t['bg']}; --text-color: {t['text']};
        --card-bg: {t['card']}; --accent-color: {t['accent']};
        --sub-text-color: {t['sub_text']};
    }}
    /* 直接覆蓋圖片路徑為 Base64 */
    .slide:nth-child(1) {{ background-image: url("data:image/jpg;base64,{img1}"); }}
    .slide:nth-child(2) {{ background-image: url("data:image/jpg;base64,{img2}"); }}
    .slide:nth-child(3) {{ background-image: url("data:image/jpg;base64,{img3}"); }}
    
    /* 移除 Checkbox 佔位 */
    div[data-testid="stCheckbox"] {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# --- 頁面渲染 ---
st.title("🎓 2026 新年派對")
st.header("📍 嘉義包棟時光")

st.markdown('<div class="slideshow-container"><div class="slide"></div><div class="slide"></div><div class="slide"></div></div>', unsafe_allow_html=True)

st.write("### ⏳ 距離出發還有")
utils.render_countdown_ui(TARGET_DATE)

st.write("### 🌦️ 即時天氣預報")
utils.weather_widget()

st.divider()

st.subheader("🗺️ 集合地點：小艾山青 I’s Home")
st.map(pd.DataFrame([EVENT_LOCATION]), zoom=14)
st.link_button("🚀 開啟 Google 地圖導航", "https://www.google.com/maps?q=23.4416322,120.5189539")