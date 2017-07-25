from .models import Event
from django.forms.widgets import DateTimeInput, Textarea, TextInput
from django import forms


class EventForm(forms.ModelForm):
    """
    This class is used for combining the Event Class model with a form (ModelForm).
    """
    class Meta:
        model = Event
        exclude = ('id', 'creator', 'date_created')
        widgets = {
            'date_hosted': DateTimeInput(attrs={'id': 'calendar'}),
            'date_expire': DateTimeInput(attrs={'id': 'calendar'}),
            'title': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 3}),
            'link': TextInput(),
        }
