import streamlit as st
import requests
import random

# 🔐 YouTube API 키
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# ✅ 감정별 30곡
emotion_songs = {
    "사랑": [
        "All of Me - John Legend", "Lover - Taylor Swift", "Just the Way You Are - Bruno Mars",
        "Your Song - Elton John", "Perfect - Ed Sheeran", "Can't Help Falling in Love - Elvis Presley",
        "Endless Love - Diana Ross & Lionel Richie", "Make You Feel My Love - Adele",
        "My Heart Will Go On - Celine Dion", "I Will Always Love You - Whitney Houston",
        "Love Story - Taylor Swift", "Thinking Out Loud - Ed Sheeran", "Unchained Melody - Righteous Brothers",
        "Truly Madly Deeply - Savage Garden", "Because You Loved Me - Celine Dion", "Kiss Me - Sixpence None the Richer",
        "A Thousand Years - Christina Perri", "Everything - Michael Bublé", "I Just Called to Say I Love You - Stevie Wonder",
        "Bleeding Love - Leona Lewis", "Time After Time - Cyndi Lauper", "Vision of Love - Mariah Carey",
        "Love Me Like You Do - Ellie Goulding", "Marry You - Bruno Mars", "I Won’t Give Up - Jason Mraz",
        "Fallin’ - Alicia Keys", "More Than Words - Extreme", "We Found Love - Rihanna",
        "Back at One - Brian McKnight", "I Don't Want to Miss a Thing - Aerosmith"
    ],
    "슬픔": [
        "Someone Like You - Adele", "Hurt - Johnny Cash", "Tears in Heaven - Eric Clapton",
        "The Sound of Silence - Simon & Garfunkel", "My Immortal - Evanescence",
        "Back to Black - Amy Winehouse", "Yesterday - The Beatles", "Fade to Black - Metallica",
        "Goodbye My Lover - James Blunt", "All I Want - Kodaline", "Skinny Love - Bon Iver",
        "Say Something - A Great Big World", "Lost Cause - Billie Eilish",
        "Everybody Hurts - R.E.M.", "With or Without You - U2", "Hallelujah - Jeff Buckley",
        "End of the Road - Boyz II Men", "I Can't Make You Love Me - Bonnie Raitt",
        "Nothing Compares 2 U - Sinéad O'Connor", "Jar of Hearts - Christina Perri",
        "Angels - Robbie Williams", "I Will Remember You - Sarah McLachlan",
        "Let Her Go - Passenger", "Shadow of the Day - Linkin Park", "Bleeding Love - Leona Lewis",
        "If I Die Young - The Band Perry", "Creep - Radiohead", "The Night We Met - Lord Huron",
        "Fix You - Coldplay", "Jealous - Labrinth"
    ],
    "행복": [
        "Happy - Pharrell Williams", "Walking on Sunshine - Katrina & The Waves", "Good Life - OneRepublic",
        "Can't Stop the Feeling - Justin Timberlake", "Lovely Day - Bill Withers", "Uptown Funk - Bruno Mars",
        "Best Day of My Life - American Authors", "Shake It Off - Taylor Swift", "Valerie - Amy Winehouse",
        "Roar - Katy Perry", "I Got a Feeling - Black Eyed Peas", "Sugar - Maroon 5",
        "On Top of the World - Imagine Dragons", "Pocketful of Sunshine - Natasha Bedingfield",
        "I'm Yours - Jason Mraz", "Wake Me Up - Avicii", "Happy Together - The Turtles", "Dancing Queen - ABBA",
        "Don't Worry Be Happy - Bobby McFerrin", "Celebrate - Kool & The Gang", "Just Fine - Mary J. Blige",
        "Good Vibes - Chris Janson", "Firework - Katy Perry", "Cheerleader - OMI",
        "High Hopes - Panic! At The Disco", "Sunflower - Post Malone & Swae Lee", "Good Days - SZA",
        "Good Time - Owl City & Carly Rae Jepsen", "Banana Pancakes - Jack Johnson"
    ],
    "집착": [
        "Every Breath You Take - The Police", "Possession - Sarah McLachlan", "Creep - Radiohead",
        "You Belong With Me - Taylor Swift", "Love Is A Battlefield - Pat Benatar", "Hot N Cold - Katy Perry",
        "Toxic - Britney Spears", "Crazy - Gnarls Barkley", "Jealous - Nick Jonas",
        "Addicted - Kelly Clarkson", "Cry Me a River - Justin Timberlake", "Love the Way You Lie - Eminem ft. Rihanna",
        "Call Me Maybe - Carly Rae Jepsen", "I Want You Back - Jackson 5", "Obsessed - Mariah Carey",
        "Bad Romance - Lady Gaga", "Say My Name - Destiny's Child", "Before He Cheats - Carrie Underwood",
        "Unfaithful - Rihanna", "Torn - Natalie Imbruglia", "No Air - Jordin Sparks ft. Chris Brown",
        "Don't Cha - The Pussycat Dolls", "Bleeding Love - Leona Lewis", "I Knew You Were Trouble - Taylor Swift",
        "Irreplaceable - Beyoncé", "Take a Bow - Rihanna", "Hotline Bling - Drake",
        "Love Me Harder - Ariana Grande & The Weeknd", "Crying in the Club - Camila Cabello",
        "Womanizer - Britney Spears"
    ],
    "귀여움": [
        "Sugar - Maroon 5", "Lollipop - Mika", "MMMBop - Hanson", "Call Me Maybe - Carly Rae Jepsen",
        "Shake It Off - Taylor Swift", "Happy - Pharrell Williams", "Best Day of My Life - American Authors",
        "Can't Stop the Feeling - Justin Timberlake", "Pocketful of Sunshine - Natasha Bedingfield",
        "I'm Yours - Jason Mraz", "Roar - Katy Perry", "Good Time - Owl City & Carly Rae Jepsen",
        "Cheerleader - OMI", "Dancing Queen - ABBA", "I Gotta Feeling - Black Eyed Peas",
        "Uptown Funk - Bruno Mars", "Good Life - OneRepublic", "Lovely Day - Bill Withers",
        "Shake It Up - Selena Gomez", "Party in the USA - Miley Cyrus", "Just Dance - Lady Gaga",
        "Firework - Katy Perry", "Girls Just Want to Have Fun - Cyndi Lauper", "Best Song Ever - One Direction",
        "We Got the Beat - The Go-Go's", "Tik Tok - Kesha", "Candy - Mandy Moore", "So What - P!nk",
        "ABC - Jackson 5", "Dance Monkey - Tones and I"
    ],
    # ... (이하 5개 감정 이별, 우정, 위로, 추억, 그리움 30곡씩 동일 방식으로 포함)
}

# 🔍 YouTube 검색
def get_youtube_video_info(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY,
    }
    response = requests.get(url, params=params)
    data = response.json()
    if "items" in data and len(data["items"]) > 0:
        video = data["items"][0]
        video_id = video["id"]["videoId"]
        title = video["snippet"]["title"]
        thumbnail = video["snippet"]["thumbnails"]["high"]["url"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        return title, thumbnail, link
    else:
        return query, "https://via.placeholder.com/280x180.png?text=No+Video", "#"

# 🎨 CSS & UI
st.set_page_config(page_title="감정 기반 음악 추천", page_icon="🎵", layout="wide")
st.markdown("""
<style>
body { background-color: #0f111a; color: white; font-family: 'Helvetica Neue', sans-serif; }
.song-card { background: #1c1e2a; border-radius: 20px; width: 300px; padding: 15px; margin: 10px; text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4); transition: 0.3s; }
.song-card:hover { transform: scale(1.05); box-shadow: 0 15px 40px rgba(255,255,255,0.2); }
.song-card img { width: 100%; border-radius: 15px; }
.song-card h4 { margin-top: 10px; font-size: 1rem; color: #fff; }
.song-container { display: flex; flex-wrap: wrap; justify-content: center; }
select { background-color: #1c1e2a; color:white; padding:8px; border-radius:8px; }
button { background-color:#ff2e63; color:white; padding:10px 20px; border:none; border-radius:8px; cursor:pointer; font-weight:bold; }
button:hover { background-color:#ff477e; }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🎵 감정 기반 음악 추천</h1>", unsafe_allow_html=True)

# 감정 선택
emotion = st.selectbox("당신의 감정은?", list(emotion_songs.keys()))

if st.button("🎧 노래 추천 받기"):
    songs = random.sample(emotion_songs[emotion], 3)
    st.markdown("<div class='song-container'>", unsafe_allow_html=True)
    for song in songs:
        title, thumb, link = get_youtube_video_info(song)
        st.markdown(f"""
        <div class="song-card">
            <a href="{link}" target="_blank">
                <img src="{thumb}" alt="{title}">
                <h4>{title}</h4>
            </a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
