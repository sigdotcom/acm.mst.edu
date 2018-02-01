"""
Custom managers for the Sigs app's models.
"""
# Django
from django.db import models


class SIGManager(models.Manager):
    """
    Handles high abstraction database interaction for the SIG model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, id):
        """
        Gets the SIG model by it's id.

        :param id: The id of the SIG.
        :type id: int

        :return: Returns a SIG model object with the id equal to the input
                 specified id.
        :rtype: :class:`sigs.models.SIG`
        """
        return self.get(id=id)

    def _create_sig(self, **kwargs):
        """
        Private method for creating a SIG.

        :param \**kwargs: See sigs.managers.SIGManager.create_sig.

        :return: A created SIG object.
        :rtype: :class:`sigs.models.SIG`
        """

        if not kwargs.get('founder'):
            raise ValueError(
                "create_sig() must have the keyword argument 'founder'"
            )

        if not kwargs.get('description'):
            raise ValueError(
                "create_sig() must have the keywork argument 'description'"
            )

        SIG = self.model(**kwargs)
        SIG.save(using=self._db)

        return SIG

    def create_sig(self, **kwargs):
        r"""
        Creates a SIG.

        :param \**kwargs: See below
        :Keyword Arguments:
            * *founder* (django.db.models.ForeignKey) --
                The founder of the SIG
            * *description* (django.db.models.CharField) --
                A summary of the SIG and its purpose.
            * *id* (django.db.models.CharField) --
                Unique id for the SIG
            * *is_active* (django.db.models.BooleanField) --
                A value that tells whether the SIG is active or not.
            * *date_created* (django.db.models.DateTimeField) --
                What date the SIG was created.
            * *chair* (django.db.models.ForeignKey) --
                The current Chair of the SIG.

        :return: A created SIG object.
        :rtype: :class:`sigs.models.SIG`
        """
        return self._create_sig(**kwargs)
