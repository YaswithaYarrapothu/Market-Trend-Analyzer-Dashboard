from django import forms

class StockForm(forms.Form):
    symbol = forms.CharField(max_length=10, label='Stock Symbol')
    start_date = forms.DateField(label='Start Date', widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='End Date', widget=forms.DateInput(attrs={'type': 'date'}))
class StockComparisonForm(forms.Form):
    company1 = forms.CharField(label="First Company Symbol", max_length=10, required=True)
    company2 = forms.CharField(label="Second Company Symbol", max_length=10, required=True)
    start_date = forms.DateField(label="Start Date", required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label="End Date", required=True, widget=forms.DateInput(attrs={'type': 'date'}))