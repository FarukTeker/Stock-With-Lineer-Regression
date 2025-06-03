import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
from pathlib import Path

DATA_FILE = Path('SP 500 Stock Prices 2014-2017.csv')
NEW_DATA_FILE = Path('recent_data.csv')
MODEL_FILE = Path('model.pkl')

hist_df = pd.read_csv(DATA_FILE)

if NEW_DATA_FILE.exists():
    new_df = pd.read_csv(NEW_DATA_FILE)
    hist_df = pd.concat([hist_df, new_df], ignore_index=True)

hist_df['date'] = pd.to_datetime(hist_df['date'])
hist_df = hist_df.sort_values(['symbol', 'date'])
hist_df['close_tomorrow'] = hist_df.groupby('symbol')['close'].shift(-1)
hist_df = hist_df.dropna(subset=['close_tomorrow'])

feature_cols = ['open', 'high', 'low', 'close', 'volume']
X = hist_df[feature_cols]
y = hist_df['close_tomorrow']

# Replace any remaining NaN values
X = X.fillna(method='ffill').fillna(method='bfill')

model = LinearRegression()
model.fit(X, y)

joblib.dump(model, MODEL_FILE)
print('Model trained and saved to', MODEL_FILE)
