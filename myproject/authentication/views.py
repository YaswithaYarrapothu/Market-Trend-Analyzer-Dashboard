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
# views.py



def market_dashboard(request):
    if request.method == 'POST':
        symbol = request.POST.get('symbol', 'AAPL')
        years = int(request.POST.get('years', 1))

        # Fetch the data and plot
        raw_data, plot = fetch_market_data(symbol, years)

        # Check if raw_data is empty
        if raw_data.empty:
            return render(request, 'dashboard.html', {
                'error_message': 'No data available for the selected stock symbol and date range.'
            })

        return render(request, 'dashboard.html', {
            'raw_data': raw_data,
            'plot': plot
        })

    return render(request, 'dashboard.html')


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')