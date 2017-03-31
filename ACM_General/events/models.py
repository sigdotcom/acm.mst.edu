from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from . import managers
import uuid

##
# To stop circular import errors and allow for djangos model resolution
# to do its thing
##

User = 'accounts.User'
SIG = 'sigs.SIG'

# Create your models here.


class Event(models.Model):
    objects=managers.EventManager()
    id = models.UUIDField(
            verbose_name=_('ACM User ID'),
            primary_key=True,
            default=uuid.uuid1,
            editable=False
        )
    date_created = models.DateTimeField(
            verbose_name=_('Date Created'),
            help_text=_('When the event was created.'),
            auto_now_add=True,
            editable=False,
        )
    date_hosted = models.DateTimeField(
            verbose_name=_('Date Hosted'),
            help_text=_('When the event will be held.'),
        )
    date_expire = models.DateTimeField(
            verbose_name=_('Expire Date'),
            help_text=_('When the event is over.'),
        )
    creator = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            verbose_name=_('Creator'),
            help_text=_('The user who created the event.'),
            related_name='User',
        )
    hosting_sig = models.ForeignKey(
            SIG,
            verbose_name=_('Hosting SIG'),
            help_text=_('The SIG hosting the event.'),
            on_delete=models.CASCADE,
            related_name='SIG'
        )
    title = models.CharField(
            verbose_name=_('Event Title'),
            help_text=_('A human-readable title of the event.'),
            max_length=256,
        )
    description = models.CharField(
            verbose_name=_('Event Description'),
            help_text=_('A description of what the event will consist of.'),
            max_length=1000,
        )
    location = models.CharField(
            verbose_name=_('Event Location'),
            help_text=_('Where the event is being hosted.'),
            max_length=256,
        )
    presenter = models.CharField(
            verbose_name=_('Event Presenter'),
            help_text=_('Who is presenting at the event.'),
            max_length=256,
            blank=True,
        )
    cost = models.DecimalField(
            verbose_name=_('Event Cost'),
            help_text=_('How much the event costs to participate.'),
            max_digits=6,
            decimal_places=2,
            blank=True,
            default=0,
        )

    @property
    def is_active(self):
        return self.date_expire >= timezone.now()


class EventParticipation(models.Model):
    class Meta:
        unique_together = (("event_id", "user_id"),)

    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
