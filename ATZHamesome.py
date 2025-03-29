from re import A
import streamlit as st

import requests

# 初始化会话状态
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'progress' not in st.session_state:
    st.session_state.progress = 0
if 'instruction' not in st.session_state:
    st.session_state.instruction = ""
if 'content' not in st.session_state:
    st.session_state.content = ""

# 定义DeepSeek API端点
API_ENDPOINT = "https://api.deepseek.com/v1/chat/completions"

# 定义DeepSeek API密钥
API_KEY = "sk-e066a49d769a46669e46f8ca60181b9d"  # 请替换为实际的API密钥

col1, col2 = st.columns(2)
with col1:
    st.title("艾天卓很帅")
# 界面布局
with col2:
# 下拉菜单
    model = st.selectbox("选择DeepSeek模型", ["deepseek-chat", "deepseek-reasoner"])

# 将指令和内容输入框并排摆放
col1, col2 = st.columns(2)
with col1:
    instruction = st.text_area("指令", value=st.session_state.instruction, height=200)
    # 更新会话状态中的指令值
    st.session_state.instruction = instruction
with col2:
    content = st.text_area("内容", value=st.session_state.content, height=200)
    # 更新会话状态中的内容值
    st.session_state.content = content

# 使用 st.empty() 预留结果文本框位置
result_text_area = st.empty()
result_text_area.text_area("结果", value=st.session_state.result, height=200)

# 按钮
if st.button("开始处理"):
        content_blocks = content.split("//")
        num_blocks = len(content_blocks)
        st.session_state.result = ""
        st.session_state.progress = 0
        progress_bar = st.progress(0)

        for i, block in enumerate(content_blocks):
            # 构建请求数据
            data = {
                "model": model,
                "messages": [
                    {"role": "user", "content": instruction + block}
                ]
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }

            # 发送请求
            response = requests.post(API_ENDPOINT, headers=headers, json=data)
            if response.status_code == 200:
                response_data = response.json()
                content_part = response_data['choices'][0]['message']['content']
                if i > 0:
                    st.session_state.result += "\n---\n\n"
                st.session_state.result += content_part
                st.session_state.progress = (i + 1) / num_blocks
                progress_bar.progress(st.session_state.progress)
                # 更新预留的结果文本框
                result_text_area.text_area("结果", value=st.session_state.result, height=200)
            else:
                st.error(f"请求失败，状态码: {response.status_code}")




