from django.db import models
from django.contrib.auth.models import User

class MarketData(models.Model):
    market_name = models.CharField(max_length=100)
    date = models.DateField()
    open_price = models.FloatField()
    close_price = models.FloatField()
    high_price = models.FloatField()
    low_price = models.FloatField()
    volume = models.IntegerField()

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_market = models.CharField(max_length=100, blank=True)
