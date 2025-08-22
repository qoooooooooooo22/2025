import streamlit as st

# openai 설치 여부 확인
try:
    import openai
except ModuleNotFoundError:
    st.error("⚠️ openai 라이브러리가 설치되지 않았습니다. requirements.txt 확인")
    openai = None

# 페이지 설정
st.set_page_config(page_title="🎵 음악 추천기", page_icon="🎧")
st.title("🎤 키워드 기반 노래 추천기")
st.markdown("키워드를 입력하고 엔터를 치면 자동으로 추가됩니다. 예: 감성, 사랑, 락, 팝송")

# 세션 상태 초기화
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "new_keyword" not in st.session_state:
    st.session_state["new_keyword"] = ""

# 키워드 추가 함수 (엔터 입력 시)
def add_keyword():
    keyword = st.session_state.new_keyword.strip()
    if keyword and keyword not in st.session_state.keywords:
        st.session_state.keywords.append(keyword)
    st.session_state.new_keyword = ""  # 입력창 초기화

# 키워드 입력 (엔터로 추가)
st.text_input(
    "🎵 키워드 입력", 
    key="new_keyword", 
    placeholder="예: 몽환적, 에너지 넘치는", 
    on_change=add_keyword
)

# 키워드 리스트 출력
if st.session_state.keywords:
    st.markdown("#### 📌 현재 키워드:")
    st.write(", ".join(st.session_state.keywords))
    if st.button("❌ 키워드 모두 초기화"):
        st.session_state.keywords = []

# 추천 버튼
if st.button("🎶 추천 받기") and st.session_state.keywords:
    if openai is None:
        st.error("OpenAI 라이브러리가 설치되지 않았습니다.")
    else:
        # OpenAI API 키 불러오기 (Secrets)
        try:
            openai.api_key = st.secrets["OPENAI_API_KEY"]
        except KeyError:
            st.error("❌ OPENAI_API_KEY가 st.secrets에 없습니다. Streamlit Cloud settings → Secrets에 추가하세요.")
        
        with st.spinner("AI가 음악 추천 중...🎧"):
            try:
                keywords_str = ", ".join(st.session_state.keywords)

                prompt = f"""
                다음 키워드를 기반으로 한국 음악 또는 팝송 중 어울리는 노래 3곡을 추천해줘.
                각 곡은 다음 형식으로 출력해줘:
                1. 곡 제목 - 아티스트 (YouTube 링크)
                키워드: {keywords_str}
                """

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8
                )

                result = response.choices[0].message.content
                st.subheader("🎵 AI 추천 결과:")
                st.markdown(result)

            except Exception as e:
                st.error(f"OpenAI 호출 중 오류: {e}")
