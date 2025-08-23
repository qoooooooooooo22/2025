# app.py
import streamlit as st
from packaging import version
import traceback

# ----- 자체 추천 데이터 (YouTube 링크는 실제 가능한 예시로 채움) -----
songs = [
    {"title": "밤편지", "artist": "아이유", "keywords": ["감성", "발라드", "잔잔한"], "youtube": "https://www.youtube.com/watch?v=-2wMByiPrUE"},
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "keywords": ["락", "감성"], "youtube": "https://www.youtube.com/watch?v=mDWKfZJYytA"},
    {"title": "Dynamite", "artist": "BTS", "keywords": ["팝", "신나는", "댄스"], "youtube": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Love Poem", "artist": "아이유", "keywords": ["감성", "사랑", "발라드"], "youtube": "https://www.youtube.com/watch?v=omYoHGvQnq4"},
    {"title": "Permission to Dance", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=CuklIb9d3fI"},
    {"title": "Tomboy", "artist": "혁오 (HYUKOH)", "keywords": ["인디", "감성", "록"], "youtube": "https://www.youtube.com/watch?v=F6q0uQYzQhw"},
    {"title": "밤과 별의 노래", "artist": "적재", "keywords": ["잔잔한", "감성"], "youtube": "https://www.youtube.com/watch?v=example1"},  # 필요시 실링크 교체
    {"title": "Any Song", "artist": "Zico", "keywords": ["힙합","신나는"], "youtube": "https://www.youtube.com/watch?v=_QJnlLEb0-M"},
    {"title": "Everything", "artist": "검정치마", "keywords": ["몽환적","인디"], "youtube": "https://www.youtube.com/watch?v=fIHLFFlsw_c"},
    {"title": "Gravity", "artist": "John Mayer", "keywords": ["기타","잔잔한","블루스"], "youtube": "https://www.youtube.com/watch?v=Bu92GmnXf3w"},
]

# ---- 도움 함수: 로컬(자체) 추천 ----
def local_recommend(keywords, max_results=3):
    kws = [k.strip().lower() for k in keywords if k.strip()]
    matched = []
    for song in songs:
        song_kws = [s.lower() for s in song.get("keywords", [])]
        # 완전 일치 키워드 또는 부분 매칭 (제목/아티스트에 포함)
        score = 0
        for kw in kws:
            if any(kw == sk for sk in song_kws):
                score += 10
            elif any(kw in sk for sk in song_kws):
                score += 5
            elif kw in song["title"].lower() or kw in song["artist"].lower():
                score += 3
        if score > 0:
            matched.append((score, song))
    # score로 정렬 내림차순
    matched.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matched[:max_results]]

# ---- 도움 함수: OpenAI 응답 텍스트에서 노래 라인 파싱 (간단) ----
def parse_openai_text_to_list(text):
    # 기대형식: "1. 곡 - 아티스트 (YouTube link)\n2. ..."
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    results = []
    for ln in lines:
        # remove leading numbering if present
        import re
        ln2 = re.sub(r"^\d+\.\s*", "", ln)
        # try to extract title - artist (link)
        # naive split by '(' to find link
        link = None
        if "(" in ln2 and "http" in ln2:
            # assume last parentheses contain link
            try:
                link = re.search(r"\((https?://[^\)]+)\)", ln2).group(1)
                ln2 = re.sub(r"\s*\(https?://[^\)]+\)\s*$", "", ln2)
            except Exception:
                link = None
        # split by ' - ' or ' — ' or ' – '
        if " - " in ln2:
            parts = ln2.split(" - ", 1)
        elif " — " in ln2:
            parts = ln2.split(" — ", 1)
        elif " – " in ln2:
            parts = ln2.split(" – ", 1)
        else:
            parts = [ln2, ""]
        title = parts[0].strip()
        artist = parts[1].strip() if len(parts) > 1 else ""
        results.append({"title": title, "artist": artist, "youtube": link})
    return results

# ---- OpenAI 호출 안전 래퍼: 버전 감지 후 호출 ----
def ai_recommend(keywords, max_results=3):
    try:
        import openai
    except Exception as e:
        # openai 라이브러리 자체 없음
        raise RuntimeError("OpenAI 라이브러리 없음") from e

    # get installed version if present
    try:
        ver = getattr(openai, "__version__", None)
    except Exception:
        ver = None

    prompt = f"다음 키워드를 기반으로 한국 음악 또는 팝송 중 어울리는 노래 {max_results}곡을 추천해줘. 각 곡은 '곡 제목 - 아티스트 (YouTube 링크)' 형식으로 한 줄에 하나씩 출력해줘.\n키워드: {', '.join(keywords)}"

    # 신버전(openai>=1.0.0)인지 구분
    is_new_api = False
    if ver is not None:
        try:
            is_new_api = version.parse(ver) >= version.parse("1.0.0")
        except Exception:
            is_new_api = hasattr(openai, "OpenAI")
    else:
        is_new_api = hasattr(openai, "OpenAI")

    # retrieve API key from st.secrets or environment if already set outside
    api_key = None
    if st.secrets.get("OPENAI_API_KEY"):
        api_key = st.secrets["OPENAI_API_KEY"]

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 없음")

    # call accordingly
    if is_new_api:
        # openai.OpenAI client
        try:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            # try different response access patterns
            try:
                content = response.choices[0].message.content
            except Exception:
                try:
                    content = response.choices[0].message["content"]
                except Exception:
                    # fallback: try to string-convert whole response
                    content = str(response)
        except Exception as e:
            raise RuntimeError("OpenAI 호출 실패 (신버전)") from e
    else:
        # old API (0.28)
        try:
            openai.api_key = api_key
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )
            try:
                # 여러 포맷 처리
                content = response.choices[0].message["content"]
            except Exception:
                try:
                    content = response.choices[0].message.content
                except Exception:
                    content = str(response)
        except Exception as e:
            raise RuntimeError("OpenAI 호출 실패 (구버전)") from e

    # parse content into structured list
    parsed = parse_openai_text_to_list(content)
    # ensure we return up to max_results items
    return parsed[:max_results]

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(page_title="🎧 정확한 음악 추천기", page_icon="🎶")
st.title("🎤 키워드 기반 노래 추천기 — AI 우선, 실패 시 자체 추천")

st.markdown(
    "키워드를 입력하고 엔터를 누르면 자동 추가됩니다. 여러 키워드를 추가한 뒤 '추천 받기' 버튼을 눌러보세요. "
    "OpenAI 키(선택)를 넣으면 AI 추천을 먼저 시도합니다."
)

# 세션 상태 초기화 (안전)
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "new_keyword" not in st.session_state:
    st.session_state["new_keyword"] = ""

def add_keyword():
    if "new_keyword" in st.session_state:
        kw = st.session_state["new_keyword"].strip()
        if kw and kw not in st.session_state["keywords"]:
            st.session_state["keywords"].append(kw)
        st.session_state["new_keyword"] = ""

st.text_input("🎵 키워드 입력 (엔터로 추가)", key="new_keyword", placeholder="예: 감성, 사랑, 락", on_change=add_keyword)

if st.session_state["keywords"]:
    st.markdown("#### 📌 현재 키워드:")
    st.write(", ".join(st.session_state["keywords"]))
    if st.button("❌ 키워드 모두 초기화"):
        st.session_state["keywords"] = []

# 추천 버튼
if st.button("🎶 추천 받기") and st.session_state["keywords"]:
    keywords = st.session_state["keywords"]
    # 1) 시도: AI
    did_ai = False
    ai_failed_reason = None
    try:
        # only attempt AI if openai lib present and secret provided
        import importlib
        if importlib.util.find_spec("openai") and st.secrets.get("OPENAI_API_KEY"):
            with st.spinner("AI가 추천하는 중..."):
                ai_results = ai_recommend(keywords, max_results=3)
                # if ai_results empty -> consider failure
                if ai_results:
                    st.subheader("🎵 AI 추천 결과:")
                    for idx, item in enumerate(ai_results, start=1):
                        title = item.get("title") or ""
                        artist = item.get("artist") or ""
                        youtube = item.get("youtube")
                        st.markdown(f"{idx}. **{title}** - {artist}")
                        if youtube:
                            st.video(youtube)
                    did_ai = True
                else:
                    ai_failed_reason = "AI가 유효한 추천을 반환하지 않았습니다."
        else:
            ai_failed_reason = "OpenAI 라이브러리 또는 OPENAI_API_KEY 없음"
    except Exception as e:
        ai_failed_reason = f"AI 호출 실패: {e}\n{traceback.format_exc()}"

    # 2) AI 실패 시 자체 추천
    if not did_ai:
        st.info(f"⚠️ AI 추천 불가 — 자체 추천으로 대체합니다. ({ai_failed_reason})")
        local = local_recommend(keywords, max_results=3)
        if not local:
            st.warning("🔎 입력한 키워드와 매칭되는 노래가 없습니다.")
        else:
            st.subheader("🎵 자체 추천 결과:")
            for i, song in enumerate(local, start=1):
                st.markdown(f"{i}. **{song['title']}** - {song['artist']}")
                # 유튜브 미리보기 (유효한 링크일 때만)
                if song.get("youtube"):
                    st.video(song["youtube"])
