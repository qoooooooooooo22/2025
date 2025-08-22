import streamlit as st
import openai

# 🔑 OpenAI API 키 설정 (보안 위해 환경변수로 관리 추천)
openai.api_key = "YOUR_OPENAI_API_KEY"

# 🎧 페이지 설정
st.set_page_config(page_title="노래 추천기🎶", page_icon="🎸")
st.title("🎤 키워드를 입력하면 AI가 노래를 추천해줄게!")
st.markdown("ex) 감성, 기타, 몽환적인, 드라이브할 때 듣기 좋은 노래 등 자유롭게 입력하세요!")

# 사용자 입력
user_input = st.text_input("🎵 어떤 분위기의 노래를 원해?", placeholder="예: 잔잔하고 기타가 예쁜 노래")

# 결과 버튼
if st.button("🎶 노래 추천 받기") and user_input:
    with st.spinner("AI가 생각 중...💭"):
        prompt = f"""
        다음 키워드를 가진 한국 대중음악 추천 3곡을 해줘. 각 곡에는 제목, 아티스트, 유튜브 링크를 포함해줘.
        키워드: {user_input}

        출력 예시:
        1. 곡 제목 - 아티스트 (YouTube 링크)
        2. ...
        """

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # gpt-4도 가능
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8
            )
            answer = response.choices[0].message.content
            st.markdown("### ✅ 추천된 노래들:")
            st.markdown(answer)
        except Exception as e:
            st.error("❌ 에러가 발생했어요: " + str(e))

