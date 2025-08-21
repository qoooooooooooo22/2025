# edu_site.py
import streamlit as st

# 1. 사이트 제목
st.title("📚 EduSmart - 당신을 위한 스마트 교육 플랫폼")
st.markdown("### 원하는 과목을 선택하고, 학습을 시작하세요!")

# 2. 과목 선택
subject = st.selectbox("과목 선택", ["국어", "영어", "수학", "과학", "사회"])

# 3. 주제별 요약 정보
st.markdown("---")
st.subheader(f"🔍 {subject} 요약 강의")

if subject == "국어":
    st.write("오늘의 주제: 비문학 독해\n- 핵심 키워드 찾기\n- 글의 구조 파악하기")
elif subject == "영어":
    st.write("오늘의 주제: 관계대명사\n- who, which, that 차이점 정리\n- 예문 학습")
elif subject == "수학":
    st.write("오늘의 주제: 이차방정식\n- 근의 공식\n- 판별식의 의미")
elif subject == "과학":
    st.write("오늘의 주제: 광합성\n- 엽록체 역할\n- 빛의 흡수와 에너지 전환")
elif subject == "사회":
    st.write("오늘의 주제: 민주주의\n- 삼권분립\n- 시민의 권리와 의무")

# 4. 간단한 퀴즈 기능
st.markdown("---")
st.subheader("📝 퀴즈 테스트")
quiz_answer = st.text_input("Q1. '대한민국의 수도는 어디일까요?'")

if st.button("정답 확인"):
    if quiz_answer.strip() == "서울":
        st.success("정답입니다! 🎉")
    else:
        st.error("틀렸습니다. 정답은 '서울'입니다.")

# 5. 파일 업로드 / 다운로드
st.markdown("---")
st.subheader("📤 과제 업로드")
uploaded_file = st.file_uploader("과제를 PDF 또는 DOCX 형식으로 제출하세요.", type=['pdf', 'docx'])

if uploaded_file:
    st.success(f"{uploaded_file.name} 업로드 완료!")

# 다운로드 예시
st.markdown("---")
st.subheader("📥 강의자료 다운로드")
with open("sample_lecture.txt", "w") as f:
    f.write("이것은 예시 강의자료입니다.\nStreamlit으로 만든 교육 플랫폼입니다.")
with open("sample_lecture.txt", "rb") as f:
    st.download_button("강의자료 받기", f, file_name="lecture.txt")

# 끝
st.markdown("---")
st.caption("© 2025 EduSmart Inc.")

