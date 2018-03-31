"""
Contains all of the unit tests for the rest_api app.
"""
# standard library
import copy
import json
from io import BytesIO

# Django
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# third-party
from PIL import Image
from rest_framework.test import APIClient

# local Django
from accounts.models import User
from accounts.serializers import UserSerializer
from events.models import Event
from events.serializers import EventSerializer
from products.models import Product, Transaction, TransactionCategory
from products.serializers import (CategorySerializer, ProductSerializer,
                                  TransactionSerializer)
from sigs.models import SIG
from sigs.serializers import SIGSerializer


class RestAPITestCase(TestCase):
    """
    Provides standard utilities to the test cases that access the REST API.
    Moreover, implements some standard test cases for all REST endpoints for the
    GET, POST, PUT, and DELETE HTTP methods. In order for these standard tests
    to work, the user must define some initial variables for the TestCase
    including:
        1. ``self.data``: A dictionary containing all the data necessary to
            create a instance of the model with the serializer.
        2. ``self.mod_data``: A modified version of ``self.data`` which can be
            used to make a PUT request.
        3. ``self.model``: The generic model object representative of the
            TestCase. For example, the :class:`accounts.models.User` when
            testing the User endpoints.
        4. ``self.serializer``: The generic serializer instance for the model
            specified in ``self.model``.
        5. ``self.list_path``: The namespace name associated with the list
            endpoint of the API .
        6. ``self.default_path``: The namespace name associated with the detail
            endpoint of the API.
        7. ``self.content_type``: The content_type which can be used to make a
            PUT request with. For most cases it is safe to use
            "application/json" unless there is an attribute which cannot be
            serialized to a JSON.

    Optionally, there are some other class variables that will help with running
    tests on more complicated models:
        1. ``self.exclude``: A list of keys in ``self.data`` or
            ``self.mod_data`` which will be excluded when performing comparisons on
            request results. For example, if there is an ImageField in the
            model, it is impossible to compare a raw image field with a
            serialized image field.

    .. todo::
        There may be a way to compare the results of the response and the raw
        data in the ``self.data`` field more robustly using serializers without
        the self.exclude field.
    """

    def setUp(self):
        """
        Creates all references in the database necessary to instantiate models
        that require related objects and defines some global defaults for all
        test cases. Specifically, rebinds the ``self.client`` to the Django REST
        freamework client and collects the default admin user as
        ``self.default_user``.
        """
        super().setUp()
        self.exclude = []
        self.client = APIClient()
        self.user = User.objects.create_user('ksyh3@mst.edu')
        self.default_user = User.objects.get(email="acm@mst.edu")

        # Save photo to an in-memory bytes buffer. See
        # https://stackoverflow.com/questions/48075739/unit-testing-a-django-form-with-a-imagefield-without-external-file.
        im_io = BytesIO()
        im = Image.new(mode='RGB', size=(50, 50))
        im.save(im_io, 'JPEG')
        # Sets up image variable for creating Event
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=im_io.getvalue(),
            content_type='multipart/form-data'
        )

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

    def assert_request(self, http_method, path, status_code, **kwargs):
        """
        Asserts that a given HTTP method responds with a given status code.

        :param http_method: The HTTP method to perform.
        :type http_method: str
        :param path: The path of the route to perform the request on. Usually
            passed as a result of the reverse() function.
        :type path: str
        :param status_code: The status code to assert the response.status_code
            is equal to.
        :type status_code: int
        :param kwargs: Extra paramaters to pass into the request.
        :type kwargs: dict
        """
        request_func = getattr(self.client, http_method)
        response = request_func(path, **kwargs)
        self.assertEqual(response.status_code, status_code)

    def assert_get_method(self, path, test_dict=None, status_code=200, **kwargs):
        """
        Generically tests a GET method on the specified path by asserting the
        proper status code and if the response content has a element that
        matches the test_dict.

        :param path: The path of the route to perform the request on. Usually
            passed as a result of the reverse() function.
        :type path: str
        :param test_dict: Key, value pairs to assert whether they exist in the
            JSON response. Ensures response.json()[key] equals value for a given
            key, value pair.
        :type test_dict: dict
        :param kwargs: Parameters to be passed into the GET request.
        :type kwargs: dict
        """
        response = self.client.get(path, kwargs=kwargs)
        self.assertEqual(response.status_code, status_code)
        json_response = response.json()

        if test_dict:
            test_items = test_dict.items()
            comparitor = lambda x: test_items <= x.items()
            filtered_resp = list(filter(comparitor, json_response))
            self.assertTrue(filtered_resp)

    def assert_post_method(self, list_path, data, status_code=201, **kwargs):
        """
        Generically tests a POST method on the specified path by ensuring the
        proper response code and the proper data is returned from the post.

        :param list_path: The namespace name associated with the list endpoint
            of the API.
        :type list_path: str
        :param data: The data to be POSTed to the specified ``list_path``.
        :type data: dict
        :param status_code: The status_code to assert the response returns.
        :type status_code: int
        :param kwargs: Parameters to be passed into the POST request.
        :type kwargs: dict
        """
        response = self.client.post(list_path, data)
        self.assertEqual(response.status_code, status_code)
        json_response = response.json()

        for key, value in data.items():
            if not key in self.exclude:
                self.assertEqual(json_response[key], value)

    def assert_put_method(self, detail_path, data, status_code=200, **kwargs):
        """
        Generically tests a PUT method on the specific path by ensuring the
        proper response.

        :param detail_path: The namespace name associated with the detail
            endpoint of the API.
        :type detail_path: str
        :param data: The data to be PUT to the specified ``detail_path``.
        :type data: dict
        :param status_code: The status_code to assert the response returns.
        :type status_code: int
        :param kwargs: Parameters to be passed into the PUT request.
        :type kwargs: dict
        """
        request_data = None
        content_type = kwargs.get("content_type")
        kwargs["content_type"] = "application/json"
        if content_type == "multipart/form-data":
            kwargs.setdefault("format", "multipart")
            kwargs.pop("content_type")
            request_data = data
        else:
            request_data = json.dumps(data)

        response = self.client.put(
            detail_path,
            data=request_data,
            **kwargs
        )
        self.assertEqual(response.status_code, status_code)
        json_response = response.json()
        for key, value in data.items():
            if not key in self.exclude:
                self.assertEqual(json_response[key], value)


    def assert_delete_method(self, list_path, detail_path, key, value,
                             status_code=204):
        """
        Generically tests a DELETE method on the specific path by ensuring the
        proper response and the item specified is successfully deleted.

        :param list_path: The namespace name associated with the list endpoint
            of the API.
        :type list_path: str
        :param detail_path: The namespace name associated with the detail
            endpoint of the API.
        :type detail_path: str
        :param key: A primary key to look the model up by in the master list.
        :type key: str
        :param value: The value of the primary key for the model specified in
            the ``detail_path``.
        :type value: str or int
        """
        response = self.client.delete(
            detail_path
        )
        self.assertEqual(response.status_code, status_code)
        self.assert_not_exists(detail_path)

        ##
        # Ensure it doesnt exist on the master list
        ##
        response = self.client.get(list_path)
        response_json = response.json()
        filtered_resp = list(
            filter(lambda x: x.get(key) == value, response_json)
        )

        # Asert the filtered list is empty (The item does not exist in the
        # master list)
        self.assertFalse(filtered_resp)

    def assert_not_exists(self, path):
        """
        Asserts that a given path returns a 404 in the response status code.

        :param path: The path to perform the GET request on.
        :type path: str
        """
        self.assert_request("get", path, 404)

    def assert_rest_actions(self, list_viewname, detail_viewname,
                            data, mod_data, model, content_type):
        """
        Asserts that the GET, POST, PUT, and DELETE behave properly by
        returning the correct values and status codes.

        :param list_viewname: The path namespace associated with the list
            endpoint for the model.
        :type list_viewname: str
        :param detail_viewname: The path namespace asscoiated with the detail
            endpoint for the model.
        :type detail_viewname: str
        :param data: Data that can be used to instatiate the model with the
            serializer.
        :type data: dict
        :param mod_data: A modified version of ``data`` which can be
            used to make a PUT request and modify the original instance of the
            model.
        :type mod_data: dict
        :param model: The generic model object that can be viewed and modified
        in ``list_viewname`` and ``detail_viewname``.
        :type model: :class:`django.db.models.Model`
        :param content_type: The content_type which can be used to make a
            PUT request with.
        :type content_type: str
        """
        # If these are the same, it defeats the purpose of the PUT request
        self.assertNotEqual(data, mod_data)

        self.assert_post_method(reverse(list_viewname), data)
        search_data = {k: v for k, v in data.items() if not k in self.exclude}

        pk_key = model._meta.pk.name
        pk_val = getattr(model.objects.get(**search_data), pk_key)
        self.assert_put_method(
            reverse(detail_viewname, kwargs={'pk': pk_val}),
            data=mod_data,
            content_type=content_type,
        )

        self.assert_delete_method(
            reverse(list_viewname),
            reverse(detail_viewname, kwargs={'pk': pk_val}),
            pk_key,
            pk_val,
        )

    def assert_requires_proper_permissions(self, list_path, detail_path):
        """
        Asserts that the endpoints for a model requires proper permissions to
        perform actions.

        :param list_path: The namespace name associated with the list endpoint
            of the API .
        :type list_path: str
        :param detail_path: The namespace name associated with the detail
            endpoint of the API .
        :type detail_path: str
        """
        self.assert_request("post", list_path, 403, data={})
        self.assert_request("put", detail_path, 403, data={})
        self.assert_request("delete", detail_path, 403)

    def acquire_permissions(self):
        """
        Gives the ``self.client`` attribute the required permissions to perform
        all action the API.

        .. todo::
            Allow more granular permissions granting when the permission system
            is implemented.
        """
        self.client.force_login(self.default_user)

    def test_rest_actions(self):
        """
        Ensures that the rest actions for the model specified in the class
        returns the proper results for the GET, POST, PUT, and DELETE methods.
        """
        self.acquire_permissions()

        data = self.data
        mod_data = self.mod_data

        self.assert_get_method(reverse(self.list_path))
        self.assert_rest_actions(
            self.list_path, self.detail_path,
            data, mod_data, self.model, self.content_type
        )

    def test_rest_actions_without_permissions(self):
        """
        Ensures that the rest actions for the model specified in the class fails
        if the user does not have the proper permissions.
        """
        model_serializer = self.serializer(data=self.data)
        if model_serializer.is_valid():
            model_obj = model_serializer.save()
            model_obj_pk_val = getattr(model_obj, model_obj._meta.pk.name)

            self.assert_requires_proper_permissions(
                reverse(self.list_path),
                reverse(self.detail_path, kwargs={'pk': model_obj_pk_val}),
            )
        else:
            raise ValueError("Serializer is not valid.")


class AccountsTestCase(RestAPITestCase):
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
        self.data = {
            "email": "test@mst.edu",
            "first_name": "test",
            "last_name": "test",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False
        }
        self.mod_data = {
            "email": "test1@mst.edu",
            "first_name": "test",
            "last_name": "test",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False
        }
        self.model = User
        self.serializer = UserSerializer
        self.list_path = 'rest_api:user-list'
        self.detail_path = 'rest_api:user-detail'
        self.content_type = "application/json"

    def test_serializer_validation(self):
        """
        Ensures that the :class:`~accounts.serializers.UserSerializer`
        functions as intended.
        """
        user = self.data
        self.client.force_login(self.default_user)
        user['email'] = "test@fail.com"
        response = self.client.post(reverse('rest_api:user-list'), user)
        self.assertEqual(response.status_code, 400)

    def test_rest_actions(self):
        super().test_rest_actions()


class EventsTestCase(RestAPITestCase):
    """
    Ensures Events behave as expected throughout their lifecycle.
    """

    def setUp(self):
        """
        Initializes all variables and data required to test Event
        functionality.
        """
        super().setUp()
        self.exclude = ["date_hosted", "date_expire", "flier"]

        self.data = {
            "date_hosted": timezone.now(),
            "date_expire": timezone.now(),
            "title": "test1",
            "description": "test",
            "location": "test",
            "presenter": "test",
            "cost": "3.00",
            "flier": self.image,
            "creator": str(self.user.id),
            "hosting_sig": str(self.sig.id),
        }
        self.mod_data = copy.deepcopy(self.data)
        self.mod_data["title"] = "test2"
        self.model = Event
        self.serializer = EventSerializer
        self.list_path = 'rest_api:event-list'
        self.detail_path = 'rest_api:event-detail'
        self.content_type = "multipart/form-data"

    def test_rest_actions(self):
        super().test_rest_actions()


class SigsTestCase(RestAPITestCase):
    """
    Ensures that a SIG behaves as expected throughout it's lifecycle.
    """

    def setUp(self):
        """
        Initializes all variables and data required to test SIG functionality.
        """
        super().setUp()
        self.data = {
            "id": "sig_test",
            "is_active": True,
            "description": "test",
            "founder": str(self.user.id),
            "chair": str(self.user.id)
        }
        self.mod_data = {
            "id": "sig_test1",
            "is_active": True,
            "description": "test",
            "founder": str(self.user.id),
            "chair": str(self.user.id)
        }

        self.model = SIG
        self.serializer = SIGSerializer
        self.list_path = 'rest_api:sig-list'
        self.detail_path = 'rest_api:sig-detail'
        self.content_type = "application/json"

    def test_rest_actions(self):
        super().test_rest_actions()


class TransactionsTestCase(RestAPITestCase):
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
        self.data = {
            "description": "test",
            "cost": "3.00",
            "stripe_token": "test",
            "customer_id": "test",
            "coupon_id": "test",
            "subscription_id": "test",
            "charge_id": "test",
            "category": str(self.category.id),
            "sig": str(self.sig.id),
            "user": str(self.user.id)
        }
        self.mod_data = {
            "description": "test2",
            "cost": "3.00",
            "stripe_token": "test",
            "customer_id": "test",
            "coupon_id": "test",
            "subscription_id": "test",
            "charge_id": "test",
            "category": str(self.category.id),
            "sig": str(self.sig.id),
            "user": str(self.user.id)
        }
        self.model = Transaction
        self.serializer = TransactionSerializer
        self.list_path = 'rest_api:transaction-list'
        self.detail_path = 'rest_api:transaction-detail'
        self.content_type = "application/json"

    def test_rest_actions(self):
        super().test_rest_actions()


class CategoryTestCase(RestAPITestCase):
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
        self.data = {
            "name": "test1"
        }
        self.mod_data = {
            "name": "test2"
        }
        self.model = TransactionCategory

        self.serializer = CategorySerializer
        self.list_path = 'rest_api:category-list'
        self.detail_path = 'rest_api:category-detail'
        self.content_type = "application/json"

    def test_rest_actions(self):
        super().test_rest_actions()


class ProductTestCase(RestAPITestCase):
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
        self.data = {
            "tag": "name",
            "name": "test",
            "cost": "3.00",
            "description": "test",
            "category": str(self.category.id),
            "sig": str(self.sig.id)
        }
        self.mod_data = {
            "tag": "name",
            "name": "test1",
            "cost": "3.00",
            "description": "test",
            "category": str(self.category.id),
            "sig": str(self.sig.id)
        }
        self.model = Product
        self.serializer = ProductSerializer
        self.list_path = 'rest_api:product-list'
        self.detail_path = 'rest_api:product-detail'
        self.content_type = "application/json"

    def test_rest_actions(self):
        super().test_rest_actions()
