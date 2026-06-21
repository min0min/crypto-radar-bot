import asyncio
import logging
import time

from telegram import Bot

import config
from exchange import get_exchange, fetch_ohlcv_df, calc_change_pct
from chart import generate_chart_image
from alert import get_detection_level, build_alert_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("crypto-radar")

# 심볼별 마지막 알림 전송 시각 (쿨다운 관리용)
_last_alert_time: dict[str, float] = {}


async def send_alert(bot: Bot, symbol: str, price: float,
                      c1: float, c5: float, c1d: float, chart_df) -> None:
    level = get_detection_level(abs(c1), config.DETECTION_LEVELS)
    if level == 0:
        return

    now = time.time()
    last = _last_alert_time.get(symbol, 0)
    if now - last < config.COOLDOWN_SECONDS:
        return
    _last_alert_time[symbol] = now

    label = symbol.split("/")[0]
    msg = build_alert_message(label, price, c1, c5, c1d, level)
    img_buf = generate_chart_image(chart_df, label, c1)

    await bot.send_photo(chat_id=config.TELEGRAM_CHAT_ID, photo=img_buf, caption=msg)
    log.info(f"알림 전송 완료: {symbol} level={level} 1m={c1:.2f}% 5m={c5:.2f}%")


async def check_symbol(bot: Bot, exchange, symbol: str) -> None:
    try:
        df_1m = fetch_ohlcv_df(exchange, symbol, "1m", limit=max(config.CHART_CANDLE_COUNT, 10))
        df_5m = fetch_ohlcv_df(exchange, symbol, "5m", limit=10)
        df_1d = fetch_ohlcv_df(exchange, symbol, "1d", limit=5)

        c1 = calc_change_pct(df_1m)
        c5 = calc_change_pct(df_5m)
        c1d = calc_change_pct(df_1d)
        price = float(df_1m["close"].iloc[-1])

        if abs(c1) >= config.THRESHOLDS["1m"] or abs(c5) >= config.THRESHOLDS["5m"]:
            chart_df = df_1m.tail(config.CHART_CANDLE_COUNT)
            await send_alert(bot, symbol, price, c1, c5, c1d, chart_df)

    except Exception as e:
        log.error(f"{symbol} 체크 중 오류 발생: {e}")


async def main_loop() -> None:
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        raise RuntimeError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 환경변수를 설정해주세요.")

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    exchange = get_exchange()

    log.info("Crypto Radar AI 봇 시작 — 감시 심볼: %s", config.SYMBOLS)

    while True:
        for symbol in config.SYMBOLS:
            await check_symbol(bot, exchange, symbol)
        await asyncio.sleep(config.CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main_loop())
