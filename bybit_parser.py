from logging import lastResort

import requests

base_url_bybit = "https://api.bybit.com"

def get_tickers(category: str, symbol: str) -> list[dict]:
    url = f'{base_url_bybit}/v5/market/tickers'
    params = {"category": category}
    if symbol:
        params["symbol"] = symbol

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()
    if data.get("retCode") != 0:
        raise RuntimeError(f'Bybit error: retCode={data.get("retCode")}, retMsg={data.get("retMsg")}')

    return data["result"]["list"]

def parse_ticker_fields(t: dict) -> dict:
    return {
        "symbol": t.get("symbol"),
        "lastPrice": float(t["lastPrice"]) if "lastPrice" in t else None,
        #"bid1Price": float(t["bid1Price"]) if "bid1Price" in t else None,
        #"ask1Price": float(t["ask1Price"]) if "ask1Price" in t else None,
        "volume24h": float(t["volume24h"]) if "volume24h" in t else None,
        #"turnover24h": float(t["turnover24h"]) if "turnover24h" in t else None,
        #"price24hPcnt": float(t["price24hPcnt"]) if "price24hPcnt" in t else None,
    }

if __name__ == "__main__":
    tickers = get_tickers(category="spot", symbol=None)
    print("Всего тикеров(bybit):", len(tickers))

    MIN_VOLUME_24H = 1000000
    filtered_tickers = []
    for ticker in tickers:
        sym = ticker.get("symbol") or ""
        if not sym.endswith("USDT"):
            continue
        vol = float(ticker.get("volume24h", 0) or 0)
        if vol < MIN_VOLUME_24H:
            continue
        filtered_tickers.append(ticker)

    print(f'Кандидаты в "хорошие" монеты после фильтра по USDT и volume:', len(filtered_tickers))