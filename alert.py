def get_detection_level(abs_change_1m: float, levels) -> int:
    """1분봉 변동률 절대값을 기준으로 탐지레벨(0~5)을 계산"""
    level = 0
    for threshold, lvl in levels:
        if abs_change_1m >= threshold:
            level = lvl
    return level


def level_bar(level: int, max_level: int = 5) -> str:
    level = max(0, min(level, max_level))
    return "■" * level + "□" * (max_level - level)


def build_alert_message(symbol_label: str, price: float, change_1m: float,
                         change_5m: float, change_1d: float, level: int) -> str:
    is_down = change_1m < 0
    direction = "급하락" if is_down else "급상승"
    arrow = "📉" if is_down else "📈"
    pressure = "강한 매도압력이 감지되었습니다." if is_down else "강한 매수세가 감지되었습니다."

    msg = (
        f"🔴 알림 🔴\n"
        f"{arrow} {symbol_label} {direction} 발생!\n"
        f"━━━━━━━━━━━━━\n"
        f"🔎 탐지레벨 : {level}단계 {level_bar(level)}\n\n"
        f"👉 현재가 : ${price:,.1f}\n"
        f"# 1분봉 : {change_1m:+.2f}%\n"
        f"# 5분봉 : {change_5m:+.2f}%\n"
        f"# 일봉 : {change_1d:+.2f}%\n\n"
        f"⚠️ {pressure}\n"
        f"👀 현명한 투자자들이 지켜보고 있습니다.\n\n"
        f"📕 해당 정보는 참고용이며 정보의 오류 등에 의한 손익은 책임지지 않습니다."
    )
    return msg
