from django.forms import ModelForm
from .models import Event
from django.forms.widgets import DateTimeInput


class EventForm(ModelForm):
    class Meta:
        model = Event
        exclude = ('id', 'creator', 'date_created')
        widgets = {
            'date_hosted': DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'id': 'calendar'}),
            'date_expire': DateTimeInput(format='%Y-%m-%d %H:%M', attrs={'id': 'calendar'}),
        }