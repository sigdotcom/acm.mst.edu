from django.urls import reverse
from django.test import TestCase
from accounts.models import User
from events.models import Event

# Create your tests here.
class ViewTestCase(TestCase):
    def setUp(self):
        self.user=User.objects.create_user('test@mst.edu')
        #self.event=Event.objects.create_event()
        super().setUp()

    def test_view_templates(self):
        """
        TODO: Docstring
        """
        response = self.client.get(reverse('rest_api:user-list'))
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('rest_api:user-detail', kwargs={'pk':self.user.id}))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:event-list'))
        self.assertEqual(response.status_code, 200)
        # response = self.client.get(reverse('rest_api:event-detail', kwargs={'pk':self.event.id}))
        # self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:sigs-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:transaction-list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('rest_api:category-list'))
        self.assertEqual(response.status_code, 200)



