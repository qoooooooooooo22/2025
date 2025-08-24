import streamlit as st
import requests

# --- 설정 ---
st.set_page_config(page_title="감정 음악 추천기", page_icon="🎶")

# --- YouTube API 키 ---
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# --- 감정 → 이모지 맵 ---
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

# --- 감정 → 추천곡 (제목 + 아티스트) ---
emotion_songs = {
    "사랑": ["Fake Love BTS", "Love Scenario iKON"],
    "이별": ["이 소설의 끝을 다시 써보려 해 한동근", "그날처럼 장덕철"],
    "집착": ["사랑은 늘 도망가 임영웅"],
    "행복": ["좋은 날 아이유"],
    "귀여움": ["Dynamite BTS"],
    "우정": ["언제나 네 편 10cm"],
    "위로": ["밤편지 아이유"],
    "추억": ["소녀 오혁"],
    "그리움": ["눈의 꽃 박효신"],
    "슬픔": ["비도 오고 그래서 헤이즈"]
}

# --- YouTube 검색 함수 ---
def search_youtube_video(api_key, query):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": api_key
    }
    response = requests.get(search_url, params=params)
    results = response.json()

    if "items" in results and len(results["items"]) > 0:
        video = results["items"][0]
        video_id = video["id"]["videoId"]
        title = video["snippet"]["title"]
        thumbnail = video["snippet"]["thumbnails"]["high"]["url"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        return {"title": title, "url": video_url, "thumbnail": thumbnail}
    else:
        return None

# --- 앱 제목 ---
st.title("🎶 감정 키워드 기반 음악 추천기")

# --- 감정 선택 ---
selected_emotion = st.selectbox("오늘 당신의 감정은?", list(emoji_map.keys()))

if selected_emotion:
    emoji = emoji_map[selected_emotion]
    st.markdown(f"## {emoji} {selected_emotion} 감정에 어울리는 노래들")

    songs = emotion_songs.get(selected_emotion, [])
    for song in songs:
        result = search_youtube_video(YOUTUBE_API_KEY, song)
        if result:
            st.image(result["thumbnail"], use_column_width=True)
            st.markdown(f"**🎵 {result['title']}**")
            st.markdown(f"[📺 YouTube에서 보기]({result['url']})")
            st.markdown("---")
        else:
            st.write("😢 해당 노래의 영상을 찾을 수 없습니다.")
