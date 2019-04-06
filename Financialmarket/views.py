from django.shortcuts import render
from django.http import HttpResponse
import pandas_datareader.data as pdr
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from datapackage import Package

package = Package('https://datahub.io/core/s-and-p-500-companies-financials/datapackage.json')


def store_company():
    df = pd.read_csv('constituents.csv')
    print(df)

# Create your views here.
def home(request):
    #start = datetime(2010, 12, 31)
    #end = datetime.now()
    #spy = pdr.DataReader('SPY', 'yahoo', start, end)
    #spy.to_csv('1.csv')
    #print(spy)

    #resources = package.resources
    #for resource in resources:
    #    if resource.tabular:
    #        data = pd.read_csv(resource.descriptor['path'])
            #print(data)
    #df = pd.DataFrame()
    #print(df)
    #df.to_csv('company.csv')
    store_company()
    return HttpResponse('Welcome')