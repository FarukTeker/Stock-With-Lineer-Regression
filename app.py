from flask import Flask, render_template_string
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import joblib
from pathlib import Path
from datetime import datetime
import update_data

MODEL_FILE = Path('model.pkl')
DATA_FILE = Path('recent_data.csv')

app = Flask(__name__)

latest_close = None
latest_pred = None

@app.route('/')
def index():
    global latest_close, latest_pred
    if latest_close is None or latest_pred is None:
        status = 'No data yet.'
    else:
        status = f'Latest close: {latest_close:.2f}, Predicted next close: {latest_pred:.2f}'
    return render_template_string('<h1>Stock Predictor</h1><p>{{status}}</p>', status=status)

def update():
    global latest_close, latest_pred
    update_data.main() if hasattr(update_data, 'main') else None
    if DATA_FILE.exists() and MODEL_FILE.exists():
        df = pd.read_csv(DATA_FILE)
        df['date'] = pd.to_datetime(df['date'])
        last_row = df.sort_values('date').iloc[-1]
        latest_close = last_row['close']
        model = joblib.load(MODEL_FILE)
        feature_cols = ['open', 'high', 'low', 'close', 'volume']
        X_new = last_row[feature_cols].values.reshape(1, -1)
        latest_pred = model.predict(X_new)[0]
        print(f'Updated prediction at {datetime.utcnow()}')

scheduler = BackgroundScheduler()
scheduler.add_job(update, 'cron', hour=17, minute=0)
scheduler.start()

# initial update on startup
update()

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
