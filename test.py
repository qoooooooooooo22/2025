<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🎶 감정 기반 음악 추천</title>
<style>
body {
  margin:0; padding:0;
  font-family: 'Arial', sans-serif;
  background-color: #121212;
  color: #fff;
  display:flex; justify-content:center; align-items:flex-start;
}
.container {
  max-width:1200px; width:100%; padding:50px 20px; text-align:center;
}
h1 { font-size:3rem; margin-bottom:30px; animation:fadeIn 1s ease-out;}
select, button {
  background-color:#333; color:#fff; border:none; padding:10px 20px;
  font-size:1rem; border-radius:5px; cursor:pointer; margin:10px; transition:0.3s;
}
select:hover, button:hover { background-color:#444; }
.song-list { display:flex; flex-wrap:wrap; justify-content:center; gap:20px; margin-top:30px;}
.song-card {
  background-color:#1e1e1e; padding:20px; border-radius:10px; width:250px;
  text-align:left; box-shadow:0 4px 8px rgba(0,0,0,0.2); transition:transform 0.3s ease;
}
.song-card:hover { transform:translateY(-10px); }
.song-card img { width:100%; border-radius:10px; }
.song-card h3 { font-size:1.2rem; margin:10px 0; }
.song-card a {
  display:inline-block; margin-top:10px; padding:8px 15px; background-color:#ff4081;
  color:#fff; text-decoration:none; border-radius:5px; transition:0.3s;
}
.song-card a:hover { background-color:#e040fb; }
@keyframes fadeIn {
  0% {opacity:0; transform:translateY(20px);}
  100% {opacity:1; transform:translateY(0);}
}
</style>
</head>
<body>
<div class="container">
  <h1>🎶 감정 기반 음악 추천</h1>
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
</div>

<script>
// 10가지 감정 × 30곡 데이터 (재즈/팝 등 다양한 장르 포함)
const emotionSongs = {
  "사랑": ["All of Me John Legend","Just the Way You Are Bruno Mars","Fly Me to the Moon Frank Sinatra","Lover Taylor Swift","Your Song Elton John","At Last Etta James","Perfect Ed Sheeran","Can't Help Falling in Love Elvis Presley","Endless Love Diana Ross & Lionel Richie","Make You Feel My Love Adele","Something The Beatles","When I Fall in Love Nat King Cole","My Heart Will Go On Celine Dion","I Will Always Love You Whitney Houston","Love Story Taylor Swift","Thinking Out Loud Ed Sheeran","How Deep Is Your Love Bee Gees","Unchained Melody The Righteous Brothers","All My Life K-Ci & JoJo","Because You Loved Me Celine Dion","A Thousand Years Christina Perri","Vision of Love Mariah Carey","Everything Michael Bublé","I Just Called to Say I Love You Stevie Wonder","Truly Madly Deeply Savage Garden","Bleeding Love Leona Lewis","Time After Time Cyndi Lauper","Endless Love Luther Vandross","Kiss Me Sixpence None the Richer"],
  "슬픔": ["Someone Like You Adele","Hurt Johnny Cash","Tears Dry on Their Own Amy Winehouse","Everybody Hurts R.E.M.","Nothing Compares 2 U Sinéad O'Connor","Creep Radiohead","The Sound of Silence Simon & Garfunkel","My Immortal Evanescence","Back to Black Amy Winehouse","Yesterday The Beatles","Fade to Black Metallica","Goodbye My Lover James Blunt","All I Want Kodaline","Skinny Love Bon Iver","I Will Always Love You Whitney Houston","Jar of Hearts Christina Perri","Say Something A Great Big World","Lost Cause Billie Eilish","Everybody's Got to Learn Sometime The Korgis","With or Without You U2","Hallelujah Jeff Buckley","End of the Road Boyz II Men","I Can't Make You Love Me Bonnie Raitt","Nothing Else Matters Metallica","One Last Time Ariana Grande","Bleeding Love Leona Lewis","Angels Robbie Williams","Yesterday Once More Carpenters","Back to December Taylor Swift","Don't Speak No Doubt"],
  "행복": ["Happy Pharrell Williams","Walking on Sunshine Katrina & The Waves","Good Life OneRepublic","Can't Stop the Feeling Justin Timberlake","Lovely Day Bill Withers","Uptown Funk Mark Ronson ft. Bruno Mars","Best Day of My Life American Authors","Shake It Off Taylor Swift","Valerie Amy Winehouse","Roar Katy Perry","I Got a Feeling Black Eyed Peas","Sugar Maroon 5","On Top of the World Imagine Dragons","Pocketful of Sunshine Natasha Bedingfield","I'm Yours Jason Mraz","Wake Me Up Avicii","Happy Together The Turtles","Dancing Queen ABBA","Don't Worry Be Happy Bobby McFerrin","Good Morning Sunshine Lenka","Celebrate Kool & The Gang","Just Fine Mary J. Blige","Can't Stop Loving You Phil Collins","Lovely Justin Bieber","Best Song Ever One Direction","Good Time Owl City & Carly Rae Jepsen","Shut Up and Dance Walk The Moon","Cheerleader OMI","Sugar Baby Maroon 5","Good Vibes Chris Janson"],
  "집착": ["Every Breath You Take The Police","Obsessed Mariah Carey","Creep Radiohead","Possession Sarah McLachlan","Disturbia Rihanna","Control Janet Jackson","Jealous Nick Jonas","Toxic Britney Spears","Fix You Coldplay","Under Pressure Queen & David Bowie","Mad World Tears for Fears","Can't Get You Out of My Head Kylie Minogue","Addicted Kelly Clarkson","Love the Way You Lie Eminem ft. Rihanna","In the End Linkin Park","Black Widow Iggy Azalea","Crazy Gnarls Barkley","Bad Romance Lady Gaga","Stay Rihanna","Take a Bow Rihanna","Animal Neon Trees","Love on the Brain Rihanna","Don't Let Me Down The Chainsmokers","Monster Kanye West","Tainted Love Soft Cell","Running Up That Hill Kate Bush","You Give Love a Bad Name Bon Jovi","Control My Heart Lana Del Rey","I'm Not the Only One Sam Smith"],
  "귀여움": ["Baby Justin Bieber","Call Me Maybe Carly Rae Jepsen","Sugar Maroon 5","Shake It Off Taylor Swift","Happy Pharrell Williams","Love Me Like You Do Ellie Goulding","Candy Mandy Moore","Wannabe Spice Girls","Havana Camila Cabello","As It Was Harry Styles","Uptown Funk Mark Ronson ft. Bruno Mars","Good Time Owl City & Carly Rae Jepsen","La La La Naughty Boy","What Makes You Beautiful One Direction","Roar Katy Perry","Can't Stop the Feeling Justin Timberlake","Best Day of My Life American Authors","Cheerleader OMI","I'm a Believer Smash Mouth","Barbie Girl Aqua","I Like Me Better Lauv","Bubble Pop! HyunA","Sugar Baby Maroon 5","Lollipop Mika","Happy Together The Turtles","Walking on Sunshine Katrina & The Waves","Friday Rebecca Black","Hot N Cold Katy Perry","Hey Ya! OutKast","Electric Love BØRNS"],
  "이별": ["Someone Like You Adele","Back to December Taylor Swift","Cry Me a River Justin Timberlake","Bleeding Love Leona Lewis","Goodbye My Lover James Blunt","The Night We Met Lord Huron","Un-break My Heart Toni Braxton","I Will Remember You Sarah McLachlan","All I Want Kodaline","Say Something A Great Big World","Tears Dry on Their Own Amy Winehouse","Lost Cause Billie Eilish","Nothing Compares 2 U Sinéad O'Connor","Hurt Christina Aguilera","End of the Road Boyz II Men","Back to Black Amy Winehouse","One Last Time Ariana Grande","Creep Radiohead","With or Without You U2","I Can't Make You Love Me Bonnie Raitt","Time After Time Cyndi Lauper","My Immortal Evanescence","Don't Speak No Doubt","Bleeding Love Leona Lewis","Angels Robbie Williams","Yesterday Once More Carpenters","Goodbye Yellow Brick Road Elton John","Fade to Black Metallica","All My Life K-Ci & JoJo","I Will Always Love You Whitney Houston"],
  "우정": ["Lean on Me Bill Withers","With a Little Help from My Friends The Beatles","Count on Me Bruno Mars","You've Got a Friend Carole King","I'll Be There Jackson 5","We Are Young Fun ft. Janelle Monáe","Stand by Me Ben E. King","Best Friend Saweetie","Wannabe Spice Girls","Graduation Vitamin C","Hold My Hand Jess Glynne","Friends Marshmello & Anne-Marie","True Colors Cyndi Lauper","You've Got the Love Florence + The Machine","Wind Beneath My Wings Bette Midler","Good Riddance Green Day","Happy Pharrell Williams","Firework Katy Perry","We Go Together Grease Cast","It's My Life Bon Jovi","Walking on Sunshine Katrina & The Waves","We Are the Champions Queen","Don't Stop Believin' Journey","Count on Me Whitney Houston & CeCe Winans","I'll Be There for You The Rembrandts","You're My Best Friend Queen","Heroes David Bowie","You Raise Me Up Josh Groban","We Belong Pat Benatar","I'll Stand by You Pretenders"],
  "위로": ["Fix You Coldplay","Let It Be The Beatles","Bridge Over Troubled Water Simon & Garfunkel","Heal the World Michael Jackson","Everybody Hurts R.E.M.","The Climb Miley Cyrus","True Colors Cyndi Lauper","Lean on Me Bill Withers","Stronger Kelly Clarkson","Carry On Fun","Don't Give Up Peter Gabriel & Kate Bush","You Raise Me Up Josh Groban","Stand by Me Ben E. King","Rise Katy Perry","Keep Holding On Avril Lavigne","Beautiful Christina Aguilera","Firework Katy Perry","Brave Sara Bareilles","I Will Survive Gloria Gaynor","Titanium David Guetta ft. Sia","Skyscraper Demi Lovato","Hold On Wilson Phillips","Somewhere Over the Rainbow Israel Kamakawiwo'ole","Count on Me Bruno Mars","Heal Coldplay","Let Her Go Passenger","You Are Not Alone Michael Jackson","Three Little Birds Bob Marley","Don't Stop Believin' Journey","What a Wonderful World Louis Armstrong"],
  "추억": ["Summer of '69 Bryan Adams","Yesterday The Beatles","Time After Time Cyndi Lauper","Sweet Child O' Mine Guns N' Roses","Girls Just Want to Have Fun Cyndi Lauper","We Are Young Fun ft. Janelle Monáe","Take Me Home, Country Roads John Denver","Don't Stop Believin' Journey","Wonderwall Oasis","I'm Yours Jason Mraz","Landslide Fleetwood Mac","Ironic Alanis Morissette","Every Breath You Take The Police","Brown Eyed Girl Van Morrison","Hotel California Eagles","Boulevard of Broken Dreams Green Day","With or Without You U2","Another Day in Paradise Phil Collins","All Star Smash Mouth","Viva La Vida Coldplay","Chasing Cars Snow Patrol","Let Her Go Passenger","Yellow Coldplay","Clocks Coldplay","She Will Be Loved Maroon 5","Hey There Delilah Plain White T's","Time Coldplay","Wake Me Up Avicii","Rolling in the Deep Adele","Someone Like You Adele"],
  "그리움": ["I Miss You Blink-182","Far Away Nickelback","Need You Now Lady A","Home Michael Bublé","Back to December Taylor Swift","See You Again Wiz Khalifa ft. Charlie Puth","All I Want Kodaline","When I Was Your Man Bruno Mars","Somebody That I Used to Know Gotye","Tears Dry on Their Own Amy Winehouse","Yesterday The Beatles","Nothing Compares 2 U Sinéad O'Connor","My Heart Will Go On Celine Dion","Bleeding Love Leona Lewis","Say Something A Great Big World","Lost Without You Freya Ridings","Against All Odds Phil Collins","Un-break My Heart Toni Braxton","Back to Black Amy Winehouse","I Will Always Love You Whitney Houston","With or Without You U2","End of the Road Boyz II Men","Goodbye My Lover James Blunt","Time After Time Cyndi Lauper","Creep Radiohead","Everybody Hurts R.E.M.","All My Life K-Ci & JoJo","One Last Time Ariana Grande","Angels Robbie Williams","Someone Like You Adele","Hallelujah Jeff Buckley"]
};

function getRandomSongs(arr, count=3){
  let shuffled = arr.sort(()=>0.5-Math.random());
  return shuffled.slice(0,count);
}

const songList = document.getElementById('songList');
const emotionSelect = document.getElementById('emotionSelect');
const recommendBtn = document.getElementById('recommendBtn');

function displaySongs(){
  const emotion = emotionSelect.value;
  const songs = getRandomSongs(emotionSongs[emotion]);
  songList.innerHTML = '';
  songs.forEach(song=>{
    const card = document.createElement('div');
    card.classList.add('song-card');
    card.innerHTML = `
      <img src="https://via.placeholder.com/250x250?text=${encodeURIComponent(song)}" alt="${song}">
      <h3>${song}</h3>
      <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(song)}" target="_blank">YouTube에서 보기</a>
    `;
    songList.appendChild(card);
  });
}

recommendBtn.addEventListener('click', displaySongs);
displaySongs(); // 초기 로드 시
</script>
</body>
</html>
