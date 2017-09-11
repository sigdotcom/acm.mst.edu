# Django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

# local Django
from accounts.models import User
from events.forms import EventForm
from sigs.models import SIG
from events.models import Event


class HomeViewCase(TestCase):
    """
    A class that tests whether pages function work
    and verifies the events function as expected
    """

    def setUp(self):
        """
        Sets up an testing event with test data and a super user.

        :rtype: None
        :return: None
        """
        self.user = User.objects.create_superuser('test@mst.edu')
        self.sig = SIG.objects.create_sig(
            founder=self.user,
            chair=self.user,
            description='test',
        )

        # Sets up image variable for creating Event
        image_path = 'test_data/test_image.jpg'
        self.image = SimpleUploadedFile(
            name='test_image.jpg',
            content=open(image_path, 'rb').read(),
            content_type='multipart/form-data'
        )

        # Test data for filling the event form
        self.data = {
            'creator': self.user,
            'date_hosted': timezone.now() + timezone.timedelta(days=1),
            'date_expire': timezone.now() + timezone.timedelta(days=7),
            'hosting_sig': self.sig,
            'title': 'Test Title',
            'description': 'Here is a test description',
            'location': 'CS 207',
            'presenter': 'test',
            'cost': 10.00,
            'link': 'acm.mst.edu'
        }

        self.image_data = {'flier': self.image}
        super().setUp()

    def test_view_responses(self):
        """
        Makes requests to each page of the site and asserts a 200 response code
        (or success)

        :rtype: None
        :return: None
        """
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

        response = self.client.get(reverse('home:sponsors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/sponsors.html')

        response = self.client.get(reverse('home:calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/calendar.html')

        response = self.client.get(reverse('home:media'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/media.html')

        response = self.client.get(reverse('home:officers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/officers.html')

        response = self.client.get(reverse('home:membership'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/membership.html')

        response = self.client.get(reverse('home:sigs'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/sigs.html')

    def test_number_of_fliers_that_appear_on_home_page(self):
        """
        On top of testing that the correct number of events appear on the
        homepage, this test also makes sure that the correct number of events
        get added to the database.

        :rtype: None
        :return: None
        """
        settings.MAX_HOME_FLIER_COUNT = 3
        number_of_events = 4

        # Adds 4 events to the database
        for i in range(1, number_of_events + 1):
            self.data['title'] = "Test Title {}".format(i)
            self.data['date_hosted'] = (
                timezone.now() + timezone.timedelta(days=i)
            )
            form = EventForm(self.data, self.image_data)
            if form.is_valid():
                event = form.save(commit=False)
                event.creator = self.user
                event.save()

            # Resets the image pointer to be pointing at the beginning of the
            # image file rather than the end which would cause an error with
            # the 'put' command.
            self.image.seek(0)

        # Makes sure the correct number of events were added to the database.
        self.assertEqual(len(Event.objects.all()), number_of_events)

        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

        num_events = 0
        for event in response.context['upcoming_events']:
            num_events += 1
            self.assertEqual(event.title, 'Test Title {}'.format(num_events))

        self.assertEqual(num_events, settings.MAX_HOME_FLIER_COUNT)
