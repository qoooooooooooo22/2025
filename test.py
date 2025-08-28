import streamlit as st
import requests
import random

# 🔐 YouTube API 키
YOUTUBE_API_KEY = "AIzaSyBLuzIZRaRKshJJkGClpLDrPB55F0ETfVo"

# ✅ 감정별 30곡 (팝, 재즈, K-pop 등 다양)
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
    "이별": [
        "Someone Like You - Adele", "Back to December - Taylor Swift", "Un-break My Heart - Toni Braxton",
        "Nothing Compares 2 U - Sinéad O'Connor", "Stay - Rihanna", "Let Her Go - Passenger",
        "When I Was Your Man - Bruno Mars", "All I Want - Kodaline", "Say Something - A Great Big World",
        "Too Good at Goodbyes - Sam Smith", "Goodbye My Lover - James Blunt", "The Night We Met - Lord Huron",
        "If I Die Young - The Band Perry", "Creep - Radiohead", "Fix You - Coldplay", "Bleeding Love - Leona Lewis",
        "I Will Always Love You - Whitney Houston", "Jealous - Labrinth", "Lost Without You - Freya Ridings",
        "Almost Lover - A Fine Frenzy", "Don't Speak - No Doubt", "Hard to Say I'm Sorry - Chicago",
        "Right Here Waiting - Richard Marx", "Somebody That I Used to Know - Gotye", "Hurt - Christina Aguilera",
        "Love Yourself - Justin Bieber", "Cry Me a River - Justin Timberlake", "Against All Odds - Phil Collins",
        "Too Little Too Late - JoJo", "Back at One - Brian McKnight"
    ],
    "우정": [
        "Count on Me - Bruno Mars", "Lean on Me - Bill Withers", "With a Little Help from My Friends - The Beatles",
        "I'll Be There for You - The Rembrandts", "You've Got a Friend - Carole King", "Umbrella - Rihanna ft. Jay-Z",
        "We Are Young - Fun ft. Janelle Monáe", "Best Friend - Saweetie", "Graduation (Friends Forever) - Vitamin C",
        "Stand by Me - Ben E. King", "Walking on Sunshine - Katrina & The Waves", "Happy - Pharrell Williams",
        "Good Time - Owl City & Carly Rae Jepsen", "Count on Me - Whitney Houston", "That's What Friends Are For - Dionne Warwick",
        "Hold My Hand - Jess Glynne", "Girls Just Want to Have Fun - Cyndi Lauper", "Shake It Off - Taylor Swift",
        "Dynamite - BTS", "On Top of the World - Imagine Dragons", "We Belong Together - Mariah Carey",
        "You’ve Got a Friend in Me - Randy Newman", "True Colors - Cyndi Lauper", "Ain't No Mountain High Enough - Marvin Gaye & Tammi Terrell",
        "One Call Away - Charlie Puth", "I'll Be There - Jackson 5", "Lean On Me - Club Nouveau", "Friend Like Me - Robin Williams",
        "Walking on Sunshine - Aly & AJ", "Count on Me - Bruno Mars"
    ],
    "위로": [
        "Fix You - Coldplay", "Lean on Me - Bill Withers", "Bridge Over Troubled Water - Simon & Garfunkel",
        "Everybody Hurts - R.E.M.", "True Colors - Cyndi Lauper", "I Will Remember You - Sarah McLachlan",
        "Heal the World - Michael Jackson", "Let It Be - The Beatles", "Don't Give Up - Peter Gabriel & Kate Bush",
        "Rise Up - Andra Day", "Stronger - Kelly Clarkson", "Fight Song - Rachel Platten", "You've Got a Friend - James Taylor",
        "Beautiful - Christina Aguilera", "Carry On - Fun", "Somewhere I Belong - Linkin Park", "Man in the Mirror - Michael Jackson",
        "Here Comes the Sun - The Beatles", "Unwritten - Natasha Bedingfield", "Roar - Katy Perry", "Eye of the Tiger - Survivor",
        "Shake It Off - Taylor Swift", "Happy - Pharrell Williams", "Brave - Sara Bareilles", "We Are the Champions - Queen",
        "Ain't No Mountain High Enough - Marvin Gaye & Tammi Terrell", "Count on Me - Bruno Mars",
        "Don't Stop Believin' - Journey", "What a Wonderful World - Louis Armstrong", "Walking on Sunshine - Katrina & The Waves"
    ],
    "추억": [
        "Summer of '69 - Bryan Adams", "Wake Me Up When September Ends - Green Day", "Photograph - Ed Sheeran",
        "Time After Time - Cyndi Lauper", "The Nights - Avicii", "Memories - Maroon 5", "Yesterday - The Beatles",
        "Good Riddance (Time of Your Life) - Green Day", "September - Earth, Wind & Fire", "I Gotta Feeling - Black Eyed Peas",
        "My Way - Frank Sinatra", "Viva La Vida - Coldplay", "Castle on the Hill - Ed Sheeran", "Graduation - Vitamin C",
        "Sweet Child O' Mine - Guns N' Roses", "Take Me Home, Country Roads - John Denver", "I Will Remember You - Sarah McLachlan",
        "Don't Stop Believin' - Journey", "Fast Car - Tracy Chapman", "Brown Eyed Girl - Van Morrison", "Hotel California - Eagles",
        "Stairway to Heaven - Led Zeppelin", "Bohemian Rhapsody - Queen", "Imagine - John Lennon", "Landslide - Fleetwood Mac",
        "Time in a Bottle - Jim Croce", "We Are Young - Fun", "Photograph - Nickelback", "Drive - Incubus", "The Scientist - Coldplay"
    ],
    "그리움": [
        "Missing - Everything But The Girl", "I Miss You - Blink-182", "Far Away - Nickelback",
        "Someone Like You - Adele", "Need You Now - Lady A", "Right Here Waiting - Richard Marx",
        "Unchained Melody - Righteous Brothers", "All by Myself - Celine Dion", "When You Say Nothing at All - Ronan Keating",
        "If I Ain't Got You - Alicia Keys", "Back to December - Taylor Swift", "The Night We Met - Lord Huron",
        "My Heart Will Go On - Celine Dion", "Stay - Rihanna", "Say You Love Me - Jessie Ware",
        "Jealous - Labrinth", "I Can't Make You Love Me - Bonnie Raitt", "Lost Without You - Freya Ridings",
        "Too Good at Goodbyes - Sam Smith", "Bleeding Love - Leona Lewis", "All I Want - Kodaline",
        "Tears Dry on Their Own - Amy Winehouse", "How to Save a Life - The Fray", "Someone You Loved - Lewis Capaldi",
        "Nothing Compares 2 U - Sinéad O'Connor", "Creep - Radiohead", "Hurt - Johnny Cash",
        "Fix You - Coldplay", "Say Something - A Great Big World", "Almost Lover - A Fine Frenzy"
    ]
}


# YouTube 검색
def get_youtube_video_info(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {"part": "snippet", "q": query, "type": "video", "maxResults": 1, "key": YOUTUBE_API_KEY}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return query, "https://via.placeholder.com/450.png?text=No+Video", "#"
    data = response.json()
    try:
        video = data["items"][0]
        video_id = video["id"]["videoId"]
        title = video["snippet"]["title"]
        thumbnail = video["snippet"]["thumbnails"]["high"]["url"]
        link = f"https://www.youtube.com/watch?v={video_id}"
        return title, thumbnail, link
    except:
        return query, "https://via.placeholder.com/450.png?text=No+Video", "#"

# 페이지 설정
st.set_page_config(page_title="Mood Music Recommender", page_icon="🎵", layout="wide")

# CSS 디자인
st.markdown("""
<style>
body { background: linear-gradient(135deg, #0f111a 0%, #1a1c2a 100%); color: white; font-family: 'Helvetica Neue', sans-serif; scroll-behavior: smooth; }
select { background-color: #1c1e2a; color:white; padding:12px; border-radius:10px; margin:10px; font-size:1rem; }
button { background-color:#ff2e63; color:white; padding:12px 24px; border:none; border-radius:10px; cursor:pointer; font-weight:bold; margin-left:10px; font-size:1rem; transition:0.3s;}
button:hover { background-color:#ff477e; transform: scale(1.05); }
h1 { text-align:center; margin-bottom:40px; font-size:3rem; color:#ff477e; text-shadow: 2px 2px 10px rgba(0,0,0,0.7); }

.song-container { display:flex; flex-wrap:wrap; justify-content:center; padding-bottom:50px; scroll-snap-type: y mandatory; }
.song-card { background: #1f2130; border-radius: 25px; width: 450px; padding: 20px; margin: 20px; text-align:center;
             box-shadow: 0 10px 30px rgba(0,0,0,0.5); transition: transform 0.6s ease, opacity 0.6s ease; scroll-snap-align: start; opacity:1; transform: translateY(0);}
.song-card:hover { transform: scale(1.05); box-shadow: 0 20px 50px rgba(255,71,126,0.4); }

.song-card img { width: 400px; height: 400px; object-fit: cover; border-radius: 20px; display: block; margin-left: auto; margin-right: auto; }
.song-card h4 { margin-top:15px; font-size:1.2rem; color:#fff; font-weight:bold; }

.section { padding:50px 0; }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown("<h1>Mood Music Recommender</h1>", unsafe_allow_html=True)

# 감정 선택
emotion = st.selectbox("Choose your mood:", list(emotion_songs.keys()))

# 추천 버튼
if st.button("🎧 Get Recommendations"):
    songs = random.sample(emotion_songs[emotion], 3)
    st.markdown("<section class='section'><div class='song-container'>", unsafe_allow_html=True)
    for song in songs:
        title, thumb, link = get_youtube_video_info(song)
        # 🔹 디버깅 출력
        st.write(f"Title: {title}, Link: {link}, Thumbnail: {thumb}")
        st.markdown(f"""
        <div class="song-card">
            <a href="{link}" target="_blank">
                <img src="{thumb}" alt="{title}">
                <h4>{title}</h4>
            </a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></section>", unsafe_allow_html=True)
