import streamlit as st
import google.generativeai as genai

# 페이지 기본 설정
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# API 키 설정 (Streamlit Secrets에서 가져옵니다)
# 절대 이 파일 안에 직접 API 키를 적지 마세요!
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("API 키가 설정되지 않았습니다.")
except Exception as e:
    st.error(f"설정 오류: {e}")

# 모델 설정
model = genai.GenerativeModel('gemini-1.5-pro')

st.title("🤖 AI 챗봇")
st.markdown("자유롭게 대화해보세요.")

# 대화 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("메시지를 입력하세요..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        try:
            response = model.generate_content([m["content"] for m in st.session_state.messages], stream=True)
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            full_response = "죄송합니다. 오류가 발생했습니다."
            message_placeholder.markdown(full_response)
            
    st.session_state.messages.append({"role": "model", "content": full_response})
