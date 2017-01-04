from django.test import TestCase
from accounts.models import User
from django.db import IntegrityError

# Create your tests here.

class UserSetupCase(TestCase):

    def setUp(self):
        User.objects.create(
            email="test@mst.edu",
            first_name="test_me",
            last_name="test_please",
        )

        User.objects.create(
            email="test2@mst.edu",
            first_name="test",
            last_name="test",
        )
        
    def test_create_users(self):
        superuser = User.objects.create_superuser("superadmin@mst.edu")
        user = User.objects.create_user("eeafjeakl@mst.edu")
        with self.assertRaises(ValueError):
            user2 = User.objects.create_user("feafsda@test.edu")

        User.objects.create(
            email="lol@mst.edu",
            first_name="lol",
            last_name="lol",
        )

    def test_user_unique_exception_thrown(self):
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email="duplicate@mst.edu",
                first_name="test",
                last_name="test",
            )
            User.objects.create(
                email="duplicate@mst.edu",
                first_name="test",
                last_name="test",
            )
            

    def test_can_retrieve_users(self):
        User.objects.get(email="test@mst.edu")

        User.objects.all()
        
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(
                email="test@mst.edu",
                first_name = "test",
            )

        User.objects.get(
                email="test@mst.edu",
                first_name= "test_me",
                last_name="test_please",
            ) 
    def test_can_change_user(self):
        user = User.objects.get(email="test@mst.edu")

        ##
        # Don't make a test with matching email please, will break test
        ##
        user.email = "GETCHANGEDKID@mst.edu"

        user.save(update_fields=['email'])
        User.objects.get(email="GETCHANGEDKID@mst.edu")

    def test_user_model_member_functions(self):
        user = User.objects.create(
            email="johndoe@mst.edu",
            first_name="John",
            last_name="Doe",
            is_superuser = False,
        )

        superuser = User.objects.create_superuser("superadmin@mst.edu")

        self.assertEqual(superuser.is_admin, True)
        self.assertEqual(user.is_admin, False)
        self.assertEqual(user.get_full_name(), "John Doe")
        self.assertEqual(user.get_short_name(), "johndoe@mst.edu")
        self.assertEqual(str(user), "johndoe@mst.edu")
