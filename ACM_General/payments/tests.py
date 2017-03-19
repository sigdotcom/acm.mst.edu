from . import models
from django.test import TestCase

##
# NOTE: Because all of the models in the Transactions apps are so closely
#       linked, we need to test them all at once.
##

class ProductsModelsCase(TestCase):
    def setUp(self):
        super().setUp()

