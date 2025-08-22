import streamlit as st

# =======================
# 샘플 노래 데이터베이스 (자체 추천)
# =======================
songs = [
    {"title": "밤편지", "artist": "아이유", "keywords": ["감성", "발라드"], "youtube": "https://www.youtube.com/watch?v=-2wMByiPrUE"},
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "keywords": ["락", "감성"], "youtube": "https://www.youtube.com/watch?v=12345"},
    {"title": "Dynamite", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Love Poem", "artist": "아이유", "keywords": ["감성", "사랑", "발라드"], "youtube": "https://www.youtube.com/watch?v=abcde"},
    {"title": "Permission to Dance", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=xyz12"},
]

# =======================
# 페이지 설정
# =======================
st.set_page_config(page_title="🎵 안정형 음악 추천기", page_icon="🎧")
st.title("🎤 키워드 기반 음악 추천기 (안정형)")

# =======================
# 세션 상태 초기화
# =======================
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "new_keyword" not in st.session_state:
    st.session_state["new_keyword"] = []

# =======================
# 키워드 추가 함수
# =======================
def add_keyword():
    kw = st.session_state.new_keyword.strip()
    if kw and kw not in st.session_state.keywords:
        st.session_state.keywords.append(kw)
    st.session_state.new_keyword = ""

# =======================
# 키워드 입력
# =======================
st.text_input(
    "🎵 키워드 입력", 
    key="new_keyword", 
    placeholder="예: 감성, 사랑, 락", 
    on_change=add_keyword
)

# =======================
# 현재 키워드 출력
# =======================
if st.session_state.keywords:
    st.markdown("#### 📌 현재 키워드:")
    st.write(", ".join(st.session_state.keywords))
    if st.button("❌ 키워드 모두 초기화"):
        st.session_state.keywords = []

# =======================
# 추천 버튼
# =======================
if st.button("🎶 추천 받기") and st.session_state.keywords:
    try:
        import openai
        # OpenAI API 키 확인
        if st.secrets.get("OPENAI_API_KEY"):
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            # AI 추천
            with st.spinner("AI가 음악 추천 중...🎧"):
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
                result = response.choices[0].message['content']
                st.subheader("🎵 AI 추천 결과:")
                st.markdown(result)
                raise SystemExit  # AI 결과가 나오면 자체 추천 건너뜀
        else:
            raise Exception("OPENAI_API_KEY 없음")
    except Exception:
        # =======================
        # 자체 키워드 기반 추천
        # =======================
        matched = []
        for song in songs:
            if any(k.lower() in [kw.lower() for kw in st.session_state.keywords] for k in song["keywords"]):
                matched.append(song)
        if not matched:
            st.info("🔍 입력한 키워드와 매칭되는 노래가 없습니다.")
        else:
            st.subheader("🎵 자체 추천 결과:")
            for i, song in enumerate(matched[:3], 1):
                st.markdown(f"{i}. **{song['title']}** - {song['artist']}")
                st.video(song["youtube"])
