from . import models
from sigs.models import SIG
from accounts.models import User
from django.test import TestCase

##
# NOTE: Because all of the models in the Transactions apps are so closely
#       linked, we need to test them all at once.
##

class PaymentsManagerCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('ksyh3@mst.edu')
        self.sig = SIG.objects.create_sig(
                        id='test',
                        chair=self.user,
                        founder=self.user,
                        description='test',
                    )

    def test_create_manager(self):
        category = models.TransactionCategory.objects.create_category('test')
        self.assertIsNotNone(category)
        product = models.Product.objects.create_product(
                                        'test',
                                        cost=3.00,
                                        category=category,
                                        sig=self.sig,
                                                                            )
        self.assertIsNotNone(product)
        transaction = models.Transaction.objects.create_transaction(
                                                        '3232',
                                                        cost=3.00,
                                                        category=category,
                                                        sig=self.sig,
                                                    )
        self.assertIsNotNone(transaction)

    def test_get_by_natural_key(self):
        category = models.TransactionCategory.objects.create_category('test')
        product = models.Product.objects.create_product(
                                        'test',
                                        cost=3.00,
                                        category=category,
                                        sig=self.sig,
                                    )
        transaction = models.Transaction.objects.create_transaction(
                                                        '3232',
                                                        cost=3.00,
                                                        category=category,
                                                        sig=self.sig,
                                                    )
        self.assertIsNotNone(models.TransactionCategory.objects.get_by_natural_key('test'))
        self.assertIsNotNone(models.Product.objects.get_by_natural_key('test'))
        self.assertIsNotNone(models.Transaction.objects.get_by_natural_key('3232'))

        with self.assertRaises(models.Transaction.DoesNotExist):
            models.Transaction.objects.get_by_natural_key('424242424242')

        with self.assertRaises(models.TransactionCategory.DoesNotExist):
            models.TransactionCategory.objects.get_by_natural_key('thisdoesntexist')

        with self.assertRaises(models.Product.DoesNotExist):
            models.Product.objects.get_by_natural_key('thisdoesntexist')

