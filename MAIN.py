# edu_galaxy.py
import streamlit as st
import random

# 🎇 페이지 전체 스타일
st.set_page_config(page_title="EDU GALAXY 🌌", layout="wide")

# 🌟 타이틀 & 소개
st.markdown("""
# 🌌✨ **EDU GALAXY** 🚀📚  
### 🎓 당신을 위한 은하계 최강의 교육 플랫폼 🌈
---
""")

# 🌠 애니메이션 효과 느낌 주는 텍스트
taglines = [
    "📘 오늘도 한 페이지 성장하기 💪",
    "🌟 지식은 너를 빛나게 해 ✨",
    "🚀 지금부터 공부는 게임이다 🎮",
    "💡 작은 이해가 큰 변화를 만든다 🔥"
]
st.markdown(f"### {random.choice(taglines)}")

# 💫 과목 선택
st.markdown("## 🧠 과목 선택하기 🛸")
subject = st.selectbox("🎯 배우고 싶은 과목을 골라봐!", ["🌸 국어", "🌍 영어", "🧮 수학", "🔬 과학", "🧭 사회"])

# 📚 요약 콘텐츠
st.markdown("---")
st.markdown(f"## 📖 {subject} 요약 강의 🔥")

if "국어" in subject:
    st.success("📝 **주제: 비문학 독해**\n- 🔍 핵심 키워드 찾기\n- 🧠 문단 구조 파악하기\n- 💬 주제문 찾는 법 익히기")
elif "영어" in subject:
    st.success("📘 **주제: 관계대명사**\n- 🤓 who, which, that 차이점\n- 🧩 문장 속 쓰임 확인하기\n- 🧪 예문으로 연습!")
elif "수학" in subject:
    st.success("➗ **주제: 이차방정식**\n- 🧬 근의 공식 정복하기\n- 🧠 판별식과 해의 수 관계\n- 🧮 그래프로 확인!")
elif "과학" in subject:
    st.success("🌿 **주제: 광합성**\n- ☀️ 태양에너지의 변환\n- 🧪 엽록체 역할\n- 🌱 산소 발생 실험")
elif "사회" in subject:
    st.success("🏛️ **주제: 민주주의**\n- ⚖️ 삼권분립 구조\n- 🗳️ 시민의 권리와 의무\n- 🕊️ 공동체 의식 기르기")

# 🎯 퀴즈
st.markdown("---")
st.markdown("## 🧩 미니 퀴즈 타임! 🎉")
quiz_answer = st.text_input("❓ Q. '대한민국의 수도는 어디일까요?' 🇰🇷")

if st.button("🚨 정답 확인!"):
    if quiz_answer.strip() == "서울":
        st.balloons()
        st.success("🎊 정답입니다! 역시 똑똑이! 🧠💥")
    else:
        st.error("❌ 땡! 정답은 '서울'이에요! 📍")

# 📤 과제 업로드
st.markdown("---")
st.markdown("## 📤 과제 제출 존 ✍️")
uploaded_file = st.file_uploader("📎 PDF 또는 DOCX 파일을 올려줘요!", type=["pdf", "docx"])

if uploaded_file:
    st.success(f"✅ `{uploaded_file.name}` 업로드 완료! 🚀")

# 📥 강의자료 다운로드
st.markdown("---")
st.markdown("## 📚 강의자료 다운로드 📥")
with open("galaxy_lecture.txt", "w") as f:
    f.write("⭐ Welcome to EDU GALAXY!\n이것은 은하계 스타일 강의자료입니다.\n즐겁게 공부하세요!")
with open("galaxy_lecture.txt", "rb") as f:
    st.download_button("🌟 강의자료 받기", f, file_name="EDU_GALAXY_Lecture.txt")

# 🪐 마무리
st.markdown("---")
st.markdown("#### 👨‍🚀 오늘도 EDU GALAXY와 함께한 당신은 이미 우주급 인재! 💫")
st.caption("© 2025 EDU GALAXY Inc. | Powered by Streamlit 🌈")
