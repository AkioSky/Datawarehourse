"""Datawarehouse URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from Financialmarket import views
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.home, name='company-list'),
                  path('gold-price/', views.gold_price_page, name='gold-price'),
                  path('stock/<int:company_id>/', views.company_stock, name='company-stock'),
                  path('404/', views.page_not_found, name='page-not-found')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)