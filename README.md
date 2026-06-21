# Crypto Radar AI - 텔레그램 변동성 알림 봇

Bitget 선물(USDT-M) 시세를 감시하다가 1분봉/5분봉 변동률이 임계값을 넘으면
캔들차트 이미지와 함께 텔레그램으로 알림을 보내는 봇입니다.

## 1. 사전 준비

### 텔레그램 봇 토큰 발급
1. 텔레그램에서 `@BotFather` 검색 → `/newbot` 실행
2. 봇 이름/유저네임 설정 후 발급되는 토큰 복사 (`TELEGRAM_BOT_TOKEN`)

### 채팅 ID 확인
1. 만든 봇과 1:1 대화를 시작하거나, 알림 받을 그룹에 봇을 초대
2. 아무 메시지나 하나 보낸 뒤, 브라우저에서 아래 주소 접속
   `https://api.telegram.org/bot<여기에 토큰>/getUpdates`
3. 응답 JSON에서 `chat.id` 값 확인 (`TELEGRAM_CHAT_ID`)

## 2. 로컬 실행

```bash
pip install -r requirements.txt

export TELEGRAM_BOT_TOKEN="발급받은 토큰"
export TELEGRAM_CHAT_ID="채팅 ID"

python main.py
```

## 3. Railway 배포

1. 이 폴더를 GitHub 레포로 push
2. Railway → New Project → Deploy from GitHub repo 선택
3. Variables 탭에서 환경변수 등록
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Settings → Start Command가 비어있으면 `python main.py`로 지정
   (Procfile이 있으므로 자동 인식되는 경우가 많습니다)
5. Deploy 후 로그에서 `Crypto Radar AI 봇 시작` 메시지 확인

> Hobby 플랜 기준으로도 충분히 동작합니다 (이전 변동성 봇과 동일한 방식).

## 4. 설정 커스터마이징 (`config.py`)

| 항목 | 설명 |
|---|---|
| `SYMBOLS` | 감시할 코인 목록 (ccxt unified 심볼, 예: `"ETH/USDT:USDT"`) |
| `THRESHOLDS` | 1분봉/5분봉 변동률 알림 임계값(%) |
| `DETECTION_LEVELS` | 변동률 크기에 따른 탐지레벨(1~5) 매칭 기준 |
| `COOLDOWN_SECONDS` | 같은 코인 재알림까지 최소 대기시간(초) — 도배 방지 |
| `CHECK_INTERVAL_SECONDS` | 시세 체크 주기(초) |
| `CHART_CANDLE_COUNT` | 차트에 표시할 1분봉 캔들 개수 |

여러 코인을 감시하려면 `SYMBOLS`에 추가하면 됩니다. 코인마다 독립적으로
쿨다운이 적용되어 한 코인의 알림이 다른 코인 알림을 막지 않습니다.

## 5. 동작 방식 요약

1. 매 60초(`CHECK_INTERVAL_SECONDS`)마다 각 심볼의 1분/5분/일봉 데이터를 조회
2. 1분봉 또는 5분봉 변동률이 임계값을 넘으면 알림 후보로 판단
3. 1분봉 변동률 절대값으로 탐지레벨(1~5단계) 계산
4. 최근 60개 1분봉으로 캔들차트 이미지 생성
5. 텍스트 알림 + 차트 이미지를 텔레그램으로 전송 (쿨다운 내 중복 전송 방지)

## 6. 확장 아이디어

- Upbit/Bithumb 시세와 크로스체크해서 "해외-국내 괴리율" 같이 표시 (이전 봇 로직 재사용 가능)
- 거래량 급증도 함께 감지해서 "세력 움직임" 코멘트 정교화
- 레벨별로 다른 이모지/문구 적용
- 다수 코인 동시 감시 + 코인별 알림 채널 분리
