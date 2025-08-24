import streamlit as st
import requests

# --- 페이지 설정 ---
st.set_page_config(page_title="감정 음악 추천기 (무료 안정화)", page_icon="🎵")

# --- YouTube API 키 ---
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# --- 감정별 노래 추천 ---
emotion_songs = {
    "사랑": ["Fake Love 방탄소년단", "사랑했나봐 윤도현", "첫눈처럼 너에게 가겠다 에일리"],
    "이별": ["눈의 꽃 박효신", "이별택시 멜로망스", "안녕 폴킴"],
    "집착": ["HOT HOT", "미쳐 싸이", "어쩌면 좋아 장범준"],
    "행복": ["좋은 날 아이유", "Dynamite 방탄소년단", "LALISA 리사"],
    "귀여움": ["TT 트와이스", "Ice Cream BLACKPINK", "DALLA DALLA ITZY"],
    "우정": ["우정의 노래 트와이스", "우리가 만난 기적 에픽하이", "친구라도 될 걸 그랬어 볼빨간사춘기"],
    "위로": ["그대라는 사치 한동근", "위로 윤하", "걱정말아요 그대 이적"],
    "추억": ["벚꽃 엔딩 버스커 버스커", "너의 의미 아이유", "봄날 방탄소년단"],
    "그리움": ["밤편지 아이유", "Missing You BTOB", "보고싶다 김범수"],
    "슬픔": ["눈물의 이유 윤미래", "사랑비 김태우", "어른 소유"]
}

emoji_map = {
    "사랑": "💕", "이별": "💔", "집착": "😠", "행복": "😆", "귀여움": "🐰",
    "우정": "🎉", "위로": "🧸", "추억": "🌅", "그리움": "🌧️", "슬픔": "😢"
}

# --- YouTube 검색 안정화 ---
def search_youtube_video(api_key, query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 5,  # 여러 개 가져와서 정확도 높임
        "key": api_key
    }
    resp = requests.get(url, params=params)
    results = resp.json()
    if "items" in results:
        for vid in results["items"]:
            vid_id = vid["id"]["videoId"]
            title = vid["snippet"]["title"]
            thumb = vid["snippet"]["thumbnails"]["high"]["url"]
            url = f"https://www.youtube.com/watch?v={vid_id}"
            # 제목에 검색어 일부라도 포함되면 반환
            if query.split()[0].lower() in title.lower():
                return {"title": title, "url": url, "thumbnail": thumb}
    return None

# --- UI ---
st.title("🎶 감정 키워드 기반 음악 추천기 (무료 안정화)")

selected_emotion = st.selectbox("오늘 당신의 감정은?", list(emotion_songs.keys()))
emoji = emoji_map.get(selected_emotion, "")

if st.button("🎧 추천곡 보기"):
    st.markdown(f"## {emoji} {selected_emotion} 감정에 어울리는 노래들")
    for song in emotion_songs[selected_emotion]:
        yt = search_youtube_video(YOUTUBE_API_KEY, song)
        if yt:
            st.image(yt["thumbnail"], use_container_width=True)
            st.markdown(f"**🎵 {yt['title']}**")
            st.markdown(f"[📺 YouTube에서 보기]({yt['url']})")
            st.markdown("---")
        else:
            st.warning(f"🔍 '{song}' 영상 못 찾음")
