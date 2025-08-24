import streamlit as st
import streamlit.components.v1 as components
import random
import urllib.parse

st.set_page_config(page_title="Emotion Music", page_icon="🎵", layout="wide")

st.markdown("""
<style>
body {background-color:#0f111a; color:#fff; font-family:'Inter', sans-serif;}
h2 {color:#ff4081;}
button, select {background:#1e1e2f; color:#fff; border:none; padding:12px 20px; margin:10px; border-radius:12px; cursor:pointer; transition:0.3s;}
button:hover, select:hover {background:#ff4081; color:#000;}
.song-card {background:#222236; border-radius:20px; padding:20px; width:260px; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.5); transition:0.3s;}
.song-card:hover {transform:scale(1.05) rotate(-1deg); box-shadow:0 15px 35px rgba(255,64,129,0.6);}
.song-card img {width:100%; border-radius:15px;}
.song-card h3 {margin-top:10px; font-size:1.2rem; font-weight:700;}
</style>
""", unsafe_allow_html=True)

# 감정별 30곡 리스트 (샘플)
emotion_songs = {
    "사랑": ["All of Me John Legend","Just the Way You Are Bruno Mars","Fly Me to the Moon Frank Sinatra","Lover Taylor Swift","Your Song Elton John","At Last Etta James","Perfect Ed Sheeran","Can't Help Falling in Love Elvis Presley","Endless Love Diana Ross & Lionel Richie","Make You Feel My Love Adele","Something The Beatles","When I Fall in Love Nat King Cole","My Heart Will Go On Celine Dion","I Will Always Love You Whitney Houston","Love Story Taylor Swift","Thinking Out Loud Ed Sheeran","How Deep Is Your Love Bee Gees","Unchained Melody The Righteous Brothers","All My Life K-Ci & JoJo","Because You Loved Me Celine Dion","A Thousand Years Christina Perri","Vision of Love Mariah Carey","Everything Michael Bublé","I Just Called to Say I Love You Stevie Wonder","Truly Madly Deeply Savage Garden","Bleeding Love Leona Lewis","Time After Time Cyndi Lauper","Endless Love Luther Vandross","Kiss Me Sixpence None the Richer"],
    "슬픔": ["Someone Like You Adele","Hurt Johnny Cash","Tears Dry on Their Own Amy Winehouse","Everybody Hurts R.E.M.","Nothing Compares 2 U Sinéad O'Connor","Creep Radiohead","The Sound of Silence Simon & Garfunkel","My Immortal Evanescence","Back to Black Amy Winehouse","Yesterday The Beatles","Fade to Black Metallica","Goodbye My Lover James Blunt","All I Want Kodaline","Skinny Love Bon Iver","I Will Always Love You Whitney Houston","Jar of Hearts Christina Perri","Say Something A Great Big World","Lost Cause Billie Eilish","Everybody's Got to Learn Sometime The Korgis","With or Without You U2","Hallelujah Jeff Buckley","End of the Road Boyz II Men","I Can't Make You Love Me Bonnie Raitt","Nothing Else Matters Metallica","One Last Time Ariana Grande","Bleeding Love Leona Lewis","Angels Robbie Williams","Yesterday Once More Carpenters","Don't Speak No Doubt"],
    "행복": ["Happy Pharrell Williams","Walking on Sunshine Katrina & The Waves","Good Life OneRepublic","Can't Stop the Feeling Justin Timberlake","Lovely Day Bill Withers","Uptown Funk Mark Ronson ft. Bruno Mars","Best Day of My Life American Authors","Shake It Off Taylor Swift","Valerie Amy Winehouse","Roar Katy Perry","I Got a Feeling Black Eyed Peas","Sugar Maroon 5","On Top of the World Imagine Dragons","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Wake Me Up Avicii","Happy Together The Turtles","Dancing Queen ABBA","Don't Worry Be Happy Bobby McFerrin","Good Morning Sunshine Lenka","Celebrate Kool & The Gang","Just Fine Mary J. Blige","Can't Stop Loving You Phil Collins","Lovely Justin Bieber","Best Song Ever One Direction","Good Time Owl City & Carly Rae Jepsen","Shut Up and Dance Walk The Moon","Cheerleader OMI","Sugar Baby Maroon 5","Good Vibes Chris Janson"],
    "집착": ["Every Breath You Take The Police","Possession Sarah McLachlan","Creep Radiohead","You Belong With Me Taylor Swift","Love Is A Battlefield Pat Benatar","Hot N Cold Katy Perry","Toxic Britney Spears","Crazy Gnarls Barkley","Jealous Nick Jonas","Addicted Kelly Clarkson","Cry Me a River Justin Timberlake","Love the Way You Lie Eminem ft. Rihanna","Call Me Maybe Carly Rae Jepsen","I Want You Back Jackson 5","Obsessed Mariah Carey","Bad Romance Lady Gaga","Say My Name Destiny's Child","Before He Cheats Carrie Underwood","Unfaithful Rihanna","Torn Natalie Imbruglia","No Air Jordin Sparks ft. Chris Brown","Don't Cha The Pussycat Dolls","Every Little Thing She Does Is Magic The Police","Cry Kelly Clarkson","Bleeding Love Leona Lewis","I Knew You Were Trouble Taylor Swift","Irreplaceable Beyoncé","Take a Bow Rihanna","Hotline Bling Drake","Love Me Harder Ariana Grande & The Weeknd"],
    "귀여움": ["Sugar Maroon 5","Lollipop Mika","MMMBop Hanson","Call Me Maybe Carly Rae Jepsen","Shake It Off Taylor Swift","Happy Pharrell Williams","Best Day of My Life American Authors","Can't Stop the Feeling Justin Timberlake","Walking on Sunshine Katrina & The Waves","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Roar Katy Perry","Good Time Owl City & Carly Rae Jepsen","Cheerleader OMI","Dancing Queen ABBA","I Gotta Feeling Black Eyed Peas","Uptown Funk Mark Ronson ft. Bruno Mars","Good Life OneRepublic","Lovely Day Bill Withers","Shake It Up Selena Gomez","Party in the USA Miley Cyrus","Sugar Baby Maroon 5","Just Dance Lady Gaga","Firework Katy Perry","I Love It Icona Pop","Girls Just Want to Have Fun Cyndi Lauper","Best Song Ever One Direction","We Got the Beat The Go-Go's","Tik Tok Kesha","Candy Mandy Moore"],
    "이별": ["Someone Like You Adele","Back to December Taylor Swift","Un-break My Heart Toni Braxton","My Heart Will Go On Celine Dion","Bleeding Love Leona Lewis","I Will Always Love You Whitney Houston","Goodbye My Lover James Blunt","End of the Road Boyz II Men","Tears Dry on Their Own Amy Winehouse","Don't Speak No Doubt","All I Want Kodaline","Without You Mariah Carey","Nothing Compares 2 U Sinéad O'Connor","Say Something A Great Big World","When I Was Your Man Bruno Mars","Irreplaceable Beyoncé","Too Little Too Late JoJo","It Must Have Been Love Roxette","The One That Got Away Katy Perry","I Knew You Were Trouble Taylor Swift","Love the Way You Lie Eminem ft. Rihanna","Cry Me a River Justin Timberlake","Before He Cheats Carrie Underwood","Jar of Hearts Christina Perri","Somebody That I Used to Know Gotye","Hot N Cold Katy Perry","Better in Time Leona Lewis","All Out of Love Air Supply","We Belong Pat Benatar"],
    "우정": ["Count on Me Bruno Mars","With a Little Help from My Friends The Beatles","Lean on Me Bill Withers","You've Got a Friend Carole King","I'll Be There Jackson 5","Umbrella Rihanna","We Are Young Fun ft. Janelle Monáe","See You Again Wiz Khalifa ft. Charlie Puth","Stand by Me Ben E. King","I'll Be There for You The Rembrandts","True Colors Cyndi Lauper","Good Riddance (Time of Your Life) Green Day","Graduation Vitamin C","Best Friend Saweetie ft. Doja Cat","Wind Beneath My Wings Bette Midler","Walking on Sunshine Katrina & The Waves","You've Got a Friend in Me Randy Newman","One Call Away Charlie Puth","Hero Enrique Iglesias","Bridge Over Troubled Water Simon & Garfunkel","Count on Me Jefferson Starship","Hold My Hand Jess Glynne","Friends Marshmello & Anne-Marie","Lean on Me Club Nouveau","We Go Together John Travolta & Olivia Newton-John","With a Little Help from My Friends Joe Cocker","I'll Be There Jess Glynne","True Friends Shannon Noll","I'll Be There Bobby Brown","You've Got a Friend Michael Jackson"],
    "위로": ["Fix You Coldplay","Let It Be The Beatles","Don't Worry Be Happy Bobby McFerrin","Bridge Over Troubled Water Simon & Garfunkel","Lean on Me Bill Withers","Stand by Me Ben E. King","Hero Mariah Carey","I Will Survive Gloria Gaynor","You Raise Me Up Josh Groban","Eye of the Tiger Survivor","Stronger Kelly Clarkson","Rise Katy Perry","Unstoppable Sia","Keep Holding On Avril Lavigne","Skyscraper Demi Lovato","Hold On Wilson Phillips","Brave Sara Bareilles","Roar Katy Perry","Fight Song Rachel Platten","Titanium David Guetta ft. Sia","Shake It Off Taylor Swift","Happy Pharrell Williams","Best Day of My Life American Authors","Good Life OneRepublic","Lovely Day Bill Withers","Walking on Sunshine Katrina & The Waves","Uptown Funk Mark Ronson ft. Bruno Mars","On Top of the World Imagine Dragons","Pocketful of Sunshine Natasha Bedingfield","Celebrate Kool & The Gang"],
    "추억": ["Summer of '69 Bryan Adams","Wake Me Up Avicii","Good Riddance (Time of Your Life) Green Day","Yesterday The Beatles","I Gotta Feeling Black Eyed Peas","Don't Stop Believin' Journey","Dancing Queen ABBA","Happy Pharrell Williams","Viva La Vida Coldplay","On Top of the World Imagine Dragons","Best Day of My Life American Authors","Sugar Maroon 5","I Will Remember You Sarah McLachlan","Walking on Sunshine Katrina & The Waves","Celebration Kool & The Gang","La La La Naughty Boy","I Gotta Feeling Black Eyed Peas","Friday Rebecca Black","Hey Ya! OutKast","We Are Young Fun ft. Janelle Monáe","Valerie Amy Winehouse","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Good Life OneRepublic","Lovely Day Bill Withers","Wake Me Up Before You Go-Go Wham!","Summer Justin Timberlake","Cheerleader OMI","Shut Up and Dance Walk The Moon","Good Time Owl City & Carly Rae Jepsen"],
    "그리움": ["Missing Everything But The Girl","I Miss You Blink-182","Far Away Nickelback","Someone Like You Adele","Tears Dry on Their Own Amy Winehouse","My Heart Will Go On Celine Dion","Unchained Melody The Righteous Brothers","All I Want Kodaline","Hurt Johnny Cash","With or Without You U2","Goodbye My Lover James Blunt","Back to December Taylor Swift","Everybody Hurts R.E.M.","Nothing Compares 2 U Sinéad O'Connor","Creep Radiohead","End of the Road Boyz II Men","Jar of Hearts Christina Perri","Lost Cause Billie Eilish","One Last Time Ariana Grande","Hallelujah Jeff Buckley","I Will Always Love You Whitney Houston","Bleeding Love Leona Lewis","The Scientist Coldplay","Say Something A Great Big World","Somebody That I Used to Know Gotye","Before He Cheats Carrie Underwood","Somebody I Used to Know Gotye","I Can't Make You Love Me Bonnie Raitt","Angels Robbie Williams","Yesterday Once More Carpenters"]
}

st.subheader("🎧 감정을 선택하고 추천 버튼을 눌러주세요")
selected_emotion = st.selectbox("감정 선택", list(emotion_songs.keys()))

if st.button("추천곡 보기"):
    songs = random.sample(emotion_songs[selected_emotion], 3)
    cards_html = "<div style='display:flex; gap:30px; justify-content:center; flex-wrap:wrap;'>"
    for song in songs:
        query = urllib.parse.quote(song)
        youtube_search = f"https://www.youtube.com/results?search_query={query}"
        thumbnail_url = f"https://img.youtube.com/vi/{random.randint(1,999999999)}/0.jpg"
        card = f"""
        <div class='song-card'>
            <a href="{youtube_search}" target="_blank" style='text-decoration:none; color:#fff;'>
                <img src="{thumbnail_url}" />
                <h3>{song}</h3>
            </a>
        </div>
        """
        cards_html += card
    cards_html += "</div>"
    st.components.v1.html(cards_html, height=450)
