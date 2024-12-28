from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MarketDataViewSet

router = DefaultRouter()
router.register(r'market-data', MarketDataViewSet, basename='market-data')

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('signin', views.signin, name='signin'),
    path('signout', views.signout, name='signout'),
    path('index', views.market_dashboard, name='index'),
    path('dashboard',views.predict,name='dashboard'),
    path('update',views.updates,name='update'),
    path('compare_stock',views.comparision,name='compare_stock')
] + router.urls
