import streamlit as st
import openai
import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.text import MIMEText

# GPT API 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI 감정 기반 마케팅 메시지 생성기")
st.title("🧠 감정 맞춤 마케팅 메시지 생성기")

# 이메일 전송 함수
def send_email(to_email, subject, body):
    from_email = st.secrets["EMAIL"]
    app_password = st.secrets["EMAIL_PASSWORD"]

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(from_email, app_password)
    server.send_message(msg)
    server.quit()

# 사용자 정보 입력 폼
with st.form("user_info"):
    name = st.text_input("고객 이름")
    email = st.text_input("이메일 주소")
    review = st.text_area("✍️ 고객 리뷰 또는 문의 내용을 입력하세요:", height=150)
    submitted = st.form_submit_button("리뷰 분석 및 메시지 생성")

if submitted and review:
    with st.spinner("AI가 분석 중입니다..."):
        # 감정 분석 프롬프트
        emotion_prompt = f"""
        아래 고객 리뷰의 감정을 [긍정 / 중립 / 부정] 중 하나로 분류해줘:
        리뷰: "{review}"
        감정:
        """
        emotion_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": emotion_prompt}]
        )
        emotion = emotion_response.choices[0].message.content.strip()

        # 마케팅 메시지 생성 프롬프트
        message_prompt = f"""
        고객 리뷰: "{review}"
        감정: {emotion}
        문체: 정중하고 브랜드 친화적으로
        목적: 감정에 맞는 맞춤형 마케팅 메시지를 생성해줘 (필요 시 쿠폰 안내 포함)
        """
        message_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message_prompt}]
        )
        message = message_response.choices[0].message.content.strip()

        # 쿠폰 코드 삽입 (부정일 경우)
        if "부정" in emotion:
            coupon_code = "WELCOME10"
            message += f"\n\n🎁 위로의 마음으로 할인코드 `{coupon_code}` 를 드립니다!"

        # 감정 카운트 세션 저장
        if "emotion_counts" not in st.session_state:
            st.session_state.emotion_counts = {"긍정": 0, "중립": 0, "부정": 0}
        if emotion in st.session_state.emotion_counts:
            st.session_state.emotion_counts[emotion] += 1

        # 결과 출력
        st.markdown(f"### 🧠 감정 분석 결과: `{emotion}`")
        st.markdown("### 📩 생성된 마케팅 메시지:")
        st.success(message)

        # 결과 저장
        if "history" not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({
            "이름": name,
            "이메일": email,
            "리뷰": review,
            "감정": emotion,
            "메시지": message
        })

        # CSV 다운로드
        df = pd.DataFrame(st.session_state.history)
        st.download_button("📥 전체 결과 다운로드 (CSV)", df.to_csv(index=False), file_name="emotion_results.csv")

        # 감정 통계 시각화
        st.subheader("📊 감정 분석 통계")
        fig, ax = plt.subplots()
        labels = list(st.session_state.emotion_counts.keys())
        values = list(st.session_state.emotion_counts.values())
        ax.bar(labels, values, color=["green", "gray", "red"])
        st.pyplot(fig)

        # 이메일 전송 버튼
        if st.button("📧 이메일로 보내기"):
            send_email(email, "AI 감정 메시지", message)
            st.success("✅ 이메일이 성공적으로 전송되었습니다!")
