from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from . import managers
import uuid

# To stop circular import errors and allow for djangos model resolution to
# work as it should.
User = 'accounts.User'
SIG = 'sigs.SIG'

def get_path_for_flier(instance, filename):
    """
    Used to obtain a path that uses an instance of the Event object to get the "date_hosted" variable.

    :type instance: Event object
    :param instance: An instance of the current Event being created

    :type filename: string
    :param filename: The filename of the image being used as a flier for the current event being created

    :rtype: string
    :return: String that contains a path to where to save the current event flier.

    .. note::

        This is done so that fliers can be stored in path that looks like: 'fliers/<date_hosted>/'. (This
        makes it easier to find media uploaded about an Event).
    """
    return '{}/{}'.format(str(instance.date_hosted)[:10], filename)

class Event(models.Model):
    """
    Class used to define what is needed when creating new events.
    """
    objects = managers.EventManager()

    #: An ACM member's user id; represented as a UUID field.
    id = models.UUIDField(
            verbose_name=_('ACM User ID'),
            primary_key=True,
            default=uuid.uuid1,
            editable=False
        )

    #: When the event was created; represented as a DateTimeField.
    date_created = models.DateTimeField(
            verbose_name=_('Date Created'),
            help_text=_('When the event was created.'),
            auto_now_add=True,
            editable=False,
        )

    #: When the event will be held; represented as a DateTimeField.
    date_hosted = models.DateTimeField(
            verbose_name=_('Date Hosted'),
            help_text=_('When the event will be held.'),
        )

    #: When the event is over; represented as a DateTimeField.
    date_expire = models.DateTimeField(
            verbose_name=_('Expire Date'),
            help_text=_('When the event is over.'),
        )

    #: The user who created the event; represented as a ForeignKey of the User model.
    creator = models.ForeignKey(
            User,
            on_delete=models.CASCADE,
            verbose_name=_('Creator'),
            help_text=_('The user who created the event.'),
            related_name='User',
        )

    #: The SIG hosting the event; represented as a ForeignKey og the SIG model.
    hosting_sig = models.ForeignKey(
            SIG,
            verbose_name=_('Hosting SIG'),
            help_text=_('The SIG hosting the event.'),
            on_delete=models.CASCADE,
            related_name='SIG'
        )

    #: The title of the event; represented as a CharField.
    title = models.CharField(
            verbose_name=_('Event Title'),
            help_text=_('A human-readable title of the event.'),
            max_length=256,
        )

    #: A description of what the event will consist of; as represented as a CharField.
    description = models.CharField(
            verbose_name=_('Event Description'),
            help_text=_('A description of what the event will consist of.'),
            max_length=1000,
        )

    #: Where the event is being hosted; represented as a CharField.
    location = models.CharField(
            verbose_name=_('Event Location'),
            help_text=_('Where the event is being hosted.'),
            max_length=256,
        )

    #: Who is presenting at the event; represented as a CharField.
    presenter = models.CharField(
            verbose_name=_('Event Presenter'),
            help_text=_('Who is presenting at the event.'),
            max_length=256,
            blank=True,
        )

    #: How much the event costs to participate; represented as a DecimalField.
    cost = models.DecimalField(
            verbose_name=_('Event Cost'),
            help_text=_('How much the event costs to participate.'),
            max_digits=6,
            decimal_places=2,
            blank=True,
            default=0,
        )

    #: The image for the flier; represented as a ImageField.
    flier = models.ImageField(
            verbose_name=_('Flier Image'),
            help_text=_('The image for the flier.'),
            upload_to=get_path_for_flier,
        )

    #: An optional link for the event; represented as a URLField.
    link = models.URLField(
            verbose_name=_('Event Link'),
            help_text=_('An optional link for the event.'),
            blank=True,
        )

    @property
    def is_active(self):
        """
        Function used for checking whether or not an event has already expired
        (gone past the current date).
        """
        return self.date_expire >= timezone.now()


class EventParticipation(models.Model):
    """
    Class used for keeping track of users' participation in different events.
    """
    class Meta:
        unique_together = (("event_id", "user_id"),)

    #: A foreign key to the id field of the Event model.
    event_id = models.ForeignKey(
                Event,
                on_delete=models.CASCADE
        )

    #: A foreign key to the id field of the User model.
    user_id = models.ForeignKey(
                User,
                on_delete=models.CASCADE
        )
