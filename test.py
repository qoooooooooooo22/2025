import streamlit as st
import requests
import random

# --- 페이지 설정 ---
st.set_page_config(page_title="감정 음악 추천기 (30곡 무작위)", page_icon="🎵")

# --- YouTube API 키 ---
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# --- 감정별 30곡 리스트 (완전 다른 곡, 장르 다양화) ---
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
    "이별": [
        "Someone Like You Adele", "Back to December Taylor Swift", "Ne Me Quitte Pas Jacques Brel",
        "Un-break My Heart Toni Braxton", "Tears Dry on Their Own Amy Winehouse", "All I Want Kodaline",
        "Stay Rihanna", "When I Was Your Man Bruno Mars", "Skinny Love Bon Iver",
        "Say Something A Great Big World", "Happier Ed Sheeran", "Lose You to Love Me Selena Gomez",
        "Too Good at Goodbyes Sam Smith", "Goodbye My Lover James Blunt", "Jealous Labrinth",
        "Nothing Compares 2 U Sinéad O'Connor", "Without You Mariah Carey", "Crying Roy Orbison",
        "Somebody That I Used to Know Gotye", "Blue Ain't Your Color Keith Urban", "Last Kiss Taylor Swift",
        "The Night We Met Lord Huron", "Back to Black Amy Winehouse", "I Can't Make You Love Me Bonnie Raitt",
        "Hard to Say I'm Sorry Chicago", "Everybody Hurts R.E.M.", "Lost Without You Freya Ridings",
        "All I Ask Adele", "Hello Lionel Richie"
    ],
    "집착": [
        "Every Breath You Take The Police", "Obsessed Mariah Carey", "Creep Radiohead",
        "Stalker Dua Lipa", "Possessive Ne-Yo", "Control Janet Jackson", "I Want You Savage Garden",
        "Jealous Nick Jonas", "Can't Get You Out of My Head Kylie Minogue", "Toxic Britney Spears",
        "Bad Guy Billie Eilish", "Rolling in the Deep Adele", "Black Magic Little Mix", "Problem Ariana Grande",
        "Complicated Avril Lavigne", "Boulevard of Broken Dreams Green Day", "Locked Out of Heaven Bruno Mars",
        "Shape of You Ed Sheeran", "Somebody to Love Queen", "Addicted Kelly Clarkson", "Say My Name Destiny's Child",
        "Love Me Harder Ariana Grande", "Bleeding Love Leona Lewis", "Attention Charlie Puth", "Love on the Brain Rihanna",
        "In the End Linkin Park", "Hotline Bling Drake", "Like a Stone Audioslave", "Disturbia Rihanna", "You Belong With Me Taylor Swift"
    ],
    "행복": [
        "Happy Pharrell Williams", "Walking on Sunshine Katrina & The Waves", "Can't Stop the Feeling Justin Timberlake",
        "Uptown Funk Mark Ronson ft. Bruno Mars", "Shake It Off Taylor Swift", "Good Life OneRepublic",
        "Best Day of My Life American Authors", "I'm a Believer Smash Mouth", "I'm Yours Jason Mraz",
        "Roar Katy Perry", "I Gotta Feeling Black Eyed Peas", "Don't Worry Be Happy Bobby McFerrin",
        "Good Time Owl City & Carly Rae Jepsen", "Cheerleader OMI", "Sugar Maroon 5",
        "Don't Stop Me Now Queen", "Valerie Amy Winehouse", "Can't Stop Loving You Phil Collins",
        "Send Me On My Way Rusted Root", "Firework Katy Perry", "Pocketful of Sunshine Natasha Bedingfield",
        "Love on Top Beyoncé", "Treasure Bruno Mars", "Counting Stars OneRepublic", "Dancing Queen ABBA",
        "La La La Naughty Boy", "Viva La Vida Coldplay", "Love Me Like You Do Ellie Goulding", "Domino Jessie J"
    ],
    "귀여움": [
        "Call Me Maybe Carly Rae Jepsen", "TT TWICE", "Ice Cream BLACKPINK", "DALLA DALLA ITZY",
        "Sugar Maroon 5", "Lollipop Mika", "Barbie Girl Aqua", "I'm a Gummy Bear Gummy Bear",
        "Happy Happy TWICE", "Cheer Up TWICE", "Ponyo Ponyo", "Havana Camila Cabello", "Shake It Off Taylor Swift",
        "Bubbly Colbie Caillat", "What Makes You Beautiful One Direction", "Baby Justin Bieber",
        "La La La LMFAO", "Wannabe Spice Girls", "I Like to Move It Reel 2 Real", "Friday Rebecca Black",
        "Girls Just Want to Have Fun Cyndi Lauper", "Uptown Girl Billy Joel", "Cups Anna Kendrick",
        "Hey Mickey Toni Basil", "Boom Clap Charli XCX", "I Wanna Dance with Somebody Whitney Houston",
        "I’m So Excited Pointer Sisters", "Sugar Sugar Archies", "Walking on Sunshine Katrina & The Waves",
        "Banana Pancakes Jack Johnson"
    ]
    # 나머지 감정도 같은 방식으로 30곡씩 추가 가능
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
