from traceback import format_list

import requests

base_url_mexc = "http://api.mexc.com"

def get_tickers(symbol:str) -> list[dict]:
    url = f'{base_url_mexc}/api/v3/ticker/24hr'
    params = {"symbol": symbol}
    if symbol:
        params["symbol"] = symbol.upper()

    r = requests.get(url, params=params, timeout=10)
    r.raise_for_status()

    data = r.json()

    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data

    raise RuntimeError(f'Unexpected response type: {type(data)}')

def parse_ticker_fields(t: dict) -> dict:
    return {
        "symbol": t.get("symbol"),
        "lastPrice": float(t["lastPrice"]) if "lastPrice" in t else None,
        "volume": float(t["volume"]) if "volume" in t else None,
    }

if __name__ == "__main__":
    tickers = get_tickers(symbol = None)
    print("Всего тикеров(mexc):", len(tickers))

    MIN_VOLUME_24H = 1000000
    filtered_tickers = []
    for ticker in tickers:
        sym = ticker.get("symbol") or ""
        if not sym.endswith("USDT"):
            continue
        vol = float(ticker.get("volume", 0) or 0)
        if vol < MIN_VOLUME_24H:
            continue
        filtered_tickers.append(ticker)
    print('Кандидаты в "хорошие" монеты после фильтра по USDT и volume:', len(filtered_tickers))

