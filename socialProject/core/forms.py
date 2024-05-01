from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(label='Search Students', max_length=100)
