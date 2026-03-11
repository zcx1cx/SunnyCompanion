# 导入必要的库
import streamlit as st  # 做网页界面的
import requests  # 调用API的
import json  # 处理数据格式


# 填个人信息 


# 方舟coding plan API Key 
API_KEY = ""#先空着 去Steamlit后台填

# 养老专属 System Prompt 

ELDERLY_PROMPT = """

"""


API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"  # 


# 页面
st.set_page_config(page_title="暖阳陪伴", layout="centered")

# 自定义样式：大字体、暖色调
# 界面看起来适合老人
st.markdown("""
    <style>
    .big-title {
        font-size: 36px !important;
        color: #FF8C00; /* 暖橙色 */
        font-weight: bold;
        text-align: center;
    }
    .chat-text {
        font-size: 24px !important;
        line-height: 1.6;
    }
    .stButton>button {
        font-size: 20px !important;
        height: 3em !important;
        width: 100% !important;
        background-color: #FFE4B5; /* 暖黄色背景 */
        color: #8B4513;
        border-radius: 10px;
        border: 2px solid #FF8C00;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-title">🌞 暖阳陪伴</p>', unsafe_allow_html=True)
st.write("---")  


# 对话功能


# 初始化会话状态（让机器人能记住之前的对话）
if "messages" not in st.session_state:
    st.session_state.messages = []
    # 把养老Prompt作为系统消息加进去
    st.session_state.messages.append({"role": "system", "content": ELDERLY_PROMPT})

# 显示历史对话记录
for message in st.session_state.messages:
    if message["role"] != "system":  # 不显示系统Prompt给用户看
        with st.chat_message(message["role"]):
            st.markdown(f'<p class="chat-text">{message["content"]}</p>', unsafe_allow_html=True)


# 定义调用豆包API的函数
def get_response(prompt):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # 构建请求数据
    data = {
        "model": "ep-2024...", 
        "messages": st.session_state.messages,
        "temperature": 0.7  # 控制回复的随机性，0.7比较适中
    }

    try:
        # 发送请求
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"哎呀，网络有点问题，稍后再试吧。(错误: {str(e)})"


# 老人输入的地方

# 底部快捷按钮区域
st.write("---")
st.markdown("### 快捷问话")
col1, col2 = st.columns(2)

with col1:
    if st.button("📰 今天天气怎么样？"):
        # 把按钮内容当作用户输入
        st.session_state.messages.append({"role": "user", "content": "今天天气怎么样？"})
        st.rerun()  # 刷新

with col2:
    if st.button("📖 讲个红色故事"):
        st.session_state.messages.append({"role": "user", "content": "请给我讲一个简短的红色革命故事。"})
        st.rerun()

# 另一个行的按钮
col3, col4 = st.columns(2)
with col3:
    if st.button("😊 我有点不开心"):
        st.session_state.messages.append({"role": "user", "content": "我有点不开心，你能陪陪我吗？"})
        st.rerun()

with col4:
    if st.button("⏰ 提醒我吃药"):
        st.session_state.messages.append({"role": "user", "content": "现在是早上，请温柔地提醒我该吃药了。"})
        st.rerun()

# 文字输入
user_input = st.chat_input("想说点什么...")

# 处理用户输入
if user_input:
    # 1. 显示用户的话
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(f'<p class="chat-text">{user_input}</p>', unsafe_allow_html=True)

    # 2. 生成并显示机器人的回复
    with st.chat_message("assistant"):
        with st.spinner("正在思考中..."):  # 显示加载动画
            full_response = get_response(user_input)
            st.markdown(f'<p class="chat-text">{full_response}</p>', unsafe_allow_html=True)

    # 3. 把机器人回复存进历史记录
    st.session_state.messages.append({"role": "assistant", "content": full_response})

