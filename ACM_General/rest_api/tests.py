from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from accounts.models import User
from events.models import Event
from sigs.models import SIG
from payments.models import TransactionCategory, Product, Transaction
from events.models import Event

# Create your tests here.
class ViewTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('ksyh3@mst.edu')
        self.sig = SIG.objects.create_sig(
                        id='test',
                        chair=self.user,
                        founder=self.user,
                        description='test',
                    )
        self.event = Event.objects.create_event(
                        creator=self.user,
                        hosting_sig=self.sig,
                        title='test',
                        date_hosted=timezone.now(),
                        date_expire=timezone.now(),
                    )

        self.category = TransactionCategory.objects.create_category('test')
        self.product = Product.objects.create_product(
                                        'test',
                                        cost=3.00,
                                        category=self.category,
                                        sig=self.sig,
                                    )
        self.transaction = Transaction.objects.create_transaction(
                                                        '3232',
                                                        cost=3.00,
                                                        category=self.category,
                                                        sig=self.sig,
                                                    )

    def test_view_templates(self):
        """
        TODO: Docstring
        """
        response = self.client.get(reverse('rest_api:user-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rest_api:user-detail', kwargs={'pk':self.user.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:event-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rest_api:event-detail', kwargs={'pk':self.event.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:sigs-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rest_api:sigs-detail', kwargs={'pk':self.sig.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:transaction-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rest_api:transaction-detail', kwargs={'pk':self.transaction.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:category-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rest_api:category-detail', kwargs={'pk':self.category.id}))
        self.assertEqual(response.status_code, 200)

    def test_post_views(self):
        response = self.client.get(reverse('rest_api:user-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:event-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:sigs-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:transaction-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:category-list'))
        self.assertEqual(response.status_code, 200)

