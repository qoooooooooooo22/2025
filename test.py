import streamlit as st

# 감정별 이모지 사전
emoji_map = {
    "사랑": "💕",
    "이별": "💔",
    "집착": "😠",
    "행복": "😆",
    "귀여움": "🐰",
    "우정": "🎉",
    "위로": "🧸",
    "추억": "🌅",
    "그리움": "🌧️",
    "슬픔": "😢"
}

# 노래 추천 목록
song_recommendations = {
    "사랑": [
        {"title": "Fake Love", "artist": "BTS", "youtube": "https://youtu.be/7C2z4GqqS5E"},
        {"title": "Love Scenario", "artist": "iKON", "youtube": "https://youtu.be/vecSVX1QYbQ"},
    ],
    "이별": [
        {"title": "이 소설의 끝을 다시 써보려 해", "artist": "한동근", "youtube": "https://youtu.be/6xBzG_C5TJU"},
        {"title": "그날처럼", "artist": "장덕철", "youtube": "https://youtu.be/a8RJZtGZFGg"},
    ],
    "집착": [
        {"title": "사랑은 늘 도망가", "artist": "임영웅", "youtube": "https://youtu.be/sA3W9J1hH9I"},
    ],
    "행복": [
        {"title": "좋은 날", "artist": "아이유", "youtube": "https://youtu.be/Q0xvVgKJxfs"},
    ],
    "귀여움": [
        {"title": "Dynamite", "artist": "BTS", "youtube": "https://youtu.be/gdZLi9oWNZg"},
    ],
    "우정": [
        {"title": "언제나 네 편", "artist": "10cm", "youtube": "https://youtu.be/tZ9OdKo7JVo"},
    ],
    "위로": [
        {"title": "밤편지", "artist": "아이유", "youtube": "https://youtu.be/BzYnNdJhZQw"},
    ],
    "추억": [
        {"title": "소녀", "artist": "오혁", "youtube": "https://youtu.be/KH6ZwnqZ7Wo"},
    ],
    "그리움": [
        {"title": "눈의 꽃", "artist": "박효신", "youtube": "https://youtu.be/wzdmhthU2tU"},
    ],
    "슬픔": [
        {"title": "비도 오고 그래서", "artist": "헤이즈", "youtube": "https://youtu.be/tQ0yjYUFKAE"},
    ]
}

# Streamlit 앱 시작
st.set_page_config(page_title="감정 음악 추천기", page_icon="🎶")

st.title("🎶 감정 키워드 기반 음악 추천기")

# 키워드 선택
keyword_options = list(emoji_map.keys())
selected_keyword = st.selectbox("당신의 감정을 선택하세요:", keyword_options)

# 선택된 감정에 맞는 이모지 출력
if selected_keyword:
    st.markdown(f"## {emoji_map[selected_keyword]} {selected_keyword} 감정에 어울리는 노래들")

    for song in song_recommendations.get(selected_keyword, []):
        st.markdown(f"**🎧 {song['title']}** - {song['artist']}")
        st.markdown(f"[YouTube에서 듣기]({song['youtube']})")

    # 감성 강조용 마무리 문구
    st.markdown("---")
    st.markdown(f"💬 감정은 음악으로 풀어요. 오늘의 감정: **{selected_keyword} {emoji_map[selected_keyword]}**")
