<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>🎶 감정 기반 음악 추천</title>
  <style>
    /* 전체 스타일링 */
    body, html {
      margin: 0;
      padding: 0;
      height: 100%;
      font-family: 'Inter', sans-serif;
      background-color: #080808;
      color: #f0f0f0;
      overflow: hidden;
    }
    section {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      text-align: center;
      opacity: 0;
      transform: translateY(100px);
    }
    section.active {
      opacity: 1;
      transform: translateY(0);
      transition: opacity 0.8s ease, transform 0.8s ease;
    }
    h1 {
      font-size: 3rem;
      font-weight: 900;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }
    .song-card {
      background: #1c1c1c;
      border-radius: 15px;
      padding: 20px;
      margin: 10px;
      width: 250px;
      text-align: center;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
      opacity: 0;
      transform: translateY(50px);
      transition: opacity 0.5s ease, transform 0.5s ease;
    }
    .song-card.active {
      opacity: 1;
      transform: translateY(0);
    }
    .song-card img {
      width: 100%;
      border-radius: 10px;
    }
    .song-card h3 {
      margin-top: 10px;
      font-size: 1.2rem;
      font-weight: 600;
    }
    .song-card a {
      display: inline-block;
      margin-top: 10px;
      color: #f0f0f0;
      text-decoration: none;
      font-weight: 500;
      transition: color 0.3s ease;
    }
    .song-card a:hover {
      color: #ff4081;
    }
  </style>
</head>
<body>
  <section id="intro">
    <h1>🎶 감정 기반 음악 추천</h1>
  </section>
  <section id="recommendation">
    <h2>당신의 감정을 선택하세요</h2>
    <select id="emotionSelect">
      <option value="happy">행복</option>
      <option value="sad">슬픔</option>
      <option value="angry">화남</option>
      <option value="relaxed">편안함</option>
      <option value="excited">신남</option>
    </select>
    <button id="recommendBtn">추천 받기</button>
    <div id="songList"></div>
  </section>

  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.1/gsap.min.js"></script>
  <script>
    const emotionSongs = {
      happy: ["Happy Song 1", "Happy Song 2", "Happy Song 3"],
      sad: ["Sad Song 1", "Sad Song 2", "Sad Song 3"],
      angry: ["Angry Song 1", "Angry Song 2", "Angry Song 3"],
      relaxed: ["Relaxed Song 1", "Relaxed Song 2", "Relaxed Song 3"],
      excited: ["Excited Song 1", "Excited Song 2", "Excited Song 3"]
    };

    function getRandomSongs(emotion, count = 3) {
      const songs = emotionSongs[emotion];
      const shuffled = songs.sort(() => 0.5 - Math.random());
      return shuffled.slice(0, count);
    }

    function displaySongs() {
      const emotion = document.getElementById('emotionSelect').value;
      const songs = getRandomSongs(emotion);
      const songList = document.getElementById('songList');
      songList.innerHTML = '';
      songs.forEach((song, index) => {
        const card = document.createElement('div');
        card.classList.add('song-card');
        card.innerHTML = `
          <img src="https://via.placeholder.com/250x250?text=${encodeURIComponent(song)}" alt="${song}">
          <h3>${song}</h3>
          <a href="https://www.youtube.com/results?search_query=${encodeURIComponent(song)}" target="_blank">YouTube에서 보기</a>
        `;
        songList.appendChild(card);
        gsap.to(card, { opacity: 1, y: 0, delay: index * 0.2 });
      });
    }

    document.getElementById('recommendBtn').addEventListener('click', () => {
      gsap.to("#recommendation", { opacity: 0, y: 100, duration: 0.5 });
      setTimeout(() => {
        displaySongs();
        gsap.to("#recommendation", { opacity: 1, y: 0, duration: 0.5 });
      }, 500);
    });

    window.addEventListener('scroll', () => {
      const sections = document.querySelectorAll('section');
      sections.forEach(section => {
        const rect = section.getBoundingClientRect();
        if (rect.top <= window.innerHeight * 0.75) {
          section.classList.add('active');
        }
      });
    });

    // 초기화
    gsap.from("#intro", { opacity: 0, y: 100, duration: 1 });
    gsap.from("#recommendation", { opacity: 0, y: 100, duration: 1, delay: 1 });
  </script>
</body>
</html>
