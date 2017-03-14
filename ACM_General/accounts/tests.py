from django.test import TestCase
from . import models
from django.db import IntegrityError

# Create your tests here.


class UserSetupCase(TestCase):
    def setUp(self):
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
        
    def test_create_users(self):
        superuser = models.User.objects.create_superuser("superadmin@mst.edu")
        user = models.User.objects.create_user("eeafjeakl@mst.edu")

        self.assertIsNotNone(superuser)
        self.assertIsNotNone(user)

        with self.assertRaises(ValueError):
            models.User.objects.create_user("feafsda@test.edu")

        test = models.User.objects.create(
            email="lol@mst.edu",
            first_name="lol",
            last_name="lol",
        )

        self.assertIsNotNone(test)

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
