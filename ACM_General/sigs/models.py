from django.db import models
from django.utils.translation import ugettext_lazy as _

import uuid

# Create your models here.

##
# To stop circular import errors and allow for djangos model resolution
# to do its thing
##
User = 'accounts.User'

class SIG(models.Model):
    id = models.CharField(
                    verbose_name = _('SIG ID'),
                    help_text = _('The UUID of the Special Interest Group.'),
                    max_length=15,
                    primary_key=True,
         )
    is_active = models.BooleanField(
                        verbose_name = _('Is Active'),
                        help_text = _('Whether or not the SIG is active'),
                        default = True,
                )
    date_created = models.DateTimeField(
                        verbose_name = _('Date Created'),
                        help_text = _('The date the SIG was created.'),
                        auto_now_add = True,
                        editable = False,
                   )
    founder = models.ForeignKey(
                        User,
                        verbose_name = _('SIG Founder'),
                        help_text = _('The person who founded the SIG.'),
                        on_delete=models.CASCADE,
                        related_name = "founder",
              )
    chair = models.ForeignKey(
                    User,
                    verbose_name = _('SIG Chair'),
                    help_text = _('The current Chair of the SIG.'),
                    on_delete=models.CASCADE,
                    related_name = "chair",
            )
    description = models.CharField(
                        verbose_name = _('Description'),
                        help_text = _('A description of what the special'
                                      ' interest of the group is.'),
                        max_length=1000,
                  )

    def __str__(self):
        return(self.id)

    def __unicode__(self):
        return(self.id)


class Perm_Groups(models.Model):
    class Meta:
        unique_together = (("group_id","sig_id"),)

    group_id = models.CharField(
                        verbose_name = _('Permission ID'),
                        help_text = _('The UUID for the Permission Group.'),
                        max_length = 10,
                        unique = True,
               )
    sig_id = models.ForeignKey(
                        SIG,
                        verbose_name = _('SIG ID'),
                        help_text = _('The UUID for the Special Interest'
                                      ' Group'),
                        on_delete=models.CASCADE,
             )
    name = models.CharField(
                    verbose_name = _('Permission Name'),
                    help_text = _('The name of the Permission Group.'),
                    max_length = 10,
                    unique = True,
           )
    description = models.CharField(
                            verbose_name = _('Description'),
                            help_text = _('The description of what the'
                                          ' Permission Group does.'),
                            max_length = 1000,
                  )
