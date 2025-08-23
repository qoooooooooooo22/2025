# app.py (완전 안정판)
import os
import re
import traceback
import streamlit as st

# -------------------------
# 설정: 페이지
# -------------------------
st.set_page_config(page_title="🎧 안정형 음악 추천기", page_icon="🎶")
st.title("🎤 키워드 기반 음악 추천기 (AI 우선, 실패 시 자체 추천)")

# -------------------------
# 자체 DB (유효한 YouTube 링크로 필요시 교체)
# -------------------------
SONGS = [
    {"title": "밤편지", "artist": "아이유", "keywords": ["감성", "발라드", "잔잔한"], "youtube": "https://www.youtube.com/watch?v=-2wMByiPrUE"},
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "keywords": ["락", "감성"], "youtube": "https://www.youtube.com/watch?v=mDWKfZJYytA"},
    {"title": "Dynamite", "artist": "BTS", "keywords": ["팝", "신나는", "댄스"], "youtube": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Love Poem", "artist": "아이유", "keywords": ["감성", "사랑", "발라드"], "youtube": "https://www.youtube.com/watch?v=omYoHGvQnq4"},
    {"title": "Permission to Dance", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=CuklIb9d3fI"},
]

# -------------------------
# 유틸: 키워드 기반 자체 추천
# -------------------------
def local_recommend(keywords, max_results=3):
    kws = [k.strip().lower() for k in keywords if k.strip()]
    matched = []
    for song in SONGS:
        song_kws = [s.lower() for s in song.get("keywords", [])]
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
    matched.sort(key=lambda x: x[0], reverse=True)
    return [m[1] for m in matched[:max_results]]

# -------------------------
# 유틸: API 키 안전 읽기/정리 (st.secrets -> env)
# -------------------------
def get_sanitized_api_key():
    raw = None
    try:
        raw = st.secrets.get("OPENAI_API_KEY")
    except Exception:
        raw = None
    if not raw:
        raw = os.environ.get("OPENAI_API_KEY")
    if not raw:
        return None, "NO_KEY"

    # strip BOM, whitespace, surrounding quotes
    api = raw.strip()
    if api.startswith("\ufeff"):
        api = api.lstrip("\ufeff")
    if api.startswith('"') and api.endswith('"'):
        api = api[1:-1]
    # remove control chars
    api = "".join(ch for ch in api if ord(ch) >= 32)
    # find non-ascii
    non_ascii = [i for i, ch in enumerate(api) if ord(ch) >= 128]
    note = None
    if non_ascii:
        note = f"NON_ASCII_AT: {non_ascii}"
    return api, note

# -------------------------
# 유틸: OpenAI 호출 (구버전 0.28 스타일)
# -------------------------
def call_openai_chat_completion(api_key, prompt, max_results=3):
    try:
        import openai
    except Exception as e:
        raise RuntimeError("openai 라이브러리 미설치") from e

    # assign key
    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.8,
            max_tokens=400
        )
        # 안전하게 내용 추출
        try:
            content = response.choices[0].message["content"]
        except Exception:
            try:
                content = response.choices[0].message.content
            except Exception:
                content = str(response)
        return content
    except Exception as e:
        # 래핑된 에러 전달
        raise RuntimeError(f"OpenAI 호출 실패: {e}") from e

# -------------------------
# UI: 키워드 입력 (엔터로 추가)
# -------------------------
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
    st.markdown("**현재 키워드:** " + ", ".join(st.session_state["keywords"]))
    if st.button("❌ 키워드 모두 초기화"):
        st.session_state["keywords"] = []

# -------------------------
# 추천 처리 (AI 우선, 실패 시 자체)
# -------------------------
if st.button("🎶 추천 받기") and st.session_state["keywords"]:
    keywords = st.session_state["keywords"]
    api_key, key_note = get_sanitized_api_key()

    tried_ai = False
    ai_error = None

    if api_key and api_key.startswith("sk-") and (key_note is None):
        # 준비: 빌드 프롬프트
        prompt = f"다음 키워드를 기반으로 한국 음악 또는 팝송 중 어울리는 노래 3곡을 추천해줘. 각 곡은 '곡 제목 - 아티스트 (YouTube 링크)' 형식으로 한 줄에 하나씩 출력해줘.\n키워드: {', '.join(keywords)}"
        try:
            with st.spinner("AI 추천 시도 중..."):
                content = call_openai_chat_completion(api_key, prompt, max_results=3)
                # 간단 파싱: 줄별로 출력
                lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
                if lines:
                    st.subheader("🎵 AI 추천 결과:")
                    for i, ln in enumerate(lines[:3], start=1):
                        # 번호 및 링크 처리(간단)
                        st.markdown(ln)
                        # try to extract link and show video
                        m = re.search(r"(https?://[^\s\)]+)", ln)
                        if m:
                            url = m.group(1).rstrip(")")
                            try:
                                st.video(url)
                            except Exception:
                                pass
                    tried_ai = True
                else:
                    ai_error = "AI가 빈 응답을 반환했습니다."
        except Exception as e:
            ai_error = str(e)
    else:
        if not api_key:
            ai_error = "OPENAI_API_KEY 미설정"
        elif not api_key.startswith("sk-"):
            ai_error = "OPENAI_API_KEY 형식 오류 (sk-로 시작하지 않음)"
        elif key_note:
            ai_error = f"OPENAI_API_KEY 비ASCII 문제: {key_note}"
        else:
            ai_error = "OPENAI_API_KEY 문제"

    # AI 실패 또는 비시도인 경우 로컬 추천 사용
    if not tried_ai:
        st.info(f"⚠️ AI 추천 불가 — 자체 추천으로 대체합니다. (원인: {ai_error})")
        local = local_recommend(keywords, max_results=3)
        if not local:
            st.warning("🔎 입력한 키워드와 매칭되는 노래가 없습니다.")
        else:
            st.subheader("🎵 자체 추천 결과:")
            for i, s in enumerate(local, start=1):
                st.markdown(f"{i}. **{s['title']}** - {s['artist']}")
                if s.get("youtube"):
                    try:
                        st.video(s.get("youtube"))
                    except Exception:
                        # 유튜브 재생 불가 시 링크만 제공
                        st.markdown(f"[YouTube 링크]({s.get('youtube')})")
