from django import forms
import pycountry


class SearchForm(forms.Form):
    month = forms.ChoiceField(choices=[
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December')
    ])
    country = forms.ChoiceField(choices=[(country.name, country.name) for country in pycountry.countries])
