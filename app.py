import streamlit as st
import openai

# API 키 불러오기
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI 감정 기반 마케팅 메시지 생성기")
st.title("🧠 감정 맞춤 마케팅 메시지 생성기")

review = st.text_area("✍️ 고객 리뷰 또는 문의 내용을 입력하세요:", height=150)

if review:
    with st.spinner("AI가 분석 중입니다..."):
        # 감정 분석
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

        # 마케팅 메시지 생성
        message_prompt = f"""
        고객 리뷰: "{review}"
        감정: {emotion}
        문체: 정중하고 브랜드 친화적으로
        목적: 감정에 맞는 맞춤형 마케팅 메시지를 생성해줘
        """
        message_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message_prompt}]
        )
        message = message_response.choices[0].message.content.strip()

    st.markdown(f"### 감정 분석 결과: `{emotion}`")
    st.markdown("### 생성된 메시지:")
    st.success(message)

    st.download_button("💾 메시지 저장하기", message, file_name="message.txt")

