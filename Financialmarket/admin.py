from django.contrib import admin
from .models import CompanyInfo, StockPrice, GoldPrice


# Register your models here.
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol', 'sector', 'website', 'country')
    search_fields = ('name', 'symbol', 'sector',)


class StockPriceAdmin(admin.ModelAdmin):
    list_display = ('company', 'open', 'close', 'high', 'low', 'volume', 'adj_close', 'date',)
    search_fields = ('company__name', 'company__symbol', 'company__sector', )


class GoldPriceAdmin(admin.ModelAdmin):
    list_display = ('price', 'date',)


admin.site.register(CompanyInfo, CompanyInfoAdmin)
admin.site.register(StockPrice, StockPriceAdmin)
admin.site.register(GoldPrice, GoldPriceAdmin)
