# USE VPN BEFORE RUN
import requests

base_url_htx = "https://api.huobi.pro"

def get_tickers(symbol: str) -> list[dict]:
    url = f'{base_url_htx}/market/tickers'

    r = requests.get(url, timeout=10)
    r.raise_for_status()

    data = r.json()
    if data.get("status") != "ok":
        raise RuntimeError(f'HTX error: status = {data.get("status")}, error_msg = {data.get("err-msg")}')

    tickers = data["data"]

    if symbol:
        s = symbol.lower()
        tickers = [t for t in tickers if t.get("symbol") == s]

    return tickers

def get_bsc_coins() -> set[str]:
    url = f'{base_url_htx}/v2/reference/currencies'
    r = requests.get(url,timeout=10)
    r.raise_for_status()
    data = r.json()
    if data.get("code") != 200:
        raise RuntimeError(f'HTX error: code = {data.get("code")}, message = {data.get("message")}')

    bsc = set()
    for item in data.get("data", []):
        coin = (item.get("currency") or "").upper()
        chains = item.get("chains") or []
        for ch in chains:
            chain_name = (ch.get("chain") or "").lower()
            if "bsc" in chain_name or "bep20" in chain_name:
                bsc.add(coin)
                break
    return bsc

def parse_ticker_fields(t:dict) -> dict:
    return {
        "symbol": (t.get("symbol") or "").upper(),
        "lastPrice": float(t["close"]) if "close" in t else None,
        "volume24h": float(t["amount"]) if "amount" in t else None,
    }

if __name__ == "__main__":
    tickers = get_tickers(None)
    print("Всего тикеров(htx):", len(tickers))
    bsc_coins = get_bsc_coins()
    print("Монет с сетью BSC:", len(bsc_coins))

    MIN_VOLUME_24H = 1000000
    filtered_tickers = []
    for ticker in tickers:
        sym = ticker.get("symbol") or ""
        if not sym.endswith("usdt"):
            continue

        base_coin = sym[:-4].upper()
        if base_coin not in bsc_coins:
            continue

        vol = float(ticker.get("amount",0) or 0)
        if vol < MIN_VOLUME_24H:
            continue
        filtered_tickers.append(ticker)
    print('Кандидаты в "хорошие" монеты после фильтра по USDT и volume:', len(filtered_tickers))

