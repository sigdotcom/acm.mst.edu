from django.db import models


class EventManager(models.Manager):
    def get_by_natural_key(self, title):
        return self.get(title=title)

    def _create_event(self, **kwargs):
        model = self.model(**kwargs)
        model.save(using=self._db)
        return model;

    def create_event(self, **kwargs):
        return self._create_event(**kwargs)

