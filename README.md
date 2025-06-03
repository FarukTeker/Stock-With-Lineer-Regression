# Stock Price Predictor

This project demonstrates training a simple model on S&P 500 data and updating predictions with daily market data. The included scripts allow you to fetch recent prices, retrain the model, and serve the latest prediction through a small web application.

## Setup

1. Install the dependencies:

```bash
pip install -r requirements.txt
```

2. Fetch the latest data and train the model:

```bash
python update_data.py
python train_model.py
```

3. Start the web server:

```bash
python app.py
```

The server schedules a daily task at 17:00 UTC to download the most recent closing price for `AAPL` and update the prediction shown on the main page.
