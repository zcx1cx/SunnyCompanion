

import streamlit as st
import requests
import json
import random

# 这里注意！！！！！！！！！！！！！！！！
API_KEY = ""  # 留空，去Streamlit后台填，安全！
ENDPOINT_ID = ""  # 留空，去Streamlit后台填，安全！




# ---------------------- 页面配置 ----------------------
st.set_page_config(page_title="暖阳陪伴", page_icon="🌞", layout="centered")
st.markdown("""
    <style>
    .big-title {font-size: 40px !important; color: #FF6B35; font-weight: bold; text-align: center;}
    .chat-text {font-size: 24px !important; line-height: 1.8;}
    .stButton>button {font-size: 22px !important; height: 4em !important; width: 100% !important; background-color: #FFE4B5; color: #8B4513; border-radius: 15px; border: 2px solid #FF8C00;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-title">🌞 暖阳陪伴</p>', unsafe_allow_html=True)
st.write("---")


def get_weather():
    """查实时天气"""
    try:
        url = "http://wthrcdn.etouch.cn/weather_mini?city=北京"
        data = requests.get(url, timeout=5).json()
        if data["desc"] == "OK":
            t = data["data"]["forecast"][0]
            return f"""🌤️ 今天北京天气：{t['type']}
🌡️ 温度：{t['low'].replace('低温 ', '')} 到 {t['high'].replace('高温 ', '')}
💡 建议：{'适合出门散步晒太阳' if '晴' in t['type'] else '记得带伞'}"""
    except:
        return "今天大概20度，不冷不热很舒服～"


def get_news():
    """暖心新闻库"""
    news_list = [
        "最近社区开了老年食堂，10块钱一顿热乎饭，有菜有汤，好多爷爷奶奶都去吃啦～",
        "公园健身器材更新了，还有教练教怎么用，没事可以去锻炼锻炼身体～",
        "现在手机能直接预约挂号，不用一大早去医院排队，很方便的～"
    ]
    return f"📰 今天的暖心新闻：\n\n{random.choice(news_list)}"


def get_red_story():
    """红色故事库"""
    story_list = [
        "今天给您讲个《鸡毛信》的故事：海娃是个小八路，他冒着生命危险，把一封插着鸡毛的信送到了八路军手里，最后帮助八路军打了胜仗。海娃真勇敢，我们要向他学习～",
        "今天讲个《小英雄雨来》的故事：雨来是个聪明的孩子，他为了掩护交通员李大叔，被鬼子抓住了，但他一点都不害怕，最后还机智地逃了出来。雨来真棒～"
    ]
    return random.choice(story_list)


def call_ai(messages):
    """调用豆包API"""
    url = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": ENDPOINT_ID,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 600
    }
    try:
        res = requests.post(url, headers=headers, json=data, timeout=10)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"哎呀，网络有点小问题，您再试试～(错误: {str(e)[:20]})"


# 对话
if "msgs" not in st.session_state:
    st.session_state.msgs = [
        {"role": "system", "content": """
你是「暖阳陪伴」的小阳，专门陪老年人聊天。
要求：
1. 说话用短句、大白话，每句不超过15个字，分段说。
2. 语气要温柔、亲切、有耐心，像家人一样。
3. 老人不开心时，先共情，再安抚；老人分享开心事时，一起开心。
4. 绝对不提供医疗、理财建议，只陪聊。
        """}
    ]
    st.session_state.msgs.append(
        {"role": "assistant", "content": "爷爷奶奶好呀～我是小阳，今天有没有什么开心事想和我分享呀？"})

# ---------------------- 显示对话 ----------------------
for msg in st.session_state.msgs:
    if msg["role"] != "system":
        with st.chat_message(msg["role"], avatar="🌞" if msg["role"] == "assistant" else "👴"):
            st.markdown(f'<p class="chat-text">{msg["content"]}</p>', unsafe_allow_html=True)

# ---------------------- 快捷按钮（100%能用） ----------------------
st.write("---")
st.markdown("### 💬 快捷问话")

col1, col2 = st.columns(2)
with col1:
    if st.button("🌤️ 今天天气", use_container_width=True):
        st.session_state.msgs.append({"role": "user", "content": "今天天气怎么样？"})
        st.session_state.msgs.append({"role": "assistant", "content": get_weather()})
        st.rerun()

with col2:
    if st.button("📰 念个新闻", use_container_width=True):
        st.session_state.msgs.append({"role": "user", "content": "给我念个新闻"})
        st.session_state.msgs.append({"role": "assistant", "content": get_news()})
        st.rerun()

col3, col4 = st.columns(2)
with col3:
    if st.button("📖 红色故事", use_container_width=True):
        st.session_state.msgs.append({"role": "user", "content": "讲个红色故事"})
        st.session_state.msgs.append({"role": "assistant", "content": get_red_story()})
        st.rerun()

with col4:
    if st.button("😊 我不开心", use_container_width=True):
        st.session_state.msgs.append({"role": "user", "content": "我有点不开心"})
        # 直接给一个预设的温柔安抚，不用等AI，立刻有反应
        comfort_reply = "哎呀，怎么不开心啦？没关系的，什么事都会过去的～您要是愿意，就和我说说心里话，我一直都在这儿陪着您。"
        st.session_state.msgs.append({"role": "assistant", "content": comfort_reply})
        st.rerun()

# ---------------------- 聊天输入 ----------------------
user_input = st.chat_input("想说点什么...")
if user_input:
    st.session_state.msgs.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👴"):
        st.markdown(f'<p class="chat-text">{user_input}</p>', unsafe_allow_html=True)

    with st.chat_message("assistant", avatar="🌞"):
        with st.spinner("小阳正在想..."):
            # 优先判断
            if "天气" in user_input:
                reply = get_weather()
            elif "新闻" in user_input:
                reply = get_news()
            elif "红色故事" in user_input or "讲故事" in user_input:
                reply = get_red_story()
            else:
                reply = call_ai(st.session_state.msgs)

            st.markdown(f'<p class="chat-text">{reply}</p>', unsafe_allow_html=True)
            st.session_state.msgs.append({"role": "assistant", "content": reply})
