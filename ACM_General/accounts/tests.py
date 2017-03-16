from . import models
from django.db import IntegrityError
from accounts.backends import UserBackend
from django.test import TestCase
from django.urls import reverse
# Create your tests here.


class UserModelCase(TestCase):
    def setUp(self):
        super(UserModelCase, self).setUp()
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

    def test_user_unique_exception_thrown(self):
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
        models.User.objects.get(email="test@mst.edu")

        models.User.objects.all()

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

    @staticmethod
    def test_can_change_user():
        user = models.User.objects.get(email="test@mst.edu")

        ##
        # Don't make a test with matching email please, will break test
        ##
        user.email = "GETCHANGEDKID@mst.edu"

        user.save(update_fields=['email'])
        models.User.objects.get(email="GETCHANGEDKID@mst.edu")

    def test_user_model_member_functions(self):
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
        self.assertEqual(str(user), "johndoe@mst.edu")

class ManagerTestCase(TestCase):
    """
    @Desc - Testing the User Manager and all of its member functinos.
    """
    def setUp:
        super(TestCase, self).setUp()

    def test_get_by_natural_key(self):
        pass

    def test_create_user_function(self):
        pass

    def test_create_superuser_function(self):
        pass


class AccountsViewCase(TestCase):
    """
    @Desc - This Test Case evaluates each of the different facets of the views
            in the accounts app.
    """

    def setUp(self):
        """
        @Desc - Setup a global client in which all the test cases may use to
                reduce redundancy.
        """
        super(AccountsViewCase, self).setUp()

    def test_status_codes(self):
        """
        @Desc - Determines whether every view returns the proper response code
                in the accounts app. Could determine in-view syntax errors or
                initial procsesing errors.
        """

        response = self.client.get(reverse('accounts:user-logout'), follow=True)
        self.assertEqual(response.redirect_chain[0][1], 302)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

        response = self.client.get(reverse('accounts:user-login'))
        self.assertTemplateUsed(response, 'accounts/login.html')

        self.assertEqual(response.status_code, 200)

    def test_logout_system(self):
        """
        @Desc - Determines whether or not the user logout is working properly
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


class UserAuthBackendCase(TestCase):
    """
    @Desc - This test case evalatues all of the different authentication
            methodso which accounts.managers.UserBackend provides.
    """

    def setUp(self):
        """
        @Desc - Creates a 'global' user for each function to run authentication
                functions on as well as spare users in the database.
        """
        super(UserAuthBackendCase, self).setUp()
        self.backend = UserBackend()
        models.User.objects.create_user("test@mst.edu")
        models.User.objects.create_user("test2@mst.edu", is_active=False)


    def test_authenticate_function(self):
        """
        @Desc - Tests the authenticate function in the Backend.
        """


        self.assertEqual(self.backend.authenticate(email="fail@mst.edu"), None)
        self.assertIsNotNone(self.backend.authenticate(email="test@mst.edu"))
        self.assertEqual(self.backend.authenticate(email="fail2@mst.edu"), None)
        self.assertEqual(self.backend.authenticate(), None)

    def test_user_can_authenticate_function(self):
        """
        @Desc - Tests the user_can_authenticate function
        """
        self.assertEqual(self.backend.user_can_authenticate(models.User.objects.get(email="test@mst.edu")), True)
        self.assertEqual(self.backend.user_can_authenticate(models.User.objects.get(email="test2@mst.edu")), False)
        with self.assertRaises(TypeError):
            self.assertEqual(self.backend.user_can_authenticate())

    def test_get_user_function(self):
        user = models.User.objects.create_user('test4@mst.edu')
        self.assertIsNotNone(self.backend.get_user(user.id))
        with self.assertRaises(ValueError):
            self.backend.get_user('1232-a4')
        self.assertEqual(self.backend.get_user('e1e73e34-09f1-11e7-bff3-afc1ff1d82f0'), None)
