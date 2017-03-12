from django.db import models


class SIGManager(models.Manager):
    """
    TODO: Docstring
    """
    use_in_migrations = True

    def get_by_natural_key(self, perm_code):
        """
        TODO: Docstring
        """
        return self.get(perm_code=perm_code)

    def _create_sig(self, **kwargs):
        """
        TODO: Docstring
        """

        if not kwargs.get('id'):
            raise ValueError("create_sig() must have the keyword argument 'id'")

        if not kwargs.get('founder'):
            raise ValueError("create_sig() must have the keyword argument 'founder'")

        if not kwargs.get('description'):
            raise ValueError("create_sig() must have the keywork argument 'description'")

        SIG = self.model(**kwargs)
        SIG.save(using=self._db)

    def create_sig(self, **kwargs):
        """
        TODO: Docstring
        """

        self._create_sig(**kwargs)

