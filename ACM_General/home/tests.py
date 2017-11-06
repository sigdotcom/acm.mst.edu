"""
Contains all unit tests for the Home app.
"""

# Django
from django.conf import settings
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

# local Django
from accounts.models import User
from events.forms import EventForm
from sigs.models import SIG
from events.models import Event
from products.models import Product, Transaction

# Third-party
import stripe


class HomeViewCase(TestCase):
    """
    A class that tests whether pages function work and verifies the events
    function as expected
    """

    def setUp(self):
        """
        Sets up an testing event with test data and a super user.
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
        """
        response = self.client.get(reverse('home:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')

        response = self.client.get(reverse('home:sponsors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/sponsors.html')

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

    def test_calendar_page(self):
        response = self.client.get(reverse('home:calendar'), follow=True)
        self.assertEqual(response.redirect_chain[0][1], 301)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertEqual(
            response.redirect_chain[0][0], reverse("home:index")+"#calendar"
        )

    def test_number_of_fliers_that_appear_on_home_page(self):
        """
        On top of testing that the correct number of events appear on the
        homepage, this test also makes sure that the correct number of events
        get added to the database.
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


class MembershipViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(email="testuser@mst.edu")

    def post_data(self, user=None, stripeToken=None, mem_type=None, **kwargs):
        """
        Creates a POST request to the membership url with specified paramters.

        :param user: The use to force the client to authenticate as
        :type user: :class:`~accounts.models.User`
        :param stripeToken: The tokenized credit card information to passed to
                            the view
        :type stripeToken: str
        :param mem_type: The type of membership the user is requesting.
        :type mem_type: str

        :return: The response from the view
        :rtype: :class:`django.http.response.HttpResponse`
        """
        if user:
            self.client.force_login(user)
        data = dict()
        if stripeToken:
            data["stripeToken"] = stripeToken
        if mem_type:
            data["type"] = mem_type
        return self.client.post(reverse("home:membership"), data, **kwargs)

    def check_post_response(self, status_code, **kwargs):  # pragma: no cover
        """
        Asserts that the status_code passed is equal to that returned by the
        post.

        :param int status_code: The status code to check against the response
        """
        response = self.post_data(**kwargs)
        self.assertEqual(response.status_code, status_code)

    def check_messages(self, message, **kwargs):  # pragma: no cover
        """
        Check the request context to ensure a certain message has be posted.

        :param str message: The message string to check against
        :param dict kwargs: The kwargs to pass to the ``post_data`` function
        """
        response = self.post_data(**kwargs)

        user_messages = messages.get_messages(response.wsgi_request)
        message_list = list(user_messages)

        # TODO: Change when messages are implemented
        self.assertIsNotNone(message_list)
        self.assertEqual(len(message_list), 1)
        self.assertEqual(
            str(message_list[0]),
            message
        )
        self.assertTemplateUsed(response, 'home/membership.html')

    def test_membership_page_uses_correct_template(self):
        response = self.client.get(reverse("home:membership"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/membership.html')

    def test_necessary_products_exist(self):
        membership_year = Product.objects.get(tag="membership-semester")
        self.assertIsNotNone(membership_year)

        membership_year = Product.objects.get(tag="membership-year")
        self.assertIsNotNone(membership_year)

    def test_return_404_if_user_is_not_logged_in(self):
        error_code = "Invalid User"
        response = self.post_data()
        self.assertEquals(response.status_code, 404)
        self.assertContains(response, error_code, status_code=404)

    def test_return_400_on_not_existing_token(self):
        error_code = (
            "ProductHandler view did not receive a stripe"
            " token in the POST request."
        )

        response = self.post_data(user=self.user)
        self.assertEquals(response.status_code, 400)
        self.assertContains(response, error_code, status_code=400)

    @override_settings(STRIPE_PRIV_KEY=None)
    def test_valueerror_on_invalid_stripe_api_key(self):
        with self.assertRaises(ValueError):
            self.post_data(user=self.user, stripeToken="fake_token")

    @override_settings(STRIPE_PRIV_KEY="fake_key")
    def test_400_error_on_invalid_membership_type(self):
        error_response = (
            "Invalid membership type specified."
        )
        response = self.post_data(user=self.user, stripeToken="fake_token")
        self.assertEquals(response.status_code, 400)
        self.assertContains(response, error_response, status_code=400)

        response = self.post_data(
            user=self.user, stripeToken="fake_token", mem_type="yearl"
        )
        self.assertEquals(response.status_code, 400)
        self.assertContains(response, error_response, status_code=400)

        response = self.post_data(
            user=self.user, stripeToken="fake_token", mem_type="mem"
        )
        self.assertEquals(response.status_code, 400)
        self.assertContains(response, error_response, status_code=400)

    @override_settings(STRIPE_PRIV_KEY="fake_key")
    def test_500_error_on_invalid_api_key_with_proper_initials(self):
        error_response = (
            "Unexpected error occurred. Invalid Stripe API key "
            "specified by the backend. Please contact the administrator."
        )
        # Semester
        response = self.post_data(
            user=self.user, stripeToken="fake_token", mem_type="semester",
            follow=True
        )
        self.assertEquals(response.status_code, 500)
        self.assertContains(response, error_response, status_code=500)

        # Year
        response = self.post_data(
            user=self.user, stripeToken="fake_token", mem_type="year",
            follow=True
        )
        self.assertEquals(response.status_code, 500)
        self.assertContains(response, error_response, status_code=500)

    def test_card_error_on_charge_declined(self):
        """
        See https://stripe.com/docs/testing for more information.
        """
        stripe.api_key = settings.STRIPE_PRIV_KEY
        token = "tok_chargeDeclined"

        # Semester
        response = self.post_data(
            user=self.user, stripeToken=token,
            mem_type="semester", follow=True
        )
        user_messages = messages.get_messages(response.wsgi_request)
        message_list = list(user_messages)

        # TODO: Change when messages are implemented
        self.assertIsNotNone(message_list)
        self.assertEqual(len(message_list), 1)
        self.assertEqual(
            str(message_list[0]),
            "Received a card error from the Stripe payment server."
        )
        self.assertTemplateUsed(response, 'home/membership.html')

        # Year
        response = self.post_data(
            user=self.user, stripeToken=token,
            mem_type="year", follow=True
        )
        user_messages = messages.get_messages(response.wsgi_request)
        message_list = list(user_messages)

        # TODO: Change when messages are implemented
        self.assertIsNotNone(message_list)
        self.assertEqual(len(message_list), 2)
        self.assertEqual(
            str(message_list[1]),
            "Received a card error from the Stripe payment server."
        )
        self.assertTemplateUsed(response, 'home/membership.html')

    def test_card_error_on_failed_cvc_check(self):
        stripe.api_key = settings.STRIPE_PRIV_KEY
        token = "tok_cvcCheckFail"
        message_str = "Received a card error from the Stripe payment server."

        # Semester
        response = self.post_data(
            user=self.user, stripeToken=token,
            mem_type="semester", follow=True
        )
        user_messages = messages.get_messages(response.wsgi_request)
        message_list = list(user_messages)

        # TODO: Change when messages are implemented
        self.assertIsNotNone(message_list)
        self.assertEqual(len(message_list), 1)
        self.assertEqual(
            str(message_list[0]),
            message_str
        )
        self.assertTemplateUsed(response, 'home/membership.html')

        # Year
        response = self.post_data(
            user=self.user, stripeToken=token,
            mem_type="year", follow=True
        )
        user_messages = messages.get_messages(response.wsgi_request)
        message_list = list(user_messages)

        # TODO: Change when messages are implemented
        self.assertIsNotNone(message_list)
        self.assertEqual(len(message_list), 2)
        self.assertEqual(
            str(message_list[1]),
            message_str
        )
        self.assertTemplateUsed(response, 'home/membership.html')

    def test_successful_charge_on_semester_type(self):
        stripe.api_key = settings.STRIPE_PRIV_KEY
        tag = "membership-semester"
        delta_months = 6
        message_str = "Successfully applied ACM Membership to account."
        tokens = [
            "tok_visa", "tok_visa_debit", "tok_mastercard",
            "tok_mastercard_debit", "tok_mastercard_prepaid",
        ]

        for index, token in enumerate(tokens):
            # Post
            response = self.post_data(
                user=self.user, stripeToken=token,
                mem_type="semester", follow=True
            )
            self.user.refresh_from_db()

            # Backend Check
            self.assertTrue(self.user.is_member)
            total_delta = self.user.membership_expiration - timezone.now()
            delta_days = round(total_delta.days / 28)
            self.assertEqual(index+1, int(delta_days / delta_months))

            product = Product.objects.get(tag=tag)
            transaction = Transaction.objects.get(stripe_token=token)

            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.stripe_token, token)
            self.assertEqual(transaction.cost, product.cost)
            self.assertEqual(transaction.user, self.user)
            self.assertEqual(transaction.sig, product.sig)
            self.assertEqual(transaction.category, product.category)
            self.assertEqual(transaction.description, product.description)

            # Template + Messages
            user_messages = messages.get_messages(response.wsgi_request)
            message_list = list(user_messages)
            # TODO: Change when messages are implemented
            self.assertIsNotNone(message_list)
            self.assertEqual(len(message_list), index+1)
            self.assertEqual(
                str(message_list[index]),
                message_str
            )

            self.assertTemplateUsed(response, 'home/index.html')

    def test_successful_charge_on_year_type(self):
        stripe.api_key = settings.STRIPE_PRIV_KEY
        tag = "membership-year"
        delta_months = 12
        message_str = "Successfully applied ACM Membership to account."
        tokens = [
            "tok_visa", "tok_visa_debit", "tok_mastercard",
            "tok_mastercard_debit", "tok_mastercard_prepaid",
        ]

        for index, token in enumerate(tokens):
            # Post
            response = self.post_data(
                user=self.user, stripeToken=token,
                mem_type="year", follow=True
            )
            self.user.refresh_from_db()

            # Backend Check
            self.assertTrue(self.user.is_member)
            total_delta = self.user.membership_expiration - timezone.now()
            delta_days = round(total_delta.days / 28)
            self.assertEqual(index+1, int(delta_days / delta_months))

            product = Product.objects.get(tag=tag)
            transaction = Transaction.objects.get(stripe_token=token)

            self.assertIsNotNone(transaction)
            self.assertEqual(transaction.stripe_token, token)
            self.assertEqual(transaction.cost, product.cost)
            self.assertEqual(transaction.user, self.user)
            self.assertEqual(transaction.sig, product.sig)
            self.assertEqual(transaction.category, product.category)
            self.assertEqual(transaction.description, product.description)

            # Template + Messages
            user_messages = messages.get_messages(response.wsgi_request)
            message_list = list(user_messages)
            # TODO: Change when messages are implemented
            self.assertIsNotNone(message_list)
            self.assertEqual(len(message_list), index+1)
            self.assertEqual(
                str(message_list[index]),
                message_str
            )

            self.assertTemplateUsed(response, 'home/index.html')
