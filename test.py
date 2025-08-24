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
  body, html { margin:0; padding:0; font-family:'Inter', sans-serif; background:#0f111a; color:#fff; overflow-x:hidden; }
  section { height:100vh; display:flex; justify-content:center; align-items:center; flex-direction:column; text-align:center; opacity:0; transform:translateY(50px);}
  section.active { opacity:1; transform:translateY(0); transition:1s ease;}
  h1 { font-size:4rem; font-weight:900; letter-spacing:0.1em; margin-bottom:20px; color:#fff; }
  h2 { font-size:2rem; margin-bottom:20px; color:#ff4081; }
  p { font-size:1.2rem; color:#ddd; }
  select, button { background:#1e1e2f; color:#fff; border:none; padding:12px 25px; margin:10px; border-radius:12px; cursor:pointer; transition:0.3s;}
  select:hover, button:hover { background:#ff4081; color:#000; }
  .song-list { display:flex; flex-wrap:wrap; justify-content:center; margin-top:30px; gap:25px; }
  .song-card { background:#222236; border-radius:20px; padding:20px; width:260px; text-align:center; box-shadow:0 10px 30px rgba(0,0,0,0.5); opacity:0; transform:translateY(50px); transition:0.5s ease, transform 0.5s ease; cursor:pointer; }
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
  <p>아래에서 감정을 선택하고 추천 버튼을 눌러보세요 🎧</p>
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
  <button id="recommendBtn">🎵 추천곡 보기</button>
</section>
<section id="recommendation">
  <div class="song-list" id="songList"></div>
</section>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.1/gsap.min.js"></script>
<script>
const emotionSongs = {
  // 각 감정별 30곡 유지 (재즈, 팝 등 다양)
  "사랑": ["All of Me John Legend","Just the Way You Are Bruno Mars","Fly Me to the Moon Frank Sinatra","Lover Taylor Swift","Your Song Elton John","At Last Etta James","Perfect Ed Sheeran","Can't Help Falling in Love Elvis Presley","Endless Love Diana Ross & Lionel Richie","Make You Feel My Love Adele","Something The Beatles","When I Fall in Love Nat King Cole","My Heart Will Go On Celine Dion","I Will Always Love You Whitney Houston","Love Story Taylor Swift","Thinking Out Loud Ed Sheeran","How Deep Is Your Love Bee Gees","Unchained Melody The Righteous Brothers","All My Life K-Ci & JoJo","Because You Loved Me Celine Dion","A Thousand Years Christina Perri","Vision of Love Mariah Carey","Everything Michael Bublé","I Just Called to Say I Love You Stevie Wonder","Truly Madly Deeply Savage Garden","Bleeding Love Leona Lewis","Time After Time Cyndi Lauper","Endless Love Luther Vandross","Kiss Me Sixpence None the Richer"],
  "슬픔": ["Someone Like You Adele","Hurt Johnny Cash","Tears Dry on Their Own Amy Winehouse","Everybody Hurts R.E.M.","Nothing Compares 2 U Sinéad O'Connor","Creep Radiohead","The Sound of Silence Simon & Garfunkel","My Immortal Evanescence","Back to Black Amy Winehouse","Yesterday The Beatles","Fade to Black Metallica","Goodbye My Lover James Blunt","All I Want Kodaline","Skinny Love Bon Iver","I Will Always Love You Whitney Houston","Jar of Hearts Christina Perri","Say Something A Great Big World","Lost Cause Billie Eilish","Everybody's Got to Learn Sometime The Korgis","With or Without You U2","Hallelujah Jeff Buckley","End of the Road Boyz II Men","I Can't Make You Love Me Bonnie Raitt","Nothing Else Matters Metallica","One Last Time Ariana Grande","Bleeding Love Leona Lewis","Angels Robbie Williams","Yesterday Once More Carpenters","Don't Speak No Doubt"],
  "행복": ["Happy Pharrell Williams","Walking on Sunshine Katrina & The Waves","Good Life OneRepublic","Can't Stop the Feeling Justin Timberlake","Lovely Day Bill Withers","Uptown Funk Mark Ronson ft. Bruno Mars","Best Day of My Life American Authors","Shake It Off Taylor Swift","Valerie Amy Winehouse","Roar Katy Perry","I Got a Feeling Black Eyed Peas","Sugar Maroon 5","On Top of the World Imagine Dragons","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Wake Me Up Avicii","Happy Together The Turtles","Dancing Queen ABBA","Don't Worry Be Happy Bobby McFerrin","Good Morning Sunshine Lenka","Celebrate Kool & The Gang","Just Fine Mary J. Blige","Can't Stop Loving You Phil Collins","Lovely Justin Bieber","Best Song Ever One Direction","Good Time Owl City & Carly Rae Jepsen","Shut Up and Dance Walk The Moon","Cheerleader OMI","Sugar Baby Maroon 5","Good Vibes Chris Janson"]
  // 나머지 감정도 동일하게 30곡씩 추가
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

components.html(html_code, height=1600)
