import streamlit as st

# 샘플 노래 데이터베이스
songs = [
    {"title": "밤편지", "artist": "아이유", "keywords": ["감성", "발라드"], "youtube": "https://www.youtube.com/watch?v=-2wMByiPrUE"},
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "keywords": ["락", "감성"], "youtube": "https://www.youtube.com/watch?v=12345"},
    {"title": "Dynamite", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Love Poem", "artist": "아이유", "keywords": ["감성", "사랑", "발라드"], "youtube": "https://www.youtube.com/watch?v=abcde"},
    {"title": "Permission to Dance", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=xyz12"},
]

st.set_page_config(page_title="🎵 음악 추천기", page_icon="🎧")
st.title("🎤 키워드 기반 노래 추천기 (YouTube 재생 포함)")

# 세션 상태 초기화
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "new_keyword" not in st.session_state:
    st.session_state["new_keyword"] = []

# 키워드 추가 함수
def add_keyword():
    kw = st.session_state.new_keyword.strip()
    if kw and kw not in st.session_state.keywords:
        st.session_state.keywords.append(kw)
    st.session_state.new_keyword = ""

# 키워드 입력
st.text_input("🎵 키워드 입력", key="new_keyword", placeholder="예: 감성, 사랑, 락", on_change=add_keyword)

# 현재 키워드 출력
if st.session_state.keywords:
    st.markdown("#### 📌 현재 키워드:")
    st.write(", ".join(st.session_state.keywords))
    if st.button("❌ 키워드 모두 초기화"):
        st.session_state.keywords = []

# 추천 버튼
if st.button("🎶 추천 받기") and st.session_state.keywords:
    matched = []
    for song in songs:
        if any(k.lower() in [kw.lower() for kw in st.session_state.keywords] for k in song["keywords"]):
            matched.append(song)
    if not matched:
        st.info("🔍 입력한 키워드와 매칭되는 노래가 없습니다.")
    else:
        st.subheader("🎵 추천 결과:")
        for i, song in enumerate(matched[:3], 1):
            st.markdown(f"{i}. **{song['title']}** - {song['artist']}")
            # YouTube 영상 바로 재생
            st.video(song["youtube"])
