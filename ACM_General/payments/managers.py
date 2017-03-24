from django.db import models


class TransactionCategoryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def _create_category(self, name, **kwargs):
        model = self.model(name=name, **kwargs)
        model.save()
        return model

    def create_category(self, name, **kwargs):
        return self._create_category(name, **kwargs)


class ProductManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)

    def _create_product(self, name, **kwargs):
        model = self.model(name=name, **kwargs)
        model.save()
        return model

    def create_product(self, name, **kwargs):
        return self._create_product(name, **kwargs)


class TransactionManager(models.Manager):
    def get_by_natural_key(self, stripe_token):
        return self.get(stripe_token = stripe_token)

    def _create_transaction(self, stripe_token, **kwargs):
        """
        @Desc - Base create_transaction() function that creates a transaction
                based on he values passed into it and returns the transaction
                created.
        """
        cost = kwargs.get('cost', None)
        if(stripe_token == None):
            raise ValueError('create_transaction() must be initialized with a'
                             ' stripe_token.')

        if(cost == None):
            raise ValueError('create_transaction() value must be greater than'
                             ' zero')

        transaction = self.model(stripe_token=stripe_token, **kwargs);
        transaction.save(using=self._db)

        return transaction

    def create_transaction(self, stripe_token, **kwargs):
        """
        @Desc - create_transaction() acts as a init() script for making a
                transaction of any type. This feeds _create_transactions with
                any necessary default values which should work for most
                transactions.
        """
        return self._create_transaction(stripe_token, **kwargs)
