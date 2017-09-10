# Django
from django.db import models
from django.utils.translation import ugettext_lazy as _

# local Django
from . import managers


##
# To stop circular import errors and allow for djangos model resolution
# to do its thing
##
User = 'accounts.User'


class SIG(models.Model):
    """
    Model that stores all information for a SIG.
    """
    objects = managers.SIGManager()

    #: A SIG's id; represented as a CharField.
    id = models.CharField(
        verbose_name=_('SIG ID'),
        help_text=_('The UUID of the Special Interest Group.'),
        max_length=25,
        default='test',
        primary_key=True,
    )
    #: Is the SIG currently active; represented as a BooleanField.
    is_active = models.BooleanField(
        verbose_name=_('Is Active'),
        help_text=_('Whether or not the SIG is active'),
        default=True,
    )
    #: When the SIG was created; represented as a DateTimeField.
    date_created = models.DateTimeField(
        verbose_name=_('Date Created'),
        help_text=_('The date the SIG was created.'),
        auto_now_add=True,
        editable=False,
    )
    #: The user that founded the SIG; represented as a ForeignKey.
    founder = models.ForeignKey(
        User,
        verbose_name=_('SIG Founder'),
        help_text=_('The person who founded the SIG.'),
        on_delete=models.CASCADE,
        related_name="founder",
    )
    #: The user that is currently chair of the SIG; represented as a ForeignKey.
    chair = models.ForeignKey(
        User,
        verbose_name=_('SIG Chair'),
        help_text=_('The current Chair of the SIG.'),
        on_delete=models.CASCADE,
        related_name="chair",
    )
    #: A description of what the SIG is; represented as a CharField.
    description = models.CharField(
        verbose_name=_('Description'),
        help_text=_('A description of what the special'
                    ' interest of the group is.'),
        max_length=1000,
    )

    def __str__(self):
        """
        Returns the id of the SIG.

        :rtype: django.db.models.CharField
        :return: The ID of the SIG.
        """
        return self.id


"""
class PermGroups(models.Model):
    class Meta:
        unique_together = (("group_id", "sig_id"),)

    group_id = models.CharField(
        verbose_name=_('Permission ID'),
        help_text=_('The UUID for the Permission Group.'),
        max_length=10,
        unique=True,
    )
    sig_id = models.ForeignKey(
        SIG,
        verbose_name=_('SIG ID'),
        help_text=_('The UUID for the Special Interest'
                    ' Group'),
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        verbose_name=_('Permission Name'),
        help_text=_('The name of the Permission Group.'),
        max_length=10,
        unique=True,
    )
    description = models.CharField(
        verbose_name=_('Description'),
        help_text=_('The description of what the'
                    ' Permission Group does.'),
        max_length=1000,
    )
"""
