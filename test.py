import streamlit as st

# openai 설치 여부 확인
try:
    import openai
except ModuleNotFoundError:
    st.error("⚠️ openai 라이브러리가 설치되지 않았습니다. requirements.txt 파일을 확인하세요.")
    openai = None

# 페이지 기본 설정
st.set_page_config(page_title="노래 추천기 🎵", page_icon="🎧")
st.title("🎧 키워드를 추가해서 노래 추천 받기")
st.markdown("예: 감성, 사랑, 락, 팝송 등 자유롭게 키워드를 추가해보세요!")

# 키워드 입력 및 저장용 세션 상태
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []

# 키워드 입력 창
new_keyword = st.text_input("🎵 키워드 입력", placeholder="예: 감성")

# 키워드 추가 버튼
if st.button("➕ 키워드 추가"):
    if new_keyword and new_keyword.strip() != "":
        st.session_state.keywords.append(new_keyword.strip())
        st.success(f"'{new_keyword}' 키워드가 추가되었어요!")

# 현재 키워드 리스트 보여주기
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
        with st.spinner("AI가 음악을 추천 중이에요...🎧"):
            try:
                openai.api_key = st.secrets["OPENAI_API_KEY"]

                # 키워드들을 문자열로 연결
                keywords_str = ", ".join(st.session_state.keywords)

                # GPT에게 줄 프롬프트
                prompt = f"""
                다음 키워드를 기반으로 한국 혹은 팝송 중에서 어울리는 음악을 3곡 추천해줘.
                각 곡은 아래 형식으로 출력해줘:
                1. 곡 제목 - 아티스트 (YouTube 링크)
                키워드: {keywords_str}
                """

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8
                )

                answer = response.choices[0].message.content
                st.subheader("🎵 AI 추천 결과:")
                st.markdown(answer)

            except Exception as e:
                st.error(f"OpenAI 호출 중 오류: {e}")
