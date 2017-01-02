from django.db import models

import uuid

# Create your models here.

##
# To stop circular import errors and allow for djangos model resolution 
# to do its thing
##
User = 'accounts.User'

class SIG(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    is_active = models.BooleanField(default = True)
    date_created = models.DateTimeField(auto_now_add = True, editable = False)
    founder = models.ForeignKey(User, 
                                on_delete=models.CASCADE, 
                                related_name = "founder")
    chair = models.ForeignKey(User, 
                              on_delete=models.CASCADE, 
                              related_name = "chair")
    description = models.CharField(max_length=1000)

    def __str__(self):
        return(self.id)

    def __unicode__(self):
        return(self.id)


class Perm_Groups(models.Model):
    class Meta:
        unique_together = (("group_id","sig_id"),)

    group_id = models.CharField(max_length = 10, unique = True)
    sig_id = models.ForeignKey(SIG, on_delete=models.CASCADE)
    name = models.CharField(max_length = 10, unique = True)
    description = models.CharField(max_length = 1000)
