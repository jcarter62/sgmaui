from django import forms
from decouple import config
import requests


class WellAssocForm(forms.Form):
    rec_id = forms.CharField(max_length=40, required=False, widget=forms.HiddenInput, label='Record ID', initial='0')
    well_id = forms.CharField(max_length=15, required=True)
    account = forms.CharField(max_length=15, required=True, label='Account', initial='0', widget=forms.TextInput(attrs={'size': 15}))
    amount = forms.FloatField(required=True, min_value=0, max_value=999999999, initial=0, label='Amount')
    method = forms.CharField(max_length=3, required=True, initial='PCT', widget=forms.Select(choices=[('PCT', 'Percent'), ('AMT', 'Amount')]), label='Method')
    begindate = forms.DateField(required=True, input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d'))
    enddate = forms.DateField(required=False, input_formats=['%Y-%m-%d'], widget=forms.DateInput(format='%Y-%m-%d'))
    ordering = forms.IntegerField(required=True, min_value=1, max_value=999, initial=1)
    isactive = forms.IntegerField(required=True, min_value=0, max_value=1, initial=1)

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')
        method = cleaned_data.get('method')
        if method == 'PCT' and amount > 100:
            self.add_error('amount', 'Amount cannot be greater than 100 when Method is Amount')
        if amount < 0:
            self.add_error('amount', 'Amount cannot be less than 0')
        return cleaned_data

    def is_valid(self):
        result = super().is_valid()
        if result:
            if self.cleaned_data['method'] == 'PCT' and self.cleaned_data['amount'] > 100:
                result = False
                self.add_error('amount', 'Amount cannot be greater than 100 when Method is Amount')
            if self.cleaned_data['amount'] < 0:
                result = False
                self.add_error('amount', 'Amount cannot be less than 0')

        return result

    def save(self, commit=True):
        def generate_params() -> str:
            p = ''
            p += '?rec_id=' + self.cleaned_data['rec_id']
            p += '&well_id=' + self.cleaned_data['well_id']
            p += '&account=' + self.cleaned_data['account'].__str__()
            p += '&amount=' + self.cleaned_data['amount'].__str__()
            p += '&method=' + self.cleaned_data['method'].__str__()
            p += '&begindate=' + self.cleaned_data['begindate'].__str__()
            p += '&enddate=' + self.cleaned_data['enddate'].__str__()
            p += '&ordering=' + self.cleaned_data['ordering'].__str__()
            p += '&isactive=' + self.cleaned_data['isactive'].__str__()
            p = p.replace(' ', '%20')
            return p

        # instance = super().save(commit=False)
        if commit:
            url = config('API_URL') + 'well-assoc/save-well-details' + generate_params()
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url)
            if response.status_code == 200:
                # save "success" message
                pass
            else:
                print(response.message)
        else:
            pass

        return

