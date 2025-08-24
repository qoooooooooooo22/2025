import streamlit as st
import requests
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="감정 음악 추천기 (30곡 무작위)", page_icon="🎵")

# --- YouTube API 키 ---
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# --- 감정별 30곡 리스트 예시 (다양한 장르 포함) ---
emotion_songs = {
    "사랑": [
        "All of Me John Legend", "Just the Way You Are Bruno Mars", "Fly Me to the Moon Frank Sinatra",
        "Lover Taylor Swift", "Your Song Elton John", "At Last Etta James",
        "Perfect Ed Sheeran", "Can't Help Falling in Love Elvis Presley", "Endless Love Diana Ross & Lionel Richie",
        "Make You Feel My Love Adele", "Something The Beatles", "When I Fall in Love Nat King Cole",
        "My Heart Will Go On Celine Dion", "I Will Always Love You Whitney Houston", "Love Story Taylor Swift",
        "Thinking Out Loud Ed Sheeran", "How Deep Is Your Love Bee Gees", "Unchained Melody The Righteous Brothers",
        "All My Life K-Ci & JoJo", "Because You Loved Me Celine Dion", "A Thousand Years Christina Perri",
        "Vision of Love Mariah Carey", "Everything Michael Bublé", "I Just Called to Say I Love You Stevie Wonder",
        "Truly Madly Deeply Savage Garden", "Bleeding Love Leona Lewis", "Time After Time Cyndi Lauper",
        "Endless Love Luther Vandross", "Kiss Me Sixpence None the Richer"
    ],
    # 다른 감정도 비슷하게 30곡 정도 추가
    "이별": ["Someone Like You Adele", "Back to December Taylor Swift", "Ne Me Quitte Pas Jacques Brel",
            "Un-break My Heart Toni Braxton", "Tears Dry on Their Own Amy Winehouse"] * 6,  # 임시 반복
    "집착": ["Every Breath You Take The Police", "Obsessed Mariah Carey", "Creep Radiohead"] * 10,
    "행복": ["Happy Pharrell Williams", "Walking on Sunshine Katrina & The Waves", "Can't Stop the Feeling Justin Timberlake"] * 10,
    "귀여움": ["Sugar Maroon 5", "Call Me Maybe Carly Rae Jepsen", "Shake It Off Taylor Swift"] * 10,
    "우정": ["Lean On Me Bill Withers", "Count on Me Bruno Mars", "With a Little Help From My Friends The Beatles"] * 10,
    "위로": ["Fix You Coldplay", "Stand By Me Ben E. King", "Hallelujah Jeff Buckley"] * 10,
    "추억": ["Yesterday The Beatles", "Summer of '69 Bryan Adams', 'Viva La Vida Coldplay"] * 10,
    "그리움": ["I Will Remember You Sarah McLachlan", "Somewhere I Belong Linkin Park", "Photograph Ed Sheeran"] * 10,
    "슬픔": ["Mad World Gary Jules", "The Sound of Silence Simon & Garfunkel", "Everybody Hurts R.E.M."] * 10
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
        "maxResults": 5,
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
            if query.split()[0].lower() in title.lower():
                return {"title": title, "url": url, "thumbnail": thumb}
    return None

# --- UI ---
st.title("🎶 감정 키워드 기반 음악 추천기 (30곡 무작위)")

selected_emotion = st.selectbox("오늘 당신의 감정은?", list(emotion_songs.keys()))
emoji = emoji_map.get(selected_emotion, "")

if st.button("🎧 추천곡 보기"):
    st.markdown(f"## {emoji} {selected_emotion} 감정에 어울리는 노래들")

    # --- 무작위 추천: 감정 리스트에서 3곡 선택 ---
    songs = random.sample(emotion_songs[selected_emotion], k=3)

    for song in songs:
        yt = search_youtube_video(YOUTUBE_API_KEY, song)
        if yt:
            st.image(yt["thumbnail"], use_container_width=True)
            st.markdown(f"**🎵 {yt['title']}**")
            st.markdown(f"[📺 YouTube에서 보기]({yt['url']})")
            st.markdown("---")
        else:
            st.warning(f"🔍 '{song}' 영상 못 찾음")
