from django.forms import ModelForm
from . import models


class MembeshipForm(ModelForm):
    class Meta:
        model = models.Transaction
