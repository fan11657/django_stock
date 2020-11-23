from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import StockForm
from .models import Stock

#pk_2731991c680a4bf9a5d63d49ccd72b30
# Create your views here.

token = 'pk_453bfa27e3ea4609b95ebbca4ae8d672'

def home(request):
	import requests
	import json

	if request.method == 'POST' and request.POST['ticker']:
		ticker = request.POST['ticker']
		api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token=' + token)

		apidata = None
		try:
			apidata = json.loads(api_request.content)
			print('FROM HOME: Get API successfully')
		except Exception as e:
			apidata = 'NA'
			print('FROM HOME:', e)

		return render(request, 'home.html', {'apidata': apidata})
	else:
		return render(request, 'home.html', {'no_ticker': 'Please Enter a Ticker Symbol Above...'})

def about(request):
	return render(request, 'about.html', {})

def add_stock(request):
	import requests
	import json

	if request.method == 'POST' and request.POST['ticker']:
		form = StockForm(request.POST or None)
		if form.is_valid():
			form.save()
			messages.success(request, ('Stock Has Been Added'))
			return redirect('add_stock')
	else:
		tickers = Stock.objects.all()
		apidata = []
		for ticker in tickers:
			try:
				api_request = requests.get(f'https://cloud.iexapis.com/stable/stock/{ticker}/quote?token=' + token)
				data = json.loads(api_request.content)
				apidata.append(data)
				print('FROM HOME: Get API successfully')
			except Exception as e:
				apidata = 'NA'
				print('FROM HOME:', e)

		return render(request, 'add_stock.html', {'tickers': tickers, 'apidata': apidata})


def del_stock(request, ticker_id):
	ticker = Stock.objects.get(pk=ticker_id)
	ticker.delete()
	messages.success(request, ('Stock Has Been Deleted!'))
	return redirect(add_stock)