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
    import base64
    import os
    if os.path.exists(path):
        with open(path, "rb") as f:
            # 去掉換行符，確保編碼是連續的長字串
            return base64.b64encode(f.read()).decode().replace("\n", "").replace("\r", "")
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

st.balloons()

st.write("### ⏳ 距離出發還有")
utils.render_countdown_ui(TARGET_DATE)

members_data = [
    {"name": "嘉鴻", "image": "static/member/CH.jpg", "bio": "規劃主理人！🍻"},
    {"name": "侑玹", "image": "static/member/YH.jpg", "bio": "規劃主理人！🍻"},
    {"name": "維彤", "image": "static/member/WT.jpg", "bio": "專業舞者！🕺"},
    {"name": "宏毅", "image": "static/member/HY.jpg", "bio": "專業 coser！🎂"},
    {"name": "虹汶", "image": "static/member/HW.jpg", "bio": "活動參與者！🚗"},
    {"name": "仔平", "image": "static/member/TP.jpg", "bio": "活動參與者！🚗"},
    {"name": "耀云", "image": "static/member/YW.jpg", "bio": "活動參與者！🚗"},
    {"name": "穗穗", "image": "static/member/SS.jpg", "bio": "活動參與者！🚗"},
    {"name": "唐彥", "image": "static/member/TY.jpg", "bio": "活動參與者！🚗"},
    # ... 你可以繼續增加成員
]

st.write("### 🌟 我們的派對小隊 🌟")

member_items = []

for member in members_data:
    img_b64 = get_base64_img(member["image"]).replace("\n", "").replace("\r", "")
    
    # 使用 f-string，但把所有換行和縮排通通拿掉
    item_html = (
        f'<div class="member-card">'
        f'<div class="member-avatar" style=\'background-image: url("data:image/jpeg;base64,{img_b64}"); background-size: cover; background-position: center; width: 100px; height: 100px; border-radius: 50%; margin: 0 auto 10px; border: 2px solid white;\'></div>'
        f'<div class="member-name">{member["name"]}</div>'
        f'<div class="member-bio">{member["bio"]}</div>'
        f'</div>'
    )
    member_items.append(item_html)

# 關鍵：將所有卡片連成「一整行」，完全不留任何換行符號或空白
all_members_content = "".join(member_items)
final_grid_html = f'<div class="members-grid">{all_members_content}</div>'

# 一次性渲染，確保沒有 Markdown 語法干擾
st.markdown(final_grid_html, unsafe_allow_html=True)

st.write("### 🌦️ 即時天氣預報")
utils.weather_widget()

# --- 派對特別企劃區塊 ---
st.write("### 🎭 派對特別企劃：創意極限挑戰")

# 使用 Markdown 渲染兩個活動說明卡片
st.markdown("""
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-bottom: 30px;">
    <div style="background: rgba(255, 75, 75, 0.1); border: 1px solid #FF4B4B; border-radius: 15px; padding: 20px; backdrop-filter: blur(10px);">
        <h4 style="color: #FF4B4B; margin-top: 0;">📸 低成本 Cosplay 大賽 & 🍳創意料理秀</h4>
        <p style="font-size: 0.9rem; line-height: 1.6;">
            <b>主題：</b>食物或網路迷因 (Meme)<br>
            <b>規則：</b>運用生活周邊的物品進行變裝，並搭配一道有趣的自製料理<br>
            <span style="color: #FF4B4B;"><i>※ 評分標準：越好笑越好，料理請確保不會拉肚子</i></span>
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("### 📅 兩日行程揭曉")

st.markdown("""
<div class="timeline-container">
    <div class="event-card">
        <div class="event-day">DAY 01</div>
        <div class="event-title">嘉義 Arrival 🥂</div>
        <div class="event-detail">1. 11:30 | <b>嘉義火車站集合</b></div>
        <div class="event-detail">2. <b>租車 & 午餐時間 🍱</b></div>
        <div class="event-detail">3. <b>市區閒晃</b></div>
        <div class="event-detail">4. <b>民宿 check-in</b></div>
        <div class="event-detail">5. <b>晚餐時間</b></div>
        <div class="event-detail">6. <b>活動+桌遊</b></div>
        <div class="event-detail">7. <b>看星星</b></div>
        <div class="event-detail">8. <b>Good night...zzZ</b></div>
    </div> <div class="event-card">
        <div class="event-day">DAY 02</div>
        <div class="event-title">悠閒時光 🥞</div>
        <div class="event-detail">1. <b>看日出</b></div>
        <div class="event-detail">2. <b>吃早餐</b></div>
        <div class="event-detail">3. <b>TBD...</b></div>
    </div> </div>
""", unsafe_allow_html=True)

# st.divider()

st.subheader("🗺️ 民宿: 小艾山青 I’s Home")
st.map(pd.DataFrame([EVENT_LOCATION]), zoom=14)
st.link_button("🚀 開啟 Google 地圖導航", "https://www.google.com/maps?q=23.4416322,120.5189539")