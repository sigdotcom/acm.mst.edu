from django.db import models
from django.utils import timezone

import uuid

##
# To stop circular import errors and allow for djangos model resolution 
# to do its thing
##

User = 'accounts.User'
SIG = 'sigs.SIG'

# Create your models here.

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_created = models.DateTimeField(auto_now_add = True, editable=False)
    date_hosted = models.DateTimeField()
    date_expire = models.DateTimeField()
    creator = models.ForeignKey(
                User, 
                on_delete=models.CASCADE,
                related_name = 'User'
            )
    hosting_sig = models.ForeignKey(
                    SIG, 
                    on_delete=models.CASCADE,
                    related_name = 'SIG'
                )
    title = models.CharField(max_length = 256)
    description = models.CharField(max_length = 1000)
    location = models.CharField(max_length = 256)
    presenter = models.CharField(max_length = 256)
    ##
    # Running out of ideas
    ##
    refreshments = models.CharField(max_length = 256)

    @property
    def is_active(self):
        return (self.date_expire > timezone.now())



class Event_Participation(models.Model):
    class Meta:
        unique_together = (("event_id","user_id"),)
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE) 

