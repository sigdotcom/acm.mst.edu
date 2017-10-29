"""
Contains all unit tests for the accounts app.
"""
# standard library
import uuid

# Django
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

# local Django
from . import models
from accounts.backends import UserBackend


class UserModelCase(TestCase):
    """
    Testing that the User model behaves as intended.
    """

    def setUp(self):
        """
        Ensures that tests are set up properly before execution.
        Initializes any required variables and data.
        Creates two test Users.
        """
        super().setUp()
        models.User.objects.create(
            email="test@mst.edu",
            first_name="test_me",
            last_name="test_please",
        )

        models.User.objects.create(
            email="test2@mst.edu",
            first_name="test",
            last_name="test",
        )

    def test_duplicate_user_error(self):
        """
        Ensures that erroneous duplicate user creation is caught
        and handled properly.
        """
        with self.assertRaises(IntegrityError):
            models.User.objects.create(
                email="duplicate@mst.edu",
                first_name="test",
                last_name="test",
            )
            models.User.objects.create(
                email="duplicate@mst.edu",
                first_name="test",
                last_name="test",
            )

    def test_can_retrieve_users(self):
        """
        Ensures that the ability to retrieve users is working as intended.
        """
        self.assertIsNotNone(models.User.objects.get(email="test@mst.edu"))
        self.assertIsNotNone(models.User.objects.all())

        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get(
                email="test@mst.edu",
                first_name="test",
            )

        models.User.objects.get(
            email="test@mst.edu",
            first_name="test_me",
            last_name="test_please",
        )

    def test_can_edit_user(self):
        """
        Ensures that the ability to edit users is working as intended.
        """
        user = models.User.objects.get(email="test@mst.edu")
        self.assertIsNotNone(user)
        ##
        # Don't make a test with matching email please, will break test
        ##
        self.assertEqual(user.email, "test@mst.edu")
        user.email = "GETCHANGEDKID@mst.edu"
        user.save(update_fields=['email'])
        self.assertIsNotNone(
            models.User.objects.get(email="GETCHANGEDKID@mst.edu")
        )

    def test_user_model_member_functions(self):
        """
        Ensures that the user model member functions are working as intended.
        """
        user = models.User.objects.create(
            email="johndoe@mst.edu",
            first_name="John",
            last_name="Doe",
            is_superuser=False,
        )
        superuser = models.User.objects.create_superuser("superadmin@mst.edu")

        self.assertEqual(superuser.is_staff, True)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.get_full_name(), "John Doe")
        self.assertEqual(user.get_short_name(), "johndoe@mst.edu")
        self.assertEqual(user.is_admin, False)
        self.assertEqual(superuser.is_admin, True)
        self.assertEqual(str(user), "johndoe@mst.edu")


class ManagerTestCase(TestCase):
    """
    Testing the User Manager and all of its member functions.
    """

    def setUp(self):
        """
        Ensures that tests are set up properly before execution.
        Initializes any required variables and data.
        """
        super().setUp()

    def test_get_by_natural_key(self):
        """
        Ensures that the user can be retrieved by natural key.
        """
        models.User.objects.create_user('testme@mst.edu')
        self.assertIsNotNone(
            models.User.objects.get_by_natural_key('testme@mst.edu')
        )
        with self.assertRaises(models.User.DoesNotExist):
            models.User.objects.get_by_natural_key('notindatabase@mst.edu')

    def test_create_user_function(self):
        """
        Ensures that the create_user function is working as intended.
        """
        self.assertIsNotNone(models.User.objects.create_user('testme@mst.edu'))
        with self.assertRaises(ValueError):
            models.User.objects.create_user('test@fail.com')
        with self.assertRaises(TypeError):
            models.User.objects.create_user()
        with self.assertRaises(ValueError):
            models.User.objects.create_user('test')
        with self.assertRaises(ValueError):
            models.User.objects.create_user('@')
        with self.assertRaises(ValueError):
            user = models.User.objects.create_user('@mst.edu')

        user = models.User.objects.create_user(
            'test@mst.edu',
            first_name="Test",
            last_name="Me",
            is_active=True,
        )
        self.assertEqual(user.email, 'test@mst.edu')
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Me")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.is_staff, False)

    def test_create_superuser_function(self):
        """
        Ensures that the create_superuser function is working as intended.
        """
        self.assertIsNotNone(
            models.User.objects.create_superuser('testadmin2@mst.edu')
        )
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser('test@fail.com')
        with self.assertRaises(TypeError):
            models.User.objects.create_superuser()
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser('test')
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser('@')
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser('@mst.edu')
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser(
                'fdksalj@mst.edu',
                is_staff=False
            )
        with self.assertRaises(ValueError):
            models.User.objects.create_superuser(
                'fdksalj@mst.edu',
                is_superuser=False
            )

        user = models.User.objects.create_superuser(
            'testadmin@mst.edu',
            first_name="Test",
            last_name="Me",
            is_active=True,
        )

        self.assertEqual(user.email, "testadmin@mst.edu")
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "Me")
        self.assertEqual(user.is_active, True)
        self.assertEqual(user.is_superuser, True)
        self.assertEqual(user.is_staff, True)


class ViewTestCase(TestCase):
    """
    Evaluates each of the different facets of the views in the accounts app.
    """

    def setUp(self):
        """
        Ensures that tests are set up properly before execution.
        Initializes any required variables and data.
        """
        super().setUp()

    def test_status_codes(self):
        """
        Determines whether every view returns the proper response code
        in the accounts app. Could determine in-view syntax errors or
        initial processing errors.
        """

        response = self.client.get(
            reverse('accounts:user-logout'), follow=True
        )
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

        response = self.client.get(reverse('accounts:user-login'))
        self.assertTemplateUsed(response, 'accounts/login.html')

        self.assertEqual(response.status_code, 200)

    def test_login_system(self):
        """
        TODO: Implement with Selenium
        """
        pass

    def test_logout_system(self):
        """
        Determines whether or not the user logout is working properly
        by creating a client, forcing the client to login, and then
        visiting the logout page.
        """
        user = models.User.objects.create_user(email="testclient@mst.edu",
                                               first_name="Client",
                                               last_name="Client")
        self.assertIsNotNone(user)
        self.client.force_login(user, backend='accounts.backends.UserBackend')
        self.assertIsNotNone(self.client.session['_auth_user_id'])
        response = self.client.get(reverse('accounts:user-logout'))
        with self.assertRaises(KeyError):
            self.client.session['_auth_user_id']
        self.assertEqual(response.status_code, 302)


class UserAuthBackendCase(TestCase):
    """
    Evaluates all of the different authentication
    methods which :class:`accounts.backends.UserBackend` provides.
    """

    def setUp(self):
        """
        Creates a 'global' user for each function to run authentication
        functions on as well as spare users in the database.
        """
        super().setUp()
        self.backend = UserBackend()
        models.User.objects.create_user("test@mst.edu")
        models.User.objects.create_user("test2@mst.edu", is_active=False)

    def test_authenticate_function(self):
        """
        Ensures that the authenticate function in the Backend works as
        intended.
        """
        self.assertEqual(
            self.backend.authenticate(email="fail@mst.edu"), None
        )
        self.assertIsNotNone(self.backend.authenticate(email="test@mst.edu"))
        self.assertEqual(
            self.backend.authenticate(email="fail2@mst.edu"), None
        )
        self.assertEqual(self.backend.authenticate(), None)
        models.User.objects.create_user(
            'thisisatest@mst.edu', is_active=False
        )
        self.assertEqual(
            self.backend.authenticate('thisisatest@mst.edu'), None
        )

    def test_user_can_authenticate_function(self):
        """
        Ensures that the user_can_authenticate function works as intended.
        """
        self.assertEqual(self.backend.user_can_authenticate(
            models.User.objects.get(email="test@mst.edu")), True
        )
        self.assertEqual(self.backend.user_can_authenticate(
            models.User.objects.get(email="test2@mst.edu")), False
        )
        with self.assertRaises(TypeError):
            self.assertEqual(self.backend.user_can_authenticate())

    def test_get_user_function(self):
        user = models.User.objects.create_user('test4@mst.edu')
        self.assertIsNotNone(self.backend.get_user(user.id))

        self.assertEqual(
            self.backend.get_user(uuid.uuid1()),
            None
        )


class PermissionModelTestCase(TestCase):
    """
    TODO: Implement after Permissions.
    """
    pass


class GroupModelTestCase(TestCase):
    """
    TODO: Implement after Groups.
    """
    pass
