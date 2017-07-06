from django.db import models


class EventManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)

    def _create_event(self, **kwargs):
        """
        @Raises - django.db.integrityError
                  ValueError
        """
        date_hosted=kwargs.get('date_hosted', None)
        date_expire=kwargs.get('date_expire', None)

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
        return model;

    def create_event(self, **kwargs):
        return self._create_event(**kwargs)
