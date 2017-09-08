# Django
from django.db import models


class SIGManager(models.Manager):
    """
    This class contains functions to test all functions of SIG's
    """
    use_in_migrations = True

    def get_by_natural_key(self, id):
        """
        Gets the SIG by it's id

        :param id: The id of the SIG 
        :type id: int
        :rtype: None
        :return: None
        """
        return self.get(id=id)

    def _create_sig(self, **kwargs):
        r"""
        Creates a SIG
        
        :param \**kwargs: See below
        :Keyword Arguments:
            * *founder* (''models.ForeignKey'') --
                The founder of the SIG
            * *description* (''models.CharField'') --
                A summary of the SIG and its purpose.
            * *id* (''models.CharField'') --
                Unique id for the SIG
            * *is_active* (''models.BooleanField'') --
                A value that tells whether the SIG is active or not.
            * *date_created* (''models.DateTimeField'') --
                What date the SIG was created.
            * *chair* (''models.ForeignKey'') --
                The current Chair of the SIG.
        """

        if not kwargs.get('founder'):
            raise ValueError("create_sig() must have the keyword argument 'founder'")

        if not kwargs.get('description'):
            raise ValueError("create_sig() must have the keywork argument 'description'")

        SIG = self.model(**kwargs)
        SIG.save(using=self._db)

        return SIG

    def create_sig(self, **kwargs):
        """
        Function wrapper for _create_sig(self, **kwargs)

        Refer to _create_sig documentation.
        """

        return self._create_sig(**kwargs)
