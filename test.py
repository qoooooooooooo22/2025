import streamlit as st
import requests
import openai

# --- 페이지 설정 ---
st.set_page_config(page_title="감정 음악 추천기", page_icon="🎵")

# --- API 키 (발급받은 것 넣기) ---
OPENAI_API_KEY = "sk-너의_sk-proj-XcKM61aLZBUULIDzZ8jpM2vlEQXleCh1hFoydKz2cCmf76Ur_-YazZ_-bcywVq4MqthEzOxfOIT3BlbkFJgp8PLt_zIus7JB3bWdtNLce3FkHqF-P0J8rOpNpXzqHuTrfCONF32z81IiucdopIDkyR5XUpYA"   # 💡 공백 없게 붙여넣기
YOUTUBE_API_KEY = "여기_너의_YouTube_API_키"  # 💡 공백 없게 붙여넣기

# --- 감정 이모지 ---
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

# --- GPT로 노래 추천 ---
def generate_song_recommendations(emotion, api_key):
    openai.api_key = api_key
    prompt = f"""
    당신은 감정에 맞는 노래를 추천하는 전문가입니다.
    감정: {emotion}
    이 감정에 맞는 한국 대중가요 3곡을 '제목 - 가수' 형식으로 추천해주세요.
    유튜브에서 쉽게 찾을 수 있는 노래로 해주세요.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        reply = response.choices[0].message["content"]
        return [line.strip() for line in reply.strip().split("\n") if line.strip()]
    except Exception as e:
        st.error(f"GPT 오류 발생: {e}")
        return []

# --- YouTube 검색 ---
def search_youtube_video(api_key, query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": api_key
    }
    resp = requests.get(url, params=params)
    results = resp.json()
    if "items" in results and len(results["items"]) > 0:
        vid = results["items"][0]
        vid_id = vid["id"]["videoId"]
        title = vid["snippet"]["title"]
        thumb = vid["snippet"]["thumbnails"]["high"]["url"]
        url = f"https://www.youtube.com/watch?v={vid_id}"
        return {"title": title, "url": url, "thumbnail": thumb}
    return None

# --- UI ---
st.title("🎶 감정 키워드 기반 음악 추천기 (GPT + YouTube)")

selected_emotion = st.selectbox("오늘 당신의 감정은?", list(emoji_map.keys()))
emoji = emoji_map.get(selected_emotion, "")

if st.button("🎧 AI 추천곡 받아보기"):
    with st.spinner("AI가 추천곡을 찾는 중..."):
        songs = generate_song_recommendations(selected_emotion, OPENAI_API_KEY)

    if songs:
        st.markdown(f"## {emoji} {selected_emotion} 감정에 어울리는 노래들")
        for song in songs:
            yt = search_youtube_video(YOUTUBE_API_KEY, song)
            if yt:
                st.image(yt["thumbnail"], use_container_width=True)
                st.markdown(f"**🎵 {yt['title']}**")
                st.markdown(f"[📺 YouTube에서 보기]({yt['url']})")
                st.markdown("---")
            else:
                st.warning(f"🔍 '{song}' 영상 못 찾음")
    else:
        st.error("노래 추천을 가져오지 못했어요. 다시 시도하세요.")
