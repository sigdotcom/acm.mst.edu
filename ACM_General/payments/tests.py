from . import models
from accounts.models import User
from django.conf import settings
from django.urls import reverse
from django.test import TestCase, LiveServerTestCase
from sigs.models import SIG
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import stripe
import time
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
                                                        description="test",
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

    def test_ensure_api_keys(self):
        self.assertIsNotNone(getattr(settings, 'STRIPE_PUB_KEY', None))
        self.assertIsNotNone(getattr(settings, 'STRIPE_PRIV_KEY', None))

    def test_view_integrity(self):
        response=self.client.get(reverse('payments:acm-memberships'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payments/acm_membership.html')

        response=self.client.get(reverse('payments:product-handler',
                                         kwargs={'pk':self.product.id}))
        self.assertEqual(response.status_code, 405)

        response=self.client.post(reverse('payments:product-handler',
                                         kwargs={'pk':self.product.id}),
                                  {'stripeToken': 'test'}
                                )
        self.assertEqual(response.status_code, 404)

        self.client.force_login(self.user)
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

# Dropping selenium for now, will revisit
'''
class PaymentsIntegrationTestCase(LiveServerTestCase):
    def setUp(self):
        super().setUp()
        binary=FirefoxBinary("/usr/bin/firefox-esr")
        self.driver=webdriver.Firefox(firefox_binary=binary)
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
                                        description='test',
                                        category=self.category,
                                        sig=self.sig,
                                    )
        self.client.login(email='ksyh3@mst.edu') #Native django test client
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)  #selenium will set cookie domain based on current page domain
        self.driver.add_cookie({'name': 'sessionid', 'value': cookie.value, 'secure': False, 'path': '/'})
        self.driver.refresh() #need to update page for logged in use
        self.maxDiff=None

    def tearDown(self):
        super().setUp()
        self.driver.quit()

    def test_acm_membership_payment(self):
        """
        TODO: Implement ACM Membership Integration Test
        """
        selenium=self.driver
        selenium.get("{}{}".format(
                                self.live_server_url,
                                reverse('payments:acm-memberships')
                            )
                        )
        stripe_button = selenium.find_element_by_css_selector('button.stripe-button-el')
        stripe_button.click()
        time.sleep(2)

        # Test that Stripe has taken over the screen
        ## We switch context to the stripe iframe with name stripe_checkout_app
        selenium.switch_to.frame('stripe_checkout_app')

        # Proceed through the Stripe workflow and redirect to a confirmation page
        email_input= selenium.find_element_by_xpath("//input[@placeholder='Email']")
        email_input.send_keys('test@mst.edu')

        card_input=selenium.find_element_by_xpath("//input[@placeholder='Card number']")
        card_input.send_keys('4242424242424242')

        expire_input=selenium.find_element_by_xpath("//input[@placeholder='MM / YY']")
        expire_input.send_keys('0250')

        expire_input=selenium.find_element_by_xpath("//input[@placeholder='CVC']")
        expire_input.send_keys('4444')

        pay_button=selenium.find_element_by_xpath("//button")
        pay_button.click()
        time.sleep(4)
        self.assertEqual(selenium.page_source, "test")

        selenium.switch_to_default_content()
        time.sleep(2)

        ##
        # If this test fails, make sure that the STRIPE_PUB_KEY and
        # STRIPE_PRIV_KEY environment variables are set in Travis CI settings
        # for the ACM account.
        ##
        self.assertIsNotNone(models.Transaction.objects.get(description="test"))
'''
