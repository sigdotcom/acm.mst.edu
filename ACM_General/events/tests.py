from . import models
from accounts.models import User
from django.db import transaction
from django.db.utils import IntegrityError
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from sigs.models import SIG
from django.core.files.uploadedfile import TemporaryUploadedFile
import os
import shutil
from datetime import datetime

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
        event = models.Event.objects.create_event(
                        creator=self.user,
                        hosting_sig=self.sig,
                        title='test',
                        date_hosted=timezone.now(),
                        date_expire=timezone.now(),
                    )
        self.assertIsNotNone(event)

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

    def test_get_path_for_flier_function_along_with_image_field(self):
        # Creating a temporary image for testing
        temp_image = TemporaryUploadedFile(name='test_image.jpg', content_type='image/jpeg', size=4, charset='utf-8')

        # Use the min datetime since I'll be adding it to the fliers folder and the deleting it;
        # using the min datetime will guaruntee that I'm not deleting any fliers that aren't being
        # used for testing purposes.
        test_date = datetime.min

        # Makes the test date 'aware' as to satisfy django's enabled timezone feature
        test_date = timezone.make_aware(test_date, timezone.get_current_timezone())

        # Create an event that uses the date and image I created
        event=models.Event.objects.create_event(
            creator=self.user,
            hosting_sig=self.sig,
            title='test',
            date_hosted=test_date,
            date_expire=test_date,
            flier=temp_image,
        )

        test_date = str(test_date)[:10]

        # Checks that image is created inside the correct directory
        self.assertEqual(os.path.exists('fliers/{}/test_image.jpg'.format(test_date)), True)

        # Close the temp image and delete the directory created for testing
        temp_image.close()
        shutil.rmtree('fliers/{}'.format(test_date))


class ViewTestCase(TestCase):
    def setUp(self):
        super().setUp()

    def test_view_integrity(self):
        response = self.client.get(reverse('events:events-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/listEvents.html')
