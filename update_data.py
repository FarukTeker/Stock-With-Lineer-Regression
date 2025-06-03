import yfinance as yf
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

SYMBOL = 'AAPL'
DATA_FILE = Path('recent_data.csv')

def fetch():
    if DATA_FILE.exists():
        existing = pd.read_csv(DATA_FILE)
        if not existing.empty:
            last_date = pd.to_datetime(existing['date']).max()
        else:
            last_date = datetime.utcnow() - timedelta(days=30)
    else:
        existing = pd.DataFrame()
        last_date = datetime.utcnow() - timedelta(days=30)

    start = last_date + timedelta(days=1)
    end = datetime.utcnow()

    if start > end:
        print('No new data to fetch')
        return existing

    df = yf.download(SYMBOL, start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'))
    df = df.reset_index()[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
    df['symbol'] = SYMBOL
    new_data = df[['symbol', 'date', 'open', 'high', 'low', 'close', 'volume']]
    all_data = pd.concat([existing, new_data], ignore_index=True)
    all_data.to_csv(DATA_FILE, index=False)
    print('Fetched and saved', len(new_data), 'rows')
    return all_data

def main():
    fetch()

if __name__ == '__main__':
    main()
