import streamlit as st
import google.generativeai as genai

# 1. 페이지 설정
st.set_page_config(page_title="노벨피아 프롬프트 메이커", page_icon="🎨")

# 2. API 키 설정 (Secrets 사용)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("API 키가 없습니다. 설정(Secrets)을 확인해주세요.")
except Exception as e:
    st.error(f"오류 발생: {e}")

# 3. 프롬프트 깎는 노인(AI 모델) 설정
# 여기에 대리님이 원하시는 '프롬프트 생성 규칙'을 입력합니다.
SYSTEM_PROMPT = """
당신은 NovelAI 및 Stable Diffusion 전용 프롬프트 생성기입니다.
사용자가 한국어나 영어로 묘사를 입력하면, 그것을 고품질의 영어 태그(Danbooru style)로 변환하세요.

[필수 규칙]
1. 문장이 아니라 '단어, 단어, 단어' 형식으로 출력할 것.
2. 항상 맨 앞에는 다음 퀄리티 태그를 붙일 것:
   (masterpiece, best quality, ultra-detailed, 8k wallpaper), 
3. 사용자의 묘사를 구체적인 시각적 태그로 확장할 것.
4. 설명이나 잡담은 하지 말고 오직 '프롬프트'만 출력할 것.
"""

model = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction=SYSTEM_PROMPT
)

# 4. 화면 구성
st.title("🎨 노벨피아 프롬프트 메이커")
st.markdown("그리고 싶은 캐릭터나 상황을 대충 적으세요. AI가 태그를 정리해줍니다.")

# 입력창 (엔터 치면 바로 생성)
user_input = st.text_input("예: 금발의 엘프 여왕, 숲 속 배경, 신비로운 분위기")

if user_input:
    with st.spinner("프롬프트 깎는 중..."):
        try:
            # AI에게 변환 요청
            response = model.generate_content(user_input)
            
            # 결과 출력
            st.success("생성 완료! 아래 코드를 복사해서 쓰세요.")
            st.code(response.text, language="text") # 복사 버튼이 자동으로 생깁니다
            
        except Exception as e:
            st.error("오류가 났어요. 잠시 후 다시 시도해주세요.")
