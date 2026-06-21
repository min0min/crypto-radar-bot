import io
import mplfinance as mpf
import pandas as pd


def generate_chart_image(df: pd.DataFrame, symbol_label: str, change_pct: float) -> io.BytesIO:
    """캔들차트를 PNG 이미지(BytesIO)로 생성해서 반환"""
    mc = mpf.make_marketcolors(
        up="#26a69a", down="#ef5350",
        edge="inherit", wick="inherit", volume="inherit",
    )
    style = mpf.make_mpf_style(
        base_mpf_style="nightclouds",
        marketcolors=mc,
        gridstyle="--",
        gridcolor="#2a2a3a",
        facecolor="#131722",
        figcolor="#131722",
    )

    buf = io.BytesIO()
    mpf.plot(
        df,
        type="candle",
        style=style,
        volume=True,
        title=f"\n{symbol_label}  ({change_pct:+.2f}%)",
        savefig=dict(fname=buf, dpi=130, bbox_inches="tight"),
    )
    buf.seek(0)
    return buf
