import streamlit as st
import requests
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="감정 음악 추천기 (무료+무작위)", page_icon="🎵")

# --- YouTube API 키 ---
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# --- 감정별 노래 리스트 (장르 다양화) ---
emotion_songs = {
    "사랑": [
        "All of Me John Legend", "Just the Way You Are Bruno Mars", "Fly Me to the Moon Frank Sinatra",
        "Lover Taylor Swift", "Your Song Elton John", "At Last Etta James"
    ],
    "이별": [
        "Someone Like You Adele", "Back to December Taylor Swift", "Ne Me Quitte Pas Jacques Brel",
        "Un-break My Heart Toni Braxton", "Tears Dry on Their Own Amy Winehouse"
    ],
    "집착": [
        "Every Breath You Take The Police", "Obsessed Mariah Carey", "Creep Radiohead"
    ],
    "행복": [
        "Happy Pharrell Williams", "Walking on Sunshine Katrina & The Waves", "Can't Stop the Feeling Justin Timberlake"
    ],
    "귀여움": [
        "Sugar Maroon 5", "Call Me Maybe Carly Rae Jepsen", "Shake It Off Taylor Swift"
    ],
    "우정": [
        "Lean On Me Bill Withers", "Count on Me Bruno Mars", "With a Little Help From My Friends The Beatles"
    ],
    "위로": [
        "Fix You Coldplay", "Stand By Me Ben E. King", "Hallelujah Jeff Buckley"
    ],
    "추억": [
        "Yesterday The Beatles", "Summer of '69 Bryan Adams", "Viva La Vida Coldplay"
    ],
    "그리움": [
        "I Will Remember You Sarah McLachlan", "Somewhere I Belong Linkin Park", "Photograph Ed Sheeran"
    ],
    "슬픔": [
        "Mad World Gary Jules", "The Sound of Silence Simon & Garfunkel", "Everybody Hurts R.E.M."
    ]
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
        "maxResults": 5,  # 여러 영상 가져오기
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
            if query.split()[0].lower() in title.lower():  # 검색어 일부 포함
                return {"title": title, "url": url, "thumbnail": thumb}
    return None

# --- UI ---
st.title("🎶 감정 키워드 기반 음악 추천기 (무료+무작위)")

selected_emotion = st.selectbox("오늘 당신의 감정은?", list(emotion_songs.keys()))
emoji = emoji_map.get(selected_emotion, "")

if st.button("🎧 추천곡 보기"):
    st.markdown(f"## {emoji} {selected_emotion} 감정에 어울리는 노래들")

    # --- 무작위 추천: 감정 리스트에서 3곡 선택 ---
    songs = random.sample(emotion_songs[selected_emotion], k=min(3, len(emotion_songs[selected_emotion])))

    for song in songs:
        yt = search_youtube_video(YOUTUBE_API_KEY, song)
        if yt:
            st.image(yt["thumbnail"], use_container_width=True)
            st.markdown(f"**🎵 {yt['title']}**")
            st.markdown(f"[📺 YouTube에서 보기]({yt['url']})")
            st.markdown("---")
        else:
            st.warning(f"🔍 '{song}' 영상 못 찾음")
