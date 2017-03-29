from . import models
from accounts.models import User
from django.conf import settings
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from sigs.models import SIG
import stripe
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
        with self.assertRaises(ValueError):
            models.Transaction.objects.create_transaction(
                                                '3232',
                                                category=category,
                                                sig=self.sig,
                                            )

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


class PaymentsModelCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('ksyh3@mst.edu')
        self.sig = SIG.objects.create_sig(
                        id='test',
                        chair=self.user,
                        founder=self.user,
                        description='test',
                    )


    def test_model_member_functions(self):
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

        self.assertEqual(str(category), 'test')
        self.assertEqual(str(product), 'test')
        self.assertEqual(str(transaction), '3232')
        # stripe_token can only be 'negatively' tested without integration
        # tests.
        with self.settings(STRIPE_PRIV_KEY=""):
            with self.assertRaises(stripe.error.AuthenticationError):
                transaction.stripe_data

class PaymentsViewCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('ksyh3@mst.edu')
        self.sig = SIG.objects.create_sig(
                        id='test',
                        chair=self.user,
                        founder=self.user,
                        description='test',
                    )
        self.category = models.TransactionCategory.objects.create_category('test')
        self.product = models.Product.objects.create_product(
                                        'test',
                                        cost=3.00,
                                        category=self.category,
                                        sig=self.sig,
                                    )
        self.transaction = models.Transaction.objects.create_transaction(
                                                        '3232',
                                                        cost=3.00,
                                                        category=self.category,
                                                        sig=self.sig,
                                                    )


    def test_view_integrity(self):
        response=self.client.get(reverse('payments:acm-memberships'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/acm_membership.html')

        response=self.client.get(reverse('payments:product-handler',
                                         kwargs={'pk':self.product.id}))
        self.assertEqual(response.status_code, 405)


        with self.assertRaises(ValueError):
            response=self.client.post(reverse('payments:product-handler',
                                              kwargs={'pk':self.product.id}))

        with self.settings(STRIPE_PRIV_KEY=""):
            with self.assertRaises(ValueError):
                response=self.client.post(reverse(
                                                'payments:product-handler',
                                                kwargs={'pk':self.product.id}
                                            ),
                                          {'stripeToken':'test'}
                                    )

        stripe_key = getattr(settings, 'STRIPE_PRIV_KEY', None)

class PaymentsIntegrationTestCase(LiveServerTestCase):
    def setUp(self):
        super().setUp()

    def test_acm_membership_payment(self):
        """
        TODO: Implement ACM Membership Integration Test
        """
        pass
