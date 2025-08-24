import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="감정 기반 음악 추천", page_icon="🎶", layout="wide")
st.title("🎶 감정 기반 음악 추천")

html_code = """
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>감정 기반 음악 추천</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  body, html { margin:0; padding:0; font-family:'Inter', sans-serif; background:#0a0a0a; color:#fff; overflow-x:hidden; }
  section { height:100vh; display:flex; justify-content:center; align-items:center; flex-direction:column; text-align:center; opacity:0; transform:translateY(50px);}
  section.active { opacity:1; transform:translateY(0); transition:1s ease;}
  h1 { font-size:4rem; font-weight:900; letter-spacing:0.1em; margin-bottom:30px; color:#fff; text-transform:uppercase; }
  h2 { font-size:2rem; margin-bottom:20px; color:#ff4081; }
  select, button { background:#222; color:#fff; border:none; padding:12px 25px; margin:10px; border-radius:12px; cursor:pointer; transition:0.3s;}
  select:hover, button:hover { background:#ff4081; color:#000; }
  .song-list { display:flex; flex-wrap:wrap; justify-content:center; margin-top:30px; gap:25px; }
  .song-card { background:#1a1a1a; border-radius:20px; padding:20px; width:260px; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.5); opacity:0; transform:translateY(50px); transition:0.5s ease, transform 0.5s ease; cursor:pointer; }
  .song-card.active { opacity:1; transform:translateY(0);}
  .song-card:hover { transform:scale(1.05) rotate(-1deg); box-shadow:0 15px 35px rgba(255,64,129,0.6); }
  .song-card img { width:100%; border-radius:15px; }
  .song-card h3 { margin-top:10px; font-size:1.2rem; font-weight:700; }
  .song-card a { display:inline-block; margin-top:10px; color:#fff; text-decoration:none; transition:0.3s;}
  .song-card a:hover { color:#ff4081; }
</style>
</head>
<body>
<section id="intro">
  <h1>Emotion Based Music</h1>
  <h2>감정에 맞는 노래를 추천받아보세요</h2>
</section>
<section id="recommendation">
  <h2>감정을 선택하세요</h2>
  <select id="emotionSelect">
    <option value="사랑">사랑 💕</option>
    <option value="슬픔">슬픔 😢</option>
    <option value="행복">행복 😆</option>
    <option value="집착">집착 😠</option>
    <option value="귀여움">귀여움 🐰</option>
    <option value="이별">이별 💔</option>
    <option value="우정">우정 🎉</option>
    <option value="위로">위로 🧸</option>
    <option value="추억">추억 🌅</option>
    <option value="그리움">그리움 🌧️</option>
  </select>
  <button id="recommendBtn">🎧 추천곡 보기</button>
  <div class="song-list" id="songList"></div>
</section>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.1/gsap.min.js"></script>
<script>
const emotionSongs = {
  "사랑": ["All of Me John Legend","Just the Way You Are Bruno Mars","Fly Me to the Moon Frank Sinatra","Lover Taylor Swift","Your Song Elton John","At Last Etta James","Perfect Ed Sheeran","Can't Help Falling in Love Elvis Presley","Endless Love Diana Ross & Lionel Richie","Make You Feel My Love Adele","Something The Beatles","When I Fall in Love Nat King Cole","My Heart Will Go On Celine Dion","I Will Always Love You Whitney Houston","Love Story Taylor Swift","Thinking Out Loud Ed Sheeran","How Deep Is Your Love Bee Gees","Unchained Melody The Righteous Brothers","All My Life K-Ci & JoJo","Because You Loved Me Celine Dion","A Thousand Years Christina Perri","Vision of Love Mariah Carey","Everything Michael Bublé","I Just Called to Say I Love You Stevie Wonder","Truly Madly Deeply Savage Garden","Bleeding Love Leona Lewis","Time After Time Cyndi Lauper","Endless Love Luther Vandross","Kiss Me Sixpence None the Richer"],
  "슬픔": ["Someone Like You Adele","Hurt Johnny Cash","Tears Dry on Their Own Amy Winehouse","Everybody Hurts R.E.M.","Nothing Compares 2 U Sinéad O'Connor","Creep Radiohead","The Sound of Silence Simon & Garfunkel","My Immortal Evanescence","Back to Black Amy Winehouse","Yesterday The Beatles","Fade to Black Metallica","Goodbye My Lover James Blunt","All I Want Kodaline","Skinny Love Bon Iver","I Will Always Love You Whitney Houston","Jar of Hearts Christina Perri","Say Something A Great Big World","Lost Cause Billie Eilish","Everybody's Got to Learn Sometime The Korgis","With or Without You U2","Hallelujah Jeff Buckley","End of the Road Boyz II Men","I Can't Make You Love Me Bonnie Raitt","Nothing Else Matters Metallica","One Last Time Ariana Grande","Bleeding Love Leona Lewis","Angels Robbie Williams","Yesterday Once More Carpenters","Don't Speak No Doubt"],
  "행복": ["Happy Pharrell Williams","Walking on Sunshine Katrina & The Waves","Good Life OneRepublic","Can't Stop the Feeling Justin Timberlake","Lovely Day Bill Withers","Uptown Funk Mark Ronson ft. Bruno Mars","Best Day of My Life American Authors","Shake It Off Taylor Swift","Valerie Amy Winehouse","Roar Katy Perry","I Got a Feeling Black Eyed Peas","Sugar Maroon 5","On Top of the World Imagine Dragons","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Wake Me Up Avicii","Happy Together The Turtles","Dancing Queen ABBA","Don't Worry Be Happy Bobby McFerrin","Good Morning Sunshine Lenka","Celebrate Kool & The Gang","Just Fine Mary J. Blige","Can't Stop Loving You Phil Collins","Lovely Justin Bieber","Best Song Ever One Direction","Good Time Owl City & Carly Rae Jepsen","Shut Up and Dance Walk The Moon","Cheerleader OMI","Sugar Baby Maroon 5","Good Vibes Chris Janson"],
  "집착": ["Every Breath You Take The Police","Obsessed Mariah Carey","Creep Radiohead","Possession Sarah McLachlan","Disturbia Rihanna","Control Janet Jackson","Jealous Nick Jonas","Toxic Britney Spears","Fix You Coldplay","Under Pressure Queen & David Bowie","Mad World Tears for Fears","Can't Get You Out of My Head Kylie Minogue","Addicted Kelly Clarkson","Love the Way You Lie Eminem ft. Rihanna","In the End Linkin Park","Black Widow Iggy Azalea","Crazy Gnarls Barkley","Bad Romance Lady Gaga","Stay Rihanna","Take a Bow Rihanna","Animal Neon Trees","Love on the Brain Rihanna","Don't Let Me Down The Chainsmokers","Monster Kanye West","Tainted Love Soft Cell","Running Up That Hill Kate Bush","You Give Love a Bad Name Bon Jovi","Control My Heart Lana Del Rey","I'm Not the Only One Sam Smith"],
  "귀여움": ["Baby Justin Bieber","Call Me Maybe Carly Rae Jepsen","Sugar Maroon 5","Shake It Off Taylor Swift","Happy Pharrell Williams","Love Me Like You Do Ellie Goulding","Candy Mandy Moore","Wannabe Spice Girls","Havana Camila Cabello","As It Was Harry Styles","Uptown Funk Mark Ronson ft. Bruno Mars","Good Time Owl City & Carly Rae Jepsen","La La La Naughty Boy","What Makes You Beautiful One Direction","Roar Katy Perry","Can't Stop the Feeling Justin Timberlake","Best Day of My Life American Authors","Cheerleader OMI","I'm a Believer Smash Mouth","Barbie Girl Aqua","I Like Me Better Lauv","Bubble Pop! HyunA","Sugar Baby Maroon 5","Lollipop Mika","Happy Together The Turtles","Walking on Sunshine Katrina & The Waves","Friday Rebecca Black","Hot N Cold Katy Perry","Hey Ya! OutKast","Electric Love BØRNS"],
  "이별": ["Someone Like You Adele","Back to December Taylor Swift","Un-break My Heart Toni Braxton","Goodbye My Lover James Blunt","The Scientist Coldplay","Nothing Compares 2 U Sinéad O'Connor","When I Was Your Man Bruno Mars","All I Want Kodaline","Love Yourself Justin Bieber","Too Good at Goodbyes Sam Smith","Without You Mariah Carey","Say Something A Great Big World","End of the Road Boyz II Men","Tears Dry on Their Own Amy Winehouse","I Will Always Love You Whitney Houston","Bleeding Love Leona Lewis","Creep Radiohead","Everybody Hurts R.E.M.","Yesterday The Beatles","Fade to Black Metallica","Back to Black Amy Winehouse","Jar of Hearts Christina Perri","Lost Cause Billie Eilish","With or Without You U2","Hallelujah Jeff Buckley","Nothing Else Matters Metallica","One Last Time Ariana Grande","Don't Speak No Doubt","Endless Love Diana Ross & Lionel Richie","My Immortal Evanescence"],
  "우정": ["Count on Me Bruno Mars","With a Little Help from My Friends The Beatles","Lean on Me Bill Withers","You've Got a Friend Carole King","I'll Be There Jackson 5","Umbrella Rihanna","We Are Young Fun ft. Janelle Monáe","See You Again Wiz Khalifa ft. Charlie Puth","Stand by Me Ben E. King","I'll Be There for You The Rembrandts","True Colors Cyndi Lauper","Good Riddance (Time of Your Life) Green Day","Graduation Vitamin C","Best Friend Saweetie ft. Doja Cat","Wind Beneath My Wings Bette Midler","Walking on Sunshine Katrina & The Waves","You've Got a Friend in Me Randy Newman","One Call Away Charlie Puth","Hero Enrique Iglesias","Bridge Over Troubled Water Simon & Garfunkel","Count on Me Jefferson Starship","Hold My Hand Jess Glynne","Friends Marshmello & Anne-Marie","Lean on Me Club Nouveau","We Go Together John Travolta & Olivia Newton-John","With a Little Help from My Friends Joe Cocker","I'll Be There Jess Glynne","True Friends Shannon Noll","I'll Be There Bobby Brown","You've Got a Friend Michael Jackson"],
  "위로": ["Fix You Coldplay","Let It Be The Beatles","Don't Worry Be Happy Bobby McFerrin","Bridge Over Troubled Water Simon & Garfunkel","Lean on Me Bill Withers","Stand by Me Ben E. King","Hero Mariah Carey","I Will Survive Gloria Gaynor","You Raise Me Up Josh Groban","Eye of the Tiger Survivor","Stronger Kelly Clarkson","Rise Katy Perry","Unstoppable Sia","Keep Holding On Avril Lavigne","Skyscraper Demi Lovato","Hold On Wilson Phillips","Brave Sara Bareilles","Roar Katy Perry","Fight Song Rachel Platten","Titanium David Guetta ft. Sia","Shake It Off Taylor Swift","Happy Pharrell Williams","Best Day of My Life American Authors","Good Life OneRepublic","Lovely Day Bill Withers","Walking on Sunshine Katrina & The Waves","Uptown Funk Mark Ronson ft. Bruno Mars","On Top of the World Imagine Dragons","Pocketful of Sunshine Natasha Bedingfield","Celebrate Kool & The Gang"],
  "추억": ["Summer of '69 Bryan Adams","Wake Me Up Avicii","Good Riddance (Time of Your Life) Green Day","Yesterday The Beatles","I Gotta Feeling Black Eyed Peas","Don't Stop Believin' Journey","Dancing Queen ABBA","Happy Pharrell Williams","Viva La Vida Coldplay","On Top of the World Imagine Dragons","Best Day of My Life American Authors","Sugar Maroon 5","I Will Remember You Sarah McLachlan","Walking on Sunshine Katrina & The Waves","Celebration Kool & The Gang","La La La Naughty Boy","I Gotta Feeling Black Eyed Peas","Friday Rebecca Black","Hey Ya! OutKast","We Are Young Fun ft. Janelle Monáe","Valerie Amy Winehouse","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Good Life OneRepublic","Lovely Day Bill Withers","Wake Me Up Before You Go-Go Wham!","Summer Justin Timberlake","Cheerleader OMI","Shut Up and Dance Walk The Moon","Good Time Owl City & Carly Rae Jepsen"],
  "그리움": ["Missing Everything But The Girl","I Miss You Blink-182","Far Away Nickelback","Someone Like You Adele","Tears Dry on Their Own Amy Winehouse","My Heart Will Go On Celine Dion","Unchained Melody The Righteous Brothers","All I Want Kodaline","Hurt Johnny Cash","With or Without You U2","Goodbye My Lover James Blunt","Back to December Taylor Swift","Everybody Hurts R.E.M.","Nothing Compares 2 U Sinéad O'Connor","Creep Radiohead","End of the Road Boyz II Men","Jar of Hearts Christina Perri","Lost Cause Billie Eilish","One Last Time Ariana Grande","Hallelujah Jeff Buckley","I Will Always Love You Whitney Houston","Bleeding Love Leona Lewis","The Scientist Coldplay","Say Something A Great Big World","Skinny Love Bon Iver","Fade to Black Metallica","Don't Speak No Doubt","Yesterday The Beatles","Back to Black Amy Winehouse","Endless Love Diana Ross & Lionel Richie"]
};

function getRandomSongs(arr,count=3){
  let shuffled = [...arr].sort(()=>0.5-Math.random());
  return shuffled.slice(0,count);
}

const songList = document.getElementById('songList');
const emotionSelect = document.getElementById('emotionSelect');
const recommendBtn = document.getElementById('recommendBtn');

function displaySongs(){
  const emotion = emotionSelect.value;
  const songs = getRandomSongs(emotionSongs[emotion]);
  songList.innerHTML='';
  songs.forEach((song,index)=>{
    const card = document.createElement('div');
    card.classList.add('song-card');
    card.innerHTML = `
      <img src="https://via.placeholder.com/260x260?text=${encodeURIComponent(song)}" alt="${song}">
      <h3>${song}</h3>
      <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(song)}" target="_blank">YouTube에서 보기</a>
    `;
    songList.appendChild(card);
    setTimeout(()=>{card.classList.add('active')}, index*150);
  });
}

recommendBtn.addEventListener('click', displaySongs);

window.addEventListener('scroll',()=>{
  document.querySelectorAll('section').forEach(section=>{
    if(window.scrollY+window.innerHeight*0.8>section.offsetTop){
      section.classList.add('active');
    }
  });
});

document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('section').forEach(section=>{
    if(window.scrollY+window.innerHeight*0.8>section.offsetTop){
      section.classList.add('active');
    }
  });
});
</script>
</body>
</html>
"""

components.html(html_code, height=1500)
