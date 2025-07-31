import streamlit as st
import openai

# GPT API 키 (Streamlit Cloud에서는 Secrets 기능으로 관리됨)
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="AI 감정 기반 마케팅 메시지 생성기")
st.title("🧠 감정 맞춤 마케팅 메시지 생성기")

st.markdown("고객의 리뷰를 입력하면 AI가 감정을 분석하고, 감정에 맞는 메시지를 자동으로 생성해줍니다.")

# 1. 사용자 입력
review = st.text_area("✍️ 고객 리뷰 또는 문의 내용을 입력하세요:", height=150)

if review:
    with st.spinner("AI가 감정을 분석하고 메시지를 작성하는 중..."):
        # 2. 감정 분석 프롬프트
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

        # 3. 메시지 생성 프롬프트
        message_prompt = f"""
        고객이 남긴 리뷰: "{review}"
        감정: {emotion}
        문체: 정중하고 브랜드 친화적으로
        목적: 감정에 맞는 맞춤형 마케팅 메시지를 생성해줘 (필요 시 쿠폰 안내 포함)
        """

        message_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message_prompt}]
        )
        message = message_response.choices[0].message.content.strip()

    # 4. 결과 출력
    st.markdown(f"### 🧠 감정 분석 결과: `{emotion}`")
    st.markdown("---")
    st.markdown("### 📩 생성된 마케팅 메시지:")
    st.success(message)

    # 5. 복사 or 다운로드
    st.download_button("💾 메시지 저장하기", data=message, file_name="marketing_message.txt", mime="text/plain")
