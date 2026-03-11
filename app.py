# ------------------------------------------------------
# 【使用说明】
# 1. 安装依赖库：在PyCharm下方的Terminal里输入：pip install streamlit requests
# 2. 填入API Key：在下方第25行填入你的豆包API Key
# 3. 填入Prompt：在下方第30行填入你优化后的养老专属Prompt
# 4. 运行代码：在Terminal里输入：streamlit run app.py
# ------------------------------------------------------

# 导入必要的库
import streamlit as st  # 用于做网页界面的库
import requests  # 用于调用API的库
import json  # 用于处理数据格式

# ------------------------------------------------------
# ⚠️ 【配置区域】请在此处填入你的信息 ⚠️
# ------------------------------------------------------

# TODO 1: 把你的豆包 API Key 填在引号里
API_KEY = "在这里填入你的API_KEY"

# TODO 2: 把你为养老场景优化的专属 System Prompt 填在这里
# 示例：你是一个贴心的养老陪伴机器人，名叫暖阳，说话要慢，语气要温柔，像家人一样...
ELDERLY_PROMPT = """
在这里填入你精心设计的养老专属Prompt
"""

# 豆包 API 的调用地址（通常不需要改，如果你用的是火山方舟，需确认具体URL）
# 这里假设使用的是通用的 OpenAI 兼容格式接口，如果是火山原生接口需调整下方请求体
API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"  # 示例地址，请以实际为准

# ------------------------------------------------------
# 【界面设计】适老化配置
# ------------------------------------------------------

# 设置页面配置
st.set_page_config(page_title="暖阳陪伴", layout="centered")

# 自定义CSS样式：大字体、暖色调
# 这就是为什么界面看起来适合老人的原因
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

# 显示标题
st.markdown('<p class="big-title">🌞 暖阳陪伴</p>', unsafe_allow_html=True)
st.write("---")  # 分割线

# ------------------------------------------------------
# 【核心逻辑】对话功能
# ------------------------------------------------------

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
        "model": "ep-2024...",  # ⚠️ 注意：这里需要替换成你在火山方舟创建的模型端点ID (Endpoint ID)
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


# ------------------------------------------------------
# 【交互区域】老人输入的地方
# ------------------------------------------------------

# 底部快捷按钮区域
st.write("---")
st.markdown("### 快捷问话")
col1, col2 = st.columns(2)

with col1:
    if st.button("📰 今天天气怎么样？"):
        # 把按钮内容当作用户输入
        st.session_state.messages.append({"role": "user", "content": "今天天气怎么样？"})
        st.rerun()  # 刷新页面

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

# 文字输入框
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

# ------------------------------------------------------
# 【部署说明】
# 1. 去 GitHub 建一个仓库，把 app.py 传上去。
# 2. 登录 share.streamlit.io，用 GitHub 账号登录。
# 3. 点击 "New app"，选择你的仓库和文件，点击 Deploy。
# 4. 在 Settings -> Secrets 里把你的 API_KEY 填进去（更安全），或者直接先填在代码里测试。
# ------------------------------------------------------