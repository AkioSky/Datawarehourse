from django import forms


class DateSelectForm(forms.Form):
    start_date = forms.DateField(label='Start Date',
                                 widget=forms.DateInput(attrs={
                                     'readonly': True,
                                     'required': True
                                 }))
    end_date = forms.DateField(label='End Date',
                               widget=forms.DateInput(attrs={
                                   'readonly': True,
                                   'required': True
                               }))
