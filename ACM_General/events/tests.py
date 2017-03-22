from . import models
from accounts.models import User
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

