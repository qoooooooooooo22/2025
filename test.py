# app.py (안정판 - openai==0.28.0용)
import streamlit as st
import traceback

# -------------------
# 자체 추천 DB (유효한 YouTube 링크로 교체했음)
# -------------------
songs = [
    {"title": "밤편지", "artist": "아이유", "keywords": ["감성", "발라드", "잔잔한"], "youtube": "https://www.youtube.com/watch?v=-2wMByiPrUE"},
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "keywords": ["락", "감성"], "youtube": "https://www.youtube.com/watch?v=mDWKfZJYytA"},
    {"title": "Dynamite", "artist": "BTS", "keywords": ["팝", "신나는", "댄스"], "youtube": "https://www.youtube.com/watch?v=gdZLi9oWNZg"},
    {"title": "Love Poem", "artist": "아이유", "keywords": ["감성", "사랑", "발라드"], "youtube": "https://www.youtube.com/watch?v=omYoHGvQnq4"},
    {"title": "Permission to Dance", "artist": "BTS", "keywords": ["팝", "신나는"], "youtube": "https://www.youtube.com/watch?v=CuklIb9d3fI"},
]

# -------------------
# 로컬 추천 함수
# -------------------
def local_recommend(keywords, max_results=3):
    kws = [k.strip().lower() for k in keywords if k.strip()]
    matched = []
    for song in songs:
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

# -------------------
# OpenAI 호출 (구버전 0.28 API 사용)
# -------------------
def ai_recommend_openai_028(keywords, max_results=3):
    try:
        import openai
    except ModuleNotFoundError:
        raise RuntimeError("OpenAI 라이브러리가 설치되어 있지 않습니다.")

    # OpenAI key 읽기 (Streamlit Cloud에서는 st.secrets에, 로컬에서는 환경변수로 넣어도 됨)
    api_key = None
    if st.secrets and st.secrets.get("OPENAI_API_KEY"):
        api_key = st.secrets.get("OPENAI_API_KEY")
    else:
        # 시나리오: 로컬 테스트 시 environment variable 사용할 경우
        import os
        api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError("OPENAI_API_KEY 없음")

    # 안전하게 키 할당
    openai.api_key = api_key

    # 한 줄 프롬프트 생성
    prompt = f"다음 키워드를 기반으로 한국 음악 또는 팝송 중 어울리는 노래 {max_results}곡을 추천해줘. 각 곡은 '곡 제목 - 아티스트 (YouTube 링크)' 한 줄 형식으로 출력해줘.\n키워드: {', '.join(keywords)}"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.8,
            max_tokens=400
        )
        # 가능한 여러 포맷 안전 처리
        try:
            content = response.choices[0].message["content"]
        except Exception:
            try:
                content = response.choices[0].message.content
            except Exception:
                content = str(response)
    except Exception as e:
        # 오류를 래핑해서 상위에서 처리하도록
        raise RuntimeError(f"OpenAI 호출 실패: {e}") from e

    # 간단 파싱: 각 줄을 "제목 - 아티스트 (링크)"로 분해
    results = []
    import re
    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
    for ln in lines:
        ln_no_num = re.sub(r"^\d+\.\s*", "", ln)
        # 링크 추출
        link = None
        link_match = re.search(r"(https?://[^\s\)]+)", ln_no_num)
        if link_match:
            link = link_match.group(1).strip().rstrip(")")
            ln_no_num = re.sub(re.escape(link), "", ln_no_num).strip()
            ln_no_num = ln_no_num.strip("() ")
        # title / artist 분리
        if " - " in ln_no_num:
            title, artist = ln_no_num.split(" - ", 1)
        else:
            parts = ln_no_num.split("—")
            if len(parts) >= 2:
                title, artist = parts[0].strip(), parts[1].strip()
            else:
                title, artist = ln_no_num, ""
        results.append({"title": title.strip(), "artist": artist.strip(), "youtube": link})
        if len(results) >= max_results:
            break
    return results

# -------------------
# Streamlit UI
# -------------------
st.set_page_config(page_title="🎧 안정형 음악 추천기", page_icon="🎶")
st.title("🎤 키워드 기반 음악 추천기 (AI 우선, 실패 시 자체추천)")

st.write("키워드를 입력하고 엔터로 추가하세요. 여러 개 추가한 뒤 '추천 받기' 버튼을 누르세요.")

# 세션 상태 초기화
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

# 디버그: 설치된 openai 버전 보기 (숨김 가능)
try:
    import importlib, pkgutil
    openai_spec = importlib.util.find_spec("openai")
    if openai_spec:
        import openai
        with st.expander("디버그: openai 버전 (클릭해서 보기)"):
            st.write("openai.__version__:", getattr(openai, "__version__", "unknown"))
    else:
        with st.expander("디버그: openai 정보 (클릭해서 보기)"):
            st.write("openai 패키지가 설치되어 있지 않습니다.")
except Exception:
    pass

# 추천 처리
if st.button("🎶 추천 받기") and st.session_state["keywords"]:
    keywords = st.session_state["keywords"]
    used_ai = False
    ai_error_msg = ""
    # 시도: OpenAI (구버전)
    try:
        # only attempt if openai is installed
        import importlib
        if importlib.util.find_spec("openai"):
            with st.spinner("AI 추천 시도 중..."):
                ai_results = ai_recommend_openai_028(keywords, max_results=3)
                if ai_results:
                    st.subheader("🎵 AI 추천 결과:")
                    for i, item in enumerate(ai_results, start=1):
                        st.markdown(f"{i}. **{item.get('title','')}** - {item.get('artist','')}")
                        if item.get("youtube"):
                            st.video(item.get("youtube"))
                    used_ai = True
                else:
                    ai_error_msg = "AI가 유효한 결과를 반환하지 않았습니다."
        else:
            ai_error_msg = "openai 라이브러리 미설치"
    except Exception as e:
        ai_error_msg = str(e) + "\n" + traceback.format_exc()

    # AI 실패시 로컬 추천
    if not used_ai:
        st.info(f"⚠️ AI 추천 불가 — 자체 추천으로 대체합니다. (원인: {ai_error_msg.splitlines()[0]})")
        local = local_recommend(keywords, max_results=3)
        if not local:
            st.warning("🔎 입력한 키워드와 매칭되는 노래가 없습니다.")
        else:
            st.subheader("🎵 자체 추천 결과:")
            for i, s in enumerate(local, start=1):
                st.markdown(f"{i}. **{s['title']}** - {s['artist']}")
                if s.get("youtube"):
                    st.video(s.get("youtube"))
