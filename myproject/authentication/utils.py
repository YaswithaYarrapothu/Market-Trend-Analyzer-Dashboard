def fetch_market_data(symbol, years):
    import streamlit as st
    import yfinance as yf
    import plotly.graph_objects as go
    from datetime import date , timedelta
    import pandas as pd

    end_date = date.today()
    start_date = end_date - timedelta(days=years * 365)

    # Fetch stock data
    data = yf.download(symbol, start=start_date, end=end_date)
    data.reset_index(inplace=True)

    # Generate plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name='Stock_Open'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name='Stock_Close'))
    fig.layout.update(title_text="Time Series Data", xaxis_rangeslider_visible=True)

    # Convert Plotly graph to HTML for embedding in Django template
    plot_html = fig.to_html(full_html=False)

    return data, plot_html
