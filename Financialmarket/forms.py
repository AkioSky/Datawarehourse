from django import forms


class DateSelectForm(forms.Form):
    start_date = forms.DateField(label='From',
                                 widget=forms.DateInput(attrs={
                                     'readonly': True,
                                     'required': True
                                 }))
    end_date = forms.DateField(label='To',
                               widget=forms.DateInput(attrs={
                                   'readonly': True,
                                   'required': True
                               }))


class MonthYearSelectForm(forms.Form):
    start_date = forms.DateField(label='From',
                                 widget=forms.DateInput(attrs={
                                     'readonly': True,
                                     'required': True
                                 }))
    end_date = forms.DateField(label='To',
                               widget=forms.DateInput(attrs={
                                   'readonly': True,
                                   'required': True
                               }))