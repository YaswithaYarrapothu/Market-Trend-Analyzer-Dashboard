def fetch_market_data(symbol, years):
    import streamlit as st
    import yfinance as yf #for company data
    import plotly.graph_objects as go #visualizations
    from datetime import date , timedelta
    import pandas as pd #preprocessing

    end_date = date.today()
    start_date = end_date - timedelta(days=years * 365)

    # Fetch stock data
    ticker = yf.Ticker(symbol)  # Initialize with just the symbol
    if start_date and end_date:  # Fetch historical data if dates are provided
        data = ticker.history(start=start_date, end=end_date)
        data.reset_index(inplace=True)
    else:  # Fetch current company info
        data = ticker.info
    df = pd.concat([data.head(), data.tail()])

    if isinstance(data, pd.DataFrame) and 'High' in data.columns and 'Low' in data.columns:
        # Pie Chart for High and Low values
        high_price = data['High'].iloc[-1]  # Most recent High
        low_price = data['Low'].iloc[-1]

    # Generate plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], mode='lines', name='Volume'))
    fig.update_layout(
    title='Volume Analysis',
    xaxis_title='Date',
    yaxis_title='Volume'
    )
    # Convert Plotly graph to HTML for embedding in Django template
    plot_html = fig.to_html(full_html=False)

    pie_chart = go.Figure(
                data=[go.Pie(labels=["High", "Low"], values=[high_price , low_price] ,hole = 0.3,marker=dict(colors=['#ff6666', '#66b3ff']))]
            ).to_html()

    # Bar Chart: Financial Metrics
    bar_chart = go.Figure(data=[
         go.Bar(x=data['Date'],y=[data['High'],data['Close'],data['Low'],data['Open']],marker=dict(color='rgb(0, 123, 255)'))
        ]
        ).to_html()
    #scatter-plot
    scatter_plot = go.Figure(data=go.Scatter(
    x=data['Volume'],  # x-axis: volume of shares traded
    y=data['Close'],  # y-axis: closing price
    mode='markers',  # Display points as markers
    name='Volume vs Closing Price'
    ))
    fig.update_layout(
    title=f"Volume vs Closing Price for {symbol}",
    xaxis_title="Volume",
    yaxis_title="Closing Price (USD)",
    showlegend=True
    ).to_html

    return df, plot_html , pie_chart , bar_chart 
