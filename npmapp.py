import streamlit as st
import google.generativeai as genai

# 1. 페이지 제목과 아이콘 설정
st.set_page_config(page_title="Novelpia Prompt Maker", page_icon="🎨")

# 2. API 키 연결 (비밀 금고에서 꺼내오기)
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    else:
        st.error("🚨 API 키가 없습니다. Streamlit 설정(Secrets)을 확인해주세요.")
except Exception as e:
    st.error(f"시스템 오류: {e}")

# 3. 프롬프트 깎는 노인 (AI 설정)
# 이 부분이 핵심입니다. 개떡같이 말해도 찰떡같이 태그로 바꿔주는 마법의 주문입니다.
SYSTEM_PROMPT = """
ROLE: You are an AI image prompt generator specializing in 'NovelAI' and 'Stable Diffusion' anime styles.
GOAL: Convert user descriptions (Korean/English) into high-quality Danbooru tags.

[RULES]
1. Output MUST be a comma-separated list of tags.
2. ALWAYS start with quality tags: (masterpiece, best quality, ultra-detailed, 8k wallpaper, cinematic lighting)
3. Convert Korean descriptions into precise English tags (e.g., "금발" -> "blonde hair").
4. Add relevant artistic tags based on context (e.g., "fantasy", "cyberpunk", "intricate details").
5. DO NOT output full sentences. ONLY tags.
"""

model = genai.GenerativeModel(
    'gemini-1.5-pro',
    system_instruction=SYSTEM_PROMPT
)

# 4. 화면 디자인 (심플하고 직관적이게)
st.title("🎨 노벨피아 프롬프트 메이커")
st.markdown("##### \"대충 적어도, 결과물은 걸작으로.\"")
st.info("💡 캐릭터의 외모, 의상, 분위기를 한글로 편하게 적어주세요.")

# 입력창
user_input = st.text_input("예시: 은발의 여기사, 붉은 눈, 피 묻은 갑옷, 전장, 비장한 분위기")

# 5. 생성 버튼 및 로직
if user_input:
    # 버튼이 눌리면 작동
    with st.spinner("AI가 뇌를 굴리는 중입니다... 🧠"):
        try:
            response = model.generate_content(user_input)
            
            st.success("✨ 프롬프트 생성 완료!")
            st.markdown("아래 코드를 복사해서 노벨AI나 WebUI에 붙여넣으세요.")
            
            # 복사하기 좋게 코드 블록으로 출력
            st.code(response.text, language="text")
            
        except Exception as e:
            st.error("이런, AI가 과부하 걸렸습니다. 잠시 후 다시 시도해주세요.")
