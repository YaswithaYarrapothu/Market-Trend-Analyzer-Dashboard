from django.test import TestCase
from .models import MarketData

class MarketDataTest(TestCase):
    def test_market_data_creation(self):
        market = MarketData.objects.create(
            market_name="Test Market",
            date="2024-01-01",
            open_price=100.0,
            close_price=150.0,
            high_price=160.0,
            low_price=90.0,
            volume=1000
        )
        self.assertEqual(market.market_name, "Test Market")
