from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import pandas_datareader.data as pdr
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline
from datapackage import Package
from Financialmarket.core import get_basic_finance, delete_all_stocks, read_gold_prices
from Financialmarket.models import CompanyInfo, StockPrice, GoldPrice
from Financialmarket.forms import DateSelectForm

package = Package('https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json')


def store_company():
    df = pd.read_csv('constituents.csv')
    print(df)


# Create your views here.
def home(request):
    #get_basic_finance()
    #delete_all_stocks()
    #read_gold_prices()
    company_list = CompanyInfo.objects.all()
    return render(request, 'company/company_list.html', {
        'company_list': company_list,
        'left_menu': 0,
        'title': 'Company List'
    })


def company_stock(request, company_id):
    try:
        company = CompanyInfo.objects.get(pk=company_id)
    except CompanyInfo.DoesNotExist:
        return redirect(reverse('page-not-found'))

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(30)
    else:
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')

    form = DateSelectForm()

    df = pd.DataFrame(list(company.stocks.filter(date__range=[start_date, end_date])
                           .values('open', 'close', 'high', 'low', 'volume', 'adj_close', 'date')
                           .order_by('-date')[::-1]))
    trace = go.Scatter(x=df['date'], y=df['adj_close'], mode='lines', name=company.name)
    data = [trace]
    layout = go.Layout(
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        ),
        yaxis=dict(
            title='Adj Close',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        )
    )
    fig = go.Figure(data, layout=layout)
    graph = plotly.offline.plot(fig, auto_open=True, output_type='div')
    return render(request, 'company/company_stock.html', {
        'left_menu': 0,
        'graph': graph,
        'stocks': df.to_html(classes="table table-striped"),
        'form': form,
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'title': '{} Finance'.format(company.symbol)
    })


def gold_price_page(request):
    df = pd.DataFrame(list(GoldPrice.objects.values('date', 'price')
                           .order_by('-date')))
    trace = go.Scatter(x=df['date'], y=df['price'], mode='lines', name='Gold Prices')
    data = [trace]
    layout = go.Layout(
        xaxis=dict(
            title='Date',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        ),
        yaxis=dict(
            title='Price',
            showgrid=True,
            gridcolor='#bdbdbd',
            zerolinecolor='#969696',
            linecolor='#636363',
        )
    )
    fig = go.Figure(data, layout=layout)
    graph = plotly.offline.plot(fig, auto_open=True, output_type='div')
    return render(request, 'gold/index.html', {
        'left_menu': 1,
        'graph': graph,
        'title': 'Gold Price'
    })


def page_not_found(request):
    return render(request, '404.html', {
        'title': 'Page not found'
    })
