# standard library
from datetime import datetime
import os
import shutil
import tempfile

# Django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# local Django
from . import models
from .forms import EventForm
from accounts.models import User
from sigs.models import SIG


class ManagerTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user('test@mst.edu')
        self.sig = SIG.objects.create_sig(
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
        event = models.Event.objects.create_event(
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
        self.user = User.objects.create_user('test@mst.edu')
        self.sig = SIG.objects.create_sig(
            founder=self.user,
            chair=self.user,
            description='test',
        )

        # Sets up image variable for creating Event
        image_path = 'test_data/test_image.jpg'
        self.image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        self.temp_dir = tempfile.TemporaryDirectory()
        settings.MEDIA_ROOT = self.temp_dir.name

    def tearDown(self):
        super().tearDown()
        self.temp_dir.cleanup()

    def test_is_active_member_function(self):
        event = models.Event.objects.create(
            creator=self.user,
            hosting_sig=self.sig,
            title='test',
            date_hosted=timezone.now(),
            date_expire=timezone.now(),
            flier=self.image,
            description='Here is a test description',
            location='test location',
        )

        # This event model is correct besides the fact that by the time the 'is_active' function is called,
        # it will notice that the host and expiration date fall before the current date (by some amount of
        # micro-seconds) and will give a ValidationError; but this error is only raised if the clean method
        # for the event model is called which is by default for models, not called. But for this scenario,
        # that's okay since we're testing to make sure the 'is_active' method works correctly.
        self.assertFalse(event.is_active)

        event2 = models.Event.objects.create(
            creator=self.user,
            hosting_sig=self.sig,
            title='test',
            date_hosted=timezone.now()+timezone.timedelta(hours=1),
            date_expire=timezone.now()+timezone.timedelta(hours=2),
            flier=self.image,
            description='Here is a test description',
            location='test location',
        )
        event2.full_clean()
        self.assertTrue(event2.is_active)

    def test_get_path_for_flier_function_along_with_image_field(self):
        test_date = timezone.now() + timezone.timedelta(hours=1)

        # Create an event that uses the datetime and image I created
        event = models.Event.objects.create(
            creator=self.user,
            hosting_sig=self.sig,
            title='test',
            date_hosted=test_date,
            date_expire=timezone.now()+timezone.timedelta(hours=2),
            flier=self.image,
            description='Here is a test description',
            location='test location',
        )

        # Cleans the model by calling clean_fields(), clean(), and validate_unique() methods
        event.full_clean()

        # Checks that image is created inside the correct directory
        test_date = str(test_date)[:10]
        self.assertTrue(os.path.exists('{}/{}/{}/test_image.jpg'.format(settings.MEDIA_ROOT, settings.FLIERS_PATH, test_date)))


class ViewTestCase(TestCase):
    def setUp(self):
        super().setUp()

        # Create a superuser and sig for testing purposes
        self.email = 'test@mst.edu'
        self.user = User.objects.create_superuser(self.email)
        self.sig = SIG.objects.create_sig(
            founder=self.user,
            chair=self.user,
            description='test',
        )

        # Sets up image variable for creating Event
        image_path = 'test_data/test_image.jpg'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        # Have to specify the datetime formats since these datetimes are being done through the create-event page
        # rather than being created via the model or modelform.
        test_date1 = str(timezone.now() + timezone.timedelta(days=1))[:16]
        test_date2 = str(timezone.now() + timezone.timedelta(days=2))[:16]

        # Test data for creating events
        self.data = {
            'creator': self.user,
            'date_hosted': test_date1,
            'date_expire': test_date2,
            'hosting_sig': self.sig,
            'title': 'Test Title',
            'description': 'Here is a test description',
            'location': 'CS 207',
            'presenter': 'test',
            'cost': 10.00,
            'link': 'acm.mst.edu',
            'flier': image,
        }

    def test_view_integrity(self):
        response = self.client.get(reverse('events:events-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/listEvents.html')

    def test_access_create_event_page_with_non_superuser(self):
        response = self.client.get(reverse('events:create-event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, '404.html')

    def test_access_create_event_page_with_superuser(self):
        self.assertTrue(self.client.login(email=self.email))
        response = self.client.get(reverse('events:create-event'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/create-event.html')

    def test_create_event_function_as_post_request_with_valid_info(self):
        # Logs the superuser in
        self.client.login(email=self.email)

        # Verifies no Event objects exist in the test database yet.
        self.assertEqual(models.Event.objects.count(), 0)

        # Sends the event data and verifies the page redirects to the homepage
        response = self.client.post(reverse('events:create-event'), self.data)
        self.assertRedirects(response, '/')

        # Verifies that an Event object now exists in the database
        self.assertEqual(models.Event.objects.count(), 1)

    def test_create_event_function_as_post_request_with_invalid_info(self):
        # Logs the superuser in
        self.client.login(email=self.email)

        # Verifies no Event objects exist in the test database yet.
        self.assertEqual(models.Event.objects.count(), 0)

        # Change event data to be invalid
        invalid_data = self.data
        invalid_data['title'] = ''
        invalid_data['flier'] = ''

        # Sends the invalid event data and asserts that the create-event page is rendered again.
        response = self.client.post(reverse('events:create-event'), invalid_data)
        self.assertTemplateUsed(response, 'events/create-event.html')

        # Asserts that the following errors appear in the form variable that is passed
        # back to the create_event page.
        self.assertFormError(response, 'form', 'title', 'This field is required.')
        self.assertFormError(response, 'form', 'flier', 'This field is required.')

        # Verifies that no Event objects have been added to the database
        self.assertEqual(models.Event.objects.count(), 0)


class EventFormTestCase(TestCase):
    def setUp(self):
        # Creates and logs user in along with a SIG
        email = 'test@mst.edu'
        self.user = User.objects.create_superuser(email)
        self.sig = SIG.objects.create_sig(
            founder=self.user,
            chair=self.user,
            description='test',
        )

        # Sets up image variable for creating Event
        image_path = 'test_data/test_image.jpg'
        image = SimpleUploadedFile(name='test_image.jpg', content=open(image_path, 'rb').read(), content_type='image/jpeg')

        # Test data for filling the event form
        self.data = {
            'creator': self.user,
            'date_hosted': timezone.now()+timezone.timedelta(days=1),
            'date_expire': timezone.now()+timezone.timedelta(days=2),
            'hosting_sig': self.sig,
            'title': 'Test Title',
            'description': 'Here is a test description',
            'location': 'CS 207',
            'presenter': 'test',
            'cost': 10.00,
            'link': 'acm.mst.edu'
        }

        self.image_data = {'flier': image}
        super().setUp()

    def test_event_form_with_valid_data(self):
        # Adds data to EventForm and checks that all data is valid
        test_form = EventForm(self.data, self.image_data)
        self.assertTrue(test_form.is_valid())

    def test_event_form_with_no_title(self):
        test_data = self.data
        test_data.pop('title')

        test_form = EventForm(test_data, self.image_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {
            'title': ['This field is required.'],
        })

    def test_event_form_with_no_data(self):
        test_data = {}
        test_form = EventForm(test_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {
            'date_hosted': ['This field is required.', 'Please fill out the host date field.'],
            'date_expire': ['This field is required.', 'Please fill out the expiration date field.'],
            'hosting_sig': ['This field is required.'],
            'title': ['This field is required.'],
            'description': ['This field is required.'],
            'location': ['This field is required.'],
            'flier': ['This field is required.'],
        })

    def test_event_form_with_both_expiration_and_host_date_before_current_time(self):
        test_data = self.data
        test_data['date_hosted'] = datetime.min
        test_data['date_expire'] = datetime.min + timezone.timedelta(days=1)
        test_form = EventForm(test_data, self.image_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {
            'date_hosted': ['The host date shouldn\'t be before the current date!'],
            'date_expire': ['The expiration date shouldn\'t be before the current date!'],
        })

    def test_event_form_with_expiration_date_before_host_date(self):
        test_data = self.data
        test_data['date_hosted'] = datetime.min + timezone.timedelta(days=1)
        test_data['date_expire'] = datetime.min
        test_form = EventForm(test_data, self.image_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors, {
            'date_hosted': ['The host date shouldn\'t be before the current date!'],
            'date_expire': [
                'The expiration date shouldn\'t be before the current date!',
                'The expiration date shouldn\'t be before the host date!'
            ],
        })
