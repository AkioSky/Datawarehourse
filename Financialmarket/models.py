from django.db import models


# Create your models here.
class CompanyInfo(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    sector = models.CharField(max_length=100)
    website = models.URLField(max_length=500)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('company-stock', args=[str(self.id)])


class StockPrice(models.Model):
    company = models.ForeignKey(CompanyInfo, on_delete=models.CASCADE, related_name='stocks')
    open = models.CharField(max_length=50)
    close = models.CharField(max_length=50)
    high = models.CharField(max_length=50)
    low = models.CharField(max_length=50)
    volume = models.CharField(max_length=50)
    adj_close = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.adj_close


class GoldPrice(models.Model):
    price = models.CharField(max_length=50)
    date = models.CharField(max_length=50)

    def __str__(self):
        return self.price