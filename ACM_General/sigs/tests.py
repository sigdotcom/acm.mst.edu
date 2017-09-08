# Django
from django.db import IntegrityError
from django.test import TestCase

# local Django
from . import models
from accounts.models import User


class SIGManagerCase(TestCase):
    """
    Tests for the SIGManager
    """
    def setUp(self):
        super(TestCase, self).setUp()

    def test_get_by_natural_key_function(self):
        """
        Verifies that the function get_by_natural_key_function() is working

        :rtype: None
        :return: None
        """
        user = User.objects.create_user('test@mst.edu')
        sig = models.SIG.objects.create_sig(
                                id="sig_sec",
                                founder=user,
                                chair=user,
                                description="test",
                            )

        self.assertIsNotNone(models.SIG.objects.get_by_natural_key("sig_sec"))
        with self.assertRaises(models.SIG.DoesNotExist):
            models.SIG.objects.get_by_natural_key("test")


    def test_create_sig_function(self):
        """
        Verifies that the create_sig_function() function is working as intended

        :rtype: None
        :return: None
        """
        user = User.objects.create_user('test@mst.edu')

        with self.assertRaises(ValueError):
            models.SIG.objects.create_sig(id='test')
        with self.assertRaises(ValueError):
            models.SIG.objects.create_sig(description='test')
        with self.assertRaises(ValueError):
            models.SIG.objects.create_sig(id='test', founder=user)

        sig = models.SIG.objects.create_sig(
                                id='test',
                                description='test',
                                founder=user,
                                chair=user,
                        )

        self.assertEqual(sig.id, 'test')
        self.assertEqual(sig.description, 'test')
        self.assertEqual(sig.founder, user)
        self.assertEqual(sig.chair, user)

class SIGModelCase(TestCase):
    """
    Test suite for SIG models and their functions.
    """
    def setUp(self):
        self.user = User.objects.create_user('test@mst.edu')
        super().setUp()

    def test_sig_model_member_functions(self):
        """
        Checks if the __str__ dunder function works inside of the SIG model.

        :rtype: None
        :return: None
        """

        sig = models.SIG.objects.create_sig(
                                id='test',
                                description='test',
                                founder=self.user,
                                chair=self.user,
                        )
        self.assertEqual(str(sig), sig.id)

    def test_sig_unique_constraint(self):
        """
        Verifies that you will get an error is trying to make two of the
        same SIG

        :rtype: None
        :return: None
        """
        sig = models.SIG.objects.create_sig(
                                id='test',
                                description='test',
                                founder=self.user,
                                chair=self.user,
                        )

        with self.assertRaises(IntegrityError):
            sig = models.SIG.objects.create_sig(
                                id='test',
                                description='test',
                                founder=self.user,
                                chair=self.user,
                        )

    def test_can_retrieve_sigs(self):
        """
        Makes sure that the get function can both return a SIG and know when to
        error.
        
        :rtype: None
        :return: None
        """
        sig = models.SIG.objects.create_sig(
                                id='test',
                                description='test',
                                founder=self.user,
                                chair=self.user,
                        )

        self.assertIsNotNone(models.SIG.objects.get(id='test'))
        self.assertIsNotNone(models.SIG.objects.all())

        with self.assertRaises(models.SIG.DoesNotExist):
            models.SIG.objects.get(id='thisisntreal')

    def test_can_edit_sig(self):
        """
        Checks that the ability to edit works as normal

        :rtype: None
        :return: None
        """
        sig = models.SIG.objects.create_sig(
                                id='test',
                                description='test',
                                founder=self.user,
                                chair=self.user,
                        )
        self.assertEqual(sig.is_active, True)
        sig.is_active = False
        sig.save(update_fields=['is_active'])
        sig2 = models.SIG.objects.get(id='test')
        self.assertEqual(sig2.is_active, False)
