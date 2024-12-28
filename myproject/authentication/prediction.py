import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import yfinance as yf

# Fetch historical stock data
def fetch_stock_data(symbol, start_date, end_date):
    ticker = yf.Ticker(symbol)
    data = ticker.history(start=start_date, end=end_date)
    return data


# Prepare the data
def prepare_data(data):
    # Create a column for the date as the number of days since the start
    data['Date'] = pd.to_datetime(data.index).map(pd.Timestamp.timestamp)
    X = data['Date'].values.reshape(-1, 1)  # Feature: Date
    y = data['Close'].values  # Target: Closing price
    return X, y

# Train a model
def train_model(X, y):
    model = LinearRegression()
    model.fit(X, y)
    return model

# Predict future trends
def predict_future(model, days=5):
    future_dates = np.array([pd.Timestamp.now().timestamp() + i * 86400 for i in range(1, days + 1)])
    predictions = model.predict(future_dates.reshape(-1, 1))
    return predictions, future_dates


# Generate Market Trend Report with plot
def generate_market_trend_report(symbol, start_date, end_date):
    data = fetch_stock_data(symbol, start_date, end_date)
    X, y = prepare_data(data)
    model = train_model(X, y)
    
    # Predict future trends (for example, 5 days ahead)
    predictions, future_dates = predict_future(model, days=5)
    
    # Visualize the prediction using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Historical Prices'))
    fig.add_trace(go.Scatter(x=pd.to_datetime(future_dates, unit='s'), y=predictions, mode='lines+markers', name='Predicted Prices'))
    
    fig.update_layout(title=f"Stock Price Prediction for {symbol}", xaxis_title="Date", yaxis_title="Price (USD)")
    predict_plot = fig.to_html(full_html = False)

    return predictions , future_dates , predict_plot
