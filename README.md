### 🤖 AI 감정 기반 마케팅 메시지 자동화 서비스

고객 리뷰 또는 문의 내용을 입력하면, AI가 감정을 분석하고
해당 감정에 맞는 마케팅 메시지를 자동 생성한 뒤 이메일로 발송하는
**실전형 CRM 자동화 도구**입니다.

---

### 🎯 프로젝트 개요

- 고객 리뷰 감정 분석 → 메시지 생성 → 이메일 발송 → 피드백 수집까지 자동화
- 실무에서 자주 등장하는 **감정 중심 고객 응대**를 AI로 해결하고자 기획
- OpenAI API + Streamlit + SMTP + SQLite 조합으로 빠르게 MVP 구현

---

### 🧠 주요 기능

| 기능 | 설명 |
|------|------|
| 감정 분석 (GPT) | 고객 리뷰에서 감정(긍/중립/부정) 분류  |
| 마케팅 메시지 생성 | 감정 + 문체 기반으로 자동 메시지 작성  |
| 쿠폰 삽입 | 부정 감정 시 자동 쿠폰 코드 안내  |
| 이메일 발송 | 입력된 이메일로 바로 메시지 전송  |
| 피드백 수집 | 메시지에 대해 👍👎 클릭 가능  |
| 감정 통계 시각화 | 시간대별 감정 추이 그래프 등 제공  |
| SQLite 저장 | 분석 결과 로컬 DB에 저장  |

---

### 🛠️ 사용 기술

- Python / Streamlit (웹 UI 및 로직 구성)
- OpenAI GPT-3.5 (텍스트 분석 및 메시지 생성)
- SQLite (로컬 DB 저장)
- SMTP (Gmail 앱 비밀번호 기반 이메일 발송)
- matplotlib / pandas (감정 통계 시각화)

---

### 🧪 시연 예시 흐름

1. 고객 리뷰 입력 → GPT 감정 분석
2. 감정 + 문체 기반 마케팅 메시지 생성
3. 부정 감정 시 쿠폰 삽입
4. 이메일 자동 발송
5. 감정/시간대 통계 시각화 + 피드백 수집

---

### 🔧 설치 및 실행 방법

```bash
# 필수 라이브러리 설치
pip install -r requirements.txt

# 실행
streamlit run app.py
```

> `.streamlit/secrets.toml` 파일에 아래처럼 키를 등록해야 합니다:

```toml
OPENAI_API_KEY = "sk-..."
EMAIL = "your_email@gmail.com"
EMAIL_PASSWORD = "앱 비밀번호"
```

---

### 🔗 배포 링크 & 저장소

- 배포 링크: https://ai-marketing-message-2qcbof8sejevxz3cfjnhs8.streamlit.app/
- GitHub: [https://github.com/your-name/emotion-marketing-app](https://github.com/SNSSNSKSSK/ai-marketing-message)

---

### 🧠 회고 및 학습 포인트

- AI의 언어 분석 능력을 마케팅 도구로 활용한 첫 실전 프로젝트
- GPT의 답변을 단순히 받는 것이 아니라, **실무 자동화 흐름에 통합**하는 설계 경험
- Streamlit + GPT + SMTP + DB까지 전 과정을 손으로 구현해본 점에서 큰 성취감 있음

---

### 🙋 기타 참고

- 프로젝트 프롬프트 테스트: [https://gptonline.ai/ko](https://gptonline.ai/ko)

---

> 이 프로젝트는 감정 중심 마케팅 자동화 가능성을 탐색하고,
> 실무형 GPT 응용 능력을 포트폴리오로 증명하기 위해 제작되었습니다.
