import requests
import streamlit as st
from streamlit_lottie import st_lottie
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

def get_chiayi_weather():
    # 嘉義中埔鄉的經緯度 (或是直接搜 'Chiayi')
    api_key = "ba9bec91fd67776e4884065120251ec4" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q=Chiayi&appid={api_key}&units=metric&lang=zh_tw"
    
    try:
        res = requests.get(url).json()
        temp = int(res['main']['temp']) # 溫度
        desc = res['weather'][0]['description'] # 多雲、晴...
        humidity = res['main']['humidity'] # 濕度
        icon = res['weather'][0]['main'] # 天氣狀態 (Rain, Clear, Clouds)
        return temp, desc, humidity, icon
    except:
        return 22, "連線中...", 60, "Clear" # 如果出錯給個預設值

def load_lottieurl(url: str):
    import requests
    try:
        r = requests.get(url, timeout=3) # 加入 timeout 防止網頁卡死
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None


def weather_widget():
    temp, desc, humidity, weather_type = get_chiayi_weather()
    
    # 根據天氣狀態決定 Lottie 網址
    lottie_urls = {
        "Clear": "https://lottie.host/805166f2-1430-47b2-8418-2029302e6040/z0T03Xj4bM.json", # 太陽
        "Clouds": "https://lottie.host/936a7114-114c-473d-963d-4c3e80f9fe63/Gq8Y31O8H9.json", # 雲
        "Rain": "https://lottie.host/64299b82-628f-4f65-8b37-2938171d7d06/mSj1kG9x9B.json"    # 下雨
    }
    selected_url = lottie_urls.get(weather_type, lottie_urls["Clear"])
    lottie_data = load_lottieurl(selected_url)

    # 渲染組件
    st.markdown(f"""
    <div style="
        background: rgba(255, 255, 255, 0.05); 
        backdrop-filter: blur(15px); 
        border-radius: 20px; 
        border: 1px solid rgba(255, 255, 255, 0.1);
        display: flex; /* 用 flex 讓內容並排 */
        align-items: center;
        justify-content: space-between;
        padding: 20px;
    ">
        <div>
            <div style="font-size: 0.8rem; opacity: 0.7;">📍 嘉義</div>
            <div style="font-size: 2.5rem; font-weight: bold; color: white;">{temp}°C</div>
            <div style="font-size: 1rem; color: #FF4B4B;">{desc}</div>
            <div style="font-size: 0.7rem; opacity: 0.5;">濕度 {humidity}%</div>
        </div>
        <div id="icon-placeholder"></div>
    </div>
    """, unsafe_allow_html=True)

    # 接著在下方直接呼叫動畫，它會緊貼著上方內容
    if lottie_data:
        st_lottie(lottie_data, height=120, key="weather_icon")