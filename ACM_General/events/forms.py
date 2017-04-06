#from django.forms import ModelForm
from .models import Event
from django.forms.widgets import DateTimeInput, Textarea
from django import forms


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ('id', 'creator', 'date_created')

        # Used to add html tags to the given elements that aren't done by default
        widgets = {
            'date_hosted': DateTimeInput(attrs={'id': 'calendar'}),
            'date_expire': DateTimeInput(attrs={'id': 'calendar'}),
            'title': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 3}),
        }
