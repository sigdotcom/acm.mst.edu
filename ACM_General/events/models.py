# standard library
import uuid

# Django
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# local Django
from . import managers

# To stop circular import errors and allow for djangos model resolution to
# work as it should.
User = 'accounts.User'
SIG = 'sigs.SIG'


def get_path_for_flier(instance, filename):
    """
    Used to obtain a path based on an instance of the Event (try to make this a
    cross reference if you can) object pasted into the function.

    :type instance: Event object
    :param instance: An instance of the current Event being created

    :type filename: str
    :param filename: The filename of the image being used as a flier for the
                     current event being created

    :rtype: str
    :returns: String that contains the generated path to save or collect the
              flier image.

    .. note::

        This is done so that fliers can be stored in path that looks like:
        'media_files/fliers/<date_hosted>/<filename>'.  (This makes it easier
        to find media uploaded about an Event).
    """
    return '{}/{}/{}'.format(
        settings.FLIERS_PATH, str(instance.date_hosted)[:10], filename
    )


class Event(models.Model):
    """
    Class used to define what is needed when creating new events.
    """
    objects = managers.EventManager()

    #: An ACM member's user id; represented as a UUIDField.
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

    #: The user who created the event; represented as a ForeignKey of the User
    #: model.
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Creator'),
        help_text=_('The user who created the event.'),
        related_name='User',
    )

    #: The SIG hosting the event; represented as a ForeignKey of the SIG model.
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

    #: A description of what the event will consist of; represented as a
    #: CharField.
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

        :rtype: bool
        :returns: Bool value representing whether or not the event is
                  considered 'active'.
        """
        return self.date_expire >= timezone.now()

    def clean(self):
        """
        The clean function is used for making checks on the data posted to the
        form.

        :raises ValidationError: if date_expire or date_hosted are invalid.

        :rtype: None
        :returns: None
        """

        # Calls the original clean function
        super(Event, self).clean()

        # Sets up a dictionary for storing individual field errors
        errors = {'date_expire': [], 'date_hosted': []}

        # This is mostly done to catch errors when testing the EventForm with
        # certain fields empty
        if not self.date_expire:
            errors['date_expire'].append(
                ValidationError(
                    _('Please fill out the expiration date field.')
                )
            )
        if not self.date_hosted:
            errors['date_hosted'].append(
                ValidationError(_('Please fill out the host date field.'))
            )

        # Checks that the datetimes given for the host and expire date are
        # valid
        if self.date_expire and self.date_expire < timezone.now():
            errors['date_expire'].append(
                ValidationError(
                    _(
                        'The expiration date shouldn\'t be'
                        ' before the current date!'
                     )
                )
            )
        if self.date_hosted and self.date_hosted < timezone.now():
            errors['date_hosted'].append(
                ValidationError(
                    _(
                        'The host date shouldn\'t be before the current date!'
                    )
                )
            )
        if (
            self.date_expire and self.date_hosted and
            self.date_expire < self.date_hosted
        ):
            errors['date_expire'].append(
                ValidationError(
                    _(
                        'The expiration date shouldn\'t be'
                        ' before the host date!'
                    )
                )
            )

        # Returns errors if any occured
        if errors['date_expire'] or errors['date_hosted']:
            raise ValidationError(errors)


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
