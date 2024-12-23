from django.contrib import admin
from .models import MarketData

class MarketDataAdmin(admin.ModelAdmin):
    list_display = ('market_name', 'date', 'open_price', 'close_price')
    search_fields = ('market_name',)

admin.site.register(MarketData, MarketDataAdmin)
