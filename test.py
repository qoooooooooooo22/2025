import streamlit as st

# 🎶 자체 추천용 노래 데이터베이스
songs = [
    {"title": "밤편지", "artist": "아이유", "keywords": ["감성", "발라드"], "youtube": "https://www.youtube.com/watch?v=-2wMByiPrUE"},
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "keywords": ["락", "감성"], "youtube": "https://www.youtube.com/watch?v=12345"},
    {"title": "Dynamite", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Love Poem", "artist": "아이유", "keywords": ["감성", "사랑", "발라드"], "youtube": "https://www.youtube.com/watch?v=abcde"},
    {"title": "Permission to Dance", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=xyz12"},
]

# 페이지 설정
st.set_page_config(page_title="🎧 음악 추천기", page_icon="🎶")
st.title("🎤 키워드 기반 음악 추천기 (AI + 백업 추천)")

# 세션 상태 초기화
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "new_keyword" not in st.session_state:
    st.session_state["new_keyword"] = ""

# ✅ 키워드 추가 함수
def add_keyword():
    if "new_keyword" in st.session_state:
        kw = st.session_state["new_keyword"].strip()
        if kw and kw not in st.session_state["keywords"]:
            st.session_state["keywords"].append(kw)
        st.session_state["new_keyword"] = ""  # 입력창 초기화

# ✅ 키워드 입력창 (엔터로 추가)
st.text_input("🎵 키워드 입력", key="new_keyword", placeholder="예: 감성, 사랑, 락", on_change=add_keyword)

# ✅ 현재 키워드 출력
if st.session_state.keywords:
    st.markdown("#### 📌 현재 키워드:")
    st.write(", ".join(st.session_state.keywords))
    if st.button("❌ 키워드 모두 초기화"):
        st.session_state["keywords"] = []

# ✅ 추천 버튼 눌렀을 때 처리
if st.button("🎶 추천 받기") and st.session_state.keywords:
    try:
        import openai
        # OpenAI 키 확인
        if st.secrets.get("OPENAI_API_KEY"):
            openai.api_key = st.secrets["OPENAI_API_KEY"]

            with st.spinner("AI가 음악을 추천 중입니다...🎧"):
                keywords_str = ", ".join(st.session_state["keywords"])
                prompt = f"""
                다음 키워드를 기반으로 어울리는 한국 음악 또는 팝송 3곡을 추천해줘.
                각 곡은 다음 형식으로 출력해줘:
                1. 곡 제목 - 아티스트 (YouTube 링크)
                키워드: {keywords_str}
                """
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.8
                )
                result = response.choices[0].message["content"]
                st.subheader("🎵 AI 추천 결과:")
                st.markdown(result)
                raise SystemExit  # AI 결과 있으면 백업 추천 안 함
        else:
            raise Exception("OpenAI 키 없음")
    except Exception as e:
        # 🔁 OpenAI 안 될 때 자체 추천
        st.info("⚠️ AI 추천 불가능 — 대신 자체 추천을 보여드릴게요.")
        matched = []
        for song in songs:
            if any(k.lower() in [kw.lower() for kw in st.session_state["keywords"]] for k in song["keywords"]):
                matched.append(song)

        if not matched:
            st.warning("❌ 키워드와 일치하는 노래를 찾지 못했어요.")
        else:
            st.subheader("🎵 자체 추천 결과:")
            for i, song in enumerate(matched[:3], 1):
                st.markdown(f"{i}. **{song['title']}** - {song['artist']}")
                st.video(song["youtube"])
