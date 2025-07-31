import streamlit as st
import openai
import matplotlib.pyplot as plt
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import sqlite3

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

# SQLite DB 연결
conn = sqlite3.connect("customer_data.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    name TEXT,
    email TEXT,
    review TEXT,
    emotion TEXT,
    tag TEXT,
    message TEXT,
    timestamp TEXT
)
""")
conn.commit()

def save_to_db(name, email, review, emotion, tag, message, timestamp):
    c.execute("INSERT INTO messages VALUES (?, ?, ?, ?, ?, ?, ?)",
              (name, email, review, emotion, tag, message, timestamp))
    conn.commit()

# 세션 초기화
if "emotion_counts" not in st.session_state:
    st.session_state.emotion_counts = {"긍정": 0, "중립": 0, "부정": 0}
if "history" not in st.session_state:
    st.session_state.history = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# 탭 구성
input_tab, dashboard_tab = st.tabs(["📥 입력 및 생성", "📊 분석 대시보드"])

with input_tab:
    with st.form("user_info"):
        name = st.text_input("고객 이름")
        email = st.text_input("이메일 주소")
        review = st.text_area("✍️ 고객 리뷰 또는 문의 내용을 입력하세요:", height=150)
        tone = st.selectbox("문체 선택", ["정중한 톤", "친근한 말투", "브랜드 중심 톤"])
        submitted = st.form_submit_button("리뷰 분석 및 메시지 생성")

    if submitted and review:
        with st.spinner("AI가 분석 중입니다..."):
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

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
            st.session_state.emotion_counts[emotion] += 1

            # 리뷰 주제 태깅
            tag_prompt = f"""
            고객 리뷰: "{review}"
            이 리뷰의 주제를 한 단어로 태그해줘 (예: 배송, 가격, 품질 등):
            """
            tag_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": tag_prompt}]
            )
            topic = tag_response.choices[0].message.content.strip()

            # 마케팅 메시지 생성
            message_prompt = f"""
            고객 리뷰: "{review}"
            감정: {emotion}
            문체: {tone}
            목적: 감정에 맞는 맞춤형 마케팅 메시지를 생성해줘 (필요 시 쿠폰 안내 포함)
            """
            message_response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": message_prompt}]
            )
            message = message_response.choices[0].message.content.strip()

            if "부정" in emotion:
                coupon_code = "WELCOME10"
                message += f"\n\n🎁 위로의 마음으로 할인코드 `{coupon_code}` 를 드립니다!"

            st.markdown(f"### 🧠 감정 분석 결과: `{emotion}`")
            st.markdown(f"**토픽 태그**: `{topic}`")
            st.markdown("### 📩 생성된 마케팅 메시지:")
            st.success(message)

            # DB 저장
            save_to_db(name, email, review, emotion, topic, message, timestamp)

            # CSV 저장용
            st.session_state.history.append({
                "이름": name,
                "이메일": email,
                "리뷰": review,
                "감정": emotion,
                "태그": topic,
                "메시지": message,
                "시간": timestamp
            })

            # 피드백 버튼
            st.markdown("### 💬 이 메시지가 마음에 드시나요?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👍 좋아요"):
                    st.session_state.feedback.append({"리뷰": review, "피드백": "좋음"})
            with col2:
                if st.button("👎 아쉬워요"):
                    st.session_state.feedback.append({"리뷰": review, "피드백": "아쉬움"})

            # 이메일 전송
            if st.button("📧 이메일로 보내기"):
                send_email(email, "AI 감정 메시지", message)
                st.success("✅ 이메일이 성공적으로 전송되었습니다!")

            # CSV 다운로드
            df = pd.DataFrame(st.session_state.history)
            st.download_button("📥 전체 결과 다운로드 (CSV)", df.to_csv(index=False), file_name="emotion_results.csv")

with dashboard_tab:
    st.header("📊 감정 통계 및 피드백")

    # 감정 카운트
    fig, ax = plt.subplots()
    labels = list(st.session_state.emotion_counts.keys())
    values = list(st.session_state.emotion_counts.values())
    ax.bar(labels, values, color=["green", "gray", "red"])
    st.pyplot(fig)

    # 시간대 추이 분석
    if st.session_state.history:
        st.subheader("⏱ 감정 시간대 변화 추이")
        df_time = pd.DataFrame(st.session_state.history)
        df_time['시간'] = pd.to_datetime(df_time['시간'])
        emotion_trend = df_time.groupby([df_time['시간'].dt.hour, '감정']).size().unstack(fill_value=0)
        st.line_chart(emotion_trend)

    # 피드백 요약
    st.subheader("💬 피드백 통계")
    if st.session_state.feedback:
        df_feedback = pd.DataFrame(st.session_state.feedback)
        feedback_count = df_feedback['피드백'].value_counts()
        st.bar_chart(feedback_count)


