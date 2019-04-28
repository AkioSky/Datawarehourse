from django import forms
from .models import CompanyInfo


class DateSelectForm(forms.Form):
    start_date = forms.DateField(label='From',
                                 widget=forms.DateInput(attrs={
                                     'readonly': True,
                                     'required': True,
                                     'class': 'form-control'
                                 }))
    end_date = forms.DateField(label='To',
                               widget=forms.DateInput(attrs={
                                   'readonly': True,
                                   'required': True,
                                   'class': 'form-control'
                               }))
    sma_days = forms.IntegerField(label='SMA',
                                  widget=forms.NumberInput(attrs={
                                      'class': 'form-control'
                                  }))


class MonthYearSelectForm(forms.Form):
    start_date = forms.DateField(label='From',
                                 widget=forms.DateInput(attrs={
                                     'readonly': True,
                                     'required': True,
                                     'class': 'form-control'
                                 }))
    end_date = forms.DateField(label='To',
                               widget=forms.DateInput(attrs={
                                   'readonly': True,
                                   'required': True,
                                   'class': 'form-control'
                               }))
    sma_days = forms.IntegerField(label='SMA',
                                  widget=forms.NumberInput(attrs={
                                      'class': 'form-control'
                                  }))


class CompareCompanyForm(forms.Form):
    first_company = forms.ModelChoiceField(queryset=CompanyInfo.objects.all())
    second_company = forms.ModelChoiceField(queryset=CompanyInfo.objects.all())
