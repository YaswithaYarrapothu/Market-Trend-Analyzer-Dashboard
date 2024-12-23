from django.core.management.base import BaseCommand
from authentication.utils import fetch_market_data  # Import the utility function

class Command(BaseCommand):
    help = "Fetch market data from external APIs and store it in the database"

    def handle(self, *args, **kwargs):
        try:
            fetch_market_data()  # Call the function that fetches and stores data
            self.stdout.write(self.style.SUCCESS("Market data fetched successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error fetching market data: {e}"))
