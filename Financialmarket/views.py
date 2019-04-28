from django.shortcuts import render, redirect
from django.urls import reverse
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.offline
from datapackage import Package
from Financialmarket.core import get_basic_finance, delete_all_stocks, read_gold_prices, \
    delete_all_gold_stocks, get_last_stocks
from Financialmarket.models import CompanyInfo, GoldPrice
from Financialmarket.forms import DateSelectForm, MonthYearSelectForm, CompareCompanyForm
from django.db.models import Q
from pandas_finance import Equity


package = Package('https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json')


def store_company():
    df = pd.read_csv('constituents.csv')
    aapl = Equity('AAPL')
    print(aapl.profile)
    for index, row in df.head(50).iterrows():
        company_check = CompanyInfo.objects.filter(symbol=row['Symbol']).count()
        if company_check == 0:
            company = Equity(row['Symbol'])
            try:
                print(company.profile)
                newCompany = CompanyInfo(
                    name=row['Name'],
                    symbol=row['Symbol'],
                    sector=company.profile['Sector'],
                    website=company.profile['Website'],
                    country=company.profile['Country']
                )
                newCompany.save()
            except:
                pass


# Create your views here.
def home(request):
    #get_basic_finance()
    #delete_all_stocks()
    #read_gold_prices()
    #delete_all_gold_stocks()
    #get_last_stocks()
    #store_company()
    company_list = CompanyInfo.objects.all()
    query = request.GET.get('search')
    if query:
        company_list = CompanyInfo.objects.filter(Q(name__contains=query) | Q(symbol__contains=query) |
                                                  Q(sector__contains=query))
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
    sma_days = request.GET.get('sma_days')

    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(30)
    else:
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')

    if not sma_days:
        sma_days = 5

    form = DateSelectForm()
    start_date_min = start_date - timedelta(4)

    df = pd.DataFrame(list(company.stocks.filter(date__range=[start_date_min, end_date])
                           .values('open', 'close', 'high', 'low', 'volume', 'adj_close', 'date')
                           .order_by('-date')[::-1]))
    df['SMA({})'.format(sma_days)] = df['adj_close'].rolling(int(sma_days)).mean()
    df_result = df[df['SMA({})'.format(sma_days)].notnull()]

    trace1 = go.Scatter(x=df_result['date'], y=df_result['adj_close'], mode='lines', name=company.name)
    trace2 = go.Scatter(x=df_result['date'], y=df_result['SMA({})'.format(sma_days)], mode='lines', name='SMA({})'.format(sma_days))
    data = [trace1, trace2]
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
        'stocks': df_result.to_html(classes="table table-striped"),
        'form': form,
        'start_date': start_date.date(),
        'end_date': end_date.date(),
        'sma_days': int(sma_days),
        'title': '{} Finance'.format(company.symbol)
    })


def gold_price_page(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    sma_days = request.GET.get('sma_days')

    if not start_date:
        end_date = datetime.now()
        start_date = end_date - timedelta(1060)
        start_date = datetime(year=start_date.year, month=start_date.month, day=1)
    else:
        start_date = datetime.strptime(start_date, '%m/%d/%Y')
        end_date = datetime.strptime(end_date, '%m/%d/%Y')

    if not sma_days:
        sma_days = 5

    start_date_min = start_date - timedelta(130)

    form = MonthYearSelectForm()

    df = pd.DataFrame(list(GoldPrice.objects.
                           filter(date__range=[start_date_min, end_date])
                           .values('date', 'price')
                           .order_by('-date')[::-1]))
    df['SMA({})'.format(sma_days)] = df['price'].rolling(int(sma_days)).mean()
    df_result = df[df['SMA({})'.format(sma_days)].notnull()]
    print(df.head())
    trace1 = go.Scatter(x=df_result['date'], y=df_result['price'], mode='lines', name='Gold Prices')
    trace2 = go.Scatter(x=df_result['date'], y=df_result['SMA({})'.format(sma_days)], mode='lines', name='SMA({})'.format(sma_days))
    data = [trace1, trace2]
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
        'title': 'Gold Price',
        'form': form,
        'start_date': '{}'.format(start_date.date()),
        'end_date': '{}'.format(end_date.date()),
        'sma_days': sma_days
    })


def compare_stock(request):
    if request.method == "POST":
        form = CompareCompanyForm(request.POST)
        if form.is_valid():
            first_company = form.cleaned_data.get('first_company')
            second_company = form.cleaned_data.get('second_company')
            print(first_company.symbol)
            print(second_company.symbol)

            df_first = pd.DataFrame(list(first_company.stocks
                                         .values('open', 'close', 'high', 'low', 'volume', 'adj_close', 'date')
                                         .order_by('-date')[::-1]))
            df_second = pd.DataFrame(list(second_company.stocks
                                          .values('open', 'close', 'high', 'low', 'volume', 'adj_close', 'date')
                                          .order_by('-date')[::-1]))
            print(df_first)
            trace1 = go.Scatter(x=df_first['date'], y=df_first['adj_close'], mode='lines', name=first_company.name)
            trace2 = go.Scatter(x=df_second['date'], y=df_second['adj_close'], mode='lines', name=second_company.name)
            data = [trace1, trace2]
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
    else:
        form = CompareCompanyForm()
        graph = None

    return render(request, 'compare/index.html', {
        'left_menu': 2,
        'form': form,
        'graph': graph,
        'title': 'Compare Companies',
    })


def jupyter_view(request):
    return render(request, 'jupyter/index.html', {
        'left_menu': 3,
        'title': 'Jupyter Inline',
    })


def page_not_found(request):
    return render(request, '404.html', {
        'title': 'Page not found',
    })
