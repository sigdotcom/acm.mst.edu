"""
Contains all of the unit tests for the rest_api app.
"""
# standard library
import json

# third-party
from rest_framework.test import APIClient

# Django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# local Django
from accounts.models import User
from events.models import Event
# from events.serializers import EventSerializer
from payments.models import TransactionCategory, Product, Transaction
from sigs.models import SIG


class AccountsTestCase(TestCase):
    """
    Ensures that a user account behaves as expected throughout various
    interactions they may have throughout the website.  This includes all basic
    functionality pertaining to data associated with the user, as well as the
    user itself.
    """

    def setUp(self):
        """
        Initializes all variables and data that is required to
        test Account functionality.
        """
        super().setUp()
        self.client = APIClient()
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
        self.user_data = {
            "email": "test@mst.edu",
            "first_name": "test",
            "last_name": "test",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False
        }

    def test_accounts_rest_actions(self):
        """
        Ensures that an Accounts interactions with each REST API (post, get,
        put, destroy) results in expected behavior.
        """
        user = self.user_data

        ##
        # Testing standard views with initial created model
        ##
        response = self.client.get(reverse('rest_api:user-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('rest_api:user-detail', kwargs={'pk': self.user.id})
        )
        self.assertEqual(response.status_code, 200)

        ##
        # Testing creating a new user
        ##
        response = self.client.post(reverse('rest_api:user-list'), user)
        self.assertEqual(response.status_code, 201)
        for k, v in user.items():
            self.assertEqual(response.json()[k], v)

        ##
        # Testing "PUT" or modifing a user
        # NOTE: This test requires the data to be sent in a special way due to
        #       how the django client does put requests.
        ##
        user['email'] = "test1@mst.edu"
        response = self.client.put(
            reverse(
                'rest_api:user-detail',
                kwargs={'pk': response.json()['id']}
            ),
            data=json.dumps(user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["email"], "test1@mst.edu")

        ##
        # Testing delete capability
        ##
        user_id = response.json()['id']
        response = self.client.get(reverse('rest_api:user-list'))
        self.assertIsNotNone(response.json()[1])

        response = self.client.delete(
            reverse(
                'rest_api:user-detail',
                kwargs={'pk': user_id}
            )
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.get(
            reverse(
                'rest_api:user-detail',
                kwargs={'pk': user_id}
            )
        )
        self.assertEqual(response.status_code, 404)

        ##
        # Ensure it doesnt exist on the master list
        ##
        response = self.client.get(reverse('rest_api:user-list'))
        with self.assertRaises(IndexError):
            self.assertEqual(response.json()[1], None)
        self.assertIsNotNone(response.json()[0])

    def test_serializer_validation(self):
        """
        Ensures that the :class:`~accounts.serializers.UserSerializer`
        functions as intended.
        """
        user = self.user_data
        user['email'] = "test@fail.com"
        response = self.client.post(reverse('rest_api:user-list'), user)
        self.assertEqual(response.status_code, 400)


class EventsTestCase(TestCase):
    """
    Ensures Events behave as expected throughout their lifecycle.
    """

    def setUp(self):
        """
        Initializes all variables and data required to test Event
        functionality.
        """
        super().setUp()
        self.client = APIClient()
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

        # Sets up image variable for creating Event
        image_path = './test_data/test_image.jpg'
        self.image = SimpleUploadedFile(name='test_image.jpg', content=open(
            image_path, 'rb').read(), content_type='multipart/form-data')

    def test_events_rest_actions(self):
        """
        Ensures that an event behaves as expected at each point in the REST
        api.
        """
        event = {
            "date_hosted": timezone.now(),
            "date_expire": timezone.now(),
            "title": "test1",
            "description": "test",
            "location": "test",
            "presenter": "test",
            "cost": 3.00,
            "flier": self.image,
            "creator": self.user.id,
            "hosting_sig": self.sig.id,
        }

        ##
        # Testing standard views with initial created model
        ##
        response = self.client.get(reverse('rest_api:event-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('rest_api:event-detail', kwargs={'pk': self.event.id}))
        self.assertEqual(response.status_code, 200)

        ##
        # Testing creating a new event
        ##
        response = self.client.post(reverse('rest_api:event-list'), event)
        self.assertEqual(response.status_code, 201)
        for k in ('title', 'description', 'location'):
            self.assertEqual(response.json()[k], event[k])

        ##
        # Testing "PUT" or modifying a event
        # NOTE: This test requires the data to be sent in a special way due to
        #       how the django client does put requests.
        ##

        # Resets the image pointer to be pointing at the beginning of the image
        # file rather than the end which would cause an error with the 'put'
        # command.
        self.image.seek(0)

        event['title'] = "test1"
        response = self.client.put(
            reverse('rest_api:event-detail',
                    kwargs={'pk': response.json()['id']}),
            event,
            format="multipart"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "test1")

        ##
        # Testing delete capability of an Event
        ##
        event_id = response.json()['id']
        response = self.client.get(reverse('rest_api:event-list'))
        self.assertIsNotNone(response.json()[1])

        response = self.client.delete(
            reverse(
                'rest_api:event-detail',
                kwargs={'pk': event_id}
            )
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.get(
            reverse(
                'rest_api:event-detail',
                kwargs={'pk': event_id}
            )
        )
        self.assertEqual(response.status_code, 404)

        ##
        # Ensure it doesnt exist on the master list
        ##
        response = self.client.get(reverse('rest_api:event-list'))
        with self.assertRaises(IndexError):
            self.assertEqual(response.json()[1], None)
        self.assertIsNotNone(response.json()[0])


class SigsTestCase(TestCase):
    """
    Ensures that a SIG behaves as expected throughout it's lifecycle.
    """

    def setUp(self):
        """
        Initializes all variables and data required to test SIG functionality.
        """
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

    def test_sigs_rest_actions(self):
        """
        Ensures that a SIG behaves as expected at each
        point in the REST API.
        """
        sig = {
            "id": "sig_test",
            "is_active": True,
            "description": "test",
            "founder": self.user.id,
            "chair": self.user.id
        }

        ##
        # Testing standard views with initial created model
        ##
        response = self.client.get(reverse('rest_api:sigs-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse('rest_api:sigs-detail', kwargs={'pk': self.sig.id})
        )
        self.assertEqual(response.status_code, 200)

        ##
        # Testing creating a new event
        ##
        response = self.client.post(
            reverse('rest_api:sigs-list'),
            data=json.dumps(sig, default=str),
            content_type='application/json'

        )
        self.assertEqual(response.status_code, 201)
        for k in sig:
            self.assertEqual(str(response.json()[k]), str(sig[k]))

        ##
        # Testing "PUT" or modifing a user
        # NOTE: This test requires the data to be sent in a special way due to
        #       how the django client does put requests.
        ##
        sig["description"] = "sig-web"
        response = self.client.put(
            reverse(
                'rest_api:sigs-detail',
                kwargs={'pk': response.json()['id']}
            ),
            data=json.dumps(sig, default=str),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "sig-web")

        ##
        # Testing delete capability
        ##
        sig_id = response.json()['id']
        response = self.client.get(reverse('rest_api:sigs-list'))
        self.assertIsNotNone(response.json()[1])

        response = self.client.delete(
            reverse(
                'rest_api:sigs-detail',
                kwargs={'pk': sig_id}
            )
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.get(
            reverse(
                'rest_api:sigs-detail',
                kwargs={'pk': sig_id}
            )
        )
        self.assertEqual(response.status_code, 404)

        ##
        # Ensure it doesnt exist on the master list
        ##
        response = self.client.get(reverse('rest_api:sigs-list'))
        with self.assertRaises(IndexError):
            self.assertEqual(response.json()[1], None)
        self.assertIsNotNone(response.json()[0])


class TransactionsTestCase(TestCase):
    """
    Ensures a Transaction behaves as expected throughout all
    points in it's lifecycle.
    """

    def setUp(self):
        """
        Initializes all variables and data required to test Transaction
        functionality.
        """
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

    def test_transactions_rest_actions(self):
        """
        Ensures a Transaction behaves as expected throughout all points in the
        REST API.
        """
        transaction = {
            "description": "test",
            "cost": 3,
            "stripe_token": "test",
            "customer_id": "test",
            "coupon_id": "test",
            "subscription_id": "test",
            "category": self.category.id,
            "sig": self.sig.id,
            "user": self.user.id
        }

        ##
        # Testing standard views with initial created model
        ##
        response = self.client.get(reverse('rest_api:transaction-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse(
                'rest_api:transaction-detail',
                kwargs={'pk': self.transaction.id}
            )
        )
        self.assertEqual(response.status_code, 200)

        ##
        # Testing creating a new event
        ##
        response = self.client.post(
            reverse('rest_api:transaction-list'),
            data=json.dumps(transaction, default=str),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        for k in ('description', 'stripe_token'):
            self.assertEqual(str(response.json()[k]), str(transaction[k]))

        ##
        # Testing "PUT" or modifying a user
        # NOTE: This test requires the data to be sent in a special way due to
        #       how the Django client does put requests.
        ##
        transaction["description"] = "test"
        response = self.client.put(
            reverse(
                'rest_api:transaction-detail',
                kwargs={'pk': response.json()['id']}
            ),
            data=json.dumps(transaction, default=str),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["description"], "test")

        ##
        # Testing delete capability
        ##
        transaction_id = response.json()['id']
        response = self.client.get(reverse('rest_api:transaction-list'))
        self.assertIsNotNone(response.json()[1])

        response = self.client.delete(
            reverse(
                'rest_api:transaction-detail',
                kwargs={'pk': transaction_id}
            )
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.get(
            reverse(
                'rest_api:transaction-detail',
                kwargs={'pk': transaction_id}
            )
        )
        self.assertEqual(response.status_code, 404)

        ##
        # Ensure it doesn't exist on the master list
        ##
        response = self.client.get(reverse('rest_api:transaction-list'))
        with self.assertRaises(IndexError):
            self.assertEqual(response.json()[1], None)
        self.assertIsNotNone(response.json()[0])


class CategoryTestCase(TestCase):
    """
    Ensures that Categories behave as expected throughout all points in their
    life-cycle.
    """

    def setUp(self):
        """
        Initializes all variables and data required to test Category
        functionality.
        """
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

    def test_category_rest_actions(self):
        """
        Ensures that a Category behaves as expected at
        each point in the REST API.
        """
        category = {
            "name": "test"
        }

        ##
        # Testing standard views with initial created model
        ##
        response = self.client.get(reverse('rest_api:category-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse(
                'rest_api:category-detail',
                kwargs={'pk': self.category.id}
            )
        )
        self.assertEqual(response.status_code, 200)

        ##
        # Testing creating a new event
        ##
        response = self.client.post(
            reverse('rest_api:category-list'),
            data=json.dumps(category, default=str),
            content_type='application/json'

        )
        self.assertEqual(response.status_code, 201)
        for k in category:
            self.assertEqual(str(response.json()[k]), str(category[k]))

        ##
        # Testing "PUT" or modifying a user
        # NOTE: This test requires the data to be sent in a special way due to
        #       how the Django client does put requests.
        ##
        category["name"] = "test1"
        response = self.client.put(
            reverse(
                'rest_api:category-detail',
                kwargs={'pk': response.json()['id']}
            ),
            data=json.dumps(category, default=str),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "test1")

        ##
        # Testing delete capability
        ##
        category_id = response.json()['id']
        response = self.client.get(reverse('rest_api:category-list'))
        self.assertIsNotNone(response.json()[1])

        response = self.client.delete(
            reverse(
                'rest_api:category-detail',
                kwargs={'pk': category_id}
            )
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.get(
            reverse(
                'rest_api:category-detail',
                kwargs={'pk': category_id}
            )
        )
        self.assertEqual(response.status_code, 404)

        ##
        # Ensure it doesn't exist on the master list
        ##
        response = self.client.get(reverse('rest_api:category-list'))
        with self.assertRaises(IndexError):
            self.assertEqual(response.json()[1], None)
        self.assertIsNotNone(response.json()[0])


class ProductTestCase(TestCase):
    """
    Ensures that a Product behaves as expected throughout all points of its
    life-cycle.
    """

    def setUp(self):
        """
        Initialize all variables and data required to test
        Product functionality.
        """
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

    def test_product_rest_actions(self):
        """
        Ensures that a Product behaves as expected at
        each point in the REST API.
        """
        product = {
            "name": "test",
            "cost": 3.00,
            "description": "test",
            "category": self.category.id,
            "sig": self.sig.id
        }

        ##
        # Testing standard views with initial created model
        ##
        response = self.client.get(reverse('rest_api:product-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(
            reverse(
                'rest_api:product-detail',
                kwargs={'pk': self.product.id}
            )
        )
        self.assertEqual(response.status_code, 200)

        ##
        # Testing creating a new event
        ##
        response = self.client.post(
            reverse('rest_api:product-list'),
            data=json.dumps(product, default=str),
            content_type='application/json'

        )
        self.assertEqual(response.status_code, 201)
        for k in ('name', 'description'):
            self.assertEqual(str(response.json()[k]), str(product[k]))

        ##
        # Testing "PUT" or modifying a user
        # NOTE: This test requires the data to be sent in a special way due to
        #       how the Django client does put requests.
        ##
        product["name"] = "test1"
        response = self.client.put(
            reverse(
                'rest_api:product-detail',
                kwargs={'pk': response.json()['id']}
            ),
            data=json.dumps(product, default=str),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "test1")

        ##
        # Testing delete capability
        ##
        product_id = response.json()['id']
        response = self.client.get(reverse('rest_api:product-list'))
        self.assertIsNotNone(response.json()[1])

        response = self.client.delete(
            reverse(
                'rest_api:product-detail',
                kwargs={'pk': product_id}
            )
        )
        self.assertEqual(response.status_code, 204)
        response = self.client.get(
            reverse(
                'rest_api:product-detail',
                kwargs={'pk': product_id}
            )
        )
        self.assertEqual(response.status_code, 404)

        ##
        # Ensure it doesn't exist on the master list
        ##
        response = self.client.get(reverse('rest_api:product-list'))
        with self.assertRaises(IndexError):
            self.assertEqual(response.json()[1], None)
        self.assertIsNotNone(response.json()[0])
