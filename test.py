import streamlit as st

# openai 설치 여부 확인
try:
    import openai
except ModuleNotFoundError:
    st.error("⚠️ openai 라이브러리가 설치되지 않았습니다. requirements.txt 파일을 확인하세요.")
    openai = None

# 세션 상태 초기화
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "new_keyword" not in st.session_state:
    st.session_state["new_keyword"] = ""

# 키워드 추가 함수 (엔터로 입력되었을 때 실행됨)
def add_keyword():
    keyword = st.session_state.new_keyword.strip()
    if keyword and keyword not in st.session_state.keywords:
        st.session_state.keywords.append(keyword)
    st.session_state.new_keyword = ""  # 입력창 초기화

# 페이지 UI
st.set_page_config(page_title="노래 추천기 🎵", page_icon="🎧")
st.title("🎧 키워드를 추가해서 노래 추천 받기")
st.markdown("예: 감성, 사랑, 락, 팝송 등 키워드를 엔터로 추가해보세요!")

# 키워드 입력 (엔터만 치면 바로 추가됨)
st.text_input("🎵 키워드 입력", 
              key="new_keyword", 
              placeholder="예: 몽환적인, 에너지 넘치는", 
              on_change=add_keyword)

# 키워드 리스트 출력
if st.session_state.keywords:
    st.markdown("#### 📌 현재 키워드:")
    st.write(", ".join(st.session_state.keywords))

    if st.button("❌ 키워드 모두 초기화"):
        st.session_state.keywords = []

# 추천 받기 버튼
if st.button("🎶 추천 받기") and st.session_state.keywords:
    if openai is None:
        st.error("OpenAI 라이브러리가 설치되지 않았습니다.")
    else:
        with st.spinner("AI가 음악을 추천 중이에요...🎧"):
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]

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
