import os

# ── 텔레그램 설정 ─────────────────────────────────────────
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# ── 감시할 심볼 (Bitget 선물(USDT-M) 기준, ccxt unified symbol) ──
SYMBOLS = [
    "BTC/USDT:USDT",
    "ETH/USDT:USDT",
    "SOL/USDT:USDT",
]

# ── 변동률 감지 임계값 (%) - 이 값을 넘으면 알림 후보가 됩니다 ──
THRESHOLDS = {
    "1m": 0.3,
    "5m": 0.5,
}

# ── 탐지레벨 기준표 (1분봉 변동률 절대값 % 기준) ──
# (임계값, 레벨) - 값이 클수록 더 높은 레벨로 매칭됩니다.
DETECTION_LEVELS = [
    (0.3, 1),
    (0.6, 2),
    (1.0, 3),
    (1.5, 4),
    (2.5, 5),
]
MAX_LEVEL = 5

# ── 동일 심볼 재알림 방지 쿨다운 (초) ──
COOLDOWN_SECONDS = 300

# ── 체크 주기 (초) ──
CHECK_INTERVAL_SECONDS = 60

# ── 알림에 첨부할 차트 설정 ──
CHART_TIMEFRAME = "1m"
CHART_CANDLE_COUNT = 60
