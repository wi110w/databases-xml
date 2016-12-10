from django import forms
from .models import *


class AddEditForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=20)
    reader = forms.ChoiceField(label='Reader:', choices=get_readers)
    librarian = forms.ChoiceField(label='Librarian:', choices=get_librarians)
    book = forms.ChoiceField(label='Book:', choices=get_books)
    issue_date = forms.DateField(label='Issue date:',
                                 widget=forms.SelectDateWidget(
                                     empty_label=('Year:', 'Month:', 'Day:')
                                 )
                                 )
    repay_date = forms.DateField(label='Must return on:',
                                 widget=forms.SelectDateWidget(
                                     empty_label=('Year:', 'Month:', 'Day:')
                                 )
                                 )
    real_repay_date = forms.DateField(label='Returned on:',
                                      widget=forms.SelectDateWidget(
                                          empty_label=('Year:', 'Month:', 'Day:')
                                      )
                                      )


class SearchForm(forms.Form):
    year = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '2010'}))