import ccxt
import pandas as pd


def get_exchange():
    """Bitget 선물(USDT-M Perpetual) 거래소 객체 생성"""
    return ccxt.bitget({
        "options": {"defaultType": "swap"},
        "enableRateLimit": True,
    })


def fetch_ohlcv_df(exchange, symbol: str, timeframe: str, limit: int = 100) -> pd.DataFrame:
    """OHLCV 캔들 데이터를 pandas DataFrame으로 반환 (mplfinance 호환 포맷)"""
    raw = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df.set_index("timestamp", inplace=True)
    df = df.astype(float)
    return df


def calc_change_pct(df: pd.DataFrame) -> float:
    """가장 최근 캔들의 시가 대비 종가 변동률(%) 계산"""
    if df.empty:
        return 0.0
    last = df.iloc[-1]
    if last["open"] == 0:
        return 0.0
    return (last["close"] - last["open"]) / last["open"] * 100
