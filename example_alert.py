"""
예시 알림을 딱 한 번 전송하는 스크립트.
Railway Console에서 `python3 example_alert.py` 로 실행하세요.
실제 BTC 데이터로 차트를 만들되, 임계값과 상관없이 강제로 전송합니다.
"""
import asyncio
import io

from telegram import Bot

import config
from exchange import get_exchange, fetch_ohlcv_df, calc_change_pct
from chart import generate_chart_image
from alert import build_alert_message


async def main():
    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    exchange = get_exchange()

    symbol = "BTC/USDT:USDT"
    df_1m = fetch_ohlcv_df(exchange, symbol, "1m", limit=config.CHART_CANDLE_COUNT)
    df_5m = fetch_ohlcv_df(exchange, symbol, "5m", limit=10)
    df_1d = fetch_ohlcv_df(exchange, symbol, "1d", limit=5)

    c1 = calc_change_pct(df_1m)
    c5 = calc_change_pct(df_5m)
    c1d = calc_change_pct(df_1d)
    price = float(df_1m["close"].iloc[-1])

    level = 3  # 예시용으로 임의 지정 (실제 변동률과 무관)
    label = "BTC"
    msg = "📋 [예시 알림 - 실제 변동성과 무관]\n\n" + build_alert_message(label, price, c1, c5, c1d, level)

    chart_df = df_1m.tail(config.CHART_CANDLE_COUNT)
    img_buf = generate_chart_image(chart_df, label, c1)
    img_bytes = img_buf.getvalue()

    for chat_id in config.TELEGRAM_CHAT_IDS:
        photo = io.BytesIO(img_bytes)
        await bot.send_photo(chat_id=chat_id, photo=photo, caption=msg)
        print(f"전송 완료 → {chat_id}")


if __name__ == "__main__":
    asyncio.run(main())
