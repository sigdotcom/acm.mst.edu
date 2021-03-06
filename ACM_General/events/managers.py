"""
Custom Event Manager and helper functions.
"""
# Django
from django.db import models


class EventManager(models.Manager):
    """
    Used to automate the creation of events.
    """

    def get_by_natural_key(self, title):
        """
        Queries the database for an Event based on event title.

        :param title: Title of the event
        :type title: str

        :return: The event object that matches with the passed title variable
                  (if there is one) or None.
        :rtype: :class:`~events.models.Event` or None
        """
        return self.get(title=title)

    def _create_event(self, **kwargs):
        """
        Checks the date_hosted and date_expire variable to make sure they
        are valid and then saves the event to the database.

        :return: The event object that was created.
        :rtype: :class:`~events.models.Event`

        :raises ValueError: if date_hosted or date_expire is invalid.
        """
        date_hosted = kwargs.get('date_hosted', None)
        date_expire = kwargs.get('date_expire', None)

        if date_hosted is None:
            raise ValueError('EventManager received an invalid date_hosted.')

        if date_expire is None:
            raise ValueError('EventManager received an invalid date_expire.')

        if date_expire < date_hosted:
            raise ValueError('EventManager received a date_expire which falls'
                             ' before the date_hosted, please make sure the'
                             ' dates are correct.')

        model = self.model(**kwargs)
        model.save(using=self._db)
        return model

    def create_event(self, **kwargs):
        """
        Calls the '_create_event' public wrapper which a user can overwrite to
        add extra functionality to the private function.

        :return: The event object that was created.
        :rtype: :class:`~events.models.Event`
        """

        return self._create_event(**kwargs)
