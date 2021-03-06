"""
Custom managers for handling different Payments models.
"""

# Django
from django.db import models


class TransactionCategoryManager(models.Manager):
    """
    Used to automate the creation of Transaction Categories.
    """

    def get_by_natural_key(self, name):
        """
        Queries the database for a TransactionCategory based on category name.

        :param name: The name of Transaction.
        :type name: str

        :returns: The TransactionCategory object that matches with the passed
                  name variable (if there is one) or None.
        :rtype: :class:`~payments.models.TransactionCategory` or None
        """
        return self.get(name=name)

    def _create_category(self, name, **kwargs):
        """
        Used to create a Transaction Category and save it to the database.

        :param name: The name of Transaction.
        :type name: str

        :returns: The created Transaction Category.
        :rtype: :class:`~payments.models.TransactionCategory`
        """
        model = self.model(name=name, **kwargs)
        model.save()
        return model

    def create_category(self, name, **kwargs):
        """
        Used to create a Transaction Category and save it to the database
        (calls `_create_category`).

        :param name: The name of Transaction.
        :type name: str

        :returns: The created Transaction Category.
        :rtype: :class:`~payments.models.TransactionCategory`
        """
        return self._create_category(name, **kwargs)


class ProductManager(models.Manager):
    """
    Used to automate the creation of Products.
    """

    def get_by_natural_key(self, name):
        """
        :param name: The name of Product.
        :type name: str

        :returns: The Product object that matches with the passed name variable
                  (if there is one) or None.
        :rtype: :class:`~payments.models.Product` or None
        """
        return self.get(name=name)

    def _create_product(self, tag, name, **kwargs):
        """
        Used to create a Product and save it to the database.

        :param name: The name of Product.
        :type name: str

        :returns: The created Product.
        :rtype: :class:`payments.models.Product`
        """
        model = self.model(name=name, tag=tag, **kwargs)
        model.save()
        return model

    def create_product(self, tag, name, **kwargs):
        """
        Used to create a Product and save it to the database (calls
        `_create_product`).

        :param name: The name of Product.
        :type name: str

        :returns: The created Product.
        :rtype: :class:`payments.models.Product`
        """
        return self._create_product(tag, name, **kwargs)


class TransactionManager(models.Manager):
    """
    Used to automate the creation of Transactions.
    """

    def get_by_natural_key(self, stripe_token):
        """
        Queries the database for a Transaction based on stripe token.

        :param stripe_token: The stripe token associated with the Transaction.
        :type stripe_token: str

        :returns: The Transaction object that matches with the passed
                  stripe_token variable (if there is one) or None.
        :rtype: :class:`payments.models.Transaction` or None
        """
        return self.get(stripe_token=stripe_token)

    def _create_transaction(self, stripe_token, **kwargs):
        """
        The base function that gets called by `create_transaction`.

        :param stripe_token: The stripe token associated with the transaction
                             in the Payment model.
        :type stripe_token: str

        :returns: The created transaction.
        :rtype: :class:`payments.models.Transaction`

        :raises ValueError: If the transaction cost was less than or equal to
                            zero.
        """
        cost = kwargs.get('cost', None)

        if cost is None:
            raise ValueError('create_transaction() value must be greater than'
                             ' zero')

        transaction = self.model(stripe_token=stripe_token, **kwargs)
        transaction.save(using=self._db)

        return transaction

    def create_transaction(self, stripe_token, **kwargs):
        """
        Used to create a Transaction and save it to the database.

        :param stripe_token: The stripe token associated with the Transaction.
        :type stripe_token: str

        :returns: The created transaction.
        :rtype: :class:`payments.models.Transaction`
        """
        return self._create_transaction(stripe_token, **kwargs)
