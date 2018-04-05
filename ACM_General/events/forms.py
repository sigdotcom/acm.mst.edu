"""
Contains all of the forms utilized for the Events app.
"""

# Django
from django.forms import ModelForm
from django.forms.widgets import DateTimeInput, Textarea, TextInput, CheckboxSelectMultiple

# local Django
from .models import Event, Tag


class EventForm(ModelForm):
    """
    This class is used for combining the Event Class model with a form
    (ModelForm).
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
            'tags': CheckboxSelectMultiple(),
        }
    def __init__(self, **kwargs):
        super(EventForm, self).__init__(**kwargs)
        self.fields['tags'].queryset = Tag.objects.filter(is_disabled=False)
