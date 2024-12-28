from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import MarketData
from .serializers import MarketDataSerializer
from .utils import fetch_market_data
from django.shortcuts import render



class MarketDataViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]  # Ensures only authenticated users can access
    queryset = MarketData.objects.all()  # Fetch all market data from the database
    serializer_class = MarketDataSerializer 

# Create your views here.
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST['uname']
        email = request.POST['email']
        pass1 = request.POST['psw']
        pass2 = request.POST['psw-repeat']
        
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = username
        # myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully")
        
        return redirect('signin')
        
        
    return render(request, "signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['uname']
        pass1 = request.POST['psw']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            # messages.success(request, "Logged In Sucessfully!!")
            return render(request, "index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('home')
    
    return render(request, "signin.html")
@login_required


def market_dashboard(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol', 'AAPL')
        years = int(request.POST.get('years', 1))

        # Fetch the data and plot
        raw_data, plot , pie_chart , bar_chart  = fetch_market_data(symbol, years)

        # Check if raw_data is empty
        if raw_data.empty:
            return render(request, 'index.html', {
                'error_message': 'No data available for the selected stock symbol and date range.'
            })

        return render(request, 'index.html', {
            'raw_data': raw_data,
            'plot': plot,
            'pie_chart':pie_chart,
            'bar_chart':bar_chart,
        })

    return render(request, 'index.html')

from .forms import StockForm
from .prediction import generate_market_trend_report
import pandas as pd

def predict(request):
    predictions = None
    symbol = None
    predict_plot = None
    if request.method == "POST":
        form = StockForm(request.POST)
        if form.is_valid():
            symbol = form.cleaned_data['symbol']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Generate the market trend report and get predictions
            predictions, future_dates ,predict_plot = generate_market_trend_report(symbol, start_date, end_date)
            predictions = list(zip(pd.to_datetime(future_dates, unit='s').strftime('%Y-%m-%d'), predictions)) 
    
    else:
        form = StockForm()

    return render(request, 'dashboard.html', {'form': form, 'predictions': predictions, 'predict_plot': predict_plot , 'symbol': symbol})

#comparing two companies stock data
import yfinance as yf
import plotly.graph_objects as go
from .forms import StockComparisonForm

def comparision(request):
    comparison_chart = None
    company1 = None
    company2 = None
    form = StockComparisonForm()

    if request.method == 'POST':
        form = StockComparisonForm(request.POST)
        if form.is_valid():
            company1 = form.cleaned_data['company1']
            company2 = form.cleaned_data['company2']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Fetch stock data for both companies
            stock1 = yf.Ticker(company1).history(start=start_date, end=end_date)
            stock2 = yf.Ticker(company2).history(start=start_date, end=end_date)

            # Ensure both have the same index for comparison
            stock1.reset_index(inplace=True)
            stock2.reset_index(inplace=True)

            # Plot the data
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=stock1['Date'],
                y=stock1['Close'],
                mode='lines',
                name=f"{company1} Closing Prices"
            ))
            fig.add_trace(go.Scatter(
                x=stock2['Date'],
                y=stock2['Close'],
                mode='lines',
                name=f"{company2} Closing Prices"
            ))

            fig.update_layout(
                title=f"Stock Comparison: {company1} vs {company2}",
                xaxis_title="Date",
                yaxis_title="Closing Price (USD)",
                legend_title="Companies"
            )

            comparison_chart = fig.to_html()

    return render(request, 'compare_stock.html', {'form': form, 'comparison_chart': comparison_chart})


def updates(request):
    return render(request,"update.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')