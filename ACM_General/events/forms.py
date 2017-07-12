"""
.. _modelform-link: https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/
.. _class-meta-fields: https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#selecting-the-fields-to-use
"""

from .models import Event
from django.forms.widgets import DateTimeInput, Textarea, TextInput
from django import forms


class EventForm(forms.ModelForm):
    """
    This class is used for combining the Event Class model with a form
    (ModelForm). This ModelForm adds extra information about what to
    display on the form that is created. More information about ModelForm
    can be found `here <modelform-link_>`_.
    """
    class Meta:
        """
        Inside the class Meta, you can use different variables to change the
        way model fields will be displayed such as using the widget variable.
        For example, the title field of the model is changed with the widget
        variable to include having a Textarea (which is an HTML element used
        to define having a larger input area for text). To learn more about
        the changing the fields in the Class Meta, click
        `here <class-meta-fields_>`_.
        """

        model = Event

        #: Used to exclude certain fields from appearing on the event creation
        #: page.
        exclude = ('id', 'creator', 'date_created')

        #: Used to add html tags to the given elements that aren't done by default
        widgets = {
            'date_hosted': DateTimeInput(attrs={'id': 'calendar'}),
            'date_expire': DateTimeInput(attrs={'id': 'calendar'}),
            'title': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 3}),
            'link': TextInput(),
        }
