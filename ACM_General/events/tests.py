from . import models
from accounts.models import User
from django.db import transaction
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from sigs.models import SIG

# Create your tests here.

class ManagerTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user=User.objects.create_user('test@mst.edu')
        self.sig=SIG.objects.create_sig(
                            founder=self.user,
                            chair=self.user,
                            description='test',
                        )

    def test_create_event(self):
        self.assertIsNotNone(timezone.now)
        models.Event.objects.create_event(
                        creator=self.user,
                        hosting_sig=self.sig,
                        title='test',
                        date_hosted=timezone.now(),
                        date_expire=timezone.now(),
                    )
        with transaction.atomic():
            with self.assertRaises(ValueError):
                models.Event.objects.create_event(
                                creator=self.user,
                                hosting_sig=self.sig,
                                title='test',
                                date_hosted=timezone.now(),
                                date_expire=timezone.now()-timezone.timedelta(days=1),
                            )

        with transaction.atomic():
            with self.assertRaises(ValueError):
                models.Event.objects.create_event(title='test2')

        with transaction.atomic():
            with self.assertRaises(ValueError):
                models.Event.objects.create_event()

        with transaction.atomic():
            with self.assertRaises(ValueError):
                models.Event.objects.create_event(
                                        creator=self.user,
                                        hosting_sig=self.sig,
                                )
        with transaction.atomic():
            with self.assertRaises(ValueError):
                models.Event.objects.create_event(
                                        creator=self.user,
                                        hosting_sig=self.sig,
                                        date_hosted=timezone.now(),
                                )

    def test_get_by_natural_key(self):
        event=models.Event.objects.create_event(
                        creator=self.user,
                        hosting_sig=self.sig,
                        title='test',
                        date_hosted=timezone.now(),
                        date_expire=timezone.now(),
                    )

        self.assertIsNotNone(models.Event.objects.get_by_natural_key('test'))
        with self.assertRaises(models.Event.DoesNotExist):
            models.Event.objects.get_by_natural_key('notreal')

        self.assertEqual(event.is_active, False)


class ModelTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user=User.objects.create_user('test@mst.edu')
        self.sig=SIG.objects.create_sig(
                            founder=self.user,
                            chair=self.user,
                            description='test',
                        )


    def test_member_functions(self):
        event=models.Event.objects.create_event(
                        creator=self.user,
                        hosting_sig=self.sig,
                        title='test',
                        date_hosted=timezone.now(),
                        date_expire=timezone.now(),
                    )

        self.assertEqual(event.is_active, False)

        event2=models.Event.objects.create_event(
                        creator=self.user,
                        hosting_sig=self.sig,
                        title='test',
                        date_hosted=timezone.now(),
                        date_expire=timezone.now()+timezone.timedelta(days=1),
                    )
        self.assertEqual(event2.is_active, True)


class ViewTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def test_view_integrity(self):
        response = self.client.get(reverse('events:events-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/listEvents.html')

